# Railway Setup Guide

This guide walks you through deploying this FastAPI application to Railway with YouTube Transcript API support.

## Prerequisites

1. A [Railway account](https://railway.app/)
2. A [Webshare account](https://www.webshare.io/) with a **Residential proxy package** (NOT "Proxy Server" or "Static Residential")

## Why Proxies Are Required

YouTube blocks most cloud provider IPs (AWS, GCP, Azure, Railway, etc.). Without proxies, you'll encounter `RequestBlocked` or `IpBlocked` errors when trying to fetch transcripts from Railway.

## Step 1: Get Webshare Credentials

1. Create a [Webshare account](https://www.webshare.io/)
2. Purchase a **Residential** proxy package (make sure it's NOT "Proxy Server" or "Static Residential")
3. Go to [Webshare Proxy Settings](https://dashboard.webshare.io/proxy/settings)
4. Copy your **Proxy Username** and **Proxy Password**

## Step 2: Deploy to Railway

1. Push your code to a GitHub repository
2. Go to [Railway Dashboard](https://railway.app/dashboard)
3. Click **New Project** → **Deploy from GitHub repo**
4. Select your repository
5. Railway will auto-detect the Python project and deploy it

## Step 3: Configure Environment Variables

In your Railway project:

1. Go to your service → **Variables** tab
2. Add the following environment variables:

```
WEBSHARE_PROXY_USERNAME=your_proxy_username
WEBSHARE_PROXY_PASSWORD=your_proxy_password
```

3. Click **Deploy** to restart with the new variables

## Step 4: Test Your Deployment

Once deployed, Railway will provide a URL like `https://your-app.railway.app`

Test the endpoints:

```bash
# Check if the API is running
curl https://your-app.railway.app/

# List available transcripts for a video
curl https://your-app.railway.app/transcript/dQw4w9WgXcQ/list

# Fetch English transcript
curl https://your-app.railway.app/transcript/dQw4w9WgXcQ?languages=en
```

## API Endpoints

### GET /
Health check endpoint

### GET /transcript/{video_id}
Fetch transcript for a video

**Parameters:**
- `video_id` (path): YouTube video ID (e.g., `dQw4w9WgXcQ`)
- `languages` (query, optional): Comma-separated language codes (default: `en`)

**Example:**
```
https://your-app.railway.app/transcript/dQw4w9WgXcQ?languages=en,de
```

### GET /transcript/{video_id}/list
List all available transcripts for a video

**Parameters:**
- `video_id` (path): YouTube video ID

**Example:**
```
https://your-app.railway.app/transcript/dQw4w9WgXcQ/list
```

## Local Development

For local development, you can run without proxies:

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally (no proxy needed)
hypercorn main:app --reload
```

The app automatically detects if proxy credentials are available and only uses them when set.

## Troubleshooting

### "RequestBlocked" or "IpBlocked" errors
- Ensure you have the correct Webshare credentials set in Railway
- Verify you purchased a **Residential** proxy package (not "Proxy Server")
- Check your Webshare account has available bandwidth

### "No transcript found" errors
- Some videos don't have transcripts available
- Try the `/transcript/{video_id}/list` endpoint first to see available languages
- Specify the correct language codes in the `languages` parameter

### Connection timeouts
- Webshare proxies can occasionally be slow
- Try the request again
- Consider adding timeout handling to your application

## Cost Considerations

- **Railway**: Free tier available, then pay-as-you-go
- **Webshare**: Residential proxies start at ~$15/mo for 1GB bandwidth
  - 1GB ≈ 10,000-50,000 transcript requests depending on transcript size

## Optional: Country Filtering

To reduce latency or work around location-based restrictions, you can filter proxy IPs by country. Update `main.py`:

```python
proxy_config = WebshareProxyConfig(
    proxy_username=proxy_username,
    proxy_password=proxy_password,
    filter_ip_locations=["us", "de"],  # Only use US and Germany IPs
)
```

See [Webshare locations](https://www.webshare.io/features/proxy-locations) for available countries.
