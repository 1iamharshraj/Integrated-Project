"""
Risk Profile model
"""

from extensions import db
from datetime import datetime

class RiskProfile(db.Model):
    __tablename__ = 'risk_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    risk_score = db.Column(db.Integer, nullable=False)  # 0-100
    risk_category = db.Column(db.String(50), nullable=False)  # conservative, moderate, aggressive
    questions_data = db.Column(db.JSON, nullable=True)  # Q-Score related data
    ai_analysis = db.Column(db.JSON, nullable=True)  # G-Score, B-Score, cultural modifiers
    q_score = db.Column(db.Float, nullable=True)  # Questionnaire score (40%)
    g_score = db.Column(db.Float, nullable=True)  # Goal-based score (35%)
    b_score = db.Column(db.Float, nullable=True)  # Behavioral score (25%)
    cultural_modifier = db.Column(db.Float, nullable=True)  # Cultural adjustment factor
    regional_factor = db.Column(db.Float, nullable=True)
    demographic_factor = db.Column(db.Float, nullable=True)
    tradition_factor = db.Column(db.Float, nullable=True)
    confidence = db.Column(db.Float, nullable=True)  # Confidence score 0-1
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """Convert risk profile to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'risk_score': self.risk_score,
            'risk_category': self.risk_category,
            'q_score': self.q_score,
            'g_score': self.g_score,
            'b_score': self.b_score,
            'cultural_modifier': self.cultural_modifier,
            'regional_factor': self.regional_factor,
            'demographic_factor': self.demographic_factor,
            'tradition_factor': self.tradition_factor,
            'confidence': self.confidence,
            'questions_data': self.questions_data,
            'ai_analysis': self.ai_analysis,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<RiskProfile {self.risk_category} - Score: {self.risk_score}>'

