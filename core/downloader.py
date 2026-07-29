import os
import yt_dlp
from config.settings import MAX_FILE_SIZE_BYTES
from core.exceptions import (
    FileSizeLimitExceededError,
    DownloadError,
    FFmpegMissingError,
)


def _progress_hook_factory(status_container):
    def hook(d):
        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
            downloaded = d.get("downloaded_bytes", 0)
            pct = (downloaded / total * 100) if total else 0
            mb_dl = downloaded / (1024 * 1024)
            mb_total = total / (1024 * 1024) if total else 0
            status_container.markdown(
                f"Downloading... {pct:.0f}% ({mb_dl:.1f}MB of {mb_total:.1f}MB)"
            )
        elif d["status"] == "finished":
            status_container.markdown("Processing... Converting file format.")
    return hook


def _check_ffmpeg():
    import shutil
    if shutil.which("ffmpeg") is None:
        raise FFmpegMissingError()


def _read_and_cleanup(filepath):
    size = os.path.getsize(filepath)
    if size > MAX_FILE_SIZE_BYTES:
        os.unlink(filepath)
        raise FileSizeLimitExceededError(size / (1024 * 1024))
    with open(filepath, "rb") as f:
        data = f.read()
    os.unlink(filepath)
    return data


def download_video(url, height, session_dir, progress_container):
    _check_ffmpeg()
    outtmpl = os.path.join(session_dir, "%(title)s.%(ext)s")
    opts = {
        "format": f"bestvideo[height<={height}]+bestaudio/best[height<={height}]",
        "outtmpl": outtmpl,
        "merge_output_format": "mp4",
        "quiet": True,
        "no_warnings": True,
        "progress_hooks": [_progress_hook_factory(progress_container)],
        "socket_timeout": 30,
        "extractor_args": {
            "youtube": {
                "player_client": ["default", "web_safari"],
                "player_js_version": ["actual"]
            }
        },
    }
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filepath = ydl.prepare_filename(info).rsplit(".", 1)[0] + ".mp4"
    except Exception as e:
        raise DownloadError(f"Download failed: {str(e)[:200]}")
    return _read_and_cleanup(filepath)


def download_audio(url, session_dir, progress_container):
    _check_ffmpeg()
    outtmpl = os.path.join(session_dir, "%(title)s.%(ext)s")
    opts = {
        "format": "bestaudio/best",
        "outtmpl": outtmpl,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "quiet": True,
        "no_warnings": True,
        "progress_hooks": [_progress_hook_factory(progress_container)],
        "socket_timeout": 30,
        "extractor_args": {
            "youtube": {
                "player_client": ["default", "web_safari"],
                "player_js_version": ["actual"]
            }
        },
    }
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filepath = ydl.prepare_filename(info).rsplit(".", 1)[0] + ".mp3"
    except Exception as e:
        raise DownloadError(f"Download failed: {str(e)[:200]}")
    return _read_and_cleanup(filepath)
