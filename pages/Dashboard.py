import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Retail Sales Analytics Dashboard")
st.markdown("---")

# -----------------------------
# Database Connection
# -----------------------------
conn = sqlite3.connect("database/sales.db")
df = pd.read_sql("SELECT * FROM sales", conn)
conn.close()

# -----------------------------
# Check Data
# -----------------------------
if df.empty:
    st.warning("⚠ No sales data found. Please add some sales first.")
    st.stop()

# -----------------------------
# Convert Date
# -----------------------------
df["date"] = pd.to_datetime(df["date"])

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔍 Filters")

products = ["All"] + sorted(df["product"].unique().tolist())
selected_product = st.sidebar.selectbox(
    "Select Product",
    products
)

if selected_product != "All":
    df = df[df["product"] == selected_product]

# -----------------------------
# KPIs
# -----------------------------
total_sales = df["total"].sum()
orders = len(df)
customers = df["customer"].nunique()
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
    customers
)

st.markdown("---")

# -----------------------------
# Charts
# -----------------------------
left, right = st.columns(2)

with left:

    st.subheader("📈 Sales Trend")

    sales_by_date = (
        df.groupby("date")["total"]
        .sum()
        .reset_index()
    )

    fig1 = px.line(
        sales_by_date,
        x="date",
        y="total",
        markers=True,
        title="Sales Over Time"
    )

    st.plotly_chart(fig1, use_container_width=True)

with right:

    st.subheader("🥧 Product-wise Sales")

    product_sales = (
        df.groupby("product")["total"]
        .sum()
        .reset_index()
    )

    fig2 = px.pie(
        product_sales,
        names="product",
        values="total",
        hole=0.4,
        title="Sales Distribution"
    )

    st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# Top Customers
# -----------------------------
st.markdown("---")
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

fig3 = px.bar(
    customer_sales,
    x="customer",
    y="total",
    title="Customer-wise Sales"
)

st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# Sales Table
# -----------------------------
st.markdown("---")
st.subheader("📄 Sales Records")

st.dataframe(
    df,
    use_container_width=True
)

# -----------------------------
# Download CSV
# -----------------------------
csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇ Download Sales Report",
    csv,
    "sales_report.csv",
    "text/csv"
)