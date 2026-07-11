import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(
    page_title="Admin Panel",
    page_icon="👨‍💼",
    layout="wide"
)

st.title("👨‍💼 Admin Panel")

conn = sqlite3.connect("database/sales.db")

sales = pd.read_sql("SELECT * FROM sales", conn)

users = pd.read_sql("SELECT * FROM users", conn)

conn.close()

col1, col2 = st.columns(2)

col1.metric(
    "Total Users",
    len(users)
)

col2.metric(
    "Total Sales Records",
    len(sales)
)

st.divider()

st.subheader("Registered Users")

st.dataframe(
    users,
    width="stretch"
)

st.divider()

st.subheader("Sales Database")

st.dataframe(
    sales,
    width="stretch"
)