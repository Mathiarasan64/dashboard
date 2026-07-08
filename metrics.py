import pandas as pd


def calculate_metrics(df):

    # ---------------- Learners ----------------

    total_learners = len(df)

    closed_df = df[
        df["Learner Status"]
        .astype(str)
        .str.strip()
        .str.lower() == "closed"
    ]

    active_df = df[
        df["Learner Status"]
        .astype(str)
        .str.strip()
        .str.lower() != "closed"
    ]

    closed_learners = len(closed_df)

    active_learners = len(active_df)

    # ---------------- Sales ----------------

    total_sales = df["Total price"].sum()

    closed_sales = closed_df["Total price"].sum()

    active_sales = active_df["Total price"].sum()

    # ---------------- Payment Type ----------------

    one_shot_df = active_df[
        active_df["Payment Type"]
        .astype(str)
        .str.strip()
        .str.lower() == "one shot"
    ]

    emi_df = active_df[
        active_df["Payment Type"]
        .astype(str)
        .str.strip()
        .str.lower() != "one shot"
    ]

    one_shot_sales = one_shot_df["Total price"].sum()

    emi_sales = emi_df["Total price"].sum()

    # ---------------- Collections ----------------

    amount_collected = df["Advance / amount paid"].sum()

    pending_amount = df["Pending"].sum()

    # ---------------- Monthly ----------------

    june_collection = df["June"].sum()

    july_collection = df["July"].sum()

    expected_june = df["Expected EMI Collection for June"].sum()

    expected_july = df["Expected EMI Collection for July"].sum()

    # ---------------- Exited ----------------

    june_exited = len(
        df[
            df["Payment Status June"]
            .astype(str)
            .str.lower()
            == "exited"
        ]
    )
print(df.columns.tolist())

    july_exited = len(
        df[
            df["Payment Status July"]
            .astype(str)
            .str.lower()
            == "exited"
        ]
    )

    # ---------------- Collection % ----------------

    collection_percentage = (
        amount_collected / active_sales * 100
        if active_sales > 0
        else 0
    )

    return {

        "total_learners": total_learners,

        "active_learners": active_learners,

        "closed_learners": closed_learners,

        "total_sales": total_sales,

        "active_sales": active_sales,

        "closed_sales": closed_sales,

        "one_shot_sales": one_shot_sales,

        "emi_sales": emi_sales,

        "amount_collected": amount_collected,

        "pending_amount": pending_amount,

        "collection_percentage": collection_percentage,

        "june_collection": june_collection,

        "july_collection": july_collection,

        "expected_june": expected_june,

        "expected_july": expected_july,

        "june_exited": june_exited,

        "july_exited": july_exited,
    }
