from pathlib import Path
import streamlit as st
import pandas as pd

# ---------------------------------
# PAGE CONFIGURATION
# ---------------------------------
st.set_page_config(
    page_title="Afficionado Coffee Analytics",
    page_icon="☕",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent
CHARTS_DIR = BASE_DIR / "charts"
OUTPUTS_DIR = BASE_DIR / "outputs"

# ---------------------------------
# CUSTOM STYLING
# ---------------------------------
st.markdown("""
<style>
.main {
    background-color: #faf8f5;
}
h1, h2, h3 {
    color: #5b3825;
}
[data-testid="stMetric"] {
    background-color: #f0e7df;
    padding: 18px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------
# HEADER
# ---------------------------------
st.title("☕ Afficionado Coffee Roasters")
st.subheader("Sales Trend and Time-Based Performance Analysis")
st.caption("FY 2025 | Unified Mentor – Data Analytics Internship")

st.markdown("""
This interactive dashboard presents sales performance, store comparisons,
product category contribution and time-based transaction patterns using
149,116 transaction records.
""")

st.divider()

# ---------------------------------
# SIDEBAR
# ---------------------------------
st.sidebar.title("Dashboard Navigation")

page = st.sidebar.radio(
    "Select a section",
    ["Overview", "Time Analysis", "Store & Product Analysis",
     "All Charts", "Data Outputs", "Key Findings"]
)

# ---------------------------------
# OVERVIEW
# ---------------------------------
if page == "Overview":

    st.header("Business Performance Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Transaction Records", "149,116")
    col2.metric("Gross Revenue", "$698,812.33")
    col3.metric("Units Sold", "214,470")

    col4, col5 = st.columns(2)

    col4.metric("Average Transaction Value", "$4.69")
    col5.metric("Average Units per Record", "1.44")

    st.divider()

    st.subheader("Project Scope")

    st.write("""
    - Analyze overall sales and transaction performance.
    - Evaluate hourly and daypart performance.
    - Compare revenue across three store locations.
    - Identify high-performing product categories.
    - Examine transaction quantity distribution.
    """)

    st.info(
        "The dataset does not contain a transaction date column. "
        "Therefore, daily, weekly and monthly sales trends are not included."
    )

# ---------------------------------
# TIME ANALYSIS
# ---------------------------------
elif page == "Time Analysis":

    st.header("Time-Based Performance")

    col1, col2, col3 = st.columns(3)

    col1.metric("Morning Revenue", "$388,288.67")
    col2.metric("Afternoon Revenue", "$204,720.83")
    col3.metric("Evening Revenue", "$105,802.83")

    st.subheader("Daypart Distribution")

    daypart_data = pd.DataFrame({
        "Daypart": ["Morning", "Afternoon", "Evening"],
        "Transaction Records": [81751, 44427, 22938],
        "Revenue": [388288.67, 204720.83, 105802.83]
    })

    st.dataframe(daypart_data, use_container_width=True)

    st.write("""
    **Key observation:** Morning recorded the highest activity,
    contributing 54.82% of transaction records and 55.56% of revenue.

    The busiest individual hour was 10:00–10:59, with 18,545 records.
    """)

    chart = CHARTS_DIR / "01_hourly_sales_and_volume_trend.png"

    if chart.exists():
        st.image(str(chart), use_container_width=True)

    chart = CHARTS_DIR / "02_daypart_performance_unified_mentor.png"

    if chart.exists():
        st.image(str(chart), use_container_width=True)

    chart = CHARTS_DIR / "03_peak_moderate_offpeak_distribution.png"

    if chart.exists():
        st.image(str(chart), use_container_width=True)

# ---------------------------------
# STORE AND PRODUCT ANALYSIS
# ---------------------------------
elif page == "Store & Product Analysis":

    st.header("Store Performance")

    store_data = pd.DataFrame({
        "Store": ["Hell's Kitchen", "Astoria", "Lower Manhattan"],
        "Transaction Records": [50735, 50599, 47782],
        "Units Sold": [71737, 70991, 71742],
        "Revenue": [236511.17, 232243.91, 230057.25],
        "Average Transaction Value": [4.66, 4.59, 4.81]
    })

    st.dataframe(store_data, use_container_width=True)

    st.subheader("Product Category Performance")

    category_data = pd.DataFrame({
        "Category": [
            "Coffee", "Tea", "Bakery", "Drinking Chocolate",
            "Coffee beans", "Branded", "Loose Tea",
            "Flavours", "Packaged Chocolate"
        ],
        "Revenue": [
            269952.45, 196405.95, 82315.64, 72416.00,
            40085.25, 13607.00, 11213.60, 8408.80, 4407.64
        ],
        "Revenue Share (%)": [
            38.63, 28.11, 11.78, 10.36, 5.74,
            1.95, 1.60, 1.20, 0.63
        ]
    })

    st.dataframe(category_data, use_container_width=True)

    st.subheader("Store Comparison Chart")

    chart = CHARTS_DIR / "04_store_revenue_and_atv_comparison.png"

    if chart.exists():
        st.image(str(chart), use_container_width=True)

    st.subheader("Product Category Chart")

    chart = CHARTS_DIR / "05_product_category_pareto_distribution.png"

    if chart.exists():
        st.image(str(chart), use_container_width=True)

    chart = CHARTS_DIR / "06_top_10_revenue_generating_products.png"

    if chart.exists():
        st.image(str(chart), use_container_width=True)

# ---------------------------------
# ALL CHARTS
# ---------------------------------
elif page == "All Charts":

    st.header("Complete Visual Analysis")

    if CHARTS_DIR.exists():

        chart_files = sorted(CHARTS_DIR.glob("*.png"))

        if chart_files:

            for i in range(0, len(chart_files), 2):

                col1, col2 = st.columns(2)

                with col1:
                    st.image(
                        str(chart_files[i]),
                        caption=chart_files[i].stem.replace("_", " "),
                        use_container_width=True
                    )

                if i + 1 < len(chart_files):
                    with col2:
                        st.image(
                            str(chart_files[i + 1]),
                            caption=chart_files[i + 1].stem.replace("_", " "),
                            use_container_width=True
                        )
        else:
            st.warning("No chart images were found in the charts folder.")

    else:
        st.error("The charts folder is missing.")

# ---------------------------------
# DATA OUTPUTS
# ---------------------------------
elif page == "Data Outputs":

    st.header("Generated Analysis Files")

    if OUTPUTS_DIR.exists():

        csv_files = sorted(OUTPUTS_DIR.glob("*.csv"))

        if csv_files:

            selected_file = st.selectbox(
                "Choose an output file",
                csv_files,
                format_func=lambda x: x.name
            )

            try:
                data = pd.read_csv(selected_file)

                st.write(f"File: {selected_file.name}")
                st.dataframe(data, use_container_width=True)

                st.download_button(
                    "Download CSV",
                    data=data.to_csv(index=False).encode("utf-8"),
                    file_name=selected_file.name,
                    mime="text/csv"
                )

            except Exception as e:
                st.error(f"Could not read this file: {e}")

        else:
            st.warning("No CSV output files were found.")

    else:
        st.warning("The outputs folder is missing.")

# ---------------------------------
# KEY FINDINGS
# ---------------------------------
elif page == "Key Findings":

    st.header("Key Business Findings")

    st.markdown("""
    ### 1. Overall Performance
    - Gross revenue reached $698,812.33.
    - The dataset contains 149,116 transaction records.

    ### 2. Time-Based Performance
    - Morning generated the highest revenue contribution.
    - 10:00–10:59 was the busiest individual hour.

    ### 3. Store Performance
    - Hell's Kitchen recorded the highest revenue.
    - Lower Manhattan recorded the highest average transaction value.

    ### 4. Product Performance
    - Coffee was the leading revenue-generating category.
    - Tea was the second-largest category.

    ### 5. Business Recommendations
    - Consider aligning staffing with observed morning demand.
    - Monitor the performance of individual stores.
    - Evaluate product-category performance when planning promotions.
    """)

# ---------------------------------
# FOOTER
# ---------------------------------
st.divider()

st.caption(
    "Afficionado Coffee Roasters | FY 2025 | "
    "Unified Mentor Data Analytics Internship"
)