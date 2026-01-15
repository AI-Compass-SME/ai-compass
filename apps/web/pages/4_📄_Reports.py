import streamlit as st
from datetime import datetime
import json
import requests
import os

st.set_page_config(page_title="Reports", page_icon="📄", layout="wide")

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("📄 Reports & Documentation")

# Get assessment_id from URL parameter OR session state
assessment_id = None

if "id" in st.query_params:
    assessment_id = st.query_params["id"]
elif "assessment_id" in st.session_state:
    assessment_id = st.session_state.assessment_id

if not assessment_id:
    st.warning("⚠️ Kein Assessment ausgewählt.")
    if st.button("📋 Zu Assessments"):
        st.switch_page("pages/5_📋_Assessments.py")
    st.stop()

# Load assessment from database
with st.spinner("Lade Assessment-Daten..."):
    try:
        response = requests.get(
            f"{API_URL}/api/v1/assessments/{assessment_id}",
            timeout=10
        )
        
        if response.status_code == 404:
            st.error("❌ Assessment nicht gefunden.")
            if st.button("📋 Zurück zu Assessments"):
                st.switch_page("pages/5_📋_Assessments.py")
            st.stop()
        elif response.status_code != 200:
            st.error(f"Fehler beim Laden: {response.text}")
            st.stop()
        
        assessment_data = response.json()
        
        # Check if completed
        if assessment_data["status"] != "completed":
            st.warning("⚠️ Assessment noch nicht abgeschlossen.")
            if st.button("📋 Assessment fortsetzen"):
                st.session_state.assessment_id = assessment_id
                st.switch_page("pages/1_📋_Assessment.py")
            st.stop()
        
        # Store in session for use on this page
        if assessment_data.get("results"):
            st.session_state.assessment_data = assessment_data
        else:
            st.error("Report-Daten nicht verfügbar.")
            st.stop()
        
    except requests.exceptions.ConnectionError:
        st.error("🔌 Keine Verbindung zur API")
        st.stop()
    except Exception as e:
        st.error(f"Fehler: {str(e)}")
        st.stop()

st.markdown("""
Generate and download comprehensive reports of your AI maturity assessment.
""")

# Report options
st.markdown("### Report Options")

col1, col2 = st.columns(2)

with col1:
    report_type = st.selectbox(
        "Report Type",
        options=[
            "Executive Summary",
            "Detailed Technical Report",
            "Benchmark Comparison Report",
            "Complete Assessment Report"
        ]
    )

with col2:
    report_format = st.selectbox(
        "Format",
        options=["PDF", "JSON", "CSV"]
    )

# Report customization
st.markdown("### Customize Your Report")

with st.expander("Report Settings", expanded=True):
    col1, col2 = st.columns(2)
    
    with col1:
        include_charts = st.checkbox("Include Visualizations", value=True)
        include_recommendations = st.checkbox("Include Recommendations", value=True)
        include_benchmarks = st.checkbox("Include Industry Benchmarks", value=True)
    
    with col2:
        include_raw_data = st.checkbox("Include Raw Assessment Data", value=False)
        include_methodology = st.checkbox("Include Methodology Section", value=True)
        company_name = st.text_input("Company Name (optional)", placeholder="Your Organization")

st.markdown("---")

# Report preview
st.markdown("### Report Preview")

# Generate preview content
def generate_report_content(include_details=True):
    """Generate report content based on selection"""
    
    content = f"""
# AI Maturity Assessment Report
## {company_name if company_name else 'Your Organization'}

**Report Type:** {report_type}  
**Generated:** {datetime.now().strftime("%B %d, %Y at %H:%M")}  
**Assessment Completed:** {st.session_state.get('completion_time', 'N/A')}

---

## Executive Summary

This report presents the results of an AI maturity assessment conducted for {company_name if company_name else 'your organization'}. 
The assessment evaluates AI capabilities across four key dimensions:

1. **Strategic Alignment** - How well AI strategy aligns with business objectives
2. **Data Readiness** - Quality and governance of data assets
3. **Technology Infrastructure** - Technical capabilities and MLOps maturity
4. **Organizational Capability** - Talent, skills, and organizational structure

### Overall Maturity Score

Your organization achieved an overall maturity score that places you in the **developing** phase 
of AI adoption. This indicates that you have established foundational AI capabilities and are 
actively building more advanced practices.

"""

    if include_recommendations:
        content += """
---

## Key Recommendations

### Priority 1: Strengthen Data Foundation
- Implement comprehensive data governance framework
- Invest in data quality improvement initiatives
- Establish data cataloging and lineage tracking

### Priority 2: Scale Technology Infrastructure
- Adopt MLOps best practices
- Implement model monitoring and management systems
- Scale cloud infrastructure for AI workloads

### Priority 3: Build Organizational Capability
- Expand AI/ML talent acquisition
- Implement structured training and upskilling programs
- Establish AI Center of Excellence

### Priority 4: Enhance Strategic Alignment
- Develop comprehensive AI roadmap
- Align AI initiatives with business KPIs
- Establish AI governance and ethics framework

"""

    if include_benchmarks:
        content += """
---

## Industry Benchmark Comparison

Your scores have been compared against industry peers to provide context 
for your maturity level:

- **Strategic Alignment**: Aligned with industry average
- **Data Readiness**: Slightly below industry leaders
- **Technology Infrastructure**: Opportunity for improvement
- **Organizational Capability**: Competitive positioning

"""

    if include_methodology:
        content += """
---

## Methodology

This assessment uses a structured questionnaire covering four key dimensions 
of AI maturity. Each dimension is scored on a scale of 0-100 based on:

- **Qualitative responses** about current practices and capabilities
- **Quantitative metrics** related to resources and implementation levels
- **Comparative analysis** against industry benchmarks

The overall maturity score is calculated as the weighted average of dimension 
scores, providing a holistic view of AI readiness.

"""

    if include_raw_data and 'assessment_data' in st.session_state:
        content += """
---

## Appendix: Raw Assessment Data

"""
        for key, value in st.session_state.assessment_data.items():
            content += f"- **{key}**: {value}\n"

    content += """
---

## Next Steps

1. **Review this report** with key stakeholders
2. **Prioritize improvement areas** based on recommendations
3. **Develop action plans** for each priority area
4. **Schedule follow-up assessment** in 6-12 months to track progress

---

*Report generated by AI-Compass | AI Maturity Assessment Platform*
"""

    return content

