import streamlit as st

def main():
    st.set_page_config(page_title="AI Compass", page_icon="🧭")
    
    st.title("AI Compass 🧭")
    st.subheader("Navigating AI Maturity for SMEs")
    
    st.write("""
    Welcome to AI Compass! This tool helps you assess your organization's AI readiness.
    """)
    
    if st.button("Start Assessment"):
        st.info("Assessment flow coming soon...")

if __name__ == "__main__":
    main()
    print("ci test")
