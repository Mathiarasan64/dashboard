from anyio import current_time
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from datetime import datetime
from zoneinfo import ZoneInfo

from components.kpi_cards import kpi_card
from components.learner_profile import show_learner_profile

from data import load_data
from metrics import calculate_metrics
from charts import (
    monthly_collection_chart,
    payment_type_chart,
    active_closed_chart,
    collection_pending_chart,
    top_pending_students,
    revenue_breakdown_chart,
    expected_actual_chart,
    learner_distribution_chart
)
from styles import load_css
from utils import (
    format_currency,
    dataframe_to_csv,
    search_student
)

# ==========================
# PAGE CONFIG
# ==========================



st.set_page_config(
    page_title="Revenue Dashboard",
    page_icon="💰",
    layout="wide"
)

# ==========================
# LOAD CSS
# ==========================

st.markdown(load_css(), unsafe_allow_html=True)

# ==========================
# AUTO REFRESH
# ==========================

st_autorefresh(
    interval=5000,
    key="dashboard_refresh"
)

# ==========================
# LOAD DATA
# ==========================
st.cache_data.clear()
df = load_data()
master_df = df.copy()


#st.write("Master Rows:", len(master_df))
#st.write("Current Rows:", len(df))

# =====================================
# FILTER SESSION STATE
# =====================================