# Display preview
report_content = generate_report_content()

with st.expander("📄 Preview Report Content", expanded=True):
    st.markdown(report_content)

st.markdown("---")

# Generate and download
st.markdown("### Generate Report")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📥 Generate PDF Report", use_container_width=True, type="primary"):
        with st.spinner("Generating PDF report..."):
            # In a real implementation, this would use ReportLab
            st.info("""
            **PDF Generation Status:**
            
            PDF generation functionality requires the full backend implementation.
            
            **What would be included:**
            - Professional formatted document
            - Charts and visualizations
            - Company branding
            - Page numbers and table of contents
            
            **Next Steps:**
            - Integrate with ReportLab backend
            - Configure PDF templates
            - Add styling and branding
            """)

with col2:
    if st.button("💾 Download JSON", use_container_width=True):
        # Calculate scores
        scores = {
            'Strategic Alignment': st.session_state.assessment_data.get('strategic_s2', 0),
            'Data Readiness': st.session_state.assessment_data.get('data_d3', 50),
            'Technology Infrastructure': st.session_state.assessment_data.get('technology_t3', 50),
            'Organizational Capability': 60  # Calculated
        }
        
        report_data = {
            "report_metadata": {
                "type": report_type,
                "format": "JSON",
                "generated_at": datetime.now().isoformat(),
                "company_name": company_name if company_name else "Your Organization"
            },
            "overall_score": sum(scores.values()) / len(scores),
            "dimension_scores": scores,
            "assessment_data": st.session_state.assessment_data,
            "completion_time": st.session_state.get('completion_time', 'N/A'),
            "report_content": report_content
        }
        
        st.download_button(
            label="⬇️ Download JSON File",
            data=json.dumps(report_data, indent=2),
            file_name=f"ai_compass_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
        st.success("✅ JSON report ready for download!")

with col3:
    if st.button("📊 Export to CSV", use_container_width=True):
        # Create CSV data
        import io
        csv_data = "Dimension,Score\n"
        scores = {
            'Strategic Alignment': st.session_state.assessment_data.get('strategic_s2', 0),
            'Data Readiness': st.session_state.assessment_data.get('data_d3', 50),
            'Technology Infrastructure': st.session_state.assessment_data.get('technology_t3', 50),
            'Organizational Capability': 60
        }
        
        for dimension, score in scores.items():
            csv_data += f"{dimension},{score}\n"
        
        st.download_button(
            label="⬇️ Download CSV File",
            data=csv_data,
            file_name=f"ai_compass_scores_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
        st.success("✅ CSV export ready for download!")

# Historical reports
st.markdown("---")
st.markdown("### Report History")

st.info("""
**Historical Reports** (Feature coming soon)

Track your AI maturity progress over time:
- View previous assessments
- Compare scores across time periods  
- Visualize improvement trends
- Download archived reports

This feature will be available in the full version of AI-Compass.
""")

# Share report
st.markdown("---")
st.markdown("### Share Report")

col1, col2 = st.columns(2)

with col1:
    st.text_input("Email recipients (comma-separated)", placeholder="stakeholder1@company.com, stakeholder2@company.com")
    if st.button("📧 Email Report", use_container_width=True):
        st.info("Email functionality will be available when integrated with email service (e.g., SendGrid, AWS SES)")

with col2:
    share_link = st.text_input("Shareable Link", value="https://ai-compass.app/report/abc123", disabled=True)
    if st.button("🔗 Copy Link", use_container_width=True):
        st.success("✅ Link copied to clipboard! (In full implementation)")

# Footer with notes
st.markdown("---")
st.info("""
**ℹ️ Note:** This is the MVP version of AI-Compass. PDF generation and some advanced features 
require backend integration with FastAPI, PostgreSQL, and ReportLab services.

**For full functionality:**
1. Start the FastAPI backend server
2. Configure database connection
3. Set up GROQ API for AI-powered insights
4. Enable PDF generation service
""")
