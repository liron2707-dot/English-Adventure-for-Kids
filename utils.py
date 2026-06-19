import streamlit as st
from pathlib import Path
from gtts import gTTS
import base64
import db

def init_app_style():
    st.markdown(open("assets/css/style.css", "r", encoding="utf-8").read(), unsafe_allow_html=True)
    # load optional js
    try:
        st.components.v1.html(open("assets/js/animations.js", "r", encoding="utf-8").read(), height=1)
    except Exception:
        pass

def ensure_db():
    db.init_db()

def tts_save(word, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    tts = gTTS(word, lang="en")
    tts.save(path)

def audio_player_bytes(path):
    try:
        with open(path, "rb") as f:
            return f.read()
    except Exception:
        return None
