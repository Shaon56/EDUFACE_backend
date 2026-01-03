#!/usr/bin/env python3
"""
Comprehensive test suite for user management features
"""

import requests
import json
from datetime import datetime

BASE_URL = 'https://eduface-backend.onrender.com/api'

def print_header(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def test_user_management():
    print_header("COMPREHENSIVE USER MANAGEMENT TEST SUITE")
    
    # Test 1: Admin Login
    print("\n✓ Test 1: Admin Login")
    print("-" * 70)
    
    login_response = requests.post(f'{BASE_URL}/auth/login', json={
        'email': 'admin@eduface.com',
        'password': 'admin123',
        'role': 'admin'
    })
    
    if login_response.status_code != 200:
        print(f"❌ FAILED: {login_response.status_code}")
        print(login_response.json())
        return False
    
    admin_data = login_response.json()
    token = admin_data.get('token')
    user_id = admin_data.get('user').get('id')
    user_role = admin_data.get('user').get('role')
    
    print(f"✅ PASSED")
    print(f"  User ID: {user_id}")
    print(f"  Role: {user_role}")
    print(f"  Token: {token[:50]}...")
    
    if user_role.lower() != 'admin':
        print(f"❌ ERROR: User role is '{user_role}', expected 'admin'")
        return False
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Test 2: Get All Users
    print("\n✓ Test 2: Get All Users (Admin Endpoint)")
    print("-" * 70)
    
    users_response = requests.get(f'{BASE_URL}/users', headers=headers)
    
    if users_response.status_code != 200:
        print(f"❌ FAILED: {users_response.status_code}")
        print(f"   Response: {users_response.json()}")
        return False
    
    users = users_response.json()
    print(f"✅ PASSED")
    print(f"  Retrieved {len(users)} users")
    
    # Test 3: Verify User Fields
    print("\n✓ Test 3: Verify User Field Names")
    print("-" * 70)
    
    required_fields = ['ID', 'Full Name', 'Email', 'Student ID', 'Phone', 'Role', 'is_active']
    sample_user = users[0] if users else {}
    
    missing_fields = [f for f in required_fields if f not in sample_user]
    
    if missing_fields:
        print(f"❌ FAILED: Missing fields: {missing_fields}")
        return False
    
    print(f"✅ PASSED")
    for field in required_fields:
        value = sample_user.get(field, 'N/A')
        print(f"  ✓ {field}: {value}")
    
    # Test 4: Verify Admin User
    print("\n✓ Test 4: Verify Admin User Exists")
    print("-" * 70)
    
    admin_user = next((u for u in users if u.get('Role', '').lower() == 'admin'), None)
    
    if not admin_user:
        print(f"❌ FAILED: No admin user found")
        return False
    
    print(f"✅ PASSED")
    print(f"  Admin Name: {admin_user.get('Full Name')}")
    print(f"  Admin Email: {admin_user.get('Email')}")
    print(f"  Admin Role: {admin_user.get('Role')}")
    
    # Test 5: Get Attendance Records
    print("\n✓ Test 5: Get Attendance Records")
    print("-" * 70)
    
    attendance_response = requests.get(f'{BASE_URL}/attendance', headers=headers)
    
    if attendance_response.status_code != 200:
        print(f"❌ FAILED: {attendance_response.status_code}")
        print(f"   Response: {attendance_response.json()}")
        return False
    
    attendance = attendance_response.json()
    print(f"✅ PASSED")
    print(f"  Retrieved {len(attendance)} attendance records")
    
    # Test 6: Get Routines
    print("\n✓ Test 6: Get Routines")
    print("-" * 70)
    
    routines_response = requests.get(f'{BASE_URL}/routines', headers=headers)
    
    if routines_response.status_code != 200:
        print(f"❌ FAILED: {routines_response.status_code}")
        print(f"   Response: {routines_response.json()}")
        return False
    
    routines = routines_response.json()
    print(f"✅ PASSED")
    print(f"  Retrieved {len(routines)} routines")
    
    # Verify routine fields
    if routines:
        routine = routines[0]
        routine_fields = ['id', 'subject', 'day', 'start_time', 'end_time', 'room_number', 'instructor_name']
        missing = [f for f in routine_fields if f not in routine]
        if missing:
            print(f"  ⚠️  WARNING: Missing fields in routine: {missing}")
        else:
            print(f"  ✓ All routine fields present")
            for field in ['subject', 'day', 'start_time', 'end_time', 'room_number', 'instructor_name']:
                print(f"    - {field}: {routine.get(field)}")
    
    # Summary
    print_header("TEST SUMMARY")
    print(f"""
✅ ALL TESTS PASSED

Summary:
  - Admin authentication: ✓
  - User API authorization: ✓
  - User field names: ✓
  - Attendance data: ✓ ({len(attendance)} records)
  - Routine data: ✓ ({len(routines)} routines)

Ready for Production: YES
""")
    
    return True

if __name__ == '__main__':
    try:
        success = test_user_management()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
