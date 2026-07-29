import os
import tempfile
import streamlit as st

from config.settings import MAX_FILE_SIZE_BYTES
from core.metadata import (
    fetch_video_info,
    parse_available_resolutions,
    estimate_size_for_resolution,
)
from core.downloader import download_video, download_audio
from core.exceptions import (
    VideoDownloaderError,
)
from utils.validators import is_valid_youtube_url, is_playlist_url
from utils.file_utils import sanitize_filename, cleanup_session_dir
from ui.layout import (
    setup_page_config,
    inject_custom_css,
    render_header,
    render_footer_note,
)
from ui.state import init_session_state, reset_download_state
from ui.components import (
    render_url_input,
    render_video_card,
    render_resolution_selector,
    render_download_button,
    render_download_delivery,
    render_status_text,
)


def main():
    setup_page_config()
    inject_custom_css()
    init_session_state()
    render_header()

    url = render_url_input()

    if url and st.session_state.download_status == "idle":
        if is_playlist_url(url):
            st.markdown(
                "<div class='error-box'>Playlist URLs are not supported. "
                "Please use a single video URL.</div>",
                unsafe_allow_html=True,
            )
            st.stop()

        if not is_valid_youtube_url(url):
            st.markdown(
                "<div class='error-box'>Invalid YouTube URL. "
                "Please enter a valid video link.</div>",
                unsafe_allow_html=True,
            )
            st.stop()

        st.session_state.url = url
        st.session_state.download_status = "fetching"

    if st.session_state.download_status == "fetching":
        st.session_state.video_info = None
        st.session_state.download_error = None
        status_placeholder = st.empty()
        status_placeholder.markdown(
            "<div style='text-align:center;padding:1rem;'>Fetching video info...</div>",
            unsafe_allow_html=True,
        )

        try:
            info = fetch_video_info(url)
            st.session_state.video_info = info
            st.session_state.download_status = "ready"
        except VideoDownloaderError as e:
            st.session_state.download_error = str(e)
            st.session_state.download_status = "error"

        status_placeholder.empty()

    if st.session_state.download_status == "error":
        st.markdown(
            f"<div class='error-box'>{st.session_state.download_error}</div>",
            unsafe_allow_html=True,
        )
        st.session_state.download_status = "idle"
        return

    if st.session_state.video_info:
        with st.container():
            st.markdown("<div class='video-card'>", unsafe_allow_html=True)
            render_video_card(st.session_state.video_info)
            st.markdown("</div>", unsafe_allow_html=True)

        resolutions = parse_available_resolutions(
            st.session_state.video_info.get("formats", [])
        )
        selected = render_resolution_selector(resolutions)
        st.session_state.selected_resolution = selected

        size_exceeded = False
        if selected != "Audio Only (MP3)" and st.session_state.video_info.get("formats"):
            height = int(selected.replace("p", ""))
            est = estimate_size_for_resolution(
                st.session_state.video_info["formats"], height
            )
            if est > MAX_FILE_SIZE_BYTES:
                size_exceeded = True
                st.markdown(
                    f"<div class='size-warning'>⚠️ To maintain server stability on our free "
                    f"hosting platform, downloads are capped at 300MB. Please select a lower "
                    f"resolution or choose a shorter video. "
                    f"(Estimated: {est / (1024*1024):.0f}MB)</div>",
                    unsafe_allow_html=True,
                )

        if render_download_button(
            disabled=size_exceeded, label=f"⬇ Download {selected}"
        ):
            st.session_state.download_status = "downloading"
            st.rerun()

    if st.session_state.download_status == "downloading":
        session_dir = tempfile.mkdtemp(
            prefix=f"yt_dl_{st.session_state.session_id}_"
        )
        status_placeholder = st.empty()
        status_placeholder.markdown(
            "<div style='text-align:center;padding:1rem;'>Starting download...</div>",
            unsafe_allow_html=True,
        )

        try:
            if st.session_state.selected_resolution == "Audio Only (MP3)":
                data = download_audio(
                    st.session_state.url, session_dir, status_placeholder
                )
                ext = "mp3"
                res_label = "Audio"
            else:
                height = int(st.session_state.selected_resolution.replace("p", ""))
                data = download_video(
                    st.session_state.url, height, session_dir, status_placeholder
                )
                ext = "mp4"
                res_label = st.session_state.selected_resolution

            title = sanitize_filename(st.session_state.video_info["title"])
            filename = f"{title}_{res_label}.{ext}"
            st.session_state.download_bytes = data
            st.session_state.download_filename = filename
            st.session_state.download_status = "done"
        except VideoDownloaderError as e:
            st.session_state.download_status = "error"
            st.session_state.download_error = str(e)
        finally:
            cleanup_session_dir(session_dir)
            status_placeholder.empty()

    if st.session_state.download_status == "done":
        render_download_delivery(
            st.session_state.download_bytes, st.session_state.download_filename
        )
        reset_download_state()

    if st.session_state.download_status == "error":
        st.markdown(
            f"<div class='error-box'>{st.session_state.download_error}</div>",
            unsafe_allow_html=True,
        )
        st.session_state.download_status = "idle"

    render_footer_note()


if __name__ == "__main__":
    main()
