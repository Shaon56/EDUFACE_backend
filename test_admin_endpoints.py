#!/usr/bin/env python3
"""
Test admin endpoints to verify fixes
"""

import requests
import json

BASE_URL = 'https://eduface-backend.onrender.com/api'

def test_admin_operations():
    print("="*70)
    print("Testing Admin Operations")
    print("="*70)
    
    # Step 1: Login as admin
    print("\n1. Admin Login...")
    login_response = requests.post(f'{BASE_URL}/auth/login', json={
        'email': 'admin@eduface.com',
        'password': 'admin123',
        'role': 'admin'
    })
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.text}")
        return
    
    admin_data = login_response.json()
    token = admin_data.get('token')
    print(f"✅ Admin login successful")
    print(f"   Token: {token[:50]}...")
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Step 2: Get all users
    print("\n2. Get All Users...")
    users_response = requests.get(f'{BASE_URL}/users', headers=headers)
    
    if users_response.status_code == 200:
        users = users_response.json()
        print(f"✅ Retrieved {len(users)} users")
        for user in users[:3]:
            print(f"   - {user.get('Full Name')} ({user.get('Email')})")
    else:
        print(f"❌ Failed to get users: {users_response.status_code}")
        print(f"   Response: {users_response.text}")
    
    # Step 3: Get all routines
    print("\n3. Get All Routines...")
    routines_response = requests.get(f'{BASE_URL}/routines', headers=headers)
    
    if routines_response.status_code == 200:
        routines = routines_response.json()
        print(f"✅ Retrieved {len(routines)} routines")
        for routine in routines[:3]:
            print(f"   - {routine.get('Subject')} on {routine.get('Day')} at {routine.get('Start Time')}")
    else:
        print(f"❌ Failed to get routines: {routines_response.status_code}")
        print(f"   Response: {routines_response.text}")
    
    # Step 4: Create a new routine
    print("\n4. Create New Routine...")
    routine_data = {
        'subject': 'Physics',
        'day': 'Wednesday',
        'startTime': '11:00',
        'endTime': '12:30',
        'room': '307',
        'instructor': 'Dr. Physics'
    }
    
    create_routine_response = requests.post(
        f'{BASE_URL}/routines',
        headers=headers,
        json=routine_data
    )
    
    if create_routine_response.status_code == 201:
        routine = create_routine_response.json()
        print(f"✅ Routine created successfully")
        print(f"   Response: {routine}")
    else:
        print(f"❌ Failed to create routine: {create_routine_response.status_code}")
        print(f"   Response: {create_routine_response.text}")
    
    print("\n" + "="*70)
    print("Test completed!")
    print("="*70)

if __name__ == '__main__':
    test_admin_operations()
