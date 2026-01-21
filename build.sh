#!/bin/bash
set -o errexit

# Install dependencies
echo "Installing dependencies..."
pip install --no-cache-dir -r requirements.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run migrations
echo "Running database migrations..."
python manage.py migrate

echo "Build completed successfully!"
