#!/usr/bin/env python
"""
Vercel Deployment Readiness Checker
Validates that all required configurations are in place for Vercel deployment
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if Path(filepath).exists():
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} NOT FOUND")
        return False

def check_settings_config():
    """Check Django settings configuration"""
    settings_file = Path('mysite/settings.py')
    if not settings_file.exists():
        return False
    
    content = settings_file.read_text()
    checks = {
        'Environment variable imports': 'import os' in content,
        'SECRET_KEY from environment': "os.environ.get" in content and "SECRET_KEY" in content,
        'DEBUG from environment': "os.environ.get('DEBUG'" in content,
        'ALLOWED_HOSTS from environment': "os.environ.get('ALLOWED_HOSTS'" in content,
        'WhiteNoise middleware': 'whitenoise.middleware.WhiteNoiseMiddleware' in content,
        'Production security settings': 'SECURE_SSL_REDIRECT' in content,
        'CSRF_TRUSTED_ORIGINS': 'CSRF_TRUSTED_ORIGINS' in content,
        'Static files configuration': 'STATIC_ROOT' in content,
    }
    
    all_passed = True
    for check_name, passed in checks.items():
        if passed:
            print(f"✅ {check_name}")
        else:
            print(f"❌ {check_name}")
            all_passed = False
    
    return all_passed

def check_requirements():
    """Check if all required packages are in requirements.txt"""
    req_file = Path('requirements.txt')
    if not req_file.exists():
        print("❌ requirements.txt not found")
        return False
    
    # Try different encodings
    content = None
    for encoding in ['utf-16', 'utf-8', 'latin-1', 'cp1252']:
        try:
            with open(req_file, 'r', encoding=encoding) as f:
                content = f.read()
                break
        except:
            continue
    
    if content is None:
        print("❌ Could not read requirements.txt")
        return False
    
    required_packages = [
        ('Django', 'Django'),
        ('whitenoise', 'whitenoise'),
        ('python-dotenv', 'python-dotenv'),
        ('dj-database-url', 'dj-database-url'),
        ('gunicorn', 'gunicorn'),
    ]
    
    all_found = True
    for name, search_term in required_packages:
        if search_term in content:
            print(f"✅ {name}")
        else:
            print(f"❌ {name} NOT in requirements.txt")
            all_found = False
    
    return all_found

def check_vercel_config():
    """Check Vercel configuration"""
    config_file = Path('vercel.json')
    if not config_file.exists():
        print("❌ vercel.json not found")
        return False
    
    content = config_file.read_text()
    checks = {
        'Build command configured': 'buildCommand' in content,
        'WSGI entry point configured': 'api/wsgi.py' in content,
        'Output directory set': 'outputDirectory' in content,
        'Rewrites configured': 'rewrites' in content,
    }
    
    all_passed = True
    for check_name, passed in checks.items():
        if passed:
            print(f"✅ {check_name}")
        else:
            print(f"❌ {check_name}")
            all_passed = False
    
    return all_passed

def main():
    """Run all checks"""
    print("=" * 60)
    print("Vercel Deployment Readiness Checker")
    print("=" * 60)
    print()
    
    results = []
    
    print("📄 Checking Configuration Files:")
    print("-" * 60)
    results.append(check_file_exists('vercel.json', 'Vercel config'))
    results.append(check_file_exists('requirements.txt', 'Requirements'))
    results.append(check_file_exists('.env.example', 'Environment example'))
    results.append(check_file_exists('.vercelignore', 'Vercel ignore'))
    results.append(check_file_exists('api/wsgi.py', 'WSGI application'))
    results.append(check_file_exists('mysite/settings.py', 'Django settings'))
    print()
    
    print("⚙️ Checking Django Settings:")
    print("-" * 60)
    results.append(check_settings_config())
    print()
    
    print("📦 Checking Requirements.txt:")
    print("-" * 60)
    results.append(check_requirements())
    print()
    
    print("🔧 Checking Vercel Configuration:")
    print("-" * 60)
    results.append(check_vercel_config())
    print()
    
    if all(results):
        print("=" * 60)
        print("✅ ALL CHECKS PASSED - Ready for Vercel Deployment!")
        print("=" * 60)
        return 0
    else:
        print("=" * 60)
        print("❌ Some checks failed - Please review above")
        print("=" * 60)
        return 1

if __name__ == '__main__':
    sys.exit(main())
