"""
Education Progress model
"""

from extensions import db
from datetime import datetime

class EducationProgress(db.Model):
    __tablename__ = 'education_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    course_id = db.Column(db.String(100), nullable=False)
    course_name = db.Column(db.String(200), nullable=False)
    progress_percent = db.Column(db.Numeric(5, 2), default=0.0, nullable=False)
    completed_modules = db.Column(db.JSON, nullable=True)  # List of completed module IDs
    last_accessed = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """Convert education progress to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'course_id': self.course_id,
            'course_name': self.course_name,
            'progress_percent': float(self.progress_percent) if self.progress_percent else 0.0,
            'completed_modules': self.completed_modules,
            'last_accessed': self.last_accessed.isoformat() if self.last_accessed else None
        }
    
    def __repr__(self):
        return f'<EducationProgress {self.course_name} - {self.progress_percent}%>'

