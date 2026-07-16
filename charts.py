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

    fig.update_traces(
    textposition="outside",
    marker_line_width=0
)

    fig.update_layout(
    title="📅 Monthly Collection",
    title_x=0.5,
    template="plotly_white",
    height=380,
    margin=dict(l=20, r=20, t=60, b=20),
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(
        family="Arial",
        size=13,
        color="#0F172A"
    ),
    xaxis_title="Month",
    yaxis_title="Amount (₹)",
    legend_title=""
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
    textinfo="percent+label",
    hole=0.55
)

    fig.update_layout(
    title="💳 Payment Distribution",
    title_x=0.5,
    template="plotly_white",
    height=380,
    margin=dict(l=20, r=20, t=60, b=20),
    paper_bgcolor="white",
    font=dict(
        family="Arial",
        size=13
    ),
    legend_title=""
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

    fig.update_traces(
    textposition="outside",
    marker_line_width=0
)

    fig.update_layout(
    title="👨‍🎓 Learner Status",
    title_x=0.5,
    template="plotly_white",
    height=380,
    margin=dict(l=20, r=20, t=60, b=20),
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(
        family="Arial",
        size=13
    ),
    legend_title=""
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

    fig.update_traces(
    textposition="outside",
    marker_line_width=0
)

    fig.update_layout(
    title="💰 Collection vs Pending",
    title_x=0.5,
    template="plotly_white",
    height=380,
    margin=dict(l=20, r=20, t=60, b=20),
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(
        family="Arial",
        size=13
    ),
    legend_title=""
)

    return fig




import plotly.express as px


def top_pending_students(df):

    # ==================================
    # ACTIVE LEARNERS ONLY
    # ==================================

    active_df = df[
        df["Learner Status"]
        .astype(str)
        .str.strip()
        .str.lower() != "closed"
    ]

    # ==================================
    # ONLY PENDING LEARNERS
    # ==================================

    pending_df = active_df[
    active_df["Total Payable Fee"] > 0
]

    # ==================================
    # TOP 10
    # ==================================

    pending_df = pending_df.sort_values(
    by="Total Payable Fee",
    ascending=False
).head(10)
    # ==================================
    # BAR CHART
    # ==================================

    fig = px.bar(

        pending_df,

        x="Total Payable Fee",

        y="Student Name",

        orientation="h",

        text="Total Payable Fee",

        color="Total Payable Fee",

        color_continuous_scale=[
    "#DBEAFE",
    "#93C5FD",
    "#60A5FA",
    "#2563EB"
]

    )

    # ==================================
    # SHOW ₹
    # ==================================

    fig.update_traces(
    texttemplate="₹ %{x:,.0f}",
    textposition="outside",
    textfont=dict(
        size=12,
        color="#111827"
    ),
    cliponaxis=False
)

    # ==================================
    # LAYOUT
    # ==================================

    fig.update_layout(

    title="🏆 Top 10 Learners with Outstanding Fees",

    title_x=0.5,

    template="plotly_white",

    height=520,

    paper_bgcolor="white",

    plot_bgcolor="white",

    margin=dict(
        l=20,
        r=40,
        t=70,
        b=20
    ),

    xaxis_title="Outstanding Amount (₹)",

    yaxis_title="",

    coloraxis_showscale=False,

    font=dict(
        family="Arial",
        size=13,
        color="#111827"
    )
)


    fig.update_xaxes(
    tickprefix="₹ ",
    separatethousands=True,
    showgrid=True,
    gridcolor="#E5E7EB",
    zeroline=False
)

    return fig

    # ---------------- Revenue Breakdown ----------------

def revenue_breakdown_chart(metrics):

    data = {
        "Category": [
            "Active Sales",
            "Closed Sales",
            "Collected",
            "Pending"
        ],
        "Amount": [
            metrics["active_sales"],
            metrics["closed_sales"],
            metrics["amount_collected"],
            metrics["pending_amount"]
        ]
    }

    fig = px.bar(
        data,
        x="Category",
        y="Amount",
        color="Category",
        text_auto=True,
        title="Revenue Breakdown",
        template="plotly_white"
    )

    fig.update_traces(
    textposition="outside",
    marker_line_width=0
)

    fig.update_layout(
        title_x=0.5,
        height=420
    )

    return fig

    # ---------------- Expected vs Actual ----------------

def expected_actual_chart(metrics):

    data = {
        "Month": [
            "June",
            "June",
            "July",
            "July"
        ],

        "Type": [
            "Expected",
            "Collected",
            "Expected",
            "Collected"
        ],

        "Amount": [
            metrics["expected_june"],
            metrics["june_collection"],
            metrics["expected_july"],
            metrics["july_collection"]
        ]
    }

    fig = px.bar(
        data,
        x="Month",
        y="Amount",
        color="Type",
        barmode="group",
        text_auto=True,
        title="Expected vs Actual EMI",
        template="plotly_white"
    )

    fig.update_traces(
    textposition="outside",
    marker_line_width=0
)

    fig.update_layout(
        title_x=0.5,
        height=420
    )

    return fig

    # ---------------- Learner Distribution ----------------

def learner_distribution_chart(metrics):

    data = {
        "Type": [
            "One Shot",
            "EMI"
        ],

        "Learners": [
            metrics["one_shot_learners"],
            metrics["emi_learners"]
        ]
    }

    fig = px.pie(
        data,
        names="Type",
        values="Learners",
        hole=0.45,
        title="Learner Distribution",
        template="plotly_white"
    )

    fig.update_traces(
    textposition="inside",
    textinfo="percent+label",
    hole=0.55
)

    fig.update_layout(
        title_x=0.5,
        height=420
    )

    return fig


