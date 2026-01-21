"""
Vercel WSGI application wrapper for Django
"""
import os
import sys
from pathlib import Path

# Add project to path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

# Django setup
import django
django.setup()

from django.core.wsgi import get_wsgi_application

# Get WSGI application
application = get_wsgi_application()
