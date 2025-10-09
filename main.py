import os
import requests
from datetime import timedelta
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import PlainTextResponse
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Get model name from environment variables
MODEL_NAME = os.getenv("model_id") or os.getenv("MODEL_ID") or "qwen/qwen3-coder:free"

# Initialize YouTube Transcript API with proxy support for Railway deployment
def get_youtube_api():
    """Create YouTubeTranscriptApi instance with optional proxy configuration"""
    # Support multiple environment variable naming conventions
    proxy_username = os.getenv("webshare_user") or os.getenv("WEBSHARE_PROXY_USERNAME")
    proxy_password = os.getenv("webshare_pass") or os.getenv("WEBSHARE_PROXY_PASSWORD")

    if proxy_username and proxy_password:
        # Use Webshare rotating residential proxy with numbered username
        # Webshare requires username-X format (e.g., opgdacdt-1)
        if not proxy_username.endswith(tuple(f'-{i}' for i in range(1, 1000))):
            proxy_username = f"{proxy_username}-1"

        proxy_config = WebshareProxyConfig(
            proxy_username=proxy_username,
            proxy_password=proxy_password,
        )
        return YouTubeTranscriptApi(proxy_config=proxy_config)

    # No proxy for local development
    return YouTubeTranscriptApi()

def format_timestamp(seconds: float) -> str:
    """Convert seconds to HH:MM:SS or MM:SS format"""
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"

def format_as_text(transcript_data: list) -> str:
    """Format transcript as plain text with timestamps"""
    lines = []
    for entry in transcript_data:
        timestamp = format_timestamp(entry['start'])
        lines.append(f"[{timestamp}] {entry['text']}")
    return "\n".join(lines)

def format_as_srt(transcript_data: list) -> str:
    """Format transcript as SRT subtitle format"""
    srt_lines = []
    for i, entry in enumerate(transcript_data, start=1):
        start_time = format_srt_timestamp(entry['start'])
        end_time = format_srt_timestamp(entry['start'] + entry['duration'])

        srt_lines.append(f"{i}")
        srt_lines.append(f"{start_time} --> {end_time}")
        srt_lines.append(entry['text'])
        srt_lines.append("")  # Empty line between entries

    return "\n".join(srt_lines)

def format_srt_timestamp(seconds: float) -> str:
    """Convert seconds to SRT timestamp format (HH:MM:SS,mmm)"""
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    millis = int((seconds - int(seconds)) * 1000)

    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def format_as_vtt(transcript_data: list) -> str:
    """Format transcript as WebVTT subtitle format"""
    vtt_lines = ["WEBVTT", ""]

    for entry in transcript_data:
        start_time = format_vtt_timestamp(entry['start'])
        end_time = format_vtt_timestamp(entry['start'] + entry['duration'])

        vtt_lines.append(f"{start_time} --> {end_time}")
        vtt_lines.append(entry['text'])
        vtt_lines.append("")  # Empty line between entries

    return "\n".join(vtt_lines)

def format_vtt_timestamp(seconds: float) -> str:
    """Convert seconds to WebVTT timestamp format (HH:MM:SS.mmm)"""
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    millis = int((seconds - int(seconds)) * 1000)

    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"

@app.get("/")
async def root():
    return {"greeting": "Hello, World!", "message": "Welcome to FastAPI!"}

@app.get("/transcript/{video_id}")
async def get_transcript(
    video_id: str,
    languages: str = "en",
    format: str = Query(
        default="json",
        description="Output format: json, text, srt, or vtt"
    )
):
    """
    Fetch YouTube transcript for a given video ID

    Args:
        video_id: YouTube video ID (not full URL)
        languages: Comma-separated language codes (e.g., "en,de,es")
        format: Output format - json (default), text, srt, or vtt

    Examples:
        /transcript/dQw4w9WgXcQ?languages=en&format=json
        /transcript/dQw4w9WgXcQ?format=text
        /transcript/dQw4w9WgXcQ?format=srt
        /transcript/dQw4w9WgXcQ?format=vtt
    """
    try:
        ytt_api = get_youtube_api()
        language_list = [lang.strip() for lang in languages.split(",")]

        # Fetch the transcript
        fetched_transcript = ytt_api.fetch(video_id, languages=language_list)
        transcript_data = fetched_transcript.to_raw_data()

        # Return based on format
        format_lower = format.lower()

        if format_lower == "text":
            return PlainTextResponse(
                content=format_as_text(transcript_data),
                media_type="text/plain"
            )
        elif format_lower == "srt":
            return PlainTextResponse(
                content=format_as_srt(transcript_data),
                media_type="text/plain"
            )
        elif format_lower == "vtt":
            return PlainTextResponse(
                content=format_as_vtt(transcript_data),
                media_type="text/plain"
            )
        elif format_lower == "json":
            return {
                "video_id": fetched_transcript.video_id,
                "language": fetched_transcript.language,
                "language_code": fetched_transcript.language_code,
                "is_generated": fetched_transcript.is_generated,
                "transcript": transcript_data
            }
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid format '{format}'. Must be one of: json, text, srt, vtt"
            )

    except HTTPException:
        raise  # Re-raise HTTPException without modification
    except TranscriptsDisabled:
        raise HTTPException(status_code=404, detail="Transcripts are disabled for this video")
    except NoTranscriptFound:
        raise HTTPException(
            status_code=404,
            detail=f"No transcript found for languages: {languages}"
        )
    except VideoUnavailable:
        raise HTTPException(status_code=404, detail="Video not found or unavailable")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching transcript: {str(e)}")

