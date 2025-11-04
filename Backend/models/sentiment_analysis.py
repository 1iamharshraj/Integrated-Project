"""
Sentiment Analysis model (Project 25)
"""

from extensions import db
from datetime import datetime
from decimal import Decimal

class SentimentAnalysis(db.Model):
    __tablename__ = 'sentiment_analysis'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, index=True)
    source_url = db.Column(db.String(500), nullable=False)
    title = db.Column(db.String(500), nullable=False)
    content = db.Column(db.Text, nullable=True)
    sentiment = db.Column(db.String(20), nullable=False)  # positive, negative, neutral
    confidence_score = db.Column(db.Numeric(5, 4), nullable=False)  # 0-1
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    def to_dict(self):
        """Convert sentiment analysis to dictionary"""
        return {
            'id': self.id,
            'date': self.date.isoformat() if self.date else None,
            'source_url': self.source_url,
            'title': self.title,
            'content': self.content[:500] if self.content else None,  # Truncate for API response
            'sentiment': self.sentiment,
            'confidence_score': float(self.confidence_score) if self.confidence_score else 0.0,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<SentimentAnalysis {self.sentiment} - {self.confidence_score}>'

