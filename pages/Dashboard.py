import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# ---------------------------------
# Page Configuration
# ---------------------------------
st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Retail Sales Analytics Dashboard")
st.markdown("---")

# ---------------------------------
# Database Connection
# ---------------------------------
conn = sqlite3.connect("database/sales.db")
df = pd.read_sql("SELECT * FROM sales", conn)
conn.close()

# ---------------------------------
# Check Data
# ---------------------------------
if df.empty:
    st.warning("⚠ No sales data available.")
    st.stop()

# ---------------------------------
# Data Preparation
# ---------------------------------
df["date"] = pd.to_datetime(df["date"])

# ---------------------------------
# Sidebar Filters
# ---------------------------------
st.sidebar.header("🔍 Filters")

products = ["All"] + sorted(df["product"].unique().tolist())
selected_product = st.sidebar.selectbox(
    "Product",
    products
)

customers = ["All"] + sorted(df["customer"].unique().tolist())
selected_customer = st.sidebar.selectbox(
    "Customer",
    customers
)

if selected_product != "All":
    df = df[df["product"] == selected_product]

if selected_customer != "All":
    df = df[df["customer"] == selected_customer]

# ---------------------------------
# KPI Cards
# ---------------------------------
total_sales = df["total"].sum()
orders = len(df)
customer_count = df["customer"].nunique()
profit = total_sales * 0.20

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💰 Total Sales",
    f"₹ {total_sales:,.2f}"
)

col2.metric(
    "📦 Orders",
    orders
)

col3.metric(
    "💵 Estimated Profit",
    f"₹ {profit:,.2f}"
)

col4.metric(
    "👥 Customers",
    customer_count
)

st.markdown("---")

# ---------------------------------
# Charts Row 1
# ---------------------------------
col1, col2 = st.columns(2)

with col1:

    st.subheader("📈 Sales Trend")

    sales_by_date = (
        df.groupby("date")["total"]
        .sum()
        .reset_index()
    )

    fig = px.line(
        sales_by_date,
        x="date",
        y="total",
        markers=True
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    st.subheader("🥧 Product-wise Sales")

    product_sales = (
        df.groupby("product")["total"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        product_sales,
        names="product",
        values="total",
        hole=0.45
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------
# Charts Row 2
# ---------------------------------
col1, col2 = st.columns(2)

with col1:

    st.subheader("🏆 Top Customers")

    customer_sales = (
        df.groupby("customer")["total"]
        .sum()
        .reset_index()
        .sort_values(
            by="total",
            ascending=False
        )
    )

    fig = px.bar(
        customer_sales,
        x="customer",
        y="total"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    st.subheader("📦 Product Sales")

    product_chart = (
        df.groupby("product")["total"]
        .sum()
    )

    st.bar_chart(product_chart)

# ---------------------------------
# Monthly Sales
# ---------------------------------
st.markdown("---")

st.subheader("📅 Monthly Sales")

monthly_sales = (
    df.groupby(
        df["date"].dt.to_period("M")
    )["total"]
    .sum()
)

monthly_sales.index = monthly_sales.index.astype(str)

st.area_chart(monthly_sales)

# ---------------------------------
# Sales Records
# ---------------------------------
st.markdown("---")

st.subheader("📄 Sales Records")

st.dataframe(
    df,
    use_container_width=True
)

# ---------------------------------
# Download CSV
# ---------------------------------
csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇ Download Sales Report",
    data=csv,
    file_name="sales_report.csv",
    mime="text/csv"
)