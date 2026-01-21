# Pre-Deployment Checklist

## TaskMaster - Production Deployment Verification

### ✅ Code Quality
- [x] No syntax errors in Python files
- [x] All imports properly declared
- [x] No circular dependencies
- [x] All required packages in requirements.txt

### ✅ Configuration Files
- [x] Procfile created for Gunicorn
- [x] render.yaml configured for automated deployment
- [x] build.sh ready with build commands
- [x] requirements.txt cleaned (production only)
- [x] requirements-dev.txt for local development

### ✅ Django Settings
- [x] SECRET_KEY uses environment variable
- [x] DEBUG uses environment variable
- [x] ALLOWED_HOSTS configurable via environment
- [x] CSRF_TRUSTED_ORIGINS set
- [x] Database configured with dj-database-url
- [x] WhiteNoise middleware enabled for static files
- [x] Static files configuration correct
- [x] Email backend configured

### ✅ Database
- [x] Migrations created and tested
- [x] Database models complete
- [x] Django signals working (auto profile creation)
- [x] No missing migrations

### ✅ Security
- [x] No hardcoded secrets in code
- [x] SECURE_SSL_REDIRECT available
- [x] SESSION_COOKIE_SECURE available
- [x] CSRF_COOKIE_SECURE available
- [x] CORS headers configured
- [x] SQL injection prevention (using ORM)
- [x] XSS protection via Django templates
- [x] CSRF protection enabled

### ✅ Testing
- [x] All 27 unit tests passing
- [x] No import errors
- [x] Forms validation working
- [x] Authentication flows tested

### ✅ Static Files & Media
- [x] CSS files created and compressed
- [x] Static file paths correct
- [x] WhiteNoise configured
- [x] collectstatic command works

### ✅ Deployment-Specific
- [x] Gunicorn configured in Procfile
- [x] Worker configuration optimized
- [x] Build script includes all steps
- [x] No development-only packages in production requirements

## Environment Variables Required for Render

```
DEBUG = False
ALLOWED_HOSTS = taskmaster.onrender.com
CSRF_TRUSTED_ORIGINS = https://taskmaster.onrender.com
SECRET_KEY = (generate new secure key)
DATABASE_URL = (auto-set by Render PostgreSQL)
```

## Deployment Steps

1. **Create Render Account**
   - Visit render.com
   - Sign in with GitHub

2. **Connect Repository**
   - Click "New +"
   - Select "Web Service"
   - Choose your GitHub repository

3. **Configure Service**
   - Name: `taskmaster`
   - Runtime: Python 3.11
   - Build Command: `pip install --no-cache-dir -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - Start Command: `gunicorn --workers 3 --worker-class sync --max-requests 1000 --max-requests-jitter 50 mysite.wsgi:application`

4. **Add PostgreSQL Database**
   - Click "New +"
   - Select "PostgreSQL"
   - Free tier available

5. **Set Environment Variables**
   - In Render dashboard, click "Environment"
   - Add variables from list above
   - Generate strong SECRET_KEY: 
     ```
     python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
     ```

6. **Deploy**
   - Click "Create Web Service"
   - Monitor build logs
   - Verify no errors
   - Test application

## Monitoring Post-Deployment

- [ ] Visit application URL
- [ ] Test login/registration
- [ ] Test task creation
- [ ] Test static files load (CSS visible)
- [ ] Check Render logs for errors
- [ ] Verify database is connected
- [ ] Test password reset email (check logs)

## Troubleshooting

### Build Failures
- Check build logs in Render dashboard
- Verify all dependencies in requirements.txt
- Ensure no Windows-specific packages
- Test locally: `pip install -r requirements.txt`

### Static Files Not Loading
- Verify STATIC_ROOT is set to 'staticfiles'
- Run: `python manage.py collectstatic --noinput`
- Ensure WhiteNoise middleware is enabled
- Check file permissions

### Database Connection Errors
- Verify DATABASE_URL environment variable is set
- Ensure PostgreSQL database is created
- Check database name and credentials
- Run migrations: `python manage.py migrate`

### 502 Bad Gateway
- Check application logs in Render
- Verify SECRET_KEY is set
- Ensure DEBUG = False
- Check worker processes are running

## Production Checklist (Post-Deploy)

- [ ] All pages loading
- [ ] Static assets (CSS, images) working
- [ ] Login functionality working
- [ ] Task CRUD operations working
- [ ] Database queries performing well
- [ ] No 404/500 errors in logs
- [ ] Email functionality tested
- [ ] Backup strategy in place

---

✅ **Your application is ready for production deployment!**

Current Status: Ready for Render deployment with cleaned requirements and optimized configuration.

Last Updated: January 21, 2026
