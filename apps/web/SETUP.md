# AI-Compass Streamlit App - Setup & Run Instructions

## ✅ What Was Created

A complete Streamlit multipage web application with 5 pages:

1. **Home.py** - Landing page with overview and navigation
2. **1_📋_Assessment.py** - Multi-section AI maturity questionnaire
3. **2_📊_Results.py** - Score calculations with visualizations (gauge, radar, bar charts)
4. **3_📈_Benchmark.py** - Industry comparison and gap analysis
5. **4_📄_Reports.py** - Report generation and export (JSON, CSV)

## 📂 File Structure

```
ai-compass/
├── apps/web/
│   ├── Home.py                    # Main entry point
│   ├── pages/
│   │   ├── 1_📋_Assessment.py
│   │   ├── 2_📊_Results.py
│   │   ├── 3_📈_Benchmark.py
│   │   └── 4_📄_Reports.py
│   ├── run.sh                     # Run script
│   └── README.md                  # Detailed documentation
└── requirements.txt               # Updated with pytest fix
```

## 🚀 How to Run

###  Step 1: Install Dependencies

The app needs these Python packages:
- streamlit (web framework)
- pandas (data handling)
- plotly (visualizations)
- numpy (calculations)

**Option A: Install all project dependencies**
```bash
cd /home/sinai/bootcamp/capstone/ai-compass
pip install -r requirements.txt
```

**Option B: Install just what's needed for Streamlit**
```bash
pip install streamlit pandas plotly numpy
```

### Step 2: Run the Application

```bash
cd /home/sinai/bootcamp/capstone/ai-compass/apps/web
streamlit run Home.py
```

Or use the run script:
```bash
cd /home/sinai/bootcamp/capstone/ai-compass/apps/web
chmod +x run.sh
./run.sh
```

### Step 3: Open in Browser

The app will automatically open at: **http://localhost:8501**

If it doesn't open automatically, navigate to that URL in your browser.

## 🎯 How to Use the App

1. **Home Page** - Read the overview
2. **Assessment** - Answer questions across 4 sections:
   - Strategic Alignment
   - Data Readiness
   - Technology Infrastructure
   - Organizational Capability
3. **Results** - View your maturity scores and recommendations
4. **Benchmark** - Compare with industry peers
5. **Reports** - Generate and download reports in JSON or CSV format

## 🔧 Fixed Issues

- ✅ Fixed `requirements.txt` dependency conflict (pytest 8.0.0 → 7.4.4)
- ✅ Created complete multipage Streamlit app
- ✅ Added session state management for data persistence
- ✅ Included interactive visualizations (Plotly charts)
- ✅ Implemented scoring logic
- ✅ Added export functionality (JSON, CSV)

## 📝 Features

### Assessment Page
- Multi-section questionnaire with progress tracking
- Various input types: radio buttons, sliders, multiselect, number inputs
- Session state saves progress
- Navigation between sections

### Results Page
- Overall maturity score with gauge chart
- Maturity level classification (Initial, Developing, Defined, Optimized)
- Radar chart for dimension comparison
- Bar charts for scores
- Personalized recommendations
- JSON export option

### Benchmark Page
- Compare scores with mock industry data
- Multiple visualization types (box plots, bar charts)
- Percentile ranking
- Gap analysis with actionable insights
- CSV export

### Reports Page
- Customizable report options
- Report preview
- Multiple export formats
- Metadata inclusion options

## ⚠️ Note

This is a **standalone MVP version** that works without the backend. For full functionality:

- **PDF generation** requires FastAPI + ReportLab integration
- **Persistent storage** requires PostgreSQL database
- **AI insights** require GROQ API integration
- **Email sharing** requires email service integration

The current version uses:
- Session state for temporary data storage
- Mock data for industry benchmarks
- Client-side calculations for scoring

## 🐛 Troubleshooting

**"streamlit: command not found"**
```bash
pip install streamlit
# or
pip3 install streamlit
```

**"Port already in use"**
```bash
streamlit run Home.py --server.port=8502
```

**Dependencies not installing**
Check your Python/pip version:
```bash
python3 --version
pip3 --version
```

## 📈 Next Steps

To enhance the app:
1. Integrate with FastAPI backend (`apps/api/`)
2. Connect to PostgreSQL for data persistence
3. Implement real PDF generation with ReportLab
4. Add GROQ API for AI-powered recommendations
5. Add user authentication
6. Store historical assessments
7. Add more assessment questions
8. Customize scoring algorithms

## 📚 Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Plotly Charts](https://plotly.com/python/)
- Project README: `../../README.md`
- API Reference: `../../API_REFERENCE.md`
