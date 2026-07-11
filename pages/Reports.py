import streamlit as st
import sqlite3
import pandas as pd
from utils.export import export_excel

# -----------------------------------
# Page Configuration
# -----------------------------------
st.set_page_config(
    page_title="Reports",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Sales Reports & Analytics")

# -----------------------------------
# Load Data
# -----------------------------------
conn = sqlite3.connect("database/sales.db")

df = pd.read_sql("SELECT * FROM sales", conn)

conn.close()

if df.empty:
    st.warning("No sales data available.")
    st.stop()

# -----------------------------------
# Data Preparation
# -----------------------------------
df["date"] = pd.to_datetime(df["date"])

df["Month"] = df["date"].dt.strftime("%B")

# -----------------------------------
# KPI Cards
# -----------------------------------
total_sales = df["total"].sum()
orders = len(df)
customers = df["customer"].nunique()
products = df["product"].nunique()

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Sales", f"₹{total_sales:,.2f}")
col2.metric("📦 Orders", orders)
col3.metric("👥 Customers", customers)
col4.metric("🛍 Products", products)

st.divider()

# -----------------------------------
# Monthly Sales
# -----------------------------------
st.subheader("📈 Monthly Sales")

monthly_sales = (
    df.groupby("Month")["total"]
      .sum()
      .sort_values(ascending=False)
)

st.bar_chart(monthly_sales)

st.divider()

# -----------------------------------
# Top Products
# -----------------------------------
st.subheader("🏆 Top 5 Products")

top_products = (
    df.groupby("product")["total"]
      .sum()
      .sort_values(ascending=False)
      .head(5)
)

st.bar_chart(top_products)

st.divider()

# -----------------------------------
# Top Customers
# -----------------------------------
st.subheader("👥 Top Customers")

top_customers = (
    df.groupby("customer")["total"]
      .sum()
      .sort_values(ascending=False)
      .head(5)
)

st.bar_chart(top_customers)

st.divider()

# -----------------------------------
# Sales Records
# -----------------------------------
st.subheader("📋 Sales Records")

st.dataframe(
    df,
    width="stretch"
)

# -----------------------------------
# Export Excel
# -----------------------------------
st.divider()

st.subheader("📥 Export Report")

if st.button("Export to Excel"):

    file = export_excel(df)

    with open(file, "rb") as f:

        st.download_button(
            label="⬇ Download Excel Report",
            data=f,
            file_name=file,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )