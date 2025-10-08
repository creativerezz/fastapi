# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a FastAPI application using Hypercorn as the ASGI server. The application is designed to be deployed to Railway and provides API endpoints for YouTube transcript extraction using the youtube-transcript-api library.

## Development Commands

### Running the application
```bash
# Install dependencies
pip install -r requirements.txt

# Run locally with hot reload
hypercorn main:app --reload

# Run in background (for development)
hypercorn main:app --reload &
```

### Deployment
The application is configured for Railway deployment via `railway.json`:
- Uses NIXPACKS builder
- Start command: `hypercorn main:app --bind "[::]:$PORT"`
- The server binds to IPv6 `[::]` to accept connections on the Railway-provided PORT

## Architecture

### Core Components

**main.py** - Application entry point
- FastAPI app instance (`app = FastAPI()`)
- Root endpoint returns JSON greeting

### YouTube Transcript API Integration

The application is designed to work with the `youtube-transcript-api` library for extracting YouTube video transcripts. Key considerations:

**IP Blocking Workaround:**
- YouTube blocks most cloud provider IPs (AWS, GCP, Azure, etc.)
- Will likely encounter `RequestBlocked` or `IpBlocked` exceptions when deployed
- Solution: Use rotating residential proxies via Webshare

**Using Webshare Proxies:**
```python
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig

ytt_api = YouTubeTranscriptApi(
    proxy_config=WebshareProxyConfig(
        proxy_username="<proxy-username>",
        proxy_password="<proxy-password>",
        filter_ip_locations=["de", "us"],  # optional: limit to specific countries
    )
)
```

**Basic API Usage:**
```python
from youtube_transcript_api import YouTubeTranscriptApi

ytt_api = YouTubeTranscriptApi()

# Fetch transcript (pass video ID, not URL)
fetched_transcript = ytt_api.fetch(video_id, languages=['en', 'de'])

# List available transcripts
transcript_list = ytt_api.list(video_id)

# Find specific transcript types
transcript = transcript_list.find_transcript(['de', 'en'])
transcript = transcript_list.find_manually_created_transcript(['de', 'en'])
transcript = transcript_list.find_generated_transcript(['de', 'en'])

# Translate transcripts
translated_transcript = transcript.translate('de')

# Format output
from youtube_transcript_api.formatters import JSONFormatter, TextFormatter

formatter = JSONFormatter()
json_output = formatter.format_transcript(fetched_transcript)
```

## Dependencies

- **fastapi==0.100.0** - Web framework
- **hypercorn==0.14.4** - ASGI server (chosen over uvicorn for production deployment)

## Important Notes

- Always use `hypercorn` instead of `uvicorn` for consistency with deployment
- When adding YouTube transcript functionality, always configure proxy support to avoid IP bans in production
- Pass video IDs to the transcript API, not full YouTube URLs
- The application expects to bind to a PORT environment variable in production (Railway)
