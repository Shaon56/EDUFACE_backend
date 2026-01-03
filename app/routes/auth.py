"""
Authentication routes - Using Google Sheets
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.google_sheets_db import GoogleSheetsDB
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new student"""
    try:
        db = GoogleSheetsDB()
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['full_name', 'student_id', 'email', 'contact_number', 'password']
        if not all(field in data for field in required_fields):
            return jsonify({'message': 'Missing required fields'}), 400
        
        # Check if user already exists
        existing_user = db.find_user_by_email(data['email'])
        if existing_user:
            return jsonify({'message': 'Email already registered'}), 400
        
        # Check if student ID already exists
        users = db.get_all_users()
        if any(str(u.get('Student ID', '')) == str(data['student_id']) for u in users):
            return jsonify({'message': 'Student ID already exists'}), 400
        
        # Create new user
        user_data = {
            'name': data['full_name'],
            'student_id': data['student_id'],
            'email': data['email'],
            'password': generate_password_hash(data['password']),
            'phone': data.get('contact_number', ''),
            'role': 'student',
            'section': data.get('section', '')
        }
        
        new_user = db.add_user(user_data)
        
        if new_user:
            return jsonify({
                'message': 'Registration successful',
                'user': new_user
            }), 201
        else:
            return jsonify({'message': 'Failed to create user'}), 500
            
    except Exception as e:
        print(f'[REGISTER ERROR] {e}')
        return jsonify({'message': f'Registration failed: {str(e)}'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        db = GoogleSheetsDB()
        data = request.get_json()
        print(f'[LOGIN] Login attempt with email: {data.get("email")}, role: {data.get("role")}')
        
        # Validate required fields
        if not data.get('email') or not data.get('password'):
            print('[LOGIN ERROR] Missing email or password')
            return jsonify({'message': 'Missing email or password'}), 400
        
        # Find user
        user = db.find_user_by_email(data['email'])
        print(f'[LOGIN] User found: {user is not None}')
        
        if not user:
            print('[LOGIN ERROR] User not found')
            return jsonify({'message': 'Invalid email or password'}), 401
        
        # Check password
        if not check_password_hash(user.get('Password', ''), data['password']):
            print('[LOGIN ERROR] Invalid password')
            return jsonify({'message': 'Invalid email or password'}), 401
        
        if user.get('is_active', 'true').lower() == 'false':
            print('[LOGIN ERROR] User account is disabled')
            return jsonify({'message': 'User account is disabled'}), 403
        
        # Check role match if specified
        if 'role' in data and data['role'] != user.get('Role', 'student'):
            print(f'[LOGIN ERROR] Role mismatch. User role: {user.get("Role")}, requested: {data["role"]}')
            return jsonify({'message': 'Invalid role'}), 401
        
        # Create JWT token
        user_id = user.get('ID', '')
        print(f'[LOGIN] Creating token for user ID: {user_id}')
        access_token = create_access_token(identity=str(user_id))
        
        print(f'[LOGIN] Login successful for user {user_id}')
        return jsonify({
            'message': 'Login successful',
            'token': access_token,
            'user': {
                'id': user.get('ID'),
                'full_name': user.get('Full Name'),
                'email': user.get('Email'),
                'student_id': user.get('Student ID'),
                'role': user.get('Role', 'student')
            }
        }), 200
        
    except Exception as e:
        print(f'[LOGIN ERROR] {e}')
        return jsonify({'message': f'Login failed: {str(e)}'}), 500

@auth_bp.route('/verify-token', methods=['GET'])
@jwt_required()
def verify_token():
    """Verify if token is valid"""
    db = GoogleSheetsDB()
    user_id = int(get_jwt_identity())
    user = db.find_user_by_id(user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    return jsonify({
        'valid': True,
        'user': {
            'id': user.get('ID'),
            'name': user.get('Full Name'),
            'email': user.get('Email'),
            'role': user.get('Role', 'student')
        }
    }), 200
