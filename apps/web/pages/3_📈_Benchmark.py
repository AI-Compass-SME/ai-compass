import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import requests
import os

st.set_page_config(page_title="Benchmark", page_icon="📈", layout="wide")

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("📈 Industry Benchmark Comparison")

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
with st.spinner("Lade Benchmark-Daten..."):
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
        
        # Check if results exist
        if not assessment_data.get("results"):
            st.error("Benchmark-Daten nicht verfügbar.")
            st.stop()
        
        # Store in session state for this page's use
        results = assessment_data["results"]
        
    except requests.exceptions.ConnectionError:
        st.error("🔌 Keine Verbindung zur API")
        st.stop()
    except Exception as e:
        st.error(f"Fehler: {str(e)}")
        st.stop()

# Mock industry data (in a real app, this would come from a database)
def get_industry_benchmarks():
    """Generate mock industry benchmark data"""
    industries = ['Financial Services', 'Healthcare', 'Retail', 'Manufacturing', 'Technology', 'Your Organization']
    
    # Use the actual 7 dimensions from the assessment
    dimensions = [
        'Strategy & Business Vision',
        'Data Maturity',
        'Tech Infrastructure', 
        'People & Culture',
        'Processes & Scaling',
        'Governance & Compliance',
        'Use Cases & Business Value'
    ]
    
    # Generate random benchmark data for industries
    np.random.seed(42)
    data = []
    
    for industry in industries[:-1]:  # Exclude 'Your Organization'
        for dimension in dimensions:
            # Different industries have different maturity levels
            if industry == 'Technology':
                base_score = np.random.uniform(70, 90)
            elif industry == 'Financial Services':
                base_score = np.random.uniform(60, 80)
            else:
                base_score = np.random.uniform(40, 70)
            
            data.append({
                'Industry': industry,
                'Dimension': dimension,
                'Score': base_score
            })
    
    return pd.DataFrame(data)

# Calculate user scores from actual assessment results
def get_user_scores(results_data):
    """Get user's scores from assessment results - all 7 dimensions"""
    scores = {}
    
    # Get dimension scores from results
    dimension_scores = results_data.get("dimension_scores", [])
    
    # Map each dimension by title to score
    for dim in dimension_scores:
        title = dim.get("title", "")
        score = dim.get("score_0_100", 0)
        scores[title] = score
    
    return scores

# Get benchmark data
benchmark_df = get_industry_benchmarks()
user_scores = get_user_scores(results)


# Add user data to benchmark
for dimension, score in user_scores.items():
    benchmark_df = pd.concat([
        benchmark_df,
        pd.DataFrame({
            'Industry': ['Your Organization'],
            'Dimension': [dimension],
            'Score': [score]
        })
    ], ignore_index=True)

# Introduction
st.markdown("""
Compare your AI maturity scores with industry benchmarks to understand your position 
and identify areas for improvement.
""")

# Industry selector
st.markdown("### Select Industries to Compare")
all_industries = benchmark_df['Industry'].unique().tolist()
all_industries.remove('Your Organization')

selected_industries = st.multiselect(
    "Choose industries:",
    options=all_industries,
    default=['Technology', 'Financial Services', 'Healthcare']
)

selected_industries.append('Your Organization')  # Always include user's org

# Filter data
filtered_df = benchmark_df[benchmark_df['Industry'].isin(selected_industries)]

st.markdown("---")

# Overall comparison
st.markdown("### Overall Maturity Comparison")

col1, col2 = st.columns(2)

