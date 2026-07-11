import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

# ----------------------------------
# Page Configuration
# ----------------------------------
st.set_page_config(
    page_title="Sales Management",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 Sales Management")

# ----------------------------------
# Database Connection
# ----------------------------------
conn = sqlite3.connect("database/sales.db")
cursor = conn.cursor()

# ----------------------------------
# Add New Sale
# ----------------------------------
st.subheader("➕ Add New Sale")

col1, col2 = st.columns(2)

with col1:
    customer = st.text_input("Customer Name")

with col2:
    product = st.text_input("Product Name")

col3, col4 = st.columns(2)

with col3:
    price = st.number_input(
        "Price",
        min_value=0.0,
        format="%.2f"
    )

with col4:
    qty = st.number_input(
        "Quantity",
        min_value=1,
        step=1
    )

if st.button("💾 Save Sale", use_container_width=True):

    if customer.strip() == "" or product.strip() == "":
        st.warning("Please enter Customer and Product name.")

    else:

        total = price * qty

        cursor.execute(
            """
            INSERT INTO sales
            (customer, product, price, quantity, total, date)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                customer,
                product,
                price,
                qty,
                total,
                str(date.today())
            )
        )

        conn.commit()

        st.success("✅ Sale Saved Successfully!")
        st.rerun()

# ----------------------------------
# Load Data
# ----------------------------------
df = pd.read_sql(
    "SELECT * FROM sales ORDER BY id DESC",
    conn
)

if df.empty:

    st.info("No sales available.")

else:

    df["date"] = pd.to_datetime(df["date"])

    st.divider()

    # ----------------------------------
    # Search & Filters
    # ----------------------------------
    st.subheader("🔍 Search & Filters")

    col1, col2, col3 = st.columns(3)

    with col1:
        search = st.text_input("Search Customer")

    with col2:
        products = ["All"] + sorted(df["product"].unique().tolist())

        selected_product = st.selectbox(
            "Filter Product",
            products
        )

    with col3:
        selected_date = st.date_input(
            "Filter Date",
            value=None
        )

    filtered_df = df.copy()

    if search:

        filtered_df = filtered_df[
            filtered_df["customer"].str.contains(
                search,
                case=False,
                na=False
            )
        ]

    if selected_product != "All":

        filtered_df = filtered_df[
            filtered_df["product"] == selected_product
        ]

    if selected_date:

        filtered_df = filtered_df[
            filtered_df["date"].dt.date == selected_date
        ]

    # ----------------------------------
    # Sales History
    # ----------------------------------
    st.divider()

    st.subheader("📋 Sales History")

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

    # ----------------------------------
    # Edit / Delete
    # ----------------------------------
    st.divider()

    st.subheader("✏ Edit / 🗑 Delete Sale")

    if filtered_df.empty:

        st.warning("No sales found for selected filters.")

    else:

        sale_id = st.selectbox(
            "Select Sale ID",
            filtered_df["id"].tolist()
        )

        sale = filtered_df[
            filtered_df["id"] == sale_id
        ]

        if not sale.empty:

            sale = sale.iloc[0]

            customer_edit = st.text_input(
                "Customer",
                value=sale["customer"]
            )

            product_edit = st.text_input(
                "Product",
                value=sale["product"]
            )

            price_edit = st.number_input(
                "Price",
                value=float(sale["price"])
            )

            qty_edit = st.number_input(
                "Quantity",
                value=int(sale["quantity"])
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "✏ Update Sale",
                    use_container_width=True
                ):

                    total = price_edit * qty_edit

                    cursor.execute(
                        """
                        UPDATE sales
                        SET customer=?,
                            product=?,
                            price=?,
                            quantity=?,
                            total=?
                        WHERE id=?
                        """,
                        (
                            customer_edit,
                            product_edit,
                            price_edit,
                            qty_edit,
                            total,
                            sale_id
                        )
                    )

                    conn.commit()

                    st.success("✅ Sale Updated Successfully!")

                    st.rerun()

            with col2:

                if st.button(
                    "🗑 Delete Sale",
                    use_container_width=True
                ):

                    cursor.execute(
                        "DELETE FROM sales WHERE id=?",
                        (sale_id,)
                    )

                    conn.commit()

                    st.success("🗑 Sale Deleted Successfully!")

                    st.rerun()

conn.close()