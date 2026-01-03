#!/usr/bin/env python3
"""
Detailed test to verify user field names and API response
"""

import requests
import json

BASE_URL = 'https://eduface-backend.onrender.com/api'

def test_user_fields():
    print("="*70)
    print("Testing User Field Names")
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
    print(f"   Token: {token[:50]}...")
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Step 2: Get all users and check field names
    print("\n2. Get All Users and Check Field Names...")
    users_response = requests.get(f'{BASE_URL}/users', headers=headers)
    
    print(f"   Response Status: {users_response.status_code}")
    print(f"   Response Headers: {dict(users_response.headers)}")
    
    if users_response.status_code == 200:
        users = users_response.json()
        print(f"✅ Retrieved {len(users)} users")
        print("\nDetailed User Data:")
        print("-" * 70)
        
        for i, user in enumerate(users[:2], 1):  # Show first 2 users
            print(f"\nUser {i}:")
            print(f"  ID: {user.get('ID')}")
            print(f"  Full Name: {user.get('Full Name')} {'✅' if user.get('Full Name') else '❌ MISSING'}")
            print(f"  Email: {user.get('Email')} {'✅' if user.get('Email') else '❌ MISSING'}")
            print(f"  Student ID: {user.get('Student ID')} {'✅' if user.get('Student ID') else '❌ MISSING'}")
            print(f"  Phone: {user.get('Phone')} {'✅' if user.get('Phone') else '❌ MISSING'}")
            print(f"  Role: {user.get('Role')} {'✅' if user.get('Role') else '❌ MISSING'}")
            print(f"  is_active: {user.get('is_active')} {'✅' if user.get('is_active') else '❌ MISSING'}")
            
            # Show all keys
            print(f"  All Keys: {list(user.keys())}")
            print(f"\n  Raw JSON:")
            print(f"  {json.dumps(user, indent=4)}")
    else:
        print(f"❌ Failed to get users: {users_response.status_code}")
        print(f"   Response: {users_response.text}")
    
    print("\n" + "="*70)

if __name__ == '__main__':
    test_user_fields()
