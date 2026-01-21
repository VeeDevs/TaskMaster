# Deploy to Vercel via Terminal - Quick Guide

## Option 1: Interactive Deployment (Recommended)

Run this command to start the interactive deployment process:

```bash
npx vercel --prod
```

This will:
1. Ask you to log in to Vercel (opens browser)
2. Link your project to Vercel
3. Ask about build settings (use defaults)
4. Ask about environment variables
5. Deploy your app
6. Give you the production URL

## Option 2: Using Environment Token

If you have a Vercel token, set it first:

```bash
set VERCEL_TOKEN=your_token_here
npx vercel --prod --token %VERCEL_TOKEN%
```

## Option 3: Using .vercelignore and vercel.json

Your project already has:
- ✓ vercel.json - Build configuration
- ✓ api/wsgi.py - WSGI entry point
- ✓ .vercelignore - Build optimization
- ✓ requirements.txt - All dependencies

## Step-by-Step Terminal Deployment

### Step 1: Install Vercel CLI (if not already installed)
```bash
npm install -g vercel
```

### Step 2: Navigate to project
```bash
cd c:\Users\HP 280\work\TaskMaster
```

### Step 3: Deploy to production
```bash
npx vercel --prod
```

### Step 4: Follow prompts
- Confirm you want to link to Vercel account
- Confirm project settings
- Add environment variables when asked:
  - SECRET_KEY (from https://djecrety.ir/)
  - ALLOWED_HOSTS (your-domain.vercel.app)

### Step 5: Monitor deployment
After deployment, you'll get:
- Production URL (e.g., taskmaster.vercel.app)
- Deployment ID
- Log access

## If You're Having Permission Issues

PowerShell execution policy is blocking scripts. Use cmd.exe instead:

```bash
cmd.exe /c "cd /d c:\Users\HP 280\work\TaskMaster && npx vercel --prod"
```

## Vercel Configuration Already Set

Your vercel.json has:
- Build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
- Framework: Django
- WSGI function: api/wsgi.py
- Output directory: staticfiles

## Need Help?

1. Check Vercel logs: `npx vercel logs`
2. View project settings: `npx vercel env`
3. Get more info: `npx vercel --help`

---

**Ready to deploy?** Run: `npx vercel --prod`
