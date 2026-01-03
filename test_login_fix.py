#!/usr/bin/env python
import requests
import json

BASE_URL = 'https://eduface-backend.onrender.com/api'

print("=" * 60)
print("TESTING EDUFACE API")
print("=" * 60)

# Test 1: Login with Student Account
print("\n1. Testing Student Login (Shaon Mondal):")
student_login = {
    'email': 'mondal33-1627@diu.edu.bd',
    'password': 'test123'  # or whatever password was set
}

try:
    response = requests.post(f'{BASE_URL}/auth/login', json=student_login)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response: {json.dumps(data, indent=2)}")
    
    if response.ok:
        print(f"\n✅ Student Login Successful!")
        print(f"   - User Name: {data['user'].get('full_name', 'MISSING')}")
        print(f"   - User ID: {data['user'].get('id')}")
        print(f"   - Role: {data['user'].get('role')}")
        print(f"   - Token Received: {'token' in data}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: Login with Admin Account
print("\n" + "=" * 60)
print("2. Testing Admin Login:")
admin_login = {
    'email': 'admin@eduface.com',
    'password': 'admin123',
    'role': 'admin'
}

try:
    response = requests.post(f'{BASE_URL}/auth/login', json=admin_login)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response: {json.dumps(data, indent=2)}")
    
    if response.ok:
        print(f"\n✅ Admin Login Successful!")
        print(f"   - User Name: {data['user'].get('full_name', 'MISSING')}")
        print(f"   - User ID: {data['user'].get('id')}")
        print(f"   - Role: {data['user'].get('role')}")
        print(f"   - Token Received: {'token' in data}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 60)
