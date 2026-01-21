# TaskMaster - Vercel Deployment Guide

## Quick Start

Your TaskMaster Django application is configured for deployment on Vercel.

### Prerequisites
- Vercel account (free at vercel.com)
- GitHub repository (already set up)
- PostgreSQL database (Vercel's storage or external service)

---

## Deployment Steps

### 1. Connect to Vercel

```bash
# Option A: Via Vercel CLI
npm install -g vercel
vercel login
vercel

# Option B: Via Vercel Dashboard
# 1. Go to vercel.com
# 2. Sign in with GitHub
# 3. Click "New Project"
# 4. Select your TaskMaster repository
# 5. Click "Import"
```

### 2. Configure Environment Variables

In Vercel Dashboard → Settings → Environment Variables, add:

```
DEBUG = False
ALLOWED_HOSTS = your-domain.vercel.app
CSRF_TRUSTED_ORIGINS = https://your-domain.vercel.app
SECRET_KEY = (generate new secure key)
DATABASE_URL = (PostgreSQL connection string)
```

#### Generate SECRET_KEY
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 3. Database Setup

**Option A: Vercel Storage (PostgreSQL)**
```
1. Go to Vercel Dashboard
2. Click "Storage" tab
3. Create PostgreSQL database
4. Copy connection string to DATABASE_URL
```

**Option B: External PostgreSQL**
```
Services: Railway, Supabase, Amazon RDS, etc.
Copy connection string to DATABASE_URL environment variable
```

### 4. Deploy

```bash
# Option A: Auto-deploy from GitHub
# Push to GitHub → Vercel auto-deploys

# Option B: Manual deploy
vercel deploy --prod
```

### 5. Run Migrations

After first deployment:

```bash
# Via Vercel CLI
vercel env pull
python manage.py migrate

# Or manually via Vercel Bash
# 1. Vercel Dashboard → Deployments
# 2. Click your deployment
# 3. Click "Bash" or use CLI
# 4. Run: python manage.py migrate
```

---

## File Structure for Vercel

```
TaskMaster/
├── api/
│   └── wsgi.py                 # Vercel WSGI entry point
├── myapp/                      # Django app
├── mysite/                      # Django settings
├── requirements.txt            # Python dependencies
├── vercel.json                 # Vercel configuration
├── manage.py                   # Django management
└── ...other files...
```

---

## Configuration Details

### vercel.json
- `buildCommand`: Installs dependencies and collects static files
- `outputDirectory`: Where static files are stored
- `framework`: Django
- `python.version`: 3.9
- `functions`: WSGI app configuration

### settings.py Updates for Vercel
✅ DEBUG defaults to False (safe for production)
✅ ALLOWED_HOSTS configured via environment
✅ CSRF_TRUSTED_ORIGINS configured
✅ WhiteNoise middleware for static files
✅ Database via dj-database-url (supports DATABASE_URL)

---

## Testing Locally

Before deploying to Vercel, test locally:

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Run server
python manage.py runserver

# Visit http://localhost:8000
```

---

## Vercel-Specific Notes

### Database Migrations
- Vercel doesn't have a "release phase" like Heroku/Render
- Migrations should run during build command
- Or use Vercel Bash to run them manually after deploy

### Static Files
- WhiteNoise middleware serves CSS/JS/images
- `collectstatic` runs during build
- Files collected to `staticfiles/` directory

### Media Files
- Vercel's serverless doesn't have persistent storage
- Use external service for uploads (S3, Cloudinary, etc.)
- Or disable media uploads for now

### Cold Starts
- Vercel may have cold start latency
- First request might take 5-10 seconds
- Subsequent requests are fast

---

## Troubleshooting

### Issue: Database Connection Error
```
Solution:
1. Verify DATABASE_URL environment variable is set
2. Check PostgreSQL database exists and is accessible
3. Ensure IP whitelist allows Vercel IPs
```

### Issue: Static Files 404
```
Solution:
1. Verify WHITE_NOISE middleware is enabled in settings
2. Check collectstatic runs in build command
3. Verify STATIC_ROOT is set to 'staticfiles'
```

### Issue: ALLOWED_HOSTS Error
```
Solution:
1. Set ALLOWED_HOSTS environment variable in Vercel
2. Include your domain (your-domain.vercel.app)
3. Restart deployment after setting variables
```

### Issue: Import ModuleNotFoundError
```
Solution:
1. Verify all packages in requirements.txt
2. Run: pip freeze > requirements.txt locally
3. Test locally before deploying
```

---

## Post-Deployment Checklist

- [ ] Visit deployed URL (should show home page)
- [ ] Register new account (test form)
- [ ] Log in (test authentication)
- [ ] Create a task (test database)
- [ ] Check CSS loads (test static files)
- [ ] Check mobile responsive (test on phone)
- [ ] Review logs in Vercel dashboard
- [ ] Set up custom domain (optional)

---

## Monitoring

### View Logs
```bash
vercel logs your-project-name
# or via Dashboard → Deployments → Logs
```

### View Metrics
```
Vercel Dashboard → Deployments → Metrics
- Build time
- Function runtime
- Cold start duration
```

---

## Next Steps

1. ✅ Configure environment variables in Vercel
2. ✅ Set up PostgreSQL database
3. ✅ Deploy (auto or manual)
4. ✅ Run migrations
5. ✅ Test all features
6. ✅ Set up custom domain (optional)
7. ✅ Monitor logs and performance

---

## Performance Tips

### Optimize for Vercel
- Images: Use Vercel Image Optimization
- Caching: Set proper cache headers
- Database: Use connection pooling (PgBouncer)
- Static: Use CDN for assets

### Django Optimization
- Use `django-cors-headers` for CORS
- Enable gzip compression
- Optimize database queries
- Use caching middleware

---

## Support

- **Vercel Docs**: https://vercel.com/docs
- **Django Docs**: https://docs.djangoproject.com
- **PostgreSQL Docs**: https://www.postgresql.org/docs

---

**Your TaskMaster app is ready for Vercel deployment!** 🚀

Last Updated: January 21, 2026
