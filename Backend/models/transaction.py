"""
Transaction model
"""

from extensions import db
from datetime import datetime
from decimal import Decimal

class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolios.id', ondelete='SET NULL'), nullable=True, index=True)
    type = db.Column(db.String(20), nullable=False)  # buy, sell, deposit, withdrawal
    asset_name = db.Column(db.String(200), nullable=True)
    quantity = db.Column(db.Numeric(15, 4), nullable=True)
    price = db.Column(db.Numeric(15, 2), nullable=True)
    amount = db.Column(db.Numeric(15, 2), nullable=False)
    status = db.Column(db.String(20), default='pending', nullable=False)  # pending, completed, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    def to_dict(self):
        """Convert transaction to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'portfolio_id': self.portfolio_id,
            'type': self.type,
            'asset_name': self.asset_name,
            'quantity': float(self.quantity) if self.quantity else None,
            'price': float(self.price) if self.price else None,
            'amount': float(self.amount) if self.amount else 0.0,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Transaction {self.type} - {self.amount}>'

