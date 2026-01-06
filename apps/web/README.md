# AI-Compass Streamlit Application

A multipage Streamlit application for AI maturity assessment.

## 📋 Features

### Pages

1. **🏠 Home** (`Home.py`)
   - Welcome page with overview
   - Quick stats and metrics
   - Navigation guidance

2. **📋 Assessment** (`pages/1_📋_Assessment.py`)
   - Multi-section questionnaire
   - 4 dimensions: Strategic Alignment, Data Readiness, Technology Infrastructure, Organizational Capability
   - Progress tracking
   - Session state management
   - Multiple question types (radio, slider, multiselect, number input)

3. **📊 Results** (`pages/2_📊_Results.py`)
   - Overall maturity score with gauge chart
   - Maturity level determination
   - Dimension scores with radar and bar charts
   - Detailed breakdowns
   - Recommendations based on scores
   - Export options (JSON)

4. **📈 Benchmark** (`pages/3_📈_Benchmark.py`)
   - Industry comparison
   - Box plots and bar charts
   - Percentile rankings
   - Gap analysis
   - Action items
   - CSV export

5. **📄 Reports** (`pages/4_📄_Reports.py`)
   - Report generation interface
   - Multiple report types
   - Customization options
   - Preview functionality
   - Export formats: PDF (placeholder), JSON, CSV
   - Share options (placeholder for email/link)

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- pip package manager

### Installation

1. Install dependencies:
```bash
pip install -r ../../requirements.txt
```

Or install just the core Streamlit requirements:
```bash
pip install streamlit pandas plotly numpy
```

### Running the App

#### Option 1: Using the run script (Linux/Mac/WSL)
```bash
chmod +x run.sh
./run.sh
```

#### Option 2: Direct command
```bash
streamlit run Home.py
```

#### Option 3: Custom port
```bash
streamlit run Home.py --server.port=8501
```

The app will open in your default browser at `http://localhost:8501`

## 📁 Project Structure

```
apps/web/
├── Home.py                          # Main entry point
├── pages/
│   ├── 1_📋_Assessment.py          # Assessment questionnaire
│   ├── 2_📊_Results.py             # Results and scoring
│   ├── 3_📈_Benchmark.py           # Industry benchmarks
│   └── 4_📄_Reports.py             # Report generation
├── run.sh                           # Run script
└── README.md                        # This file
```

## 🎯 Usage Flow

1. **Start on Home page** - Get an overview of the tool
2. **Go to Assessment** - Complete the multi-section questionnaire
3. **View Results** - See your scores and recommendations
4. **Check Benchmarks** - Compare with industry peers
5. **Generate Reports** - Export your results

## 🔧 Technical Details

### Dependencies

- **streamlit** - Web framework
- **pandas** - Data manipulation
- **plotly** - Interactive visualizations
- **numpy** - Numerical operations

### Session State

The app uses Streamlit's session state to:
- Store assessment answers (`assessment_data`)
- Track current section (`current_section`)
- Mark completion status (`assessment_completed`)
- Record completion time (`completion_time`)

### Data Flow

1. User completes assessment → Data stored in `st.session_state.assessment_data`
2. Results page calculates scores from assessment data
3. Benchmark page compares scores with mock industry data
4. Reports page generates downloadable reports

## 🎨 Customization

### Adding Questions

Edit `ASSESSMENT_SECTIONS` in `pages/1_📋_Assessment.py`:

```python
{
    "title": "New Section",
    "key": "section_key",
    "questions": [
        {
            "id": "q1",
            "question": "Your question?",
            "type": "radio",  # or "slider", "multiselect", "number"
            "options": ["Option 1", "Option 2"]
        }
    ]
}
```

### Modifying Scoring Logic

Update the `calculate_scores()` function in `pages/2_📊_Results.py`

### Changing Styling

Add custom CSS in any page:

```python
st.markdown("""
<style>
    /* Your custom CSS */
</style>
""", unsafe_allow_html=True)
```

## 🔗 Integration Points

This MVP Streamlit app is designed to work standalone, but can be integrated with:

- **FastAPI Backend** - For persistent storage and advanced features
- **PostgreSQL Database** - Store assessments and historical data
- **GROQ API** - AI-powered insights and recommendations
- **ReportLab** - PDF report generation

See the main project README for full-stack integration instructions.

## 📝 Notes

- This is an MVP version with mock/calculated data
- PDF generation shows placeholder (requires backend integration)
- Industry benchmarks use generated data (can be replaced with real data from API)
- Email and share features are placeholders

## 🐛 Troubleshooting

**App won't start:**
- Check Python version: `python3 --version`
- Install dependencies: `pip install streamlit`
- Try running directly: `streamlit run Home.py`

**Port already in use:**
```bash
streamlit run Home.py --server.port=8502
```

**Data not persisting:**
- This is expected - session state is browser-session only
- For persistence, integrate with backend database

## 📄 License

Part of the AI-Compass MVP project.
