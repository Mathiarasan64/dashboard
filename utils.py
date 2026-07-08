import pandas as pd


# ---------------- Currency Formatter ----------------

def format_currency(amount):
    """
    Convert number to Indian Rupee format.
    Example:
    150000 -> ₹ 150,000
    """

    try:
        return f"₹ {amount:,.0f}"
    except:
        return "₹ 0"


# ---------------- Percentage ----------------

def calculate_percentage(value, total):

    if total == 0:
        return 0

    return round((value / total) * 100, 1)


# ---------------- Progress ----------------

def calculate_progress(value, total):

    if total == 0:
        return 0

    progress = value / total

    return min(progress, 1)


# ---------------- CSV Download ----------------

def dataframe_to_csv(df):

    return df.to_csv(index=False).encode("utf-8")


# ---------------- Top Pending Students ----------------

def get_top_pending(df, count=10):

    return (
        df.sort_values(
            by="Pending",
            ascending=False
        )
        .head(count)
    )


# ---------------- Search ----------------

def search_student(df, keyword):

    if keyword == "":
        return df

    return df[
        df["Student Name"]
        .astype(str)
        .str.contains(
            keyword,
            case=False,
            na=False
        )
    ]
