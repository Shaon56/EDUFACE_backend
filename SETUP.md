# EDUFACE Backend - Setup Guide

## Quick Start

### 1. Install Python
Ensure you have Python 3.8+ installed:
```bash
python --version
```

### 2. Create Virtual Environment
```bash
cd backend
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
Create `.env` file from `.env.example`:
```bash
cp .env.example .env
```

Edit `.env` with your settings:
```
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key
DATABASE_URL=sqlite:///eduface.db
```

### 5. Run Server
```bash
python run.py
```

Server will start at: `http://localhost:5000`

## Project Structure

```
backend/
├── run.py                   # Application entry point
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
└── app/
    ├── __init__.py        # App initialization
    ├── models/
    │   ├── __init__.py
    │   └── User, Routine, Attendance, Result
    ├── routes/
    │   ├── __init__.py
    │   ├── auth.py        # Authentication endpoints
    │   ├── users.py       # User management
    │   ├── routines.py    # Schedule management
    │   ├── attendance.py  # Attendance tracking
    │   └── results.py     # Results management
    └── utils/
        ├── __init__.py
        └── google_sheets.py  # Google Sheets integration
```

## Database

### SQLite (Development)
Automatically created as `eduface.db` on first run.

### MySQL (Production)
1. Install MySQL
2. Create database: `CREATE DATABASE eduface_db;`
3. Update DATABASE_URL in .env:
   ```
   DATABASE_URL=mysql://user:password@localhost/eduface_db
   ```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new student
- `POST /api/auth/login` - Login user
- `POST /api/auth/verify-token` - Verify JWT token

### Users
- `GET /api/users` - List all users (admin)
- `GET /api/users/<id>` - Get specific user
- `POST /api/users` - Create user (admin)
- `PUT /api/users/<id>` - Update user
- `DELETE /api/users/<id>` - Delete user (admin)

### Routines
- `GET /api/routines` - Get all routines
- `GET /api/routines?day=Monday` - Get routines by day
- `POST /api/routines` - Create routine (admin)
- `PUT /api/routines/<id>` - Update routine (admin)
- `DELETE /api/routines/<id>` - Delete routine (admin)

### Attendance
- `GET /api/attendance` - Get attendance records
- `GET /api/attendance/recent` - Get recent attendance
- `POST /api/attendance` - Create attendance (admin)
- `PUT /api/attendance/<id>` - Update attendance (admin)
- `DELETE /api/attendance/<id>` - Delete attendance (admin)

### Results
- `GET /api/results` - Get results
- `POST /api/results` - Upload result (admin)
- `PUT /api/results/<id>` - Update result (admin)
- `DELETE /api/results/<id>` - Delete result (admin)

## Database Models

### User
```python
- id (Primary Key)
- full_name (String)
- student_id (Unique String)
- email (Unique Email)
- parent_email (Email)
- contact_number (String)
- password_hash (String)
- role (String: 'student' or 'admin')
- is_active (Boolean)
- created_at (DateTime)
- updated_at (DateTime)
```

### Routine
```python
- id (Primary Key)
- subject (String)
- day (String)
- start_time (String: HH:MM)
- end_time (String: HH:MM)
- room_number (String)
- instructor_name (String, optional)
- created_at (DateTime)
- updated_at (DateTime)
```

### Attendance
```python
- id (Primary Key)
- student_id (Foreign Key)
- routine_id (Foreign Key, optional)
- subject (String)
- date (Date)
- status (String: 'Present' or 'Absent')
- marked_by (String)
- synced_to_sheet (Boolean)
- created_at (DateTime)
- updated_at (DateTime)
```

### Result
```python
- id (Primary Key)
- student_id (Foreign Key)
- routine_id (Foreign Key, optional)
- subject (String)
- marks (Integer)
- grade (String)
- uploaded_by (String)
- created_at (DateTime)
- updated_at (DateTime)
```

## Authentication

### JWT Token
- Issued on login
- Valid for 30 days
- Include in all requests: `Authorization: Bearer <token>`
- Stored in frontend localStorage

### Password Security
- Hashed using Werkzeug's `generate_password_hash()`
- Verified using `check_password_hash()`
- Never stored in plaintext

### Role-Based Access
- **Student**: Can only view/edit own profile
- **Admin**: Full access to all endpoints

## Google Sheets Integration

### Setup
1. Create Google Cloud Project
2. Enable Google Sheets API
3. Create Service Account
4. Download credentials.json
5. Add to .env:
   ```
   GOOGLE_CREDENTIALS_FILE=./credentials.json
   GOOGLE_SHEET_ID=your-sheet-id
   ```

### Usage
```python
from app.utils import GoogleSheetsAPI

sheets = GoogleSheetsAPI()
sheets.append_attendance(data)
```

## Development

