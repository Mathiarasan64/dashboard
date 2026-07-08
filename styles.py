def load_css():
    return """
<style>

/* ---------------- Main Background ---------------- */

.stApp{
    background-color:#F8FAFC;
}

/* ---------------- KPI Cards ---------------- */

[data-testid="stMetric"]{
    background:white;
    border-radius:15px;
    padding:18px;
    border:1px solid #E5E7EB;
    box-shadow:0px 4px 12px rgba(0,0,0,.08);
}

/* ---------------- Dashboard Title ---------------- */

h1{
    color:#1E3A8A;
    font-weight:700;
}

/* ---------------- Sidebar ---------------- */

section[data-testid="stSidebar"]{
    background:#FFFFFF;
    border-right:1px solid #E5E7EB;
}

/* ---------------- Buttons ---------------- */

.stButton>button{
    border-radius:10px;
    background:#2563EB;
    color:white;
    border:none;
    font-weight:600;
}

.stButton>button:hover{
    background:#1D4ED8;
}

/* ---------------- Download Button ---------------- */

.stDownloadButton>button{
    border-radius:10px;
    background:#16A34A;
    color:white;
    border:none;
}

/* ---------------- Dataframe ---------------- */

[data-testid="stDataFrame"]{
    border-radius:12px;
    border:1px solid #E5E7EB;
}

</style>
"""
