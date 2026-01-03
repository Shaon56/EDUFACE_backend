#!/usr/bin/env python3
"""
Test users endpoint
"""

import requests
import json

BASE_URL = 'https://eduface-backend.onrender.com/api'

# First, login to get a token
print("1. Testing login...")
login_response = requests.post(f'{BASE_URL}/auth/login', json={
    'email': 'admin@eduface.com',
    'password': 'admin123',
    'role': 'admin'
})

if login_response.status_code == 200:
    data = login_response.json()
    token = data.get('token')
    print(f"✅ Login successful")
    print(f"Token: {token[:50]}...")
    
    # Now test users endpoint
    print("\n2. Testing /api/users endpoint...")
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    users_response = requests.get(f'{BASE_URL}/users', headers=headers)
    print(f"Status Code: {users_response.status_code}")
    print(f"Response Headers: {dict(users_response.headers)}")
    print(f"Response Text: {users_response.text[:500]}")
    
    if users_response.status_code == 200:
        try:
            users_data = users_response.json()
            print(f"✅ Users endpoint working!")
            print(f"Total users: {len(users_data)}")
            for user in users_data[:3]:  # Show first 3
                print(f"  - {user.get('Full Name')} ({user.get('Email')})")
        except json.JSONDecodeError as e:
            print(f"❌ JSON decode error: {e}")
    else:
        print(f"❌ Error: {users_response.text}")
else:
    print(f"❌ Login failed: {login_response.status_code}")
    print(f"Response: {login_response.text}")
