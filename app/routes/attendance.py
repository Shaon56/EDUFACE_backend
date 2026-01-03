"""
Attendance routes - Using Google Sheets
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.google_sheets_db import GoogleSheetsDB
from datetime import datetime

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('', methods=['GET'])
@jwt_required()
def get_attendance():
    """Get attendance records"""
    try:
        db = GoogleSheetsDB()
        identity = get_jwt_identity()
        user_id = int(str(identity).strip()) if identity else None
        
        if not user_id:
            return jsonify({'message': 'Invalid token'}), 401
        
        user = db.find_user_by_id(user_id)
        
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        subject = request.args.get('subject')
        
        if user.get('Role', 'student') == 'admin':
            # Admin can see all attendance
            records = db.get_all_attendance()
            if subject:
                records = [r for r in records if r.get('Subject', '').lower() == subject.lower()]
        else:
            # Students can only see their own
            records = db.get_user_attendance(user_id)
            if subject:
                records = [r for r in records if r.get('Subject', '').lower() == subject.lower()]
        
        return jsonify(records), 200
    except Exception as e:
        print(f'[ERROR] get_attendance: {e}')
        return jsonify({'message': f'Error: {str(e)}'}), 500

@attendance_bp.route('', methods=['POST'])
@jwt_required()
def create_attendance():
    """Create attendance record (admin only)"""
    try:
        db = GoogleSheetsDB()
        identity = get_jwt_identity()
        user_id = int(str(identity).strip()) if identity else None
        
        if not user_id:
            return jsonify({'message': 'Invalid token'}), 401
        
        user = db.find_user_by_id(user_id)
        
        # Only admin can manually create records
        if not user or user.get('Role', 'student') != 'admin':
            return jsonify({'message': 'Unauthorized'}), 403
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['user_id', 'subject', 'status']
        if not all(field in data for field in required_fields):
            return jsonify({'message': 'Missing required fields'}), 400
        
        # Check if student exists
        student = db.find_user_by_id(data['user_id'])
        if not student:
            return jsonify({'message': 'Student not found'}), 404
        
        # Create attendance record
        attendance_data = {
            'user_id': data['user_id'],
        'subject': data['subject'],
        'status': data['status'],
        'date': data.get('date', datetime.now().strftime('%Y-%m-%d'))
    }
    
    new_attendance = db.add_attendance(attendance_data)
    
    if new_attendance:
        return jsonify({'message': 'Attendance recorded', 'attendance': new_attendance}), 201
    else:
        return jsonify({'message': 'Failed to record attendance'}), 500
    
    data = request.get_json()
    
    # Update fields
    if 'status' in data:
        attendance.status = data['status']
    if 'date' in data:
        attendance.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    
    db.session.commit()
    
    return jsonify({'message': 'Attendance updated', 'attendance': attendance.to_dict()}), 200

@attendance_bp.route('/<int:attendance_id>', methods=['DELETE'])
@jwt_required()
def delete_attendance(attendance_id):
    """Delete attendance record (admin only)"""
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    if not user or user.role != 'admin':
        return jsonify({'message': 'Unauthorized'}), 403
    
    attendance = Attendance.query.get(attendance_id)
    
    if not attendance:
        return jsonify({'message': 'Attendance record not found'}), 404
    
    db.session.delete(attendance)
    db.session.commit()
    
    return jsonify({'message': 'Attendance deleted'}), 200
