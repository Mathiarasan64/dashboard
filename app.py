import streamlit as st
from streamlit_autorefresh import st_autorefresh

from data import load_data
from metrics import calculate_metrics
from styles import load_css
from utils import (
    format_currency,
    dataframe_to_csv,
    search_student,
)

from charts import (
    monthly_collection_chart,
    payment_type_chart,
    active_closed_chart,
    collection_pending_chart,
    top_pending_students,
)

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Revenue Dashboard",
    page_icon="💰",
    layout="wide"
)

# ---------------- LOAD CSS ----------------

st.markdown(load_css(), unsafe_allow_html=True)

# ---------------- AUTO REFRESH ----------------

st_autorefresh(interval=5000, key="refresh")

# ---------------- LOAD DATA ----------------

df = load_data()

metrics = calculate_metrics(df)
