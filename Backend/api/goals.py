"""
Goals & Planning endpoints
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.goal import Goal
from models.user import User
from decimal import Decimal
from datetime import datetime, date

goals_bp = Blueprint('goals', __name__)

@goals_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_goals(user_id):
    """Get user's financial goals"""
    try:
        current_user_id = get_jwt_identity()
        if current_user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        goals = Goal.query.filter_by(user_id=user_id).order_by(Goal.created_at.desc()).all()
        
        return jsonify({
            'goals': [g.to_dict() for g in goals],
            'count': len(goals)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@goals_bp.route('/create', methods=['POST'])
@jwt_required()
def create_goal():
    """Create a new goal"""
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        if 'user_id' in data and data['user_id'] != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        required_fields = ['goal_name', 'target_amount', 'target_date', 'goal_type']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Parse target date
        target_date = datetime.strptime(data['target_date'], '%Y-%m-%d').date()
        
        goal = Goal(
            user_id=user_id,
            goal_name=data['goal_name'],
            target_amount=Decimal(str(data['target_amount'])),
            target_date=target_date,
            current_amount=Decimal(str(data.get('current_amount', 0))),
            goal_type=data['goal_type'],
            priority=data.get('priority', 'medium')
        )
        
        db.session.add(goal)
        db.session.commit()
        
        return jsonify({
            'message': 'Goal created successfully',
            'goal': goal.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@goals_bp.route('/<int:goal_id>', methods=['PUT'])
@jwt_required()
def update_goal(goal_id):
    """Update goal"""
    try:
        goal = Goal.query.get(goal_id)
        if not goal:
            return jsonify({'error': 'Goal not found'}), 404
        
        user_id = get_jwt_identity()
        if goal.user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        data = request.get_json()
        
        if 'goal_name' in data:
            goal.goal_name = data['goal_name']
        if 'target_amount' in data:
            goal.target_amount = Decimal(str(data['target_amount']))
        if 'target_date' in data:
            goal.target_date = datetime.strptime(data['target_date'], '%Y-%m-%d').date()
        if 'current_amount' in data:
            goal.current_amount = Decimal(str(data['current_amount']))
        if 'goal_type' in data:
            goal.goal_type = data['goal_type']
        if 'priority' in data:
            goal.priority = data['priority']
        
        goal.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Goal updated successfully',
            'goal': goal.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@goals_bp.route('/<int:goal_id>', methods=['DELETE'])
@jwt_required()
def delete_goal(goal_id):
    """Delete goal"""
    try:
        goal = Goal.query.get(goal_id)
        if not goal:
            return jsonify({'error': 'Goal not found'}), 404
        
        user_id = get_jwt_identity()
        if goal.user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        db.session.delete(goal)
        db.session.commit()
        
        return jsonify({'message': 'Goal deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@goals_bp.route('/progress/<int:user_id>', methods=['GET'])
@jwt_required()
def get_goal_progress(user_id):
    """Get goal progress tracking with Monte Carlo simulations"""
    try:
        current_user_id = get_jwt_identity()
        if current_user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        goals = Goal.query.filter_by(user_id=user_id).all()
        
        # Calculate achievement probability using Monte Carlo simulation (simplified)
        # In production, this would run actual Monte Carlo simulations
        goals_data = []
        overall_probability = 0.0
        
        for goal in goals:
            years_to_goal = (goal.target_date - date.today()).days / 365.25
            if years_to_goal <= 0:
                achievement_prob = 1.0 if goal.current_amount >= goal.target_amount else 0.0
            else:
                # Simplified calculation - in production, use actual Monte Carlo
                required_annual_return = (
                    (goal.target_amount - goal.current_amount) / goal.current_amount / years_to_goal
                ) if goal.current_amount > 0 else 0.15
                
                # Assume 85%+ target achievement probability
                if required_annual_return <= 0.10:
                    achievement_prob = 0.90
                elif required_annual_return <= 0.15:
                    achievement_prob = 0.85
                else:
                    achievement_prob = max(0.50, 0.90 - (required_annual_return - 0.15) * 2)
            
            goal_dict = goal.to_dict()
            goal_dict['achievement_probability'] = round(achievement_prob, 4)
            goals_data.append(goal_dict)
            
            overall_probability += achievement_prob
        
        if goals_data:
            overall_probability = overall_probability / len(goals_data)
        
        # Recommended allocations (simplified)
        recommended_allocations = {
            'equity': 0.50,
            'debt': 0.30,
            'gold': 0.10,
            'international': 0.10
        }
        
        return jsonify({
            'goals': goals_data,
            'achievement_probability': round(overall_probability, 4),
            'recommended_allocations': recommended_allocations
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

