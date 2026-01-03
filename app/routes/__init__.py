"""Initialize routes package"""
from .auth import auth_bp
from .users import users_bp
from .routines import routines_bp
from .attendance import attendance_bp
from .results import results_bp

__all__ = ['auth_bp', 'users_bp', 'routines_bp', 'attendance_bp', 'results_bp']
