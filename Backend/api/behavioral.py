"""
Behavioral Analytics endpoints
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.behavioral_metrics import BehavioralMetrics
from services.behavioral_service import BehavioralService

behavioral_bp = Blueprint('behavioral', __name__)

@behavioral_bp.route('/metrics/<int:user_id>', methods=['GET'])
@jwt_required()
def get_behavioral_metrics(user_id):
    """Get user behavioral metrics"""
    try:
        current_user_id = get_jwt_identity()
        if current_user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        metrics = BehavioralMetrics.query.filter_by(user_id=user_id).order_by(
            BehavioralMetrics.created_at.desc()
        ).first()
        
        if not metrics:
            # Create default metrics
            metrics = BehavioralMetrics(user_id=user_id)
            db.session.add(metrics)
            db.session.commit()
        
        return jsonify(metrics.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@behavioral_bp.route('/update', methods=['POST'])
@jwt_required()
def update_behavioral_metrics():
    """Update behavioral metrics"""
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        if 'user_id' in data and data['user_id'] != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Get or create metrics
        metrics = BehavioralMetrics.query.filter_by(user_id=user_id).order_by(
            BehavioralMetrics.created_at.desc()
        ).first()
        
        if not metrics:
            metrics = BehavioralMetrics(user_id=user_id)
            db.session.add(metrics)
        
        # Update fields
        if 'portfolio_check_frequency' in data:
            metrics.portfolio_check_frequency = data['portfolio_check_frequency']
        if 'trade_volume' in data:
            metrics.trade_volume_last_week = data['trade_volume']
        if 'life_event' in data:
            metrics.major_life_event_occurred = data['life_event']
        if 'sentiment_avg' in data:
            metrics.sentiment_avg = data['sentiment_avg']
        if 'sentiment_variance' in data:
            metrics.sentiment_variance = data['sentiment_variance']
        if 'email_tone_positive_ratio' in data:
            metrics.email_tone_positive_ratio = data['email_tone_positive_ratio']
        if 'calendar_stress_events_count' in data:
            metrics.calendar_stress_events_count = data['calendar_stress_events_count']
        if 'nudge_acceptance_rate' in data:
            metrics.nudge_acceptance_rate = data['nudge_acceptance_rate']
        if 'reaction_to_market_volatility' in data:
            metrics.reaction_to_market_volatility = data['reaction_to_market_volatility']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Behavioral metrics updated successfully',
            'metrics': metrics.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@behavioral_bp.route('/insights/<int:user_id>', methods=['GET'])
@jwt_required()
def get_behavioral_insights(user_id):
    """Get behavioral insights and recommendations"""
    try:
        current_user_id = get_jwt_identity()
        if current_user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Get behavioral metrics
        metrics = BehavioralMetrics.query.filter_by(user_id=user_id).order_by(
            BehavioralMetrics.created_at.desc()
        ).first()
        
        if not metrics:
            return jsonify({
                'insights': [],
                'recommendations': [],
                'risk_adjustments': {}
            }), 200
        
        # Analyze behavioral data
        behavioral_data = metrics.to_dict()
        analysis = BehavioralService.analyze_behavioral_metrics(behavioral_data)
        
        return jsonify(analysis), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

