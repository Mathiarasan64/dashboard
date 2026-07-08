import plotly.express as px


# ---------------- Monthly Collection Chart ----------------
def monthly_collection_chart(metrics):

    data = {
        "Month": ["June", "July"],
        "Collection": [
            metrics["june_collection"],
            metrics["july_collection"]
        ]
    }

    fig = px.bar(
        data,
        x="Month",
        y="Collection",
        color="Month",
        text_auto=True,
        title="Monthly Collection",
        template="plotly_white"
    )

    fig.update_layout(
        title_x=0.5,
        height=420,
        xaxis_title="Month",
        yaxis_title="Collection Amount"
    )

    return fig


# ---------------- Payment Type Distribution ----------------
def payment_type_chart(metrics):

    data = {
        "Payment Type": ["One Shot", "EMI"],
        "Sales": [
            metrics["one_shot_sales"],
            metrics["emi_sales"]
        ]
    }

    fig = px.pie(
        data,
        names="Payment Type",
        values="Sales",
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
        height=420
    )

    return fig


# ---------------- Active vs Closed Learners ----------------
def active_closed_chart(metrics):

    data = {
        "Status": ["Active", "Closed"],
        "Learners": [
            metrics["active_learners"],
            metrics["closed_learners"]
        ]
    }

    fig = px.bar(
        data,
        x="Status",
        y="Learners",
        color="Status",
        text_auto=True,
        title="Active vs Closed Learners",
        template="plotly_white"
    )

    fig.update_layout(
        title_x=0.5,
        height=420,
        xaxis_title="Learner Status",
        yaxis_title="No. of Learners"
    )

    return fig


# ---------------- Collection vs Pending ----------------
def collection_pending_chart(metrics):

    data = {
        "Type": ["Collected", "Pending"],
        "Amount": [
            metrics["amount_collected"],
            metrics["pending_amount"]
        ]
    }

    fig = px.bar(
        data,
        x="Type",
        y="Amount",
        color="Type",
        text_auto=True,
        title="Collection vs Pending",
        template="plotly_white"
    )

    fig.update_layout(
        title_x=0.5,
        height=420,
        xaxis_title="Status",
        yaxis_title="Amount"
    )

    return fig


# ---------------- Top 10 Pending Students ----------------
def top_pending_students(df):

    pending_df = (
        df.sort_values(
            by="Pending",
            ascending=False
        )
        .head(10)
    )

    fig = px.bar(
        pending_df,
        x="Student Name",
        y="Pending",
        color="Pending",
        text_auto=True,
        title="Top 10 Pending Students",
        template="plotly_white"
    )

    fig.update_layout(
        title_x=0.5,
        height=500,
        xaxis_title="Student Name",
        yaxis_title="Pending Amount"
    )

    return fig
