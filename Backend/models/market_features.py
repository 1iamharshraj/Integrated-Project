"""
Market Features model (Project 29)
"""

from extensions import db
from datetime import datetime

class MarketFeatures(db.Model):
    __tablename__ = 'market_features'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, index=True)
    symbol = db.Column(db.String(50), nullable=False, index=True)
    technical_indicators = db.Column(db.JSON, nullable=True)  # SMA, EMA, RSI, MACD, Bollinger Bands, ATR, OBV, etc.
    market_sentiment = db.Column(db.JSON, nullable=True)  # Sentiment scores and metrics
    volatility_metrics = db.Column(db.JSON, nullable=True)  # Volatility calculations
    volume_analysis = db.Column(db.JSON, nullable=True)  # Volume ratios and analysis
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    __table_args__ = (
        db.UniqueConstraint('date', 'symbol', name='unique_date_symbol'),
    )
    
    def to_dict(self):
        """Convert market features to dictionary"""
        return {
            'id': self.id,
            'date': self.date.isoformat() if self.date else None,
            'symbol': self.symbol,
            'technical_indicators': self.technical_indicators,
            'market_sentiment': self.market_sentiment,
            'volatility_metrics': self.volatility_metrics,
            'volume_analysis': self.volume_analysis,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<MarketFeatures {self.symbol} - {self.date}>'

