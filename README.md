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
- **AI-powered transcript summarization** using OpenRouter's free LLMs
- Webshare proxy support for cloud deployments (avoids YouTube IP blocks)
- Multi-language transcript support
- List available transcripts for any video

## 🚀 API Endpoints

- `GET /` - Health check
- `GET /transcript/{video_id}` - Fetch transcript for a video
- `GET /transcript/{video_id}/list` - List all available transcripts
- `GET /transcript/{video_id}/summarize` - **AI summary of transcript** (uses OpenRouter free models)

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
   - `WEBSHARE_PROXY_USERNAME` - Get from [Webshare](https://www.webshare.io/)
   - `WEBSHARE_PROXY_PASSWORD` - Get from [Webshare](https://www.webshare.io/)
   - `OPENROUTER_API_KEY` - Get from [OpenRouter](https://openrouter.ai/keys) (for AI summaries)

### Available Free Models

Choose from 50+ free LLMs on OpenRouter (see `openrouter-free-llms.txt`):
- `google/gemini-2.0-flash-exp:free` - 1M context window
- `deepseek/deepseek-chat-v3.1:free` - 163k context (default)
- `qwen/qwen3-coder:free` - 262k context
- `meta-llama/llama-3.3-70b-instruct:free` - 65k context

## 📖 Example Usage

### Fetch Transcript
```bash
curl "https://api.automatehub.dev/transcript/dQw4w9WgXcQ?languages=en"
```

### List Available Transcripts
```bash
curl "https://api.automatehub.dev/transcript/dQw4w9WgXcQ/list"
```

### AI Summary (Default: DeepSeek V3.1)
```bash
curl "https://api.automatehub.dev/transcript/dQw4w9WgXcQ/summarize"
```

### AI Summary with Specific Model
```bash
curl "https://api.automatehub.dev/transcript/dQw4w9WgXcQ/summarize?model=google/gemini-2.0-flash-exp:free"
```

## 📝 Notes

- To learn about FastAPI, visit the [FastAPI Documentation](https://fastapi.tiangolo.com/tutorial/)
- For Hypercorn configuration, read their [Documentation](https://hypercorn.readthedocs.io/)
- For YouTube Transcript API usage, see [youtube-transcript-api docs](https://pypi.org/project/youtube-transcript-api/)
- For OpenRouter models and pricing, see [OpenRouter Documentation](https://openrouter.ai/docs)
