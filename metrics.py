import pandas as pd


def calculate_metrics(df):

    # ==========================
    # LEARNER STATUS
    # ==========================

    learner_status = (
    df["Learner Status"]
    .astype(str)
    .str.strip()
    .str.lower()
)

    # ==========================================
    # LEARNER GROUPS
    # ==========================================

    # Revenue calculations (Active + In-Active)
    active_df = df[
        learner_status.isin(["active", "in-active"])
    ].copy()

    # Only Active learners (for KPI)
    active_learners_df = df[
        learner_status == "active"
    ].copy()

    # In-Active learners
    inactive_df = df[
        learner_status == "in-active"
    ].copy()

    # Closed learners
    closed_df = df[
        learner_status == "closed"
    ].copy()

    total_learners = len(df)
    active_learners = len(active_learners_df)
    inactive_learners = len(inactive_df)
    closed_learners = len(closed_df)

    
    print("\n========== FULLY PAID LEARNERS ==========\n")

    print(
    active_df.loc[
        active_df["Total Payable Fee"] == 0,
        [
            "Student Name",
            "Learner Status",
            "Total Payable Fee"
        ]
    ]
)

    print("\n=========================================\n")


    # ==========================
    # SALES
    # ==========================

    total_sales = df["Total price"].sum()
    closed_sales = closed_df["Total price"].sum()
    active_sales = active_df["Total price"].sum()

    # ==========================
    # PAYMENT TYPE
    # ==========================

    payment = (
        active_df["Payment Type"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    one_shot_df = active_df[
        payment.str.contains("one", na=False)
    ]

        # Manual EMI
    manual_emi_df = active_df[
        payment.str.contains("manual emi", na=False)
    ]

    # Credit Card
    credit_card_df = active_df[
        payment.str.contains("credit", na=False)
    ]

    # Revenue
    manual_emi_revenue = manual_emi_df["Total price"].sum()

    credit_card_revenue = credit_card_df["Total price"].sum()

    # Manual EMI + Credit Card Revenue
    emi_revenue = (
        manual_emi_revenue +
        credit_card_revenue
    )

    one_shot_revenue = one_shot_df["Total price"].sum()

    # Learner Count
    manual_emi_learners = len(manual_emi_df)

    credit_card_learners = len(credit_card_df)

    emi_learners = (
        manual_emi_learners +
        credit_card_learners
    )

    one_shot_learners = len(one_shot_df)

   
    # ==========================
    # COLLECTION
    # ==========================

    # Outstanding Amount
    payable_fee = active_df["Total Payable Fee"].sum()

    # Advance Amount
    # (Include Active + In-Active + Closed learners)
    advance_amount = pd.to_numeric(
        df["Advance / amount paid"],
        errors="coerce"
    ).fillna(0).sum()

    # Monthly Collection
    # (Include only Active + In-Active learners)
    monthly_columns = [
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

    monthly_columns = [
        col
        for col in monthly_columns
        if col in active_df.columns
    ]

    active_df[monthly_columns] = active_df[monthly_columns].apply(
        pd.to_numeric,
        errors="coerce"
    ).fillna(0)

    monthly_collection = active_df[
        monthly_columns
    ].sum().sum()

    # Total Amount Collected
    amount_collected = (
        advance_amount
        + monthly_collection
    )

    # Pending Amount
    pending_amount = payable_fee

    # Collection Percentage
    if active_sales > 0:
        collection_percentage = (
            amount_collected / active_sales
        ) * 100
    else:
        collection_percentage = 0

    # ==========================
    # MONTHLY COLLECTION
    # ==========================

    june_collection = active_df["June"].sum()
    july_collection = active_df["July"].sum()

    expected_june = active_df[
        "Expected EMI Collection for June"
    ].sum()

    expected_july = active_df[
        "Expected EMI Collection for July"
    ].sum()

    # ==========================
    # EXITED
    # ==========================

    june_exited = 0
    july_exited = 0

    if "Payment Status June" in df.columns:
        june_exited = (
            df["Payment Status June"]
            .astype(str)
            .str.strip()
            .str.lower()
            .eq("exited")
            .sum()
        )

    if "Payment Status July" in df.columns:
        july_exited = (
            df["Payment Status July"]
            .astype(str)
            .str.strip()
            .str.lower()
            .eq("exited")
            .sum()
        )

    # ==========================
    # BUSINESS KPIs
    # ==========================

    average_revenue = 0
    average_pending = 0

    if active_learners > 0:
        average_revenue = (
            active_sales / active_learners
        )

        average_pending = (
            payable_fee / active_learners
        )

    # ==========================
    # BUSINESS INSIGHTS
    # ==========================

    insights = []

    if collection_percentage >= 80:
        insights.append(
            "🟢 Excellent collection performance (above 80%)."
        )
    elif collection_percentage >= 60:
        insights.append(
            "🟡 Collection performance is good but can improve."
        )
    else:
        insights.append(
            "🔴 Collection performance needs immediate attention."
        )

    if pending_amount > 0:
        insights.append(
            f"💰 Outstanding payable amount: ₹{payable_fee:,.0f}"
        )

    if closed_learners > 0:
        insights.append(
            f"🚪 {closed_learners} learners are marked as Closed."
        )

    if one_shot_revenue > manual_emi_revenue:
        insights.append(
            "💵 One Shot payments contribute more revenue than EMI."
        )
    else:
        insights.append(
            "💳 EMI contributes more revenue than One Shot."
        )

    insights.append(
        f"📈 Active Sales: ₹{active_sales:,.0f}"
    )
     # ==========================
    # SMART ALERTS
    # ==========================

    # Learners who still have outstanding fees

    collection_due_count = len(
        active_df[
            active_df["Total Payable Fee"] > 0
        ]
    )

    high_pending_count = len(
        active_df[
            active_df["Total Payable Fee"] >= 50000
        ]
    )

    zero_collection_count = len(
        active_df[
            active_df["Advance / amount paid"] == 0
        ]
    )

    fully_paid_count = len(
        active_df[
            active_df["Total Payable Fee"] == 0
        ]
    )
    business_health = "Excellent"

    if collection_percentage < 80:
        business_health = "Good"

    if collection_percentage < 60:
        business_health = "Needs Attention"

    # ==========================
    # RETURN
    # ==========================

    return {

        # Learners
        "total_learners": total_learners,
        "active_learners": active_learners,
        "closed_learners": closed_learners,
        "fully_paid_count": fully_paid_count,
        "collection_due_count": collection_due_count,

        # Sales
        "total_sales": total_sales,
        "active_sales": active_sales,
        "closed_sales": closed_sales,

        # Payment Type
        "emi_revenue": emi_revenue,
        "emi_learners": emi_learners,
        "one_shot_revenue": one_shot_revenue,
        "manual_emi_learners": manual_emi_learners,
        "credit_card_learners": credit_card_learners,
        "one_shot_learners": one_shot_learners,
        

        # Collection
        "amount_collected": amount_collected,
        "pending_amount": pending_amount,
        "payable_fee": payable_fee,

        # Monthly
        "june_collection": june_collection,
        "july_collection": july_collection,
        "expected_june": expected_june,
        "expected_july": expected_july,

        # Exited
        "june_exited": june_exited,
        "july_exited": july_exited,

        # Percentage
        "collection_percentage": collection_percentage,

        # Business
        "average_revenue": average_revenue,
        "average_pending": average_pending,

        # Executive Insights
        "insights": insights,

        # Smart Alerts
        "high_pending_count": high_pending_count,
        "zero_collection_count": zero_collection_count,
        "collection_due_count": collection_due_count,
        "business_health": business_health,
        "inactive_learners": inactive_learners,
    }
