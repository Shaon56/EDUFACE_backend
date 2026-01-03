#!/usr/bin/env python3
"""
Create demo attendance records for testing
"""

from app.google_sheets_db import GoogleSheetsDB
from datetime import datetime, timedelta
import random

def create_demo_attendance():
    """Create demo attendance records"""
    db = GoogleSheetsDB()
    
    print("="*70)
    print("Creating Demo Attendance Records")
    print("="*70)
    
    # Get all students (exclude admin)
    users = db.get_all_users()
    students = [u for u in users if u.get('Role', 'student').lower() == 'student']
    
    # Get all routines
    routines = db.get_all_routines()
    
    print(f"\nFound {len(students)} students")
    print(f"Found {len(routines)} routines")
    
    if not students or not routines:
        print("❌ No students or routines found!")
        return
    
    # Create attendance records for the last 7 days
    attendance_count = 0
    
    for day_offset in range(7):
        date = (datetime.now() - timedelta(days=day_offset)).strftime('%Y-%m-%d')
        
        for routine in routines:
            # Create attendance for 4-5 random students per routine per day
            num_students = random.randint(3, len(students))
            selected_students = random.sample(students, min(num_students, len(students)))
            
            for student in selected_students:
                status = random.choice(['Present', 'Absent', 'Late'])
                
                # Add attendance record
                attendance_data = {
                    'user_id': student.get('ID'),
                    'subject': routine.get('subject', 'Unknown'),
                    'status': status,
                    'date': date
                }
                
                result = db.add_attendance(attendance_data)
                if result:
                    attendance_count += 1
                    print(f"✅ Created attendance: {student.get('Full Name')} - {routine.get('subject')} ({status}) on {date}")
    
    print("\n" + "="*70)
    print(f"✅ Successfully created {attendance_count} attendance records!")
    print("="*70)

if __name__ == '__main__':
    create_demo_attendance()
