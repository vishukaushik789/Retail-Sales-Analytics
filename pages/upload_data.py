import streamlit as st
import pandas as pd
import sqlite3

# ----------------------------------
# Page Configuration
# ----------------------------------
st.set_page_config(
    page_title="Upload Company Data",
    page_icon="📂",
    layout="wide"
)

st.title("📂 Upload Company Sales Data")

st.write(
    "Upload a CSV file containing company sales data."
)

# ----------------------------------
# File Upload
# ----------------------------------
uploaded_file = st.file_uploader(
    "Choose CSV File",
    type=["csv"]
)

if uploaded_file is not None:

    try:

        df = pd.read_csv(uploaded_file)

        st.success("✅ File Uploaded Successfully!")

        st.divider()

        # ----------------------------------
        # Preview
        # ----------------------------------
        st.subheader("📄 Dataset Preview")

        st.dataframe(
            df,
            width="stretch"
        )

        # ----------------------------------
        # Dataset Information
        # ----------------------------------
        st.divider()

        st.subheader("📊 Dataset Information")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Rows",
            len(df)
        )

        col2.metric(
            "Columns",
            len(df.columns)
        )

        col3.metric(
            "Missing Values",
            int(df.isnull().sum().sum())
        )

        # ----------------------------------
        # Required Columns
        # ----------------------------------
        required_columns = [
            "customer",
            "product",
            "price",
            "quantity",
            "total",
            "date"
        ]

        missing_columns = [
            column
            for column in required_columns
            if column not in df.columns
        ]

        st.divider()

        st.subheader("✅ Dataset Validation")

        if missing_columns:

            st.error(
                f"Missing Columns: {', '.join(missing_columns)}"
            )

            st.stop()

        else:

            st.success(
                "Dataset contains all required columns."
            )

        # ----------------------------------
        # Duplicate Rows
        # ----------------------------------
        duplicates = df.duplicated().sum()

        if duplicates > 0:

            st.warning(
                f"{duplicates} duplicate rows found."
            )

        else:

            st.success("No duplicate rows found.")

        # ----------------------------------
        # Missing Values
        # ----------------------------------
        missing_values = df.isnull().sum()

        if missing_values.sum() > 0:

            st.warning("Missing Values")

            st.dataframe(
                missing_values,
                width="stretch"
            )

        else:

            st.success("No missing values found.")

        # ----------------------------------
        # Import Button
        # ----------------------------------
        st.divider()

        if st.button(
            "📥 Import into Database",
            width="stretch"
        ):

            conn = sqlite3.connect(
                "database/sales.db"
            )

            df.to_sql(
                "sales",
                conn,
                if_exists="append",
                index=False
            )

            conn.close()

            st.success(
                "🎉 Data Imported Successfully!"
            )

            st.balloons()

    except Exception as e:

        st.error(f"Error: {e}")