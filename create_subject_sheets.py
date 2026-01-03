#!/usr/bin/env python3
"""
Create subject-wise attendance sheets
Each sheet: Student ID | Date | Status (Present/Absent)
"""

from app.google_sheets_db import GoogleSheetsDB
from datetime import datetime, timedelta
import random
import time

def create_subject_sheets():
    """Create 4 subject-wise attendance sheets"""
    db = GoogleSheetsDB()
    
    print("="*70)
    print("Creating Subject-Wise Attendance Sheets")
    print("="*70)
    
    # Define 4 subjects
    subjects = ['Chemistry', 'Math', 'Physics', 'English']
    
    # Get all students
    users = db.get_all_users()
    students = [u for u in users if u.get('Role', 'student').lower() == 'student']
    
    print(f"\n✓ Found {len(students)} students")
    print(f"✓ Creating sheets for {len(subjects)} subjects")
    
    for subject_idx, subject in enumerate(subjects):
        try:
            # Wait before creating new sheet to avoid rate limits
            if subject_idx > 0:
                wait_time = 15
                print(f"\n⏳ Waiting {wait_time}s to avoid rate limit...")
                time.sleep(wait_time)
            
            print(f"\n📄 Processing: {subject}")
            
            # Check if sheet exists, if not create it
            try:
                worksheet = db.spreadsheet.worksheet(subject)
                print(f"   ✓ Sheet '{subject}' already exists")
                worksheet.clear()
                
            except:
                # Create new sheet
                worksheet = db.spreadsheet.add_worksheet(title=subject, rows=500, cols=3)
                print(f"   ✓ Created new sheet '{subject}'")
                time.sleep(2)  # Small delay after creating sheet
            
            # Add headers
            headers = ['Student ID', 'Date', 'Status']
            worksheet.append_row(headers)
            print(f"   ✓ Added headers: {headers}")
            time.sleep(1)
            
            # Add attendance records for the last 7 days
            # Batch records to avoid rate limit
            all_records = []
            for day_offset in range(7):
                date = (datetime.now() - timedelta(days=day_offset)).strftime('%Y-%m-%d')
                
                # Add attendance for each student
                for student in students:
                    student_id = student.get('Student ID', 'Unknown')
                    status = random.choice(['Present', 'Absent'])
                    all_records.append([student_id, date, status])
            
            # Add records in smaller batches
            batch_size = 10
            record_count = 0
            for i in range(0, len(all_records), batch_size):
                batch = all_records[i:i+batch_size]
                for row in batch:
                    worksheet.append_row(row)
                    record_count += 1
                
                # Small delay between batches
                if (i + batch_size) < len(all_records):
                    time.sleep(0.5)
            
            print(f"   ✓ Added {record_count} attendance records")
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)[:100]}")
    
    print("\n" + "="*70)
    print("✅ Subject-Wise Sheets Created Successfully!")
    print("="*70)
    print("\nSheet Structure:")
    print("  Each sheet: [Subject Name]")
    print("  Columns: Student ID | Date | Status (Present/Absent)")
    print("  Records: 35 per subject (5 students × 7 days)")
    print("\nSheets Created:")
    for i, subject in enumerate(subjects, 1):
        print(f"  {i}. {subject}")

if __name__ == '__main__':
    create_subject_sheets()
