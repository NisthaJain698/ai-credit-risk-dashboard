import streamlit as st
import joblib
import numpy as np
import plotly.graph_objects as go

st.set_page_config(
    page_title="CreditSense AI",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

model = joblib.load("credit_model.pkl")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=IBM+Plex+Mono:wght@400;500&family=Inter:wght@400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main { background: #07090f !important; }

[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stSidebar"],
footer, #MainMenu { display: none !important; }

/* KEY FIX: constrain content width and add real side padding */
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* Animated grid */
[data-testid="stAppViewContainer"]::before {
    content: ''; position: fixed; inset: 0; z-index: 0; pointer-events: none;
    background-image:
        linear-gradient(rgba(0,212,180,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,212,180,0.03) 1px, transparent 1px);
    background-size: 56px 56px;
    animation: drift 25s linear infinite;
}
@keyframes drift { from{background-position:0 0} to{background-position:56px 56px} }

[data-testid="stAppViewContainer"]::after {
    content: ''; position: fixed;
    top: -300px; right: -200px;
    width: 700px; height: 700px;
    background: radial-gradient(circle, rgba(59,130,246,0.04) 0%, transparent 65%);
    pointer-events: none; z-index: 0;
}

/* ─── SHELL: THIS IS THE KEY MARGIN FIX ─── */
/* Wraps all custom HTML content with proper side margins */
.shell {
    position: relative; z-index: 1;
    max-width: 1180px;          /* narrower max-width */
    margin: 0 auto;
    padding: 32px 48px 72px;    /* generous side padding */
}

/* ── TOPBAR ── */
.topbar {
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 32px; padding-bottom: 20px;
    border-bottom: 1px solid rgba(255,255,255,0.07);
}
.topbar-logo {
    font-family: 'Syne', sans-serif;
    font-size: 22px; font-weight: 800; color: #fff; letter-spacing: -0.5px;
}
.topbar-logo span { color: #00d4b4; }
.topbar-pills { display: flex; gap: 8px; }
.pill {
    font-family: 'Inter', sans-serif; font-size: 12px; font-weight: 600;
    letter-spacing: 1px; text-transform: uppercase;
    padding: 6px 16px; border-radius: 100px;
    border: 1px solid rgba(255,255,255,0.09); color: #4a5a6a;
}
.pill.active {
    background: rgba(0,212,180,0.1); border-color: rgba(0,212,180,0.35); color: #00d4b4;
}

/* ── HERO ── */
.hero { text-align: center; padding: 8px 0 28px; }
.hero-badge {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(0,212,180,0.08); border: 1px solid rgba(0,212,180,0.22);
    color: #00d4b4; font-family: 'IBM Plex Mono', monospace;
    font-size: 11px; font-weight: 500; letter-spacing: 2px; text-transform: uppercase;
    padding: 6px 16px; border-radius: 100px; margin-bottom: 20px;
}
.hero-badge::before {
    content: ''; width: 7px; height: 7px; border-radius: 50%;
    background: #00d4b4; animation: blink 2s ease-in-out infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.25} }

.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(36px, 3.8vw, 52px);   /* SMALLER — less imposing */
    font-weight: 800; line-height: 1.1; letter-spacing: -1.5px;
    color: #fff; margin-bottom: 14px;
}
.hero h1 em {
    font-style: normal;
    background: linear-gradient(120deg, #00d4b4 20%, #3b82f6 80%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.hero p {
    font-family: 'Inter', sans-serif;
    font-size: 15px; font-weight: 400; color: #5a6a7a;
    max-width: 460px; margin: 0 auto; line-height: 1.7;
}

/* ── STAT STRIP ── */
/* 4 equal tiles in a single bar — compact height, bigger text */
.stat-strip {
    display: grid;
    grid-template-columns: repeat(4, 1fr);  /* equal 4 columns */
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px; overflow: hidden;
    margin-bottom: 32px;
}
.stat-item {
    padding: 20px 24px;
    border-right: 1px solid rgba(255,255,255,0.07);
    display: flex; align-items: center; gap: 14px;
}
.stat-item:last-child { border-right: none; }
.stat-icon {
    width: 40px; height: 40px; border-radius: 10px; flex-shrink: 0;
    display: flex; align-items: center; justify-content: center; font-size: 17px;
}
.stat-icon.t { background:rgba(0,212,180,0.12); border:1px solid rgba(0,212,180,0.22); }
.stat-icon.b { background:rgba(59,130,246,0.12); border:1px solid rgba(59,130,246,0.22); }
.stat-icon.a { background:rgba(245,158,11,0.12);  border:1px solid rgba(245,158,11,0.22); }
.stat-val {
    font-family: 'Syne', sans-serif;
    font-size: 24px; font-weight: 800; line-height: 1.1;  /* BIGGER: was 20px */
}
.stat-val.t{color:#00d4b4} .stat-val.b{color:#60a5fa} .stat-val.a{color:#f59e0b}
.stat-lbl {
    font-family: 'Inter', sans-serif;
    font-size: 11px; font-weight: 600;                     /* BIGGER: was 10px */
    letter-spacing: 0.8px; text-transform: uppercase; color: #4a5a6a; margin-top: 3px;
}
.stat-delta {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px; color: #1d6a5a; margin-top: 2px;     /* BIGGER: was 9px */
}

/* ── SECTION LABEL ── */
.sec-label {
    font-family: 'Inter', sans-serif;
    font-size: 11px; font-weight: 600;
    letter-spacing: 2px; text-transform: uppercase; color: #3a4a5a;
    margin-bottom: 14px; display: flex; align-items: center; gap: 10px;
}
.sec-label::after { content:''; flex:1; height:1px; background:rgba(255,255,255,0.06); }

/* ── PANEL (dark-teal tinted, matches theme) ── */
.panel {
    background: rgba(0,20,18,0.6);
    border: 1px solid rgba(0,212,180,0.12);
    border-radius: 16px; padding: 22px 24px 16px; margin-bottom: 14px;
}
.panel-hd {
    font-family: 'Syne', sans-serif;
    font-size: 13px; font-weight: 700;                     /* BIGGER: was 12px */
    color: #00d4b4; letter-spacing: 0.5px;
    margin-bottom: 18px; display: flex; align-items: center; gap: 8px;
}

/* ── INPUT OVERRIDES ── all bumped up for readability ── */
.stNumberInput input {
    background: #0a1018 !important;
    border: 1px solid rgba(0,212,180,0.18) !important;
    border-radius: 10px !important;
    color: #c8dce8 !important;                             /* BRIGHTER text */
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 14px !important;                            /* BIGGER: was 13px */
    padding: 10px 14px !important; height: 42px !important;
}
.stNumberInput input:focus {
    border-color: rgba(0,212,180,0.5) !important;
    box-shadow: 0 0 0 2px rgba(0,212,180,0.08) !important; outline: none !important;
}
.stNumberInput label {
    color: #5a7a82 !important;                             /* more visible label */
    font-family: 'Inter', sans-serif !important;
    font-size: 12px !important;                            /* BIGGER: was 10px */
    font-weight: 600 !important; letter-spacing: 0.8px !important;
    text-transform: uppercase !important; margin-bottom: 4px !important;
}
.stNumberInput button {
    background: #0a1018 !important;
    border: 1px solid rgba(0,212,180,0.15) !important;
    color: #3a5a62 !important; border-radius: 8px !important;
}

.stSelectbox > div > div {
    background: #0a1018 !important;
    border: 1px solid rgba(0,212,180,0.18) !important;
    border-radius: 10px !important;
    color: #c8dce8 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 14px !important;                            /* BIGGER */
}
.stSelectbox label {
    color: #5a7a82 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 12px !important;                            /* BIGGER */
    font-weight: 600 !important; letter-spacing: 0.8px !important;
    text-transform: uppercase !important; margin-bottom: 4px !important;
}

.stSlider label {
    color: #5a7a82 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 12px !important;                            /* BIGGER: was 10px */
    font-weight: 600 !important; letter-spacing: 0.8px !important;
    text-transform: uppercase !important;
}
/* slider value shown next to knob */
[data-testid="stSlider"] p {
    color: #c8dce8 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 12px !important;
}
[data-baseweb="slider"] [role="slider"] {
    background: #00d4b4 !important;
    border: 2px solid #07090f !important;
    box-shadow: 0 0 10px rgba(0,212,180,0.45) !important;
}

/* ── BUTTON ── */
.stButton > button {
    width: 100% !important;
    background: linear-gradient(130deg, #00c4a7 0%, #2563eb 100%) !important;
    color: #000 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 15px !important; font-weight: 700 !important; letter-spacing: 1px !important;
    border: none !important; border-radius: 12px !important; height: 50px !important;
    box-shadow: 0 4px 24px rgba(0,196,167,0.22) !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    opacity: 0.88 !important; transform: translateY(-1px) !important;
    box-shadow: 0 8px 32px rgba(0,196,167,0.38) !important;
}

/* ── KPI ROW ── */
.kpi-row { display:flex; gap:10px; margin-bottom:14px; }
.kpi {
    flex:1; border-radius:12px; padding:16px 18px;
    background:rgba(255,255,255,0.03);
    border:1px solid rgba(255,255,255,0.08);
}
.kpi-label {
    font-family:'Inter',sans-serif; font-size:10px; font-weight:600;
    letter-spacing:1.5px; text-transform:uppercase; color:#3a4a5a; margin-bottom:6px;
}
.kpi-value {
    font-family:'Syne',sans-serif; font-size:22px; font-weight:800; color:#fff;
}
.kpi-value.green{color:#00d4b4} .kpi-value.red{color:#ef4444} .kpi-value.amber{color:#f59e0b}

.div { height:1px; background:rgba(255,255,255,0.06); margin:24px 0; }

/* ── fix plotly chart containers flushing to edge ── */
[data-testid="stPlotlyChart"] {
    border-radius: 12px; overflow: hidden;
}
</style>
""", unsafe_allow_html=True)

# ─── SHELL OPEN ───
st.markdown('<div class="shell">', unsafe_allow_html=True)

# ── TOPBAR ──
st.markdown("""
<div class="topbar">
    <div class="topbar-logo">Credit<span>Sense</span>
        <span style="font-size:12px;font-weight:500;color:#2a3a4a;letter-spacing:2px;margin-left:4px;">AI</span>
    </div>
    <div class="topbar-pills">
        <div class="pill active">Dashboard</div>
        <div class="pill">Reports</div>
        <div class="pill">History</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── HERO ──
st.markdown("""
<div class="hero">
    <div class="hero-badge">Model v2.1 · Live</div>
    <h1>Intelligent <em>Credit Risk Engine</em></h1>
    <p>Complete the customer profile on the left — risk verdict, gauge and charts appear instantly in the right panel.</p>
</div>
""", unsafe_allow_html=True)

# ── STAT STRIP ──
st.markdown("""
<div class="stat-strip">
    <div class="stat-item">
        <div class="stat-icon t">📊</div>
        <div>
            <div class="stat-val t">24,580</div>
            <div class="stat-lbl">Assessments</div>
            <div class="stat-delta">↑ +12% this month</div>
        </div>
    </div>
    <div class="stat-item">
        <div class="stat-icon b">✅</div>
        <div>
            <div class="stat-val b">78.7%</div>
            <div class="stat-lbl">Approval Rate</div>
            <div class="stat-delta">19,340 approved</div>
        </div>
    </div>
    <div class="stat-item">
        <div class="stat-icon a">⚡</div>
        <div>
            <div class="stat-val a">18%</div>
            <div class="stat-lbl">Avg Risk Index</div>
            <div class="stat-delta">Low default pool</div>
        </div>
    </div>
    <div class="stat-item">
        <div class="stat-icon t">🎯</div>
        <div>
            <div class="stat-val t">83%</div>
            <div class="stat-lbl">Model Accuracy</div>
            <div class="stat-delta">XGBoost · v2.1</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="div"></div>', unsafe_allow_html=True)

# ─── 3-COLUMN LAYOUT ───
# Streamlit columns inherit the shell's side margins automatically
col_L, col_M, col_R = st.columns([1, 1, 1.1], gap="medium")

# ════ LEFT ════
with col_L:
    st.markdown('<div class="sec-label">💳 Financial Profile</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel"><div class="panel-hd">◈ Credit &amp; Identity</div>', unsafe_allow_html=True)
    LIMIT_BAL = st.number_input("Credit Limit (NT$)", min_value=0.0, step=1000.0, format="%.0f", key="lb")
    AGE       = st.number_input("Customer Age", min_value=18, max_value=100, step=1, value=30, key="age")
    SEX       = st.selectbox("Gender", ["Male", "Female"], key="sex")
    EDUCATION = st.selectbox("Education Level", ["Graduate", "University", "High School", "Others"], key="edu")
    MARRIAGE  = st.selectbox("Marital Status", ["Single", "Married", "Others"], key="mar")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel"><div class="panel-hd">◈ Bill Statements</div>', unsafe_allow_html=True)
    BILL_AMT1 = st.number_input("Bill — Sep (NT$)", min_value=0.0, format="%.0f", key="b1")
    BILL_AMT2 = st.number_input("Bill — Aug (NT$)", min_value=0.0, format="%.0f", key="b2")
    BILL_AMT3 = st.number_input("Bill — Jul (NT$)",  min_value=0.0, format="%.0f", key="b3")
    st.markdown('</div>', unsafe_allow_html=True)

# ════ MIDDLE ════
with col_M:
    st.markdown('<div class="sec-label">💸 Payment History</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel"><div class="panel-hd">◈ Payments Made</div>', unsafe_allow_html=True)
    PAY_AMT1 = st.number_input("Payment — Sep (NT$)", min_value=0.0, format="%.0f", key="p1")
    PAY_AMT2 = st.number_input("Payment — Aug (NT$)", min_value=0.0, format="%.0f", key="p2")
    PAY_AMT3 = st.number_input("Payment — Jul (NT$)", min_value=0.0, format="%.0f", key="p3")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="panel"><div class="panel-hd">◈ Repayment Status</div>', unsafe_allow_html=True)
    st.markdown(
        '<p style="font-size:11px;color:#3a5060;font-family:Inter,sans-serif;'
        'margin-bottom:14px;line-height:1.6;">'
        '-2 = no usage &nbsp;·&nbsp; -1 = paid duly &nbsp;·&nbsp; 0 = minimum &nbsp;·&nbsp; 1–8 = months delayed'
        '</p>', unsafe_allow_html=True
    )
    PAY_0 = st.slider("September", -2, 8, 0, key="s0")
    PAY_2 = st.slider("August",    -2, 8, 0, key="s2")
    PAY_3 = st.slider("July",      -2, 8, 0, key="s3")
    PAY_4 = st.slider("June",      -2, 8, 0, key="s4")
    PAY_5 = st.slider("May",       -2, 8, 0, key="s5")
    PAY_6 = st.slider("April",     -2, 8, 0, key="s6")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    analyze = st.button("◈  Run Credit Analysis", key="analyze")

# ════ RIGHT: Live Results ════
with col_R:
    st.markdown('<div class="sec-label">📡 Live Risk Assessment</div>', unsafe_allow_html=True)

    if not analyze:
        # ── Idle placeholder ──
        st.markdown("""
        <div style="background:rgba(0,20,18,0.6);border:1px solid rgba(0,212,180,0.1);
                    border-radius:16px;padding:36px 28px;text-align:center;margin-bottom:14px;">
            <div style="font-family:'Inter',sans-serif;font-size:11px;font-weight:600;
                        letter-spacing:2px;color:#2a4a4a;text-transform:uppercase;margin-bottom:16px;">
                Awaiting Input
            </div>
            <div style="font-family:'Syne',sans-serif;font-size:60px;font-weight:800;
                        color:rgba(255,255,255,0.04);line-height:1;margin-bottom:18px;">--%</div>
            <div style="font-family:'Inter',sans-serif;font-size:13px;color:#2a4a4a;line-height:1.8;">
                Complete the customer profile<br>and click
                <strong style="color:#00d4b4;font-weight:600;">Run Credit Analysis</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # idle gauge
        fig_idle = go.Figure(go.Indicator(
            mode="gauge+number",
            value=0,
            number=dict(suffix="%", font=dict(family="Syne", size=28, color="rgba(255,255,255,0.08)")),
            title=dict(text="Risk Score", font=dict(family="Syne", size=13, color="#2a4a4a")),
            gauge=dict(
                axis=dict(range=[0,100], tickcolor="#111820",
                          tickfont=dict(color="#111820", size=10)),
                bar=dict(color="rgba(0,212,180,0.08)", thickness=0.6),
                bgcolor="rgba(255,255,255,0.015)", borderwidth=0,
                steps=[
                    dict(range=[0,30],   color="rgba(0,212,180,0.035)"),
                    dict(range=[30,60],  color="rgba(245,158,11,0.035)"),
                    dict(range=[60,100], color="rgba(239,68,68,0.035)"),
                ]
            )
        ))
        fig_idle.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", height=210,
            margin=dict(t=10,b=0,l=10,r=10)
        )
        st.plotly_chart(fig_idle, use_container_width=True)

    else:

        if LIMIT_BAL == 0:
            st.warning("Please enter customer credit limit.")
            st.stop()

        # ── COMPUTE ──
        sex_val = 1 if SEX == "Male" else 2
        edu_val = {"Graduate":1,"University":2,"High School":3,"Others":4}[EDUCATION]
        mar_val = {"Married":1,"Single":2,"Others":3}[MARRIAGE]

        features = np.array([[
            LIMIT_BAL, sex_val, edu_val, mar_val, AGE,
            PAY_0, PAY_2, PAY_3, PAY_4, PAY_5, PAY_6,
            BILL_AMT1, BILL_AMT2, BILL_AMT3, 0, 0, 0,
            PAY_AMT1, PAY_AMT2, PAY_AMT3, 0, 0, 0
        ]], dtype=float)

        pred     = model.predict(features)[0]
        prob     = model.predict_proba(features)
        risk_pct = prob[0][1] * 100
        conf_pct = 100 - risk_pct

        util_ratio = (BILL_AMT1 / LIMIT_BAL * 100) if LIMIT_BAL > 0 else 0
        avg_bill   = (BILL_AMT1 + BILL_AMT2 + BILL_AMT3) / 3
        avg_pay    = (PAY_AMT1  + PAY_AMT2  + PAY_AMT3)  / 3
        pay_ratio  = (avg_pay / avg_bill * 100) if avg_bill > 0 else 100

        # ── GAUGE ──
        gc = "#ef4444" if risk_pct > 60 else "#f59e0b" if risk_pct > 30 else "#00d4b4"
        fig_g = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk_pct,
            number=dict(suffix="%", font=dict(family="Syne", size=34, color="#e8ecf4")),
            title=dict(text="Default Risk Score", font=dict(family="Syne", size=13, color="#5a6a7a")),
            gauge=dict(
                axis=dict(range=[0,100], tickwidth=1, tickcolor="#1a2030",
                          tickfont=dict(color="#2d4050", size=10),
                          tickvals=[0,30,60,100]),
                bar=dict(color=gc, thickness=0.65),
                bgcolor="rgba(255,255,255,0.02)", borderwidth=0,
                steps=[
                    dict(range=[0,30],   color="rgba(0,212,180,0.08)"),
                    dict(range=[30,60],  color="rgba(245,158,11,0.08)"),
                    dict(range=[60,100], color="rgba(239,68,68,0.08)"),
                ],
                threshold=dict(line=dict(color=gc,width=3), thickness=0.85, value=risk_pct)
            )
        ))
        fig_g.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", height=210,
            margin=dict(t=10,b=0,l=10,r=10)
        )
        st.plotly_chart(fig_g, use_container_width=True)

        # ── VERDICT ──
        if pred == 0:
            st.markdown(f"""
            <div style="background:rgba(0,212,180,0.07);border:1px solid rgba(0,212,180,0.2);
                        border-radius:14px;padding:22px 24px;margin-bottom:12px;">
                <div style="font-family:'Syne',sans-serif;font-size:26px;font-weight:800;
                            color:#00d4b4;margin-bottom:6px;">✓ Creditworthy</div>
                <div style="font-family:'Inter',sans-serif;font-size:13px;color:#5a7a7a;margin-bottom:14px;">
                    Approval confidence: <strong style="color:#00d4b4;font-size:15px;">{conf_pct:.1f}%</strong>
                    &nbsp;·&nbsp; Default risk: {risk_pct:.1f}%
                </div>
                <div style="background:rgba(255,255,255,0.06);border-radius:100px;
                            height:5px;overflow:hidden;margin-bottom:14px;">
                    <div style="width:{conf_pct:.1f}%;height:100%;border-radius:100px;
                                background:linear-gradient(90deg,#00d4b4,#3b82f6);"></div>
                </div>
                <div style="font-family:'Inter',sans-serif;font-size:13px;
                            color:#3a6060;line-height:1.65;">
                    Consistent repayment behavior detected. Strong candidate for credit approval.
                </div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background:rgba(239,68,68,0.07);border:1px solid rgba(239,68,68,0.2);
                        border-radius:14px;padding:22px 24px;margin-bottom:12px;">
                <div style="font-family:'Syne',sans-serif;font-size:26px;font-weight:800;
                            color:#ef4444;margin-bottom:6px;">⚠ High Risk</div>
                <div style="font-family:'Inter',sans-serif;font-size:13px;color:#7a5a5a;margin-bottom:14px;">
                    Default probability: <strong style="color:#ef4444;font-size:15px;">{risk_pct:.1f}%</strong>
                    &nbsp;·&nbsp; Approval confidence: {conf_pct:.1f}%
                </div>
                <div style="background:rgba(255,255,255,0.06);border-radius:100px;
                            height:5px;overflow:hidden;margin-bottom:14px;">
                    <div style="width:{risk_pct:.1f}%;height:100%;border-radius:100px;
                                background:linear-gradient(90deg,#f59e0b,#ef4444);"></div>
                </div>
                <div style="font-family:'Inter',sans-serif;font-size:13px;
                            color:#5a3030;line-height:1.65;">
                    Repayment delays detected across multiple months. Manual review recommended.
                </div>
            </div>""", unsafe_allow_html=True)

        # ── KPIs ──
        ur_c = "red"   if util_ratio > 75 else "amber" if util_ratio > 40 else "green"
        pr_c = "green" if pay_ratio  > 80 else "amber" if pay_ratio  > 40 else "red"
        st.markdown(f"""
        <div class="kpi-row">
            <div class="kpi">
                <div class="kpi-label">Credit Util.</div>
                <div class="kpi-value {ur_c}">{util_ratio:.0f}%</div>
            </div>
            <div class="kpi">
                <div class="kpi-label">Pay / Bill</div>
                <div class="kpi-value {pr_c}">{pay_ratio:.0f}%</div>
            </div>
            <div class="kpi">
                <div class="kpi-label">Avg Bill</div>
                <div class="kpi-value" style="font-size:18px;color:#c8dce8;">
                    NT${avg_bill:,.0f}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── BILLS vs PAYMENTS CHART ──
        months = ["Apr","May","Jun","Jul","Aug","Sep"]
        bill_s = [0, 0, 0, BILL_AMT3, BILL_AMT2, BILL_AMT1]
        pay_s  = [0, 0, 0, PAY_AMT3,  PAY_AMT2,  PAY_AMT1]

        CL = dict(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=32,b=16,l=4,r=4), height=148,
            font=dict(family="Inter", color="#3a5060", size=10),
            xaxis=dict(showgrid=False, zeroline=False,
                       tickfont=dict(size=10, color="#3a5060")),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)",
                       zeroline=False, tickfont=dict(size=9, color="#3a5060")),
            legend=dict(font=dict(size=10, color="#5a7a7a"), bgcolor="rgba(0,0,0,0)",
                        x=0, y=1.18, orientation="h"),
            title_font=dict(family="Syne", size=12, color="#5a7a82"),
        )

        fig_c = go.Figure()
        fig_c.add_trace(go.Scatter(
            x=months, y=bill_s, name="Bills",
            mode="lines+markers",
            line=dict(color="rgba(59,130,246,0.8)", width=2),
            marker=dict(size=5, color="#3b82f6"),
            fill="tozeroy", fillcolor="rgba(59,130,246,0.06)"
        ))
        fig_c.add_trace(go.Scatter(
            x=months, y=pay_s, name="Payments",
            mode="lines+markers",
            line=dict(color="#00d4b4", width=2, dash="dot"),
            marker=dict(size=5, color="#00d4b4"),
        ))
        fig_c.update_layout(**CL, title="Bills vs Payments")
        st.plotly_chart(fig_c, use_container_width=True)

        # ── REPAYMENT HEATMAP ──
        pay_statuses = [PAY_6, PAY_5, PAY_4, PAY_3, PAY_2, PAY_0]
        heat_colors  = ["#ef4444" if p > 0 else "#f59e0b" if p == 0 else "#00d4b4"
                        for p in pay_statuses]
        fig_h = go.Figure(go.Bar(
            x=months, y=[1]*6,
            marker=dict(color=heat_colors, line=dict(width=0)),
            text=[str(p) for p in pay_statuses],
            textposition="inside",
            textfont=dict(family="IBM Plex Mono", size=11, color="#07090f"),
            hovertemplate="%{x}: status %{text}<extra></extra>"
        ))
        fig_h.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=32,b=16,l=4,r=4), height=88,
            title="Repayment Status Heatmap",
            title_font=dict(family="Syne", size=12, color="#5a7a82"),
            xaxis=dict(showgrid=False, tickfont=dict(size=10, color="#3a5060")),
            yaxis=dict(visible=False), showlegend=False,
        )
        st.plotly_chart(fig_h, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)


st.markdown("""
<div style="
text-align:center;
padding:30px 0 10px;
color:#3a5060;
font-size:12px;
font-family:Inter,sans-serif;
">
Built with Streamlit · Machine Learning · Plotly · XGBoost
</div>
""", unsafe_allow_html=True)