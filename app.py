
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from data import load_data
from metrics import calculate_metrics

from charts import (
    monthly_collection_chart,
    payment_type_chart,
    active_closed_chart,
    collection_pending_chart,
    top_pending_students
)

from styles import load_css

st.set_page_config(
  page_title="Revenue Dashboard",
  page_icon="💰",
  layout="wide"
)
st.markdown(load_css(), unsafe_allow_html=True)

st_autorefresh(interval=5000,key="refresh")
df=load_data()
metrics=calculate_metrics(df)
st.title("💰 Revenue & Collection Dashboard")
c1,c2,c3,c4,c5=st.columns(5)
c1.metric("Learners",metrics["total_learners"])
c2.metric("Active",metrics["active_learners"])
c3.metric("Closed",metrics["closed_learners"])
c4.metric("Sales",f"₹ {metrics['total_sales']:,.0f}")
c5.metric("Collected",f"₹ {metrics['amount_collected']:,.0f}")
st.progress(min(metrics["collection_percentage"]/100,1.0))
l,r=st.columns(2)
with l: st.plotly_chart(monthly_collection_chart(metrics),use_container_width=True)
with r: st.plotly_chart(payment_type_chart(metrics),use_container_width=True)
st.plotly_chart(active_closed_chart(metrics),use_container_width=True)
st.plotly_chart(collection_pending_chart(metrics),use_container_width=True)
st.plotly_chart(top_pending_students(df),use_container_width=True)
st.dataframe(df,hide_index=True,use_container_width=True)
