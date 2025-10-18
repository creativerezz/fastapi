# YouTube Video Chat API

## Overview

The Chat API allows you to have conversational interactions with AI about any YouTube video, using the full transcript as context.

## Endpoint

```http
POST /transcript/{video_id}/chat
```

## Parameters

- `video_id` (path, required): YouTube video ID
- `languages` (query, optional): Comma-separated language codes (default: "en")
- `model` (query, optional): OpenRouter model ID (default: from MODEL_ID env var)

## Request Body

```json
{
  "message": "Your question about the video",
  "conversation_history": [  // Optional previous messages
    {"role": "user", "content": "Previous question"},
    {"role": "assistant", "content": "Previous answer"}
  ]
}
```

## Response

```json
{
  "video_id": "dQw4w9WgXcQ",
  "language": "English",
  "model": "qwen/qwen3-coder:free",
  "user_message": "What are the main tools mentioned?",
  "assistant_response": "Based on the transcript, the main tools mentioned are...",
  "fallback_used": false,
  "usage": {
    "prompt_tokens": 2847,
    "completion_tokens": 312,
    "total_tokens": 3159
  }
}
```

## Example Usage

### Simple Question

```bash
curl -X POST "https://api.automatehub.dev/transcript/dQw4w9WgXcQ/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are the main topics discussed in this video?"
  }'
```

### Follow-up Questions with Context

```bash
curl -X POST "https://api.automatehub.dev/transcript/VIDEO_ID/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Can you elaborate on that second point?",
    "conversation_history": [
      {"role": "user", "content": "What are the main points?"},
      {"role": "assistant", "content": "The main points are: 1) First point, 2) Second point, 3) Third point"}
    ]
  }'
```

### With Custom Model

```bash
curl -X POST "https://api.automatehub.dev/transcript/VIDEO_ID/chat?model=google/gemini-2.0-flash-exp:free" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Summarize the key takeaways"
  }'
```

## Common Use Cases

### 📝 Content Questions

```json
{
  "message": "What are the main arguments presented in this video?"
}
```

### 🔍 Specific Information

```json
{
  "message": "What tools or resources were mentioned?"
}
```

### 📊 Analysis Requests

```json
{
  "message": "What are the strengths and weaknesses of the approach discussed?"
}
```

### 📚 Learning Questions

```json
{
  "message": "Can you explain the concept mentioned at 5:30 in more detail?"
}
```

### 🎯 Fact Checking

```json
{
  "message": "What evidence was provided for the claims made?"
}
```

## Best Practices

### 1. **Be Specific**

Instead of "What's this about?" ask "What are the main technical concepts explained in this video?"

### 2. **Reference Timestamps**

"What was discussed around the 10-minute mark?" or "Can you explain the point made at 5:30?"

### 3. **Use Context**

Build on previous questions using `conversation_history` for more coherent discussions.

### 4. **Choose Appropriate Models**

- **Short videos (< 10 min)**: Any model works
- **Medium videos (10-30 min)**: DeepSeek V3.1, Qwen3 Coder
- **Long videos (30+ min)**: Gemini 2.0 Flash (1M context)

## Conversation Flow Example

### Initial Question

```json
{
  "message": "What programming languages are discussed in this tutorial?"
}
```

**Response**: "The video covers Python, JavaScript, and Go..."

### Follow-up Question

```json
{
  "message": "Which one does the presenter recommend for beginners?",
  "conversation_history": [
    {"role": "user", "content": "What programming languages are discussed in this tutorial?"},
    {"role": "assistant", "content": "The video covers Python, JavaScript, and Go..."}
  ]
}
```

**Response**: "Based on the earlier discussion, the presenter recommends Python for beginners because..."

### Deep Dive

```json
{
  "message": "What specific Python features were highlighted?",
  "conversation_history": [
    {"role": "user", "content": "What programming languages are discussed in this tutorial?"},
    {"role": "assistant", "content": "The video covers Python, JavaScript, and Go..."},
    {"role": "user", "content": "Which one does the presenter recommend for beginners?"},
    {"role": "assistant", "content": "Based on the earlier discussion, the presenter recommends Python for beginners because..."}
  ]
}
```

## Integration Examples

### iOS Shortcuts

1. Get video URL from share sheet
2. Extract video ID
3. Send POST request with predefined questions
4. Display formatted response

### Chrome Extension

```javascript
const response = await fetch(`/transcript/${videoId}/chat`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: userQuestion,
    conversation_history: chatHistory
  })
});
```

### Python Client

```python
import requests

def chat_with_video(video_id, message, history=[]):
    response = requests.post(
        f"https://api.automatehub.dev/transcript/{video_id}/chat",
        json={
            "message": message,
            "conversation_history": history
        }
    )
    return response.json()

# Usage
result = chat_with_video("dQw4w9WgXcQ", "What are the main points?")
print(result["assistant_response"])
```

## Error Handling

### Common Errors

- **400**: Missing message field
- **404**: Video not found or transcripts disabled
- **500**: API configuration issues
- **503**: All AI models temporarily unavailable
- **504**: Request timeout

### Robust Error Handling

```javascript
try {
  const response = await fetch(url, options);
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }
  const data = await response.json();
  return data.assistant_response;
} catch (error) {
  console.error('Chat API error:', error);
  return "Sorry, I couldn't process your question right now.";
}
```

## Rate Limits & Performance

- **Timeout**: 60 seconds per request
- **Context Limit**: Varies by model (8K - 1M tokens)
- **Conversation History**: Keep to last 5-10 exchanges for performance
- **Fallback Models**: Automatic fallback if primary model is rate-limited

## Tips for Better Results

### 1. **Clear Questions**

❌ "What about that thing?"  
✅ "What was the solution proposed for the scalability issue?"

### 2. **Context Awareness**

❌ "More details please"  
✅ "Can you provide more details about the authentication method mentioned at 8:45?"

### 3. **Conversation Management**

Keep conversation history focused - remove older exchanges if context becomes too long.

### 4. **Model Selection**

- **Quick answers**: Mistral 7B, Gemma models
- **Detailed analysis**: DeepSeek V3.1, Qwen3 Coder
- **Long videos**: Gemini 2.0 Flash

## Security & Privacy

- No conversation data is stored
- Each request is independent (unless you provide history)
- Video transcripts are fetched fresh for each session
- API keys are required for AI model access

## Coming Soon

- **Conversation persistence**: Save and resume chat sessions
- **Multi-video chat**: Ask questions across multiple videos
- **Suggested questions**: AI-generated follow-up questions
- **Export conversations**: Save chat history as markdown
- **Voice interface**: Speech-to-text and text-to-speech support