# YouTube Transcript API - Complete Reference

## Base URL

```
Production: https://fastapi-youtube-transcript.up.railway.app
Local: http://127.0.0.1:8000
```

## Table of Contents

1. [Root Endpoint](#root-endpoint)
2. [Get Transcript](#get-transcript)
3. [List Available Transcripts](#list-available-transcripts)
4. [Summarize Transcript](#summarize-transcript)
5. [Extract Wisdom](#extract-wisdom)
6. [Chat About Video](#chat-about-video)
7. [Search YouTube Videos](#search-youtube-videos)
8. [Error Codes](#error-codes)
9. [Available Models](#available-models)

---

## Root Endpoint

### GET /

Returns API status and basic information.

**Response:**
```json
{
  "message": "YouTube Transcript API"
}
```

**Example:**
```bash
curl https://fastapi-youtube-transcript.up.railway.app/
```

---

## Get Transcript

### GET /transcript/{video_id}

Fetches the transcript for a YouTube video.

**Path Parameters:**
- `video_id` (required) - YouTube video ID (e.g., "dQw4w9WgXcQ")

**Query Parameters:**
- `languages` (optional) - Comma-separated language codes (default: "en")
- `format` (optional) - Output format: `json`, `text`, `srt`, `vtt`, `sbv` (default: "json")

**Response (JSON format):**
```json
{
  "video_id": "dQw4w9WgXcQ",
  "language": "English",
  "transcript": [
    {
      "text": "Hello everyone",
      "start": 0.0,
      "duration": 2.5
    },
    {
      "text": "Welcome to the video",
      "start": 2.5,
      "duration": 3.0
    }
  ]
}
```

**Response (text format):**
```
Hello everyone
Welcome to the video
...
```

**Response (srt format):**
```
1
00:00:00,000 --> 00:00:02,500
Hello everyone

2
00:00:02,500 --> 00:00:05,500
Welcome to the video
```

**Examples:**

```bash
# Default JSON format
curl "https://fastapi-youtube-transcript.up.railway.app/transcript/dQw4w9WgXcQ"

# Text format
curl "https://fastapi-youtube-transcript.up.railway.app/transcript/dQw4w9WgXcQ?format=text"

# SRT format for subtitles
curl "https://fastapi-youtube-transcript.up.railway.app/transcript/dQw4w9WgXcQ?format=srt"

# Multiple languages preference
curl "https://fastapi-youtube-transcript.up.railway.app/transcript/dQw4w9WgXcQ?languages=en,es,fr"
```

**Error Responses:**
- `404` - Transcripts disabled or video not found
- `500` - Server error

---

## List Available Transcripts

### GET /transcript/{video_id}/list

Lists all available transcripts for a video (manual and auto-generated).

**Path Parameters:**
- `video_id` (required) - YouTube video ID

**Response:**
```json
{
  "video_id": "dQw4w9WgXcQ",
  "available_transcripts": [
    {
      "language": "English",
      "language_code": "en",
      "is_generated": false,
      "is_translatable": true
    },
    {
      "language": "Spanish",
      "language_code": "es",
      "is_generated": true,
      "is_translatable": true
    }
  ]
}
```

**Example:**
```bash
curl "https://fastapi-youtube-transcript.up.railway.app/transcript/dQw4w9WgXcQ/list"
```

---

## Summarize Transcript

### POST /transcript/{video_id}/summarize

Generates an AI-powered summary of the video transcript.

**Path Parameters:**
- `video_id` (required) - YouTube video ID

**Query Parameters:**
- `languages` (optional) - Comma-separated language codes (default: "en")
- `model` (optional) - OpenRouter model ID (default: from MODEL_ID env var)

**Request Body:**
```json
{
  "custom_prompt": "Optional: Custom instructions for the AI"
}
```

**Response:**
```json
{
  "video_id": "dQw4w9WgXcQ",
  "language": "English",
  "model": "meta-llama/llama-3.3-70b-instruct:free",
  "summary": "This video discusses... [AI-generated summary]",
  "fallback_used": false,
  "usage": {
    "prompt_tokens": 2847,
    "completion_tokens": 312,
    "total_tokens": 3159
  }
}
```

**Examples:**

```bash
# Basic summary
curl -X POST "https://fastapi-youtube-transcript.up.railway.app/transcript/dQw4w9WgXcQ/summarize" \
  -H "Content-Type: application/json" \
  -d '{}'

# Custom prompt
curl -X POST "https://fastapi-youtube-transcript.up.railway.app/transcript/dQw4w9WgXcQ/summarize" \
  -H "Content-Type: application/json" \
  -d '{
    "custom_prompt": "Provide a technical summary focusing on the coding concepts discussed"
  }'

# Specific model
curl -X POST "https://fastapi-youtube-transcript.up.railway.app/transcript/dQw4w9WgXcQ/summarize?model=google/gemini-2.0-flash-exp:free" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Default Prompt:**
The AI uses a comprehensive default prompt that extracts:
- Main topics and themes
- Key points and insights
- Actionable takeaways
- Important quotes or examples

---

## Extract Wisdom

### POST /transcript/{video_id}/extract_wisdom

Uses the Fabric "extract_wisdom" pattern to extract insights, ideas, quotes, habits, facts, references, and recommendations from the video.

**Path Parameters:**
- `video_id` (required) - YouTube video ID

**Query Parameters:**
- `languages` (optional) - Comma-separated language codes (default: "en")
- `model` (optional) - OpenRouter model ID (default: from MODEL_ID env var)

**Request Body:**
```json
{
  "custom_prompt": "Optional: Custom extraction instructions"
}
```

**Response:**
```json
{
  "video_id": "dQw4w9WgXcQ",
  "language": "English",
  "model": "meta-llama/llama-3.3-70b-instruct:free",
  "wisdom": {
    "summary": "Brief overview...",
    "ideas": [
      "Key idea 1",
      "Key idea 2"
    ],
    "insights": [
      "Important insight 1",
      "Important insight 2"
    ],
    "quotes": [
      "Memorable quote 1",
      "Memorable quote 2"
    ],
    "habits": [
      "Recommended habit 1"
    ],
    "facts": [
      "Interesting fact 1"
    ],
    "references": [
      "Book/resource mentioned 1"
    ],
    "recommendations": [
      "Action item 1"
    ]
  },
  "fallback_used": false,
  "usage": {
    "prompt_tokens": 3521,
    "completion_tokens": 876,
    "total_tokens": 4397
  }
}
```

**Example:**
```bash
curl -X POST "https://fastapi-youtube-transcript.up.railway.app/transcript/jNQXAC9IVRw/extract_wisdom" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Use Cases:**
- Content curation
- Note-taking and knowledge management
- Research and learning
- Extracting actionable insights
- Finding references and resources

---

## Chat About Video

### POST /transcript/{video_id}/chat

Have conversational interactions with AI about any YouTube video using the full transcript as context.

**Path Parameters:**
- `video_id` (required) - YouTube video ID

**Query Parameters:**
- `languages` (optional) - Comma-separated language codes (default: "en")
- `model` (optional) - OpenRouter model ID (default: from MODEL_ID env var)

**Request Body:**
```json
{
  "message": "Your question about the video",
  "conversation_history": [
    {
      "role": "user",
      "content": "Previous question"
    },
    {
      "role": "assistant",
      "content": "Previous answer"
    }
  ]
}
```

**Response:**
```json
{
  "video_id": "dQw4w9WgXcQ",
  "language": "English",
  "model": "meta-llama/llama-3.3-70b-instruct:free",
  "user_message": "What are the main points discussed?",
  "assistant_response": "Based on the transcript, the main points are...",
  "fallback_used": false,
  "usage": {
    "prompt_tokens": 2847,
    "completion_tokens": 312,
    "total_tokens": 3159
  }
}
```

**Examples:**

```bash
# Simple question
curl -X POST "https://fastapi-youtube-transcript.up.railway.app/transcript/dQw4w9WgXcQ/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are the main topics discussed?"
  }'

# Follow-up with history
curl -X POST "https://fastapi-youtube-transcript.up.railway.app/transcript/dQw4w9WgXcQ/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Can you elaborate on that?",
    "conversation_history": [
      {"role": "user", "content": "What are the main topics?"},
      {"role": "assistant", "content": "The main topics are X, Y, and Z"}
    ]
  }'
```

**Best Practices:**
- Be specific with questions
- Reference timestamps when relevant
- Use conversation history for context
- Keep history to last 5-10 exchanges for performance

[See detailed chat API documentation](./chat-api.md)

---

## Search YouTube Videos

### GET /search

Search for YouTube videos and get their video IDs for use with other endpoints.

**Query Parameters:**
- `q` (required) - Search query
- `max_results` (optional) - Number of results (1-50, default: 10)
- `order` (optional) - Sort order: `relevance`, `date`, `rating`, `viewCount`, `title` (default: "relevance")

**Response:**
```json
{
  "query": "python tutorial",
  "max_results": 10,
  "order": "relevance",
  "results": [
    {
      "video_id": "dQw4w9WgXcQ",
      "title": "Python Tutorial for Beginners",
      "channel": "Tech Channel",
      "published_at": "2024-01-15T10:30:00Z",
      "description": "Learn Python programming...",
      "thumbnail": "https://i.ytimg.com/vi/dQw4w9WgXcQ/default.jpg",
      "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    }
  ]
}
```

**Examples:**

```bash
# Basic search
curl "https://fastapi-youtube-transcript.up.railway.app/search?q=python+tutorial"

# More results
curl "https://fastapi-youtube-transcript.up.railway.app/search?q=machine+learning&max_results=25"

# Sort by date (newest first)
curl "https://fastapi-youtube-transcript.up.railway.app/search?q=ai+news&order=date"

# Sort by view count
curl "https://fastapi-youtube-transcript.up.railway.app/search?q=viral+video&order=viewCount"
```

**Use Cases:**
- Find videos by topic
- Get video IDs for batch processing
- Build video discovery features
- Content research and curation

---

## Error Codes

### Common HTTP Status Codes

- `200` - Success
- `400` - Bad Request (invalid parameters)
- `404` - Not Found (video doesn't exist or transcripts disabled)
- `422` - Validation Error (invalid request body)
- `500` - Internal Server Error
- `503` - Service Unavailable (all AI models rate-limited)
- `504` - Gateway Timeout

### Error Response Format

```json
{
  "detail": "Transcripts are disabled for this video"
}
```

### Specific Error Messages

**Transcript Errors:**
- "Transcripts are disabled for this video"
- "No transcript found for this video in the specified language(s)"
- "Video unavailable"

**API Errors:**
- "OpenRouter API key not configured"
- "Message field is required"
- "YouTube API key not configured"
- "Search query parameter 'q' is required"

**AI Model Errors:**
- "All models failed. Please try again later." (503 status)
- "Error calling OpenRouter API"

---

## Available Models

### Free Models (Default)

The API uses free OpenRouter models with automatic fallback:

**Primary Model:**
- `meta-llama/llama-3.3-70b-instruct:free` (Default)

**Fallback Models (in order):**
1. `deepseek/deepseek-v3.1-free` - Large context, good reasoning
2. `qwen/qwen3-coder:free` - Code-focused, technical content
3. `google/gemini-2.0-flash-exp:free` - 1M context window
4. `google/gemini-2.5-flash:free` - Latest Gemini with vision
5. `mistralai/mistral-7b-instruct:free` - Fast, efficient
6. `google/gemma-2-9b-it:free` - Balanced performance
7. `meta-llama/llama-3.1-8b-instruct:free` - Lightweight

### Model Recommendations

**Short videos (< 10 min):**
- Any model works well
- Mistral 7B or Gemma 2 for speed

**Medium videos (10-30 min):**
- Llama 3.3 70B (default)
- DeepSeek V3.1
- Qwen3 Coder

**Long videos (30+ min):**
- Gemini 2.0 Flash (1M context)
- DeepSeek V3.1

**Technical content:**
- Qwen3 Coder
- DeepSeek V3.1
- Llama 3.3 70B

### Using Custom Models

You can specify any OpenRouter model:

```bash
curl -X POST "https://fastapi-youtube-transcript.up.railway.app/transcript/VIDEO_ID/summarize?model=anthropic/claude-3.5-sonnet" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Note:** Paid models require OpenRouter credits. Free models have rate limits.

---

## Rate Limits & Performance

### Timeouts
- AI endpoints: 60 seconds
- Transcript fetch: 30 seconds

### Best Practices
1. **Cache results** - Store transcripts and summaries to avoid repeated API calls
2. **Use appropriate models** - Match model to video length and complexity
3. **Batch operations** - Process multiple videos during off-peak hours
4. **Handle errors gracefully** - Implement retry logic with exponential backoff

### Context Limits
- **Mistral 7B**: 8K tokens
- **Gemma 2**: 8K tokens
- **Llama 3.1/3.3**: 128K tokens
- **DeepSeek V3.1**: 64K tokens
- **Qwen3 Coder**: 32K tokens
- **Gemini 2.0 Flash**: 1M tokens

---

## Authentication

Currently, no authentication is required for public endpoints. The API uses server-side API keys for:
- OpenRouter API (for AI models)
- YouTube Data API v3 (for search)
- Webshare proxies (for transcript fetching)

---

## Integration Examples

### Python

```python
import requests

BASE_URL = "https://fastapi-youtube-transcript.up.railway.app"

# Get transcript
response = requests.get(f"{BASE_URL}/transcript/dQw4w9WgXcQ")
transcript = response.json()

# Summarize
response = requests.post(
    f"{BASE_URL}/transcript/dQw4w9WgXcQ/summarize",
    json={"custom_prompt": "Focus on key takeaways"}
)
summary = response.json()

# Chat
response = requests.post(
    f"{BASE_URL}/transcript/dQw4w9WgXcQ/chat",
    json={"message": "What are the main points?"}
)
answer = response.json()
```

### JavaScript/TypeScript

```typescript
const BASE_URL = "https://fastapi-youtube-transcript.up.railway.app";

// Get transcript
const transcript = await fetch(`${BASE_URL}/transcript/dQw4w9WgXcQ`)
  .then(r => r.json());

// Summarize
const summary = await fetch(
  `${BASE_URL}/transcript/dQw4w9WgXcQ/summarize`,
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({})
  }
).then(r => r.json());

// Chat
const response = await fetch(
  `${BASE_URL}/transcript/dQw4w9WgXcQ/chat`,
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message: "What are the main topics?"
    })
  }
).then(r => r.json());
```

### cURL

```bash
# Get all available transcripts
curl "https://fastapi-youtube-transcript.up.railway.app/transcript/VIDEO_ID/list"

# Get transcript in SRT format
curl "https://fastapi-youtube-transcript.up.railway.app/transcript/VIDEO_ID?format=srt" > subtitles.srt

# Search and summarize workflow
VIDEO_ID=$(curl "https://fastapi-youtube-transcript.up.railway.app/search?q=python+tutorial&max_results=1" | jq -r '.results[0].video_id')
curl -X POST "https://fastapi-youtube-transcript.up.railway.app/transcript/$VIDEO_ID/summarize" \
  -H "Content-Type: application/json" \
  -d '{}'
```

---

## OpenAPI Documentation

Interactive API documentation is available at:

- **Swagger UI**: https://fastapi-youtube-transcript.up.railway.app/docs
- **ReDoc**: https://fastapi-youtube-transcript.up.railway.app/redoc

---

## Support & Feedback

For issues, questions, or feature requests, please contact the API maintainer or open an issue in the project repository.

## Version

**Current Version**: 1.0.0
**Last Updated**: 2025-01-18
