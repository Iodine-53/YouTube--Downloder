# YouTube Video Downloader

A professional YouTube video downloader with a clean Streamlit web interface powered by yt-dlp.

## Features

- Fetch video metadata (title, thumbnail, duration, available resolutions)
- Download video at quality up to 1080p
- Download audio-only (MP3, 192kbps)
- 300MB file size cap for server stability
- Session-isolated temporary files (safe for concurrent use)
- Clean, modern UI with light/dark mode support
- Public videos only — no auth/cookie support

## Prerequisites

- **Python 3.10+**
- **FFmpeg** (system-wide installation)

### Installing FFmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
```bash
winget install ffmpeg
# Or download from https://ffmpeg.org/download.html
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update && sudo apt install ffmpeg -y
```

**Linux (Fedora/RHEL):**
```bash
sudo dnf install ffmpeg -y
```

Verify installation:
```bash
ffmpeg -version
```

## Local Setup

```bash
# Enter the project directory
cd youtube-downloader

# Create virtual environment
python -m venv .venv

# Activate it
# macOS/Linux:
source .venv/bin/activate
# Windows:
# .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

## Deploy to Streamlit Cloud

1. Push this project to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Set Python version to `3.10` or higher
5. The `packages.txt` file will automatically install FFmpeg on Streamlit Cloud's servers
6. Deploy!

## Usage

1. Paste a YouTube video URL into the input box
2. Wait for the video metadata to load (thumbnail, title, duration)
3. Select quality — available resolutions or Audio Only (MP3)
4. Click **Download**
5. Wait for processing, then click the download button in your browser

## Limitations

- **Public videos only** — no authentication or cookie support
- **Single videos only** — playlists are not supported
- **Max 300MB** per download to maintain server stability
- **Max ~1 hour** duration recommended to prevent timeouts
