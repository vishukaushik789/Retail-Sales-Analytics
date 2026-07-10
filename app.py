import streamlit as st
import sqlite3
import bcrypt

DB_PATH = "database/sales.db"

st.set_page_config(
    page_title="Retail Sales Analytics",
    page_icon="📊",
    layout="wide"
)

# ---------------- Session ---------------- #

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# ---------------- Login Function ---------------- #

def login(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT password, role FROM users WHERE username=?",
        (username,)
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        stored_password = user[0]

        if bcrypt.checkpw(password.encode(), stored_password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()

# ---------------- Main ---------------- #

if not st.session_state.logged_in:

    st.title("📊 Retail Sales Analytics Platform")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        login(username, password)

else:

    st.sidebar.title("Navigation")

    page = st.sidebar.radio(
        "Go to",
        [
            "Dashboard"
        ]
    )

    st.sidebar.write(f"👤 {st.session_state.username}")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    if page == "Dashboard":
        exec(open("pages/Dashboard.py").read())