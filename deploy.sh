#!/bin/bash
# Render deployment script with error handling

set -e  # Exit on error

echo "======================================"
echo "TaskMaster Deployment Script"
echo "======================================"

# Step 1: Install dependencies
echo ""
echo "Step 1: Installing Python dependencies..."
pip install --no-cache-dir -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
echo "✓ Dependencies installed successfully"

# Step 2: Collect static files
echo ""
echo "Step 2: Collecting static files..."
python manage.py collectstatic --noinput --clear
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to collect static files"
    exit 1
fi
echo "✓ Static files collected successfully"

# Step 3: Check Django configuration
echo ""
echo "Step 3: Checking Django configuration..."
python manage.py check
if [ $? -ne 0 ]; then
    echo "ERROR: Django configuration check failed"
    exit 1
fi
echo "✓ Django configuration is valid"

echo ""
echo "======================================"
echo "Build completed successfully!"
echo "======================================"
echo ""
echo "Next steps:"
echo "- Migrations will run during release phase"
echo "- Web service will start with Gunicorn"
echo ""
