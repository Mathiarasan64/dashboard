import pandas as pd

URL = "https://sheet.zohopublic.in/sheet/published/sfoej993e5907c3fb4e70a21047d22db57a9c?download=xlsx"

def load_data():
    try:
        df = pd.read_excel(URL)
        return df
    except Exception as e:
        return pd.DataFrame({"Error": [str(e)]})
