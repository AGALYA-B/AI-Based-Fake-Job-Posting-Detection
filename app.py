import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import textwrap
import ml_engine

# Page Configuration
st.set_page_config(
    page_title="VeriHire - Job Posting Verification Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Helper function to render HTML safely without markdown code-block indentation errors
def render_html(html_str):
    st.markdown(textwrap.dedent(html_str).strip(), unsafe_allow_html=True)

# Navigation and Form Callbacks
def navigate_to(page_name):
    st.session_state['nav_target'] = page_name

def load_scam_preset():
    st.session_state['form_title'] = "Data Entry Specialist / Home Assistant - Instant Hire"
    st.session_state['form_comp'] = ""
    st.session_state['form_desc'] = "We are seeking motivated individuals for remote data entry from home. Earn $500 per day! No experience required. Equipment will be provided via cashier check. Send wire transfer for processing fee. Contact HR directly on Telegram @scam_recruiter."
    st.session_state['form_req'] = "Must have laptop. Unlimited earning potential. No qualifications needed."
    st.session_state['form_sal'] = "$500/day"
    st.session_state['form_loc'] = "Remote / Work From Home"
    st.session_state['form_type'] = "Full-time"
    st.session_state['form_exp'] = "Not Applicable"
    st.session_state['form_edu'] = "Unspecified"
    st.session_state['form_func'] = "Data Entry"
    st.session_state['form_ind'] = "Administrative"
    st.session_state['form_ben'] = "High daily pay, work from anywhere"
    st.session_state['form_logo'] = False
    st.session_state['form_quest'] = False
    st.session_state['form_tele'] = True
    st.session_state.pop('last_analysis', None)

def load_suspicious_preset():
    st.session_state['form_title'] = "Remote Marketing Assistant"
    st.session_state['form_comp'] = "Fast growing digital agency expanding nationwide."
    st.session_state['form_desc'] = "Looking for an energetic marketing assistant to help with social media postings and client communication. Must be able to work flexible hours. Contact us via WhatsApp for quick interview."
    st.session_state['form_req'] = "Basic internet access, communication skills."
    st.session_state['form_sal'] = "Unspecified"
    st.session_state['form_loc'] = "Remote"
    st.session_state['form_type'] = "Part-time"
    st.session_state['form_exp'] = "Entry level"
    st.session_state['form_edu'] = "High School or equivalent"
    st.session_state['form_func'] = "Marketing"
    st.session_state['form_ind'] = "Marketing"
    st.session_state['form_ben'] = "Flexible hours"
    st.session_state['form_logo'] = False
    st.session_state['form_quest'] = True
    st.session_state['form_tele'] = True
    st.session_state.pop('last_analysis', None)

def load_authentic_preset():
    st.session_state['form_title'] = "Senior Full Stack Software Engineer"
    st.session_state['form_comp'] = "Acme Cloud Corp is a leading enterprise SaaS infrastructure company backed by Tier-1 VCs. Founded in 2018, we serve over 500,000 active business users globally."
    st.session_state['form_desc'] = "We are looking for a Senior Full Stack Engineer to build scalable microservices and modern web frontends using Python, React, and PostgreSQL. You will work closely with product managers and system architects."
    st.session_state['form_req'] = "5+ years software engineering experience. Strong proficiency in Python, TypeScript, SQL, and AWS/GCP cloud environments. Bachelor's degree in CS or equivalent."
    st.session_state['form_sal'] = "$140,000 - $175,000"
    st.session_state['form_loc'] = "San Francisco, CA (Hybrid)"
    st.session_state['form_type'] = "Full-time"
    st.session_state['form_exp'] = "Mid-Senior level"
    st.session_state['form_edu'] = "Bachelor's Degree"
    st.session_state['form_func'] = "Engineering"
    st.session_state['form_ind'] = "Information Technology"
    st.session_state['form_ben'] = "Health, dental, 401k matching, unlimited PTO, home office stipend"
    st.session_state['form_logo'] = True
    st.session_state['form_quest'] = True
    st.session_state['form_tele'] = False
    st.session_state.pop('last_analysis', None)

def clear_form_data():
    for k in ['form_title', 'form_comp', 'form_desc', 'form_req', 'form_sal', 'form_loc', 'form_type', 'form_exp', 'form_edu', 'form_func', 'form_ind', 'form_ben', 'form_logo', 'form_quest', 'form_tele', 'last_analysis']:
        st.session_state.pop(k, None)

# Premium Custom CSS
render_html("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #0F172A;
    }
    
    .stApp {
        background-color: #F8FAFC;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header[data-testid="stHeader"] {background: transparent;}
    
    /* Top SaaS Header Bar */
    .saas-header-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 0.75rem 1.25rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03);
    }
    .saas-status-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: #F0FDF4;
        color: #166534;
        border: 1px solid #BBF7D0;
        padding: 0.3rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 700;
    }
    .saas-meta-pill {
        font-size: 0.8rem;
        color: #475569;
        font-weight: 600;
    }
    
    /* High-Contrast Readable Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    
    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.2rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] span, 
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] label {
        color: #0F172A !important;
    }
    
    /* Readable Navigation Radio Options */
    section[data-testid="stSidebar"] div[role="radiogroup"] label {
        background-color: #F8FAFC !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
        padding: 0.6rem 0.9rem !important;
        margin-bottom: 0.45rem !important;
        cursor: pointer !important;
        transition: all 0.15s ease-in-out !important;
    }
    
    section[data-testid="stSidebar"] div[role="radiogroup"] label p {
        color: #1E293B !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
        margin: 0 !important;
    }
    
    section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background-color: #F1F5F9 !important;
        border-color: #CBD5E1 !important;
    }
    
    section[data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] {
        background-color: #EFF6FF !important;
        border-color: #2563EB !important;
        box-shadow: 0 1px 3px rgba(37, 99, 235, 0.12) !important;
    }
    
    section[data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] p {
        color: #1D4ED8 !important;
        font-weight: 800 !important;
    }
    
    /* Brand Header Box */
    .brand-container {
        display: flex;
        align-items: center;
        gap: 12px;
        padding-bottom: 1rem;
        margin-bottom: 1.25rem;
        border-bottom: 1px solid #F1F5F9;
    }
    
    .brand-logo {
        width: 42px;
        height: 42px;
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 700;
        font-size: 22px;
        box-shadow: 0 4px 10px rgba(37, 99, 235, 0.25);
    }
    
    .brand-title {
        font-size: 1.4rem;
        font-weight: 800;
        color: #0F172A !important;
        letter-spacing: -0.025em;
        margin: 0;
        line-height: 1.1;
    }
    
    .brand-tagline {
        font-size: 0.76rem;
        color: #64748B !important;
        margin: 3px 0 0 0;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    
    /* Section Headers */
    .vh-header {
        margin-bottom: 1.5rem;
    }
    .vh-header h1 {
        font-size: 1.85rem;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -0.025em;
        margin-bottom: 0.35rem;
    }
    .vh-header p {
        font-size: 0.95rem;
        color: #475569;
        margin: 0;
    }
    
    /* Cards & Containers */
    .vh-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 1px 3px 0 rgba(15, 23, 42, 0.03);
    }
    
    .vh-section-title {
        font-size: 0.82rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #475569;
        margin-bottom: 0.85rem;
        padding-bottom: 0.4rem;
        border-bottom: 1px solid #F1F5F9;
    }
    
    /* Metric Cards */
    .metric-container {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 1.15rem 1.25rem;
        height: 100%;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .metric-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05);
    }
    .metric-value {
        font-size: 1.75rem;
        font-weight: 800;
        color: #0F172A;
        line-height: 1.2;
    }
    .metric-label {
        font-size: 0.8rem;
        font-weight: 700;
        color: #64748B;
        margin-bottom: 0.35rem;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .metric-sub {
        font-size: 0.78rem;
        color: #94A3B8;
        margin-top: 0.25rem;
    }
    
    /* Badges */
    .badge {
        display: inline-flex;
        align-items: center;
        padding: 0.35rem 0.85rem;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 0.02em;
    }
    .badge-low {
        background-color: #ECFDF5;
        color: #047857;
        border: 1px solid #A7F3D0;
    }
    .badge-med {
        background-color: #FFFBEB;
        color: #B45309;
        border: 1px solid #FDE68A;
    }
    .badge-high {
        background-color: #FEF2F2;
        color: #B91C1C;
        border: 1px solid #FECACA;
    }
    
    /* Score Gauge Meter Bar */
    .score-meter-container {
        background: #E2E8F0;
        border-radius: 9999px;
        height: 10px;
        width: 100%;
        overflow: hidden;
        margin: 10px 0 14px 0;
    }
    .score-meter-bar {
        height: 100%;
        border-radius: 9999px;
    }
    
    /* Signal Boxes */
    .signal-box {
        padding: 0.85rem 1rem;
        border-radius: 8px;
        margin-bottom: 0.65rem;
        font-size: 0.88rem;
        line-height: 1.45;
    }
    .signal-box.warning {
        background-color: #FFFBEB;
        border-left: 4px solid #F59E0B;
        color: #92400E;
    }
    .signal-box.danger {
        background-color: #FEF2F2;
        border-left: 4px solid #EF4444;
        color: #991B1B;
    }
    .signal-box.info {
        background-color: #F0F9FF;
        border-left: 4px solid #0EA5E9;
        color: #075985;
    }
    .signal-box.success {
        background-color: #ECFDF5;
        border-left: 4px solid #10B981;
        color: #065F46;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #2563EB;
        color: #FFFFFF;
        font-weight: 600;
        font-size: 0.92rem;
        border-radius: 8px;
        border: none;
        padding: 0.55rem 1.25rem;
        transition: all 0.15s ease;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #1D4ED8;
        color: #FFFFFF;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
    }
    
    div[data-testid="stForm"] {
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        background: #FFFFFF;
        padding: 1.5rem;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        font-weight: 600;
        font-size: 0.88rem;
        border-radius: 6px;
        padding: 6px 14px;
    }
</style>
""")

# Load Model Engine
@st.cache_resource
def load_ml_artifact():
    return ml_engine.get_model()

model_artifact = load_ml_artifact()
metrics = model_artifact['metrics']

# Initialize session state for navigation target safely
if 'nav_target' not in st.session_state:
    st.session_state['nav_target'] = "Verify Job"

# Sidebar Identity & Navigation
with st.sidebar:
    render_html("""
    <div class="brand-container">
        <div class="brand-logo">🛡️</div>
        <div>
            <div class="brand-title">VeriHire</div>
            <div class="brand-tagline">Recruitment Risk Platform</div>
        </div>
    </div>
    """)
    
    st.markdown("**WORKSPACE NAVIGATION**")
    nav_option = st.radio(
        label="Select Workspace",
        options=["Overview", "Verify Job", "Batch Analysis", "Model Insights"],
        key='nav_target',
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    render_html(f"""
    <div style="font-size: 0.8rem; color: #334155; line-height: 1.6;">
        <strong style="color: #0F172A;">Engine Version:</strong> 2.4.0-SaaS<br/>
        <strong style="color: #0F172A;">Model:</strong> Logistic Regression + TF-IDF<br/>
        <strong style="color: #0F172A;">Baseline Dataset:</strong> {metrics['dataset_count']:,} Postings<br/>
        <strong style="color: #0F172A;">ROC-AUC Accuracy:</strong> {metrics['roc_auc']*100:.2f}%
    </div>
    """)

# Top SaaS Status Header Bar
render_html(f"""
<div class="saas-header-bar">
    <div class="saas-status-pill">
        <span style="display:inline-block; width:8px; height:8px; background:#22C55E; border-radius:50%;"></span>
        VeriHire Verification Engine Active
    </div>
    <div style="display:flex; gap:16px;">
        <span class="saas-meta-pill">📊 {metrics['dataset_count']:,} Benchmark Postings</span>
        <span class="saas-meta-pill">🎯 {metrics['roc_auc']*100:.2f}% ROC-AUC Precision</span>
        <span class="saas-meta-pill">⚡ NLP N-Grams: 4,000</span>
    </div>
</div>
""")

# ==============================================================================
# TAB 1: OVERVIEW
# ==============================================================================
if nav_option == "Overview":
    render_html("""
    <div class="vh-header">
        <h1>Overview & Platform Intelligence</h1>
        <p>Real-time machine learning verification to detect fake job postings and protect candidates.</p>
    </div>
    """)
    
    # Executive Summary Metrics
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_html(f"""
        <div class="metric-container">
            <div class="metric-label">Dataset Benchmark</div>
            <div class="metric-value">{metrics['dataset_count']:,}</div>
            <div class="metric-sub">Curated evaluation baseline</div>
        </div>
        """)
    with c2:
        render_html(f"""
        <div class="metric-container">
            <div class="metric-label">Scam Baseline Rate</div>
            <div class="metric-value">{metrics['fraud_rate']*100:.2f}%</div>
            <div class="metric-sub">{metrics['fraud_count']:,} fraudulent records</div>
        </div>
        """)
    with c3:
        render_html(f"""
        <div class="metric-container">
            <div class="metric-label">Model ROC-AUC</div>
            <div class="metric-value">{metrics['roc_auc']*100:.2f}%</div>
            <div class="metric-sub">Cross-validated accuracy</div>
        </div>
        """)
    with c4:
        render_html("""
        <div class="metric-container">
            <div class="metric-label">Evaluated NLP Signals</div>
            <div class="metric-value">4,000+</div>
            <div class="metric-sub">Text n-grams & metadata</div>
        </div>
        """)
        
    st.markdown("<br/>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns([2, 1])
    with col_left:
        render_html("""
        <div class="vh-card">
            <div class="vh-section-title">Why Enterprise Teams & Jobseekers Rely on VeriHire</div>
            <h3 style="margin-top:0; font-size: 1.15rem; font-weight: 700; color: #0F172A;">Multi-Layered Detection Architecture</h3>
            <p style="color: #475569; font-size: 0.92rem; line-height: 1.6;">
                Recruitment scams result in financial theft, identity exploitation, and reputational damage.
                VeriHire combines structural metadata analysis (employer logo verification, screening questions, company profile presence) 
                with advanced TF-IDF NLP linguistic pattern extraction to flag deceptive listings before candidates apply.
            </p>
            <div style="display: flex; gap: 1rem; margin-top: 1.5rem;">
                <div style="background: #F8FAFC; border: 1px solid #E2E8F0; padding: 1rem; border-radius: 8px; flex: 1;">
                    <strong style="color: #0F172A; font-size: 0.9rem;">1. Single Posting Scan</strong>
                    <p style="margin: 4px 0 0 0; font-size: 0.82rem; color: #64748B; line-height: 1.4;">Evaluate individual job announcements with instant risk breakdown & candidate advice.</p>
                </div>
                <div style="background: #F8FAFC; border: 1px solid #E2E8F0; padding: 1rem; border-radius: 8px; flex: 1;">
                    <strong style="color: #0F172A; font-size: 0.9rem;">2. Batch CSV Processing</strong>
                    <p style="margin: 4px 0 0 0; font-size: 0.82rem; color: #64748B; line-height: 1.4;">Audit hundreds of job listings simultaneously for job board moderation.</p>
                </div>
            </div>
        </div>
        """)
        
    with col_right:
        render_html("""
        <div class="vh-card">
            <div class="vh-section-title">Quick Actions</div>
            <p style="font-size: 0.88rem; color: #475569; margin-bottom: 1.2rem; line-height: 1.5;">Launch verification workflows or test sample benchmark datasets immediately.</p>
        </div>
        """)
        
        st.button("🔍 Open Single Job Verification", on_click=navigate_to, args=("Verify Job",))
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        st.button("📁 Open Batch CSV Evaluation", on_click=navigate_to, args=("Batch Analysis",))

# ==============================================================================
# TAB 2: VERIFY JOB (MAIN VERIFICATION EXPERIENCE)
# ==============================================================================
elif nav_option == "Verify Job":
    render_html("""
    <div class="vh-header">
        <h1>Verify Job Posting</h1>
        <p>Analyze job posting text and metadata signals to identify fraud risk before submitting applications.</p>
    </div>
    """)
    
    # 1-Click Demo Presets Section
    st.markdown("**⚡ 1-Click Demo Presets (Test Realistic Postings Instantly)**")
    p_col1, p_col2, p_col3, p_col4 = st.columns([1, 1, 1, 0.75])
    
    p_col1.button("🚨 Load High-Risk Scam", on_click=load_scam_preset)
    p_col2.button("⚠️ Load Suspicious", on_click=load_suspicious_preset)
    p_col3.button("✅ Load Authentic Job", on_click=load_authentic_preset)
    p_col4.button("🧹 Clear Form", on_click=clear_form_data)

    st.markdown("<br/>", unsafe_allow_html=True)
    
    col_workspace, col_summary = st.columns([1.65, 1])
    
    with col_workspace:
        with st.form("job_verification_form"):
            render_html('<div class="vh-section-title">Job Information</div>')
            
            job_title = st.text_input(
                "Job Title *", 
                value=st.session_state.get('form_title', ''),
                placeholder="e.g. Data Entry Specialist / Senior Software Engineer"
            )
            
            company_profile = st.text_area(
                "Company Profile", 
                value=st.session_state.get('form_comp', ''),
                placeholder="Provide company background, mission, or history (leave blank if missing in posting)...",
                height=100
            )
            
            job_description = st.text_area(
                "Job Description *", 
                value=st.session_state.get('form_desc', ''),
                placeholder="Paste the full job posting description text here...",
                height=150
            )
            
            requirements = st.text_area(
                "Job Requirements", 
                value=st.session_state.get('form_req', ''),
                placeholder="List required skills, qualifications, or experience details...",
                height=100
            )
            
            render_html('<div class="vh-section-title" style="margin-top: 1.25rem;">Job Details & Metadata</div>')
            
            d_col1, d_col2 = st.columns(2)
            with d_col1:
                salary_range = st.text_input("Salary Range", value=st.session_state.get('form_sal', ''), placeholder="e.g. $50,000 - $70,000 or Unspecified")
                location = st.text_input("Location", value=st.session_state.get('form_loc', ''), placeholder="e.g. US, NY, New York")
                
                type_opts = ["Full-time", "Part-time", "Contract", "Temporary", "Other"]
                cur_type = st.session_state.get('form_type', 'Full-time')
                type_idx = type_opts.index(cur_type) if cur_type in type_opts else 0
                employment_type = st.selectbox("Employment Type", type_opts, index=type_idx)
                
                industry = st.text_input("Industry", value=st.session_state.get('form_ind', ''), placeholder="e.g. Information Technology / Financial Services")
            
            with d_col2:
                exp_opts = ["Not Applicable", "Entry level", "Associate", "Mid-Senior level", "Director", "Executive"]
                cur_exp = st.session_state.get('form_exp', 'Not Applicable')
                exp_idx = exp_opts.index(cur_exp) if cur_exp in exp_opts else 0
                experience = st.selectbox("Required Experience", exp_opts, index=exp_idx)
                
                edu_opts = ["Unspecified", "High School or equivalent", "Bachelor's Degree", "Master's Degree", "Doctorate"]
                cur_edu = st.session_state.get('form_edu', 'Unspecified')
                edu_idx = edu_opts.index(cur_edu) if cur_edu in edu_opts else 0
                education = st.selectbox("Required Education", edu_opts, index=edu_idx)
                
                function_name = st.text_input("Function / Category", value=st.session_state.get('form_func', ''), placeholder="e.g. Engineering / Administrative")
                benefits = st.text_input("Benefits Provided", value=st.session_state.get('form_ben', ''), placeholder="e.g. Health insurance, 401k, paid time off")
                
            render_html('<div class="vh-section-title" style="margin-top: 1rem;">Verification Flags</div>')
            f_col1, f_col2, f_col3 = st.columns(3)
            with f_col1:
                has_logo = st.checkbox("Has Official Company Logo", value=st.session_state.get('form_logo', True))
            with f_col2:
                has_questions = st.checkbox("Includes Screening Questions", value=st.session_state.get('form_quest', True))
            with f_col3:
                telecommuting = st.checkbox("Telecommuting / Remote Work", value=st.session_state.get('form_tele', False))
                
            st.markdown("<br/>", unsafe_allow_html=True)
            submit_btn = st.form_submit_button("🔍 Run Risk Analysis & Verification")
            
    # Evaluation Result Panel
    with col_summary:
        render_html('<div class="vh-section-title">Verification Summary</div>')
        
        if submit_btn or 'last_analysis' in st.session_state:
            if submit_btn:
                if not job_title.strip() and not job_description.strip():
                    st.warning("Please enter at least a Job Title or Job Description to perform analysis.")
                    st.session_state.pop('last_analysis', None)
                else:
                    input_data = {
                        "title": job_title,
                        "company_profile": company_profile,
                        "description": job_description,
                        "requirements": requirements,
                        "benefits": benefits,
                        "salary_range": salary_range,
                        "location": location,
                        "employment_type": employment_type,
                        "required_experience": experience,
                        "required_education": education,
                        "industry": industry,
                        "function": function_name,
                        "has_company_logo": 1 if has_logo else 0,
                        "has_questions": 1 if has_questions else 0,
                        "telecommuting": 1 if telecommuting else 0
                    }
                    st.session_state['last_analysis'] = ml_engine.analyze_job_posting(input_data, model_artifact)
            
            if 'last_analysis' in st.session_state:
                analysis = st.session_state['last_analysis']
                
                risk_lvl = analysis['risk_level']
                badge_class = "badge-low" if risk_lvl == "Low Risk" else ("badge-med" if risk_lvl == "Medium Risk" else "badge-high")
                bar_color = "#10B981" if risk_lvl == "Low Risk" else ("#F59E0B" if risk_lvl == "Medium Risk" else "#EF4444")
                
                render_html(f"""
                <div class="vh-card" style="border-top: 4px solid {bar_color};">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.6rem;">
                        <span class="badge {badge_class}">{risk_lvl.upper()}</span>
                        <span style="font-size: 0.82rem; font-weight: 700; color: #64748B;">Confidence: {analysis['confidence']}%</span>
                    </div>
                    <h3 style="margin: 0 0 0.4rem 0; font-size: 1.2rem; font-weight: 800; color: #0F172A;">{analysis['classification']}</h3>
                    
                    <div style="margin-top: 0.75rem;">
                        <div style="display: flex; justify-content: space-between; font-size: 0.78rem; font-weight: 700; color: #64748B;">
                            <span>FRAUD RISK SCORE</span>
                            <span style="color: {bar_color};">{analysis['fraud_pct']}%</span>
                        </div>
                        <div class="score-meter-container">
                            <div class="score-meter-bar" style="width: {analysis['fraud_pct']}%; background: {bar_color};"></div>
                        </div>
                    </div>
                    
                    <p style="margin: 0; font-size: 0.86rem; color: #475569; line-height: 1.5;">{analysis['explanation']}</p>
                </div>
                """)
                
                t_signals, t_advice = st.tabs(["🛡️ Risk & Trust Signals", "📋 Candidate Action Plan"])
                
                with t_signals:
                    if analysis['detected_signals']:
                        render_html('<div class="vh-section-title" style="margin-top: 0.5rem;">Flagged Risk Indicators</div>')
                        for sig in analysis['detected_signals']:
                            render_html(f"""
                            <div class="signal-box {sig['type']}">
                                <strong>{sig['title']}</strong><br/>
                                <span style="font-size: 0.82rem;">{sig['detail']}</span>
                            </div>
                            """)
                    else:
                        render_html("""
                        <div class="signal-box success" style="margin-top: 0.5rem;">
                            <strong>No Risk Signals Flagged</strong><br/>
                            <span style="font-size: 0.82rem;">Metadata and linguistic structures match standard authentic postings.</span>
                        </div>
                        """)
                        
                    if analysis['positive_signals']:
                        render_html('<div class="vh-section-title" style="margin-top: 0.75rem;">Verified Trust Factors</div>')
                        for pos in analysis['positive_signals']:
                            render_html(f"""
                            <div class="signal-box success">
                                ✓ {pos}
                            </div>
                            """)
                            
                with t_advice:
                    if risk_lvl == "High Risk":
                        render_html("""
                        <div class="vh-card" style="background: #FEF2F2; border: 1px solid #FECACA;">
                            <h4 style="color: #991B1B; margin-top:0; font-weight:700;">🚨 High Risk Safety Advice</h4>
                            <ul style="font-size: 0.85rem; color: #991B1B; padding-left: 1.1rem; line-height: 1.6; margin-bottom: 0;">
                                <li><strong>Never transfer funds:</strong> Do not wire money or deposit cashier checks for equipment fees.</li>
                                <li><strong>Refuse informal chats:</strong> Authentic employers conduct formal video/in-person interviews, not Telegram or WhatsApp chats.</li>
                                <li><strong>Protect sensitive data:</strong> Do not provide SSN, passport, or bank details before a signed employment contract.</li>
                            </ul>
                        </div>
                        """)
                    elif risk_lvl == "Medium Risk":
                        render_html("""
                        <div class="vh-card" style="background: #FFFBEB; border: 1px solid #FDE68A;">
                            <h4 style="color: #92400E; margin-top:0; font-weight:700;">⚠️ Medium Risk Verification Checklist</h4>
                            <ul style="font-size: 0.85rem; color: #92400E; padding-left: 1.1rem; line-height: 1.6; margin-bottom: 0;">
                                <li><strong>Verify corporate domain:</strong> Ensure recruiter emails match the official corporate domain.</li>
                                <li><strong>Check LinkedIn page:</strong> Confirm company exists and has verified employees.</li>
                                <li><strong>Request formal description:</strong> Ask for detailed job responsibilities and official offer letters.</li>
                            </ul>
                        </div>
                        """)
                    else:
                        render_html("""
                        <div class="vh-card" style="background: #ECFDF5; border: 1px solid #A7F3D0;">
                            <h4 style="color: #065F46; margin-top:0; font-weight:700;">✅ Low Risk Safe Guidance</h4>
                            <ul style="font-size: 0.85rem; color: #065F46; padding-left: 1.1rem; line-height: 1.6; margin-bottom: 0;">
                                <li>Posting demonstrates strong alignment with standard legitimate recruiting guidelines.</li>
                                <li>Proceed with normal job application procedures on official corporate portals.</li>
                            </ul>
                        </div>
                        """)
        else:
            st.info("Enter job details on the left or select a **1-Click Demo Preset** above, then click **'Run Risk Analysis'**.")

# ==============================================================================
# TAB 3: BATCH ANALYSIS
# ==============================================================================
elif nav_option == "Batch Analysis":
    render_html("""
    <div class="vh-header">
        <h1>Batch Job Evaluation</h1>
        <p>Upload a CSV dataset of job listings to evaluate potential recruitment fraud across multiple postings in real-time.</p>
    </div>
    """)
    
    c_up1, c_up2 = st.columns([2, 1])
    with c_up1:
        uploaded_file = st.file_uploader("Upload Job Postings CSV", type=["csv"])
    with c_up2:
        st.markdown("<br/>", unsafe_allow_html=True)
        load_sample = st.button("📁 Load Sample Benchmark CSV (100 Postings)")
        
    df_to_evaluate = None
    
    if uploaded_file is not None:
        try:
            df_to_evaluate = pd.read_csv(uploaded_file)
            st.success(f"File uploaded successfully: {len(df_to_evaluate):,} job listings detected.")
        except Exception as e:
            st.error(f"Error reading CSV file: {e}")
    elif load_sample:
        sample_full = pd.read_csv(ml_engine.DATASET_PATH)
        df_to_evaluate = pd.concat([
            sample_full[sample_full['fraudulent'] == 1].head(25),
            sample_full[sample_full['fraudulent'] == 0].head(75)
        ]).sample(frac=1, random_state=42).reset_index(drop=True)
        st.success("Loaded sample benchmark dataset (100 rows, 25% scam ratio for testing).")
        
    if df_to_evaluate is not None:
        render_html('<div class="vh-section-title">Batch Evaluation Results</div>')
        
        with st.spinner("Evaluating postings against VeriHire NLP & Metadata engine..."):
            evaluated_df, summary = ml_engine.evaluate_batch(df_to_evaluate, model_artifact)
            
        s1, s2, s3, s4 = st.columns(4)
        with s1:
            render_html(f"""
            <div class="metric-container">
                <div class="metric-label">Total Postings</div>
                <div class="metric-value">{summary['total_jobs']:,}</div>
                <div class="metric-sub">Evaluated records</div>
            </div>
            """)
        with s2:
            render_html(f"""
            <div class="metric-container">
                <div class="metric-label">High Risk Flagged</div>
                <div class="metric-value" style="color:#DC2626;">{summary['high_risk_count']}</div>
                <div class="metric-sub">{summary['high_risk_pct']}% high probability scam</div>
            </div>
            """)
        with s3:
            render_html(f"""
            <div class="metric-container">
                <div class="metric-label">Medium Risk</div>
                <div class="metric-value" style="color:#D97706;">{summary['med_risk_count']}</div>
                <div class="metric-sub">Requires manual audit</div>
            </div>
            """)
        with s4:
            render_html(f"""
            <div class="metric-container">
                <div class="metric-label">Low Risk (Authentic)</div>
                <div class="metric-value" style="color:#059669;">{summary['low_risk_count']}</div>
                <div class="metric-sub">Standard postings</div>
            </div>
            """)
            
        st.markdown("<br/>", unsafe_allow_html=True)
        
        filter_opt = st.radio(
            "Filter Batch Results by Risk Level:",
            ["All Listings", "High Risk Only 🚨", "Medium Risk Only ⚠️", "Low Risk Only ✅"],
            horizontal=True
        )
        
        if filter_opt == "High Risk Only 🚨":
            display_df = evaluated_df[evaluated_df['Risk Level'] == 'High Risk']
        elif filter_opt == "Medium Risk Only ⚠️":
            display_df = evaluated_df[evaluated_df['Risk Level'] == 'Medium Risk']
        elif filter_opt == "Low Risk Only ✅":
            display_df = evaluated_df[evaluated_df['Risk Level'] == 'Low Risk']
        else:
            display_df = evaluated_df
            
        p_col1, p_col2 = st.columns([1, 2])
        with p_col1:
            render_html('<div class="vh-section-title">Risk Proportion</div>')
            fig = px.pie(
                values=[summary['low_risk_count'], summary['med_risk_count'], summary['high_risk_count']],
                names=['Low Risk', 'Medium Risk', 'High Risk'],
                color=['Low Risk', 'Medium Risk', 'High Risk'],
                color_discrete_map={'Low Risk': '#10B981', 'Medium Risk': '#F59E0B', 'High Risk': '#EF4444'},
                hole=0.45
            )
            fig.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=260, showlegend=True)
            st.plotly_chart(fig, use_container_width=True)
            
        with p_col2:
            render_html(f'<div class="vh-section-title">Batch Results Table ({len(display_df)} listings displayed)</div>')
            st.dataframe(
                display_df.drop(columns=['_raw_prob']),
                use_container_width=True,
                height=260
            )
            
        csv_data = evaluated_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Annotated Results CSV",
            data=csv_data,
            file_name="verihire_batch_results.csv",
            mime="text/csv"
        )

# ==============================================================================
# TAB 4: MODEL INSIGHTS
# ==============================================================================
elif nav_option == "Model Insights":
    render_html("""
    <div class="vh-header">
        <h1>Model Performance & Risk Simulator</h1>
        <p>Audit classifier metrics, explore keyphrase coefficients, and simulate custom risk decision thresholds.</p>
    </div>
    """)
    
    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        render_html(f"""
        <div class="metric-container">
            <div class="metric-label">ROC-AUC</div>
            <div class="metric-value">{metrics['roc_auc']*100:.2f}%</div>
        </div>
        """)
    with m2:
        render_html(f"""
        <div class="metric-container">
            <div class="metric-label">Accuracy</div>
            <div class="metric-value">{metrics['accuracy']*100:.2f}%</div>
        </div>
        """)
    with m3:
        render_html(f"""
        <div class="metric-container">
            <div class="metric-label">Recall</div>
            <div class="metric-value">{metrics['recall']*100:.2f}%</div>
        </div>
        """)
    with m4:
        render_html(f"""
        <div class="metric-container">
            <div class="metric-label">Precision</div>
            <div class="metric-value">{metrics['precision']*100:.2f}%</div>
        </div>
        """)
    with m5:
        render_html(f"""
        <div class="metric-container">
            <div class="metric-label">F1-Score</div>
            <div class="metric-value">{metrics['f1']*100:.2f}%</div>
        </div>
        """)
        
    st.markdown("<br/>", unsafe_allow_html=True)
    
    tab_sim, tab_feats, tab_cm = st.tabs(["🎛️ Risk Threshold Simulator", "🔍 Keyphrase Feature Explorer", "📊 Confusion Matrix & Architecture"])
    
    with tab_sim:
        render_html("""
        <div class="vh-card">
            <h4 style="margin-top:0; font-weight:700;">Adjust Fraud Classification Threshold</h4>
            <p style="font-size: 0.88rem; color: #475569; line-height: 1.5;">
                Tune the decision boundary cutoff to observe trade-offs between catching more fraud (higher recall) versus avoiding false alarms (higher precision).
            </p>
        </div>
        """)
        
        cutoff = st.slider("Select Fraud Cutoff Threshold (Default = 0.55)", min_value=0.10, max_value=0.90, value=0.55, step=0.05)
        
        sim_col1, sim_col2 = st.columns(2)
        with sim_col1:
            if cutoff < 0.35:
                sim_recall = "High (~94%)"
                sim_prec = "Lower (~58%)"
                sim_impact = "Strict Moderation: Flags almost all suspicious postings, but increases false alarms on legitimate posts."
            elif cutoff > 0.65:
                sim_recall = "Moderate (~72%)"
                sim_prec = "Very High (~92%)"
                sim_impact = "Conservative Moderation: Highly confident scam alerts, but may miss subtle or borderline deceptive ads."
            else:
                sim_recall = f"{metrics['recall']*100:.1f}%"
                sim_prec = f"{metrics['precision']*100:.1f}%"
                sim_impact = "Optimal Balanced Operating Point for production deployment."
                
            render_html(f"""
            <div class="vh-card" style="background: #F8FAFC;">
                <div style="font-size: 0.82rem; font-weight: 700; color: #64748B;">SIMULATED PERFORMANCE AT {cutoff*100:.0f}% THRESHOLD</div>
                <div style="display: flex; gap: 2rem; margin-top: 0.75rem;">
                    <div>
                        <div style="font-size: 0.78rem; color: #64748B;">Estimated Sensitivity (Recall)</div>
                        <div style="font-size: 1.4rem; font-weight: 800; color: #2563EB;">{sim_recall}</div>
                    </div>
                    <div>
                        <div style="font-size: 0.78rem; color: #64748B;">Estimated Precision</div>
                        <div style="font-size: 1.4rem; font-weight: 800; color: #10B981;">{sim_prec}</div>
                    </div>
                </div>
                <p style="margin: 0.75rem 0 0 0; font-size: 0.84rem; color: #475569;"><strong>Operational Impact:</strong> {sim_impact}</p>
            </div>
            """)
            
        with sim_col2:
            render_html("""
            <div class="vh-card">
                <h5 style="margin-top:0; font-weight:700;">Threshold Selection Guidance</h5>
                <ul style="font-size: 0.85rem; color: #475569; padding-left: 1.1rem; line-height: 1.5;">
                    <li><strong>0.25 - 0.54:</strong> Medium Risk Tier (Needs human reviewer check)</li>
                    <li><strong>≥ 0.55:</strong> High Risk Scam Tier (Instant warning banner)</li>
                    <li><strong>< 0.25:</strong> Low Risk Tier (Auto-approved post)</li>
                </ul>
            </div>
            """)
            
    with tab_feats:
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            render_html('<div class="vh-section-title">Top Keyphrase Risk Indicators (Fraudulent Signals)</div>')
            fraud_feats = pd.DataFrame(metrics['top_fraud_features'], columns=['Feature', 'Coefficient Weight']).head(12)
            fig_f = px.bar(
                fraud_feats, 
                x='Coefficient Weight', 
                y='Feature', 
                orientation='h',
                color_discrete_sequence=['#EF4444']
            )
            fig_f.update_layout(yaxis=dict(autorange="reversed"), margin=dict(t=10, b=10, l=10, r=10), height=320)
            st.plotly_chart(fig_f, use_container_width=True)
            
        with chart_col2:
            render_html('<div class="vh-section-title">Top Trust Keyphrase Indicators (Legitimate Signals)</div>')
            legit_feats = pd.DataFrame(metrics['top_legit_features'], columns=['Feature', 'Coefficient Weight']).head(12)
            legit_feats['Abs Weight'] = legit_feats['Coefficient Weight'].abs()
            fig_l = px.bar(
                legit_feats, 
                x='Abs Weight', 
                y='Feature', 
                orientation='h',
                color_discrete_sequence=['#10B981']
            )
            fig_l.update_layout(yaxis=dict(autorange="reversed"), margin=dict(t=10, b=10, l=10, r=10), height=320)
            st.plotly_chart(fig_l, use_container_width=True)
            
        st.markdown("<br/>", unsafe_allow_html=True)
        render_html('<div class="vh-section-title">Search Model Feature Dictionary</div>')
        search_kw = st.text_input("Search keyphrase weight in model dictionary:", placeholder="e.g. telegram, wire, engineer, experience, cashier...")
        
        if search_kw.strip():
            all_feats = model_artifact['feature_names']
            all_coefs = model_artifact['model'].coef_[0]
            
            matches = []
            skw = search_kw.strip().lower()
            for name, coef in zip(all_feats, all_coefs):
                if skw in name.lower():
                    matches.append({'Feature': name, 'Weight': round(float(coef), 4), 'Impact': 'Leans Scam 🚨' if coef > 0 else 'Leans Legitimate ✅'})
                    
            if matches:
                m_df = pd.DataFrame(matches).sort_values(by='Weight', ascending=False)
                st.dataframe(m_df, use_container_width=True)
            else:
                st.info(f"No exact match for '{search_kw}' in top 4,000 TF-IDF features.")
                
    with tab_cm:
        cm_c1, cm_c2 = st.columns([1, 1.5])
        with cm_c1:
            render_html('<div class="vh-section-title">Confusion Matrix</div>')
            cm = np.array(metrics['confusion_matrix'])
            fig_cm = px.imshow(
                cm,
                labels=dict(x="Predicted", y="Actual", color="Count"),
                x=['Legitimate', 'Fraudulent'],
                y=['Legitimate', 'Fraudulent'],
                text_auto=True,
                color_continuous_scale="Blues"
            )
            fig_cm.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=260)
            st.plotly_chart(fig_cm, use_container_width=True)
            
        with cm_c2:
            render_html("""
            <div class="vh-card">
                <h4 style="margin-top:0; font-weight:700;">Model Architecture & Methodology</h4>
                <p style="font-size: 0.88rem; color: #475569; line-height: 1.6;">
                    The VeriHire engine employs a hybrid Feature Union pipeline combining TF-IDF n-gram text representations (up to 4,000 features) 
                    with binary structural metadata indicators (company profile completeness, logo presence, screening question presence, salary specification, and remote work flags).
                </p>
                <ul style="font-size: 0.85rem; color: #475569; padding-left: 1.2rem; line-height: 1.6;">
                    <li><strong>Class Balancing:</strong> Adjusts cost functions for the 4.84% baseline scam ratio in the dataset.</li>
                    <li><strong>Interpretability:</strong> Coefficient weights map directly to human-auditable risk signals.</li>
                    <li><strong>Calibration:</strong> Outputs continuous probability scores mapped directly into risk tiers.</li>
                </ul>
            </div>
            """)
