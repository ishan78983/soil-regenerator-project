import streamlit as st
import requests
import json

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Soil Intelligence",
    page_icon="🌿",
    layout="wide"
)

# --- Custom CSS for a clean, minimalist, professional design ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

    html, body, [class*="st-"] {
        font-family: 'Poppins', sans-serif;
    }

    /* Main background */
    [data-testid="stAppViewContainer"] {
        background-color: #f0f2f5; /* A very light grey */
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e6e6e6;
    }

    /* Main content container */
    .main .block-container {
        padding: 2rem 3rem;
    }
    
    /* Text colors */
    h1, h2, h3 {
        color: #0a2540; /* Deep navy blue for headings */
    }
    p, label, .st-emotion-cache-10trblm {
        color: #333333; /* Dark grey for body text */
    }

    /* Custom Metric Card styling */
    .metric-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 25px;
        border: 1px solid #e6e6e6;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        transition: all 0.3s ease-in-out;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.1);
    }
    .metric-title {
        font-size: 16px;
        font-weight: 600;
        color: #555555;
        margin-bottom: 5px;
    }
    .metric-value {
        font-size: 36px;
        font-weight: 700;
        color: #0a2540;
    }
    .metric-icon {
        font-size: 24px;
        float: right;
    }
    .progress-bar-container {
        height: 8px;
        width: 100%;
        background-color: #e9ecef;
        border-radius: 4px;
        margin-top: 15px;
    }
    .progress-bar {
        height: 100%;
        background-color: #0a2540; /* Navy progress bar */
        border-radius: 4px;
    }
    
    /* Professional Button Style */
    .stButton>button {
        color: #FFFFFF;
        background-color: #ff8c42; /* Warm orange accent */
        border: none;
        border-radius: 8px;
        padding: 12px 28px;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #ff7722;
        box-shadow: 0 4px 12px rgba(255, 140, 66, 0.4);
    }

    /* Container for the final report */
    .report-container {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 30px;
        border: 1px solid #e6e6e6;
    }

</style>
""", unsafe_allow_html=True)

# --- Backend API URL ---
API_URL = " https://soil-api-02a6.onrender.com"

# --- Sidebar Inputs ---
with st.sidebar:
    st.image("https://i.imgur.com/gYf2sPo.png", width=80)
    st.title("Soil Console")
    st.markdown("Enter your soil data for analysis.")

    location = st.text_input("📍 Location/Climate Zone", "Indore, Madhya Pradesh")
    ph_level = st.slider("💧 pH Level", 0.0, 14.0, 6.5, 0.1)
    organic_matter = st.slider("🌿 Organic Matter (%)", 0.0, 15.0, 3.5, 0.1)
    moisture_content = st.slider("💧 Moisture Content (%)", 0.0, 60.0, 20.0, 0.5)

    crop_list = ["Not Applicable", "Soybean", "Wheat", "Maize (Corn)", "Cotton", "Gram (Chickpea)", "Sugarcane", "Other"]
    selected_crop = st.selectbox("🌾 Previous Crop", options=crop_list)
    
    if selected_crop == "Other":
        previous_crop = st.text_input("Please specify the crop:")
    else:
        previous_crop = selected_crop
    
    st.markdown("---")
    # Using st.form to group the button and inputs
    with st.form("generation_form"):
        submitted = st.form_submit_button("Generate Regeneration Plan", use_container_width=True)


# --- Main Dashboard ---
st.title("🌿 AI Soil Intelligence")
st.markdown("A professional-grade tool for data-driven soil regeneration strategies.")
st.markdown("---")

# --- Elegant Metric Cards ---
st.header("Soil Metrics Overview")

def display_metric(icon, title, value, unit, max_value, color):
    """Creates an elegant metric card with a progress bar."""
    progress = (value / max_value) * 100
    st.markdown(f"""
        <div class="metric-card">
            <span class="metric-icon">{icon}</span>
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}{unit}</div>
            <div class="progress-bar-container">
                <div class="progress-bar" style="width: {progress}%; background-color: {color};"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    display_metric("💧", "pH Level", ph_level, "", 14, "#4a90e2") # A calm blue
with col2:
    display_metric("🌿", "Organic Matter", organic_matter, "%", 15, "#50e3c2") # A vibrant teal
with col3:
    display_metric("💧", "Moisture Content", moisture_content, "%", 60, "#7ed321") # A lively green


# --- Generation Logic ---
if submitted:
    with st.spinner("Analyzing data and consulting AI Agronomist..."):
        payload = {"location": location, "ph_level": ph_level, "organic_matter": organic_matter, 
                   "moisture_content": moisture_content, "previous_crop": previous_crop}
        try:
            response = requests.post(f"{API_URL}/generate", json=payload, timeout=60)
            response.raise_for_status()
            st.session_state['last_recommendation'] = response.json().get("recommendation")
            st.toast('Analysis Complete!', icon='✅')
        except requests.exceptions.RequestException as e:
            st.toast(f"Error: Could not connect to API. {e}", icon='🔥')

# --- Display Result ---
if 'last_recommendation' in st.session_state and st.session_state['last_recommendation']:
    st.header("AI-Generated Regeneration Plan", divider='gray')
    st.markdown(f"<div class='report-container'>{st.session_state['last_recommendation']}</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.download_button(label="Download Full Report (.txt)", data=st.session_state['last_recommendation'],
                       file_name="soil_regeneration_plan.txt", mime="text/plain", use_container_width=True)