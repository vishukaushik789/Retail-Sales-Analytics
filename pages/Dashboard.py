import streamlit as st

st.title("📊 Retail Sales Dashboard")

st.success("Welcome to the Dashboard!")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", "₹0")
col2.metric("Orders", "0")
col3.metric("Profit", "₹0")
col4.metric("Customers", "0")

st.divider()

st.write("Charts and analytics will appear here.")