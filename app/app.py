from flask import Flask
from flask_cors import CORS
from .config import *
from .api.routes import api_bp




def create_app():
    app = Flask(__name__)
    
    config_app(app)
    register_blueprints(app)

    return app

def register_blueprints(app):
    app.register_blueprint(api_bp)

def config_app(app):
    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    config_class = {
    'production': ProductionConfig,
    'testing': TestingConfig,
    }.get(app.config.get('FLASK_DEBUG', 1), DevelopmentConfig)
    app.config.from_object(config_class)





