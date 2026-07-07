import streamlit as st
import pandas as pd
import plotly.express as px

from data import load_data
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="Student Dashboard",
    layout="wide"
)

st_autorefresh(interval=5000, key="refresh")

st.title("🎓 Student Performance Dashboard")

df = load_data()

if "Error" in df.columns:
    st.error(df.iloc[0]["Error"])
    st.stop()

st.success("Live data loaded successfully!")

st.dataframe(df)

numeric_columns = df.select_dtypes(include="number").columns.tolist()

if numeric_columns:

    column = st.selectbox(
        "Select Numeric Column",
        numeric_columns
    )

    col1, col2 = st.columns(2)

    with col1:
        fig = px.histogram(df, x=column)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.box(df, y=column)
        st.plotly_chart(fig2, use_container_width=True)

else:
    st.warning("No numeric columns found.")
