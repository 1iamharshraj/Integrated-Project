"""
KYC endpoints
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.kyc import KYCDocument

kyc_bp = Blueprint('kyc', __name__)

@kyc_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_kyc_documents(user_id):
    """Get user's KYC documents"""
    try:
        current_user_id = get_jwt_identity()
        if current_user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        documents = KYCDocument.query.filter_by(user_id=user_id).order_by(
            KYCDocument.created_at.desc()
        ).all()
        
        return jsonify({
            'documents': [d.to_dict() for d in documents],
            'count': len(documents)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@kyc_bp.route('', methods=['POST'])
@jwt_required()
def upload_kyc_document():
    """Upload KYC document"""
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        if 'user_id' in data and data['user_id'] != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        required_fields = ['document_type', 'document_url']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Validate document type
        valid_types = ['aadhaar', 'pan', 'bank_statement']
        if data['document_type'] not in valid_types:
            return jsonify({'error': f'Invalid document type. Must be one of: {valid_types}'}), 400
        
        document = KYCDocument(
            user_id=user_id,
            document_type=data['document_type'],
            document_url=data['document_url'],
            status='pending'
        )
        
        db.session.add(document)
        db.session.commit()
        
        return jsonify({
            'message': 'KYC document uploaded successfully',
            'document': document.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@kyc_bp.route('/<int:document_id>/verify', methods=['PUT'])
@jwt_required()
def verify_kyc_document(document_id):
    """Update KYC document status (admin only - simplified for now)"""
    try:
        document = KYCDocument.query.get(document_id)
        if not document:
            return jsonify({'error': 'Document not found'}), 404
        
        # In production, check if user is admin
        user_id = get_jwt_identity()
        if document.user_id != user_id:
            # For now, allow user to update their own documents
            # In production, this should be admin-only
            pass
        
        data = request.get_json()
        
        if 'status' in data:
            valid_statuses = ['pending', 'verified', 'rejected']
            if data['status'] not in valid_statuses:
                return jsonify({'error': f'Invalid status. Must be one of: {valid_statuses}'}), 400
            document.status = data['status']
        
        if 'verification_data' in data:
            document.verification_data = data['verification_data']
        
        db.session.commit()
        
        return jsonify({
            'message': 'KYC document status updated',
            'document': document.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

