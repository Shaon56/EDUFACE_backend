#!/usr/bin/env python3
"""
Test login with different users
"""

import requests
import json

BASE_URL = 'https://eduface-backend.onrender.com/api'

def test_login(email, password, role='student'):
    """Test login"""
    print(f"\n{'='*60}")
    print(f"Testing Login: {email} (Role: {role})")
    print('='*60)
    
    try:
        response = requests.post(
            f'{BASE_URL}/auth/login',
            json={
                'email': email,
                'password': password,
                'role': role
            },
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        data = response.json()
        
        if response.status_code == 200:
            print("✅ Login successful!")
            print(f"   Token: {data.get('token', 'N/A')[:50]}...")
            print(f"   User ID: {data.get('user', {}).get('id')}")
            print(f"   Full Name: {data.get('user', {}).get('full_name')}")
            print(f"   Email: {data.get('user', {}).get('email')}")
            print(f"   Role: {data.get('user', {}).get('role')}")
        else:
            print(f"❌ Login failed: {data.get('message')}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    # Test admin login
    test_login('admin@eduface.com', 'admin123', 'admin')
    
    # Test student login
    test_login('mondal33-1627@diu.edu.bd', 'Password123', 'student')
    
    # Test student login (wrong password)
    test_login('mondal33-1627@diu.edu.bd', 'wrongpassword', 'student')
