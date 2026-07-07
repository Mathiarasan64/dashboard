import pandas as pd

URL = "https://sheet.zohopublic.in/sheet/published/sfoej993e5907c3fb4e70a21047d22db57a9c?download=csv&sheetname=Sheet1"


def load_data():

    df = pd.read_csv(URL)

    # Remove empty rows
    df = df.dropna(how="all")

    # Clean column names
    df.columns = (
        df.columns
        .str.strip()
        .str.replace("\n", " ", regex=False)
    )

    # Standardize column names
    df.rename(columns={
        "Students Name": "Student Name",
        "Payment type": "Payment Type",
        "Payment Status (June)": "Payment Status June",
        "Payment Status (July)": "Payment Status July",
    }, inplace=True)

    # Remove rows with empty student names
    if "Student Name" in df.columns:
        df = df[
            df["Student Name"].notna()
        ]

    # Currency Columns
    money_columns = [
        "Total price",
        "Advance / amount paid",
        "Pending",
        "June",
        "July",
        "Total Payable Fee",
        "Expected EMI Collection for June",
        "Expected EMI Collection for July"
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

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            ).fillna(0)

    # S.No
    if "S.No" in df.columns:

        df["S.No"] = (
            pd.to_numeric(
                df["S.No"],
                errors="coerce"
            )
            .fillna(0)
            .astype(int)
        )

    return df
