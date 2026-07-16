def load_css():
    return """
<style>

/* ==========================================
   PREMIUM HEADER
========================================== */

.header-card{

background:#FFFFFF;

padding:30px;

border-radius:24px;

box-shadow:0px 8px 30px rgba(15,23,42,.08);

border:1px solid #E2E8F0;

margin-bottom:30px;

}

.header-divider{

border-left:2px solid #E5E7EB;

height:180px;

margin:auto;

}

.live-card{

background:#ECFDF5;

padding:18px;

border-radius:18px;

text-align:center;

border:1px solid #D1FAE5;

}

.time-card{

background:white;

padding:18px;

border-radius:18px;

border:1px solid #E2E8F0;

box-shadow:0px 2px 10px rgba(0,0,0,.05);

margin-top:15px;

text-align:center;

}
<style>

/* =========================
   PREMIUM KPI CARD
========================= */

.kpi-card{
    background:#FFFFFF;
    border-radius:18px;
    padding:22px;
    box-shadow:0 8px 24px rgba(15,23,42,.08);
    border-top:5px solid #2563EB;
    transition:all .25s ease;
    margin-bottom:12px;
}

.kpi-card:hover{
    transform:translateY(-4px);
    box-shadow:0 16px 35px rgba(37,99,235,.18);
}

.kpi-title{
    color:#64748B;
    font-size:15px;
    font-weight:600;
}

.kpi-value{
    color:#0F172A;
    font-size:34px;
    font-weight:700;
    margin-top:8px;
}

.kpi-sub{
    color:#16A34A;
    font-size:14px;
    margin-top:10px;
}

/* ========================================
   IMPORT FONT
======================================== */

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* ========================================
   APP
======================================== */

.stApp{
    background:#F4F7FC;
}

/* ========================================
   REMOVE STREAMLIT HEADER
======================================== */

header{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

/* ========================================
   SIDEBAR
======================================== */

section[data-testid="stSidebar"]{
    background:#0F172A;
}

section[data-testid="stSidebar"] *{
    color:white !important;
}

/* ========================================
   SECTION TITLE
======================================== */

.section-header{

    font-size:24px;

    font-weight:700;

    color:#0F172A;

    margin-top:25px;

    margin-bottom:15px;

    border-left:6px solid #2563EB;

    padding-left:12px;

}

/* ========================================
   METRIC CARD
======================================== */

[data-testid="stMetric"]{
    background:#FFFFFF;
    border:1px solid #E2E8F0;
    border-radius:12px;
    padding:12px;
    min-height:95px;
    box-shadow:0 2px 8px rgba(0,0,0,.05);
}

[data-testid="stMetricLabel"]{
    color:#64748B;
    font-size:13px;
    font-weight:600;
}

[data-testid="stMetricValue"]{
    color:#0F172A;
    font-size:24px;
    font-weight:700;
}

[data-testid="stMetricDelta"]{
    font-size:12px;
    font-weight:600;
}

/* ========================================
   BUTTONS
======================================== */

.stButton>button{

    width:100%;

    border-radius:12px;

    border:none;

    background:#2563EB;

    color:white;

    height:48px;

    font-weight:600;

}

.stButton>button:hover{

    background:#1D4ED8;

}

/* ========================================
   DOWNLOAD BUTTON
======================================== */

.stDownloadButton>button{

    width:100%;

    border-radius:12px;

    border:none;

    background:#16A34A;

    color:white;

    height:48px;

    font-weight:600;

}

/* ========================================
   DATAFRAME
======================================== */

[data-testid="stDataFrame"]{

    border-radius:15px;

    border:1px solid #E5E7EB;

}

/* ========================================
   INFO / SUCCESS
======================================== */

.stAlert{

    border-radius:15px;

}

</style>
"""