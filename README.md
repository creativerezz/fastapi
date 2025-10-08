---
title: FastAPI YouTube Transcript API
description: A FastAPI server with YouTube transcript extraction
tags:
  - fastapi
  - hypercorn
  - python
  - youtube
---

# FastAPI YouTube Transcript API

A FastAPI application that fetches YouTube video transcripts using the youtube-transcript-api library, with proxy support for cloud deployments.

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/-NvLj4?referralCode=CRJ8FE)

## ✨ Features

- FastAPI REST API
- [Hypercorn](https://hypercorn.readthedocs.io/) ASGI server
- YouTube transcript extraction
- Webshare proxy support for cloud deployments (avoids YouTube IP blocks)
- Multi-language transcript support
- List available transcripts for any video

## 🚀 API Endpoints

- `GET /` - Health check
- `GET /transcript/{video_id}` - Fetch transcript for a video
- `GET /transcript/{video_id}/list` - List all available transcripts

## 💁‍♀️ Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally with hot reload
hypercorn main:app --reload
```

No proxy configuration needed for local development.

## 🚂 Railway Deployment

**Important:** YouTube blocks cloud provider IPs. You'll need Webshare residential proxies for Railway.

See the [Railway Setup Guide](docs/railway-setup.md) for detailed deployment instructions.

Quick setup:
1. Deploy to Railway
2. Add environment variables:
   - `WEBSHARE_PROXY_USERNAME`
   - `WEBSHARE_PROXY_PASSWORD`
3. Get credentials from [Webshare](https://www.webshare.io/)

## 📝 Notes

- To learn about FastAPI, visit the [FastAPI Documentation](https://fastapi.tiangolo.com/tutorial/)
- For Hypercorn configuration, read their [Documentation](https://hypercorn.readthedocs.io/)
- For YouTube Transcript API usage, see [youtube-transcript-api docs](https://pypi.org/project/youtube-transcript-api/)
