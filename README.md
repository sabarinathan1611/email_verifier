# Email Verification Service

A lightweight FastAPI service for email deliverability verification, optimized for Docker and cloud deployment.

## Features

- Email syntax validation
- Domain MX record verification
- SMTP connection testing
- Disposable email detection
- Clear deliverability status
- Docker optimized for cloud deployment

## Quick Start with Docker

### Option 1: Using Docker Compose (Recommended)

1. **Build and run the service:**

   ```bash
   docker-compose up --build
   ```

2. **Run in background:**

   ```bash
   docker-compose up -d --build
   ```

3. **Stop the service:**
   ```bash
   docker-compose down
   ```

### Option 2: Using Docker directly

1. **Build the image:**

   ```bash
   docker build -t email-verifier .
   ```

2. **Run the container:**
   ```bash
   docker run -p 8000:8000 email-verifier
   ```

## 🚀 Deploy to Render

### Method 1: Using render.yaml (Recommended)

1. **Push your code to GitHub/GitLab**
2. **Connect your repository to Render**
3. **Render will automatically detect the render.yaml file**
4. **Deploy with one click**

### Method 2: Manual Render Setup

1. **Create a new Web Service on Render**
2. **Connect your Git repository**
3. **Configure the service:**
   - **Environment**: Docker
   - **Build Command**: `docker build -t email-verifier .`
   - **Start Command**: `docker run -p $PORT:8000 -e PORT=$PORT email-verifier`
   - **Health Check Path**: `/docs`

### Render Environment Variables

The service automatically uses Render's `PORT` environment variable. No additional configuration needed.

## API Usage

### Verify Email Endpoint

**POST** `/verify`

**Request Body:**

```json
{
  "email": "user@example.com"
}
```

**Response:**

```json
{
  "email": "user@example.com",
  "status": "deliverable",
  "deliverable": true,
  "confidence": "high",
  "reason": "Email verified successfully",
  "checks": {
    "syntax": true,
    "domain": true,
    "mx_records": true,
    "smtp": true
  }
}
```

## Status Values

- `"deliverable"` - Email is confirmed valid
- `"likely_undeliverable"` - Email likely invalid
- `"undeliverable"` - Email definitely invalid
- `"uncertain"` - Cannot determine

## Confidence Levels

- `"high"` - Very confident in result
- `"medium"` - Moderately confident
- `"low"` - Low confidence

## Access the API

- **API Documentation:** http://localhost:8000/docs (or your Render URL)
- **Alternative Docs:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/docs

## Development

### Local Development (without Docker)

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the service:**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## Docker Optimizations

### Security Features

- Non-root user execution
- Minimal base image (Python 3.11-slim)
- Only essential system dependencies

### Performance Features

- Multi-layer caching
- Optimized .dockerignore
- Health checks included
- Environment variable support

### Image Size

- Base image: ~200MB
- Final image: ~300MB
- Optimized for cloud deployment

## Health Checks

The container includes health checks that monitor the service every 30 seconds. Render will use the `/docs` endpoint for health monitoring.

## Production Considerations

- The service is optimized for Render's environment
- Automatic port detection via `PORT` environment variable
- Health checks ensure service availability
- Non-root user for enhanced security
