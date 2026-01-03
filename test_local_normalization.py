#!/usr/bin/env python3
"""
Test locally to verify field normalization
"""

import sys
sys.path.insert(0, '/d/demo website/backend')

from app.google_sheets_db import GoogleSheetsDB

print("Testing Local Field Normalization")
print("="*70)

try:
    db = GoogleSheetsDB()
    
    print("\n1. Getting all routines...")
    routines = db.get_all_routines()
    
    print(f"✅ Retrieved {len(routines)} routines\n")
    
    if routines:
        routine = routines[0]
        print(f"First Routine Fields:")
        print(f"  'id': {routine.get('id')} (expected: not None)")
        print(f"  'subject': {routine.get('subject')} (expected: not None)")
        print(f"  'day': {routine.get('day')} (expected: not None)")
        print(f"  'start_time': {routine.get('start_time')}")
        print(f"  'end_time': {routine.get('end_time')}")
        print(f"  'room_number': {routine.get('room_number')}")
        print(f"  'instructor_name': {routine.get('instructor_name')}")
        
        print(f"\nAll Keys: {list(routine.keys())}")
        
        # Check if Subject and Day are now lowercase
        if 'subject' in routine and routine['subject']:
            print(f"\n✅ Subject field is present and normalized: {routine['subject']}")
        else:
            print(f"\n❌ Subject field is missing or empty")
            
        if 'day' in routine and routine['day']:
            print(f"✅ Day field is present and normalized: {routine['day']}")
        else:
            print(f"❌ Day field is missing or empty")
    
    print("\n" + "="*70)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
