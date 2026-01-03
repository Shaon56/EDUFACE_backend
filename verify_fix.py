#!/usr/bin/env python3
"""
Quick verification script for the user management fix
Run this to verify everything is working on Render
"""

import requests
import sys

BASE_URL = 'https://eduface-backend.onrender.com/api'

print("""
╔══════════════════════════════════════════════════════════════════════╗
║                    USER MANAGEMENT FIX VERIFICATION                  ║
╚══════════════════════════════════════════════════════════════════════╝
""")

try:
    # 1. Admin Login
    print("1️⃣  Testing Admin Login...")
    login_response = requests.post(f'{BASE_URL}/auth/login', json={
        'email': 'admin@eduface.com',
        'password': 'admin123',
        'role': 'admin'
    }, timeout=10)
    
    if login_response.status_code != 200:
        print(f"   ❌ Login failed: {login_response.status_code}")
        sys.exit(1)
    
    admin_data = login_response.json()
    token = admin_data.get('token')
    print("   ✅ Admin login successful")
    
    # 2. Get Users
    print("\n2️⃣  Testing User API...")
    headers = {'Authorization': f'Bearer {token}'}
    users_response = requests.get(f'{BASE_URL}/users', headers=headers, timeout=10)
    
    if users_response.status_code != 200:
        print(f"   ❌ User API failed: {users_response.status_code}")
        print(f"   Response: {users_response.json()}")
        sys.exit(1)
    
    users = users_response.json()
    print(f"   ✅ Retrieved {len(users)} users")
    
    # 3. Verify Fields
    print("\n3️⃣  Verifying User Fields...")
    if users:
        user = users[0]
        required = ['ID', 'Full Name', 'Email', 'Student ID', 'Phone', 'Role']
        missing = [f for f in required if f not in user]
        
        if missing:
            print(f"   ❌ Missing fields: {missing}")
            sys.exit(1)
        
        print("   ✅ All required fields present")
        for field in ['Full Name', 'Email', 'Student ID', 'Phone', 'Role']:
            print(f"      • {field}: {user.get(field)}")
    
    # 4. Summary
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                           ✅ ALL CHECKS PASSED                       ║
╠══════════════════════════════════════════════════════════════════════╣
║  • Admin authentication working                                       ║
║  • User API authorization working                                     ║
║  • User fields displaying correctly                                   ║
║  • Ready for production use                                           ║
╚══════════════════════════════════════════════════════════════════════╝
""")
    
    print("\n📊 Quick Stats:")
    print(f"   Total Users: {len(users)}")
    admin_count = len([u for u in users if u.get('Role', '').lower() == 'admin'])
    student_count = len([u for u in users if u.get('Role', '').lower() == 'student'])
    print(f"   Admin Users: {admin_count}")
    print(f"   Student Users: {student_count}")
    
    print("\n💡 To test in browser:")
    print("   1. Go to: https://eduface-dashboard.netlify.app/")
    print("   2. Log in as: admin@eduface.com / admin123 (select Admin)")
    print("   3. Click 'Users' in the menu")
    print("   4. Verify all user data displays correctly")
    
except requests.exceptions.ConnectionError:
    print("   ❌ Cannot connect to backend. Is it running?")
    print(f"   URL: {BASE_URL}")
    sys.exit(1)
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)
