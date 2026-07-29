import re

DEFAULT_RESOLUTIONS = ["1080p", "720p", "480p", "360p", "Audio Only (MP3)"]
MAX_FILE_SIZE_BYTES = 300 * 1024 * 1024
MAX_DURATION_SECONDS = 3600
TEMP_DIR_PREFIX = "yt_dl_"
DOWNLOAD_TIMEOUT = 300
FILENAME_TEMPLATE = "{title}_{resolution}.{ext}"

SAFE_FILENAME_REGEX = re.compile(r'[^\w\-_\. ]')
