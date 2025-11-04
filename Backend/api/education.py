"""
Education endpoints
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.education import EducationProgress
from decimal import Decimal

education_bp = Blueprint('education', __name__)

@education_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_education_progress(user_id):
    """Get user's education progress"""
    try:
        current_user_id = get_jwt_identity()
        if current_user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        progress_records = EducationProgress.query.filter_by(user_id=user_id).order_by(
            EducationProgress.last_accessed.desc()
        ).all()
        
        return jsonify({
            'progress': [p.to_dict() for p in progress_records],
            'count': len(progress_records)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@education_bp.route('/progress', methods=['POST'])
@jwt_required()
def update_education_progress():
    """Update education progress"""
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        if 'user_id' in data and data['user_id'] != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        required_fields = ['course_id', 'course_name']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Get or create progress record
        progress = EducationProgress.query.filter_by(
            user_id=user_id,
            course_id=data['course_id']
        ).first()
        
        if not progress:
            progress = EducationProgress(
                user_id=user_id,
                course_id=data['course_id'],
                course_name=data['course_name'],
                progress_percent=Decimal('0.00')
            )
            db.session.add(progress)
        
        # Update progress
        if 'progress_percent' in data:
            progress.progress_percent = Decimal(str(data['progress_percent']))
        
        if 'completed_modules' in data:
            progress.completed_modules = data['completed_modules']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Education progress updated successfully',
            'progress': progress.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

