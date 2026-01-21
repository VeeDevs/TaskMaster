# 🚀 Deploy TaskMaster to Vercel - Quick Start

## Prerequisites
- ✅ GitHub account (VeeDevs)
- ✅ Vercel account (free tier available)
- ✅ Code pushed to GitHub (Done ✓)

---

## Step 1: Go to Vercel Dashboard

1. **Open Vercel**: https://vercel.com/
2. **Login** with GitHub account (VeeDevs)
3. Click **"New Project"**

---

## Step 2: Import from GitHub

1. Click **"Import from Git Repository"**
2. Search for: **TaskMaster**
3. Select: **VeeDevs/TaskMaster**
4. Click **"Import"**

---

## Step 3: Configure Project

### Environment Variables
1. Scroll to **"Environment Variables"**
2. Add the following:

```
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.vercel.app,localhost
DATABASE_URL=postgresql://user:password@host:5432/db_name
```

**Get values:**
- **SECRET_KEY**: Generate at https://djecrety.ir/
- **DATABASE_URL**: Use PostgreSQL (optional, can use SQLite for testing)
- **ALLOWED_HOSTS**: Will be your Vercel domain (e.g., taskmaster-xyz.vercel.app)

### Build Settings
- **Framework Preset**: Other (already configured)
- **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
- **Output Directory**: `staticfiles`
- **Install Command**: `pip install -r requirements.txt`

---

## Step 4: Deploy

1. **Click "Deploy"**
2. **Wait for build** (2-5 minutes)
3. **Once complete**, you'll see:
   - ✅ Production URL
   - ✅ Visit your deployed app

---

## Step 5: Configure Database (Optional)

For production with real database:

1. **Choose PostgreSQL provider:**
   - Heroku (free tier)
   - ElephantSQL
   - Railway
   - Supabase

2. **Get connection string** and add to Vercel env vars as `DATABASE_URL`

3. **Run migrations on Vercel:**
   - Use Vercel CLI or run migrations in admin

---

## Quick Deployment (No Database Setup)

If you want to test immediately:

1. Skip DATABASE_URL setup
2. Deploy with SQLite (included)
3. Create admin account via Vercel CLI

---

## Post-Deployment

### Access Your App
```
Production URL: https://your-domain.vercel.app/
Admin Panel: https://your-domain.vercel.app/admin/
```

### Create Admin Account
```bash
vercel env pull
python manage.py createsuperuser --noinput --username admin --email admin@example.com
```

### Common Issues

| Issue | Solution |
|-------|----------|
| 502 Bad Gateway | Check env vars, ensure SECRET_KEY is set |
| Static files not loading | collectstatic already runs in build |
| Database errors | Ensure DATABASE_URL is correct |
| Migrations not applied | Use Vercel CLI to run: `vercel env pull` then run migrations |

---

## Vercel CLI Alternative

```powershell
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
vercel
```

---

## Configuration Files (Already Added)

✅ **vercel.json** - Build configuration  
✅ **api/wsgi.py** - WSGI entry point  
✅ **.vercelignore** - Files to exclude  

---

## Environment Variables Reference

```
# Django Settings
DJANGO_SETTINGS_MODULE=mysite.settings
SECRET_KEY=<generate-at-djecrety.ir>
DEBUG=False

# Allowed Hosts
ALLOWED_HOSTS=yourdomain.vercel.app,localhost

# Database (Optional)
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Security
CSRF_TRUSTED_ORIGINS=https://yourdomain.vercel.app

# Admin
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@example.com
```

---

## Status

✅ **Configuration Files**: Added  
✅ **GitHub**: Pushed to origin/docs  
✅ **Ready to Deploy**: Yes  

**Next**: Go to https://vercel.com/ and follow Steps 1-4 above

---

**Deployment Time**: ~5-10 minutes  
**Cost**: Free (with optional upgrades)  
**Support**: Vercel docs at https://vercel.com/docs

