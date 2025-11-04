"""
ZeTheta FinArcade - Flask REST API Backend
Main application entry point
"""

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from extensions import db, migrate, redis_client
import logging
from logging.handlers import RotatingFileHandler
import os

def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    jwt = JWTManager(app)
    
    # JWT blacklist handling
    from api.auth import blacklisted_tokens
    
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload['jti']
        return jti in blacklisted_tokens
    
    # Initialize Redis if available
    if app.config.get('REDIS_URL'):
        try:
            redis_client.init_app(app)
        except Exception as e:
            app.logger.warning(f"Redis not available: {e}")
    
    # Register blueprints
    from api.auth import auth_bp
    from api.risk_profiling import risk_bp
    from api.portfolio import portfolio_bp
    from api.market import market_bp
    from api.behavioral import behavioral_bp
    from api.goals import goals_bp
    from api.ai_insights import ai_bp
    from api.kyc import kyc_bp
    from api.transactions import transactions_bp
    from api.education import education_bp
    from api.news import news_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(risk_bp, url_prefix='/api/risk-profiling')
    app.register_blueprint(portfolio_bp, url_prefix='/api/portfolio')
    app.register_blueprint(market_bp, url_prefix='/api/market')
    app.register_blueprint(behavioral_bp, url_prefix='/api/behavioral')
    app.register_blueprint(goals_bp, url_prefix='/api/goals')
    app.register_blueprint(ai_bp, url_prefix='/api/ai')
    app.register_blueprint(kyc_bp, url_prefix='/api/kyc')
    app.register_blueprint(transactions_bp, url_prefix='/api/transactions')
    app.register_blueprint(education_bp, url_prefix='/api/education')
    app.register_blueprint(news_bp, url_prefix='/api/news')
    
    # Setup logging
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/finarcade.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('ZeTheta FinArcade startup')
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {'error': 'Internal server error'}, 500
    
    @app.route('/')
    def health_check():
        return {'status': 'healthy', 'service': 'ZeTheta FinArcade API'}, 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)

