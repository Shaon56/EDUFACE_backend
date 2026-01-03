"""
Google Sheets integration utility
"""

import os
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from googleapiclient.discovery import build

class GoogleSheetsAPI:
    """Handle Google Sheets operations"""
    
    def __init__(self, credentials_file=None, sheet_id=None):
        """Initialize Google Sheets API"""
        self.sheet_id = sheet_id or os.environ.get('GOOGLE_SHEET_ID')
        self.credentials_file = credentials_file or os.environ.get('GOOGLE_CREDENTIALS_FILE')
        self.service = None
        
        if self.credentials_file and self.sheet_id:
            self.authenticate()
    
    def authenticate(self):
        """Authenticate with Google Sheets API"""
        try:
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_file,
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
            self.service = build('sheets', 'v4', credentials=credentials)
        except Exception as e:
            print(f"Error authenticating with Google Sheets: {e}")
    
    def append_attendance(self, attendance_data):
        """Append attendance record to Google Sheet"""
        if not self.service:
            return False
        
        try:
            values = [[
                attendance_data['student_id'],
                attendance_data['subject'],
                attendance_data['date'],
                attendance_data['status']
            ]]
            
            body = {'values': values}
            result = self.service.spreadsheets().values().append(
                spreadsheetId=self.sheet_id,
                range='Sheet1!A:D',
                valueInputOption='USER_ENTERED',
                body=body
            ).execute()
            
            return True
        except Exception as e:
            print(f"Error appending to Google Sheet: {e}")
            return False
    
    def read_attendance(self):
        """Read attendance data from Google Sheet"""
        if not self.service:
            return []
        
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.sheet_id,
                range='Sheet1!A:D'
            ).execute()
            
            return result.get('values', [])
        except Exception as e:
            print(f"Error reading from Google Sheet: {e}")
            return []
    
    def update_attendance(self, row, attendance_data):
        """Update attendance record in Google Sheet"""
        if not self.service:
            return False
        
        try:
            values = [[
                attendance_data['student_id'],
                attendance_data['subject'],
                attendance_data['date'],
                attendance_data['status']
            ]]
            
            body = {'values': values}
            result = self.service.spreadsheets().values().update(
                spreadsheetId=self.sheet_id,
                range=f'Sheet1!A{row}:D{row}',
                valueInputOption='USER_ENTERED',
                body=body
            ).execute()
            
            return True
        except Exception as e:
            print(f"Error updating Google Sheet: {e}")
            return False
