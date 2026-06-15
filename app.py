import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

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
        .login-box {
            max-width: 400px;
            margin: 8vh auto 0;
            padding: 2.5rem;
            background: #1a1d27;
            border: 1px solid #2e3350;
            border-radius: 16px;
        }
        .login-label { font-size:10px; font-weight:700; letter-spacing:2px; color:#555c7a; text-transform:uppercase; margin-bottom:4px; }
        .login-title { font-size:24px; font-weight:700; color:#e8eaf0; margin-bottom:4px; }
        .login-sub { font-size:13px; color:#8b90a7; margin-bottom:2rem; }
        </style>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div style="text-align:center;margin-top:8vh">', unsafe_allow_html=True)
            st.markdown('<p style="font-size:10px;font-weight:700;letter-spacing:2px;color:#555c7a;text-transform:uppercase">COMMSCHOOL</p>', unsafe_allow_html=True)
            st.markdown('<h1 style="font-size:28px;font-weight:700;color:#e8eaf0;margin:0">Digital <span style="color:#6c63ff">CFO</span></h1>', unsafe_allow_html=True)
            st.markdown('<p style="font-size:13px;color:#8b90a7;margin-bottom:2rem">Internal financial dashboard</p>', unsafe_allow_html=True)
            pwd = st.text_input("Access Code", type="password", placeholder="Enter passcode")
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
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&display=swap');

[data-testid="stAppViewContainer"] { background: #0f1117; }
[data-testid="stSidebar"] { background: #1a1d27; border-right: 1px solid #2e3350; }
[data-testid="stSidebar"] * { color: #8b90a7 !important; }
h1,h2,h3 { font-family: 'Space Grotesk', sans-serif !important; color: #e8eaf0 !important; }
.stDataFrame { border: 1px solid #2e3350 !important; border-radius: 10px !important; }

.kpi-card {
    background: #1a1d27;
    border: 1px solid #2e3350;
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 4px;
}
.kpi-label { font-size:10px; font-weight:700; letter-spacing:1.5px; text-transform:uppercase; color:#555c7a; margin-bottom:6px; }
.kpi-value { font-family:'Space Grotesk',sans-serif; font-size:22px; font-weight:700; margin-bottom:3px; }
.kpi-sub { font-size:11px; color:#8b90a7; }
.kpi-pos { color: #00d4aa; }
.kpi-neg { color: #ff5f7e; }
.kpi-warn { color: #ffa94d; }

.insight-card {
    background: #22263a;
    border: 1px solid #2e3350;
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 10px;
    display: flex;
    gap: 12px;
    align-items: flex-start;
}
.badge-pos { background:rgba(0,212,170,.15); color:#00d4aa; padding:2px 8px; border-radius:4px; font-size:11px; font-weight:700; }
.badge-neg { background:rgba(255,95,126,.15); color:#ff5f7e; padding:2px 8px; border-radius:4px; font-size:11px; font-weight:700; }
.badge-warn { background:rgba(255,169,77,.15); color:#ffa94d; padding:2px 8px; border-radius:4px; font-size:11px; font-weight:700; }
.badge-b2g { background:rgba(0,212,170,.12); color:#00d4aa; padding:1px 6px; border-radius:3px; font-size:11px; font-weight:700; }
.badge-b2b { background:rgba(108,99,255,.12); color:#6c63ff; padding:1px 6px; border-radius:3px; font-size:11px; font-weight:700; }

div[data-testid="stHorizontalBlock"] > div { gap: 0.75rem; }
.stButton > button { background: #6c63ff !important; color: white !important; border: none !important; border-radius: 8px !important; font-weight:600 !important; }
.stButton > button:hover { background: #5a52e8 !important; }
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
    {"name":"Graphic Design","month":"Jan","students":3,"price":1250,"lecturer":2800,"mat":175,"mkt":1111,"zoom":40},
    {"name":"Marketing Management","month":"Feb","students":4,"price":1500,"lecturer":3500,"mat":236,"mkt":1021,"zoom":40},
    {"name":"Content Management","month":"Feb","students":0,"price":1400,"lecturer":0,"mat":0,"mkt":1638,"zoom":0},
    {"name":"Data Analytics","month":"Feb","students":8,"price":1700,"lecturer":5357,"mat":420,"mkt":1225,"zoom":40},
    {"name":"AI in Content","month":"Feb","students":8,"price":1400,"lecturer":3000,"mat":360,"mkt":1439,"zoom":40},
    {"name":"AI Agents","month":"Mar","students":9,"price":1400,"lecturer":2551,"mat":405,"mkt":1542,"zoom":40},
    {"name":"Data Science","month":"Mar","students":9,"price":2700,"lecturer":12117,"mat":405,"mkt":1369,"zoom":40},
    {"name":"Growth Marketing","month":"Mar","students":17,"price":1500,"lecturer":4000,"mat":765,"mkt":569,"zoom":40},
    {"name":"IT BA","month":"Apr","students":8,"price":1500,"lecturer":3571,"mat":400,"mkt":1334,"zoom":40},
    {"name":"ADS","month":"Apr","students":14,"price":1400,"lecturer":5357,"mat":630,"mkt":1385,"zoom":40},
    {"name":"AI SEO","month":"May","students":5,"price":1400,"lecturer":3061,"mat":265,"mkt":1651,"zoom":40},
    {"name":"AI Essentials","month":"May","students":5,"price":1050,"lecturer":2551,"mat":265,"mkt":1557,"zoom":40},
    {"name":"Data Analytics","month":"May","students":6,"price":1700,"lecturer":5357,"mat":310,"mkt":1210,"zoom":40},
    {"name":"GITA: IT PM","month":"May","students":7,"price":1000,"lecturer":3571,"mat":355,"mkt":262,"zoom":40},
    {"name":"GITA: Motion Design","month":"May","students":7,"price":1000,"lecturer":3000,"mat":355,"mkt":262,"zoom":40},
    {"name":"GITA: IT BA","month":"May","students":7,"price":1000,"lecturer":3571,"mat":355,"mkt":262,"zoom":40},
    {"name":"GITA: Python","month":"May","students":29,"price":2000,"lecturer":13500,"mat":1305,"mkt":262,"zoom":40},
    {"name":"GITA: C#","month":"May","students":26,"price":2000,"lecturer":14000,"mat":1210,"mkt":262,"zoom":40},
    {"name":"GITA: QA","month":"May","students":6,"price":1000,"lecturer":6300,"mat":310,"mkt":262,"zoom":40},
    {"name":"GITA: Graphic Design","month":"May","students":13,"price":1000,"lecturer":3150,"mat":635,"mkt":262,"zoom":40},
    {"name":"GITA: UI/UX Design","month":"May","students":15,"price":1000,"lecturer":3571,"mat":715,"mkt":262,"zoom":40},
    {"name":"AI in Content","month":"Jun","students":12,"price":1400,"lecturer":2600,"mat":580,"mkt":1077,"zoom":40},
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
    rv = c["students"] * c["price"]
    rx = rv / 1.18
    cs = c["lecturer"] + c["mat"] + c["mkt"] + c["zoom"]
    net = rx - cs
    mg = net / rx * 100 if rx > 0 else 0
    return {"rv": rv, "rx": rx, "cs": cs, "gp": rv - cs, "net": net, "mg": mg}

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
        textfont=dict(size=10, color="#8b90a7"),
    ))
    fig.update_layout(
        paper_bgcolor="#1a1d27", plot_bgcolor="#1a1d27",
        font=dict(color="#8b90a7", size=11),
        margin=dict(t=20, b=10, l=10, r=10),
        height=220,
        xaxis=dict(showgrid=False, tickfont=dict(size=10, color="#555c7a")),
        yaxis=dict(showgrid=True, gridcolor="#2e3350", tickfont=dict(size=10)),
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div style="padding:4px 0 16px"><p style="font-size:10px;font-weight:700;letter-spacing:2px;color:#555c7a;text-transform:uppercase;margin:0">COMMSCHOOL</p><h2 style="font-size:22px;font-weight:700;color:#e8eaf0;margin:0">Digital <span style="color:#6c63ff">CFO</span></h2></div>', unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("", ["📊 Dashboard", "📌 Fixed Costs", "🎓 Courses P&L", "🏢 Corporate Projects"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown('<p style="font-size:10px;color:#555c7a">₾ GEL · 2026 · H1 actuals</p>', unsafe_allow_html=True)
    if st.button("🔒 Lock", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

# ── DASHBOARD ─────────────────────────────────────────────────────────────────
if page == "📊 Dashboard":
    st.markdown("## Financial Overview")
    st.markdown('<p style="color:#8b90a7;margin-top:-12px">2026 H1 · Courses + Corporate actuals</p>', unsafe_allow_html=True)

    mi = MONTHS.index("Jun")  # default to Jun for H1 snapshot
    sal_m = sum(s["m"][mi] for s in SALARIES)
    sub_m = sum(s["m"][mi] for s in SUBS)
    sal_a = sum(sum(s["m"]) for s in SALARIES)
    sub_a = sum(sum(s["m"]) for s in SUBS)

    c_data = [cpnl(c) for c in COURSES]
    c_rev = sum(d["rv"] for d in c_data)
    c_net = sum(d["net"] for d in c_data)
    c_rx  = sum(d["rx"] for d in c_data)
    c_cs  = sum(d["cs"] for d in c_data)

    crp_r = sum(p["revenue"] for p in CORP26)
    crp_c = sum(p["cog"] for p in CORP26)
    crp_p = crp_r - crp_c

    tot_r = c_rev + crp_r

    col1, col2, col3, col4 = st.columns(4)
    with col1: kpi("H1 Total Revenue", fmt(tot_r), f"Courses {fmt(c_rev)} · Corp {fmt(crp_r)}", "kpi-pos")
    with col2: kpi("Course Net Profit", fmt(c_net), f"Margin {pct(c_net/c_rx*100 if c_rx else 0)} · excl. VAT", "kpi-pos" if c_net >= 0 else "kpi-neg")
    with col3: kpi("Corporate Net Profit", fmt(crp_p), f"Margin {pct(crp_p/crp_r*100 if crp_r else 0)}", "kpi-pos")
    with col4: kpi("Fixed Costs · Jun", fmt(sal_m + sub_m), f"{fmt(sal_a + sub_a)} full-year budget", "kpi-warn")

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    gita_r = sum(cpnl(c)["rv"] for c in COURSES if c["name"].startswith("GITA"))
    own_r  = c_rev - gita_r
    b2b_r  = sum(p["revenue"] for p in CORP26 if p["type"] == "B2B")
    b2g_r  = sum(p["revenue"] for p in CORP26 if p["type"] == "B2G")
    lec_t  = sum(c["lecturer"] for c in COURSES)
    mkt_t  = sum(c["mkt"] for c in COURSES)

    with col1:
        st.markdown('<div class="kpi-card"><div class="kpi-label">📈 Revenue Mix</div></div>', unsafe_allow_html=True)
        bar_chart([
            {"l":"Own Courses","v":own_r,"c":"#6c63ff"},
            {"l":"GITA Courses","v":gita_r,"c":"#a39df0"},
            {"l":"Corp B2B","v":b2b_r,"c":"#00d4aa"},
            {"l":"Corp B2G","v":b2g_r,"c":"#4ec9b0"},
        ])

    with col2:
        st.markdown('<div class="kpi-card"><div class="kpi-label">💸 Cost Structure</div></div>', unsafe_allow_html=True)
        bar_chart([
            {"l":"Salaries","v":sal_a,"c":"#ff5f7e"},
            {"l":"Admin+Subs","v":sub_a,"c":"#a39df0"},
            {"l":"Lecturer Fees","v":lec_t,"c":"#6c63ff"},
            {"l":"Advertising","v":mkt_t,"c":"#ffa94d"},
            {"l":"Corp COG","v":crp_c,"c":"#00d4aa"},
        ])

    st.markdown("### 💡 CFO Insights")
    top_c  = max([c for c in COURSES if cpnl(c)["rx"] > 0], key=lambda c: cpnl(c)["mg"])
    wrst_c = min([c for c in COURSES if cpnl(c)["rx"] > 0], key=lambda c: cpnl(c)["mg"])
    gita_dep = (gita_r + b2g_r) / tot_r * 100 if tot_r else 0

    for icon, text in [
        ("🏆", f"**Best margin:** {top_c['name']} ({top_c['month']}) at **{pct(cpnl(top_c)['mg'])}**. Low ad spend + strong cohort size."),
        ("⚠️", f"**GITA + B2G = {pct(gita_dep)} of H1 revenue.** Audit (₾28,400) still pending — watch vs. {fmt(sal_m+sub_m)}/month fixed costs."),
        ("📉", f"**Lowest margin:** {wrst_c['name']} ({wrst_c['month']}). Set a minimum enrollment threshold before launching."),
        ("💼", f"**2026 salary budget: {fmt(sal_a)}.** CEO = {pct(8929*12/sal_a*100)} of total payroll. H1 fixed budget: {fmt((sal_a+sub_a)//2)}."),
    ]:
        st.markdown(f"""<div class="insight-card"><span style="font-size:18px">{icon}</span><span style="font-size:13px;color:#8b90a7;line-height:1.6">{text}</span></div>""", unsafe_allow_html=True)

# ── FIXED COSTS ───────────────────────────────────────────────────────────────
elif page == "📌 Fixed Costs":
    st.markdown("## 📌 Fixed Costs")
    st.markdown('<p style="color:#8b90a7;margin-top:-12px">2026 budget · select month to view</p>', unsafe_allow_html=True)

    mi = st.select_slider("Month", options=list(range(12)), format_func=lambda i: MONTHS[i], value=0)
    mn = MONTHS[mi]

    st.markdown("### 👥 Salaries")
    sal_rows = []
    for s in SALARIES:
        sal_rows.append({
            "Name / Role": s["name"],
            f"{mn} (₾)": f"₾ {s['m'][mi]:,}" if s["m"][mi] > 0 else "—",
            "Annual Budget (₾)": f"₾ {sum(s['m']):,}",
            "Active Months": f"{sum(1 for v in s['m'] if v > 0)} months"
        })
    sal_df = pd.DataFrame(sal_rows)
    st.dataframe(sal_df, use_container_width=True, hide_index=True)
    sal_m = sum(s["m"][mi] for s in SALARIES)
    sal_a = sum(sum(s["m"]) for s in SALARIES)
    st.markdown(f'<div style="background:#22263a;padding:10px 16px;border-radius:8px;font-weight:700;display:flex;justify-content:space-between"><span>Total Salaries · {mn}</span><span style="color:#00d4aa">{fmt(sal_m)} <span style="color:#555c7a;font-weight:400;font-size:12px">/ {fmt(sal_a)} annual</span></span></div>', unsafe_allow_html=True)

    st.markdown("### 🏢 Admin & Subscriptions")
    sub_rows = []
    for s in SUBS:
        sub_rows.append({
            "Item": s["name"],
            f"{mn} (₾)": f"₾ {s['m'][mi]:,}",
            "Annual Budget (₾)": f"₾ {sum(s['m']):,}",
        })
    sub_df = pd.DataFrame(sub_rows)
    st.dataframe(sub_df, use_container_width=True, hide_index=True)
    sub_m = sum(s["m"][mi] for s in SUBS)
    sub_a = sum(sum(s["m"]) for s in SUBS)
    st.markdown(f'<div style="background:#22263a;padding:10px 16px;border-radius:8px;font-weight:700;display:flex;justify-content:space-between"><span>Total Admin & Subs · {mn}</span><span style="color:#00d4aa">{fmt(sub_m)} <span style="color:#555c7a;font-weight:400;font-size:12px">/ {fmt(sub_a)} annual</span></span></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    total = sal_m + sub_m
    st.markdown(f'<div style="background:#1a1d27;border:1px solid #2e3350;padding:16px 20px;border-radius:12px;font-family:Space Grotesk,sans-serif;font-size:16px;font-weight:700;display:flex;justify-content:space-between"><span>🔒 Total Fixed Costs · {mn}</span><span style="color:#ffa94d">{fmt(total)}</span></div>', unsafe_allow_html=True)

# ── COURSES P&L ───────────────────────────────────────────────────────────────
elif page == "🎓 Courses P&L":
    st.markdown("## 🎓 Courses P&L")
    st.markdown('<p style="color:#8b90a7;margin-top:-12px">2026 actuals · Net Profit = Revenue excl. VAT − Costs</p>', unsafe_allow_html=True)

    month_filter = st.selectbox("Filter by month", ["All"] + MONTHS[:6])
    filtered = COURSES if month_filter == "All" else [c for c in COURSES if c["month"] == month_filter]

    rows = []
    for c in filtered:
        p = cpnl(c)
        rows.append({
            "Program": c["name"],
            "Month": c["month"],
            "Students": c["students"],
            "Price ₾": c["price"],
            "Revenue ₾": int(p["rv"]),
            "Costs ₾": int(p["cs"]),
            "Gross Profit ₾": int(p["gp"]),
            "Net Profit ₾": int(p["net"]),
            "Margin %": round(p["mg"], 1),
        })

    df = pd.DataFrame(rows)
    tot_rv = df["Revenue ₾"].sum()
    tot_cs = df["Costs ₾"].sum()
    tot_gp = df["Gross Profit ₾"].sum()
    tot_net = df["Net Profit ₾"].sum()
    tot_rx = sum(cpnl(c)["rx"] for c in filtered)
    tot_mg = round(tot_net / tot_rx * 100, 1) if tot_rx else 0

    st.dataframe(
        df.style
          .format({"Revenue ₾": "₾ {:,.0f}", "Costs ₾": "₾ {:,.0f}", "Gross Profit ₾": "₾ {:,.0f}", "Net Profit ₾": "₾ {:,.0f}", "Margin %": "{:.1f}%"})
          .map(lambda v: "color: #00d4aa" if isinstance(v, (int,float)) and v > 0 else ("color: #ff5f7e" if isinstance(v,(int,float)) and v < 0 else ""), subset=["Net Profit ₾","Gross Profit ₾"])
          .map(lambda v: "color: #00d4aa" if isinstance(v,(int,float)) and v >= 50 else ("color: #ffa94d" if isinstance(v,(int,float)) and v >= 25 else ("color: #ff5f7e" if isinstance(v,(int,float)) and v > 0 else "")), subset=["Margin %"]),
        use_container_width=True, hide_index=True
    )

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

# ── CORPORATE ─────────────────────────────────────────────────────────────────
elif page == "🏢 Corporate Projects":
    st.markdown("## 🏢 Corporate Projects")
    st.markdown('<p style="color:#8b90a7;margin-top:-12px">B2B + B2G · 2026 actuals + 2025 history</p>', unsafe_allow_html=True)

    tR26 = sum(p["revenue"] for p in CORP26)
    tC26 = sum(p["cog"] for p in CORP26)
    tP26 = tR26 - tC26
    b2b = sum(p["revenue"] for p in CORP26 if p["type"]=="B2B")
    b2g = sum(p["revenue"] for p in CORP26 if p["type"]=="B2G")
    pp_r = sum(p["rev"] for p in PIPELINE)

    col1,col2,col3 = st.columns(3)
    with col1: kpi("2026 Revenue", fmt(tR26), f"B2B {fmt(b2b)} · B2G {fmt(b2g)}", "kpi-pos")
    with col2: kpi("2026 Net Profit", fmt(tP26), f"Margin {pct(tP26/tR26*100 if tR26 else 0)}", "kpi-pos")
    with col3: kpi("Q3–Q4 Pipeline", fmt(pp_r), f"{len(PIPELINE)} projects incl. GITA H2", "kpi-warn")

    tab1, tab2, tab3 = st.tabs(["📋 2026 Actuals", "📂 2025 History", "🔮 Pipeline"])

    with tab1:
        rows = []
        for p in CORP26:
            pf = p["revenue"] - p["cog"]
            mg = pf / p["revenue"] * 100 if p["revenue"] else 0
            rows.append({
                "Project": p["name"], "Type": p["type"], "Period": p["period"],
                "Revenue ₾": p["revenue"], "COG ₾": p["cog"],
                "Net Profit ₾": int(pf), "Margin %": round(mg,1), "Status": p["status"]
            })
        df26 = pd.DataFrame(rows)
        st.dataframe(
            df26.style.format({"Revenue ₾":"₾ {:,.0f}","COG ₾":"₾ {:,.0f}","Net Profit ₾":"₾ {:,.0f}","Margin %":"{:.1f}%"})
                .map(lambda v: "color:#00d4aa" if isinstance(v,(int,float)) and v>0 else "", subset=["Net Profit ₾"])
                .map(lambda v: "color:#00d4aa" if isinstance(v,(int,float)) and v>=50 else ("color:#ffa94d" if isinstance(v,(int,float)) and v>=25 else "color:#ff5f7e"), subset=["Margin %"]),
            use_container_width=True, hide_index=True
        )
        st.markdown(f'<div style="background:#22263a;padding:10px 16px;border-radius:8px;font-weight:700;display:flex;justify-content:space-between"><span>Total 2026</span><span style="color:#00d4aa">{fmt(tR26)} revenue · {fmt(tP26)} profit · {pct(tP26/tR26*100 if tR26 else 0)} margin</span></div>', unsafe_allow_html=True)

    with tab2:
        rows25 = []
        for p in CORP25:
            rows25.append({
                "Company": p["co"], "Project": p["pr"], "Type": p["type"], "Period": p["period"],
                "Revenue ₾": p["rev"], "Cost ₾": p["cost"],
                "Profit ₾": p["profit"], "Margin %": p["margin"]
            })
        df25 = pd.DataFrame(rows25)
        t25r = df25["Revenue ₾"].sum(); t25p = df25["Profit ₾"].sum()
        st.dataframe(
            df25.style.format({"Revenue ₾":"₾ {:,.0f}","Cost ₾":"₾ {:,.0f}","Profit ₾":"₾ {:,.0f}","Margin %":"{:.1f}%"})
                .map(lambda v: "color:#00d4aa" if isinstance(v,(int,float)) and v>0 else "", subset=["Profit ₾"]),
            use_container_width=True, hide_index=True
        )
        st.markdown(f'<div style="background:#22263a;padding:10px 16px;border-radius:8px;font-weight:700;display:flex;justify-content:space-between"><span>Total 2025</span><span style="color:#00d4aa">{fmt(t25r)} revenue · {fmt(t25p)} profit · {pct(t25p/t25r*100 if t25r else 0)} margin</span></div>', unsafe_allow_html=True)

    with tab3:
        rowspp = []
        for p in PIPELINE:
            pf = p["rev"] - p["cog"]
            mg = pf / p["rev"] * 100 if p["rev"] else 0
            rowspp.append({
                "Project": p["name"], "Type": p["type"], "Quarter": p["q"],
                "Est. Revenue ₾": p["rev"], "Est. COG ₾": p["cog"],
                "Est. Profit ₾": int(pf), "Margin %": round(mg,1), "Stage": p["stage"]
            })
        dfpp = pd.DataFrame(rowspp)
        tppr = dfpp["Est. Revenue ₾"].sum(); tppp = dfpp["Est. Profit ₾"].sum()
        st.dataframe(
            dfpp.style.format({"Est. Revenue ₾":"₾ {:,.0f}","Est. COG ₾":"₾ {:,.0f}","Est. Profit ₾":"₾ {:,.0f}","Margin %":"{:.1f}%"}),
            use_container_width=True, hide_index=True
        )
        st.markdown(f'<div style="background:#22263a;padding:10px 16px;border-radius:8px;font-weight:700;display:flex;justify-content:space-between"><span>Pipeline Total</span><span style="color:#ffa94d">{fmt(tppr)} est. revenue · {fmt(tppp)} est. profit</span></div>', unsafe_allow_html=True)
