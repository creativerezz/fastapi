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
# Default to Google Gemini 2.0 Flash (1M context window, most reliable availability)
MODEL_NAME = os.getenv("model_id") or os.getenv("MODEL_ID") or "google/gemini-2.0-flash-exp:free"

# Fallback model chain - will try these in order if one is rate-limited
FALLBACK_MODELS = [
    "google/gemini-2.0-flash-exp:free",  # 1M context, Google reliability
    "deepseek/deepseek-chat-v3.1:free",  # 163k context, very capable
    "meta-llama/llama-3.3-70b-instruct:free",  # 65k context, Meta reliability
    "mistralai/mistral-nemo:free",  # 131k context, Mistral reliability
    "nvidia/nemotron-nano-9b-v2:free",  # 128k context, NVIDIA reliability
]

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

def call_openrouter_with_fallback(
    openrouter_api_key: str,
    transcript_text: str,
    preferred_model: str,
    system_prompt: str
) -> dict:
    """
    Call OpenRouter API with automatic fallback to alternative models if rate-limited.
    
    Tries preferred_model first, then falls back to FALLBACK_MODELS chain if rate-limited.
    Returns: dict with 'summary' and 'model_used' keys
    """
    # Build list of models to try: preferred first, then fallbacks
    models_to_try = [preferred_model] if preferred_model not in FALLBACK_MODELS else []
    models_to_try.extend(FALLBACK_MODELS)
    
    headers = {
        "Authorization": f"Bearer {openrouter_api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/creativerezz/fastapi",
        "X-Title": "Automatehub YouTube Summarizer"
    }
    
    last_error = None
    
    for model in models_to_try:
        try:
            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": f"Summarize this transcript:\n\n{transcript_text}"
                    }
                ]
            }
            
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )
            
            # If successful, return immediately
            if response.status_code == 200:
                result = response.json()
                return {
                    "summary": result["choices"][0]["message"]["content"],
                    "model_used": model,
                    "usage": result.get("usage", {}),
                    "fallback_used": model != preferred_model
                }
            
            # If rate-limited (429), try next model
            if response.status_code == 429:
                print(f"Model {model} is rate-limited, trying next fallback...")
                last_error = f"Rate limited: {model}"
                continue
            
            # For other errors, raise immediately
            raise HTTPException(
                status_code=response.status_code,
                detail=f"OpenRouter API error with {model}: {response.text}"
            )
            
        except requests.exceptions.Timeout:
            print(f"Model {model} timed out, trying next fallback...")
            last_error = f"Timeout: {model}"
            continue
        except HTTPException:
            raise
        except Exception as e:
            print(f"Error with model {model}: {str(e)}, trying next fallback...")
            last_error = f"Error with {model}: {str(e)}"
            continue
    
    # If all models failed, raise error with details
    raise HTTPException(
        status_code=503,
        detail=f"All models are currently unavailable. Last error: {last_error}. Please try again in a few minutes."
    )

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

        # System prompt for summarization
        system_prompt = (
            "You are a video transcript summarizer. Create Markdown summaries with: "
            "1) Brief overview, 2) Clear headings, 3) Timestamps [MM:SS] before key points, "
            "4) Bullet points, 5) Bold takeaways, 6) Conclusion. "
            "Output only the summary, no explanations."
        )

        # Call OpenRouter with automatic fallback
        result = call_openrouter_with_fallback(
            openrouter_api_key=openrouter_api_key,
            transcript_text=transcript_text,
            preferred_model=model,
            system_prompt=system_prompt
        )

        return {
            "video_id": video_id,
            "language": fetched_transcript.language,
            "model": result["model_used"],
            "summary": result["summary"],
            "transcript_length": len(fetched_transcript.to_raw_data()),
            "usage": result.get("usage", {}),
            "fallback_used": result.get("fallback_used", False)
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

@app.get("/patterns")
async def list_patterns():
    """
    List all available Fabric AI patterns

    Returns:
        List of available pattern names that can be used with /transcript/{video_id}/pattern/{pattern_name}
    """
    import os
    patterns_dir = os.path.join(os.path.dirname(__file__), "patterns")
    
    try:
        patterns = []
        for item in sorted(os.listdir(patterns_dir)):
            item_path = os.path.join(patterns_dir, item)
            if os.path.isdir(item_path) and not item.startswith('.'):
                # Check if it has a system.md file
                system_file = os.path.join(item_path, "system.md")
                if os.path.exists(system_file):
                    patterns.append(item)
        
        return {
            "total_patterns": len(patterns),
            "patterns": patterns
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing patterns: {str(e)}")

@app.get("/transcript/{video_id}/pattern/{pattern_name}")
async def apply_pattern(
    video_id: str,
    pattern_name: str,
    languages: str = "en",
    model: str = Query(
        default=MODEL_NAME,
        description="OpenRouter model ID (use :free models from openrouter-free-llms.txt)"
    )
):
    """
    Apply any Fabric AI pattern to a YouTube transcript

    Args:
        video_id: YouTube video ID (not full URL)
        pattern_name: Name of the Fabric pattern to apply (e.g., 'extract_wisdom', 'create_summary', 'analyze_paper')
        languages: Comma-separated language codes (default: "en")
        model: OpenRouter model identifier

    Examples:
        /transcript/dQw4w9WgXcQ/pattern/extract_wisdom
        /transcript/VIDEO_ID/pattern/create_summary
        /transcript/VIDEO_ID/pattern/analyze_paper
        /transcript/VIDEO_ID/pattern/create_quiz

    Use GET /patterns to see all available patterns
    """
    import os
    
    try:
        # Get OpenRouter API key
        openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        if not openrouter_api_key:
            raise HTTPException(
                status_code=500,
                detail="OPENROUTER_API_KEY environment variable not set"
            )

        # Load the pattern's system prompt
        patterns_dir = os.path.join(os.path.dirname(__file__), "patterns")
        pattern_dir = os.path.join(patterns_dir, pattern_name)
        system_file = os.path.join(pattern_dir, "system.md")
        
        if not os.path.exists(system_file):
            raise HTTPException(
                status_code=404,
                detail=f"Pattern '{pattern_name}' not found. Use GET /patterns to see available patterns."
            )
        
        # Read the system prompt
        with open(system_file, 'r', encoding='utf-8') as f:
            system_prompt = f.read()

        # Fetch the transcript
        ytt_api = get_youtube_api()
        language_list = [lang.strip() for lang in languages.split(",")]
        fetched_transcript = ytt_api.fetch(video_id, languages=language_list)

        # Convert transcript to plain text
        transcript_text = "\n".join([
            f"[{entry['start']:.2f}s] {entry['text']}"
            for entry in fetched_transcript.to_raw_data()
        ])

        # Call OpenRouter with automatic fallback
        result = call_openrouter_with_fallback(
            openrouter_api_key=openrouter_api_key,
            transcript_text=transcript_text,
            preferred_model=model,
            system_prompt=system_prompt
        )

        return {
            "video_id": video_id,
            "language": fetched_transcript.language,
            "pattern": pattern_name,
            "model": result["model_used"],
            "result": result["summary"],  # Still called 'summary' in fallback function
            "transcript_length": len(fetched_transcript.to_raw_data()),
            "usage": result.get("usage", {}),
            "fallback_used": result.get("fallback_used", False)
        }

    except HTTPException:
        raise
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
        print(f"Pattern application error: {error_details}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=error_details)

@app.get("/transcript/{video_id}/extract-wisdom")
async def extract_wisdom(
    video_id: str,
    languages: str = "en",
    model: str = Query(
        default=MODEL_NAME,
        description="OpenRouter model ID (use :free models from openrouter-free-llms.txt)"
    )
):
    """
    Extract deep insights, ideas, quotes, and wisdom from YouTube video transcript
    using Daniel Miessler's extract_wisdom pattern from Fabric AI framework

    Args:
        video_id: YouTube video ID (not full URL)
        languages: Comma-separated language codes (default: "en")
        model: OpenRouter model identifier (default from env)

    Returns structured wisdom extraction with:
        - SUMMARY (25 words)
        - IDEAS (20-50 items, 16 words each)
        - INSIGHTS (10-20 items, 16 words each)
        - QUOTES (15-30 exact quotes)
        - HABITS (15-30 personal habits)
        - FACTS (15-30 facts)
        - REFERENCES (books, tools, projects)
        - ONE-SENTENCE TAKEAWAY
        - RECOMMENDATIONS (15-30 items)

    Example: /transcript/dQw4w9WgXcQ/extract-wisdom
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

        # Prepare OpenRouter API request with extract_wisdom system prompt
        headers = {
            "Authorization": f"Bearer {openrouter_api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/creativerezz/fastapi",
            "X-Title": "FastAPI YouTube Transcript Wisdom Extractor"
        }

        payload = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You extract surprising, insightful, and interesting information from text content. "
                        "You are interested in insights related to the purpose and meaning of life, human flourishing, "
                        "the role of technology in the future of humanity, artificial intelligence, learning, and continuous improvement.\n\n"
                        "Extract from the content:\n"
                        "- SUMMARY (25 words with who is presenting and content discussed)\n"
                        "- IDEAS (20-50 items, exactly 16 words each)\n"
                        "- INSIGHTS (10-20 items, exactly 16 words each - refined versions of best ideas)\n"
                        "- QUOTES (15-30 exact quotes from input)\n"
                        "- HABITS (15-30 personal habits mentioned, exactly 16 words each)\n"
                        "- FACTS (15-30 facts about the world, exactly 16 words each)\n"
                        "- REFERENCES (all books, tools, projects mentioned)\n"
                        "- ONE-SENTENCE TAKEAWAY (exactly 15 words capturing essence)\n"
                        "- RECOMMENDATIONS (15-30 items, exactly 16 words each)\n\n"
                        "Output only Markdown. Use bulleted lists. No warnings or notes. "
                        "Do not repeat items. Do not start items with same words."
                    )
                },
                {
                    "role": "user",
                    "content": f"Extract wisdom from this content:\n\n{transcript_text}"
                }
            ]
        }

        # Call OpenRouter API
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=90  # Longer timeout for wisdom extraction
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"OpenRouter API error: {response.text}"
            )

        result = response.json()
        wisdom = result["choices"][0]["message"]["content"]

        return {
            "video_id": video_id,
            "language": fetched_transcript.language,
            "model_used": model,
            "wisdom": wisdom,
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
        print(f"Wisdom extraction error: {error_details}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=error_details)