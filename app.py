import streamlit as st
from auth import login_page
from lessons import lessons_page
from quiz import quiz_page
from profile import profile_page
from utils import init_app_style, ensure_db

st.set_page_config(page_title="English Adventure", layout="wide", page_icon=":star2:")
init_app_style()
ensure_db()

st.title("English Adventure 🌟")
st.sidebar.image("assets/images/logo.png", use_column_width=True)

user = login_page()
if not user:
    st.stop()

menu = st.sidebar.selectbox("תפריט", ["בית", "הרפתקאות (שלבים)", "חידון מהיר", "הפרופיל שלי", "אודות"])
if menu == "בית":
    st.header(f"ברוך הבא, {user['name']}! 🎉")
    st.markdown("בחר `הרפתקאות (שלבים)` כדי להמשיך לשלב הבא. צבור מדליות ופרסים לאורך הדרך!")
    st.image("assets/images/home_banner.png", use_column_width=True)
elif menu == "הרפתקאות (שלבים)":
    lessons_page(user)
elif menu == "חידון מהיר":
    quiz_page(user)
elif menu == "הפרופיל שלי":
    profile_page(user)
else:
    st.header("אודות")
    st.write("אפליקציה חינוכית מותאמת לילדים — אנגלית, משחקים, פרסים ועיצוב צבעוני.")
