"""
Test script to verify database and create routine
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from run import create_app, db
from app.models import Routine

# Create the app
app = create_app()

with app.app_context():
    # Drop all tables and recreate them
    print("Creating database tables...")
    db.create_all()
    print("✅ Database tables created!")
    
    # Test creating a routine
    try:
        print("\nTesting routine creation...")
        routine = Routine(
            subject='Test Math',
            day='Monday',
            start_time='09:00',
            end_time='10:00',
            room_number='101',
            instructor_name='Mr. Smith'
        )
        
        db.session.add(routine)
        db.session.commit()
        
        print(f"✅ Routine created successfully!")
        print(f"   ID: {routine.id}")
        print(f"   Subject: {routine.subject}")
        print(f"   Day: {routine.day}")
        print(f"   Data: {routine.to_dict()}")
        
        # Retrieve and verify
        retrieved = Routine.query.first()
        print(f"\n✅ Retrieved routine: {retrieved.to_dict()}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
