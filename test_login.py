"""
Test login endpoint
"""

import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from run import create_app

app = create_app()

# Test login
with app.test_client() as client:
    print("\n=== Testing Login ===")
    
    login_data = {
        'email': 'admin@eduface.com',
        'password': 'admin123',
        'role': 'admin'
    }
    
    response = client.post(
        '/api/auth/login',
        data=json.dumps(login_data),
        content_type='application/json'
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json}")
    
    if response.status_code == 200:
        token = response.json.get('token')
        print(f"\n✅ Login successful!")
        print(f"Token: {token[:50]}...")
        
        # Try to use the token
        print("\n=== Testing GET routines with token ===")
        response2 = client.get(
            '/api/routines',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        print(f"Status: {response2.status_code}")
        print(f"Response: {response2.json}")
    else:
        print(f"\n❌ Login failed")
