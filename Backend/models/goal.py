"""
Goal model
"""

from extensions import db
from datetime import datetime
from decimal import Decimal

class Goal(db.Model):
    __tablename__ = 'goals'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    goal_name = db.Column(db.String(200), nullable=False)
    target_amount = db.Column(db.Numeric(15, 2), nullable=False)
    target_date = db.Column(db.Date, nullable=False)
    current_amount = db.Column(db.Numeric(15, 2), default=Decimal('0.00'), nullable=False)
    goal_type = db.Column(db.String(50), nullable=False)  # retirement, education, house, etc.
    priority = db.Column(db.String(20), nullable=True)  # high, medium, low
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """Convert goal to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'goal_name': self.goal_name,
            'target_amount': float(self.target_amount) if self.target_amount else 0.0,
            'target_date': self.target_date.isoformat() if self.target_date else None,
            'current_amount': float(self.current_amount) if self.current_amount else 0.0,
            'goal_type': self.goal_type,
            'priority': self.priority,
            'progress_percent': float((self.current_amount / self.target_amount * 100)) if self.target_amount and self.target_amount > 0 else 0.0,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Goal {self.goal_name} - {self.target_amount}>'

