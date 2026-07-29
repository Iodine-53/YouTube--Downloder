import uuid
import streamlit as st


def init_session_state():
    st.session_state.setdefault("session_id", str(uuid.uuid4()))
    st.session_state.setdefault("url", "")
    st.session_state.setdefault("video_info", None)
    st.session_state.setdefault("download_status", "idle")
    st.session_state.setdefault("error_message", None)
    st.session_state.setdefault("download_bytes", None)
    st.session_state.setdefault("download_filename", None)


def reset_download_state():
    st.session_state.download_status = "idle"
    st.session_state.download_bytes = None
    st.session_state.download_filename = None
