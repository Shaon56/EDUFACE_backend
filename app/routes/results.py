"""
Results routes - Using Google Sheets
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.google_sheets_db import GoogleSheetsDB
from datetime import datetime

results_bp = Blueprint('results', __name__)

@results_bp.route('', methods=['GET'])
@jwt_required()
def get_results():
    """Get results"""
    try:
        db = GoogleSheetsDB()
        identity = get_jwt_identity()
        user_id = int(str(identity).strip()) if identity else None
        
        if not user_id:
            return jsonify({'message': 'Invalid token'}), 401
        
        user = db.find_user_by_id(user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        if user.get('Role', 'student') == 'admin':
            # Admin can see all results
            results = db.get_all_results()
        else:
            # Students can only see their own
            results = db.get_user_results(user_id)
        
        return jsonify(results), 200
    except Exception as e:
        print(f'[ERROR] get_results: {e}')
        return jsonify({'message': f'Error: {str(e)}'}), 500

@results_bp.route('/student/<int:student_id>', methods=['GET'])
@jwt_required()
def get_student_results(student_id):
    """Get results for specific student (admin only)"""
    try:
        db = GoogleSheetsDB()
        identity = get_jwt_identity()
        user_id = int(str(identity).strip()) if identity else None
        
        if not user_id:
            return jsonify({'message': 'Invalid token'}), 401
        
        user = db.find_user_by_id(user_id)
        
        if not user or user.get('Role', 'student') != 'admin':
            return jsonify({'message': 'Unauthorized'}), 403
        
        results = db.get_user_results(student_id)
        
        return jsonify(results), 200
    except Exception as e:
        print(f'[ERROR] get_student_results: {e}')
        return jsonify({'message': f'Error: {str(e)}'}), 500

@results_bp.route('', methods=['POST'])
@jwt_required()
def create_result():
    """Create result (admin only)"""
    try:
        db = GoogleSheetsDB()
        identity = get_jwt_identity()
        user_id = int(str(identity).strip()) if identity else None
        
        if not user_id:
            return jsonify({'message': 'Invalid token'}), 401
        
        user = db.find_user_by_id(user_id)
        
        if not user or user.get('Role', 'student') != 'admin':
            return jsonify({'message': 'Unauthorized'}), 403
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['user_id', 'subject', 'marks', 'grade']
        if not all(field in data for field in required_fields):
            return jsonify({'message': 'Missing required fields'}), 400
    
    # Check if student exists
    student = db.find_user_by_id(data['user_id'])
    if not student:
        return jsonify({'message': 'Student not found'}), 404
    
    # Create result record
    result_data = {
        'user_id': data['user_id'],
        'subject': data['subject'],
        'marks': data['marks'],
        'grade': data['grade'],
        'date': data.get('date', datetime.now().strftime('%Y-%m-%d'))
    }
    
    new_result = db.add_result(result_data)
    
    if new_result:
        return jsonify({'message': 'Result uploaded', 'result': new_result}), 201
    else:
        return jsonify({'message': 'Failed to upload result'}), 500
    
    db.session.commit()
    
    return jsonify({'message': 'Result updated', 'result': result.to_dict()}), 200

@results_bp.route('/<int:result_id>', methods=['DELETE'])
@jwt_required()
def delete_result(result_id):
    """Delete result (admin only)"""
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if not user or user.role != 'admin':
        return jsonify({'message': 'Unauthorized'}), 403
    
    result = Result.query.get(result_id)
    
    if not result:
        return jsonify({'message': 'Result not found'}), 404
    
    db.session.delete(result)
    db.session.commit()
    
    return jsonify({'message': 'Result deleted'}), 200
