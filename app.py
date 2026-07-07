import streamlit as st
import plotly.express as px
from streamlit_autorefresh import st_autorefresh
from data import load_data

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Revenue Dashboard",
    page_icon="💰",
    layout="wide"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
<style>

.stApp{
    background:#F8FAFC;
}

h1{
    color:#1E3A8A;
    text-align:center;
    font-weight:bold;
}

[data-testid="stMetric"]{
    background:white;
    border-radius:15px;
    padding:18px;
    border:1px solid #E5E7EB;
    box-shadow:0px 3px 10px rgba(0,0,0,.08);
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# AUTO REFRESH
# -----------------------------
st_autorefresh(interval=5000, key="refresh")

# -----------------------------
# LOAD DATA
# -----------------------------
df = load_data()

# -----------------------------
# TITLE
# -----------------------------
st.title("💰 Revenue & Collection Dashboard")

st.info("📊 Live Dashboard | Auto Refresh Every 5 Seconds")

st.divider()

# -----------------------------
# KPI CARDS
# -----------------------------
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "👨‍🎓 Learners",
        len(df)
    )

with c2:
    st.metric(
        "💰 Revenue",
        f"₹ {df['Total price'].sum():,.0f}"
    )

with c3:
    st.metric(
        "✅ Collected",
        f"₹ {df['Advance / amount paid'].sum():,.0f}"
    )

with c4:
    st.metric(
        "⚠ Outstanding",
        f"₹ {df['Pending'].sum():,.0f}"
    )

st.divider()

# -----------------------------
# CHARTS
# -----------------------------
left, right = st.columns(2)

with left:

    st.subheader("📈 Monthly Revenue")

    monthly = {
        "Month": ["June", "July"],
        "Collection": [
            df["June"].sum(),
            df["July"].sum()
        ]
    }

    fig1 = px.bar(
        monthly,
        x="Month",
        y="Collection",
        color="Month",
        text="Collection"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

with right:

    st.subheader("🥧 Payment Type")

    payment = (
        df["Payment Type"]
        .value_counts()
        .reset_index()
    )

    payment.columns = [
        "Payment Type",
        "Count"
    ]

    fig2 = px.pie(
        payment,
        names="Payment Type",
        values="Count",
        hole=.45
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# -----------------------------
# PAYMENT STATUS
# -----------------------------
left, right = st.columns(2)

with left:

    st.subheader("📊 Payment Status")

    status = (
        df["Payment Status - June"]
        .value_counts()
        .reset_index()
    )

    status.columns = [
        "Status",
        "Students"
    ]

    fig3 = px.bar(
        status,
        x="Status",
        y="Students",
        color="Status",
        text="Students"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

with right:

    st.subheader("🏆 Top 10 Highest Fee Learners")

    top = (
        df.sort_values(
            "Total price",
            ascending=False
        )
        .head(10)
    )

    fig4 = px.bar(
        top,
        x="Student Name",
        y="Total price",
        color="Total price",
        text="Total price"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

st.divider()

# -----------------------------
# STUDENT TABLE
# -----------------------------
st.subheader("📋 Student Payment Details")

search = st.text_input("🔍 Search Student")

if search:
    filtered = df[
        df["Student Name"]
        .str.contains(search, case=False, na=False)
    ]
else:
    filtered = df

st.dataframe(
    filtered,
    use_container_width=True
)

st.download_button(
    "📥 Download CSV",
    filtered.to_csv(index=False),
    file_name="student_payment_report.csv",
    mime="text/csv"
)
