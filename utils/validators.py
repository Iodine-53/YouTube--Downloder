import re

YOUTUBE_REGEX = re.compile(
    r'(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[\w-]{11}'
)
PLAYLIST_REGEX = re.compile(r'[?&]list=')


def is_valid_youtube_url(url):
    return bool(YOUTUBE_REGEX.match(url.strip()))


def is_playlist_url(url):
    return bool(PLAYLIST_REGEX.search(url))


def extract_video_id(url):
    match = re.search(r'(?:v=|youtu\.be/)([\w-]{11})', url)
    return match.group(1) if match else None
