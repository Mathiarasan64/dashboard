import streamlit as st

def kpi_card(title, value, icon="📊", color="#2563EB", subtitle=""):

    st.markdown(
        f"""
<div style="
background:white;
padding:22px;
border-radius:18px;
border-left:6px solid {color};
box-shadow:0 6px 16px rgba(0,0,0,.08);
height:150px;
">

<div style="display:flex;align-items:center;">

<div style="
width:42px;
height:42px;
border-radius:50%;
background:{color}15;
display:flex;
justify-content:center;
align-items:center;
font-size:20px;
margin-right:12px;
">
{icon}
</div>

<div>

<div style="
font-size:15px;
font-weight:600;
color:#475569;
">
{title}
</div>

<div style="
font-size:12px;
color:#94A3B8;
">
{subtitle}
</div>

</div>

</div>

<div style="
margin-top:28px;
font-size:38px;
font-weight:700;
color:#0F172A;
">

{value}

</div>

</div>
""",
        unsafe_allow_html=True,
    )