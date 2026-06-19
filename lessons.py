import streamlit as st
from data.templates import get_stage_questions
import db
from utils import tts_save, audio_player_bytes
from pathlib import Path

PRIZES = ["Pokemon Card","Football Sticker","Cool Badge","Surprise Box"]

def lessons_page(user):
    st.header("הרפתקאות — שלבים")
    st.write(f"נמצא ברמת גיל: {user['age_group']}. שלב נוכחי: {user['current_stage']}")
    cols = st.columns([2,1])
    with cols[0]:
        stage = st.number_input("בחר שלב", min_value=1, max_value=99, value=user['current_stage'], step=1)
    with cols[1]:
        if st.button("התחל שלב"):
            run_stage(user, int(stage))

def run_stage(user, stage):
    st.subheader(f"שלב {stage} — רמת {user['age_group']}")
    qs = get_stage_questions(user['age_group'], stage)
    correct = 0
    for i,q in enumerate(qs):
        st.markdown(f"### שאלה {i+1}")
        if q["type"] == "vocab":
            # הצג תמונה אם קיימת (placeholder), נגיד מציג מילה בלבד
            st.write("תמונה: (מקום לתמונה)")
            choice = st.radio(q["prompt"], q["choices"], key=f"vocab_{i}_{stage}")
            if st.button("בדוק", key=f"check_{i}_{stage}"):
                if choice == q["answer"]:
                    st.success("נכון!")
                    correct += 1
                else:
                    st.error(f"שגוי. התשובה: {q['answer']}")
        elif q["type"] == "grammar":
            if q.get("options"):
                choice = st.radio(q["prompt"], q["options"], key=f"gram_{i}_{stage}")
                if st.button("בדוק", key=f"cgram_{i}_{stage}"):
                    if choice == q["answer"]:
                        st.success("נכון!")
                        correct += 1
                    else:
                        st.error(f"שגוי. תשובה נכונה: {q['answer']}")
            else:
                ans = st.text_input(q["prompt"], key=f"text_{i}_{stage}")
                if st.button("בדוק", key=f"ctext_{i}_{stage}"):
                    if ans.strip().lower() == q["answer"].lower():
                        st.success("נכון!")
                        correct += 1
                    else:
                        st.error(f"שגוי. תשובה נכונה: {q['answer']}")
        elif q["type"] == "reading":
            st.write(q["prompt"])
            ans = st.text_input(q["question"], key=f"read_{i}_{stage}")
            if st.button("בדוק", key=f"cread_{i}_{stage}"):
                if ans.strip().lower() == q["answer"].lower():
                    st.success("נכון!")
                    correct += 1
                else:
                    st.error(f"שגוי. תשובה נכונה: {q['answer']}")
        elif q["type"] == "video":
            st.write(f"וידאו: {q['prompt']} (צפה בקובץ) ")
            choice = st.radio(q["question"], q["choices"], key=f"vid_{i}_{stage}")
            if st.button("בדוק", key=f"cvid_{i}_{stage}"):
                if choice == q["answer"]:
                    st.success("נכון!")
                    correct += 1
                else:
                    st.error(f"שגוי. תשובה נכונה: {q['answer']}")
        else:
            st.write(q["prompt"])
            if st.button("סיים משחק קטן", key=f"mini_{i}_{stage}"):
                st.success("נחשב כהשאלה הושלמה")
                correct += 1

    st.write("---")
    st.write(f"תשובות נכונות: {correct} מתוך {len(qs)}")
    stars = int((correct / len(qs)) * 3)  # 0-3 כוכבים
    st.write(f"כוכבים לזיהוי: {'★'*stars}{'☆'*(3-stars)}")
    # במידה והצליח מעבר סף (למשל 60%) — עדכון DB וקבלת פרס כל 5 שלבים
    if st.button("סיים שלב והגש"):
        if correct >= int(0.5 * len(qs)):
            db.update_user_progress(user["id"], stage+1, add_score=correct)
            db.log_progress(user["id"], user["age_group"], stage, stars)
            # פרס כל 5 שלבים
            if stage % 5 == 0:
                prize = PRIZES[(stage//5 -1) % len(PRIZES)]
                db.update_user_progress(user["id"], stage+1, add_inventory=prize)
                st.balloons()
                st.success(f"מזל טוב! קיבלת פרס: {prize}")
            st.success("התקדמת לשלב הבא!")
            # ריענון משתמש ב-session
            st.session_state.user = db.get_user_by_name(user["name"])
        else:
            st.error("לא עברת את הסף. נסה שוב כדי לקבל יותר כוכבים.")
