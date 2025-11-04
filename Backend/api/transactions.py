"""
Transactions endpoints
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.transaction import Transaction
from decimal import Decimal

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_transactions(user_id):
    """Get user's transaction history"""
    try:
        current_user_id = get_jwt_identity()
        if current_user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Filtering
        transaction_type = request.args.get('type')
        status = request.args.get('status')
        
        query = Transaction.query.filter_by(user_id=user_id)
        
        if transaction_type:
            query = query.filter_by(type=transaction_type)
        if status:
            query = query.filter_by(status=status)
        
        transactions = query.order_by(Transaction.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'transactions': [t.to_dict() for t in transactions.items],
            'total': transactions.total,
            'page': page,
            'per_page': per_page,
            'pages': transactions.pages
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@transactions_bp.route('', methods=['POST'])
@jwt_required()
def create_transaction():
    """Create new transaction"""
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        if 'user_id' in data and data['user_id'] != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        required_fields = ['type', 'amount']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Validate transaction type
        valid_types = ['buy', 'sell', 'deposit', 'withdrawal']
        if data['type'] not in valid_types:
            return jsonify({'error': f'Invalid transaction type. Must be one of: {valid_types}'}), 400
        
        transaction = Transaction(
            user_id=user_id,
            portfolio_id=data.get('portfolio_id'),
            type=data['type'],
            asset_name=data.get('asset_name'),
            quantity=Decimal(str(data['quantity'])) if data.get('quantity') else None,
            price=Decimal(str(data['price'])) if data.get('price') else None,
            amount=Decimal(str(data['amount'])),
            status=data.get('status', 'pending')
        )
        
        db.session.add(transaction)
        db.session.commit()
        
        return jsonify({
            'message': 'Transaction created successfully',
            'transaction': transaction.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@transactions_bp.route('/<int:transaction_id>/status', methods=['PUT'])
@jwt_required()
def update_transaction_status(transaction_id):
    """Update transaction status"""
    try:
        transaction = Transaction.query.get(transaction_id)
        if not transaction:
            return jsonify({'error': 'Transaction not found'}), 404
        
        user_id = get_jwt_identity()
        if transaction.user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        data = request.get_json()
        
        if 'status' in data:
            valid_statuses = ['pending', 'completed', 'failed']
            if data['status'] not in valid_statuses:
                return jsonify({'error': f'Invalid status. Must be one of: {valid_statuses}'}), 400
            transaction.status = data['status']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Transaction status updated',
            'transaction': transaction.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

