import pandas as pd

URL = "https://sheet.zohopublic.in/sheet/published/sfoej993e5907c3fb4e70a21047d22db57a9c?download=csv&sheetname=Sheet1"

def load_data():
    df = pd.read_csv(URL)

    money_cols = [
        "Total price",
        "Advance / amount paid",
        "Pending",
        "June",
        "July",
        "Total Payable Fee",
        "Expected EMI Collection for June",
        "Expected EMI Collection for July"
    ]

    for col in money_cols:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", "", regex=False)
                .replace("-", "0")
            )
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df
