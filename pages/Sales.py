import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

st.set_page_config(page_title="Sales")

st.title("🛒 Sales Management")

conn = sqlite3.connect("database/sales.db")

st.subheader("Add New Sale")

customer = st.text_input("Customer Name")
product = st.text_input("Product Name")

price = st.number_input("Price", min_value=0.0)
qty = st.number_input("Quantity", min_value=1)

if st.button("Save Sale"):

    total = price * qty

    conn.execute("""
    INSERT INTO sales
    (customer,product,price,quantity,total,date)
    VALUES (?,?,?,?,?,?)
    """,
    (
        customer,
        product,
        price,
        qty,
        total,
        str(date.today())
    ))

    conn.commit()

    st.success("Sale Saved Successfully!")

st.divider()

st.subheader("Sales History")

df = pd.read_sql("SELECT * FROM sales", conn)

st.dataframe(df, use_container_width=True)