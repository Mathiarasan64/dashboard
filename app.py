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


# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("🎛 Dashboard Filters")

# Payment Type Filter
if "Payment Type" in df.columns:
    payment_types = sorted(df["Payment Type"].dropna().unique())

    selected_payment = st.sidebar.multiselect(
        "Payment Type",
        payment_types,
        default=payment_types
    )

    df = df[df["Payment Type"].isin(selected_payment)]

# Search Student
if "Student Name" in df.columns:
    student = st.sidebar.text_input("🔍 Search Student")

    if student:
        df = df[df["Student Name"].str.contains(student, case=False, na=False)]


# ---------- NORMALIZE COLUMN NAMES ----------
df.columns = (
    df.columns
    .str.strip()
    .str.replace("\n", " ", regex=False)
)



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
    "Payment Status July": "Payment Status July",
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

# ---------------- KPI CALCULATIONS ----------------

# ---------------- KPI CALCULATIONS ----------------

total_learners = len(df)

closed_learners = len(
    df[df["Learner Status"].astype(str).str.strip().str.lower() == "closed"]
)

active_learners = total_learners - closed_learners

total_sales = df["Total price"].sum()

one_shot_sales = df[
    df["Payment Type"].astype(str).str.strip().str.lower() == "one shot"
]["Total price"].sum()

emi_sales = df[
    df["Payment Type"].astype(str).str.strip().str.lower() == "emi"
]["Total price"].sum()

closed_sales = df[
    df["Learner Status"].astype(str).str.strip().str.lower() == "closed"
]["Total price"].sum()

active_sales = total_sales - closed_sales

amount_collected = df["Advance / amount paid"].sum()

pending_amount = df["Pending"].sum()

collection_percentage = (
    (amount_collected / active_sales) * 100
    if active_sales > 0 else 0
)
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.metric("👨‍🎓 Total Learners", total_learners)

with c2:
    st.metric("👥 Active Learners", active_learners)

with c3:
    st.metric("🚫 Closed Learners", closed_learners)

with c4:
    st.metric("💰 Total Sales", f"₹ {total_sales:,.0f}")

with c5:
    st.metric("🟢 Active Sales", f"₹ {active_sales:,.0f}")

c6, c7, c8, c9, c10 = st.columns(5)

with c6:
    st.metric("💵 One Shot Sales", f"₹ {one_shot_sales:,.0f}")

with c7:
    st.metric("💳 EMI Sales", f"₹ {emi_sales:,.0f}")

with c8:
    st.metric("✅ Amount Collected", f"₹ {amount_collected:,.0f}")

with c9:
    st.metric("⚠ Pending Amount", f"₹ {pending_amount:,.0f}")

with c10:
    st.metric("📈 Collection %", f"{collection_percentage:.1f}%")

# ---------------- REVENUE PROGRESS ----------------
st.subheader("📈 Revenue Collection Progress")

# ---------------- REVENUE PROGRESS ----------------

st.subheader("📈 Revenue Collection Progress")

if active_sales > 0:
    progress = amount_collected / active_sales
else:
    progress = 0

progress = min(progress, 1.0)

st.progress(progress)

st.write(
    f"Collected ₹{amount_collected:,.0f} / ₹{active_sales:,.0f} ({progress*100:.1f}%)"
)
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
            text_auto=True,
            title="Monthly Collection",
            template="plotly_white"
        )

        fig.update_layout(
            title_x=0.5,
            height=450
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
            hole=0.45,
            title="Payment Type Distribution",
            template="plotly_white"
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

        fig.update_layout(
            title_x=0.5,
            height=450
        )

        st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---------------- SEARCH ----------------
filtered = df.copy()

# ---------------- TABLE ----------------
# ---------------- TABLE ----------------
# ---------------- TABLE ----------------
# ---------------- TABLE ----------------
st.subheader("📋 Student Details")

# Reset dataframe index
filtered = filtered.reset_index(drop=True)

# Display dataframe without Streamlit index
st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True
)

# ---------------- DOWNLOAD ----------------
st.download_button(
    "📥 Download CSV",
    filtered.to_csv(index=False),
    file_name="Revenue_Report.csv",
    mime="text/csv"
)
