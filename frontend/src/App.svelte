<script lang="ts">
  import { onMount } from 'svelte';

  let videoId = 'dQw4w9WgXcQ';
  let format: 'json' | 'text' | 'srt' | 'vtt' = 'text';
  let loading = false;
  let error = '';
  let result = '';
  let theme = 'dark';
  let availableTranscripts: any[] = [];
  let selectedLanguage = 'en';
  let showSummary = false;
  let summary = '';
  let summaryLoading = false;

  const API_BASE = import.meta.env.DEV ? '/api' : 'https://api.automatehub.dev';

  function extractVideoId(input: string): string {
    // Handle full YouTube URLs
    const urlPattern = /(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})/;
    const match = input.match(urlPattern);
    return match ? match[1] : input;
  }

  async function fetchTranscript() {
    error = '';
    result = '';
    loading = true;

    try {
      const id = extractVideoId(videoId);
      const url = `${API_BASE}/transcript/${id}?format=${format}&languages=${selectedLanguage}`;
      const response = await fetch(url);

      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || 'Failed to fetch transcript');
      }

      if (format === 'json') {
        const data = await response.json();
        result = JSON.stringify(data, null, 2);
      } else {
        result = await response.text();
      }
    } catch (err: any) {
      error = err.message;
    } finally {
      loading = false;
    }
  }

  async function listTranscripts() {
    error = '';
    availableTranscripts = [];
    loading = true;

    try {
      const id = extractVideoId(videoId);
      const response = await fetch(`${API_BASE}/transcript/${id}/list`);

      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || 'Failed to list transcripts');
      }

      const data = await response.json();
      availableTranscripts = data.available_transcripts;
    } catch (err: any) {
      error = err.message;
    } finally {
      loading = false;
    }
  }

  async function summarizeTranscript() {
    error = '';
    summary = '';
    summaryLoading = true;

    try {
      const id = extractVideoId(videoId);
      const response = await fetch(`${API_BASE}/transcript/${id}/summarize?languages=${selectedLanguage}`);

      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || 'Failed to summarize transcript');
      }

      const data = await response.json();
      summary = data.summary;
      showSummary = true;
    } catch (err: any) {
      error = err.message;
    } finally {
      summaryLoading = false;
    }
  }

  function downloadTranscript() {
    const blob = new Blob([result], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `transcript-${extractVideoId(videoId)}.${format}`;
    a.click();
    URL.revokeObjectURL(url);
  }

  function toggleTheme() {
    const themes = ['dark', 'light', 'cupcake', 'cyberpunk'];
    const currentIndex = themes.indexOf(theme);
    theme = themes[(currentIndex + 1) % themes.length];
    document.documentElement.setAttribute('data-theme', theme);
  }

  onMount(() => {
    document.documentElement.setAttribute('data-theme', theme);
  });
</script>

<div class="min-h-screen bg-base-200">
  <div class="navbar bg-base-100 shadow-lg">
    <div class="flex-1">
      <a href="/" class="btn btn-ghost text-xl">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="M3.375 19.5h17.25m-17.25 0a1.125 1.125 0 01-1.125-1.125M3.375 19.5h1.5C5.496 19.5 6 18.996 6 18.375m-3.75 0V5.625m0 12.75v-1.5c0-.621.504-1.125 1.125-1.125m18.375 2.625V5.625m0 12.75c0 .621-.504 1.125-1.125 1.125m1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125m0 3.75h-1.5A1.125 1.125 0 0118 18.375M20.625 4.5H3.375m17.25 0c.621 0 1.125.504 1.125 1.125M20.625 4.5h-1.5C18.504 4.5 18 5.004 18 5.625m3.75 0v1.5c0 .621-.504 1.125-1.125 1.125M3.375 4.5c-.621 0-1.125.504-1.125 1.125M3.375 4.5h1.5C5.496 4.5 6 5.004 6 5.625m-3.75 0v1.5c0 .621.504 1.125 1.125 1.125m0 0h1.5m-1.5 0c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125m1.5-3.75C5.496 8.25 6 7.746 6 7.125v-1.5M4.875 8.25C5.496 8.25 6 8.754 6 9.375v1.5m0-5.25v5.25m0-5.25C6 5.004 6.504 4.5 7.125 4.5h9.75c.621 0 1.125.504 1.125 1.125m1.125 2.625h1.5m-1.5 0A1.125 1.125 0 0118 7.125v-1.5m1.125 2.625c-.621 0-1.125.504-1.125 1.125v1.5m2.625-2.625c.621 0 1.125.504 1.125 1.125v1.5c0 .621-.504 1.125-1.125 1.125M18 5.625v5.25M7.125 12h9.75m-9.75 0A1.125 1.125 0 016 10.875M7.125 12C6.504 12 6 12.504 6 13.125m0-2.25C6 11.496 5.496 12 4.875 12M18 10.875c0 .621-.504 1.125-1.125 1.125M18 10.875c0 .621.504 1.125 1.125 1.125m-2.25 0c.621 0 1.125.504 1.125 1.125m-12 5.25v-5.25m0 5.25c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125m-12 0v-1.5c0-.621-.504-1.125-1.125-1.125M18 18.375v-5.25m0 5.25v-1.5c0-.621.504-1.125 1.125-1.125M18 13.125v1.5c0 .621.504 1.125 1.125 1.125M18 13.125c0-.621.504-1.125 1.125-1.125M6 13.125v1.5c0 .621-.504 1.125-1.125 1.125M6 13.125C6 12.504 5.496 12 4.875 12m-1.5 0h1.5m-1.5 0c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125M19.125 12h1.5m0 0c.621 0 1.125.504 1.125 1.125v1.5c0 .621-.504 1.125-1.125 1.125m-17.25 0h1.5m14.25 0h1.5" />
        </svg>
        YouTube Transcript
      </a>
    </div>
    <div class="flex-none">
      <button class="btn btn-ghost btn-circle" on:click={toggleTheme}>
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M9.53 16.122a3 3 0 00-5.78 1.128 2.25 2.25 0 01-2.4 2.245 4.5 4.5 0 008.4-2.245c0-.399-.078-.78-.22-1.128zm0 0a15.998 15.998 0 003.388-1.62m-5.043-.025a15.994 15.994 0 011.622-3.395m3.42 3.42a15.995 15.995 0 004.764-4.648l3.876-5.814a1.151 1.151 0 00-1.597-1.597L14.146 6.32a15.996 15.996 0 00-4.649 4.763m3.42 3.42a6.776 6.776 0 00-3.42-3.42" />
        </svg>
      </button>
    </div>
  </div>

  <div class="container mx-auto p-4 max-w-4xl">
    <div class="card bg-base-100 shadow-xl">
      <div class="card-body">
        <h2 class="card-title text-2xl mb-4">Extract YouTube Transcripts</h2>

        <div class="form-control">
          <label class="label">
            <span class="label-text">YouTube Video ID or URL</span>
          </label>
          <input
            type="text"
            placeholder="dQw4w9WgXcQ or https://youtube.com/watch?v=..."
            class="input input-bordered w-full"
            bind:value={videoId}
          />
        </div>

        <div class="flex gap-4">
          <div class="form-control flex-1">
            <label class="label">
              <span class="label-text">Language</span>
            </label>
            <input
              type="text"
              placeholder="en"
              class="input input-bordered"
              bind:value={selectedLanguage}
            />
            <label class="label">
              <span class="label-text-alt">e.g., en, es, de</span>
            </label>
          </div>

          <div class="form-control flex-1">
            <label class="label">
              <span class="label-text">Output Format</span>
            </label>
            <select class="select select-bordered" bind:value={format}>
              <option value="text">Text</option>
              <option value="json">JSON</option>
              <option value="srt">SRT Subtitles</option>
              <option value="vtt">WebVTT</option>
            </select>
          </div>
        </div>

        <div class="flex gap-2 mt-4 flex-wrap">
          <button class="btn btn-primary" on:click={fetchTranscript} disabled={loading}>
            {#if loading}
              <span class="loading loading-spinner"></span>
            {/if}
            Fetch Transcript
          </button>

          <button class="btn btn-secondary" on:click={listTranscripts} disabled={loading}>
            List Languages
          </button>

          <button class="btn btn-accent" on:click={summarizeTranscript} disabled={summaryLoading}>
            {#if summaryLoading}
              <span class="loading loading-spinner"></span>
            {/if}
            AI Summary
          </button>

          {#if result}
            <button class="btn btn-info" on:click={downloadTranscript}>
              Download
            </button>
          {/if}
        </div>

        {#if error}
          <div class="alert alert-error mt-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
            <span>{error}</span>
          </div>
        {/if}

        {#if availableTranscripts.length > 0}
          <div class="mt-4">
            <h3 class="text-lg font-bold mb-2">Available Transcripts</h3>
            <div class="overflow-x-auto">
              <table class="table table-zebra">
                <thead>
                  <tr>
                    <th>Language</th>
                    <th>Code</th>
                    <th>Generated</th>
                    <th>Translatable</th>
                  </tr>
                </thead>
                <tbody>
                  {#each availableTranscripts as transcript}
                    <tr>
                      <td>{transcript.language}</td>
                      <td><span class="badge badge-primary">{transcript.language_code}</span></td>
                      <td><span class="badge {transcript.is_generated ? 'badge-warning' : 'badge-success'}">{transcript.is_generated ? 'Auto' : 'Manual'}</span></td>
                      <td>{transcript.is_translatable ? '✓' : '✗'}</td>
                    </tr>
                  {/each}
                </tbody>
              </table>
            </div>
          </div>
        {/if}

        {#if showSummary && summary}
          <div class="mt-4">
            <div class="flex justify-between items-center mb-2">
              <h3 class="text-lg font-bold">AI Summary</h3>
              <button class="btn btn-sm btn-ghost" on:click={() => showSummary = false}>Close</button>
            </div>
            <div class="prose max-w-none bg-base-200 p-4 rounded-lg">
              {@html summary.replace(/\n/g, '<br>')}
            </div>
          </div>
        {/if}

        {#if result}
          <div class="mt-4">
            <h3 class="text-lg font-bold mb-2">Result</h3>
            <div class="mockup-code">
              <pre><code>{result}</code></pre>
            </div>
          </div>
        {/if}
      </div>
    </div>

    <div class="mt-8 text-center text-sm opacity-60">
      <p>Built with Svelte + DaisyUI</p>
      <p class="mt-2">
        <a href="https://github.com/yourusername/fastapi-youtube-transcript" class="link link-hover">View on GitHub</a>
      </p>
    </div>
  </div>
</div>
