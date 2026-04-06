import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Fitness Categorization",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

from pages import home, input_form, results

import sys
from pathlib import Path

# Add the app directory to path
app_dir = Path(__file__).parent
sys.path.insert(0, str(app_dir))



# Custom CSS for dark theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f0f1e 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 20px;
        backdrop-filter: blur(10px);
        margin-bottom: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .main-header h1 {
        color: #00d4ff;
        font-size: 2.8rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
    }
    
    .main-header p {
        color: #b8b8d1;
        font-size: 1.1rem;
        font-weight: 300;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 2rem;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .feature-card:hover {
        background: rgba(255, 255, 255, 0.08);
        transform: translateY(-5px);
        border-color: #00d4ff;
        box-shadow: 0 10px 30px rgba(0, 212, 255, 0.2);
    }
    
    .feature-card h3 {
        color: #00d4ff;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .feature-card p {
        color: #b8b8d1;
        line-height: 1.6;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #00d4ff 0%, #0099ff 100%);
        color: white;
        border: none;
        padding: 0.8rem 2.5rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 50px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 5px 20px rgba(0, 212, 255, 0.3);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0, 212, 255, 0.5);
    }
    
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: #7a7a9d;
        font-size: 0.9rem;
        margin-top: 3rem;
    }
    
    .footer span {
        color: #ff6b9d;
    }
    
    /* Input styling */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div,
    .stSlider > div > div {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #e0e0f0 !important;
        border-radius: 10px !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #00d4ff !important;
        box-shadow: 0 0 0 2px rgba(0, 212, 255, 0.1) !important;
    }
    
    label {
        color: #b8b8d1 !important;
        font-weight: 500 !important;
    }
    
    .stRadio > label {
        color: #b8b8d1 !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .result-card {
        background: linear-gradient(135deg, rgba(0, 212, 255, 0.1) 0%, rgba(0, 153, 255, 0.05) 100%);
        padding: 2rem;
        border-radius: 20px;
        border: 2px solid rgba(0, 212, 255, 0.3);
        margin: 1rem 0;
    }
    
    .result-card h2 {
        color: #00d4ff;
        margin-bottom: 1rem;
    }
    
    .result-card p {
        color: #e0e0f0;
        line-height: 1.8;
        font-size: 1.05rem;
    }
    
    .feedback-section {
        background: rgba(255, 255, 255, 0.03);
        padding: 2rem;
        border-radius: 15px;
        margin-top: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'user_inputs' not in st.session_state:
    st.session_state.user_inputs = {}
if 'prediction_result' not in st.session_state:
    st.session_state.prediction_result = None

# Navigation functions
def navigate_to(page):
    st.session_state.page = page
    st.rerun()

# Import pages
# from app.streamlit_app.pages import results

# Page routing
if st.session_state.page == 'home':
    home.show()
elif st.session_state.page == 'input':
    input_form.show()
elif st.session_state.page == 'results':
    results.show()
