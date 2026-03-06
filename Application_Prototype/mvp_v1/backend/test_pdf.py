import os
from services.pdf_service import PDFService

# Mock Data
mock_data = {
    "company": {"name": "Test Firma GmbH"},
    "overall_score": 3.8,
    "percentile": {"percentage": 85, "industry": "Marketing"},
    "cluster": {"cluster_name": "1 - Traditionalist"},
    "dimension_scores": {"Strategy": 4.1, "Technology": 3.2, "People": 3.9},
    "executive_briefing": "Das ist ein Testbericht für KI-Kompass. **Wichtige Erkenntnisse** sind hier zu finden.",
    "strategic_gaps": [
        {
            "type": "Critical Weakness",
            "title": "Data Infrastructure Gap",
            "score": 1.5,
            "context": "Cloud ist nicht vorhanden.",
            "strategic_risk": "Langsame Integration"
        }
    ],
    "roadmap": {
        "Phase 1": [
            {
                "theme": "Cloud Migration",
                "explanation": "Analysis: Needs complete shift.\nAction 1: Setup AWS"
            }
        ]
    }
}

service = PDFService()
try:
    pdf_bytes_en = service.generate_pdf(mock_data, lang='en')
    with open('test_en.pdf', 'wb') as f:
        f.write(pdf_bytes_en)
    print("Generated English PDF.")
    
    pdf_bytes_de = service.generate_pdf(mock_data, lang='de')
    with open('test_de.pdf', 'wb') as f:
        f.write(pdf_bytes_de)
    print("Generated German PDF.")
except Exception as e:
    import traceback
    traceback.print_exc()
