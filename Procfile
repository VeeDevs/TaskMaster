web: gunicorn --workers 3 --worker-class sync --max-requests 1000 --max-requests-jitter 50 mysite.wsgi:application
