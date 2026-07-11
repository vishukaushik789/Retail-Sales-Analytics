import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Sales Forecast",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Sales Forecasting")

# -----------------------------
# Load Data
# -----------------------------
conn = sqlite3.connect("database/sales.db")

df = pd.read_sql("SELECT * FROM sales", conn)

conn.close()

if df.empty:
    st.warning("No sales data available.")
    st.stop()

# -----------------------------
# Prepare Data
# -----------------------------
df["date"] = pd.to_datetime(df["date"])

daily_sales = (
    df.groupby("date")["total"]
      .sum()
      .reset_index()
)

daily_sales = daily_sales.sort_values("date")

# Create day numbers
daily_sales["day"] = np.arange(len(daily_sales))

# Features & Target
X = daily_sales[["day"]]
y = daily_sales["total"]

# -----------------------------
# Train Model
# -----------------------------
model = LinearRegression()

model.fit(X, y)

# -----------------------------
# Predict Next 30 Days
# -----------------------------
future_days = np.arange(
    len(daily_sales),
    len(daily_sales) + 30
).reshape(-1, 1)

predictions = model.predict(future_days)

future_dates = pd.date_range(
    daily_sales["date"].max() + pd.Timedelta(days=1),
    periods=30
)

forecast_df = pd.DataFrame({
    "Date": future_dates,
    "Predicted Sales": predictions
})

# -----------------------------
# Show Forecast Table
# -----------------------------
st.subheader("📋 Next 30 Days Forecast")

st.dataframe(
    forecast_df,
    width="stretch"
)

# -----------------------------
# Forecast Chart
# -----------------------------
chart_df = pd.DataFrame({
    "Date": list(daily_sales["date"]) + list(future_dates),
    "Sales": list(daily_sales["total"]) + list(predictions),
    "Type": (
        ["Actual"] * len(daily_sales)
        + ["Forecast"] * 30
    )
})

fig = px.line(
    chart_df,
    x="Date",
    y="Sales",
    color="Type",
    markers=True,
    title="Sales Forecast"
)

st.plotly_chart(
    fig,
    width="stretch"
)

st.success("Forecast generated successfully!")