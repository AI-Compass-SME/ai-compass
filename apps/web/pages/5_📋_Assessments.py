"""
Assessment List Page
Shows all assessments from database with ability to continue/view results.
"""
import streamlit as st
import requests
import os
from datetime import datetime

st.set_page_config(page_title="Assessments", page_icon="📋", layout="wide")

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("📋 Ihre Assessments")
st.markdown("---")

# Fetch assessments from API
try:
    response = requests.get(
        f"{API_URL}/api/v1/assessments",
        params={"limit": 100},
        timeout=10
    )
    
    if response.status_code == 200:
        assessments = response.json()
        
        if not assessments:
            st.info("📝 Noch keine Assessments vorhanden.")
            if st.button("➕ Neues Assessment erstellen"):
                st.switch_page("pages/0_Company_Snapshot.py")
        else:
            # Filter buttons
            col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
            
            with col1:
                show_all = st.button("🔍 Alle", use_container_width=True)
            with col2:
                show_completed = st.button("✅ Abgeschlossen", use_container_width=True)
            with col3:
                show_draft = st.button("📝 Entwurf", use_container_width=True)
            
            # Filter assessments
            filtered_assessments = assessments
            if show_completed:
                filtered_assessments = [a for a in assessments if a['status'] == 'completed']
            elif show_draft:
                filtered_assessments = [a for a in assessments if a['status'] == 'draft']
            
            st.markdown(f"**{len(filtered_assessments)} Assessment(s) gefunden**")
            st.markdown("---")
            
            # Display assessments as cards
            for assessment in filtered_assessments:
                with st.container():
                    col1, col2, col3 = st.columns([3, 2, 1])
                    
                    with col1:
                        # Company info
                        st.markdown(f"### 🏢 {assessment['company_name']}")
                        st.markdown(f"**Branche:** {assessment['industry']}")
                        st.markdown(f"**Mitarbeiter:** {assessment['employee_count']}")
                    
                    with col2:
                        # Status and dates
                        status_icon = "✅" if assessment['status'] == 'completed' else "📝"
                        status_text = "Abgeschlossen" if assessment['status'] == 'completed' else "Entwurf"
                        st.markdown(f"**Status:** {status_icon} {status_text}")
                        
                        # Parse and format dates
                        try:
                            created_dt = datetime.fromisoformat(assessment['created_at'].replace('Z', '+00:00'))
                            st.markdown(f"**Erstellt:** {created_dt.strftime('%d.%m.%Y %H:%M')}")
                        except:
                            st.markdown(f"**Erstellt:** {assessment['created_at'][:10]}")
                        
                        if assessment['completed_at']:
                            try:
                                completed_dt = datetime.fromisoformat(assessment['completed_at'].replace('Z', '+00:00'))
                                st.markdown(f"**Abgeschlossen:** {completed_dt.strftime('%d.%m.%Y %H:%M')}")
                            except:
                                st.markdown(f"**Abgeschlossen:** {assessment['completed_at'][:10]}")
                    
                    with col3:
                        # Action buttons
                        assessment_id = assessment['id']
                        
                        if assessment['status'] == 'completed':
                            if st.button("📊 Ergebnisse", key=f"view_{assessment_id}", use_container_width=True):
                                st.session_state.assessment_id = assessment_id
                                st.switch_page("pages/2_📊_Results.py")
                        else:
                            if st.button("▶️ Fortsetzen", key=f"continue_{assessment_id}", use_container_width=True):
                                st.session_state.assessment_id = assessment_id
                                st.switch_page("pages/1_📋_Assessment.py")
                        
                        # Delete button (optional)
                        # if st.button("🗑️", key=f"delete_{assessment_id}", use_container_width=True):
                        #     # TODO: Implement delete functionality
                        #     pass
                    
                    st.markdown("---")
            
            # New assessment button at bottom
            st.markdown("")
            if st.button("➕ Neues Assessment erstellen", type="primary", use_container_width=True):
                # Clear session state for new assessment
                if 'assessment_id' in st.session_state:
                    del st.session_state.assessment_id
                st.switch_page("pages/0_Company_Snapshot.py")
    
    else:
        st.error(f"Fehler beim Laden der Assessments: {response.status_code}")
        st.info("Hinweis: Stellen Sie sicher, dass die API läuft (http://localhost:8000)")

except requests.exceptions.ConnectionError:
    st.error("🔌 Keine Verbindung zur API möglich")
    st.warning("""
    **API ist nicht erreichbar**
    
    Bitte stellen Sie sicher, dass die FastAPI Backend läuft:
    ```bash
    cd apps/api
    uvicorn main:app --reload
    ```
    """)
except Exception as e:
    st.error(f"Fehler: {str(e)}")

# Sidebar help
with st.sidebar:
    st.markdown("### ℹ️ Über Assessments")
    st.markdown("""
    Hier sehen Sie alle Ihre AI-Maturity Assessments.
    
    **Status:**
    - 📝 **Entwurf**: Assessment gestartet, aber nicht abgeschlossen
    - ✅ **Abgeschlossen**: Assessment komplett, Ergebnisse verfügbar
    
    **Aktionen:**
    - **Fortsetzen**: Assessment weitermachen
    - **Ergebnisse**: Scores, Benchmark, Empfehlungen ansehen
    """)
