# Extract Wisdom Endpoint

## Overview

The `/transcript/{video_id}/extract-wisdom` endpoint uses Daniel Miessler's "extract_wisdom" pattern from the Fabric AI framework to perform deep analysis of YouTube video transcripts.

## Endpoint

```
GET /transcript/{video_id}/extract-wisdom
```

## Parameters

- `video_id` (path, required): YouTube video ID
- `languages` (query, optional): Comma-separated language codes (default: "en")
- `model` (query, optional): OpenRouter model ID (default: from MODEL_ID env var)

## Response Structure

The endpoint returns structured wisdom extraction with:

### SUMMARY (25 words)
Brief overview including who is presenting and the content being discussed

### IDEAS (20-50 items, 16 words each)
Most surprising, insightful, and interesting ideas from the content

### INSIGHTS (10-20 items, 16 words each)
Refined, more insightful, abstracted versions of the best ideas

### QUOTES (15-30 items)
Exact quotes from the input with speaker attribution

### HABITS (15-30 items, 16 words each)
Practical personal habits mentioned: sleep, reading, productivity tips, diet, exercise, etc.

### FACTS (15-30 items, 16 words each)
Surprising, insightful facts about the greater world mentioned in content

### REFERENCES
All mentions of writing, art, tools, projects, and sources of inspiration

### ONE-SENTENCE TAKEAWAY (15 words)
Most potent takeaway capturing the essence of the content

### RECOMMENDATIONS (15-30 items, 16 words each)
Most surprising and actionable recommendations from the content

## Example Usage

### Basic Request
```bash
curl "http://localhost:8001/transcript/dQw4w9WgXcQ/extract-wisdom"
```

### With Custom Model
```bash
curl "http://localhost:8001/transcript/F5JadFdhy9E/extract-wisdom?model=google/gemini-2.0-flash-exp:free"
```

### Production URL
```bash
curl "https://api.automatehub.dev/transcript/VIDEO_ID/extract-wisdom"
```

## Response Example

```json
{
  "video_id": "dQw4w9WgXcQ",
  "language": "English (auto-generated)",
  "model_used": "qwen/qwen3-coder:free",
  "wisdom": "# SUMMARY\n\nRick Astley presents a heartfelt declaration...\n\n# IDEAS\n\n- True love requires absolute dedication...",
  "transcript_length": 89,
  "usage": {
    "prompt_tokens": 2500,
    "completion_tokens": 428,
    "total_tokens": 2928
  }
}
```

## Comparison: Summarize vs Extract Wisdom

| Feature | `/summarize` | `/extract-wisdom` |
|---------|-------------|-------------------|
| **Output Format** | Markdown summary with timestamps | Structured sections (IDEAS, INSIGHTS, QUOTES, etc.) |
| **Best For** | Quick overviews, educational content | Deep analysis, interviews, podcasts |
| **Length** | Concise | Comprehensive |
| **Structure** | Headings + bullets | 9 distinct sections |
| **Processing Time** | ~30-45 seconds | ~60-90 seconds |
| **Token Usage** | Lower | Higher |
| **Quotes** | None | Exact quotes extracted |
| **Habits** | Not extracted | Extracted systematically |
| **Recommendations** | General conclusion | 15-30 specific items |

## Use Cases

### Extract Wisdom Is Ideal For:
- 🎙️ Podcast transcripts
- 🎤 Interview content
- 📚 Educational lectures
- 💡 Thought leadership content
- 🧠 Personal development videos
- 📖 Book summaries
- 🔬 Research presentations

### Summarize Is Ideal For:
- 📺 General videos
- 🎬 Quick overviews
- ⏱️ Time-sensitive content
- 📰 News/current events
- 🎓 Tutorial videos

## Credits

The extract_wisdom pattern is from [Fabric AI](https://github.com/danielmiessler/fabric) by Daniel Miessler, licensed under MIT.

## Notes

- Longer timeout (90s vs 60s) to accommodate comprehensive extraction
- Requires more tokens due to structured output format
- Works best with conversational content (interviews, discussions, lectures)
- May extract fewer items if content doesn't contain enough material for each section
