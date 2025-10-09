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
- YouTube transcript extraction with **multiple output formats** (JSON, Text, SRT, VTT)
- **AI-powered transcript analysis** using OpenRouter's free LLMs
- **226 Fabric AI patterns** by Daniel Miessler (analyze, create, extract, improve content)
- Webshare proxy support for cloud deployments (avoids YouTube IP blocks)
- Multi-language transcript support
- List available transcripts for any video

## 🚀 API Endpoints

### Basic Endpoints

- `GET /` - Health check
- `GET /transcript/{video_id}` - Fetch transcript for a video (supports multiple formats)
- `GET /transcript/{video_id}/list` - List all available transcripts
- `GET /transcript/{video_id}/summarize` - **AI summary of transcript** (uses OpenRouter free models)

### 🎨 Fabric AI Pattern Endpoints (NEW!)

- `GET /patterns` - **List all 226 available patterns**
- `GET /transcript/{video_id}/pattern/{pattern_name}` - **Apply any Fabric pattern dynamically**
- `GET /transcript/{video_id}/extract-wisdom` - Extract ideas, insights, quotes, habits, facts, references

**Popular patterns include:**

- `create_summary` - Concise summary with main points
- `extract_ideas` - Extract all ideas from content
- `create_quiz` - Generate quiz questions
- `analyze_paper` - Analyze research papers
- `analyze_debate` - Analyze debate arguments
- `improve_writing` - Improve writing quality
- And 220+ more! See [Fabric Patterns Documentation](docs/fabric-patterns-api.md)

### Output Formats

The `/transcript/{video_id}` endpoint supports multiple output formats via the `format` query parameter:

- **`json`** (default) - Structured JSON with metadata and transcript array
- **`text`** - Plain text with timestamps (e.g., `[00:18] transcript text`)
- **`srt`** - SubRip subtitle format (standard subtitle file)
- **`vtt`** - WebVTT subtitle format (web video text tracks)

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

### Fetch Transcript (JSON format, default)

```bash
curl "https://api.automatehub.dev/transcript/dQw4w9WgXcQ?languages=en"
```

### Fetch Transcript as Plain Text

```bash
curl "https://api.automatehub.dev/transcript/dQw4w9WgXcQ?format=text"
```

### Fetch Transcript as SRT Subtitles

```bash
curl "https://api.automatehub.dev/transcript/dQw4w9WgXcQ?format=srt" > subtitles.srt
```

### Fetch Transcript as WebVTT

```bash
curl "https://api.automatehub.dev/transcript/dQw4w9WgXcQ?format=vtt" > subtitles.vtt
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

### 🎨 Fabric AI Patterns (NEW!)

#### List All Available Patterns

```bash
curl "https://api.automatehub.dev/patterns"
```

#### Apply create_summary Pattern

```bash
curl "https://api.automatehub.dev/transcript/dQw4w9WgXcQ/pattern/create_summary"
```

#### Apply extract_wisdom Pattern

```bash
curl "https://api.automatehub.dev/transcript/dQw4w9WgXcQ/pattern/extract_wisdom"
```

#### Apply analyze_paper Pattern

```bash
curl "https://api.automatehub.dev/transcript/VIDEO_ID/pattern/analyze_paper"
```

#### Create Quiz Questions

```bash
curl "https://api.automatehub.dev/transcript/VIDEO_ID/pattern/create_quiz"
```

**See the [Complete Fabric Patterns Guide](docs/fabric-patterns-api.md) for all 226 patterns organized by category!**

## 📝 Notes

- To learn about FastAPI, visit the [FastAPI Documentation](https://fastapi.tiangolo.com/tutorial/)
- For Hypercorn configuration, read their [Documentation](https://hypercorn.readthedocs.io/)
- For YouTube Transcript API usage, see [youtube-transcript-api docs](https://pypi.org/project/youtube-transcript-api/)
- For OpenRouter models and pricing, see [OpenRouter Documentation](https://openrouter.ai/docs)
