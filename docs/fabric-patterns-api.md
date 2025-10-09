# Fabric AI Patterns API

## Overview

This API now supports **ALL 226 Fabric AI patterns** created by Daniel Miessler. You can apply any pattern to YouTube video transcripts dynamically.

## Endpoints

### 1. List All Available Patterns

```http
GET /patterns
```

**Response:**

```json
{
  "total_patterns": 226,
  "patterns": [
    "agility_story",
    "analyze_paper",
    "create_summary",
    "extract_wisdom",
    ...
  ]
}
```

### 2. Apply Any Pattern to a Transcript

```http
GET /transcript/{video_id}/pattern/{pattern_name}
```

**Parameters:**

- `video_id` (path, required): YouTube video ID
- `pattern_name` (path, required): Name of the Fabric pattern to apply
- `languages` (query, optional): Comma-separated language codes (default: "en")
- `model` (query, optional): OpenRouter model ID (default: from MODEL_ID env var)

**Response:**

```json
{
  "video_id": "dQw4w9WgXcQ",
  "language": "English",
  "pattern_used": "create_summary",
  "model_used": "qwen/qwen3-coder:free",
  "output": "ONE SENTENCE SUMMARY:\n...",
  "transcript_length": 61,
  "usage": {
    "prompt_tokens": 1479,
    "completion_tokens": 245,
    "total_tokens": 1724
  }
}
```

## Example Usage

### Get List of Patterns

```bash
curl "https://api.automatehub.dev/patterns"
```

### Apply create_summary Pattern

```bash
curl "https://api.automatehub.dev/transcript/dQw4w9WgXcQ/pattern/create_summary"
```

### Apply extract_wisdom Pattern

```bash
curl "https://api.automatehub.dev/transcript/VIDEO_ID/pattern/extract_wisdom"
```

### Apply analyze_paper Pattern

```bash
curl "https://api.automatehub.dev/transcript/VIDEO_ID/pattern/analyze_paper"
```

### With Custom Model

```bash
curl "https://api.automatehub.dev/transcript/VIDEO_ID/pattern/create_quiz?model=google/gemini-2.0-flash-exp:free"
```

## Popular Patterns

### Content Analysis

- `analyze_paper` - Analyze research papers for findings and quality
- `analyze_presentation` - Analyze presentation structure and effectiveness
- `analyze_debate` - Analyze debate arguments and positions
- `analyze_claims` - Analyze and fact-check claims
- `analyze_prose` - Analyze writing style and quality

### Content Creation

- `create_summary` - Create concise summaries (ONE SENTENCE + MAIN POINTS + TAKEAWAYS)
- `create_quiz` - Generate quiz questions from content
- `create_keynote` - Create keynote presentation outline
- `create_newsletter_entry` - Format content for newsletter
- `create_micro_summary` - Ultra-concise summary

### Extraction

- `extract_wisdom` - Extract ideas, insights, quotes, habits, facts, references
- `extract_ideas` - Extract main ideas
- `extract_insights` - Extract key insights
- `extract_recommendations` - Extract actionable recommendations
- `extract_references` - Extract books, tools, resources mentioned

### Educational

- `create_quiz` - Generate quiz questions
- `create_reading_plan` - Create structured reading plan
- `create_flash_cards` - Generate flashcards for learning
- `explain_code` - Explain code functionality
- `explain_project` - Explain project structure

### Writing Assistance

- `improve_writing` - Improve writing quality
- `write_essay` - Generate essay structure
- `write_micro_essay` - Write short essay
- `create_academic_paper` - Create academic paper structure

### Technical

- `analyze_logs` - Analyze system logs
- `analyze_malware` - Analyze malware behavior
- `analyze_threat_report` - Analyze security threats
- `create_sigma_rules` - Create SIGMA detection rules
- `create_stride_threat_model` - Create STRIDE threat model

### Business

- `analyze_sales_call` - Analyze sales call effectiveness
- `create_hormozi_offer` - Create compelling offers (Alex Hormozi style)
- `create_prd` - Create Product Requirements Document
- `create_report_finding` - Create report findings
- `analyze_product_feedback` - Analyze product feedback

