import streamlit as st
import joblib
import numpy as np

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="AI Credit Risk Dashboard",
    page_icon="💳",
    layout="wide"
)

# =========================================
# LOAD MODEL
# =========================================

model = joblib.load("credit_model.pkl")

# =========================================
# CUSTOM CSS
# =========================================

st.markdown("""
<style>

/* Main Background */
[data-testid="stAppViewContainer"]{
    background: linear-gradient(
        135deg,
        #0f0c29,
        #302b63,
        #24243e
    );
    color: white;
}

/* Remove Streamlit Header */
[data-testid="stHeader"]{
    background: rgba(0,0,0,0);
}

/* Main Layout */
.block-container{
    padding-top: 2rem;
    padding-left: 8%;
    padding-right: 8%;
    max-width: 1400px;
    margin: auto;
}

/* Main Title */
.main-title{
    font-size: 60px;
    font-weight: 800;
    text-align: center;
    color: white;
    margin-bottom: 10px;
}

/* Subtitle */
.sub-title{
    text-align: center;
    color: #d1d1d1;
    font-size: 22px;
    margin-bottom: 40px;
}

/* Glass Card */
.glass-card{
    background: rgba(255,255,255,0.06);
    padding: 28px;
    border-radius: 24px;
    backdrop-filter: blur(18px);
    border: 1px solid rgba(255,255,255,0.10);
    box-shadow: 0 8px 40px rgba(0,0,0,0.35);
    margin-bottom: 24px;
}

/* Inputs */
.stNumberInput input{
    background-color: rgba(255,255,255,0.12) !important;
    color: #ffffff !important;
    border-radius: 14px !important;
    border: 1px solid rgba(255,255,255,0.18) !important;
    height: 52px !important;
    font-size: 18px !important;
    font-weight: 600 !important;
}

/* Placeholder */
.stNumberInput input::placeholder{
    color: #dcdcdc !important;
    opacity: 1 !important;
}

/* Labels */
.stNumberInput label,
.stSelectbox label,
.stSlider label{
    color: white !important;
    font-weight: 600 !important;
}

/* Selectbox */
.stSelectbox div[data-baseweb="select"]{
    background-color: rgba(255,255,255,0.08) !important;
    border-radius: 14px !important;
}

/* Button */
.stButton button{
    width: 100%;
    height: 60px;
    border-radius: 16px;
    border: none;
    background: linear-gradient(
        90deg,
        #8e2de2,
        #4a00e0
    );
    color: white;
    font-size: 22px;
    font-weight: bold;
    transition: 0.3s;
    margin-top: 20px;
}

.stButton button:hover{
    transform: scale(1.02);
    background: linear-gradient(
        90deg,
        #ff0080,
        #7928ca
    );
}

/* Slider */
.stSlider{
    padding-top: 10px;
    padding-bottom: 10px;
}

/* Slider line */
.stSlider [data-baseweb="slider"] > div > div{
    background-color: #6c63ff !important;
}

/* Slider knob */
.stSlider [role="slider"]{
    background-color: #00f5ff !important;
    border: 2px solid white !important;
}

/* Slider value */
.stSlider span{
    color: #ffffff !important;
    font-weight: bold !important;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# TITLE SECTION
# =========================================

st.markdown("""
<div class="main-title">
    💳 AI Credit Risk Dashboard
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="sub-title">
    Modern Financial Risk Analysis System
</div>
""", unsafe_allow_html=True)

# =========================================
# DASHBOARD CARDS
# =========================================

card1, card2, card3 = st.columns(3)

with card1:
    st.markdown("""
    <div class="glass-card">
        <h3 style="color:white;">💰 Total Applications</h3>
        <h1 style="color:#00f5ff;">24,580</h1>
        <p style="color:#cfcfcf;">+12% this month</p>
    </div>
    """, unsafe_allow_html=True)

with card2:
    st.markdown("""
    <div class="glass-card">
        <h3 style="color:white;">⚠️ Risk Rate</h3>
        <h1 style="color:#ff4b91;">18%</h1>
        <p style="color:#cfcfcf;">Low default probability</p>
    </div>
    """, unsafe_allow_html=True)

with card3:
    st.markdown("""
    <div class="glass-card">
        <h3 style="color:white;">✅ Approved Clients</h3>
        <h1 style="color:#7dff72;">19,340</h1>
        <p style="color:#cfcfcf;">Strong customer profile</p>
    </div>
    """, unsafe_allow_html=True)

# =========================================
# SECTION HEADER
# =========================================

st.markdown("""
<div class="glass-card">
    <h2 style="
        color:white;
        text-align:center;
        margin:0;
    ">
        Customer Financial Information
    </h2>
</div>
""", unsafe_allow_html=True)

# =========================================
# INPUT SECTION
# =========================================

st.markdown(
    '<div class="glass-card">',
    unsafe_allow_html=True
)

left_col, right_col = st.columns(2)

# =========================================
# LEFT PANEL
# =========================================

with left_col:

    st.markdown("""
    <h2 style="
        color:white;
        margin-bottom:25px;
    ">
        💳 Financial Profile
    </h2>
    """, unsafe_allow_html=True)

    LIMIT_BAL = st.number_input(
        "Credit Limit",
        min_value=0.0,
        step=1000.0
    )

    AGE = st.number_input(
        "Age",
        min_value=18,
        max_value=100,
        step=1
    )

    BILL_AMT1 = st.number_input(
        "Bill Amount 1",
        min_value=0.0
    )

    BILL_AMT2 = st.number_input(
        "Bill Amount 2",
        min_value=0.0
    )

    BILL_AMT3 = st.number_input(
        "Bill Amount 3",
        min_value=0.0
    )

    PAY_AMT1 = st.number_input(
        "Payment Amount 1",
        min_value=0.0
    )

    PAY_AMT2 = st.number_input(
        "Payment Amount 2",
        min_value=0.0
    )

    PAY_AMT3 = st.number_input(
        "Payment Amount 3",
        min_value=0.0
    )

# =========================================
# RIGHT PANEL
# =========================================

with right_col:

    st.markdown("""
    <h2 style="
        color:white;
        margin-bottom:25px;
    ">
        🧠 Behavioral Analysis
    </h2>
    """, unsafe_allow_html=True)

    SEX = st.selectbox(
        "Gender",
        ["Male", "Female"]
    )

    EDUCATION = st.selectbox(
        "Education Level",
        [
            "Graduate",
            "University",
            "High School",
            "Others"
        ]
    )

    MARRIAGE = st.selectbox(
        "Marital Status",
        [
            "Single",
            "Married",
            "Others"
        ]
    )

    PAY_0 = st.slider("Repayment Status 0", -2, 8, 0)
    PAY_2 = st.slider("Repayment Status 2", -2, 8, 0)
    PAY_3 = st.slider("Repayment Status 3", -2, 8, 0)
    PAY_4 = st.slider("Repayment Status 4", -2, 8, 0)
    PAY_5 = st.slider("Repayment Status 5", -2, 8, 0)
    PAY_6 = st.slider("Repayment Status 6", -2, 8, 0)

st.markdown(
    '</div>',
    unsafe_allow_html=True
)

# =========================================
# BUTTON
# =========================================

st.markdown("<br><br>", unsafe_allow_html=True)

predict = st.button("Analyze Credit Risk")

# =========================================
# PREDICTION
# =========================================

if predict:

    sex_value = 1 if SEX == "Male" else 2

    education_value = (
        1 if EDUCATION == "Graduate"
        else 2 if EDUCATION == "University"
        else 3 if EDUCATION == "High School"
        else 4
    )

    marriage_value = (
        1 if MARRIAGE == "Married"
        else 2 if MARRIAGE == "Single"
        else 3
    )

    features = np.array([[

        LIMIT_BAL,
        sex_value,
        education_value,
        marriage_value,
        AGE,

        PAY_0,
        PAY_2,
        PAY_3,
        PAY_4,
        PAY_5,
        PAY_6,

        BILL_AMT1,
        BILL_AMT2,
        BILL_AMT3,

        0,
        0,
        0,

        PAY_AMT1,
        PAY_AMT2,
        PAY_AMT3,

        0,
        0,
        0

    ]], dtype=float)

    prediction = model.predict(features)

    probability = model.predict_proba(features)

    risk_score = probability[0][1] * 100

    st.markdown("<br>", unsafe_allow_html=True)

    # =====================================
    # HIGH RISK
    # =====================================

    if prediction[0] == 1:

        st.markdown(f"""
        <div class="glass-card">
            <h1 style="
                color:#ff4b91;
                text-align:center;
            ">
                ⚠️ High Credit Risk
            </h1>

            <h2 style="
                color:white;
                text-align:center;
            ">
                Risk Probability:
                {risk_score:.2f}%
            </h2>

            <p style="
                color:#d3d3d3;
                text-align:center;
                font-size:18px;
            ">
                This customer has a high probability
                of default payment.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # =====================================
    # LOW RISK
    # =====================================

    else:

        st.markdown(f"""
        <div class="glass-card">
            <h1 style="
                color:#00ff9f;
                text-align:center;
            ">
                ✅ Creditworthy Customer
            </h1>

            <h2 style="
                color:white;
                text-align:center;
            ">
                Approval Confidence:
                {100-risk_score:.2f}%
            </h2>

            <p style="
                color:#d3d3d3;
                text-align:center;
                font-size:18px;
            ">
                Customer shows strong financial reliability.
            </p>
        </div>
        """, unsafe_allow_html=True)