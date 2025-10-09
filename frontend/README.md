# YouTube Transcript Frontend

A modern, responsive web interface for the YouTube Transcript API built with Svelte and DaisyUI.

## Features

- 🎨 Beautiful UI with DaisyUI components
- 🌓 Multiple theme support (Dark, Light, Cupcake, Cyberpunk)
- 📝 Multiple output formats (JSON, Text, SRT, WebVTT)
- 🌍 Multi-language transcript support
- 🤖 AI-powered transcript summarization
- 📥 Download transcripts in any format
- 📱 Fully responsive design

## Quick Start

### Development

```bash
# Install dependencies
bun install

# Start dev server
bun run dev
```

The app will be available at `http://localhost:5173`

### Building for Production

```bash
# Build for production
bun run build

# Preview production build
bun run preview
```

## API Configuration

The app automatically detects the environment:

- **Development**: Uses `/api` proxy to `http://127.0.0.1:8000`
- **Production**: Uses `https://api.automatehub.dev`

To change the production API URL, update `API_BASE` in `src/App.svelte`:

```typescript
const API_BASE = import.meta.env.DEV ? '/api' : 'https://your-api-url.com';
```

## Usage

1. **Enter Video ID or URL**: Paste a YouTube video ID (e.g., `dQw4w9WgXcQ`) or full URL
2. **Select Language**: Choose the transcript language (default: `en`)
3. **Choose Format**: Select output format (Text, JSON, SRT, or VTT)
4. **Actions**:
   - **Fetch Transcript**: Get the transcript in selected format
   - **List Languages**: See all available transcript languages
   - **AI Summary**: Generate an AI-powered summary
   - **Download**: Save the transcript to your device

## Tech Stack

- **Svelte 5** - Modern reactive UI framework
- **Vite** - Fast build tool and dev server
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first CSS framework
- **DaisyUI** - Beautiful component library
- **Bun** - Fast JavaScript runtime and package manager

## Project Structure

```
frontend/
├── src/
│   ├── App.svelte       # Main application component
│   ├── main.ts          # Application entry point
│   ├── app.css          # Global styles with Tailwind
│   └── vite-env.d.ts    # TypeScript definitions
├── public/              # Static assets
├── index.html           # HTML template
├── vite.config.ts       # Vite configuration
├── tailwind.config.js   # Tailwind + DaisyUI config
└── package.json         # Dependencies
```

## Available Themes

Toggle between themes using the theme button in the navbar:

- 🌙 **Dark** (default)
- ☀️ **Light**
- 🧁 **Cupcake**
- 🤖 **Cyberpunk**

## Development Notes

- The app uses Vite's proxy feature to avoid CORS issues in development
- All API calls are type-safe with TypeScript
- Components use Svelte 5's new runes syntax for reactivity
- DaisyUI provides ready-to-use, accessible components

## License

MIT
