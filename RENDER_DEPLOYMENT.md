# Render Deployment Guide for TaskMaster

## Step 1: Prepare Your Repository
Your files are already configured:
- ✅ `Procfile` - Specifies how to run the application
- ✅ `render.yaml` - Render deployment configuration
- ✅ `build.sh` - Build script for Render
- ✅ `requirements.txt` - Updated with production dependencies
- ✅ `settings.py` - Configured for production

## Step 2: Deploy to Render

### Option A: Automatic Deployment (Recommended)

1. **Go to [Render.com](https://render.com)**
   - Sign in with GitHub account

2. **Connect Your Repository**
   - Click "New +"
   - Select "Web Service"
   - Choose "Deploy an existing repository"
   - Select your TaskMaster repository

3. **Configure the Service**
   - Name: `taskmaster`
   - Runtime: `Python 3.9`
   - Build Command: `pip install --no-cache-dir -r requirements.txt && python manage.py collectstatic --noinput`
   - Start Command: `gunicorn --workers 3 --worker-class sync --max-requests 1000 --max-requests-jitter 50 mysite.wsgi:application`
   - Instance Type: `Free`
   - **Important**: The Procfile includes a release command that runs migrations automatically before the web service starts

4. **Add Environment Variables**
   Click "Advanced" and add these variables:
   ```
   DEBUG = False
   ALLOWED_HOSTS = yourdomain.onrender.com
   CSRF_TRUSTED_ORIGINS = https://yourdomain.onrender.com
   SECRET_KEY = (Generate a new secure key)
   DATABASE_URL = (Auto-populated by Render when you add a PostgreSQL database)
   ```

5. **Add PostgreSQL Database**
   - In Render dashboard, click "New +"
   - Select "PostgreSQL"
   - Name: `taskmaster-db`
   - Region: Select your preferred region
   - Instance Type: `Free`
   - Connect it to your web service

6. **Deploy**
   - Click "Create Web Service"
   - Render will automatically deploy when you push to GitHub
   - Wait for build to complete (5-10 minutes)

### Option B: Using render.yaml (Blueprint)

1. **Push your code to GitHub**:
   ```bash
   git add .
   git commit -m "Setup Render deployment"
   git push origin main
   ```

2. **Go to [Render.com](https://render.com/blueprints)**
   - Click "New Blueprint Instance"
   - Select your repository
   - Click "Apply"
   - Set environment variables if needed

## Step 3: Verify Deployment

1. **Check Build Logs**
   - In Render dashboard, go to your service
   - Click "Logs" tab
   - Verify no errors during build

2. **Test Your Application**
   - Visit: `https://yourdomain.onrender.com`
   - You should see your TaskMaster home page
   - Try registering a new account
   - Test all features

## Step 4: Generate a Secure SECRET_KEY

Run this Python command to generate a strong secret key:

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Copy the output and set it as the `SECRET_KEY` environment variable in Render.

## Important Notes

1. **Database Persistence**
   - Render's free PostgreSQL is deleted after 90 days of inactivity
   - For production, upgrade to paid tier
   - Data is saved in the PostgreSQL database, not in code

2. **Static Files**
   - WhiteNoise middleware handles serving CSS, JS, and images
   - No additional configuration needed
   - Run `python manage.py collectstatic` during build (already in build command)

3. **Email Configuration**
   - Currently using Django console backend (prints to logs)
   - For production, update EMAIL_BACKEND in settings.py to use SendGrid, Mailgun, etc.

4. **Automatic Redeployment**
   - Every push to GitHub automatically triggers a new deployment
   - Monitor the Logs tab for any errors

5. **Logs and Debugging**
   - View real-time logs in Render dashboard
   - Check "Events" tab for deployment history

## Rollback

If something goes wrong:
1. Go to Render dashboard
2. Click your service
3. Go to "Deployments" tab
4. Click "Redeploy" on a previous deployment
5. Or push a fix to GitHub for a new deployment

## Next Steps

- ✅ Deploy to Render
- ✅ Test all functionality
- ✅ Set up a custom domain (optional)
- ✅ Configure email backend for production
- ✅ Add backup strategy for database
- ✅ Monitor logs and performance

## Troubleshooting

**Issue: Build fails**
- Check build logs for specific error
- Ensure all imports in code are installed in requirements.txt
- Verify no syntax errors

**Issue: 502 Bad Gateway**
- Check that all environment variables are set
- Verify database is running and connected
- Check application logs

**Issue: Static files not showing**
- Ensure `python manage.py collectstatic` runs
- Verify STATIC_ROOT is set to `staticfiles`
- Clear browser cache

**Issue: Database errors**
- Ensure DATABASE_URL is set correctly
- Run migrations: `python manage.py migrate` (should happen in build)
- Check PostgreSQL database is created and running

---

Your TaskMaster application is now ready for production deployment! 🚀
