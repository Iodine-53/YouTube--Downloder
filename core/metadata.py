import yt_dlp
from core.exceptions import (
    PlaylistURLError,
    AgeRestrictedError,
    VideoUnavailableError,
)


def fetch_video_info(url):
    opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": False,
        "skip_download": True,
        "impersonate": None,
        "extractor_args": {
            "youtube": {
                "player_client": ["default", "-web_safari"],
                "player_js_version": ["actual"]
            }
        },
    }
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
    except yt_dlp.utils.DownloadError as e:
        msg = str(e).lower()
        if "private" in msg or "unavailable" in msg:
            raise VideoUnavailableError("This video is private or unavailable.")
        if "age" in msg:
            raise AgeRestrictedError()
        if "playlist" in msg:
            raise PlaylistURLError()
        if "unsupported url" in msg:
            raise VideoUnavailableError("Invalid or unsupported URL.")
        raise VideoUnavailableError(f"Could not fetch video: {str(e)[:200]}")

    if info.get("_type") == "playlist" or info.get("entries"):
        raise PlaylistURLError()

    if info.get("age_limit") and info["age_limit"] >= 18:
        raise AgeRestrictedError()

    if not info.get("title"):
        raise VideoUnavailableError("Video is unavailable or private.")

    return info


def parse_available_resolutions(formats):
    seen = set()
    result = []
    for f in formats:
        if f.get("height") and f.get("vcodec") != "none":
            label = f"{f['height']}p"
            if label not in seen:
                seen.add(label)
                result.append(label)
    result.sort(key=lambda x: int(x.replace("p", "")), reverse=True)
    result.append("Audio Only (MP3)")
    return result


def estimate_size_for_resolution(formats, height):
    candidates = [f for f in formats if f.get("height") == height]
    for f in candidates:
        if f.get("filesize"):
            return f["filesize"]
        if f.get("filesize_approx"):
            return f["filesize_approx"]
    return 0


def format_duration(seconds):
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    if h:
        return f"{h}h {m}m {s}s"
    return f"{m}m {s}s"
