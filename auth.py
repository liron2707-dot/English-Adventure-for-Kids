import streamlit as st
import db

def login_page():
    st.sidebar.header("כניסה / יצירת משתמש")
    name = st.sidebar.text_input("שם הילד/ה")
    age_group = st.sidebar.selectbox("קבוצת גיל", ["7-9", "10-12", "13-15"])
    if st.sidebar.button("התחבר / צור משתמש"):
        if not name.strip():
            st.sidebar.error("אנא הכנס שם חוקי.")
        else:
            user = db.get_user_by_name(name.strip())
            if user:
                # אם קיים אבל קבוצת גיל שונה — נעדכן רק אם המשתמש בוחר לשנות
                if user["age_group"] != age_group:
                    db.update_user_progress(user["id"], user["current_stage"])  # dummy
                st.sidebar.success(f"התחברת בתור {user['name']}")
                st.session_state.user = user
                return user
            else:
                user = db.create_user(name.strip(), age_group)
                st.sidebar.success(f"משתמש נוצר: {user['name']}")
                st.session_state.user = user
                return user
    # אם כבר מחובר ב-session
    if "user" in st.session_state:
        return st.session_state.user
    return None
