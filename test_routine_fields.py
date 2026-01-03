#!/usr/bin/env python3
"""
Detailed test to verify routine field names
"""

import requests
import json

BASE_URL = 'https://eduface-backend.onrender.com/api'

def test_routine_fields():
    print("="*70)
    print("Testing Routine Field Names")
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
    
    # Step 2: Get all routines and check field names
    print("\n2. Get All Routines and Check Field Names...")
    routines_response = requests.get(f'{BASE_URL}/routines', headers=headers)
    
    if routines_response.status_code == 200:
        routines = routines_response.json()
        print(f"✅ Retrieved {len(routines)} routines")
        print("\nDetailed Routine Data:")
        print("-" * 70)
        
        for i, routine in enumerate(routines, 1):
            print(f"\nRoutine {i}:")
            print(f"  ID: {routine.get('id')}")
            print(f"  subject: {routine.get('subject')} {'✅' if routine.get('subject') else '❌ MISSING'}")
            print(f"  day: {routine.get('day')} {'✅' if routine.get('day') else '❌ MISSING'}")
            
            # Check field existence AND values
            start_time = routine.get('start_time')
            end_time = routine.get('end_time')
            room = routine.get('room_number')
            instructor = routine.get('instructor_name')
            
            print(f"  Start Time: '{start_time}' {'✅' if start_time else '❌ EMPTY/NULL'}")
            print(f"  End Time: '{end_time}' {'✅' if end_time else '❌ EMPTY/NULL'}")
            print(f"  Room: '{room}' {'✅' if room else '❌ EMPTY/NULL'}")
            print(f"  Instructor: '{instructor}' {'✅' if instructor else '❌ EMPTY/NULL'}")
            
            # Show all keys
            print(f"  All Keys: {list(routine.keys())}")
            print(f"\n  Raw JSON: {json.dumps(routine, indent=4)}")
    else:
        print(f"❌ Failed to get routines: {routines_response.status_code}")
    
    print("\n" + "="*70)

if __name__ == '__main__':
    test_routine_fields()
