import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from services.pdf_service import PDFService

# Mock Data
mock_data = {
    "company": {"name": "Test Company"},
    "overall_score": 3.5,
    "percentile": {"percentage": 15, "industry": "Tech"},
    "cluster": {"cluster_name": "3 - Builder", "description": "A builder company."},
    "executive_briefing": "This is a test briefing.",
    "strategic_gaps": [
        {"title": "Test Gap", "score": 4.5, "type": "Critical Weakness", "context": "Context here", "strategic_risk": "High Risk"}
    ],
    "dimension_scores": {"Dim 1": 3.0, "Dim 2": 4.0},
    "roadmap": {
        "Phase 1": [{"theme": "Theme A", "explanation": "**Analysis**: Test.\n- **Action 1**: Do this."}]
    }
}

try:
    print("Initializing PDF Service...")
    service = PDFService()
    print("Generating PDF...")
    pdf_bytes = service.generate_pdf(mock_data)
    print(f"Success! PDF bytes: {len(pdf_bytes)}")
    with open("debug_output.pdf", "wb") as f:
        f.write(pdf_bytes)
except Exception as e:
    print("ERROR:")
    import traceback
    traceback.print_exc()
