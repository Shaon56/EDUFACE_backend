#!/usr/bin/env python3
"""
Test logins after fixes
"""

import requests

BASE_URL = 'https://eduface-backend.onrender.com/api'

print("Testing Admin Login...")
r = requests.post(f'{BASE_URL}/auth/login', json={
    'email': 'admin@eduface.com',
    'password': 'admin123',
    'role': 'admin'
})
data = r.json()
if r.status_code == 200:
    print("✅ Admin Login: SUCCESS")
    user = data.get('user', {})
    print(f"   Name: {user.get('full_name')}")
    print(f"   Role: {user.get('role')}")
else:
    print(f"❌ Admin Login: FAILED - {data.get('message')}")

print()
print("Testing Student Login...")
r = requests.post(f'{BASE_URL}/auth/login', json={
    'email': 'mondal33-1627@diu.edu.bd',
    'password': 'TestPass123',
    'role': 'student'
})
data = r.json()
if r.status_code == 200:
    print("✅ Student Login: SUCCESS")
    user = data.get('user', {})
    print(f"   Name: {user.get('full_name')}")
    print(f"   Role: {user.get('role')}")
else:
    print(f"❌ Student Login: FAILED - {data.get('message')}")
