"""
KYC Document model
"""

from extensions import db
from datetime import datetime
import json

class KYCDocument(db.Model):
    __tablename__ = 'kyc_documents'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    document_type = db.Column(db.String(50), nullable=False)  # aadhaar, pan, bank_statement
    document_url = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(20), default='pending', nullable=False)  # pending, verified, rejected
    verification_data = db.Column(db.JSON, nullable=True)  # JSONB in PostgreSQL
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """Convert KYC document to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'document_type': self.document_type,
            'document_url': self.document_url,
            'status': self.status,
            'verification_data': self.verification_data,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<KYCDocument {self.document_type} - {self.status}>'

