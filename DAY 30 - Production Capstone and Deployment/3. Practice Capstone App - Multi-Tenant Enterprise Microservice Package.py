# Day 30 Practice App: Production Capstone Microservice Entrypoint
from flask import Flask, jsonify

def create_production_app():
    app = Flask(__name__)
    
    @app.route('/healthz')
    def health_check():
        return jsonify({
            "status": "UP",
            "environment": "production",
            "microservice": "Masterclass Capstone API",
            "version": "3.0.0"
        }), 200
        
    return app

app = create_production_app()

if __name__ == '__main__':
    app.run()
