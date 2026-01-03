#!/usr/bin/env python3
"""
Test user management API response
"""

import requests
import json

BASE_URL = 'https://eduface-backend.onrender.com/api'

def test_users_api():
    print("="*70)
    print("Testing User Management API")
    print("="*70)
    
    # Step 1: Login as admin
    print("\n1. Admin Login...")
    login_response = requests.post(f'{BASE_URL}/auth/login', json={
        'email': 'admin@eduface.com',
        'password': 'admin123',
        'role': 'admin'
    })
    
    admin_data = login_response.json()
    token = admin_data.get('token')
    print(f"✅ Admin login successful")
    
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
        print("\nUser Data (First User):")
        print("-" * 70)
        
        if users:
            user = users[0]
            print(f"\nUser 1:")
            for key, value in user.items():
                print(f"  {key}: {value}")
            
            print("\n✅ Frontend Field Mapping Check:")
            print(f"  Full Name: {user.get('Full Name', 'MISSING')} ✅" if user.get('Full Name') else f"  Full Name: MISSING ❌")
            print(f"  Student ID: {user.get('Student ID', 'MISSING')} ✅" if user.get('Student ID') else f"  Student ID: MISSING ❌")
            print(f"  Email: {user.get('Email', 'MISSING')} ✅" if user.get('Email') else f"  Email: MISSING ❌")
            print(f"  Phone: {user.get('Phone', 'MISSING')} ✅" if user.get('Phone') else f"  Phone: MISSING ❌")
            print(f"  Status (is_active): {user.get('is_active', 'MISSING')} ✅" if user.get('is_active') is not None else f"  Status: MISSING ❌")
    else:
        print(f"❌ Failed to get users: {users_response.status_code}")
        print(users_response.text)
    
    print("\n" + "="*70)

if __name__ == '__main__':
    test_users_api()
