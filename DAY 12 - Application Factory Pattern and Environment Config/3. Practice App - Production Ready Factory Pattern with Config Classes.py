# Day 12 Practice App: Application Factory & Config Switching
import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BaseConfig:
    SECRET_KEY = 'masterclass-secret'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev_factory.db'

def create_app(config_object=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config_object)
    
    db.init_app(app)
    
    @app.route('/info')
    def app_info():
        return jsonify({
            "debug": app.config['DEBUG'],
            "database_uri": app.config['SQLALCHEMY_DATABASE_URI']
        })
        
    return app

if __name__ == '__main__':
    app = create_app()
    app.run()
