"""
User management routes - Using Google Sheets
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.google_sheets_db import GoogleSheetsDB
from werkzeug.security import generate_password_hash

users_bp = Blueprint('users', __name__)

@users_bp.route('', methods=['GET'])
@jwt_required()
def get_users():
    """Get all users (admin only)"""
    try:
        db = GoogleSheetsDB()
        identity = get_jwt_identity()
        # Handle both string and int identities
        user_id = int(str(identity).strip()) if identity else None
        
        if not user_id:
            return jsonify({'message': 'Invalid token'}), 401
        
        user = db.find_user_by_id(user_id)
        
        if not user or user.get('Role', 'student') != 'admin':
            return jsonify({'message': 'Unauthorized'}), 403
        
        users = db.get_all_users()
        return jsonify(users), 200
    except Exception as e:
        print(f'[ERROR] get_users: {e}')
        return jsonify({'message': f'Error: {str(e)}'}), 500

@users_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """Get specific user"""
    try:
        db = GoogleSheetsDB()
        identity = get_jwt_identity()
        current_user_id = int(str(identity).strip()) if identity else None
        
        if not current_user_id:
            return jsonify({'message': 'Invalid token'}), 401
        
        user = db.find_user_by_id(user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        # Users can only view their own profile unless they're admin
        current_user = db.find_user_by_id(current_user_id)
        if current_user.get('Role', 'student') != 'admin' and current_user_id != user_id:
            return jsonify({'message': 'Unauthorized'}), 403
        
        return jsonify(user), 200
    except Exception as e:
        print(f'[ERROR] get_user: {e}')
        return jsonify({'message': f'Error: {str(e)}'}), 500
