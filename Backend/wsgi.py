"""
WSGI entry point for production deployment
"""

from app import create_app
from config import config
import os

# Get environment from environment variable
env = os.environ.get('FLASK_ENV', 'production')
app = create_app(config.get(env, config['default']))

if __name__ == "__main__":
    app.run()

