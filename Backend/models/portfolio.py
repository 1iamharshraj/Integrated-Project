"""
Portfolio and Holdings models
"""

from extensions import db
from datetime import datetime
from decimal import Decimal

class Portfolio(db.Model):
    __tablename__ = 'portfolios'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    total_value = db.Column(db.Numeric(15, 2), default=Decimal('0.00'), nullable=False)
    total_gain_loss = db.Column(db.Numeric(15, 2), default=Decimal('0.00'), nullable=False)
    total_gain_loss_percent = db.Column(db.Numeric(10, 4), default=Decimal('0.0000'), nullable=False)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    holdings = db.relationship('Holding', backref='portfolio', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert portfolio to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'total_value': float(self.total_value) if self.total_value else 0.0,
            'total_gain_loss': float(self.total_gain_loss) if self.total_gain_loss else 0.0,
            'total_gain_loss_percent': float(self.total_gain_loss_percent) if self.total_gain_loss_percent else 0.0,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
            'holdings_count': self.holdings.count()
        }
    
    def __repr__(self):
        return f'<Portfolio User {self.user_id} - Value: {self.total_value}>'


class Holding(db.Model):
    __tablename__ = 'holdings'
    
    id = db.Column(db.Integer, primary_key=True)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolios.id', ondelete='CASCADE'), nullable=False, index=True)
    asset_type = db.Column(db.String(50), nullable=False)  # equity, debt, gold, international
    asset_name = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Numeric(15, 4), nullable=False)
    current_price = db.Column(db.Numeric(15, 2), nullable=False)
    purchase_price = db.Column(db.Numeric(15, 2), nullable=False)
    allocation = db.Column(db.Numeric(5, 2), nullable=False)  # Percentage allocation
    ai_recommendation = db.Column(db.String(20), nullable=True)  # buy, hold, sell
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """Convert holding to dictionary"""
        return {
            'id': self.id,
            'portfolio_id': self.portfolio_id,
            'asset_type': self.asset_type,
            'asset_name': self.asset_name,
            'quantity': float(self.quantity) if self.quantity else 0.0,
            'current_price': float(self.current_price) if self.current_price else 0.0,
            'purchase_price': float(self.purchase_price) if self.purchase_price else 0.0,
            'allocation': float(self.allocation) if self.allocation else 0.0,
            'ai_recommendation': self.ai_recommendation,
            'current_value': float(self.quantity * self.current_price) if self.quantity and self.current_price else 0.0,
            'gain_loss': float((self.current_price - self.purchase_price) * self.quantity) if self.quantity and self.current_price and self.purchase_price else 0.0,
            'gain_loss_percent': float(((self.current_price - self.purchase_price) / self.purchase_price * 100)) if self.purchase_price and self.purchase_price > 0 else 0.0,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }
    
    def __repr__(self):
        return f'<Holding {self.asset_name} - {self.quantity} units>'

