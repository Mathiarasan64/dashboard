import pandas as pd

URL = "https://sheet.zohopublic.in/sheet/published/sfoej993e5907c3fb4e70a21047d22db57a9c?download=csv&sheetname=Sheet1"

def load_data():
    # Read CSV
    df = pd.read_csv(URL)

    # Remove completely empty rows
    df = df.dropna(how="all")

    # Remove first row if it contains 'None'
    if len(df) > 0:
        first_row = df.iloc[0].astype(str).str.lower()
        if first_row.str.contains("none").any():
            df = df.iloc[1:]

    # Clean column names
    df.columns = (
        df.columns
        .str.strip()
        .str.replace("\n", " ", regex=False)
    )

    # Rename columns
    df.rename(columns={
        "Students Name": "Student Name",
        "Payment type": "Payment Type",
        "Payment Status (June)": "Payment Status June",
        "Payment Status (July)": "Payment Status July"
    }, inplace=True)

    # Remove rows where Student Name is empty
    if "Student Name" in df.columns:
        df = df[df["Student Name"].notna()]
        df = df[df["Student Name"].astype(str).str.strip() != ""]

    # Convert currency columns
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
                .replace("", "0")
            )
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # Keep S.No column
    if "S.No" in df.columns:
        df["S.No"] = pd.to_numeric(df["S.No"], errors="coerce")
        df = df[df["S.No"].notna()]
        df["S.No"] = df["S.No"].astype(int)

    # Reset DataFrame index
    df.reset_index(drop=True, inplace=True)

    return df
