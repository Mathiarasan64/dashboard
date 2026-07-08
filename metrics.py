import pandas as pd


def calculate_metrics(df):
    """
    Calculate all dashboard KPI metrics.
    """

    # ---------------- Learner Status ----------------

    learner_status = df["Learner Status"].astype(str).str.strip().str.lower()

    active_df = df[learner_status != "closed"]
    closed_df = df[learner_status == "closed"]

    total_learners = len(df)
    active_learners = len(active_df)
    closed_learners = len(closed_df)

    # ---------------- Sales ----------------

    total_sales = df["Total price"].sum()
    active_sales = active_df["Total price"].sum()
    closed_sales = closed_df["Total price"].sum()

    # ---------------- Payment Type ----------------

    payment_type = active_df["Payment Type"].astype(str).str.strip().str.lower()

    one_shot_df = active_df[payment_type == "one shot"]
    emi_df = active_df[payment_type != "one shot"]

    one_shot_sales = one_shot_df["Total price"].sum()
    emi_sales = emi_df["Total price"].sum()

    one_shot_count = len(one_shot_df)
    emi_count = len(emi_df)

    # ---------------- Collections ----------------

    amount_collected = df["Advance / amount paid"].sum()
    pending_amount = df["Pending"].sum()

    # ---------------- Monthly ----------------

    june_collection = df["June"].sum()
    july_collection = df["July"].sum()

    expected_june = df["Expected EMI Collection for June"].sum()
    expected_july = df["Expected EMI Collection for July"].sum()

    total_payable_fee = df["Total Payable Fee"].sum()

    # ---------------- Exited ----------------

    june_exited = 0
    july_exited = 0

    if "Payment Status (June)" in df.columns:
        june_exited = (
            df["Payment Status (June)"]
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

    # ---------------- Collection Percentage ----------------

    if active_sales > 0:
        collection_percentage = (amount_collected / active_sales) * 100
    else:
        collection_percentage = 0

    return {
        "total_learners": total_learners,
        "active_learners": active_learners,
        "closed_learners": closed_learners,

        "total_sales": total_sales,
        "active_sales": active_sales,
        "closed_sales": closed_sales,

        "one_shot_sales": one_shot_sales,
        "emi_sales": emi_sales,

        "one_shot_count": one_shot_count,
        "emi_count": emi_count,

        "amount_collected": amount_collected,
        "pending_amount": pending_amount,

        "june_collection": june_collection,
        "july_collection": july_collection,

        "expected_june": expected_june,
        "expected_july": expected_july,

        "total_payable_fee": total_payable_fee,

        "june_exited": june_exited,
        "july_exited": july_exited,

        "collection_percentage": collection_percentage
    }
