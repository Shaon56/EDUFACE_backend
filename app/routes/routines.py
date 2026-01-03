"""
Routine management routes - Using Google Sheets
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.google_sheets_db import GoogleSheetsDB

routines_bp = Blueprint('routines', __name__)

@routines_bp.route('', methods=['GET'])
@jwt_required()
def get_routines():
    """Get all routines or filter by day"""
    try:
        db = GoogleSheetsDB()
        day = request.args.get('day')
        
        all_routines = db.get_all_routines()
        
        if day:
            routines = [r for r in all_routines if r.get('day', '').lower() == day.lower()]
        else:
            routines = all_routines
        
        return jsonify(routines), 200
    except Exception as e:
        print(f'[ERROR] get_routines: {e}')
        return jsonify({'message': f'Error: {str(e)}'}), 500

@routines_bp.route('/<int:routine_id>', methods=['GET'])
@jwt_required()
def get_routine(routine_id):
    """Get specific routine"""
    db = GoogleSheetsDB()
    all_routines = db.get_all_routines()
    
    for routine in all_routines:
        if str(routine.get('ID', '')) == str(routine_id):
            return jsonify(routine), 200
    
    return jsonify({'message': 'Routine not found'}), 404

@routines_bp.route('', methods=['POST'])
@jwt_required()
def create_routine():
    """Create new routine (admin only)"""
    try:
        db = GoogleSheetsDB()
        print('[DEBUG] Creating routine endpoint called')
        
        identity = get_jwt_identity()
        user_id = int(str(identity).strip()) if identity else None
        print(f'[DEBUG] User ID from JWT: {user_id}')
        
        if not user_id:
            print('[ERROR] Invalid token - no user ID')
            return jsonify({'message': 'Invalid token'}), 401
        
        user = db.find_user_by_id(user_id)
        print(f'[DEBUG] User found: {user is not None}')
        
        if not user:
            print('[ERROR] User not found in database')
            return jsonify({'message': 'User not found'}), 404
            
        if user.get('Role', 'student') != 'admin':
            print(f'[ERROR] User role is {user.get("Role")}, not admin')
            return jsonify({'message': f'Unauthorized. Your role is {user.get("Role")}, only admins can create routines'}), 403
        
        data = request.get_json()
        print(f'[DEBUG] Request data: {data}')
        
        # Validate required fields
        required_fields = ['subject', 'day', 'startTime', 'endTime', 'room']
        missing = [f for f in required_fields if f not in data]
        if missing:
            print(f'[ERROR] Missing fields: {missing}')
            return jsonify({'message': f'Missing required fields: {", ".join(missing)}'}), 400
        
        print('[DEBUG] Creating routine in Google Sheets')
        routine_data = {
            'user_id': user_id,
            'subject': data['subject'],
            'day': data['day'],
            'start_time': data['startTime'],
            'end_time': data['endTime'],
            'room_number': data['room'],
            'instructor_name': data.get('instructor', '')
        }
        
        new_routine = db.add_routine(routine_data)
        
        if new_routine:
            print(f'[SUCCESS] Routine created with ID: {new_routine.get("id")}')
            return jsonify({'message': 'Routine created', 'routine': new_routine}), 201
        else:
            return jsonify({'message': 'Failed to create routine'}), 500
        
    except Exception as e:
        error_msg = str(e)
        print(f'[ERROR] Exception in create_routine: {error_msg}')
        import traceback
        traceback.print_exc()
        return jsonify({'message': f'Error: {error_msg}'}), 500

@routines_bp.route('/<int:routine_id>', methods=['DELETE'])
@jwt_required()
def delete_routine(routine_id):
    """Delete routine (admin only)"""
    try:
        db = GoogleSheetsDB()
        identity = get_jwt_identity()
        user_id = int(str(identity).strip()) if identity else None
        
        if not user_id:
            return jsonify({'message': 'Invalid token'}), 401
        
        user = db.find_user_by_id(user_id)
        
        if not user or user.get('Role', 'student') != 'admin':
            return jsonify({'message': 'Unauthorized'}), 403
        
        success = db.delete_routine(routine_id)
        
        if success:
            return jsonify({'message': 'Routine deleted'}), 200
        else:
            return jsonify({'message': 'Routine not found'}), 404
    except Exception as e:
        print(f'[ERROR] delete_routine: {e}')
        return jsonify({'message': f'Error: {str(e)}'}), 500
