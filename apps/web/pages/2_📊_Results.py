import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Results", page_icon="📊", layout="wide")

st.title("📊 Assessment Results")

# Check if assessment is completed
if 'assessment_completed' not in st.session_state or not st.session_state.assessment_completed:
    st.warning("⚠️ You haven't completed the assessment yet. Please go to the Assessment page first.")
    st.stop()

# Calculate scores based on assessment data
def calculate_scores():
    """Calculate maturity scores from assessment data"""
    scores = {}
    
    # Strategic Alignment Score
    strategic_score = 0
    if 'strategic_s1' in st.session_state.assessment_data:
        s1_value = st.session_state.assessment_data['strategic_s1']
        strategic_map = {"No strategy": 0, "Informal strategy": 33, "Documented strategy": 67, "Well-integrated strategy": 100}
        strategic_score += strategic_map.get(s1_value, 0) * 0.5
    
    if 'strategic_s2' in st.session_state.assessment_data:
        strategic_score += st.session_state.assessment_data['strategic_s2'] * 0.5
    
    scores['Strategic Alignment'] = min(100, strategic_score)
    
    # Data Readiness Score
    data_score = 0
    if 'data_d1' in st.session_state.assessment_data:
        d1_value = st.session_state.assessment_data['data_d1']
        data_map = {"Poor": 0, "Fair": 33, "Good": 67, "Excellent": 100}
        data_score += data_map.get(d1_value, 0) * 0.4
    
    if 'data_d2' in st.session_state.assessment_data:
        d2_value = st.session_state.assessment_data['data_d2']
        governance_map = {"No": 0, "In development": 33, "Partially implemented": 67, "Fully implemented": 100}
        data_score += governance_map.get(d2_value, 0) * 0.3
    
    if 'data_d3' in st.session_state.assessment_data:
        data_score += st.session_state.assessment_data['data_d3'] * 0.3
    
    scores['Data Readiness'] = min(100, data_score)
    
    # Technology Infrastructure Score
    tech_score = 0
    if 'technology_t2' in st.session_state.assessment_data:
        t2_value = st.session_state.assessment_data['technology_t2']
        mlops_map = {"No": 0, "Planning": 25, "Basic implementation": 60, "Advanced implementation": 100}
        tech_score += mlops_map.get(t2_value, 0) * 0.5
    
    if 'technology_t3' in st.session_state.assessment_data:
        tech_score += st.session_state.assessment_data['technology_t3'] * 0.5
    
    scores['Technology Infrastructure'] = min(100, tech_score)
    
    # Organizational Capability Score
    org_score = 0
    if 'organization_o2' in st.session_state.assessment_data:
        o2_value = st.session_state.assessment_data['organization_o2']
        team_map = {"No": 0, "Ad-hoc team": 33, "Dedicated team": 67, "Center of Excellence": 100}
        org_score += team_map.get(o2_value, 0) * 0.5
    
    if 'organization_o3' in st.session_state.assessment_data:
        o3_value = st.session_state.assessment_data['organization_o3']
        training_map = {"None": 0, "Occasional training": 33, "Regular programs": 67, "Comprehensive learning culture": 100}
        org_score += training_map.get(o3_value, 0) * 0.5
    
    scores['Organizational Capability'] = min(100, org_score)
    
    return scores

# Calculate scores
scores = calculate_scores()
overall_score = sum(scores.values()) / len(scores) if scores else 0

# Determine maturity level
def get_maturity_level(score):
    if score < 25:
        return "Initial", "🔴", "Just starting the AI journey"
    elif score < 50:
        return "Developing", "🟡", "Building AI capabilities"
    elif score < 75:
        return "Defined", "🟢", "Established AI practices"
    else:
        return "Optimized", "🔵", "Advanced AI maturity"

maturity_level, level_icon, level_desc = get_maturity_level(overall_score)

# Display overall score
st.markdown("### Overall AI Maturity Score")
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    # Gauge chart for overall score
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=overall_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Overall Maturity", 'font': {'size': 24}},
        delta={'reference': 50, 'increasing': {'color': "green"}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 25], 'color': '#ffcccc'},
                {'range': [25, 50], 'color': '#ffffcc'},
                {'range': [50, 75], 'color': '#ccffcc'},
                {'range': [75, 100], 'color': '#ccccff'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': overall_score
            }
        }
    ))
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.metric(label="Maturity Level", value=maturity_level, delta=level_desc)
    st.write(f"{level_icon} **{maturity_level}**")

with col3:
    st.metric(label="Overall Score", value=f"{overall_score:.1f}/100")
    if 'completion_time' in st.session_state:
        st.caption(f"Completed: {st.session_state.completion_time}")

st.markdown("---")

# Dimension scores
st.markdown("### Scores by Dimension")

col1, col2 = st.columns(2)

with col1:
    # Radar chart
    categories = list(scores.keys())
    values = list(scores.values())
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Your Score'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=False,
        title="Maturity Dimensions",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Bar chart
    df_scores = pd.DataFrame({
        'Dimension': categories,
        'Score': values
    })
    
    fig = px.bar(
        df_scores,
        x='Score',
        y='Dimension',
        orientation='h',
        title='Dimension Scores',
        color='Score',
        color_continuous_scale='Blues',
        range_x=[0, 100]
    )
    fig.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# Detailed scores
st.markdown("### Detailed Breakdown")

for dimension, score in scores.items():
    with st.expander(f"{dimension}: {score:.1f}/100"):
        # Progress bar
        st.progress(score / 100)
        
        # Interpretation
        if score < 25:
            st.error("**Low maturity** - Significant improvement needed in this area")
        elif score < 50:
            st.warning("**Moderate maturity** - Good foundation, but room for growth")
        elif score < 75:
            st.info("**Good maturity** - Well-established practices")
        else:
            st.success("**Excellent maturity** - Leading practices in place")

# Recommendations
st.markdown("---")
st.markdown("### Key Recommendations")

recommendations = []

if scores.get('Strategic Alignment', 0) < 50:
    recommendations.append("**Strategic Alignment**: Develop a comprehensive AI strategy aligned with business objectives")

if scores.get('Data Readiness', 0) < 50:
    recommendations.append("**Data Readiness**: Invest in data governance and quality improvement initiatives")

if scores.get('Technology Infrastructure', 0) < 50:
    recommendations.append("**Technology Infrastructure**: Build robust MLOps capabilities and cloud infrastructure")

if scores.get('Organizational Capability', 0) < 50:
    recommendations.append("**Organizational Capability**: Expand AI talent and establish training programs")

if recommendations:
    for i, rec in enumerate(recommendations, 1):
        st.markdown(f"{i}. {rec}")
else:
    st.success("✅ Your organization demonstrates strong AI maturity across all dimensions! Focus on continuous improvement and innovation.")

# Export option
st.markdown("---")
st.markdown("### Export Results")

col1, col2 = st.columns(2)

with col1:
    if st.button("📄 Generate PDF Report", use_container_width=True):
        st.info("PDF generation will be available in the Reports page")

with col2:
    # Export as JSON
    if st.button("💾 Download as JSON", use_container_width=True):
        import json
        result_data = {
            "overall_score": overall_score,
            "maturity_level": maturity_level,
            "dimension_scores": scores,
            "completion_time": st.session_state.get('completion_time', 'N/A'),
            "assessment_data": st.session_state.assessment_data
        }
        st.download_button(
            label="Download JSON",
            data=json.dumps(result_data, indent=2),
            file_name="ai_compass_results.json",
            mime="application/json"
        )
