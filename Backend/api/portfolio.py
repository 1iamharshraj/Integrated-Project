"""
Portfolio Management endpoints
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.portfolio import Portfolio, Holding
from models.user import User
from services.portfolio_service import PortfolioService
from utils.cache import cache_get, cache_set, cache_delete
from config import Config
from decimal import Decimal

portfolio_bp = Blueprint('portfolio', __name__)

@portfolio_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_portfolio(user_id):
    """Get user's portfolio with holdings"""
    try:
        current_user_id = get_jwt_identity()
        if current_user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Check cache
        cache_key = f'portfolio:{user_id}'
        cached_result = cache_get(cache_key)
        if cached_result:
            return jsonify(cached_result), 200
        
        portfolio = Portfolio.query.filter_by(user_id=user_id).first()
        
        if not portfolio:
            # Create empty portfolio
            portfolio = Portfolio(user_id=user_id)
            db.session.add(portfolio)
            db.session.commit()
        
        # Get holdings
        holdings = Holding.query.filter_by(portfolio_id=portfolio.id).all()
        
        # Calculate performance
        performance = PortfolioService.calculate_portfolio_performance(holdings)
        
        # Update portfolio
        portfolio.total_value = Decimal(str(performance['total_value']))
        portfolio.total_gain_loss = Decimal(str(performance['total_gain_loss']))
        portfolio.total_gain_loss_percent = Decimal(str(performance['total_gain_loss_percent']))
        db.session.commit()
        
        result = {
            'portfolio': portfolio.to_dict(),
            'holdings': [h.to_dict() for h in holdings],
            'performance': performance
        }
        
        # Cache result
        cache_set(cache_key, result, Config.CACHE_TTL_PORTFOLIO)
        
        return jsonify(result), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@portfolio_bp.route('/optimize', methods=['POST'])
@jwt_required()
def optimize_portfolio():
    """Optimize portfolio allocation"""
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        if 'user_id' in data and data['user_id'] != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        required_fields = ['risk_category', 'investment_amount']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        goals = data.get('goals', [])
        
        # Optimize portfolio
        result = PortfolioService.optimize_portfolio(
            user_id,
            data['risk_category'],
            Decimal(str(data['investment_amount'])),
            goals
        )
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@portfolio_bp.route('/rebalance', methods=['POST'])
@jwt_required()
def rebalance_portfolio():
    """Rebalance portfolio"""
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        if 'user_id' in data and data['user_id'] != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        portfolio = Portfolio.query.filter_by(user_id=user_id).first()
        if not portfolio:
            return jsonify({'error': 'Portfolio not found'}), 404
        
        holdings = Holding.query.filter_by(portfolio_id=portfolio.id).all()
        target_allocation = data.get('target_allocation', {})
        
        recommendations = PortfolioService.rebalance_portfolio(
            holdings,
            target_allocation,
            float(portfolio.total_value)
        )
        
        return jsonify({
            'recommendations': recommendations,
            'current_value': float(portfolio.total_value)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@portfolio_bp.route('/performance/<int:user_id>', methods=['GET'])
@jwt_required()
def get_portfolio_performance(user_id):
    """Get portfolio performance metrics"""
    try:
        current_user_id = get_jwt_identity()
        if current_user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        portfolio = Portfolio.query.filter_by(user_id=user_id).first()
        if not portfolio:
            return jsonify({'error': 'Portfolio not found'}), 404
        
        holdings = Holding.query.filter_by(portfolio_id=portfolio.id).all()
        performance = PortfolioService.calculate_portfolio_performance(holdings)
        
        return jsonify(performance), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@portfolio_bp.route('/holdings', methods=['POST'])
@jwt_required()
def add_holding():
    """Add or update holding"""
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        required_fields = ['portfolio_id', 'asset_type', 'asset_name', 'quantity', 'current_price', 'purchase_price']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Verify portfolio belongs to user
        portfolio = Portfolio.query.filter_by(id=data['portfolio_id'], user_id=user_id).first()
        if not portfolio:
            return jsonify({'error': 'Portfolio not found'}), 404
        
        # Check if holding exists
        holding = Holding.query.filter_by(
            portfolio_id=data['portfolio_id'],
            asset_name=data['asset_name']
        ).first()
        
        if holding:
            # Update existing holding
            holding.quantity = Decimal(str(data['quantity']))
            holding.current_price = Decimal(str(data['current_price']))
            holding.purchase_price = Decimal(str(data['purchase_price']))
            holding.allocation = Decimal(str(data.get('allocation', 0)))
            holding.ai_recommendation = data.get('ai_recommendation')
        else:
            # Create new holding
            holding = Holding(
                portfolio_id=data['portfolio_id'],
                asset_type=data['asset_type'],
                asset_name=data['asset_name'],
                quantity=Decimal(str(data['quantity'])),
                current_price=Decimal(str(data['current_price'])),
                purchase_price=Decimal(str(data['purchase_price'])),
                allocation=Decimal(str(data.get('allocation', 0))),
                ai_recommendation=data.get('ai_recommendation')
            )
            db.session.add(holding)
        
        db.session.commit()
        
        # Clear cache
        cache_key = f'portfolio:{user_id}'
        cache_delete(cache_key)
        
        return jsonify({
            'message': 'Holding added/updated successfully',
            'holding': holding.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@portfolio_bp.route('/holdings/<int:holding_id>', methods=['DELETE'])
@jwt_required()
def delete_holding(holding_id):
    """Remove holding"""
    try:
        holding = Holding.query.get(holding_id)
        if not holding:
            return jsonify({'error': 'Holding not found'}), 404
        
        portfolio = Portfolio.query.get(holding.portfolio_id)
        user_id = get_jwt_identity()
        
        if portfolio.user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        db.session.delete(holding)
        db.session.commit()
        
        # Clear cache
        cache_key = f'portfolio:{portfolio.user_id}'
        cache_delete(cache_key)
        
        return jsonify({'message': 'Holding deleted successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

