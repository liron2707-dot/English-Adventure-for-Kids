import streamlit as st
import db

def profile_page(user):
    st.header("הפרופיל שלי")
    st.write(f"שם: {user['name']}")
    st.write(f"קבוצת גיל: {user['age_group']}")
    st.write(f"שלב נוכחי: {user['current_stage']}")
    st.write(f"ניקוד כולל: {user['score']}")
    inv = user['inventory'].split(",") if user['inventory'] else []
    if inv:
        st.write("מענקים ופרסים:")
        for it in inv:
            st.write(f"- {it}")
    else:
        st.write("עדיין אין פרסים — התחל לשחק!")

    if st.button("אפס נתוני משתמש (נקה התקדמות)"):
        # DISCLAIMER: פשוטות לצורכי דמו
        conn = db.get_conn()
        cur = conn.cursor()
        cur.execute("UPDATE users SET current_stage=1, inventory='', score=0 WHERE id=?", (user['id'],))
        conn.commit()
        conn.close()
        st.success("הנתונים אופסו.")
        st.session_state.user = db.get_user_by_name(user["name"])
