"""
AI Insights endpoints
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.ai_insight import AIInsight
from models.portfolio import Portfolio, Holding
from models.behavioral_metrics import BehavioralMetrics
from services.ai_service import AIService
from services.market_service import MarketService

ai_bp = Blueprint('ai_insights', __name__)

@ai_bp.route('/insights/<int:user_id>', methods=['GET'])
@jwt_required()
def get_ai_insights(user_id):
    """Get AI-generated insights for user"""
    try:
        current_user_id = get_jwt_identity()
        if current_user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Get unread insights
        unread_only = request.args.get('unread_only', 'false').lower() == 'true'
        limit = request.args.get('limit', 20, type=int)
        
        query = AIInsight.query.filter_by(user_id=user_id)
        if unread_only:
            query = query.filter_by(is_read=False)
        
        insights = query.order_by(AIInsight.created_at.desc()).limit(limit).all()
        
        # If no insights exist, generate some sample insights
        if not insights:
            sample_insights = AIService.generate_ai_insights(user_id, 'portfolio_recommendation')
            for insight_data in sample_insights:
                insight = AIInsight(
                    user_id=user_id,
                    type=insight_data['type'],
                    title=insight_data['title'],
                    content=insight_data['content'],
                    data=insight_data.get('data'),
                    is_read=False
                )
                db.session.add(insight)
            db.session.commit()
            
            # Query again to get the newly created insights
            query = AIInsight.query.filter_by(user_id=user_id)
            if unread_only:
                query = query.filter_by(is_read=False)
            insights = query.order_by(AIInsight.created_at.desc()).limit(limit).all()
        
        return jsonify({
            'insights': [i.to_dict() for i in insights],
            'count': len(insights)
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/recommendations', methods=['POST'])
@jwt_required()
def get_recommendations():
    """Get personalized investment recommendations"""
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        if 'user_id' in data and data['user_id'] != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Get portfolio data
        portfolio = Portfolio.query.filter_by(user_id=user_id).first()
        portfolio_data = {}
        if portfolio:
            holdings = Holding.query.filter_by(portfolio_id=portfolio.id).all()
            portfolio_data = {
                'total_value': float(portfolio.total_value),
                'holdings_count': len(holdings),
                'holdings': [h.to_dict() for h in holdings]
            }
        
        # Get behavioral data
        behavioral_metrics = BehavioralMetrics.query.filter_by(user_id=user_id).order_by(
            BehavioralMetrics.created_at.desc()
        ).first()
        behavioral_data = behavioral_metrics.to_dict() if behavioral_metrics else {}
        
        # Get market data
        market_data = {
            'sentiment': MarketService.get_market_indices(),
            'predictions': {}
        }
        
        # Generate recommendations
        recommendations = AIService.generate_portfolio_recommendations(
            user_id,
            portfolio_data,
            market_data,
            behavioral_data
        )
        
        return jsonify(recommendations), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/predictions/<symbol>', methods=['GET'])
@jwt_required()
def get_ai_predictions(symbol):
    """Get AI predictions for specific symbol"""
    try:
        predictions = MarketService.get_market_predictions(symbol)
        
        return jsonify(predictions), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_bp.route('/insights/mark-read/<int:insight_id>', methods=['POST'])
@jwt_required()
def mark_insight_read(insight_id):
    """Mark insight as read"""
    try:
        insight = AIInsight.query.get(insight_id)
        if not insight:
            return jsonify({
                'error': 'Insight not found',
                'message': f'No insight found with ID {insight_id}. Use GET /api/ai/insights/{get_jwt_identity()} to see available insights.',
                'hint': 'Make sure you have insights first. They are auto-generated when you call GET /api/ai/insights/{user_id}'
            }), 404
        
        user_id = get_jwt_identity()
        if insight.user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        insight.is_read = True
        db.session.commit()
        
        return jsonify({
            'message': 'Insight marked as read',
            'insight': insight.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

