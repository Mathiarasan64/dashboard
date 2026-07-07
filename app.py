import streamlit as st
from streamlit_autorefresh import st_autorefresh
from data import load_data

st.set_page_config(
    page_title="Revenue Dashboard",
    page_icon="💰",
    layout="wide"
)

st_autorefresh(interval=5000, key="refresh")

df = load_data()

st.title("💰 Revenue & Collection Dashboard")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Learners",
        len(df)
    )

with col2:
    st.metric(
        "Revenue",
        f"₹ {df['Total price'].sum():,.0f}"
    )

with col3:
    st.metric(
        "Collected",
        f"₹ {df['Advance / amount paid'].sum():,.0f}"
    )

with col4:
    st.metric(
        "Outstanding",
        f"₹ {df['Pending'].sum():,.0f}"
    )

st.divider()

st.dataframe(df, use_container_width=True)
