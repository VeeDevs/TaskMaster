release: python manage.py migrate --noinput && python manage.py check
web: gunicorn mysite.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --worker-class sync --timeout 60
