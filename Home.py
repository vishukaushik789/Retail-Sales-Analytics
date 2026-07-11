import streamlit as st
import sqlite3
import bcrypt

DB_PATH = "database/sales.db"

# ------------------------------------
# Page Configuration
# ------------------------------------

st.set_page_config(
    page_title="Retail Sales Analytics",
    page_icon="📊",
    layout="wide"
)

# ------------------------------------
# Custom CSS
# ------------------------------------

st.markdown("""
<style>

/* Sidebar */
section[data-testid="stSidebar"] *{
    font-weight:bold;
    font-size:16px;
}

/* Main Title */
.title{
    text-align:center;
    font-size:48px;
    font-weight:800;
    margin-top:30px;
    margin-bottom:40px;
}

/* Center Login */
.block-container{
    padding-top:2rem;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------
# Session State
# ------------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# ------------------------------------
# Login Function
# ------------------------------------

def login(username, password):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT password FROM users WHERE username=?",
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

        else:
            st.error("❌ Incorrect Password")

    else:
        st.error("❌ Username Not Found")

# ------------------------------------
# Login Page
# ------------------------------------

if not st.session_state.logged_in:

    st.markdown(
        "<div class='title'>Retail Sales Analytics Platform</div>",
        unsafe_allow_html=True
    )

    left, center, right = st.columns([1.5, 2, 1.5])

    with center:

        st.subheader("Admin Login")

        username = st.text_input("Username")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button(
            "Login",
            use_container_width=True
        ):
            login(username, password)

# ------------------------------------
# After Login
# ------------------------------------

else:

    st.title("🏠 Home")

    st.success(
        f"Welcome, **{st.session_state.username}** 👋"
    )

    st.info(
        "Select any page from the left sidebar to continue."
    )

    st.sidebar.markdown("---")

    st.sidebar.success(
        f"👤 {st.session_state.username}"
    )

    if st.sidebar.button(
        "🚪 Logout",
        use_container_width=True
    ):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()