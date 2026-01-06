"""
AI-Compass Streamlit Home Page
"""
import streamlit as st
import os

# Page config
st.set_page_config(
    page_title="AI-Compass",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .cta-button {
        background-color: #1f77b4;
        color: white;
        padding: 0.75rem 2rem;
        border-radius: 5px;
        text-align: center;
        font-size: 1.2rem;
        font-weight: 600;
        border: none;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🧭 AI-Compass</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI Maturity Assessment für KMU-Entscheider</div>', unsafe_allow_html=True)

# Introduction
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("""
    ### Willkommen bei AI-Compass
    
    **AI-Compass** ist ein professionelles Assessment-Tool zur Bewertung Ihrer KI-Reife. 
    In nur **12 Minuten** erhalten Sie:
    
    ✅ **Klaren Reifegrad** (1-5) über 7 Dimensionen  
    ✅ **Benchmarking** vs. Peer-Unternehmen  
    ✅ **Konkrete Roadmap** (Quick Wins + 90d/6m/12m)  
    ✅ **Executive PDF-Report** zum Teilen
    """)

# Features
st.markdown("---")
st.markdown("### 🎯 Die 7 Dimensionen")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="feature-box">', unsafe_allow_html=True)
    st.markdown("""
    **1. Strategy & Business Vision**  
    Klarheit und Commitment zu KI-Initiativen
    
    **2. Data Maturity**  
    Verfügbarkeit, Qualität & Governance
    
    **3. Tech Infrastructure**  
    APIs, Umgebungen, Security
    
    **4. People & Culture**  
    Literacy, Ownership, Change-Bereitschaft
    """)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="feature-box">', unsafe_allow_html=True)
    st.markdown("""
    **5. Processes & Scaling**  
    Delivery, Messung, Betrieb
    
    **6. Governance & Compliance**  
    DSGVO, KI-Policy, Vendor Risk
    
    **7. Use Cases & Business Value**  
    Pipeline, Machbarkeit, Realisierung
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# How it works
st.markdown("---")
st.markdown("### 📋 So funktioniert's")

steps_col1, steps_col2, steps_col3 = st.columns(3)

with steps_col1:
    st.markdown("""
    #### 1️⃣ Company Snapshot
    Grunddaten Ihres Unternehmens (Branche, Größe)
    """)

with steps_col2:
    st.markdown("""
    #### 2️⃣ Assessment
    21 Fragen über 7 Dimensionen (~12 Min)
    """)

with steps_col3:
    st.markdown("""
    #### 3️⃣ Ergebnisse
    Score, Benchmark, Roadmap & PDF
    """)

# CTA
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    if st.button("🚀 Assessment starten", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Company_Snapshot.py")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888; font-size: 0.9rem;'>
    AI-Compass MVP | Deterministic Scoring • ML Benchmarking • LLM Recommendations
</div>
""", unsafe_allow_html=True)

# Sidebar info
with st.sidebar:
    st.markdown("### ℹ️ Info")
    st.markdown("""
    **AI-Compass** ist ein consulting-ready Assessment-Tool.
    
    - 🎯 Deterministische Bewertung
    - 📊 Peer-Benchmarking (K-Means)
    - 🤖 LLM-Empfehlungen (Groq)
    - 📄 PDF-Export
    
    **API Status:**
    """)
    
    # Check API health
    import requests
    api_url = os.getenv("API_URL", "http://localhost:8000")
    
    try:
        response = requests.get(f"{api_url}/health", timeout=2)
        if response.status_code == 200:
            st.success("✓ API Connected")
        else:
            st.error("✗ API Error")
    except:
        st.error("✗ API Offline")
    
    st.markdown("---")
    st.markdown("""
    **Dauer:** ~12 Minuten  
    **Sprache:** Deutsch  
    **Version:** 1.0
    """)
