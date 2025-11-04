"""
Behavioral Metrics model (Project 29)
"""

from extensions import db
from datetime import datetime
from decimal import Decimal

class BehavioralMetrics(db.Model):
    __tablename__ = 'behavioral_metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    portfolio_check_frequency = db.Column(db.Integer, default=0, nullable=False)  # Times per day
    portfolio_turnover_rate = db.Column(db.Numeric(10, 4), default=Decimal('0.0000'), nullable=False)
    trade_volume_last_week = db.Column(db.Numeric(15, 2), default=Decimal('0.00'), nullable=False)
    major_life_event_occurred = db.Column(db.Boolean, default=False, nullable=False)
    sentiment_avg = db.Column(db.Numeric(5, 4), nullable=True)  # Average sentiment score
    sentiment_variance = db.Column(db.Numeric(10, 6), nullable=True)  # Sentiment variance
    email_tone_positive_ratio = db.Column(db.Numeric(5, 4), nullable=True)  # 0-1 ratio
    calendar_stress_events_count = db.Column(db.Integer, default=0, nullable=False)
    nudge_acceptance_rate = db.Column(db.Numeric(5, 4), nullable=True)  # 0-1 ratio
    reaction_to_market_volatility = db.Column(db.String(50), nullable=True)  # conservative, moderate, aggressive
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """Convert behavioral metrics to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'portfolio_check_frequency': self.portfolio_check_frequency,
            'portfolio_turnover_rate': float(self.portfolio_turnover_rate) if self.portfolio_turnover_rate else 0.0,
            'trade_volume_last_week': float(self.trade_volume_last_week) if self.trade_volume_last_week else 0.0,
            'major_life_event_occurred': self.major_life_event_occurred,
            'sentiment_avg': float(self.sentiment_avg) if self.sentiment_avg else None,
            'sentiment_variance': float(self.sentiment_variance) if self.sentiment_variance else None,
            'email_tone_positive_ratio': float(self.email_tone_positive_ratio) if self.email_tone_positive_ratio else None,
            'calendar_stress_events_count': self.calendar_stress_events_count,
            'nudge_acceptance_rate': float(self.nudge_acceptance_rate) if self.nudge_acceptance_rate else None,
            'reaction_to_market_volatility': self.reaction_to_market_volatility,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<BehavioralMetrics User {self.user_id}>'