defaults = {
    "learner_filter": "All Learners",
    "payment_filter": "All",
    "status_filter": "All",
    "course_filter": "All",
    "month_filter": "All",
    "collection_month_filter": "All",
    "search_filter": ""
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

def reset_filters():
    for key in [
        "learner_filter",
        "payment_filter",
        "status_filter",
        "course_filter",
        "month_filter",
        "collection_month_filter",
        "search_filter",
    ]:
        if key in st.session_state:
            del st.session_state[key]


# ==========================================================
# PREMIUM EXECUTIVE HEADER
# ==========================================================

from datetime import datetime
from zoneinfo import ZoneInfo

current_time = datetime.now(
    ZoneInfo("Asia/Kolkata")
)

st.markdown("""
<style>

.header-box{
background:white;
padding:28px;
border-radius:20px;
border:1px solid #E2E8F0;
box-shadow:0 8px 24px rgba(15,23,42,.08);
margin-bottom:25px;
}

.live-badge{
background:#ECFDF5;
color:#16A34A;
padding:10px 18px;
border-radius:12px;
font-weight:700;
font-size:18px;
text-align:center;
border:1px solid #BBF7D0;
}

.time-box{
background:#F8FAFC;
padding:15px;
border-radius:12px;
border:1px solid #E2E8F0;
text-align:center;
margin-top:12px;
}

</style>
""", unsafe_allow_html=True)

left, right = st.columns([4.5, 1.5])

# ----------------------------
# LEFT SIDE
# ----------------------------

with left:

    st.markdown("""
    <h1 style="
    margin-bottom:5px;
    font-size:42px;
    color:#0F172A;
    ">
    📊 Revenue Analytics Dashboard
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style="
    color:#64748B;
    font-size:20px;
    margin-top:0;
    ">
    AI Powered Training Operations Dashboard
    </p>
    """, unsafe_allow_html=True)

# ----------------------------
# RIGHT SIDE
# ----------------------------

with right:

    st.markdown("""
    <div class="live-badge">
    🟢 LIVE
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="time-box">

    <div style="
    color:#64748B;
    font-size:14px;
    ">
    Last Updated
    </div>

    <div style="
    font-size:30px;
    font-weight:700;
    color:#0F172A;
    margin-top:8px;
    ">
    {current_time.strftime("%I:%M %p")}
    </div>

    <div style="
    color:#2563EB;
    margin-top:10px;
    font-size:16px;
    font-weight:600;
    ">
    {current_time.strftime("%d %b %Y")}
    </div>

    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

st.divider()

st.markdown("""
<div style="
background:linear-gradient(90deg,#2563EB,#1D4ED8);
padding:20px;
border-radius:15px;
color:white;
margin-bottom:25px;
">

<h2 style="margin:0;">
📊 Executive Revenue Dashboard
</h2>

<p style="
margin-top:10px;
font-size:16px;
">
Real-time monitoring of learners, collections, revenue and payment analytics.
</p>

</div>
""", unsafe_allow_html=True)

# ==========================================
# FILTER OPTIONS
# ==========================================

learner_options = ["All Learners"] + sorted(
    master_df["Student Name"].dropna().unique().tolist()
)

#st.write("Learner Options Count:", len(learner_options))
#st.write(learner_options)

payment_options = ["All"] + sorted(
    master_df["Payment Type"].dropna().unique().tolist()
)

status_options = ["All"] + sorted(
    master_df["Learner Status"].dropna().unique().tolist()
)

course_options = ["All"] + sorted(
    master_df["Course Name"].dropna().unique().tolist()
)

month_options = [
    "All",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
    "January",
    "February",
    "March",
    "April",
    "May"
]

# ==========================================
# FILTER BAR
# ==========================================

st.markdown("""
<div style="
background:#F8FAFC;
padding:22px;
border-radius:18px;
border:1px solid #E2E8F0;
box-shadow:0 6px 16px rgba(15,23,42,.08);
margin-bottom:20px;
">
<h2 style="
margin:0;
font-size:38px;
font-weight:700;
color:#0F172A;">
🔍 Dashboard Filters
</h2>
""", unsafe_allow_html=True)

col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(
    [2.4, 1.4, 1.4, 1.8, 1.4, 1.4, 2.0, 0.8],
    vertical_alignment="bottom"
)

# Learner
with col1:

    learner_filter = st.selectbox(
        "👤 Learner",
        learner_options,
        key="learner_filter"
    )

# Auto Fill
if learner_filter != "All Learners":

    row = df[df["Student Name"] == learner_filter]

    if not row.empty:
    

        st.session_state.payment_filter = row.iloc[0]["Payment Type"]
        st.session_state.status_filter = row.iloc[0]["Learner Status"]
        st.session_state.course_filter = row.iloc[0]["Course Name"]

# Payment
with col2:

    payment_filter = st.selectbox(
        "💳 Payment Type",
        payment_options,
        key="payment_filter"
    )

# Status
with col3:

    status_filter = st.selectbox(
        "🟢 Learner Status",
        status_options,
        key="status_filter"
    )
with col4:

    course_filter = st.selectbox(
        "📚 Course",
        course_options,
        key="course_filter"
    )

# Month
with col5:

    month_filter = st.selectbox(
        "📅 Enrolled Month",
        month_options,
        key="month_filter"
    )

with col6:

    collection_month_filter = st.selectbox(
        "💰 Collection Month",
        month_options,
        key="collection_month_filter"
    )

# Search
with col7:

    search_text = st.text_input(
        "🔍 Search",
        key="search_filter",
        placeholder="Student Name..."
    )

# Reset
with col8:

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
<style>

/* Dropdown */
div[data-baseweb="select"] > div{
    min-height:52px;
    border-radius:12px;
}

/* Text Input */
.stTextInput input{
    height:52px;
    border-radius:12px;
}

/* Button */
.stButton > button{
    height:52px;
    border-radius:12px;
    font-weight:600;
    width:100%;
}

</style>
""", unsafe_allow_html=True)

    if st.button(
        "🔄",
        use_container_width=True
    ):
        reset_filters()
        st.rerun()
    

st.markdown("</div>", unsafe_allow_html=True)
# ==========================================
# APPLY FILTERS
# ==========================================

filtered_dashboard_df = master_df.copy()
# Learner
if learner_filter != "All Learners":

    filtered_dashboard_df = filtered_dashboard_df[
        filtered_dashboard_df["Student Name"] == learner_filter
    ]

# Payment
if payment_filter != "All":

    filtered_dashboard_df = filtered_dashboard_df[
        filtered_dashboard_df["Payment Type"] == payment_filter
    ]

# Status
if status_filter != "All":

    filtered_dashboard_df = filtered_dashboard_df[
        filtered_dashboard_df["Learner Status"] == status_filter
    ]

if course_filter != "All":

    filtered_dashboard_df = filtered_dashboard_df[
        filtered_dashboard_df["Course Name"] == course_filter
    ]



# Search
if search_text:

    filtered_dashboard_df = search_student(
        filtered_dashboard_df,
        search_text
    )

# ==========================================
# SUMMARY FILTER (Enrollment Month)
# ==========================================

summary_df = filtered_dashboard_df.copy()


if month_filter != "All":
    summary_df = summary_df[
        summary_df["Enrolled Month"] == month_filter
    ]

# Metrics
summary_metrics = calculate_metrics(
    summary_df,
    "All"
)



# ==========================================
# LEARNER PROFILE MODE
# ==========================================

if learner_filter != "All Learners":

    if not filtered_dashboard_df.empty:

        learner = filtered_dashboard_df.iloc[0]

        show_learner_profile(learner)

        st.stop()

# Dashboard Mode
is_executive_mode = learner_filter == "All Learners"

if is_executive_mode:
    st.markdown("""
    <div style="
    background:linear-gradient(90deg,#2563EB,#1D4ED8);
    padding:20px;
    border-radius:15px;
    color:white;
    margin-bottom:20px;
    ">

    <h2 style="margin:0;">
    📊 Executive Dashboard
    </h2>

    <p style="margin-top:8px;font-size:16px;">
    Monitor Revenue, Collections and Learner Performance in Real Time
    </p>

    </div>
    """, unsafe_allow_html=True)


# ==========================================
# EXECUTIVE SUMMARY
# ==========================================

st.markdown("""
<h2 style="
color:#0F172A;
margin-bottom:5px;
">
📊 Executive Summary
</h2>

<p style="
color:#64748B;
font-size:15px;
margin-top:0;
margin-bottom:20px;
">
Key business indicators for active learners and revenue collection.
</p>
""", unsafe_allow_html=True)

# ---------- Row 1 ----------

row1 = st.columns(4)

with row1[0]:
    st.metric(
        "👨‍🎓 Total Learners",
        summary_metrics["total_learners"],
        f"{summary_metrics['active_learners']} Active"
    )

with row1[1]:
    st.metric(
    label="🟢 Active Learners",
    value=summary_metrics["active_learners"],
    delta=f"{summary_metrics['inactive_learners']} InActive"
)

with row1[2]:
    st.metric(
        "💰 Active Revenue",
        format_currency(summary_metrics["active_sales"])
    )

with row1[3]:
    st.metric(
        "💼 Outstanding",
        format_currency(summary_metrics["payable_fee"])
    )

# ---------- Row 2 ----------

row2 = st.columns(4)

with row2[0]:
    st.metric(
        "✅ Amount Collected",
        format_currency(summary_metrics["amount_collected"])
    )

with row2[1]:
    st.metric(
        "📈 Collection %",
        f"{summary_metrics['collection_percentage']:.1f}%"
    )


with row2[2]:
    st.metric(
        "💵 One-shot Revenue",
        format_currency(summary_metrics["one_shot_revenue"])
    )

finance_metrics = calculate_metrics(
    summary_df,
    collection_month_filter
)
# ==========================================
# FINANCE OVERVIEW
# ==========================================

st.markdown("""
<h2 style="color:#0F172A;">
💰 Finance Overview
</h2>

<p style="
color:#64748B;
font-size:15px;
margin-top:0;
margin-bottom:20px;
">
Operational finance KPIs for collection tracking.
</p>
""", unsafe_allow_html=True)

finance1, finance2, finance3, finance4 = st.columns(4)

with finance1:
    st.metric(
        "👥 Due Learners",
        finance_metrics["collection_due_count"]
    )

with finance2:

    title = (
        "📅 All EMI Collection"
        if collection_month_filter == "All"
        else f"📅 {collection_month_filter} EMI Collection"
    )

    st.metric(
        title,
        format_currency(finance_metrics["expected_collection"]),
        delta=f"Collected: {format_currency(finance_metrics['current_collection'])}"
    )

with finance3:
    st.metric(
        "⚠️ High Pending Learners",
        finance_metrics["high_pending_count"]
    )

with finance4:
    st.metric(
        "💳 EMI Learners",
        finance_metrics["emi_learners"]
    )

st.divider()
# =====================================================
# EXECUTIVE ANALYTICS
# =====================================================

st.markdown(
    '<div class="section-header">📊 Executive Analytics</div>',
    unsafe_allow_html=True
)

# ---------------- Row 1 ----------------

left, right = st.columns(2)

with left:
    st.plotly_chart(
        monthly_collection_chart(finance_metrics),
        width="stretch"
    )

with right:
    st.plotly_chart(
        revenue_breakdown_chart(finance_metrics),
        width="stretch"
    )

# ---------------- Row 2 ----------------

left, right = st.columns(2)

with left:
    st.plotly_chart(
        expected_actual_chart(finance_metrics),
        width="stretch"
    )

with right:
    st.plotly_chart(
        collection_pending_chart(finance_metrics),
        width="stretch"
    )

# ---------------- Row 3 ----------------

left, right = st.columns(2)

with left:
    st.plotly_chart(
        learner_distribution_chart(finance_metrics),
        width="stretch"
    )

with right:
    st.plotly_chart(
        active_closed_chart(finance_metrics),
        width="stretch"
    )

# ---------------- Row 4 ----------------

st.subheader("🏆 Top 10 Outstanding Learners")

st.caption(
    "Learners with the highest pending payable amount."
)

st.plotly_chart(
    top_pending_students(filtered_dashboard_df),
    width="stretch"
)

st.divider()


# ==========================
# STUDENT SEARCH
# ==========================

st.subheader("🔍 Search Student")

search_text = st.text_input(
    "Search by Student Name"
)

filtered_df = search_student(
    filtered_dashboard_df,
    search_text
)

st.divider()

# ==========================
# STUDENT DETAILS
# ==========================

st.subheader("📋 Student Details")

st.dataframe(
    filtered_df,
    width="stretch",
    hide_index=True
)

st.divider()

# ==========================
# DOWNLOAD REPORT
# ==========================

st.subheader("📥 Download Report")

col1, col2 = st.columns(2)

with col1:

    st.download_button(
        label="📄 Download CSV",
        data=dataframe_to_csv(filtered_df),
        file_name="Revenue_Report.csv",
        mime="text/csv",
        width="stretch"
    )

with col2:

    st.info(
        f"Showing {len(filtered_df)} of {len(df)} learners"
    )

st.divider()

# ==========================
# FOOTER
# ==========================

st.caption("© 2026 Revenue Dashboard | Built with Streamlit")
