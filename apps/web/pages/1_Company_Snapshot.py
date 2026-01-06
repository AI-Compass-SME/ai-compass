"""
Company Snapshot Page
Collects company metadata before assessment.
"""
import streamlit as st
import requests
import os

st.set_page_config(page_title="Company Snapshot", page_icon="🏢", layout="wide")

# Get API URL from environment
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Custom CSS
st.markdown("""
<style>
    .snapshot-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="snapshot-header">🏢 Company Snapshot</div>', unsafe_allow_html=True)
st.markdown("Bitte geben Sie einige Grundinformationen zu Ihrem Unternehmen an.")
st.markdown("---")

# Form
with st.form("company_snapshot_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        industry = st.selectbox(
            "Branche *",
            options=[
                "Automobil",
                "Bauwesen",
                "Bildung",
                "Chemie & Pharma",
                "Einzelhandel",
                "Energie & Versorgung",
                "Finanzdienstleistungen",
                "Gesundheitswesen",
                "IT & Software",
                "Logistik & Transport",
                "Maschinenbau",
                "Medien & Kommunikation",
                "Öffentlicher Sektor",
                "Telekommunikation",
                "Sonstige"
            ],
            index=0
        )
        
        employee_band = st.selectbox(
            "Mitarbeiteranzahl *",
            options=[
                "1-10",
                "11-50",
                "51-250",
                "251-500",
                "501-1000",
                "1001-5000",
                "5000+"
            ],
            index=2
        )
    
    with col2:
        revenue_band = st.selectbox(
            "Jahresumsatz (optional)",
            options=[
                "Keine Angabe",
                "< 1 Mio €",
                "1-10 Mio €",
                "10-50 Mio €",
                "50-250 Mio €",
                "250 Mio - 1 Mrd €",
                "> 1 Mrd €"
            ],
            index=0
        )
        
        country = st.text_input(
            "Land (optional)",
            value="Deutschland"
        )
    
    st.markdown("---")
    st.markdown("**Hinweis:** Die Angaben werden nur für die Auswertung verwendet und nicht weitergegeben.")
    
    submitted = st.form_submit_button("Weiter zum Assessment →", type="primary", use_container_width=True)
    
    if submitted:
        if not industry or not employee_band:
            st.error("Bitte füllen Sie alle Pflichtfelder (*) aus.")
        else:
            # Prepare company meta
            company_meta = {
                "industry": industry,
                "employee_band": employee_band,
                "revenue_band": revenue_band if revenue_band != "Keine Angabe" else None,
                "country": country if country else None
            }
            
            # Create assessment via API
            with st.spinner("Erstelle Assessment..."):
                try:
                    response = requests.post(
                        f"{API_URL}/api/v1/assessments",
                        json={"company_meta": company_meta},
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        assessment_id = data["assessment_id"]
                        
                        # Store in session state
                        st.session_state.assessment_id = assessment_id
                        st.session_state.company_meta = company_meta
                        
                        st.success(f"✓ Assessment erstellt (ID: {assessment_id[:8]}...)")
                        st.info("Weiterleitung zum Fragebogen...")
                        
                        # Navigate to assessment page
                        st.switch_page("pages/2_Assessment.py")
                    else:
                        st.error(f"Fehler beim Erstellen des Assessments: {response.text}")
                
                except Exception as e:
                    st.error(f"Verbindungsfehler: {str(e)}")
                    st.info("Bitte stellen Sie sicher, dass die API läuft (http://localhost:8000)")

# Back button
st.markdown("---")
if st.button("← Zurück zur Startseite"):
    st.switch_page("Home.py")

# Sidebar
with st.sidebar:
    st.markdown("### 📋 Schritt 1/3")
    st.progress(0.33)
    st.markdown("""
    **Company Snapshot**
    
    Erfassen Sie Grunddaten Ihres Unternehmens.
    
    Diese Informationen helfen uns, Ihre Ergebnisse besser einzuordnen.
    """)
