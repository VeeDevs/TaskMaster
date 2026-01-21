#!/usr/bin/env python
"""
Render deployment helper script
Handles database migrations safely
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
    
    try:
        # Setup Django
        django.setup()
        
        # Run migrations
        print("=" * 60)
        print("Running migrations...")
        print("=" * 60)
        execute_from_command_line(['manage.py', 'migrate', '--noinput'])
        
        print("\n" + "=" * 60)
        print("Migrations completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"Error during migration: {e}", file=sys.stderr)
        sys.exit(1)
