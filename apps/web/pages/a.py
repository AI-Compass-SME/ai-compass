import streamlit as st
import json
from datetime import datetime

st.set_page_config(page_title="Assessment", page_icon="📋", layout="wide")

st.title("📋 AI Maturity Assessment")

st.markdown("""
Answer the following questions to evaluate your organization's AI maturity level.
Your responses will be used to generate a comprehensive maturity score.
""")

# Initialize session state
if 'assessment_data' not in st.session_state:
    st.session_state.assessment_data = {}

if 'current_section' not in st.session_state:
    st.session_state.current_section = 0

# Define assessment sections and questions
ASSESSMENT_SECTIONS = [
    {
        "title": "Strategic Alignment",
        "key": "strategic",
        "questions": [
            {
                "id": "s1",
                "question": "Does your organization have a defined AI strategy?",
                "type": "radio",
                "options": ["No strategy", "Informal strategy", "Documented strategy", "Well-integrated strategy"]
            },
            {
                "id": "s2",
                "question": "How aligned is AI with your business objectives?",
                "type": "slider",
                "min": 0,
                "max": 100
            },
            {
                "id": "s3",
                "question": "What are your primary AI use cases? (Select all that apply)",
                "type": "multiselect",
                "options": ["Customer Service", "Process Automation", "Predictive Analytics", "Product Development", "Risk Management"]
            }
        ]
    },
    {
        "title": "Data Readiness",
        "key": "data",
        "questions": [
            {
                "id": "d1",
                "question": "How would you rate your data quality?",
                "type": "radio",
                "options": ["Poor", "Fair", "Good", "Excellent"]
            },
            {
                "id": "d2",
                "question": "Do you have a data governance framework?",
                "type": "radio",
                "options": ["No", "In development", "Partially implemented", "Fully implemented"]
            },
            {
                "id": "d3",
                "question": "What percentage of your data is structured?",
                "type": "slider",
                "min": 0,
                "max": 100
            }
        ]
    },
    {
        "title": "Technology Infrastructure",
        "key": "technology",
        "questions": [
            {
                "id": "t1",
                "question": "What cloud infrastructure do you use for AI workloads?",
                "type": "multiselect",
                "options": ["AWS", "Azure", "GCP", "On-premise", "Hybrid", "None"]
            },
            {
                "id": "t2",
                "question": "Do you have MLOps practices in place?",
                "type": "radio",
                "options": ["No", "Planning", "Basic implementation", "Advanced implementation"]
            },
            {
                "id": "t3",
                "question": "Rate your model deployment capability",
                "type": "slider",
                "min": 0,
                "max": 100
            }
        ]
    },
    {
        "title": "Organizational Capability",
        "key": "organization",
        "questions": [
            {
                "id": "o1",
                "question": "How many AI/ML specialists do you have?",
                "type": "number",
                "min": 0
            },
            {
                "id": "o2",
                "question": "Do you have dedicated AI/ML teams?",
                "type": "radio",
                "options": ["No", "Ad-hoc team", "Dedicated team", "Center of Excellence"]
            },
            {
                "id": "o3",
                "question": "What is your AI training and upskilling approach?",
                "type": "radio",
                "options": ["None", "Occasional training", "Regular programs", "Comprehensive learning culture"]
            }
        ]
    }
]

# Display progress
progress = (st.session_state.current_section + 1) / len(ASSESSMENT_SECTIONS)
st.progress(progress)
st.write(f"Section {st.session_state.current_section + 1} of {len(ASSESSMENT_SECTIONS)}")

# Display current section
current_section = ASSESSMENT_SECTIONS[st.session_state.current_section]
st.header(current_section["title"])

# Display questions
for question in current_section["questions"]:
    st.markdown(f"**{question['question']}**")
    
    key = f"{current_section['key']}_{question['id']}"
    
    if question["type"] == "radio":
        answer = st.radio(
            label=f"Select an option for {question['id']}",
            options=question["options"],
            key=key,
            label_visibility="collapsed"
        )
        st.session_state.assessment_data[key] = answer
        
    elif question["type"] == "slider":
        answer = st.slider(
            label=f"Slider for {question['id']}",
            min_value=question["min"],
            max_value=question["max"],
            value=st.session_state.assessment_data.get(key, 50),
            key=key,
            label_visibility="collapsed"
        )
        st.session_state.assessment_data[key] = answer
        
    elif question["type"] == "multiselect":
        answer = st.multiselect(
            label=f"Select options for {question['id']}",
            options=question["options"],
            default=st.session_state.assessment_data.get(key, []),
            key=key,
            label_visibility="collapsed"
        )
        st.session_state.assessment_data[key] = answer
        
    elif question["type"] == "number":
        answer = st.number_input(
            label=f"Enter number for {question['id']}",
            min_value=question["min"],
            value=st.session_state.assessment_data.get(key, 0),
            key=key,
            label_visibility="collapsed"
        )
        st.session_state.assessment_data[key] = answer
    
    st.markdown("---")

# Navigation buttons
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.session_state.current_section > 0:
        if st.button("⬅️ Previous", use_container_width=True):
            st.session_state.current_section -= 1
            st.rerun()

with col2:
    if st.button("💾 Save Progress", use_container_width=True):
        st.success("Progress saved!")

with col3:
    if st.session_state.current_section < len(ASSESSMENT_SECTIONS) - 1:
        if st.button("Next ➡️", use_container_width=True):
            st.session_state.current_section += 1
            st.rerun()
    else:
        if st.button("✅ Complete Assessment", use_container_width=True, type="primary"):
            st.session_state.assessment_completed = True
            st.session_state.completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.success("Assessment completed! Go to the Results page to view your score.")

# Show summary of answers
if st.expander("View Your Answers Summary"):
    for key, value in st.session_state.assessment_data.items():
        st.write(f"**{key}**: {value}")
