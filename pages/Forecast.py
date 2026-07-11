import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
import plotly.express as px

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Sales Forecast",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Machine Learning Sales Forecast")

# -----------------------------
# Load Data
# -----------------------------
conn = sqlite3.connect("database/sales.db")

df = pd.read_sql(
    "SELECT * FROM sales",
    conn
)

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

daily_sales["day"] = np.arange(len(daily_sales))

X = daily_sales[["day"]]
y = daily_sales["total"]

# -----------------------------
# Train Model
# -----------------------------
model = LinearRegression()

model.fit(X, y)

predicted_train = model.predict(X)

# -----------------------------
# Accuracy
# -----------------------------
mae = mean_absolute_error(y, predicted_train)

rmse = np.sqrt(
    mean_squared_error(y, predicted_train)
)

# -----------------------------
# Forecast Days
# -----------------------------
st.sidebar.header("Forecast Settings")

forecast_days = st.sidebar.selectbox(
    "Forecast Period",
    [7, 30, 90]
)

future_days = np.arange(
    len(daily_sales),
    len(daily_sales) + forecast_days
).reshape(-1, 1)

future_predictions = model.predict(
    future_days
)

future_dates = pd.date_range(
    daily_sales["date"].max() + pd.Timedelta(days=1),
    periods=forecast_days
)

forecast_df = pd.DataFrame({
    "Date": future_dates,
    "Predicted Sales": future_predictions
})

# -----------------------------
# KPI Cards
# -----------------------------
col1, col2, col3 = st.columns(3)

col1.metric(
    "Forecast Days",
    forecast_days
)

col2.metric(
    "MAE",
    f"{mae:.2f}"
)

col3.metric(
    "RMSE",
    f"{rmse:.2f}"
)

st.divider()

# -----------------------------
# Forecast Table
# -----------------------------
st.subheader("📋 Forecast Data")

st.dataframe(
    forecast_df,
    width="stretch"
)

# -----------------------------
# Download CSV
# -----------------------------
csv = forecast_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    "📥 Download Forecast CSV",
    csv,
    "forecast.csv",
    "text/csv"
)

st.divider()

# -----------------------------
# Forecast Chart
# -----------------------------
actual_df = pd.DataFrame({
    "Date": daily_sales["date"],
    "Sales": daily_sales["total"],
    "Type": "Actual"
})

forecast_chart = pd.DataFrame({
    "Date": future_dates,
    "Sales": future_predictions,
    "Type": "Forecast"
})

chart_df = pd.concat(
    [actual_df, forecast_chart],
    ignore_index=True
)

fig = px.line(
    chart_df,
    x="Date",
    y="Sales",
    color="Type",
    markers=True,
    title="Actual vs Forecast Sales"
)

st.plotly_chart(
    fig,
    width="stretch"
)

st.divider()

# -----------------------------
# AI Insights
# -----------------------------
st.subheader("🤖 AI Business Insights")

avg_future = forecast_df[
    "Predicted Sales"
].mean()

last_sale = daily_sales[
    "total"
].iloc[-1]

if avg_future > last_sale:

    growth = (
        (avg_future - last_sale)
        / last_sale
    ) * 100

    st.success(
        f"""
📈 Sales are expected to increase by approximately
{growth:.2f}% over the selected forecast period.

Recommendation:
Increase inventory and prepare for higher demand.
"""
    )

else:

    drop = (
        (last_sale - avg_future)
        / last_sale
    ) * 100

    st.warning(
        f"""
📉 Sales may decrease by approximately
{drop:.2f}% over the selected forecast period.

Recommendation:
Launch promotions or marketing campaigns.
"""
    )

st.info(
    """
This forecast is generated using a Linear Regression model.
Future versions of this project can use Prophet, XGBoost,
or LSTM for more accurate predictions.
"""
)