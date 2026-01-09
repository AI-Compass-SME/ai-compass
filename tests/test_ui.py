from streamlit.testing.v1 import AppTest
import os

def test_ui_loads():
    """Test that the Streamlit app loads without errors."""
    # Correct path to the app file relative to the project root
    app_path = os.path.join(os.path.dirname(__file__), "../apps/web/main.py")
    
    # Initialize the app
    at = AppTest.from_file(app_path)
    
    # Run the app
    at.run()
    
    # Assert successful run (no exceptions) and title check
    assert not at.exception
    assert "AI Compass" in at.title[0].value
