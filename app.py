import streamlit as st
import plotly.express as px
from streamlit_autorefresh import st_autorefresh
from data import load_data

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Revenue Dashboard",
    page_icon="💰",
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown("""
<style>
.stApp{
    background:#F8FAFC;
}

h1{
    text-align:center;
    color:#1E3A8A;
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

st_autorefresh(interval=5000, key="refresh")

# ---------------- LOAD DATA ----------------
df = load_data()

# ---------- NORMALIZE COLUMN NAMES ----------
df.columns = (
    df.columns
    .str.strip()
    .str.replace("\n", " ", regex=False)
)

# Show columns once for debugging
with st.expander("🔍 Column Names (Debug)"):
    st.write(df.columns.tolist())

# Mapping (edit only if your sheet uses different names)
COLUMN_MAP = {
    "Students Name": "Student Name",
    "Student Name": "Student Name",
    "Payment type": "Payment Type",
    "Payment Type": "Payment Type",
    "Total price": "Total price",
    "Advance / amount paid": "Advance / amount paid",
    "Pending": "Pending",
    "June": "June",
    "July": "July",
    "Payment Status (June)": "Payment Status June",
    "Payment Status (July)": "Payment Status July",
}

df.rename(columns=COLUMN_MAP, inplace=True)

# Convert numeric columns
money_columns = [
    "Total price",
    "Advance / amount paid",
    "Pending",
    "June",
    "July"
]

for col in money_columns:
    if col in df.columns:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace("₹", "", regex=False)
            .str.replace("-", "0", regex=False)
        )
        df[col] = df[col].replace("", "0")
        df[col] = df[col].astype(float)

# ---------------- TITLE ----------------
st.title("💰 Revenue & Collection Dashboard")

st.info("📊 Live Dashboard | Auto Refresh Every 5 Seconds")

st.divider()

# ---------------- KPI ----------------
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("👨‍🎓 Learners", len(df))

with c2:
    revenue = df["Total price"].sum() if "Total price" in df.columns else 0
    st.metric("💰 Revenue", f"₹ {revenue:,.0f}")

with c3:
    collected = df["Advance / amount paid"].sum() if "Advance / amount paid" in df.columns else 0
    st.metric("✅ Collected", f"₹ {collected:,.0f}")

with c4:
    pending = df["Pending"].sum() if "Pending" in df.columns else 0
    st.metric("⚠ Outstanding", f"₹ {pending:,.0f}")

st.divider()

# ---------------- CHARTS ----------------
left, right = st.columns(2)

with left:

    if "June" in df.columns and "July" in df.columns:

        monthly = {
            "Month": ["June", "July"],
            "Collection": [
                df["June"].sum(),
                df["July"].sum()
            ]
        }

        fig = px.bar(
            monthly,
            x="Month",
            y="Collection",
            color="Month",
            text="Collection",
            title="Monthly Collection"
        )

        st.plotly_chart(fig, use_container_width=True)

with right:

    if "Payment Type" in df.columns:

        payment = (
            df["Payment Type"]
            .value_counts()
            .reset_index()
        )

        payment.columns = ["Payment Type", "Count"]

        fig = px.pie(
            payment,
            names="Payment Type",
            values="Count",
            hole=.45,
            title="Payment Type Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---------------- SEARCH ----------------
st.subheader("🔍 Search Student")

search = st.text_input("Enter Student Name")

if "Student Name" in df.columns:

    if search:

        filtered = df[
            df["Student Name"]
            .str.contains(search, case=False, na=False)
        ]

    else:

        filtered = df

else:

    filtered = df

# ---------------- TABLE ----------------
st.subheader("📋 Student Details")

st.dataframe(
    filtered,
    use_container_width=True
)

# ---------------- DOWNLOAD ----------------
st.download_button(
    "📥 Download CSV",
    filtered.to_csv(index=False),
    file_name="Revenue_Report.csv",
    mime="text/csv"
)
