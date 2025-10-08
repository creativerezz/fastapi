import os
import requests
from fastapi import FastAPI, HTTPException, Query
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable

app = FastAPI()

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

@app.get("/")
async def root():
    return {"greeting": "Hello, World!", "message": "Welcome to FastAPI!"}

@app.get("/transcript/{video_id}")
async def get_transcript(video_id: str, languages: str = "en"):
    """
    Fetch YouTube transcript for a given video ID

    Args:
        video_id: YouTube video ID (not full URL)
        languages: Comma-separated language codes (e.g., "en,de,es")

    Example: /transcript/dQw4w9WgXcQ?languages=en,de
    """
    try:
        ytt_api = get_youtube_api()
        language_list = [lang.strip() for lang in languages.split(",")]

        # Fetch the transcript
        fetched_transcript = ytt_api.fetch(video_id, languages=language_list)

        return {
            "video_id": fetched_transcript.video_id,
            "language": fetched_transcript.language,
            "language_code": fetched_transcript.language_code,
            "is_generated": fetched_transcript.is_generated,
            "transcript": fetched_transcript.to_raw_data()
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
        default="deepseek/deepseek-chat-v3.1:free",
        description="OpenRouter model ID (use :free models from openrouter-free-llms.txt)"
    )
):
    """
    Fetch YouTube transcript and summarize it using OpenRouter's free LLMs

    Args:
        video_id: YouTube video ID (not full URL)
        languages: Comma-separated language codes (default: "en")
        model: OpenRouter model identifier (default: deepseek/deepseek-chat-v3.1:free)

    Available free models:
        - google/gemini-2.0-flash-exp:free (1M context)
        - deepseek/deepseek-chat-v3.1:free (163k context)
        - qwen/qwen3-coder:free (262k context)
        - meta-llama/llama-3.3-70b-instruct:free (65k context)

    Example: /transcript/dQw4w9WgXcQ/summarize?model=google/gemini-2.0-flash-exp:free
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
                        "You are a helpful AI assistant that creates concise, well-structured summaries "
                        "of YouTube video transcripts. Provide a clear summary with:\n"
                        "1. Main Topic: A brief overview of what the video is about\n"
                        "2. Key Points: 3-5 bullet points highlighting the most important information\n"
                        "3. Conclusion: A brief final takeaway\n\n"
                        "Keep the summary informative but concise."
                    )
                },
                {
                    "role": "user",
                    "content": f"Please summarize this YouTube video transcript:\n\n{transcript_text}"
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
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")