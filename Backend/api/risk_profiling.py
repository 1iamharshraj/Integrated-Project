"""
Risk Profiling endpoints
Combines Q-Score (40%), G-Score (35%), B-Score (25%)
Applies cultural modifiers from Project 29
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.risk_profile import RiskProfile
from models.user import User
from services.risk_profiling_service import RiskProfilingService
from utils.cache import cache_get, cache_set
from config import Config

risk_bp = Blueprint('risk_profiling', __name__)

@risk_bp.route('/questionnaire', methods=['POST'])
@jwt_required()
def submit_questionnaire():
    """Submit questionnaire answers for Q-Score calculation"""
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        if 'answers' not in data:
            return jsonify({'error': 'Missing answers field'}), 400
        
        # Calculate Q-Score
        q_score = RiskProfilingService.calculate_q_score(data['answers'])
        
        # Update or create risk profile
        risk_profile = RiskProfile.query.filter_by(user_id=user_id).first()
        if not risk_profile:
            # Calculate preliminary risk score and category from Q-Score
            preliminary_risk_score = int(q_score)
            if q_score < 30:
                preliminary_category = 'conservative'
            elif q_score < 70:
                preliminary_category = 'moderate'
            else:
                preliminary_category = 'aggressive'
            
            risk_profile = RiskProfile(
                user_id=user_id,
                risk_score=preliminary_risk_score,
                risk_category=preliminary_category
            )
            db.session.add(risk_profile)
        
        risk_profile.q_score = q_score
        risk_profile.questions_data = data['answers']
        db.session.commit()
        
        return jsonify({
            'q_score': q_score,
            'risk_score': risk_profile.risk_score if risk_profile.risk_score else None,
            'message': 'Questionnaire submitted successfully'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@risk_bp.route('/demographics', methods=['POST'])
@jwt_required()
def submit_demographics():
    """Submit demographic data for cultural modifiers"""
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        # Calculate cultural modifiers
        cultural_modifiers = RiskProfilingService.calculate_cultural_modifiers(data)
        
        # Update risk profile
        risk_profile = RiskProfile.query.filter_by(user_id=user_id).first()
        if not risk_profile:
            # Create with default values if doesn't exist
            risk_profile = RiskProfile(
                user_id=user_id,
                risk_score=50,  # Default moderate score
                risk_category='moderate'  # Default category
            )
            db.session.add(risk_profile)
        
        risk_profile.regional_factor = cultural_modifiers['regional_factor']
        risk_profile.demographic_factor = cultural_modifiers['demographic_factor']
        risk_profile.tradition_factor = cultural_modifiers['tradition_factor']
        risk_profile.cultural_modifier = cultural_modifiers['cultural_modifier']
        db.session.commit()
        
        return jsonify(cultural_modifiers), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@risk_bp.route('/life-events', methods=['POST'])
@jwt_required()
def submit_life_events():
    """Submit life events data"""
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        life_events = data.get('life_events', [])
        
        # Calculate life event impact
        # Major life events reduce risk tolerance
        life_event_impact = 1.0
        if life_events:
            # Each major life event reduces risk tolerance by 5%
            major_events = [e for e in life_events if e.get('impact', 'low') == 'high']
            life_event_impact = 1.0 - (len(major_events) * 0.05)
            life_event_impact = max(0.7, life_event_impact)  # Minimum 0.7
        
        # Update risk profile
        risk_profile = RiskProfile.query.filter_by(user_id=user_id).first()
        if not risk_profile:
            # Create with default values if doesn't exist
            risk_profile = RiskProfile(
                user_id=user_id,
                risk_score=50,  # Default moderate score
                risk_category='moderate'  # Default category
            )
            db.session.add(risk_profile)
        
        # Apply life event impact to existing risk score
        if risk_profile.risk_score:
            adjusted_score = risk_profile.risk_score * life_event_impact
            risk_profile.risk_score = int(adjusted_score)
        
        # Store in AI analysis
        if not risk_profile.ai_analysis:
            risk_profile.ai_analysis = {}
        risk_profile.ai_analysis['life_events'] = life_events
        risk_profile.ai_analysis['life_event_impact'] = life_event_impact
        
        db.session.commit()
        
        return jsonify({
            'life_event_impact': life_event_impact,
            'adjusted_risk_score': risk_profile.risk_score
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@risk_bp.route('/behavioral', methods=['POST'])
@jwt_required()
def submit_behavioral():
    """Submit behavioral assessment data for B-Score"""
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        behavioral_data = data.get('behavioral_data', {})
        
        # Calculate B-Score
        b_score = RiskProfilingService.calculate_b_score(behavioral_data)
        
        # Update risk profile
        risk_profile = RiskProfile.query.filter_by(user_id=user_id).first()
        if not risk_profile:
            # Create with default values if doesn't exist
            risk_profile = RiskProfile(
                user_id=user_id,
                risk_score=50,  # Default moderate score
                risk_category='moderate'  # Default category
            )
            db.session.add(risk_profile)
        
        risk_profile.b_score = b_score
        if not risk_profile.ai_analysis:
            risk_profile.ai_analysis = {}
        risk_profile.ai_analysis['behavioral_data'] = behavioral_data
        risk_profile.ai_analysis['behavioral_insights'] = {
            'portfolio_check_frequency': behavioral_data.get('portfolio_check_frequency'),
            'turnover_rate': behavioral_data.get('portfolio_turnover_rate'),
            'life_event': behavioral_data.get('major_life_event_occurred', False)
        }
        
        db.session.commit()
        
        return jsonify({
            'b_score': b_score,
            'behavioral_insights': risk_profile.ai_analysis.get('behavioral_insights', {})
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@risk_bp.route('/calculate', methods=['POST'])
@jwt_required()
def calculate_risk_profile():
    """Calculate comprehensive risk profile"""
    try:
        user_id = get_jwt_identity()
        
        # Check cache
        cache_key = f'risk_profile:{user_id}'
        cached_result = cache_get(cache_key)
        if cached_result:
            return jsonify(cached_result), 200
        
        # Get risk profile
        risk_profile = RiskProfile.query.filter_by(user_id=user_id).first()
        if not risk_profile:
            return jsonify({'error': 'Risk profile not found. Please complete questionnaire first.'}), 404
        
        # Get scores
        q_score = risk_profile.q_score or 50.0
        g_score = risk_profile.g_score or 50.0
        b_score = risk_profile.b_score or 50.0
        
        # Get cultural modifiers
        cultural_modifiers = {
            'cultural_modifier': risk_profile.cultural_modifier or 1.0,
            'regional_factor': risk_profile.regional_factor or 1.0,
            'demographic_factor': risk_profile.demographic_factor or 1.0,
            'tradition_factor': risk_profile.tradition_factor or 1.0
        }
        
        # Calculate comprehensive risk profile
        result = RiskProfilingService.calculate_comprehensive_risk_profile(
            q_score, g_score, b_score, cultural_modifiers
        )
        
        # Update risk profile
        risk_profile.risk_score = result['risk_score']
        risk_profile.risk_category = result['risk_category']
        risk_profile.confidence = result['confidence']
        risk_profile.ai_analysis = result.get('factors', {})
        db.session.commit()
        
        # Cache result
        cache_set(cache_key, result, Config.CACHE_TTL_RISK_PROFILE)
        
        return jsonify(result), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@risk_bp.route('/profile/<int:user_id>', methods=['GET'])
@jwt_required()
def get_risk_profile(user_id):
    """Get user's risk profile"""
    try:
        current_user_id = get_jwt_identity()
        
        # Users can only view their own profile unless admin
        if current_user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        risk_profile = RiskProfile.query.filter_by(user_id=user_id).first()
        
        if not risk_profile:
            return jsonify({'error': 'Risk profile not found'}), 404
        
        return jsonify(risk_profile.to_dict()), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

