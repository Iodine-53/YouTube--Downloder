import os
import shutil
from config.settings import SAFE_FILENAME_REGEX


def sanitize_filename(title):
    safe = SAFE_FILENAME_REGEX.sub("", title).strip()
    return safe[:80] or "video"


def cleanup_session_dir(dirpath):
    if os.path.exists(dirpath):
        shutil.rmtree(dirpath, ignore_errors=True)