@app.get("/transcript/{video_id}/list")
async def list_transcripts(video_id: str):
    """
    List all available transcripts for a video

    Args:
        video_id: YouTube video ID

    Example: /transcript/dQw4w9WgXcQ/list
    """
    try:
        ytt_api = get_youtube_api()
        transcript_list = ytt_api.list(video_id)

        transcripts = []
        for transcript in transcript_list:
            transcripts.append({
                "language": transcript.language,
                "language_code": transcript.language_code,
                "is_generated": transcript.is_generated,
                "is_translatable": transcript.is_translatable,
            })

        return {
            "video_id": video_id,
            "available_transcripts": transcripts
        }

    except VideoUnavailable:
        raise HTTPException(status_code=404, detail="Video not found or unavailable")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing transcripts: {str(e)}")

@app.get("/transcript/{video_id}/summarize")
async def summarize_transcript(
    video_id: str,
    languages: str = "en",
    model: str = Query(
        default=MODEL_NAME,
        description="OpenRouter model ID (use :free models from openrouter-free-llms.txt)"
    )
):
    """
    Fetch YouTube transcript and summarize it using OpenRouter's free LLMs

    Args:
        video_id: YouTube video ID (not full URL)
        languages: Comma-separated language codes (default: "en")
        model: OpenRouter model identifier (default: google/gemini-2.0-flash-exp:free)

    Available free models:
        - google/gemini-2.0-flash-exp:free (1M context) - DEFAULT
        - deepseek/deepseek-chat-v3.1:free (163k context)
        - qwen/qwen3-coder:free (262k context)
        - meta-llama/llama-3.3-70b-instruct:free (65k context)

    Example: /transcript/dQw4w9WgXcQ/summarize
    """
    try:
        # Get OpenRouter API key
        openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        if not openrouter_api_key:
            raise HTTPException(
                status_code=500,
                detail="OPENROUTER_API_KEY environment variable not set"
            )

        # Fetch the transcript
        ytt_api = get_youtube_api()
        language_list = [lang.strip() for lang in languages.split(",")]
        fetched_transcript = ytt_api.fetch(video_id, languages=language_list)

        # Convert transcript to plain text
        transcript_text = "\n".join([
            f"[{entry['start']:.2f}s] {entry['text']}"
            for entry in fetched_transcript.to_raw_data()
        ])

        # Prepare OpenRouter API request
        headers = {
            "Authorization": f"Bearer {openrouter_api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/yourusername/fastapi-youtube-transcript",
            "X-Title": "FastAPI YouTube Transcript Summarizer"
        }

        payload = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a video transcript summarizer. Create Markdown summaries with: "
                        "1) Brief overview, 2) Clear headings, 3) Timestamps [MM:SS] before key points, "
                        "4) Bullet points, 5) Bold takeaways, 6) Conclusion. "
                        "Output only the summary, no explanations."
                    )
                },
                {
                    "role": "user",
                    "content": f"Summarize this transcript:\n\n{transcript_text}"
                }
            ]
        }

        # Call OpenRouter API
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"OpenRouter API error: {response.text}"
            )

        result = response.json()
        summary = result["choices"][0]["message"]["content"]

        return {
            "video_id": video_id,
            "language": fetched_transcript.language,
            "model_used": model,
            "summary": summary,
            "transcript_length": len(fetched_transcript.to_raw_data()),
            "usage": result.get("usage", {})
        }

    except TranscriptsDisabled:
        raise HTTPException(status_code=404, detail="Transcripts are disabled for this video")
    except NoTranscriptFound:
        raise HTTPException(
            status_code=404,
            detail=f"No transcript found for languages: {languages}"
        )
    except VideoUnavailable:
        raise HTTPException(status_code=404, detail="Video not found or unavailable")
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="OpenRouter API request timed out")
    except Exception as e:
        import traceback
        error_details = f"{type(e).__name__}: {str(e)}" if str(e) else f"{type(e).__name__}: {repr(e)}"
        print(f"Summarization error: {error_details}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=error_details)