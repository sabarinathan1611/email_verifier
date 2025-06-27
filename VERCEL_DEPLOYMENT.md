# Vercel Deployment Guide

## Prerequisites

1. MongoDB Atlas account (for cloud MongoDB)
2. Vercel account
3. GitHub repository connected to Vercel

## Step 1: Set up MongoDB Atlas

1. Go to [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Create a free cluster
3. Get your connection string
4. Add your IP to the whitelist (or use 0.0.0.0/0 for all IPs)

## Step 2: Deploy to Vercel

### Option A: Using Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel

# Set environment variables
vercel env add MONGODB_URL
```

### Option B: Using Vercel Dashboard

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "New Project"
3. Import your GitHub repository: `sabarinathan1611/email_verifier`
4. Configure project settings:
   - Framework Preset: Other
   - Build Command: Leave empty
   - Output Directory: Leave empty
   - Install Command: `pip install -r requirements.txt`

## Step 3: Set Environment Variables

In Vercel Dashboard:

1. Go to your project settings
2. Navigate to "Environment Variables"
3. Add:
   - Name: `MONGODB_URL`
   - Value: Your MongoDB Atlas connection string
   - Environment: Production, Preview, Development

## Step 4: Deploy

1. Click "Deploy"
2. Wait for deployment to complete
3. Your API will be available at: `https://your-project-name.vercel.app`

## API Endpoints

- `POST /` - Verify email
- `GET /verifications` - Get recent verifications
- `GET /verifications/{email}` - Get verification history for specific email
- `GET /health` - Health check

## Testing

```bash
# Test email verification
curl -X POST "https://your-project-name.vercel.app/" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com"}'

# Test health check
curl "https://your-project-name.vercel.app/health"
```

## Troubleshooting

- Check Vercel function logs for errors
- Ensure MongoDB Atlas connection string is correct
- Verify IP whitelist in MongoDB Atlas
- Check environment variables are set correctly
