import streamlit as st

# Page configuration
st.set_page_config(
    page_title="AI-Compass - Home",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
- **📋 Assessment**: Take the AI maturity questionnaire
- **📊 Results**: View your assessment scores and insights
- **📈 Benchmark**: Compare with industry peers
- **📄 Reports**: Generate and download PDF reports
""")

# Quick stats or features
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Assessment Questions", value="50+", delta="Comprehensive")

with col2:
    st.metric(label="Maturity Dimensions", value="8", delta="Multi-faceted")

with col3:
    st.metric(label="Avg. Completion Time", value="15 min", delta="Quick & Easy")

# Call to action
st.markdown("---")
st.markdown("### Ready to get started?")
st.markdown("Navigate to the **Assessment** page to begin your AI maturity journey!")

# Footer
st.markdown("---")
st.caption("AI-Compass MVP | Powered by Streamlit")
