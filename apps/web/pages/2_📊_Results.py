"""
Results Dashboard
Displays overall score, dimension scores, charts, benchmark, and recommendations.
"""
import streamlit as st
import requests
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Results", page_icon="📊", layout="wide")

API_URL = os.getenv("API_URL", "http://localhost:8000")

# Check if assessment_id exists
if "assessment_id" not in st.session_state:
    st.error("Kein Assessment gefunden.")
    if st.button("Zur Startseite"):
        st.switch_page("Home.py")
    st.stop()

assessment_id = st.session_state.assessment_id

# Complete assessment if not already done
if "results" not in st.session_state:
    with st.spinner("Berechne Ergebnisse..."):
        try:
            response = requests.post(
                f"{API_URL}/api/v1/assessments/{assessment_id}/complete",
                timeout=30
            )
            
            if response.status_code == 200:
                st.session_state.results = response.json()
            else:
                st.error(f"Fehler bei der Auswertung: {response.text}")
                st.stop()
        
        except Exception as e:
            st.error(f"Verbindungsfehler: {str(e)}")
            st.stop()

results = st.session_state.results

# Header
st.markdown("# 📊 Ihre AI-Compass Ergebnisse")
st.markdown("---")

# Overall Score
st.markdown("## 🎯 Gesamtergebnis")
col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    overall_score = results["overall"]["score_0_100"]
    st.metric(
        label="Gesamtscore",
        value=f"{overall_score:.1f}",
        delta="/ 100"
    )

with col2:
    overall_level = results["overall"]["level_1_5"]
    st.metric(
        label="Reifestufe",
        value=f"{overall_level}",
        delta="/ 5"
    )

with col3:
    # Level description
    level_descriptions = {
        1: "🟥 Beginner – Erste Schritte",
        2: "🟧 Explorierend – Grundlagen vorhanden",
        3: "🟨 Etabliert – Strukturierte Ansätze",
        4: "🟩 Fortgeschritten – Best Practices",
        5: "🟦 Führend – Weltklasse"
    }
    st.info(level_descriptions.get(overall_level, "N/A"))

st.markdown("---")

# Dimension Scores Table
st.markdown("## 📈 Reife nach Dimensionen")

dimension_scores = results["dimension_scores"]

# Create table data
table_data = []
for dim in dimension_scores:
    table_data.append({
        "Dimension": dim["title"],
        "Score": f"{dim['score_0_100']:.1f}",
        "Level": f"{dim['level_1_5']}/5"
    })

st.table(table_data)

st.markdown("---")

# Charts
st.markdown("## 📊 Visualisierungen")

chart_data = results["chart_data"]

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Radar Chart (Alle Dimensionen)")
    
    # Radar chart
    radar_fig = go.Figure()
    
    radar_fig.add_trace(go.Scatterpolar(
        r=chart_data["radar"]["values"],
        theta=chart_data["radar"]["labels"],
        fill='toself',
        name='Ihr Unternehmen',
        line=dict(color='#1f77b4', width=2),
        fillcolor='rgba(31, 119, 180, 0.3)'
    ))
    
    radar_fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=False,
        height=400
    )
    
    st.plotly_chart(radar_fig, use_container_width=True)