## Pattern Categories

### 📊 Analysis (40+ patterns)

Patterns starting with `analyze_*` - for analyzing content, code, security, etc.

### 🎨 Creation (60+ patterns)

Patterns starting with `create_*` - for generating new content in various formats

### 🔍 Extraction (20+ patterns)

Patterns starting with `extract_*` - for extracting specific information

### 📝 Improvement (15+ patterns)

Patterns starting with `improve_*` or `enhance_*` - for improving existing content

### 💡 Explanation (10+ patterns)

Patterns starting with `explain_*` - for explaining concepts

### ✨ Special Purpose (80+ patterns)

Unique patterns for specific use cases

## Use Cases by Content Type

### 🎙️ Podcasts & Interviews

- `extract_wisdom` - Deep insights and quotes
- `create_summary` - Quick overview
- `extract_ideas` - Main ideas discussed
- `create_newsletter_entry` - Format for sharing

### 📚 Educational Videos

- `create_quiz` - Test comprehension
- `create_flash_cards` - Study aids
- `create_reading_plan` - Follow-up learning
- `explain_concepts` - Clarify complex topics

### 🎬 Presentations & Talks

- `analyze_presentation` - Evaluate structure
- `create_keynote` - Convert to outline
- `extract_recommendations` - Actionable takeaways
- `create_micro_summary` - Social media snippet

### 💼 Business Content

- `analyze_sales_call` - Sales technique analysis
- `create_prd` - Product documentation
- `analyze_product_feedback` - Customer insights
- `create_report_finding` - Report format

### 🔬 Research & Academic

- `analyze_paper` - Research analysis
- `create_academic_paper` - Paper structure
- `extract_insights` - Key findings
- `summarize_lecture` - Lecture notes

### 🛡️ Security & Tech

- `analyze_threat_report` - Security analysis
- `analyze_logs` - Log analysis
- `create_sigma_rules` - Detection rules
- `analyze_malware` - Malware analysis

## Tips for Best Results

### 1. Choose the Right Pattern

Match the pattern to your content type:

- Educational → `create_quiz`, `create_flash_cards`
- Interview/Podcast → `extract_wisdom`, `extract_ideas`
- Technical → `analyze_logs`, `explain_code`

### 2. Use Appropriate Models

- Short content (< 5 min) → Any model works
- Medium content (5-30 min) → DeepSeek V3.1, Qwen3 Coder
- Long content (30+ min) → Gemini 2.0 Flash (1M context)

### 3. Language Support

Specify transcript language if not English:

```bash
curl "...?languages=es,en"  # Try Spanish first, then English
```

### 4. Combine Patterns

Run multiple patterns on same content:

```bash
# Get quick summary
curl ".../pattern/create_summary"

# Then get deep analysis
curl ".../pattern/extract_wisdom"

# Create quiz for learning
curl ".../pattern/create_quiz"
```

## iOS Shortcuts Integration

### Quick Summary

```
GET https://api.automatehub.dev/transcript/[VideoID]/pattern/create_summary
```

### Deep Analysis

```
GET https://api.automatehub.dev/transcript/[VideoID]/pattern/extract_wisdom
```

### Generate Quiz

```
GET https://api.automatehub.dev/transcript/[VideoID]/pattern/create_quiz
```

## Rate Limits & Performance

- **Timeout**: 90 seconds per request
- **Token Usage**: Varies by pattern (1K-50K tokens)
- **Best Practices**:
  - Cache results for same video + pattern combo
  - Use appropriate models for content length
  - Start with lightweight patterns (`create_summary`) before heavy ones (`extract_wisdom`)

## Credits

All patterns are from [Fabric AI](https://github.com/danielmiessler/fabric) by Daniel Miessler, licensed under MIT.

This API provides a REST interface to Fabric patterns, making them accessible for:

- iOS Shortcuts
- Web applications
- Chrome extensions
- Third-party integrations
- Automation workflows

## Coming Soon

- Pattern search by category
- Pattern recommendations based on content
- Batch processing (multiple patterns at once)
- Custom pattern upload
- Pattern output caching
