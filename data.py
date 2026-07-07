import pandas as pd

URL = "https://sheet.zohopublic.in/sheet/published/sfoej993e5907c3fb4e70a21047d22db57a9c"

def load_data():
    try:
        tables = pd.read_html(URL)
        return tables[0]
    except Exception as e:
        return pd.DataFrame({"Error": [str(e)]})
