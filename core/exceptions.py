class VideoDownloaderError(Exception):
    pass

class InvalidURLError(VideoDownloaderError):
    pass

class PlaylistURLError(VideoDownloaderError):
    def __init__(self):
        super().__init__("Playlist URLs are not supported. Please use a single video URL.")

class VideoUnavailableError(VideoDownloaderError):
    pass

class AgeRestrictedError(VideoDownloaderError):
    def __init__(self):
        super().__init__("This video is age-restricted and cannot be downloaded without authentication.")

class DownloadTimeoutError(VideoDownloaderError):
    pass

class FFmpegMissingError(VideoDownloaderError):
    def __init__(self):
        super().__init__("FFmpeg is not installed. Please install FFmpeg to use this app.")

class FileSizeLimitExceededError(VideoDownloaderError):
    def __init__(self, size_mb):
        super().__init__(
            f"To maintain server stability on our free hosting platform, "
            f"downloads are capped at 300MB. Please select a lower resolution "
            f"or choose a shorter video. (Estimated: {size_mb:.0f}MB)"
        )

class DownloadError(VideoDownloaderError):
    pass
