"""
Assessment Questionnaire Page
Multi-step wizard for answering questions across 7 dimensions.
"""
import streamlit as st
import requests
import os

st.set_page_config(page_title="Assessment", page_icon="📝", layout="wide")

API_URL = os.getenv("API_URL", "http://localhost:8000")

# Check if assessment_id exists
if "assessment_id" not in st.session_state:
    st.error("Kein Assessment gefunden. Bitte starten Sie ein neues Assessment.")
    if st.button("Zur Startseite"):
        st.switch_page("Home.py")
    st.stop()

assessment_id = st.session_state.assessment_id

# Initialize session state for responses
if "responses" not in st.session_state:
    st.session_state.responses = {}

if "current_dimension_idx" not in st.session_state:
    st.session_state.current_dimension_idx = 0

# Load questionnaire
@st.cache_data(ttl=3600)
def load_questionnaire():
    try:
        response = requests.get(f"{API_URL}/api/v1/questionnaire", timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

questionnaire_data = load_questionnaire()

if not questionnaire_data:
    st.error("Konnte Fragebogen nicht laden. Bitte überprüfen Sie die API-Verbindung.")
    st.stop()

schema = questionnaire_data["schema"]
dimensions = schema["dimensions"]
total_dimensions = len(dimensions)

# Header
st.markdown(f"### 📝 Assessment: {schema['title']}")
st.markdown(f"**Geschätzte Dauer:** {schema['estimated_time_minutes']} Minuten")
st.progress((st.session_state.current_dimension_idx + 1) / total_dimensions)
st.markdown("---")

# Get current dimension
current_dim = dimensions[st.session_state.current_dimension_idx]
dim_id = current_dim["id"]
dim_title = current_dim["title"]

st.markdown(f"## {dim_title}")
st.markdown(f"**Dimension {st.session_state.current_dimension_idx + 1} von {total_dimensions}**")
st.markdown("---")

# Display questions for current dimension
questions = current_dim["questions"]

# Form for this dimension
with st.form(key=f"dim_form_{dim_id}"):
    for question in questions:
        q_id = question["id"]
        q_text = question["text"]
        q_type = question["type"]
        render_mode = question.get("render", "radio")
        options = question["options"]
        
        st.markdown(f"**{q_text}**")
        
        # Get previous answer if exists
        previous_answer = st.session_state.responses.get(q_id, None)
        
        if q_type == "single_choice":
            if render_mode == "radio":
                # Radio buttons
                option_labels = [opt["label"] for opt in options]
                option_ids = [opt["id"] for opt in options]
                
                # Find default index
                default_idx = 0
                if previous_answer and previous_answer in option_ids:
                    default_idx = option_ids.index(previous_answer)
                
                selected_label = st.radio(
                    label=q_id,  # Hidden label
                    options=option_labels,
                    index=default_idx,
                    key=f"q_{q_id}",
                    label_visibility="collapsed"
                )
                
                # Map back to option ID
                selected_idx = option_labels.index(selected_label)
                st.session_state.responses[q_id] = option_ids[selected_idx]
            
            elif render_mode == "tags":
                # Tag-like buttons (using selectbox as fallback in Streamlit)
                option_labels = [opt["label"] for opt in options]
                option_ids = [opt["id"] for opt in options]
                
                default_idx = 0
                if previous_answer and previous_answer in option_ids:
                    default_idx = option_ids.index(previous_answer)
                
                selected_label = st.selectbox(
                    label=q_id,
                    options=option_labels,
                    index=default_idx,
                    key=f"q_{q_id}",
                    label_visibility="collapsed"
                )
                
                selected_idx = option_labels.index(selected_label)
                st.session_state.responses[q_id] = option_ids[selected_idx]
        
        st.markdown("---")
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        back_clicked = st.form_submit_button("← Zurück", use_container_width=True)
    
    with col2:
        save_clicked = st.form_submit_button("Speichern", use_container_width=True)
    
    with col3:
        if st.session_state.current_dimension_idx < total_dimensions - 1:
            next_clicked = st.form_submit_button("Weiter →", type="primary", use_container_width=True)
        else:
            next_clicked = st.form_submit_button("Zur Auswertung →", type="primary", use_container_width=True)
    
    # Handle navigation
    if back_clicked:
        if st.session_state.current_dimension_idx > 0:
            st.session_state.current_dimension_idx -= 1
            st.rerun()
    
    if save_clicked or next_clicked:
        # Prepare responses for current dimension
        responses_to_submit = []
        for question in questions:
            q_id = question["id"]
            if q_id in st.session_state.responses:
                selected_option_id = st.session_state.responses[q_id]
                responses_to_submit.append({
                    "dimension_id": dim_id,
                    "question_id": q_id,
                    "selected_option_ids": [selected_option_id]
                })
        
        # Submit to API
        if responses_to_submit:
            with st.spinner("Speichere Antworten..."):
                try:
                    response = requests.post(
                        f"{API_URL}/api/v1/assessments/{assessment_id}/responses",
                        json={"responses": responses_to_submit},
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        st.success("✓ Antworten gespeichert")
                        
                        # Move to next dimension if next was clicked
                        if next_clicked:
                            if st.session_state.current_dimension_idx < total_dimensions - 1:
                                st.session_state.current_dimension_idx += 1
                                st.rerun()
                            else:
                                # All dimensions completed - go to results
                                st.switch_page("pages/2_📊_Results.py")
                    else:
                        st.error(f"Fehler beim Speichern: {response.text}")
                
                except Exception as e:
                    st.error(f"Verbindungsfehler: {str(e)}")

# Sidebar
with st.sidebar:
    st.markdown(f"### 📋 Schritt 2/3")
    st.progress(0.66)
    st.markdown(f"""
    **Dimension {st.session_state.current_dimension_idx + 1}/{total_dimensions}**
    
    {dim_title}
    
    ---
    
    **Fortschritt gesamt:**
    """)
    
    # Show overall progress
    total_questions = sum(len(d["questions"]) for d in dimensions)
    answered_questions = len(st.session_state.responses)
    st.progress(answered_questions / total_questions if total_questions > 0 else 0)
    st.markdown(f"{answered_questions} / {total_questions} Fragen beantwortet")