with col1:
    # Box plot by dimension
    fig = px.box(
        filtered_df,
        x='Dimension',
        y='Score',
        color='Industry',
        title='Score Distribution by Dimension',
        points='all'
    )
    fig.update_layout(height=500, xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Calculate average scores per industry
    avg_scores = filtered_df.groupby('Industry')['Score'].mean().reset_index()
    avg_scores = avg_scores.sort_values('Score', ascending=True)
    
    fig = px.bar(
        avg_scores,
        x='Score',
        y='Industry',
        orientation='h',
        title='Average Maturity Score by Industry',
        color='Score',
        color_continuous_scale='Viridis',
        range_x=[0, 100]
    )
    
    # Highlight user's organization
    fig.update_traces(
        marker_line_width=3,
        marker_line_color=['red' if ind == 'Your Organization' else 'white' 
                          for ind in avg_scores['Industry']]
    )
    
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

# Dimension-by-dimension comparison
st.markdown("---")
st.markdown("### Dimension-by-Dimension Analysis")

dimensions = filtered_df['Dimension'].unique()

for dimension in dimensions:
    with st.expander(f"📊 {dimension}", expanded=False):
        dim_data = filtered_df[filtered_df['Dimension'] == dimension]
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Bar chart for this dimension
            fig = px.bar(
                dim_data,
                x='Industry',
                y='Score',
                title=f'{dimension} Scores',
                color='Industry',
                text='Score'
            )
            fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
            fig.update_layout(
                height=350,
                showlegend=False,
                yaxis_range=[0, 110]
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Statistics
            user_score = dim_data[dim_data['Industry'] == 'Your Organization']['Score'].values
            if len(user_score) > 0:
                user_score = user_score[0]
                industry_avg = dim_data[dim_data['Industry'] != 'Your Organization']['Score'].mean()
                industry_max = dim_data[dim_data['Industry'] != 'Your Organization']['Score'].max()
                
                st.metric(
                    label="Your Score",
                    value=f"{user_score:.1f}",
                    delta=f"{user_score - industry_avg:.1f} vs. avg"
                )
                
                st.metric(
                    label="Industry Average",
                    value=f"{industry_avg:.1f}"
                )
                
                st.metric(
                    label="Industry Leader",
                    value=f"{industry_max:.1f}"
                )
                
                # Gap analysis
                gap = industry_max - user_score
                if gap > 20:
                    st.error(f"⚠️ {gap:.1f} points behind leader")
                elif gap > 10:
                    st.warning(f"📊 {gap:.1f} points behind leader")
                else:
                    st.success(f"✅ Close to industry leader!")

# Percentile ranking
st.markdown("---")
st.markdown("### Your Percentile Ranking")

st.markdown("""
See where you stand compared to other organizations in each dimension.
""")

percentiles = []
for dimension in dimensions:
    dim_data = filtered_df[filtered_df['Dimension'] == dimension]
    user_score = dim_data[dim_data['Industry'] == 'Your Organization']['Score'].values
    
    if len(user_score) > 0:
        user_score = user_score[0]
        all_scores = dim_data['Score'].values
        percentile = (all_scores < user_score).sum() / len(all_scores) * 100
        percentiles.append({
            'Dimension': dimension,
            'Percentile': percentile
        })

percentile_df = pd.DataFrame(percentiles)

fig = px.bar(
    percentile_df,
    x='Percentile',
    y='Dimension',
    orientation='h',
    title='Your Percentile Ranking by Dimension',
    text='Percentile',
    color='Percentile',
    color_continuous_scale='RdYlGn',
    range_x=[0, 100]
)
fig.update_traces(texttemplate='%{text:.0f}th', textposition='outside')
fig.update_layout(height=400)
st.plotly_chart(fig, use_container_width=True)

# Gap analysis summary
st.markdown("---")
st.markdown("### Gap Analysis Summary")

gap_analysis = []
for dimension in dimensions:
    dim_data = filtered_df[filtered_df['Dimension'] == dimension]
    user_score = dim_data[dim_data['Industry'] == 'Your Organization']['Score'].values
    
    if len(user_score) > 0:
        user_score = user_score[0]
        industry_avg = dim_data[dim_data['Industry'] != 'Your Organization']['Score'].mean()
        gap = user_score - industry_avg
        
        gap_analysis.append({
            'Dimension': dimension,
            'Your Score': f"{user_score:.1f}",
            'Industry Avg': f"{industry_avg:.1f}",
            'Gap': f"{gap:+.1f}",
            'Status': '🟢 Above Avg' if gap > 0 else '🔴 Below Avg'
        })

gap_df = pd.DataFrame(gap_analysis)
st.dataframe(gap_df, use_container_width=True, hide_index=True)

# Action items
st.markdown("---")
st.markdown("### Recommended Actions")

# Identify lowest scoring dimensions
user_scores_list = [(dim, score) for dim, score in user_scores.items()]
user_scores_list.sort(key=lambda x: x[1])

st.markdown("Based on your benchmark comparison, focus on these priority areas:")

for i, (dimension, score) in enumerate(user_scores_list[:2], 1):
    dim_data = filtered_df[filtered_df['Dimension'] == dimension]
    industry_avg = dim_data[dim_data['Industry'] != 'Your Organization']['Score'].mean()
    
    st.markdown(f"""
**{i}. {dimension}** (Score: {score:.1f}, Industry Avg: {industry_avg:.1f})
- This dimension shows the largest opportunity for improvement
- Consider benchmarking best practices from leading organizations
- Develop a targeted improvement roadmap
    """)

# Export benchmark data
st.markdown("---")
if st.button("📥 Export Benchmark Report"):
    st.download_button(
        label="Download CSV",
        data=filtered_df.to_csv(index=False),
        file_name="benchmark_comparison.csv",
        mime="text/csv"
    )
