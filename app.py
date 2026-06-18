import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json, os, pathlib

# ── PERSISTENT FILE STORAGE ───────────────────────────────────────────────────
_DATA_FILE = pathlib.Path(__file__).parent / "cfo_data.json"

def _save_state():
    """Write all editable tables to disk so edits survive session restarts."""
    payload = {
        "fc_sal":     st.session_state.get("fc_sal", []),
        "fc_sub":     st.session_state.get("fc_sub", []),
        "fc_corp26":  st.session_state.get("fc_corp26", []),
        "fc_courses": st.session_state.get("fc_courses", []),
    }
    try:
        _DATA_FILE.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass  # silently ignore write errors (e.g. read-only container)

def _load_saved():
    """Return the saved payload dict, or None if no file exists."""
    if _DATA_FILE.exists():
        try:
            return json.loads(_DATA_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return None

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Commschool · Digital CFO",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── AUTH ──────────────────────────────────────────────────────────────────────
PASSCODE = "commschool782@cfo"

def check_auth():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if not st.session_state.authenticated:
        st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        html, body, [class*='css'] { font-family: 'Inter', sans-serif !important; }
        [data-testid="stAppViewContainer"] { background: #ffffff !important; }
        [data-testid="stHeader"] { background: #ffffff !important; border-bottom: none !important; }
        .stTextInput > div > div {
            background: #f9fafb !important;
            border: 1.5px solid #e5e7eb !important;
            border-radius: 10px !important;
        }
        .stTextInput > div > div:focus-within {
            border-color: #30B143 !important;
            box-shadow: 0 0 0 3px rgba(48,177,67,0.12) !important;
        }
        .stTextInput input { color: #111827 !important; background: transparent !important; }
        .stTextInput input::placeholder { color: #9ca3af !important; }
        .stTextInput label { color: #6b7280 !important; font-size:11px !important; font-weight:600 !important; letter-spacing:1px !important; text-transform:uppercase !important; }
        .stButton > button {
            background: #30B143 !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 10px !important;
            font-weight: 700 !important;
            font-size: 15px !important;
            padding: 0.65rem 1rem !important;
            width: 100% !important;
        }
        .stButton > button:hover { background: #1e8a30 !important; }
        .stAlert { background: #fef2f2 !important; border: 1px solid #fecaca !important; border-radius: 8px !important; color: #b91c1c !important; }
        </style>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div style="margin-top:10vh">', unsafe_allow_html=True)
            st.markdown('''<div style="text-align:center;margin-bottom:2.5rem">
                <p style="font-size:10px;font-weight:700;letter-spacing:2.5px;color:#9ca3af;text-transform:uppercase;margin-bottom:12px">COMMSCHOOL</p>
                <h1 style="font-size:34px;font-weight:700;color:#111827;margin:0;font-family:Inter,sans-serif">
                    Digital <span style="color:#30B143">CFO</span>
                </h1>
                <p style="font-size:13px;color:#6b7280;margin-top:10px">Internal financial dashboard</p>
            </div>''', unsafe_allow_html=True)
            pwd = st.text_input("Access Code", type="password", placeholder="Enter passcode")
            st.markdown("<div style='margin-top:8px'>", unsafe_allow_html=True)
            if st.button("Enter →", use_container_width=True, type="primary"):
                if pwd == PASSCODE:
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Incorrect code. Try again.")
        st.stop()

check_auth()

# ── CUSTOM CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
html, body, [class*='css'] { font-family: 'Inter', sans-serif !important; }

[data-testid="stAppViewContainer"] { background: #f9fafb; }
[data-testid="stHeader"] { background: #f9fafb !important; border-bottom: 1px solid #e5e7eb !important; }
[data-testid="stSidebar"] { background: #ffffff; border-right: 1px solid #e5e7eb; }
[data-testid="stSidebar"] * { color: #111827 !important; }
/* Sidebar flex layout so footer sticks to bottom */
[data-testid="stSidebar"] > div:first-child { display: flex !important; flex-direction: column !important; min-height: 100vh !important; }
.sidebar-spacer { flex: 1 !important; min-height: 24px !important; }
h1,h2,h3,h4 { font-family: "Space Grotesk", sans-serif !important; color: #111827 !important; }
p, li { color: #374151 !important; }
.stMarkdown p { color: #6b7280 !important; }

/* Sidebar nav buttons */
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    color: #6b7280 !important;
    border: none !important;
    border-left: 3px solid transparent !important;
    border-radius: 0 8px 8px 0 !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    text-align: left !important;
    padding: 10px 16px !important;
    margin: 1px 0 !important;
    width: 100% !important;
    transition: all 0.15s !important;
    box-shadow: none !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(48,177,67,0.08) !important;
    color: #111827 !important;
    border-left-color: rgba(48,177,67,0.4) !important;
}
[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: rgba(48,177,67,0.1) !important;
    color: #111827 !important;
    border-left: 3px solid #30B143 !important;
    font-weight: 700 !important;
}
/* Lock button */
[data-testid="stSidebar"] .stButton:last-of-type > button {
    color: #9ca3af !important;
    font-size: 12px !important;
    margin-top: 8px !important;
    border: 1px solid #e5e7eb !important;
    border-radius: 6px !important;
}
[data-testid="stSidebar"] .stButton:last-of-type > button:hover {
    color: #ef4444 !important;
    border-color: rgba(239,68,68,0.4) !important;
    background: rgba(239,68,68,0.06) !important;
}

/* Main content buttons (month filters) */
.main .stButton > button {
    background: #ffffff !important;
    color: #6b7280 !important;
    border: 1px solid #e5e7eb !important;
    border-radius: 6px !important;
    font-size: 11px !important;
    font-weight: 500 !important;
    padding: 4px 8px !important;
}
.main .stButton > button:hover {
    border-color: #30B143 !important;
    color: #111827 !important;
}
.main .stButton > button[kind="primary"] {
    background: rgba(48,177,67,0.12) !important;
    color: #111827 !important;
    border-color: #30B143 !important;
    font-weight: 700 !important;
}

/* KPI cards */
.kpi-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 20px 22px;
    margin-bottom: 4px;
}
.kpi-label { font-size:10px; font-weight:700; letter-spacing:1.5px; text-transform:uppercase; color:#9ca3af; margin-bottom:8px; }
.kpi-value { font-family:"Space Grotesk",sans-serif; font-size:24px; font-weight:700; margin-bottom:4px; }
.kpi-sub { font-size:11px; color:#9ca3af; }
.kpi-pos { color: #16a34a; }
.kpi-neg { color: #ef4444; }
.kpi-warn { color: #d97706; }

/* Insight cards */
.insight-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 10px;
    display: flex;
    gap: 12px;
    align-items: flex-start;
}

/* Tables */
.stDataFrame { border: 1px solid #e5e7eb !important; border-radius: 10px !important; }
[data-testid="stDataFrame"] * { color: #374151 !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { background: transparent !important; border-bottom: 1px solid #e5e7eb !important; }
.stTabs [data-baseweb="tab"] { background: transparent !important; color: #6b7280 !important; font-size:13px !important; font-weight:500 !important; }
.stTabs [data-baseweb="tab"]:hover { color: #111827 !important; }
.stTabs [aria-selected="true"] { color: #30B143 !important; border-bottom: 2px solid #30B143 !important; }

/* Inputs */
.stTextInput > div > div { background: #f9fafb !important; border: 1px solid #e5e7eb !important; border-radius: 8px !important; }
.stTextInput input { color: #111827 !important; }
.stTextInput label { color: #9ca3af !important; font-size:11px !important; font-weight:600 !important; letter-spacing:1px !important; text-transform:uppercase !important; }
[data-baseweb="select"] { background: #f9fafb !important; border-color: #e5e7eb !important; border-radius: 8px !important; }
[data-baseweb="select"] * { color: #374151 !important; }

/* Alert */
.stAlert { background: rgba(239,68,68,0.05) !important; border: 1px solid rgba(239,68,68,0.2) !important; border-radius: 8px !important; }

/* Divider */
hr { border-color: #e5e7eb !important; margin: 1.5rem 0 !important; }
.block-container { padding-top: 2rem !important; max-width: 1200px; }

/* Margin badges */
.badge-pos  { background: rgba(22,163,74,0.1); color: #16a34a; padding: 2px 8px; border-radius: 5px; font-size: 11px; font-weight: 700; }
.badge-warn { background: rgba(217,119,6,0.1); color: #d97706; padding: 2px 8px; border-radius: 5px; font-size: 11px; font-weight: 700; }
.badge-neg  { background: rgba(239,68,68,0.1); color: #ef4444; padding: 2px 8px; border-radius: 5px; font-size: 11px; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# ── DATA ──────────────────────────────────────────────────────────────────────
MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

SALARIES = [
    {"name": "CEO",                          "m": [8929,8929,8929,8929,8929,8929,8929,8929,8929,8929,8929,8929]},
    {"name": "Programs Lead (Tamri)",        "m": [3189,3189,3189,3189,1006,893,3571,3571,3571,3571,3571,3571]},
    {"name": "Programs Coord. (Masho)",      "m": [1276,1276,1276,1276,1276,1276,1276,1276,1531,1531,1531,1531]},
    {"name": "Head of Growth (Mariam)",      "m": [2551,3571,3571,3571,3571,3571,3571,3571,3571,3571,3571,3571]},
    {"name": "Growth Manager 1",             "m": [1020,1020,1276,0,0,0,0,0,0,0,0,1276]},
    {"name": "Growth Manager 2 (Mariam K)", "m": [1276,1276,1276,1276,1276,1276,1276,1276,1531,1531,1531,1531]},
    {"name": "Marketing Manager",            "m": [2551,2551,2551,1276,0,0,0,0,0,0,0,0]},
    {"name": "Marketing Specialist (Nini)", "m": [1531,1531,1531,1913,1913,1913,1913,1913,1913,1913,1913,1913]},
    {"name": "Video Editor",                 "m": [0,0,0,1000,1000,1000,1000,1000,1000,1000,1000,1000]},
]

SUBS = [
    {"name": "Office Rent",        "m": [2500]*12},
    {"name": "Financial Service",  "m": [885]*12},
    {"name": "HubSpot",            "m": [1800]*12},
    {"name": "Google G Suite",     "m": [230]*12},
    {"name": "DigitalOcean",       "m": [287,287,287,287,287,287,287,287,383,383,383,383]},
    {"name": "Bank & SMS Fees",    "m": [7,37,7,7,7,37,7,7,37,7,7,37]},
    {"name": "WARC (ann./12)",     "m": [909]*12},
    {"name": "Canva (ann.)",       "m": [33]*12},
]

COURSES = [
    {"name":"Graphic Design",       "month":"Jan","students":3, "price":1250,"lecturer":2800,"inst":0,  "zoom":40,"mkt":1111,"mat":135, "rev":3750.00},
    {"name":"Marketing Management", "month":"Feb","students":4, "price":1500,"lecturer":3500,"inst":56, "zoom":40,"mkt":1021,"mat":180, "rev":5900.00},
    {"name":"Content Management",   "month":"Feb","students":0, "price":1400,"lecturer":0,   "inst":0,  "zoom":0, "mkt":1638,"mat":0,   "rev":0.00},
    {"name":"Data Analytics",       "month":"Feb","students":8, "price":1700,"lecturer":5357,"inst":60, "zoom":40,"mkt":1225,"mat":360, "rev":13600.00},
    {"name":"AI in Content",        "month":"Feb","students":8, "price":1400,"lecturer":3000,"inst":0,  "zoom":40,"mkt":1439,"mat":360, "rev":6720.00},
    {"name":"AI Agents",            "month":"Mar","students":9, "price":1400,"lecturer":2551,"inst":0,  "zoom":40,"mkt":1542,"mat":405, "rev":12040.00},
    {"name":"Data Science",         "month":"Mar","students":9, "price":2700,"lecturer":12117,"inst":0, "zoom":40,"mkt":1369,"mat":405, "rev":23760.00},
    {"name":"Growth Marketing",     "month":"Mar","students":17,"price":1500,"lecturer":4000,"inst":0,  "zoom":40,"mkt":569, "mat":765, "rev":18776.17},
    {"name":"IT BA",                "month":"Apr","students":8, "price":1500,"lecturer":3571,"inst":0,  "zoom":40,"mkt":1334,"mat":400, "rev":12000.00},
    {"name":"ADS",                  "month":"Apr","students":14,"price":1400,"lecturer":5357,"inst":0,  "zoom":40,"mkt":1385,"mat":630, "rev":19600.00},
    {"name":"AI SEO",               "month":"May","students":5, "price":1400,"lecturer":3061,"inst":0,  "zoom":40,"mkt":1651,"mat":265, "rev":7000.00},
    {"name":"AI Essentials",        "month":"May","students":5, "price":1050,"lecturer":2551,"inst":0,  "zoom":40,"mkt":1557,"mat":265, "rev":5250.00},
    {"name":"Data Analytics",       "month":"May","students":6, "price":1700,"lecturer":5357,"inst":0,  "zoom":40,"mkt":1210,"mat":310, "rev":10200.00},
    {"name":"GITA: IT PM",          "month":"May","students":7, "price":1000,"lecturer":3571,"inst":0,  "zoom":40,"mkt":262, "mat":355, "rev":7000.00},
    {"name":"GITA: Motion Design",  "month":"May","students":7, "price":1000,"lecturer":3000,"inst":0,  "zoom":40,"mkt":262, "mat":355, "rev":7000.00},
    {"name":"GITA: IT BA",          "month":"May","students":7, "price":1000,"lecturer":3571,"inst":0,  "zoom":40,"mkt":262, "mat":355, "rev":7000.00},
    {"name":"GITA: Python",         "month":"May","students":29,"price":2000,"lecturer":13500,"inst":0, "zoom":40,"mkt":262, "mat":1305,"rev":58000.00},
    {"name":"GITA: C#",             "month":"May","students":26,"price":2000,"lecturer":14000,"inst":0, "zoom":40,"mkt":262, "mat":1210,"rev":52000.00},
    {"name":"GITA: QA",             "month":"May","students":6, "price":1000,"lecturer":6300,"inst":0,  "zoom":40,"mkt":262, "mat":310, "rev":6000.00},
    {"name":"GITA: Graphic Design", "month":"May","students":13,"price":1000,"lecturer":3150,"inst":0,  "zoom":40,"mkt":262, "mat":635, "rev":13000.00},
    {"name":"GITA: UI/UX Design",   "month":"May","students":15,"price":1000,"lecturer":3571,"inst":0,  "zoom":40,"mkt":262, "mat":715, "rev":15000.00},
    {"name":"AI in Content",        "month":"Jun","students":12,"price":1400,"lecturer":2600,"inst":0,  "zoom":40,"mkt":1077,"mat":580, "rev":16800.00},
]

CORP26 = [
    {"name":"Georgian Railway – AI","type":"B2G","period":"Jan–Feb","revenue":6435,"cog":3215,"status":"Paid"},
    {"name":"Silk Development – AI","type":"B2B","period":"Jan–Apr","revenue":10932,"cog":2710,"status":"Paid"},
    {"name":"Roche Georgia – Agentic AI","type":"B2B","period":"Mar","revenue":6780,"cog":1566,"status":"Paid"},
    {"name":"Audit – SQL, Power BI","type":"B2G","period":"Mar–May","revenue":28400,"cog":10566,"status":"Pending"},
    {"name":"Metropol – AI Group 1","type":"B2B","period":"Apr–May","revenue":4322,"cog":1023,"status":"Paid"},
    {"name":"Metropol – AI Group 2","type":"B2B","period":"May","revenue":3814,"cog":1023,"status":"Paid"},
    {"name":"Metropol – AI Groups 3–4","type":"B2B","period":"Jun","revenue":7627,"cog":1824,"status":"Paid"},
    {"name":"Archi – AI for Designers","type":"B2B","period":"Jun","revenue":8051,"cog":2697,"status":"Paid"},
    {"name":"Helvetas – Branding Ideathon","type":"B2B","period":"Jun–Jul","revenue":25000,"cog":0,"status":"Active"},
]

CORP25 = [
    {"co":"Roche Georgia","pr":"AI Workshop","type":"B2B","period":"Feb","rev":5085,"cost":2175,"profit":2910,"margin":48.5},
    {"co":"Liberty Bank","pr":"IT BA","type":"B2B","period":"Apr–May","rev":14831,"cost":7220,"profit":7611,"margin":43.5},
    {"co":"GITA","pr":"Tech Weeks","type":"B2G","period":"Apr–May","rev":78814,"cost":46710,"profit":32104,"margin":34.5},
    {"co":"GWP","pr":"AI Essentials","type":"B2B","period":"Jul","rev":3814,"cost":1020,"profit":2793,"margin":62.1},
    {"co":"Czech Caritas","pr":"AI Essentials","type":"B2B","period":"Sep–Oct","rev":4500,"cost":1020,"profit":3480,"margin":77.3},
    {"co":"GITA","pr":"Startup Intern","type":"B2G","period":"Sep–Oct","rev":60169,"cost":41024,"profit":19145,"margin":26.8},
    {"co":"Silk Hospitality","pr":"AI Essentials ×2","type":"B2B","period":"Oct–Nov","rev":6780,"cost":2041,"profit":4739,"margin":59.2},
    {"co":"GITA","pr":"Innovation from Mountains","type":"B2G","period":"Oct–Nov","rev":32881,"cost":24778,"profit":8103,"margin":20.9},
    {"co":"GITA","pr":"Hackathon","type":"B2G","period":"Nov","rev":25678,"cost":19189,"profit":6489,"margin":21.4},
    {"co":"Gagua Clinic","pr":"AI Essentials","type":"B2B","period":"Nov","rev":3644,"cost":800,"profit":2844,"margin":66.1},
    {"co":"RS (Gov)","pr":"IT Management","type":"B2G","period":"Oct–Dec","rev":23771,"cost":7000,"profit":16771,"margin":59.8},
    {"co":"Silk Hospitality","pr":"AI Essentials ×2","type":"B2B","period":"Nov","rev":6780,"cost":1400,"profit":5380,"margin":67.2},
    {"co":"Silk Hospitality","pr":"AI Essentials ×1","type":"B2B","period":"Dec","rev":3390,"cost":600,"profit":2790,"margin":69.7},
]

PIPELINE = [
    {"name":"Startup Creation Course","type":"B2B","q":"Q3","rev":15000,"cog":5000,"stage":"Confirmed"},
    {"name":"Vibe Coding","type":"B2B","q":"Q3","rev":8000,"cog":2500,"stage":"Planning"},
    {"name":"GITA H2 Payment","type":"B2G","q":"Q3","rev":47883,"cog":0,"stage":"Confirmed"},
    {"name":"Content Marketing Course","type":"B2B","q":"Q3","rev":10000,"cog":3500,"stage":"Planning"},
]

# ── HELPERS ───────────────────────────────────────────────────────────────────
def fmt(n): return f"₾ {int(round(n)):,}"
def pct(n): return f"{float(n):.1f}%"
def cpnl(c):
    rv  = c.get("rev", c["students"] * c["price"])  # actual revenue incl. VAT
    rx  = rv / 1.18                                  # revenue excl. VAT
    cs  = c["lecturer"] + c.get("inst",0) + c["zoom"] + c["mkt"] + c["mat"]
    gp  = rv - cs
    net = rx - cs
    mg  = net / rx * 100 if rx > 0 else 0
    return {"rv": rv, "rx": rx, "cs": cs, "gp": gp, "net": net, "mg": mg}

def margin_badge(m):
    m = float(m)
    if m >= 50: return f'<span class="badge-pos">{pct(m)}</span>'
    if m >= 25: return f'<span class="badge-warn">{pct(m)}</span>'
    return f'<span class="badge-neg">{pct(m)}</span>'

def kpi(label, value, sub="", color="kpi-pos"):
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value {color}">{value}</div>
        <div class="kpi-sub">{sub}</div>
    </div>
    """, unsafe_allow_html=True)

def bar_chart(items, title=""):
    colors = [i["c"] for i in items]
    fig = go.Figure(go.Bar(
        x=[i["l"] for i in items],
        y=[i["v"] for i in items],
        marker_color=colors,
        text=[fmt(i["v"]) for i in items],
        textposition="outside",
        textfont=dict(size=10, color="#374151"),
    ))
    fig.update_layout(
        paper_bgcolor="#ffffff", plot_bgcolor="#f9fafb",
        font=dict(color="#374151", size=11),
        margin=dict(t=20, b=10, l=10, r=10),
        height=220,
        xaxis=dict(showgrid=False, tickfont=dict(size=10, color="#6b7280")),
        yaxis=dict(showgrid=True, gridcolor="#e5e7eb", tickfont=dict(size=10, color="#6b7280")),
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ── PERSISTENT STATE (init once, survives all page switches) ─────────────────
if "page" not in st.session_state:
    st.session_state.page = "📊 Dashboard"
if "fc_sal" not in st.session_state:
    _saved = _load_saved()
    st.session_state.fc_sal     = _saved["fc_sal"]     if _saved and _saved.get("fc_sal")     else [{"name": s["name"], "m": s["m"][:]} for s in SALARIES]
    st.session_state.fc_sub     = _saved["fc_sub"]     if _saved and _saved.get("fc_sub")     else [{"name": s["name"], "m": s["m"][:]} for s in SUBS]
    st.session_state.fc_corp26  = _saved["fc_corp26"]  if _saved and _saved.get("fc_corp26")  else [dict(p) for p in CORP26]
    st.session_state.fc_courses = _saved["fc_courses"] if _saved and _saved.get("fc_courses") else [dict(c) for c in COURSES]

nav_items = [
    ("📊", "Dashboard"),
    ("📌", "Fixed Costs"),
    ("🎓", "Courses P&L"),
    ("🏢", "Corporate Projects"),
]

with st.sidebar:
    # ── Logo + brand header ────────────────────────────────────────────────────
    st.markdown(f"""
    <div style="padding:0 16px 12px;margin-top:-8px">
        <img src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyMDAgMjAwIiB3aWR0aD0iNjQiIGhlaWdodD0iNjQiIHN0eWxlPSJmbGV4LXNocmluazowO2JvcmRlci1yYWRpdXM6MTJweDtkaXNwbGF5OmJsb2NrIj4KICA8cmVjdCB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgZmlsbD0iIzM5REIxMyIvPgogIDwhLS0gQ08gcm93IC0tPgogIDx0ZXh0IHg9IjEwMCIgeT0iODAiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZpbGw9IiMxYTFhMGEiCiAgICAgICAgZm9udC1mYW1pbHk9IkFyaWFsIEJsYWNrLEhlbHZldGljYSBOZXVlLHNhbnMtc2VyaWYiCiAgICAgICAgZm9udC1zaXplPSI4NiIgZm9udC13ZWlnaHQ9IjkwMCIgbGV0dGVyLXNwYWNpbmc9Ii0zIj5DTzwvdGV4dD4KICA8IS0tIE1NIHJvdyAtLT4KICA8dGV4dCB4PSIxMDAiIHk9IjE0OCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZmlsbD0iIzFhMWEwYSIKICAgICAgICBmb250LWZhbWlseT0iQXJpYWwgQmxhY2ssSGVsdmV0aWNhIE5ldWUsc2Fucy1zZXJpZiIKICAgICAgICBmb250LXNpemU9Ijg2IiBmb250LXdlaWdodD0iOTAwIiBsZXR0ZXItc3BhY2luZz0iLTMiPk1NPC90ZXh0PgogIDwhLS0gU0NIT09MIHJvdyAtLT4KICA8dGV4dCB4PSIxMDAiIHk9IjE3OCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZmlsbD0iIzFhMWEwYSIKICAgICAgICBmb250LWZhbWlseT0iQXJpYWwgQmxhY2ssSGVsdmV0aWNhIE5ldWUsc2Fucy1zZXJpZiIKICAgICAgICBmb250LXNpemU9IjIyIiBmb250LXdlaWdodD0iNzAwIiBsZXR0ZXItc3BhY2luZz0iNyI+U0NIT09MPC90ZXh0Pgo8L3N2Zz4="
             width="80" style="border-radius:14px;display:block;margin-bottom:10px"/>
        <h2 style="font-size:19px;font-weight:700;color:#111827;margin:0;font-family:Space Grotesk,sans-serif;line-height:1.15">Digital <span style="color:#30B143">CFO</span></h2>
        <p style="font-size:10px;color:#9ca3af;margin:1px 0 0;letter-spacing:0.5px">Internal finance</p>
    </div>
    <hr style="border-color:#e5e7eb;margin:0 0 8px">
    """, unsafe_allow_html=True)

    # ── Nav buttons ───────────────────────────────────────────────────────────
    for icon, label in nav_items:
        full = f"{icon} {label}"
        active = st.session_state.page == full
        if st.button(f"{icon}  {label}", key=f"nav_{label}", use_container_width=True,
                     type="primary" if active else "secondary"):
            st.session_state.page = full
            st.rerun()

    # ── Spacer pushes footer to bottom ────────────────────────────────────────
    st.markdown('<div class="sidebar-spacer"></div>', unsafe_allow_html=True)

    # ── Footer ────────────────────────────────────────────────────────────────
    st.markdown('<hr style="border-color:#e5e7eb;margin:0 0 6px">', unsafe_allow_html=True)
    st.markdown('<p style="font-size:10px;color:#9ca3af;padding:0 4px;margin-bottom:8px">₾ GEL · 2026 · H1 actuals</p>', unsafe_allow_html=True)
    if st.button("🔒 Lock", key="lock_btn", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

page = st.session_state.page

# ── DASHBOARD ─────────────────────────────────────────────────────────────────
if page == "📊 Dashboard":
    st.markdown("## Financial Overview")
    st.markdown('<p style="color:#30B143;margin-top:-12px">2026 H1 · Courses + Corporate actuals</p>', unsafe_allow_html=True)

    mi = MONTHS.index("Jun")  # default to Jun for H1 snapshot
    sal_m = sum(s["m"][mi] for s in st.session_state.fc_sal)
    sub_m = sum(s["m"][mi] for s in st.session_state.fc_sub)
    sal_a = sum(sum(s["m"]) for s in st.session_state.fc_sal)
    sub_a = sum(sum(s["m"]) for s in st.session_state.fc_sub)

    c_data = [cpnl(c) for c in st.session_state.fc_courses]
    c_rev = sum(d["rv"] for d in c_data)
    c_net = sum(d["net"] for d in c_data)
    c_rx  = sum(d["rx"] for d in c_data)
    c_cs  = sum(d["cs"] for d in c_data)

    crp_r = sum(p["revenue"] for p in st.session_state.fc_corp26)
    crp_c = sum(p["cog"] for p in st.session_state.fc_corp26)
    crp_p = crp_r - crp_c

    tot_r = c_rev + crp_r

    col1, col2, col3, col4 = st.columns(4)
    with col1: kpi("H1 Total Revenue", fmt(tot_r), f"Courses {fmt(c_rev)} · Corp {fmt(crp_r)}", "kpi-pos")
    with col2: kpi("Course Net Profit", fmt(c_net), f"Margin {pct(c_net/c_rx*100 if c_rx else 0)} · excl. VAT", "kpi-pos" if c_net >= 0 else "kpi-neg")
    with col3: kpi("Corporate Net Profit", fmt(crp_p), f"Margin {pct(crp_p/crp_r*100 if crp_r else 0)}", "kpi-pos")
    with col4: kpi("Fixed Costs · Jun", fmt(sal_m + sub_m), f"{fmt(sal_a + sub_a)} full-year budget", "kpi-warn")

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    gita_r = sum(cpnl(c)["rv"] for c in st.session_state.fc_courses if c["name"].startswith("GITA"))
    own_r  = c_rev - gita_r
    b2b_r  = sum(p["revenue"] for p in st.session_state.fc_corp26 if p["type"] == "B2B")
    b2g_r  = sum(p["revenue"] for p in st.session_state.fc_corp26 if p["type"] == "B2G")
    lec_t  = sum(c["lecturer"] for c in st.session_state.fc_courses)
    mkt_t  = sum(c["mkt"] for c in st.session_state.fc_courses)

    with col1:
        st.markdown('<div class="kpi-card"><div class="kpi-label">📈 Revenue Mix</div></div>', unsafe_allow_html=True)
        bar_chart([
            {"l":"Own Courses","v":own_r,"c":"#86efac"},
            {"l":"GITA Courses","v":gita_r,"c":"#22c55e"},
            {"l":"Corp B2B","v":b2b_r,"c":"#16a34a"},
            {"l":"Corp B2G","v":b2g_r,"c":"#4ade80"},
        ])

    with col2:
        st.markdown('<div class="kpi-card"><div class="kpi-label">💸 Cost Structure</div></div>', unsafe_allow_html=True)
        bar_chart([
            {"l":"Salaries","v":sal_a,"c":"#ef4444"},
            {"l":"Admin+Subs","v":sub_a,"c":"#60a5fa"},
            {"l":"Lecturer Fees","v":lec_t,"c":"#a78bfa"},
            {"l":"Advertising","v":mkt_t,"c":"#f59e0b"},
            {"l":"Corp COG","v":crp_c,"c":"#34d399"},
        ])

    st.markdown("### 💡 CFO Insights")
    top_c  = max([c for c in st.session_state.fc_courses if cpnl(c)["rx"] > 0], key=lambda c: cpnl(c)["mg"])
    wrst_c = min([c for c in st.session_state.fc_courses if cpnl(c)["rx"] > 0], key=lambda c: cpnl(c)["mg"])
    gita_dep = (gita_r + b2g_r) / tot_r * 100 if tot_r else 0

    for icon, text in [
        ("🏆", f"**Best margin:** {top_c['name']} ({top_c['month']}) at **{pct(cpnl(top_c)['mg'])}**. Low ad spend + strong cohort size."),
        ("⚠️", f"**GITA + B2G = {pct(gita_dep)} of H1 revenue.** Audit (₾28,400) still pending — watch vs. {fmt(sal_m+sub_m)}/month fixed costs."),
        ("📉", f"**Lowest margin:** {wrst_c['name']} ({wrst_c['month']}). Set a minimum enrollment threshold before launching."),
        ("💼", f"**2026 salary budget: {fmt(sal_a)}.** CEO = {pct(8929*12/sal_a*100)} of total payroll. H1 fixed budget: {fmt((sal_a+sub_a)//2)}."),
    ]:
        st.markdown(f"""<div class="insight-card"><span style="font-size:18px">{icon}</span><span style="font-size:13px;color:#374151;line-height:1.6">{text}</span></div>""", unsafe_allow_html=True)


    # ── QUARTERLY P&L ─────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("## 📅 Quarterly P&L — Company Profitability")
    st.markdown('<p style="color:#30B143;margin-top:-12px">Income vs Expenses vs Net Profit by quarter</p>', unsafe_allow_html=True)

    # Q1: Jan+Feb+Mar
    q1_sal = sum(sum(s["m"][i] for i in range(3)) for s in st.session_state.fc_sal)
    q1_sub = sum(sum(s["m"][i] for i in range(3)) for s in st.session_state.fc_sub)
    q1_fixed = q1_sal + q1_sub
    q1_courses = [c for c in st.session_state.fc_courses if c["month"] in ["Jan","Feb","Mar"]]
    q1_course_rev = sum(cpnl(c)["rx"] for c in q1_courses)
    q1_course_costs = sum(cpnl(c)["cs"] for c in q1_courses)
    q1_corp_rev = sum(p["revenue"] for p in st.session_state.fc_corp26 if any(m in p["period"] for m in ["Jan","Feb","Mar"]))
    q1_corp_cog = sum(p["cog"] for p in st.session_state.fc_corp26 if any(m in p["period"] for m in ["Jan","Feb","Mar"]))
    q1_income = q1_course_rev + q1_corp_rev
    q1_expenses = q1_fixed + q1_course_costs + q1_corp_cog
    q1_net = q1_income - q1_expenses

    # Q2: Apr+May+Jun
    q2_sal = sum(sum(s["m"][i] for i in range(3,6)) for s in st.session_state.fc_sal)
    q2_sub = sum(sum(s["m"][i] for i in range(3,6)) for s in st.session_state.fc_sub)
    q2_fixed = q2_sal + q2_sub
    q2_courses = [c for c in st.session_state.fc_courses if c["month"] in ["Apr","May","Jun"]]
    q2_course_rev = sum(cpnl(c)["rx"] for c in q2_courses)
    q2_course_costs = sum(cpnl(c)["cs"] for c in q2_courses)
    q2_corp_rev = sum(p["revenue"] for p in st.session_state.fc_corp26 if any(m in p["period"] for m in ["Apr","May","Jun"]))
    q2_corp_cog = sum(p["cog"] for p in st.session_state.fc_corp26 if any(m in p["period"] for m in ["Apr","May","Jun"]))
    q2_income = q2_course_rev + q2_corp_rev
    q2_expenses = q2_fixed + q2_course_costs + q2_corp_cog
    q2_net = q2_income - q2_expenses

    # Q3: pipeline + estimated fixed (Jul+Aug+Sep)
    q3_sal = sum(sum(s["m"][i] for i in range(6,9)) for s in st.session_state.fc_sal)
    q3_sub = sum(sum(s["m"][i] for i in range(6,9)) for s in st.session_state.fc_sub)
    q3_fixed = q3_sal + q3_sub
    q3_pipe_rev = sum(p["rev"] for p in PIPELINE if p["q"] == "Q3")
    q3_pipe_cog = sum(p["cog"] for p in PIPELINE if p["q"] == "Q3")
    q3_income = q3_pipe_rev
    q3_expenses = q3_fixed + q3_pipe_cog
    q3_net = q3_income - q3_expenses

    # Q4: estimated fixed (Oct+Nov+Dec)
    q4_sal = sum(sum(s["m"][i] for i in range(9,12)) for s in st.session_state.fc_sal)
    q4_sub = sum(sum(s["m"][i] for i in range(9,12)) for s in st.session_state.fc_sub)
    q4_fixed = q4_sal + q4_sub
    q4_pipe_rev = sum(p["rev"] for p in PIPELINE if p["q"] == "Q4")
    q4_pipe_cog = sum(p["cog"] for p in PIPELINE if p["q"] == "Q4")
    q4_income = q4_pipe_rev
    q4_expenses = q4_fixed + q4_pipe_cog
    q4_net = q4_income - q4_expenses

    # KPI summary row
    col1,col2,col3,col4 = st.columns(4)
    quarters = [
        ("Q1 · Jan–Mar", q1_income, q1_expenses, q1_net, "Actuals"),
        ("Q2 · Apr–Jun", q2_income, q2_expenses, q2_net, "Actuals"),
        ("Q3 · Jul–Sep", q3_income, q3_expenses, q3_net, "Pipeline est."),
        ("Q4 · Oct–Dec", q4_income, q4_expenses, q4_net, "Pipeline est."),
    ]
    for col, (label, income, expenses, net, tag) in zip([col1,col2,col3,col4], quarters):
        with col:
            color = "kpi-pos" if net >= 0 else "kpi-neg"
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value {color}">{fmt(net)}</div>
                <div class="kpi-sub">↑ {fmt(income)} income · ↓ {fmt(expenses)} costs<br>
                <span style="font-size:10px;color:#16a34a">{tag}</span></div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Waterfall / grouped bar chart
    fig_q = go.Figure()
    qs = ["Q1\nActuals","Q2\nActuals","Q3\nPipeline","Q4\nPipeline"]
    incomes   = [q1_income,   q2_income,   q3_income,   q4_income]
    expenses_ = [q1_expenses, q2_expenses, q3_expenses, q4_expenses]
    nets      = [q1_net,      q2_net,      q3_net,      q4_net]

    fig_q.add_trace(go.Bar(name="Income", x=qs, y=incomes, marker_color="#16a34a",
        text=[fmt(v) for v in incomes], textposition="outside", textfont=dict(size=10,color="#16a34a")))
    fig_q.add_trace(go.Bar(name="Expenses", x=qs, y=expenses_, marker_color="#ef4444",
        text=[fmt(v) for v in expenses_], textposition="outside", textfont=dict(size=10,color="#ef4444")))
    fig_q.add_trace(go.Bar(name="Net Profit", x=qs, y=nets, marker_color="#3b82f6",
        text=[fmt(v) for v in nets], textposition="outside", textfont=dict(size=10,color="#3b82f6")))

    fig_q.update_layout(
        barmode="group",
        paper_bgcolor="#ffffff", plot_bgcolor="#f9fafb",
        font=dict(color="#374151", size=11),
        margin=dict(t=30, b=20, l=10, r=10),
        height=320,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                    font=dict(color="#374151"), bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(showgrid=False, tickfont=dict(size=11, color="#374151")),
        yaxis=dict(showgrid=True, gridcolor="#e5e7eb", tickfont=dict(size=10, color="#6b7280")),
    )
    st.plotly_chart(fig_q, use_container_width=True, config={"displayModeBar": False})

    # Detailed breakdown table
    st.markdown("### 📊 Quarterly Breakdown Detail")
    q_table = pd.DataFrame([
        {"Quarter": "Q1 (Jan–Mar)", "Status": "✅ Actuals",
         "Course Income ₾": int(q1_course_rev), "Corp Income ₾": int(q1_corp_rev), "Total Income ₾": int(q1_income),
         "Fixed Costs ₾": int(q1_fixed), "Variable Costs ₾": int(q1_course_costs+q1_corp_cog), "Total Expenses ₾": int(q1_expenses),
         "Net Profit ₾": int(q1_net), "Margin %": round(q1_net/q1_income*100,1) if q1_income else 0},
        {"Quarter": "Q2 (Apr–Jun)", "Status": "✅ Actuals",
         "Course Income ₾": int(q2_course_rev), "Corp Income ₾": int(q2_corp_rev), "Total Income ₾": int(q2_income),
         "Fixed Costs ₾": int(q2_fixed), "Variable Costs ₾": int(q2_course_costs+q2_corp_cog), "Total Expenses ₾": int(q2_expenses),
         "Net Profit ₾": int(q2_net), "Margin %": round(q2_net/q2_income*100,1) if q2_income else 0},
        {"Quarter": "Q3 (Jul–Sep)", "Status": "🔮 Pipeline",
         "Course Income ₾": 0, "Corp Income ₾": int(q3_pipe_rev), "Total Income ₾": int(q3_income),
         "Fixed Costs ₾": int(q3_fixed), "Variable Costs ₾": int(q3_pipe_cog), "Total Expenses ₾": int(q3_expenses),
         "Net Profit ₾": int(q3_net), "Margin %": round(q3_net/q3_income*100,1) if q3_income else 0},
        {"Quarter": "Q4 (Oct–Dec)", "Status": "🔮 Pipeline",
         "Course Income ₾": 0, "Corp Income ₾": int(q4_pipe_rev), "Total Income ₾": int(q4_income),
         "Fixed Costs ₾": int(q4_fixed), "Variable Costs ₾": int(q4_pipe_cog), "Total Expenses ₾": int(q4_expenses),
         "Net Profit ₾": int(q4_net), "Margin %": round(q4_net/q4_income*100,1) if q4_income else 0},
        {"Quarter": "FULL YEAR", "Status": "—",
         "Course Income ₾": int(q1_course_rev+q2_course_rev), "Corp Income ₾": int(q1_corp_rev+q2_corp_rev+q3_pipe_rev+q4_pipe_rev),
         "Total Income ₾": int(q1_income+q2_income+q3_income+q4_income),
         "Fixed Costs ₾": int(q1_fixed+q2_fixed+q3_fixed+q4_fixed),
         "Variable Costs ₾": int(q1_course_costs+q1_corp_cog+q2_course_costs+q2_corp_cog+q3_pipe_cog+q4_pipe_cog),
         "Total Expenses ₾": int(q1_expenses+q2_expenses+q3_expenses+q4_expenses),
         "Net Profit ₾": int(q1_net+q2_net+q3_net+q4_net),
         "Margin %": round((q1_net+q2_net+q3_net+q4_net)/(q1_income+q2_income+q3_income+q4_income)*100,1) if (q1_income+q2_income+q3_income+q4_income) else 0},
    ])

    st.dataframe(q_table, use_container_width=True, hide_index=True,
        column_config={
            "Course Income ₾": st.column_config.NumberColumn(format="₾ %d"),
            "Corp Income ₾": st.column_config.NumberColumn(format="₾ %d"),
            "Total Income ₾": st.column_config.NumberColumn(format="₾ %d"),
            "Fixed Costs ₾": st.column_config.NumberColumn(format="₾ %d"),
            "Variable Costs ₾": st.column_config.NumberColumn(format="₾ %d"),
            "Total Expenses ₾": st.column_config.NumberColumn(format="₾ %d"),
            "Net Profit ₾": st.column_config.NumberColumn(format="₾ %d"),
            "Margin %": st.column_config.NumberColumn(format="%.1f%%"),
        })

# ── FIXED COSTS ───────────────────────────────────────────────────────────────
elif page == "📌 Fixed Costs":
    st.markdown("## 📌 Fixed Costs")
    st.markdown('<p style="color:#30B143;margin-top:-12px">2026 budget · select month to view</p>', unsafe_allow_html=True)

    if "fx_month" not in st.session_state:
        st.session_state.fx_month = 0

    cols = st.columns(12)
    for i, m in enumerate(MONTHS):
        with cols[i]:
            active = st.session_state.fx_month == i
            if st.button(m, key=f"fx_m_{i}", use_container_width=True,
                        type="primary" if active else "secondary"):
                st.session_state.fx_month = i
                st.rerun()

    mi = st.session_state.fx_month
    mn = MONTHS[mi]

    st.markdown("### 👥 Salaries")
    sal_rows = []
    for s in st.session_state.fc_sal:
        sal_rows.append({
            "Name / Role": s["name"],
            f"{mn} ₾": s["m"][mi] if s["m"][mi] > 0 else 0,
            "Annual ₾": sum(s["m"]),
            "Active Months": sum(1 for v in s["m"] if v > 0),
        })
    sal_df = pd.DataFrame(sal_rows)
    edited_sal = st.data_editor(sal_df, use_container_width=True, hide_index=True, key=f"sal_editor_{mi}",
        column_config={
            "Name / Role": st.column_config.TextColumn("Name / Role", width="large"),
            f"{mn} ₾": st.column_config.NumberColumn(f"{mn} ₾", min_value=0, step=1, format="₾ %d"),
            "Annual ₾": st.column_config.NumberColumn("Annual ₾", disabled=True, format="₾ %d"),
            "Active Months": st.column_config.NumberColumn("Active Months", disabled=True),
        })
    # Explicit reassignment (not in-place mutation) so Streamlit detects the change
    new_fc_sal = []
    _sal_changed = False
    for i, s in enumerate(st.session_state.fc_sal):
        new_name = str(edited_sal.iloc[i]["Name / Role"] or s["name"])
        new_val = int(edited_sal.iloc[i][f"{mn} ₾"] or 0)
        if new_val != s["m"][mi] or new_name != s["name"]:
            _sal_changed = True
        new_m = s["m"][:]
        new_m[mi] = new_val
        new_fc_sal.append({"name": new_name, "m": new_m})
    st.session_state.fc_sal = new_fc_sal
    if _sal_changed:
        _save_state()
        st.rerun()
    sal_m = int(edited_sal[f"{mn} ₾"].sum())
    sal_a = sum(sum(s["m"]) for s in st.session_state.fc_sal)
    st.markdown(f'<div style="background:#f9fafb;border:1px solid #e5e7eb;padding:10px 16px;border-radius:8px;font-weight:700;display:flex;justify-content:space-between"><span>Total Salaries · {mn}</span><span style="color:#16a34a">{fmt(sal_m)} <span style="color:#9ca3af;font-weight:400;font-size:12px">/ {fmt(sal_a)} annual</span></span></div>', unsafe_allow_html=True)

    st.markdown("### 🏢 Admin & Subscriptions")
    sub_rows = []
    for s in st.session_state.fc_sub:
        sub_rows.append({
            "Item": s["name"],
            f"{mn} ₾": s["m"][mi],
            "Annual ₾": sum(s["m"]),
        })
    sub_df = pd.DataFrame(sub_rows)
    edited_sub = st.data_editor(sub_df, use_container_width=True, hide_index=True, key=f"sub_editor_{mi}",
        column_config={
            "Item": st.column_config.TextColumn("Item", width="large"),
            f"{mn} ₾": st.column_config.NumberColumn(f"{mn} ₾", min_value=0, step=1, format="₾ %d"),
            "Annual ₾": st.column_config.NumberColumn("Annual ₾", disabled=True, format="₾ %d"),
        })
    new_fc_sub = []
    _sub_changed = False
    for i, s in enumerate(st.session_state.fc_sub):
        new_name = str(edited_sub.iloc[i]["Item"] or s["name"])
        new_val = int(edited_sub.iloc[i][f"{mn} ₾"] or 0)
        if new_val != s["m"][mi] or new_name != s["name"]:
            _sub_changed = True
        new_m = s["m"][:]
        new_m[mi] = new_val
        new_fc_sub.append({"name": new_name, "m": new_m})
    st.session_state.fc_sub = new_fc_sub
    if _sub_changed:
        _save_state()
        st.rerun()
    sub_m = int(edited_sub[f"{mn} ₾"].sum())
    sub_a = sum(sum(s["m"]) for s in st.session_state.fc_sub)
    st.markdown(f'<div style="background:#f9fafb;border:1px solid #e5e7eb;padding:10px 16px;border-radius:8px;font-weight:700;display:flex;justify-content:space-between"><span>Total Admin & Subs · {mn}</span><span style="color:#16a34a">{fmt(sub_m)} <span style="color:#9ca3af;font-weight:400;font-size:12px">/ {fmt(sub_a)} annual</span></span></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    total = sal_m + sub_m
    st.markdown(f'<div style="background:#f0fdf4;border:2px solid #bbf7d0;padding:16px 20px;border-radius:12px;font-family:Space Grotesk,sans-serif;font-size:16px;font-weight:700;display:flex;justify-content:space-between"><span>🔒 Total Fixed Costs · {mn}</span><span style="color:#16a34a">{fmt(total)}</span></div>', unsafe_allow_html=True)

# ── COURSES P&L ───────────────────────────────────────────────────────────────
elif page == "🎓 Courses P&L":
    st.markdown("## 🎓 Courses P&L")
    st.markdown('<p style="color:#30B143;margin-top:-12px">2026 actuals · Net Profit = Revenue excl. VAT − Costs</p>', unsafe_allow_html=True)

    if "co_month" not in st.session_state:
        st.session_state.co_month = "All"

    st.markdown('<p style="font-size:11px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:#9d6fff;margin-bottom:6px">Filter by month</p>', unsafe_allow_html=True)
    month_opts = ["All"] + MONTHS[:6]
    cols = st.columns(len(month_opts))
    for i, m in enumerate(month_opts):
        with cols[i]:
            active = st.session_state.co_month == m
            if st.button(m, key=f"co_m_{m}", use_container_width=True,
                        type="primary" if active else "secondary"):
                st.session_state.co_month = m
                st.rerun()

    month_filter = st.session_state.co_month
    filtered = st.session_state.fc_courses if month_filter == "All" else [c for c in st.session_state.fc_courses if c["month"] == month_filter]

    rows = []
    for c in filtered:
        p = cpnl(c)
        rows.append({
            "Program": c["name"],
            "Month": c["month"],
            "Students": c["students"],
            "Price w/VAT ₾": c["price"],
            "Price w/o VAT ₾": round(c["price"] / 1.18, 0),
            "Lecturer Fee ₾": c["lecturer"],
            "Installment ₾": c.get("inst", 0),
            "Zoom ₾": c["zoom"],
            "Advertising ₾": c["mkt"],
            "Merch ₾": c["mat"],
            "Total Cost ₾": round(p["cs"], 2),
            "Revenue ₾": round(p["rv"], 2),
            "Gross Profit ₾": round(p["gp"], 2),
            "Net Profit ₾": round(p["net"], 2),
            "Profit Margin %": round(p["mg"], 2),
        })

    df = pd.DataFrame(rows)
    edited_courses = st.data_editor(df, use_container_width=True, hide_index=True, key="courses_editor",
        column_config={
            "Program":          st.column_config.TextColumn("Program", width="large"),
            "Month":            st.column_config.SelectboxColumn("Month", options=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]),
            "Students":         st.column_config.NumberColumn("Students", min_value=0, step=1),
            "Price w/VAT ₾":    st.column_config.NumberColumn("Price w/VAT ₾", min_value=0, format="₾ %d"),
            "Price w/o VAT ₾":  st.column_config.NumberColumn("Price w/o VAT ₾", disabled=True, format="₾ %d"),
            "Lecturer Fee ₾":   st.column_config.NumberColumn("Lecturer Fee ₾", min_value=0, format="₾ %d"),
            "Installment ₾":    st.column_config.NumberColumn("Installment ₾", min_value=0, format="₾ %d"),
            "Zoom ₾":           st.column_config.NumberColumn("Zoom ₾", min_value=0, format="₾ %d"),
            "Advertising ₾":    st.column_config.NumberColumn("Advertising ₾", min_value=0, format="₾ %d"),
            "Merch ₾":          st.column_config.NumberColumn("Merch ₾", min_value=0, format="₾ %d"),
            "Total Cost ₾":     st.column_config.NumberColumn("Total Cost ₾", disabled=True, format="₾ %.2f"),
            "Revenue ₾":        st.column_config.NumberColumn("Revenue ₾", min_value=0, format="₾ %.2f"),
            "Gross Profit ₾":   st.column_config.NumberColumn("Gross Profit ₾", disabled=True, format="₾ %.2f"),
            "Net Profit ₾":     st.column_config.NumberColumn("Net Profit ₾", disabled=True, format="₾ %.2f"),
            "Profit Margin %":  st.column_config.NumberColumn("Profit Margin %", disabled=True, format="%.2f%%"),
        },
        num_rows="dynamic")

    # Persist courses edits
    _new_cr = []
    _cr_chg = False
    for _, _r in edited_courses.iterrows():
        _e = {"name": str(_r.get("Program") or ""), "month": str(_r.get("Month") or "Jan"),
              "students": int(_r.get("Students") or 0), "price": float(_r.get("Price w/VAT ₾") or 0),
              "lecturer": float(_r.get("Lecturer Fee ₾") or 0), "inst": float(_r.get("Installment ₾") or 0),
              "zoom": float(_r.get("Zoom ₾") or 0), "mkt": float(_r.get("Advertising ₾") or 0),
              "mat": float(_r.get("Merch ₾") or 0), "rev": float(_r.get("Revenue ₾") or 0)}
        _new_cr.append(_e)
    if len(_new_cr) != len(st.session_state.fc_courses) or any(a != b for a, b in zip(_new_cr, st.session_state.fc_courses)):
        _cr_chg = True
    st.session_state.fc_courses = _new_cr
    if _cr_chg:
        _save_state()
        st.rerun()
    tot_rv  = edited_courses["Revenue ₾"].sum()
    tot_cs  = edited_courses["Total Cost ₾"].sum()
    tot_gp  = edited_courses["Gross Profit ₾"].sum()
    tot_net = edited_courses["Net Profit ₾"].sum()
    tot_rx  = edited_courses["Revenue ₾"].div(1.18).sum()
    tot_mg  = round(tot_net / tot_rx * 100, 1) if tot_rx else 0

    col1,col2,col3,col4 = st.columns(4)
    with col1: kpi("Total Revenue", fmt(tot_rv), "", "kpi-pos")
    with col2: kpi("Total Costs", fmt(tot_cs), "", "kpi-warn")
    with col3: kpi("Total Net Profit", fmt(tot_net), "", "kpi-pos" if tot_net>=0 else "kpi-neg")
    with col4: kpi("Avg Net Margin", pct(tot_mg), "excl. VAT basis", "kpi-pos" if tot_mg>=25 else "kpi-warn")

    st.markdown("### 🔍 Course Detail")
    selected = st.selectbox("Select a course", [c["name"] + f" ({c['month']})" for c in filtered])
    idx = [c["name"] + f" ({c['month']})" for c in filtered].index(selected)
    c = filtered[idx]
    p = cpnl(c)
    rv, rx, tot_cost = p["rv"], p["rx"], p["cs"]
    net = p["net"]

    col1, col2 = st.columns([1,2])
    with col1:
        det_rows = [
            {"Category": "Lecturer Fee", "₾": c["lecturer"], "% of Rev excl. VAT": f"{c['lecturer']/rx*100:.1f}%" if rx else "—"},
            {"Category": "Merch & Materials", "₾": c["mat"], "% of Rev excl. VAT": f"{c['mat']/rx*100:.1f}%" if rx else "—"},
            {"Category": "Advertising", "₾": c["mkt"], "% of Rev excl. VAT": f"{c['mkt']/rx*100:.1f}%" if rx else "—"},
            {"Category": "Zoom", "₾": c["zoom"], "% of Rev excl. VAT": f"{c['zoom']/rx*100:.1f}%" if rx else "—"},
            {"Category": "── Total Costs ──", "₾": tot_cost, "% of Rev excl. VAT": f"{tot_cost/rx*100:.1f}%" if rx else "—"},
            {"Category": "Revenue incl. VAT", "₾": rv, "% of Rev excl. VAT": "—"},
            {"Category": "VAT deducted (18%)", "₾": -(rv - rx), "% of Rev excl. VAT": "—"},
            {"Category": "Revenue excl. VAT", "₾": rx, "% of Rev excl. VAT": "100%"},
            {"Category": "★ Net Profit", "₾": net, "% of Rev excl. VAT": f"{net/rx*100:.1f}%" if rx else "—"},
        ]
        st.dataframe(pd.DataFrame(det_rows), use_container_width=True, hide_index=True)
    with col2:
        fig_det = go.Figure(go.Pie(
            labels=["Lecturer Fee", "Advertising", "Merch", "Zoom"],
            values=[c["lecturer"], c["mkt"], c["mat"], c["zoom"]],
            hole=0.55,
            marker_colors=["#9d6fff", "#ffd166", "#2dffb8", "#ff6b8a"],
            textinfo="label+percent",
            textfont=dict(size=11, color="#ffffff"),
        ))
        fig_det.update_layout(
            paper_bgcolor="#ffffff",
            font=dict(color="#374151", size=11),
            margin=dict(t=10, b=10, l=10, r=10),
            height=260,
            showlegend=False,
            annotations=[dict(
                text=f"<b>{fmt(tot_cost)}</b><br><span style='font-size:10px'>total cost</span>",
                x=0.5, y=0.5, font_size=13, font_color="#374151", showarrow=False
            )],
        )
        st.plotly_chart(fig_det, use_container_width=True, config={"displayModeBar": False})

# ── CORPORATE ─────────────────────────────────────────────────────────────────
elif page == "🏢 Corporate Projects":
    st.markdown("## 🏢 Corporate Projects")
    st.markdown('<p style="color:#30B143;margin-top:-12px">B2B + B2G · 2026 actuals + 2025 history</p>', unsafe_allow_html=True)

    tR26 = sum(p["revenue"] for p in st.session_state.fc_corp26)
    tC26 = sum(p["cog"] for p in st.session_state.fc_corp26)
    tP26 = tR26 - tC26
    b2b = sum(p["revenue"] for p in st.session_state.fc_corp26 if p["type"]=="B2B")
    b2g = sum(p["revenue"] for p in st.session_state.fc_corp26 if p["type"]=="B2G")
    pp_r = sum(p["rev"] for p in PIPELINE)

    col1,col2,col3 = st.columns(3)
    with col1: kpi("2026 Revenue", fmt(tR26), f"B2B {fmt(b2b)} · B2G {fmt(b2g)}", "kpi-pos")
    with col2: kpi("2026 Net Profit", fmt(tP26), f"Margin {pct(tP26/tR26*100 if tR26 else 0)}", "kpi-pos")
    with col3: kpi("Q3–Q4 Pipeline", fmt(pp_r), f"{len(PIPELINE)} projects incl. GITA H2", "kpi-warn")


    rows = []
    for p in st.session_state.fc_corp26:
        rows.append({
            "Project": p["name"], "Type": p["type"], "Period": p["period"],
            "Revenue ₾": float(p["revenue"]), "COG ₾": float(p["cog"]),
            "Status": p["status"]
        })
    df26 = pd.DataFrame(rows)
    edited_corp26 = st.data_editor(df26, use_container_width=True, hide_index=True, key="corp26_editor",
        column_config={
            "Project": st.column_config.TextColumn("Project", width="large"),
            "Type": st.column_config.SelectboxColumn("Type", options=["B2B","B2G"]),
            "Period": st.column_config.TextColumn("Period"),
            "Revenue ₾": st.column_config.NumberColumn("Revenue ₾", min_value=0, format="₾ %d"),
            "COG ₾": st.column_config.NumberColumn("COG ₾", min_value=0, format="₾ %d"),
            "Status": st.column_config.SelectboxColumn("Status", options=["Paid","Active","Pending","Upcoming"]),
        })
    # Compute Net Profit and Margin live from edited Revenue - COG
    _rev26 = edited_corp26["Revenue ₾"].fillna(0)
    _cog26 = edited_corp26["COG ₾"].fillna(0)
    _net26 = (_rev26 - _cog26).round(0).astype(int)
    _mg26  = (_net26 / _rev26 * 100).fillna(0).round(1)
    edited_corp26 = edited_corp26.copy()
    edited_corp26["Net Profit ₾"] = _net26
    edited_corp26["Margin %"]     = _mg26
    # Persist edits — compare as (revenue, cog) tuples to avoid int/float mismatch
    _new26 = []
    for i in range(len(edited_corp26)):
        r = edited_corp26.iloc[i]
        _new26.append({
            "name":    str(r["Project"])  if pd.notna(r["Project"])  else "",
            "type":    str(r["Type"])     if pd.notna(r["Type"])     else "B2B",
            "period":  str(r["Period"])   if pd.notna(r["Period"])   else "",
            "revenue": float(r["Revenue ₾"]) if pd.notna(r["Revenue ₾"]) else 0.0,
            "cog":     float(r["COG ₾"])     if pd.notna(r["COG ₾"])     else 0.0,
            "status":  str(r["Status"])  if pd.notna(r["Status"])   else "Paid",
        })
    _old_rv_cg = [(float(p["revenue"]), float(p["cog"])) for p in st.session_state.fc_corp26]
    _new_rv_cg = [(_e["revenue"], _e["cog"]) for _e in _new26]
    st.session_state.fc_corp26 = _new26
    if _old_rv_cg != _new_rv_cg or len(_new26) != len(_old_rv_cg):
        _save_state()
        st.rerun()
    tR26e = _rev26.sum()
    tP26e = _net26.sum()
    st.markdown(f'<div style="background:#f9fafb;border:1px solid #e5e7eb;padding:10px 16px;border-radius:8px;font-weight:700;display:flex;justify-content:space-between"><span>Total 2026</span><span style="color:#16a34a">{fmt(tR26e)} revenue · {fmt(tP26e)} profit · {pct(tP26e/tR26e*100 if tR26e else 0)} margin</span></div>', unsafe_allow_html=True)

    # ── PIPELINE ──────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🔮 Q3–Q4 Pipeline")
    st.markdown('<p style="color:#30B143;margin-top:-12px">Confirmed + planning stage projects</p>', unsafe_allow_html=True)

    pipe_rows = []
    for p in PIPELINE:
        pf = p["rev"] - p["cog"]
        mg = pf / p["rev"] * 100 if p["rev"] else 0
        pipe_rows.append({
            "Project": p["name"], "Type": p["type"], "Quarter": p["q"],
            "Revenue ₾": p["rev"], "COG ₾": p["cog"],
            "Net Profit ₾": int(pf), "Margin %": round(mg, 1), "Stage": p["stage"]
        })
    df_pipe = pd.DataFrame(pipe_rows)
    st.data_editor(df_pipe, use_container_width=True, hide_index=True, key="pipe_editor",
        column_config={
            "Project": st.column_config.TextColumn("Project", width="large"),
            "Type": st.column_config.SelectboxColumn("Type", options=["B2B", "B2G"]),
            "Quarter": st.column_config.TextColumn("Quarter"),
            "Revenue ₾": st.column_config.NumberColumn("Revenue ₾", min_value=0, format="₾ %d"),
            "COG ₾": st.column_config.NumberColumn("COG ₾", min_value=0, format="₾ %d"),
            "Net Profit ₾": st.column_config.NumberColumn("Net Profit ₾", disabled=True, format="₾ %d"),
            "Margin %": st.column_config.NumberColumn("Margin %", disabled=True, format="%.1f%%"),
            "Stage": st.column_config.SelectboxColumn("Stage", options=["Confirmed", "Planning", "Upcoming"]),
        })
    pipe_r = sum(p["rev"] for p in PIPELINE)
    pipe_c = sum(p["cog"] for p in PIPELINE)
    pipe_p = pipe_r - pipe_c
    st.markdown(f'<div style="background:#f9fafb;border:1px solid #e5e7eb;padding:10px 16px;border-radius:8px;font-weight:700;display:flex;justify-content:space-between"><span>Total Pipeline Q3–Q4</span><span style="color:#d97706">{fmt(pipe_r)} revenue · {fmt(pipe_p)} profit · {pct(pipe_p/pipe_r*100 if pipe_r else 0)} margin</span></div>', unsafe_allow_html=True)

    # ── 2025 HISTORY ──────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 📜 2025 Corporate History")
    st.markdown('<p style="color:#30B143;margin-top:-12px">Full-year actuals</p>', unsafe_allow_html=True)

    tR25 = sum(p["rev"] for p in CORP25)
    tC25 = sum(p["cost"] for p in CORP25)
    tP25 = sum(p["profit"] for p in CORP25)
    b2b25 = sum(p["rev"] for p in CORP25 if p["type"] == "B2B")
    b2g25 = sum(p["rev"] for p in CORP25 if p["type"] == "B2G")

    col1, col2, col3 = st.columns(3)
    with col1: kpi("2025 Revenue", fmt(tR25), f"B2B {fmt(b2b25)} · B2G {fmt(b2g25)}", "kpi-pos")
    with col2: kpi("2025 Net Profit", fmt(tP25), f"Margin {pct(tP25/tR25*100 if tR25 else 0)}", "kpi-pos")
    with col3: kpi("YoY Revenue Growth", pct((tR26-tR25)/tR25*100 if tR25 else 0), f"2025: {fmt(tR25)} → 2026: {fmt(tR26)}", "kpi-pos" if tR26 >= tR25 else "kpi-neg")

    st.markdown("<br>", unsafe_allow_html=True)
    rows25 = []
    for p in CORP25:
        rows25.append({
            "Client": p["co"], "Program": p["pr"], "Type": p["type"], "Period": p["period"],
            "Revenue ₾": p["rev"], "Cost ₾": p["cost"],
            "Net Profit ₾": p["profit"], "Margin %": p["margin"]
        })
    df25 = pd.DataFrame(rows25)
    st.dataframe(df25, use_container_width=True, hide_index=True,
        column_config={
            "Client": st.column_config.TextColumn("Client", width="medium"),
            "Program": st.column_config.TextColumn("Program", width="large"),
            "Type": st.column_config.TextColumn("Type"),
            "Period": st.column_config.TextColumn("Period"),
            "Revenue ₾": st.column_config.NumberColumn("Revenue ₾", format="₾ %d"),
            "Cost ₾": st.column_config.NumberColumn("Cost ₾", format="₾ %d"),
            "Net Profit ₾": st.column_config.NumberColumn("Net Profit ₾", format="₾ %d"),
            "Margin %": st.column_config.NumberColumn("Margin %", format="%.1f%%"),
        })
    st.markdown(f'<div style="background:#f9fafb;border:1px solid #e5e7eb;padding:10px 16px;border-radius:8px;font-weight:700;display:flex;justify-content:space-between"><span>Total 2025</span><span style="color:#16a34a">{fmt(tR25)} revenue · {fmt(tP25)} profit · {pct(tP25/tR25*100 if tR25 else 0)} margin</span></div>', unsafe_allow_html=True)
