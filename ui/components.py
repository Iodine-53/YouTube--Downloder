import streamlit as st


def render_url_input():
    return st.text_input(
        "YouTube Video URL",
        placeholder="https://www.youtube.com/watch?v=...",
        label_visibility="collapsed",
        key="url_input",
    )


def render_video_card(info):
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(info.get("thumbnail"), use_container_width=True)
    with col2:
        st.markdown(
            f"<div class='video-title'>{info.get('title', 'Untitled')}</div>",
            unsafe_allow_html=True,
        )
        dur = info.get("duration", 0)
        m, s = divmod(dur, 60)
        h, m = divmod(m, 60)
        dur_str = f"{h}h {m}m {s}s" if h else f"{m}m {s}s"
        st.markdown(
            f"<div class='video-meta'>Duration: {dur_str}</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div class='video-meta'>{info.get('view_count', 0):,} views</div>",
            unsafe_allow_html=True,
        )


def render_resolution_selector(resolutions):
    return st.selectbox("Select Quality", resolutions, key="resolution_select")


def render_download_button(disabled, label):
    return st.button(label, type="primary", use_container_width=True, disabled=disabled)


def render_download_delivery(data, filename):
    ext = filename.rsplit(".", 1)[-1]
    mime = "audio/mpeg" if ext == "mp3" else "video/mp4"
    st.success("Download ready!")
    st.download_button(
        "📥 Click to Download",
        data=data,
        file_name=filename,
        mime=mime,
        type="primary",
        use_container_width=True,
    )


def render_status_text(text):
    st.markdown(
        f"<div style='text-align:center; color: var(--text-color-muted); "
        f"padding: 1rem;'>{text}</div>",
        unsafe_allow_html=True,
    )
