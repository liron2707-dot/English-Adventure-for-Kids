import streamlit as st
from data.templates import get_stage_questions
from utils import tts_save, audio_player_bytes
import db

def quiz_page(user):
    st.header("חידון מהיר — 5 שאלות")
    if st.button("התחל חידון"):
        run_quiz(user)

def run_quiz(user):
    # נולד חידון קצר מתוך השלב הנוכחי
    stage = user["current_stage"]
    qs = get_stage_questions(user["age_group"], stage)[:5]
    correct = 0
    for i,q in enumerate(qs):
        st.markdown(f"**שאלה {i+1}**")
        if q["type"] == "vocab":
            choice = st.radio(q["prompt"], q["choices"], key=f"qv_{i}")
            if st.button("בדוק תשובה", key=f"qc_{i}"):
                if choice == q["answer"]:
                    st.success("נכון!")
                    correct += 1
                else:
                    st.error(f"שגוי. התשובה: {q['answer']}")
        else:
            ans = st.text_input(q.get("question", q.get("prompt")), key=f"qa_{i}")
            if st.button("בדוק תשובה", key=f"qat_{i}"):
                if ans.strip().lower() == (q.get("answer") or "").lower():
                    st.success("נכון!")
                    correct += 1
                else:
                    st.error(f"שגוי. תשובה נכונה: {q.get('answer')}")
    st.write(f"ניקוד בחידון: {correct}/{len(qs)}")
    if correct >= 3:
        st.success("מעולה! זכית בנקודות נוספות.")
        db.update_user_progress(user["id"], user["current_stage"], add_score=correct)
    else:
        st.info("תנסה שוב כדי לשפר את הניקוד.")
    st.session_state.user = db.get_user_by_name(user["name"])
