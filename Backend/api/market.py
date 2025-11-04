"""
Market Data endpoints
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from extensions import db
from models.market_features import MarketFeatures
from models.sentiment_analysis import SentimentAnalysis
from services.market_service import MarketService
from services.sentiment_service import SentimentService
from utils.cache import cache_get, cache_set
from config import Config
from datetime import datetime, date, timedelta

market_bp = Blueprint('market', __name__)

@market_bp.route('/indices', methods=['GET'])
@jwt_required()
def get_indices():
    """Get current market indices"""
    try:
        # Check cache
        cache_key = 'market:indices'
        cached_result = cache_get(cache_key)
        if cached_result:
            return jsonify(cached_result), 200
        
        indices = MarketService.get_market_indices()
        
        # Cache result
        cache_set(cache_key, indices, Config.CACHE_TTL_MARKET)
        
        return jsonify(indices), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@market_bp.route('/sentiment', methods=['GET'])
@jwt_required()
def get_market_sentiment():
    """Get aggregated market sentiment from news analysis"""
    try:
        # Check cache
        cache_key = 'market:sentiment'
        cached_result = cache_get(cache_key)
        if cached_result:
            return jsonify(cached_result), 200
        
        # Get today's sentiment records
        today = date.today()
        sentiment_records = SentimentAnalysis.query.filter_by(date=today).all()
        
        if not sentiment_records:
            # Return default if no records
            result = {
                'overall_sentiment': 'neutral',
                'confidence': 0.5,
                'news_count': 0,
                'daily_sentiment_score': 0.0
            }
        else:
            # Aggregate sentiment
            records_dict = [r.to_dict() for r in sentiment_records]
            result = SentimentService.aggregate_daily_sentiment(records_dict)
        
        # Cache result
        cache_set(cache_key, result, Config.CACHE_TTL_MARKET)
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@market_bp.route('/predictions/<symbol>', methods=['GET'])
@jwt_required()
def get_predictions(symbol):
    """Get market predictions for a symbol"""
    try:
        # Check cache
        cache_key = f'market:predictions:{symbol}'
        cached_result = cache_get(cache_key)
        if cached_result:
            return jsonify(cached_result), 200
        
        predictions = MarketService.get_market_predictions(symbol)
        
        # Cache result
        cache_set(cache_key, predictions, Config.CACHE_TTL_MARKET)
        
        return jsonify(predictions), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@market_bp.route('/news', methods=['GET'])
@jwt_required()
def get_news():
    """Get latest financial news"""
    try:
        # Get recent sentiment analysis records (these contain news)
        limit = request.args.get('limit', 20, type=int)
        sentiment_records = SentimentAnalysis.query.order_by(
            SentimentAnalysis.created_at.desc()
        ).limit(limit).all()
        
        news = [{
            'title': r.title,
            'url': r.source_url,
            'sentiment': r.sentiment,
            'confidence': float(r.confidence_score),
            'date': r.date.isoformat() if r.date else None
        } for r in sentiment_records]
        
        return jsonify({
            'news': news,
            'count': len(news)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@market_bp.route('/technical-indicators/<symbol>', methods=['GET'])
@jwt_required()
def get_technical_indicators(symbol):
    """Get technical indicators for a symbol"""
    try:
        # Check cache
        cache_key = f'market:technical:{symbol}'
        cached_result = cache_get(cache_key)
        if cached_result:
            return jsonify(cached_result), 200
        
        indicators = MarketService.get_technical_indicators(symbol)
        
        # Store in database
        today = date.today()
        market_feature = MarketFeatures.query.filter_by(
            date=today,
            symbol=symbol
        ).first()
        
        if market_feature:
            market_feature.technical_indicators = indicators['technical_indicators']
            market_feature.market_sentiment = indicators['market_sentiment']
            market_feature.volatility_metrics = indicators['volatility_metrics']
            market_feature.volume_analysis = indicators['volume_analysis']
        else:
            market_feature = MarketFeatures(
                date=today,
                symbol=symbol,
                technical_indicators=indicators['technical_indicators'],
                market_sentiment=indicators['market_sentiment'],
                volatility_metrics=indicators['volatility_metrics'],
                volume_analysis=indicators['volume_analysis']
            )
            db.session.add(market_feature)
        
        db.session.commit()
        
        # Cache result
        cache_set(cache_key, indicators, Config.CACHE_TTL_MARKET)
        
        return jsonify(indicators), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

