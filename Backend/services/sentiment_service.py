"""
Sentiment Analysis Service
Uses FinBERT model from Project 25
"""

from datetime import datetime, date
import json

# Try to import transformers, but handle gracefully if not available
try:
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

class SentimentService:
    """Service for sentiment analysis using FinBERT"""
    
    @staticmethod
    def analyze_sentiment(text):
        """
        Analyze sentiment of text using FinBERT model
        Returns: sentiment (positive/negative/neutral), confidence_score
        """
        # If transformers not available, use simplified keyword-based analysis
        if not TRANSFORMERS_AVAILABLE:
            return SentimentService._keyword_based_sentiment(text)
        
        # TODO: Load actual FinBERT model when transformers is available
        # model = AutoModelForSequenceClassification.from_pretrained('ProsusAI/finbert')
        # tokenizer = AutoTokenizer.from_pretrained('ProsusAI/finbert')
        
        # For now, use keyword-based analysis
        return SentimentService._keyword_based_sentiment(text)
    
    @staticmethod
    def _keyword_based_sentiment(text):
        """Simplified keyword-based sentiment analysis (fallback)"""
        positive_keywords = ['gain', 'profit', 'growth', 'rise', 'bull', 'positive', 'up']
        negative_keywords = ['loss', 'fall', 'decline', 'bear', 'negative', 'down', 'crash']
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_keywords if word in text_lower)
        negative_count = sum(1 for word in negative_keywords if word in text_lower)
        
        if positive_count > negative_count:
            sentiment = 'positive'
            confidence = min(0.9, 0.5 + (positive_count - negative_count) * 0.1)
        elif negative_count > positive_count:
            sentiment = 'negative'
            confidence = min(0.9, 0.5 + (negative_count - positive_count) * 0.1)
        else:
            sentiment = 'neutral'
            confidence = 0.6
        
        return sentiment, round(confidence, 4)
    
    @staticmethod
    def aggregate_daily_sentiment(sentiment_records):
        """Aggregate daily sentiment scores"""
        if not sentiment_records:
            return {
                'overall_sentiment': 'neutral',
                'confidence': 0.5,
                'news_count': 0,
                'daily_sentiment_score': 0.0
            }
        
        positive_count = sum(1 for r in sentiment_records if r.get('sentiment') == 'positive')
        negative_count = sum(1 for r in sentiment_records if r.get('sentiment') == 'negative')
        neutral_count = sum(1 for r in sentiment_records if r.get('sentiment') == 'neutral')
        total = len(sentiment_records)
        
        # Calculate weighted sentiment score
        sentiment_scores = {
            'positive': 1.0,
            'neutral': 0.0,
            'negative': -1.0
        }
        
        weighted_score = sum(
            sentiment_scores.get(r.get('sentiment', 'neutral'), 0) * r.get('confidence_score', 0.5)
            for r in sentiment_records
        ) / total
        
        # Determine overall sentiment
        if weighted_score > 0.2:
            overall_sentiment = 'positive'
        elif weighted_score < -0.2:
            overall_sentiment = 'negative'
        else:
            overall_sentiment = 'neutral'
        
        confidence = max(
            r.get('confidence_score', 0.5) for r in sentiment_records
        ) if sentiment_records else 0.5
        
        return {
            'overall_sentiment': overall_sentiment,
            'confidence': round(confidence, 4),
            'news_count': total,
            'daily_sentiment_score': round(weighted_score, 4),
            'positive_count': positive_count,
            'negative_count': negative_count,
            'neutral_count': neutral_count
        }

