import streamlit as st
import requests
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI-Compass - Home",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_URL = os.getenv("API_URL", "http://localhost:8000")

# Main title
st.title("🧭 AI-Compass")
st.subheader("AI Maturity Assessment Tool")

# Introduction
st.markdown("""
Welcome to **AI-Compass**, your comprehensive AI maturity assessment platform.

### What is AI-Compass?

AI-Compass is a consulting tool designed to help organizations:
- **Assess** their current AI maturity level
- **Benchmark** against industry standards
- **Identify** gaps and opportunities
- **Plan** strategic AI initiatives

### How It Works

1. **Assessment**: Complete a comprehensive questionnaire about your organization's AI capabilities
2. **Scoring**: Receive an objective maturity score across multiple dimensions
3. **Benchmarking**: Compare your results with industry standards
4. **Recommendations**: Get actionable insights powered by AI analysis
5. **Reports**: Download detailed PDF reports for stakeholders

### Get Started

Use the sidebar to navigate between different sections:
- **📋 Assessments**: View all your assessments
- **📋 Assessment**: Take the AI maturity questionnaire
- **📊 Results**: View your assessment scores and insights
- **📈 Benchmark**: Compare with industry peers
- **📄 Reports**: Generate and download PDF reports
""")

# Recent assessments section
st.markdown("---")
st.markdown("## 📋 Ihre letzten Assessments")

try:
    response = requests.get(f"{API_URL}/api/v1/assessments?limit=5", timeout=5)
    
    if response.status_code == 200:
        assessments = response.json()
        
        if assessments:
            for assessment in assessments:
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    status_icon = "✅" if assessment['status'] == 'completed' else "📝"
                    st.write(f"{status_icon} **{assessment['company_name']}** ({assessment['industry']})")
                
                with col2:
                    try:
                        created = datetime.fromisoformat(assessment['created_at'].replace('Z', '+00:00'))
                        st.write(created.strftime('%d.%m.%Y'))
                    except:
                        st.write(assessment['created_at'][:10])
                
                with col3:
                    if assessment['status'] == 'completed':
                        if st.button("Ergebnisse", key=f"home_{assessment['id']}", use_container_width=True):
                            st.session_state.assessment_id = assessment['id']
                            st.switch_page("pages/2_📊_Results.py")
                    else:
                        if st.button("Fortsetzen", key=f"home_{assessment['id']}", use_container_width=True):
                            st.session_state.assessment_id = assessment['id']
                            st.switch_page("pages/1_📋_Assessment.py")
            
            if st.button("📋 Alle Assessments anzeigen", use_container_width=True):
                st.switch_page("pages/5_📋_Assessments.py")
        else:
            st.info("Noch keine Assessments vorhanden.")
            if st.button("➕ Erstes Assessment erstellen", type="primary", use_container_width=True):
                st.switch_page("pages/0_Company_Snapshot.py")
    else:
        st.info("Assessment-Liste konnte nicht geladen werden.")
except:
    st.info("Erstellen Sie Ihr erstes Assessment!")
    if st.button("➕ Assessment starten", type="primary", use_container_width=True):
        st.switch_page("pages/0_Company_Snapshot.py")

# Quick stats or features
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Assessment Questions", value="21", delta="Umfassend")

with col2:
    st.metric(label="Maturity Dimensions", value="7", delta="Multi-faceted")

with col3:
    st.metric(label="Avg. Completion Time", value="12 min", delta="Schnell")

# Footer
st.markdown("---")
st.caption("AI-Compass MVP | Powered by FastAPI & Streamlit")
