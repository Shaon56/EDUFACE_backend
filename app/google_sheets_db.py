"""
Google Sheets Database Wrapper
Handles all database operations using Google Sheets as persistent storage
"""
import gspread
from google.oauth2.service_account import Credentials
import os
import json
from datetime import datetime

class GoogleSheetsDB:
    def __init__(self):
        """Initialize Google Sheets connection"""
        self.scopes = ['https://www.googleapis.com/auth/spreadsheets', 
                       'https://www.googleapis.com/auth/drive']
        
        # Try to load credentials from environment variable (Render production)
        creds_json_str = os.getenv('GOOGLE_SHEETS_CREDS')
        
        if creds_json_str:
            # Production: Use environment variable
            creds_dict = json.loads(creds_json_str)
            credentials = Credentials.from_service_account_info(creds_dict, scopes=self.scopes)
        else:
            # Development: Use local service_account.json
            # Look for the file in the backend folder (parent of app folder)
            backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            creds_file = os.path.join(backend_dir, 'service_account.json')
            
            if not os.path.exists(creds_file):
                raise FileNotFoundError(
                    f"service_account.json not found at {creds_file}. "
                    "Please copy it from the root folder or set GOOGLE_SHEETS_CREDS environment variable."
                )
            
            credentials = Credentials.from_service_account_file(
                creds_file,
                scopes=self.scopes
            )
        
        self.client = gspread.authorize(credentials)
        
        # Get the spreadsheet (you'll need to create this and set GOOGLE_SHEETS_ID env var)
        spreadsheet_id = os.getenv('GOOGLE_SHEETS_ID', 'EDUFACE Database')
        print(f"[DEBUG] Attempting to open spreadsheet: '{spreadsheet_id}'")
        try:
            self.spreadsheet = self.client.open(spreadsheet_id)
            print(f"[DEBUG] Successfully opened spreadsheet")
        except gspread.exceptions.SpreadsheetNotFound:
            raise Exception(f"Google Sheet '{spreadsheet_id}' not found. Create it first!")
        
        # Get worksheets - Handle both singular and plural names
        self.users_sheet = self._get_worksheet('Users', 'User')
        self.routines_sheet = self._get_worksheet('Routines', 'Routine')
        
        # Try to get Attendance sheet (may not exist if using subject-wise sheets)
        try:
            self.attendance_sheet = self._get_worksheet('Attendance', 'Attendances')
        except:
            print("[DEBUG] Attendance sheet not found - using subject-wise sheets")
            self.attendance_sheet = None
        
        self.results_sheet = self._get_worksheet('Results', 'Result')
    
    def _get_worksheet(self, *names):
        """Get worksheet by trying multiple possible names"""
        for name in names:
            try:
                return self.spreadsheet.worksheet(name)
            except:
                continue
        raise Exception(f"Could not find sheet with any of these names: {names}")
    
    # ==================== USER OPERATIONS ====================
    
    def get_all_users(self):
        """Get all users from Google Sheets"""
        try:
            records = self.users_sheet.get_all_records()
            # Return as-is to preserve all fields
            return records
        except Exception as e:
            print(f"[ERROR] Failed to get users: {e}")
            return []
    
    def find_user_by_email(self, email):
        """Find user by email"""
        try:
            records = self.users_sheet.get_all_records()
            for record in records:
                if record.get('Email', '').lower() == email.lower():
                    return record
            return None
        except Exception as e:
            print(f"[ERROR] Failed to find user by email: {e}")
            return None
    
    def find_user_by_id(self, user_id):
        """Find user by ID"""
        try:
            records = self.users_sheet.get_all_records()
            for record in records:
                if str(record.get('ID', '')).strip() == str(user_id).strip():
                    return record
            return None
        except Exception as e:
            print(f"[ERROR] Failed to find user by ID: {e}")
            return None
    
    def add_user(self, user_data):
        """Add a new user to Google Sheets"""
        try:
            # Get next ID
            records = self.users_sheet.get_all_records()
            next_id = len(records) + 1
            
            # Prepare row
            row = [
                next_id,  # ID
                user_data.get('name', ''),
                user_data.get('email', ''),
                user_data.get('password', ''),
                user_data.get('student_id', ''),
                user_data.get('phone', ''),
                user_data.get('role', 'student'),
                user_data.get('section', ''),
                'true',  # is_active
                datetime.now().isoformat()  # created_at
            ]
            
            self.users_sheet.append_row(row)
            
            # Return the added user
            return {
                'id': next_id,
                'name': user_data.get('name'),
                'email': user_data.get('email'),
                'student_id': user_data.get('student_id'),
                'phone': user_data.get('phone'),
                'role': user_data.get('role', 'student'),
                'section': user_data.get('section'),
                'is_active': True
            }
        except Exception as e:
            print(f"[ERROR] Failed to add user: {e}")
            return None
    
    # ==================== ROUTINE OPERATIONS ====================
    
    def get_all_routines(self):
        """Get all routines"""
        try:
            records = self.routines_sheet.get_all_records()
            
            # Normalize field names to lowercase for consistent API responses
            normalized = []
            for record in records:
                # Handle both possible column name formats
                normalized_record = {
                    'id': record.get('ID', record.get('id', '')),
                    'user_id': record.get('User ID', record.get('user_id', '')),
                    'day': record.get('day', ''),
                    'start_time': record.get('start_time', ''),
                    'end_time': record.get('end_time', ''),
                    'subject': record.get('subject', ''),
                    'instructor_name': record.get('instructor_name', ''),
                    'room_number': record.get('room_number', '')
                }
                normalized.append(normalized_record)
            return normalized
        except Exception as e:
            print(f"[ERROR] Failed to get routines: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def get_user_routines(self, user_id):
        """Get routines for a specific user"""
        try:
            records = self.routines_sheet.get_all_records()
            # Normalize field names to lowercase
            normalized = []
            for record in records:
                if str(record.get('User ID', '')) == str(user_id):
                    normalized_record = {
                        'id': record.get('ID', record.get('id', '')),
                        'user_id': record.get('User ID', record.get('user_id', '')),
                        'day': record.get('day', ''),
                        'start_time': record.get('start_time', ''),
                        'end_time': record.get('end_time', ''),
                        'subject': record.get('subject', ''),
                        'instructor_name': record.get('instructor_name', ''),
                        'room_number': record.get('room_number', '')
                    }
                    normalized.append(normalized_record)
            return normalized
        except Exception as e:
            print(f"[ERROR] Failed to get user routines: {e}")
            return []
    
    def add_routine(self, routine_data):
        """Add a new routine"""
        try:
            records = self.routines_sheet.get_all_records()
            next_id = len(records) + 1
            
            row = [
                next_id,  # ID
                routine_data.get('user_id', ''),
                routine_data.get('day', ''),
                routine_data.get('start_time', ''),
                routine_data.get('end_time', ''),
                routine_data.get('subject', ''),
                routine_data.get('instructor_name', ''),
                routine_data.get('room_number', ''),
                datetime.now().isoformat()
            ]
            
            self.routines_sheet.append_row(row)
            
            return {
                'id': next_id,
                'user_id': routine_data.get('user_id'),
                'day': routine_data.get('day'),
                'start_time': routine_data.get('start_time'),
                'end_time': routine_data.get('end_time'),
                'subject': routine_data.get('subject'),
                'instructor_name': routine_data.get('instructor_name'),
                'room_number': routine_data.get('room_number')
            }
        except Exception as e:
            print(f"[ERROR] Failed to add routine: {e}")
            return None
    
    def delete_routine(self, routine_id):
        """Delete a routine by ID"""
        try:
            records = self.routines_sheet.get_all_records()
            for idx, record in enumerate(records):
                if str(record.get('ID', '')) == str(routine_id):
                    # Delete the row (row index + 2 because of header row)
                    self.routines_sheet.delete_rows(idx + 2, idx + 2)
                    return True
            return False
        except Exception as e:
            print(f"[ERROR] Failed to delete routine: {e}")
            return False
    
    # ==================== ATTENDANCE OPERATIONS ====================
    
    def get_all_attendance(self):
        """Get all attendance records"""
        try:
            records = self.attendance_sheet.get_all_records()
            return records
        except Exception as e:
            print(f"[ERROR] Failed to get attendance: {e}")
            return []
    
    def get_user_attendance(self, user_id):
        """Get attendance records for a specific user from all subject sheets"""
        try:
            all_attendance = []
            
            # Define subject sheets
            subjects = ['Chemistry', 'Math', 'Physics', 'English']
            
            for subject in subjects:
                try:
                    worksheet = self.spreadsheet.worksheet(subject)
                    records = worksheet.get_all_records()
                    
                    # Get student's record from this subject
                    student_id = None
                    users = self.get_all_users()
                    for user in users:
                        if user.get('ID') == user_id:
                            student_id = user.get('Student ID')
                            break
                    
                    if student_id:
                        subject_records = [r for r in records if str(r.get('Student ID', '')) == str(student_id)]
                        # Add subject info to each record
                        for record in subject_records:
                            record['Subject'] = subject
                        all_attendance.extend(subject_records)
                except:
                    continue
            
            return all_attendance
        except Exception as e:
            print(f"[ERROR] Failed to get user attendance: {e}")
            return []
    
    def get_attendance_by_subject(self, subject):
        """Get all attendance records for a specific subject"""
        try:
            worksheet = self.spreadsheet.worksheet(subject)
            records = worksheet.get_all_records()
            
            # Add subject info to each record
            for record in records:
                record['Subject'] = subject
            
            return records
        except Exception as e:
            print(f"[ERROR] Failed to get attendance for subject {subject}: {e}")
            return []
    
    def get_all_attendance_subjects(self):
        """Get all available subject sheets"""
        subjects = ['Chemistry', 'Math', 'Physics', 'English']
        available = []
        
        for subject in subjects:
            try:
                self.spreadsheet.worksheet(subject)
                available.append(subject)
            except:
                continue
        
        return available
    
    def add_attendance_to_subject(self, subject, attendance_data):
        """Add attendance record to a specific subject sheet"""
        try:
            worksheet = self.spreadsheet.worksheet(subject)
            
            row = [
                attendance_data.get('student_id', ''),
                attendance_data.get('date', datetime.now().strftime('%Y-%m-%d')),
                attendance_data.get('status', 'Absent')
            ]
            
            worksheet.append_row(row)
            
            return {
                'subject': subject,
                'student_id': attendance_data.get('student_id'),
                'date': attendance_data.get('date'),
                'status': attendance_data.get('status')
            }
        except Exception as e:
            print(f"[ERROR] Failed to add attendance to {subject}: {e}")
            return None
    
    def add_attendance(self, attendance_data):
        """Add attendance record - tries subject sheet first, then old Attendance sheet"""
        # Try to add to subject sheet if available
        if 'subject' in attendance_data:
            result = self.add_attendance_to_subject(attendance_data['subject'], attendance_data)
            if result:
                return result
        
        # Fallback to old Attendance sheet if it exists
        if self.attendance_sheet:
            try:
                records = self.attendance_sheet.get_all_records()
                next_id = len(records) + 1
                
                row = [
                    next_id,  # ID
                    attendance_data.get('user_id', ''),
                    attendance_data.get('subject', ''),
                    attendance_data.get('status', 'Absent'),
                    attendance_data.get('date', datetime.now().strftime('%Y-%m-%d')),
                    datetime.now().isoformat()
                ]
                
                self.attendance_sheet.append_row(row)
                
                return {
                    'id': next_id,
                    'user_id': attendance_data.get('user_id'),
                    'subject': attendance_data.get('subject'),
                    'status': attendance_data.get('status'),
                    'date': attendance_data.get('date')
                }
            except Exception as e:
                print(f"[ERROR] Failed to add attendance: {e}")
        
        return None
    
    # ==================== RESULTS OPERATIONS ====================
    
    def get_all_results(self):
        """Get all results"""
        try:
            records = self.results_sheet.get_all_records()
            return records
        except Exception as e:
            print(f"[ERROR] Failed to get results: {e}")
            return []
    
    def get_user_results(self, user_id):
        """Get results for a specific user"""
        try:
            records = self.results_sheet.get_all_records()
            user_results = [r for r in records if str(r.get('User ID', '')) == str(user_id)]
            return user_results
        except Exception as e:
            print(f"[ERROR] Failed to get user results: {e}")
            return []
    
    def add_result(self, result_data):
        """Add result record"""
        try:
            records = self.results_sheet.get_all_records()
            next_id = len(records) + 1
            
            row = [
                next_id,  # ID
                result_data.get('user_id', ''),
                result_data.get('subject', ''),
                result_data.get('marks', 0),
                result_data.get('grade', 'F'),
                result_data.get('date', datetime.now().strftime('%Y-%m-%d')),
                datetime.now().isoformat()
            ]
            
            self.results_sheet.append_row(row)
            
            return {
                'id': next_id,
                'user_id': result_data.get('user_id'),
                'subject': result_data.get('subject'),
                'marks': result_data.get('marks'),
                'grade': result_data.get('grade'),
                'date': result_data.get('date')
            }
        except Exception as e:
            print(f"[ERROR] Failed to add result: {e}")
            return None
