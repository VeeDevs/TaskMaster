# TaskMaster Production Debugging Guide

## Current Status

**Live URL:** https://taskmaster-smv8.onrender.com

## Common Render Deployment Issues & Fixes

### Issue 1: Database Connection Error
**Error:** `no such table: auth_user`
**Status:** ✅ FIXED
**Solution:** Release phase in Procfile now handles migrations

### Issue 2: ALLOWED_HOSTS Error
**Error:** `Invalid HTTP_HOST header`
**Status:** ✅ FIXED
**Solution:** Updated settings to accept all hosts with `ALLOWED_HOSTS = ['*']`

### Issue 3: Static Files Not Loading
**Error:** CSS/images returning 404
**Status:** ✅ FIXED
**Solution:** WhiteNoise middleware configured for static file serving

### Issue 4: Secret Key in Production
**Status:** ✅ FIXED
**Action:** Make sure to set SECRET_KEY environment variable in Render

---

## Production Checklist

### Environment Variables (Set in Render Dashboard)
```
DEBUG = False              (Safety: defaults to False)
SECRET_KEY = <strong-key>  (Generate new key for production)
ALLOWED_HOSTS = *          (Accepts all hosts)
```

### Deployment Files
- ✅ `Procfile` - Release and web processes
- ✅ `deploy.sh` - Build script with error checking
- ✅ `requirements.txt` - Production dependencies only
- ✅ `build.sh` - Collectstatic and pre-build checks
- ✅ `mysite/settings.py` - Production configuration

### Database
- ✅ PostgreSQL configured via dj-database-url
- ✅ Migrations run in release phase
- ✅ Tables auto-created on first deploy

### Static Files
- ✅ WhiteNoise middleware enabled
- ✅ STATIC_ROOT = 'staticfiles'
- ✅ collectstatic runs during build

---

## Render Deployment Process

### Build Phase
1. Clone repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run `python manage.py collectstatic --noinput`
4. Collect custom checks (no errors expected)

### Release Phase
1. Run `python manage.py migrate --noinput`
2. Run `python manage.py check` (verify config)
3. Tables created in PostgreSQL database

### Web Phase
1. Start Gunicorn: `gunicorn mysite.wsgi:application --bind 0.0.0.0:$PORT --workers 3`
2. Listen on PORT environment variable (auto-set by Render)
3. Serve requests

---

## Monitoring & Debugging

### View Logs
1. Go to Render dashboard
2. Select TaskMaster service
3. Click "Logs" tab
4. Check for errors during deployment

### Common Log Messages

**Good (Success):**
```
==> Build successful
==> Deploying
==> Release command executed
==> Web service started
```

**Bad (Errors to Fix):**
```
ERROR: package not found
ModuleNotFoundError
Syntax error
Database connection error
No such table
```

### Debug Commands (Run in Render Shell)

```bash
# Check configuration
python manage.py check

# Check database connection
python manage.py dbshell

# List tables
python manage.py showmigrations

# Check static files
python manage.py findstatic styles.css
```

---

## Common Issues & Solutions

### Issue: ModuleNotFoundError
**Cause:** Missing package in requirements.txt
**Solution:** 
1. Check requirements.txt has all imports
2. Use only production packages (no dev-only)
3. Ensure psycopg2-binary is in requirements

### Issue: Static Files 404
**Cause:** collectstatic didn't run
**Solution:**
1. Ensure `python manage.py collectstatic --noinput` in build command
2. Verify STATIC_ROOT = BASE_DIR / 'staticfiles'
3. Check WhiteNoise middleware is enabled

### Issue: Migrations Not Running
**Cause:** Missing release phase
**Solution:**
1. Add to Procfile: `release: python manage.py migrate --noinput`
2. This runs BEFORE web service starts
3. Ensures tables exist before requests

### Issue: Database Connection Error
**Cause:** DATABASE_URL not set
**Solution:**
1. Render auto-sets DATABASE_URL with PostgreSQL
2. Verify dj-database-url is installed
3. Ensure database exists in Render

### Issue: ALLOWED_HOSTS Error
**Cause:** Domain not in ALLOWED_HOSTS
**Solution:**
1. Use ALLOWED_HOSTS = ['*'] for development
2. For production, set specific domains
3. Update CSRF_TRUSTED_ORIGINS too

---

## Performance Optimization

### Gunicorn Workers
- Current: 3 workers (good for free tier)
- Production: 4 × CPU cores
- Adjust in Procfile

### Database
- Free tier: Auto-sleeps after inactivity
- Production: Upgrade to Starter plan
- Backup: Available on all plans

### Static Files
- WhiteNoise handles compression
- Enable gzip for faster serving
- Cache-busting via filenames

---

## Security Checklist

- [ ] SECRET_KEY set to random value (not default)
- [ ] DEBUG = False in production
- [ ] ALLOWED_HOSTS configured properly
- [ ] CSRF_TRUSTED_ORIGINS includes your domain
- [ ] HTTPS enforced (auto by Render)
- [ ] Database password strong
- [ ] No secrets in code (use env vars)
- [ ] SQL injection prevention (ORM used)
- [ ] XSS protection (Django templates)

---

## Post-Deployment Testing

### Basic Tests
1. [ ] Visit home page - should load
2. [ ] Click login - should show form
3. [ ] Register new user - should create account
4. [ ] Log in - should redirect to home
5. [ ] Create task - should save to database
6. [ ] View CSS styling - should load
7. [ ] Log out - should work

### Mobile Tests
1. [ ] Open on iPhone - responsive layout
2. [ ] Open on Android - responsive layout
3. [ ] Test on tablet - wider layout works
4. [ ] Forms work on mobile - no layout issues

### Performance Tests
1. [ ] Home page loads < 3s
2. [ ] No 500 errors in logs
3. [ ] No missing static files (404)
4. [ ] Database queries fast

---

## Emergency Procedures

### If App Crashes
1. Go to Render dashboard
2. Check "Logs" for error message
3. Fix code locally
4. Push to GitHub
5. Render auto-redeploys

### If Database Corrupted
1. Create backup in Render
2. Delete existing database
3. Render auto-creates new one
4. Run migrations via release phase
5. Data resets (OK for free tier)

### If Need to Rollback
1. Go to "Deployments" tab in Render
2. Click "Redeploy" on previous deploy
3. App reverts to previous state
4. GitHub push creates new deploy

---

## Next Steps

1. ✅ Verify all files committed to GitHub
2. ✅ Check Render logs for successful deploy
3. ✅ Test core functionality
4. ✅ Monitor for errors
5. 🔄 Consider upgrading plans for production

---

**For issues not covered here, check:**
- [Django Deployment Documentation](https://docs.djangoproject.com/en/4.2/howto/deployment/)
- [Render Documentation](https://render.com/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

Last Updated: January 21, 2026
