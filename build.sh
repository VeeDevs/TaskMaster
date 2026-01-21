#!/bin/bash
set -o errexit

# Install dependencies
echo "Installing dependencies..."
pip install --no-cache-dir -r requirements.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Build completed successfully!"
echo "Migrations will run during release phase on Render..."
