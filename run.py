"""
EDUFACE Backend - Flask Application
Main entry point for the Flask server
"""


"""
from flask import Flask
from flask_cors import CORS
from app import db, jwt
import os
from datetime import timedelta

def create_app(config_name='development'):
    
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///eduface.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # JWT Configuration
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)
    
    # CORS Configuration
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    
    # Handle JWT errors
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        return False
    
    # Register blueprints
    from app.routes import auth_bp, users_bp, routines_bp, attendance_bp, results_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(routines_bp, url_prefix='/api/routines')
    app.register_blueprint(attendance_bp, url_prefix='/api/attendance')
    app.register_blueprint(results_bp, url_prefix='/api/results')
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health():
        return {'status': 'ok', 'message': 'EDUFACE backend is running'}, 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
"""

import os
from datetime import timedelta
from flask import Flask
from flask_cors import CORS

from app import db, jwt
from app.routes import (
    auth_bp,
    users_bp,
    routines_bp,
    attendance_bp,
    results_bp
)


def create_app():
    app = Flask(__name__)

    # -------------------- Configuration --------------------
    app.config["SECRET_KEY"] = os.environ.get(
        "SECRET_KEY", "your-secret-key-change-in-production"
    )

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "sqlite:///eduface.db"
    )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # -------------------- JWT --------------------
    app.config["JWT_SECRET_KEY"] = os.environ.get(
        "JWT_SECRET_KEY", "jwt-secret-key-change-in-production"
    )

    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=30)

    # -------------------- CORS --------------------
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # -------------------- Extensions --------------------
    db.init_app(app)
    jwt.init_app(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        return False

    # -------------------- Blueprints --------------------
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(routines_bp, url_prefix="/api/routines")
    app.register_blueprint(attendance_bp, url_prefix="/api/attendance")
    app.register_blueprint(results_bp, url_prefix="/api/results")

    # -------------------- Database --------------------
    with app.app_context():
        db.create_all()

    # -------------------- Health --------------------
    @app.route("/api/health")
    def health():
        return {"status": "ok", "message": "EDUFACE backend is running"}, 200

    return app


# ✅ Gunicorn entry point
app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