### Debug Mode
Set in `.env`:
```
FLASK_ENV=development
FLASK_DEBUG=True
```

### Auto-reload
With debug mode enabled, server auto-reloads on code changes.

### Database Reset
```bash
rm eduface.db
python run.py
```

### Create Admin Account
```python
from app import db, create_app
from app.models import User

app = create_app()
with app.app_context():
    admin = User(
        full_name="Admin User",
        student_id="ADMIN001",
        email="admin@eduface.com",
        parent_email="admin@eduface.com",
        contact_number="0000000000",
        role="admin"
    )
    admin.set_password("admin123")
    db.session.add(admin)
    db.session.commit()
```

## Testing

### Using cURL
```bash
# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@eduface.com","password":"admin123","role":"admin"}'

# Get users (requires token)
curl -H "Authorization: Bearer <token>" \
  http://localhost:5000/api/users
```

### Using Postman
1. Create POST request to `http://localhost:5000/api/auth/login`
2. Set body to JSON with email, password, role
3. Copy token from response
4. Add Authorization header: `Bearer <token>`
5. Test other endpoints

### Using Python requests
```python
import requests

# Login
response = requests.post('http://localhost:5000/api/auth/login', 
    json={
        'email': 'admin@eduface.com',
        'password': 'admin123',
        'role': 'admin'
    }
)
token = response.json()['token']

# Get users
headers = {'Authorization': f'Bearer {token}'}
response = requests.get('http://localhost:5000/api/users', headers=headers)
print(response.json())
```

## Deployment

### Local Testing
```bash
python run.py
```

### Production with Gunicorn
```bash
pip install gunicorn
gunicorn run:app
```

### Docker
Create Dockerfile:
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "run:app"]
```

Build and run:
```bash
docker build -t eduface-backend .
docker run -p 5000:5000 eduface-backend
```

### Render Deployment
1. Push code to GitHub
2. Create new Web Service on Render
3. Connect repository
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `gunicorn run:app`
6. Add environment variables
7. Deploy

### Railway Deployment
1. Connect GitHub
2. Select Flask template
3. Configure environment variables
4. Deploy automatically on push

### PythonAnywhere
1. Upload code
2. Create web app
3. Configure WSGI file
4. Reload application

## Environment Variables

### Required
```
SECRET_KEY          # Flask secret key
JWT_SECRET_KEY      # JWT signing key
```

### Optional
```
FLASK_ENV           # development, production, testing
FLASK_DEBUG         # True/False
DATABASE_URL        # Database connection string
GOOGLE_SHEET_ID     # Google Sheet ID
GOOGLE_CREDENTIALS  # Path to credentials.json
MAIL_SERVER         # Email server
MAIL_PORT          # Email port
MAIL_USERNAME      # Email username
MAIL_PASSWORD      # Email password
```

## Common Issues

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Database Lock
```bash
# Remove database and restart
rm eduface.db
python run.py
```

### Port Already in Use
```bash
# Find process on port 5000
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Kill process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows
```

### CORS Issues
Check CORS configuration in `run.py`. Should allow frontend origin.

### JWT Token Issues
- Ensure JWT_SECRET_KEY is set in .env
- Token expires after 30 days
- Check token format: `Bearer <token>`

## Logging

### Enable Logging
```python
import logging

logging.basicConfig(level=logging.DEBUG)
```

### View Logs
Check console output when running `python run.py`

## Performance

### Database Optimization
- Use indexes on frequently queried columns
- Optimize queries with `.limit()`
- Use pagination for large datasets

### Caching
Consider implementing caching with Redis for frequently accessed data.

### API Response Times
- Database queries are cached automatically
- Use proper HTTP methods (GET, POST, PUT, DELETE)
- Return only necessary data

## Security

### Production Checklist
- [ ] Change SECRET_KEY and JWT_SECRET_KEY
- [ ] Set FLASK_ENV to production
- [ ] Enable HTTPS
- [ ] Configure CORS properly
- [ ] Use environment variables for secrets
- [ ] Enable database encryption
- [ ] Set up logging and monitoring
- [ ] Regular security updates
- [ ] Input validation on all endpoints
- [ ] SQL injection prevention (SQLAlchemy)

## Monitoring

### Health Check
```bash
curl http://localhost:5000/api/health
```

Response:
```json
{
  "status": "ok",
  "message": "EDUFACE backend is running"
}
```

### Error Tracking
Logs are printed to console. Consider using external service:
- Sentry
- Datadog
- New Relic

## Maintenance

### Regular Tasks
- Monitor database size
- Check error logs
- Update dependencies
- Backup database
- Review API usage

### Database Backup
```bash
# SQLite
cp eduface.db eduface.db.backup

# MySQL
mysqldump -u user -p eduface_db > backup.sql
```

---

**Last Updated**: January 1, 2026
