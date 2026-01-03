#!/usr/bin/env python3
"""
Test attendance API to verify demo data was created
"""

import requests
import json

BASE_URL = 'https://eduface-backend.onrender.com/api'

def test_attendance_api():
    print("="*70)
    print("Testing Attendance API")
    print("="*70)
    
    # Step 1: Login as admin
    print("\n1. Admin Login...")
    login_response = requests.post(f'{BASE_URL}/auth/login', json={
        'email': 'admin@eduface.com',
        'password': 'admin123',
        'role': 'admin'
    })
    
    if login_response.status_code == 200:
        admin_data = login_response.json()
        token = admin_data.get('token')
        print(f"✅ Admin login successful")
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        # Step 2: Get attendance control (admin view)
        print("\n2. Get Attendance Records...")
        attendance_response = requests.get(f'{BASE_URL}/attendance', headers=headers)
        
        if attendance_response.status_code == 200:
            attendance = attendance_response.json()
            print(f"✅ Retrieved {len(attendance)} attendance records")
            
            if attendance:
                print("\nSample Attendance Records (First 10):")
                print("-" * 70)
                for i, record in enumerate(attendance[:10], 1):
                    print(f"\nRecord {i}:")
                    for key, value in record.items():
                        print(f"  {key}: {value}")
        else:
            print(f"❌ Failed to get attendance: {attendance_response.status_code}")
            print(attendance_response.text)
    else:
        print(f"❌ Failed to login: {login_response.status_code}")
        print(login_response.text)
    
    print("\n" + "="*70)

if __name__ == '__main__':
    test_attendance_api()