with col2:
    st.markdown("### Bar Chart (Sortiert)")
    
    # Bar chart
    bar_fig = go.Figure()
    
    bar_fig.add_trace(go.Bar(
        x=chart_data["bars"]["values"],
        y=chart_data["bars"]["labels"],
        orientation='h',
        marker=dict(
            color=chart_data["bars"]["values"],
            colorscale='RdYlGn',
            cmin=0,
            cmax=100
        ),
        text=[f"{v:.1f}" for v in chart_data["bars"]["values"]],
        textposition='outside'
    ))
    
    bar_fig.update_layout(
        xaxis=dict(range=[0, 110], title="Score"),
        yaxis=dict(title=""),
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(bar_fig, use_container_width=True)

st.markdown("---")

# Focus Areas (lowest scoring dimensions)
st.markdown("## 🎯 Top Handlungsfelder")
st.markdown("Die drei Dimensionen mit dem größten Verbesserungspotenzial:")

sorted_dims = sorted(dimension_scores, key=lambda x: x["score_0_100"])
focus_areas = sorted_dims[:3]

for idx, dim in enumerate(focus_areas, 1):
    with st.expander(f"{idx}. {dim['title']} (Score: {dim['score_0_100']:.1f})"):
        st.markdown("**Warum?**")
        drivers = dim.get("drivers", [])
        if drivers:
            for driver in drivers:
                st.markdown(f"- **{driver['question_text']}**  \n  Antwort: _{driver['selected_label']}_ ({driver['points']} Punkte)")
        else:
            st.markdown("Keine Details verfügbar.")

st.markdown("---")

# Benchmark
st.markdown("## 🏆 Benchmark-Vergleich")

benchmark = results["benchmark"]
cluster_label = benchmark["cluster_label"]
percentile = benchmark["percentile"]
mismatch_flag = benchmark["mismatch_flag"]
mismatch_note = benchmark.get("mismatch_note")

col1, col2 = st.columns(2)

with col1:
    st.metric(label="Cluster", value=cluster_label)

with col2:
    st.metric(label="Perzentil", value=f"{percentile:.0f}%")

if mismatch_flag and mismatch_note:
    st.warning(f"**Hinweis:** {mismatch_note}")

st.markdown("---")

# Recommendations
st.markdown("## 💡 Empfehlungen")

recommendations = results["recommendations"]

# Executive Summary
st.markdown("### Zusammenfassung")
st.info(recommendations["executive_summary"])

# Quick Wins
st.markdown("### 🚀 Quick Wins (0–30 Tage)")
for item in recommendations["quick_wins"]:
    st.markdown(f"- {item}")

# Roadmap
st.markdown("### 🗺️ Roadmap")

roadmap = recommendations["roadmap"]

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**90 Tage**")
    for item in roadmap.get("days_90", []):
        st.markdown(f"- {item}")

with col2:
    st.markdown("**6 Monate**")
    for item in roadmap.get("months_6", []):
        st.markdown(f"- {item}")

with col3:
    st.markdown("**12 Monate**")
    for item in roadmap.get("months_12", []):
        st.markdown(f"- {item}")

# Risks
st.markdown("### ⚠️ Hauptrisiken")
for item in recommendations["risks"]:
    st.markdown(f"- {item}")

st.markdown("---")

# PDF Download
st.markdown("## 📄 PDF-Report")
st.markdown("Laden Sie einen vollständigen PDF-Bericht Ihrer Ergebnisse herunter.")

if st.button("📥 PDF herunterladen", type="primary"):
    with st.spinner("Erstelle PDF..."):
        try:
            response = requests.get(
                f"{API_URL}/api/v1/assessments/{assessment_id}/pdf",
                timeout=30
            )
            
            if response.status_code == 200:
                st.download_button(
                    label="💾 PDF speichern",
                    data=response.content,
                    file_name=f"ai-compass-report-{assessment_id}.pdf",
                    mime="application/pdf"
                )
            else:
                st.error(f"Fehler beim Erstellen des PDFs: {response.text}")
        
        except Exception as e:
            st.error(f"Verbindungsfehler: {str(e)}")

# Sidebar
with st.sidebar:
    st.markdown("### 🎉 Schritt 3/3")
    st.progress(1.0)
    st.markdown("""
    **Assessment abgeschlossen!**
    
    Ihre Ergebnisse wurden erfolgreich berechnet.
    
    ---
    
    **Nächste Schritte:**
    - Ergebnisse ansehen
    - PDF herunterladen
    - Mit Team teilen
    - Roadmap umsetzen
    """)
    
    st.markdown("---")
    
    if st.button("🔄 Neues Assessment starten"):
        # Clear session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.switch_page("Home.py")
