"""
News & Web Scraping endpoints (Project 25)
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from extensions import db
from models.sentiment_analysis import SentimentAnalysis
from services.sentiment_service import SentimentService
from datetime import datetime, date

news_bp = Blueprint('news', __name__)

@news_bp.route('/scrape', methods=['POST'])
@jwt_required()
def scrape_news():
    """Trigger web scraping from Moneycontrol.com"""
    try:
        # Placeholder for web scraping functionality
        # In production, this would:
        # 1. Scrape Moneycontrol.com for financial news
        # 2. Extract article titles, content, URLs
        # 3. Analyze sentiment using FinBERT
        # 4. Store in SentimentAnalysis table
        
        # Example: Simulate scraping and sentiment analysis
        sample_articles = [
            {
                'title': 'Market gains on positive economic data',
                'url': 'https://www.moneycontrol.com/news1',
                'content': 'Stock markets surged today following positive economic indicators...',
                'date': date.today()
            },
            {
                'title': 'Investors cautious ahead of RBI policy',
                'url': 'https://www.moneycontrol.com/news2',
                'content': 'Investors remained cautious as they await RBI policy announcement...',
                'date': date.today()
            }
        ]
        
        scraped_count = 0
        
        for article in sample_articles:
            # Analyze sentiment
            sentiment, confidence = SentimentService.analyze_sentiment(
                article['content']
            )
            
            # Check if already exists
            existing = SentimentAnalysis.query.filter_by(
                source_url=article['url'],
                date=article['date']
            ).first()
            
            if not existing:
                sentiment_record = SentimentAnalysis(
                    date=article['date'],
                    source_url=article['url'],
                    title=article['title'],
                    content=article['content'],
                    sentiment=sentiment,
                    confidence_score=confidence
                )
                db.session.add(sentiment_record)
                scraped_count += 1
        
        db.session.commit()
        
        return jsonify({
            'message': f'Scraped {scraped_count} new articles',
            'articles_analyzed': scraped_count
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@news_bp.route('/sentiment', methods=['GET'])
@jwt_required()
def get_sentiment_analysis():
    """Get sentiment analysis results"""
    try:
        # Get recent sentiment records
        limit = request.args.get('limit', 50, type=int)
        date_filter = request.args.get('date')
        
        query = SentimentAnalysis.query
        
        if date_filter:
            try:
                filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
                query = query.filter_by(date=filter_date)
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        sentiment_records = query.order_by(
            SentimentAnalysis.created_at.desc()
        ).limit(limit).all()
        
        # Aggregate sentiment
        if sentiment_records:
            records_dict = [r.to_dict() for r in sentiment_records]
            aggregated = SentimentService.aggregate_daily_sentiment(records_dict)
        else:
            aggregated = {
                'overall_sentiment': 'neutral',
                'confidence': 0.5,
                'news_count': 0,
                'daily_sentiment_score': 0.0
            }
        
        return jsonify({
            'sentiment': aggregated['overall_sentiment'],
            'confidence': aggregated['confidence'],
            'news_count': aggregated['news_count'],
            'daily_sentiment_score': aggregated['daily_sentiment_score'],
            'articles': [r.to_dict() for r in sentiment_records[:10]]  # Return top 10
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

