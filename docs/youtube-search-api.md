# YouTube Search API

## Overview
The YouTube Search endpoint allows you to search for videos on YouTube using the YouTube Data API v3. This provides real-time search results with video metadata.

## Endpoint

### GET `/search`

Search YouTube videos by query string.

#### Query Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `q` | string | Yes | - | Search query string |
| `max_results` | integer | No | 10 | Maximum number of results (1-50) |

#### Example Request

```bash
# Search for "swift programming"
curl "https://api.automatehub.dev/search?q=swift%20programming&max_results=10"
```

#### Response Format

```json
{
  "query": "swift programming",
  "resultCount": 10,
  "results": [
    {
      "videoId": "ABC123XYZ",
      "title": "Swift Programming Tutorial",
      "channelTitle": "Code Academy",
      "thumbnailUrl": "https://i.ytimg.com/vi/ABC123XYZ/mqdefault.jpg",
      "publishedAt": "2024-01-15T10:30:00Z",
      "description": "Learn Swift programming from scratch..."
    }
  ]
}
```

#### Response Fields

- `query` (string) - The search query that was used
- `resultCount` (integer) - Number of results returned
- `results` (array) - Array of video search results
  - `videoId` (string) - YouTube video ID
  - `title` (string) - Video title
  - `channelTitle` (string) - Channel name
  - `thumbnailUrl` (string) - Medium quality thumbnail URL (320x180)
  - `publishedAt` (string) - ISO 8601 publication timestamp
  - `description` (string) - Video description snippet

## Setup

### Environment Variables

The search endpoint requires a YouTube Data API v3 key:

```bash
YOUTUBE_API_KEY=your_api_key_here
```

### Getting a YouTube API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable **YouTube Data API v3**
4. Go to **Credentials** → **Create Credentials** → **API Key**
5. Copy the API key and add to environment variables

### Quota Limits

YouTube Data API v3 has daily quota limits:
- Default quota: 10,000 units per day
- Search request cost: 100 units per call
- That's approximately 100 searches per day on free tier

To increase quota limits, you can request a quota increase in Google Cloud Console.

## Error Responses

### 500 - API Key Not Configured
```json
{
  "detail": "YouTube API key not configured. Please set YOUTUBE_API_KEY environment variable."
}
```

**Solution**: Add `YOUTUBE_API_KEY` to your environment variables.

### 400/403 - YouTube API Error
```json
{
  "detail": "YouTube API error: {error_message}"
}
```

**Possible causes**:
- Invalid API key
- Quota exceeded
- API not enabled in Google Cloud Console

### 500 - Internal Server Error
```json
{
  "detail": "Error: {error_details}"
}
```

## Usage in iOS App

The iOS app uses `YouTubeAPIService.shared.searchVideos()`:

```swift
let results = try await YouTubeAPIService.shared.searchVideos(
  query: "swift programming",
  maxResults: 10
)

for result in results {
  print(result.title)
  print(result.videoId)
}
```

## Integration with Other Endpoints

Search results provide `videoId` which can be used with other endpoints:

1. **Get Summary**: `/transcript/{videoId}/summarize`
2. **Apply Pattern**: `/transcript/{videoId}/pattern/{pattern_name}`
3. **Chat**: `/transcript/{videoId}/chat`

## Example Workflow

```swift
// 1. Search for videos
let results = try await YouTubeAPIService.shared.searchVideos(
  query: "SwiftUI tutorials"
)

// 2. Select a video
let selectedVideo = results[0]

// 3. Get summary
let summary = try await YouTubeAPIService.shared.fetchSummary(
  videoId: selectedVideo.videoId
)

// 4. Display summary to user
print(summary)
```

## Rate Limiting

The endpoint doesn't implement its own rate limiting, but is subject to:
- YouTube Data API v3 quota (10,000 units/day)
- Railway/hosting platform limits

Consider implementing client-side debouncing for search-as-you-type features to reduce API calls.

## Best Practices

1. **Debounce Search Input**: Wait 300-500ms after user stops typing before searching
2. **Cache Results**: Store search results locally to avoid duplicate API calls
3. **Limit Results**: Start with 10 results per search to conserve quota
4. **Error Handling**: Gracefully handle quota exceeded errors
5. **Loading States**: Show clear loading indicators during search

## Troubleshooting

### "API key not configured" error
- Verify `YOUTUBE_API_KEY` is set in environment variables
- Check Railway/deployment platform environment variables

### No results returned
- Verify search query is not empty
- Check if videos exist for the query on YouTube
- Ensure API key has proper permissions

### Quota exceeded
- Check quota usage in [Google Cloud Console](https://console.cloud.google.com/apis/api/youtube.googleapis.com/quotas)
- Wait until quota resets (midnight Pacific Time)
- Request quota increase if needed
- Implement caching to reduce API calls
