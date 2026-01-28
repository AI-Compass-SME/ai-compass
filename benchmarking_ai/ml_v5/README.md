# AI Compass ML v5 - Machine Learning System

## Overview

The ML v5 system is a comprehensive machine learning pipeline that powers the AI Compass maturity assessment platform. It combines clustering, gap analysis, and recommendation generation to provide personalized AI transformation roadmaps for organizations.

---

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Model Components](#model-components)
3. [Training Pipeline](#training-pipeline)
4. [Inference Pipeline](#inference-pipeline)
5. [Complete Workflow](#complete-workflow)
6. [File Structure](#file-structure)
7. [API Integration](#api-integration)
8. [Frontend Integration](#frontend-integration)
9. [Data Schemas](#data-schemas)
10. [Deployment](#deployment)

---

## System Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                       ML v5 System                          │
│                                                             │
│  ┌────────────────┐   ┌─────────────────┐   ┌─────────────┐ │
│  │ Cluster Engine │   │  Strategic Gap  │   │ Roadmap Gen │ │
│  │    (K-Means)   │   │ Analyzer (Rule) │   │    (KNN)    │ │
│  └───────┬────────┘   └────────┬────────┘   └──────┬──────┘ │
│          │                     │                   │        │
│          └─────────────────────┼───────────────────┘        │
│                                │                            │
│                                ▼                            │
│                     ┌──────────────────┐                    │
│                     │ Inference Engine │                    │
│                     └────────┬─────────┘                    │
│                              │                              │
└──────────────────────────────┼──────────────────────────────┘
                               │
                               ▼
                     ┌───────────────────┐
                     │  FastAPI Backend  │
                     └─────────┬─────────┘
                               │
                               ▼
                     ┌───────────────────┐
                     │   React Frontend  │
                     └───────────────────┘
```

---

## Model Components

### 1. Cluster Engine (`ClusterEngine`)

**Purpose**: Segment companies into 5 maturity levels

**Algorithm**: K-Means Clustering (k=5)

**Input Features**: 7 dimension scores
- Strategy & Business Vision
- Data Readiness & Literacy
- Governance & Compliance
- People & Culture
- Processes & Scaling
- Tech Infrastructure
- Use Cases & Business Value

**Output**:
- Cluster ID (1-5)
- Cluster Name (e.g., "3 - Builder")
- Cluster Coordinates (centroid position)

**Maturity Levels**:
1. **Traditionalist** - Minimal AI adoption
2. **Explorer** - Early experimentation
3. **Builder** - Active development
4. **Scaler** - Scaling AI initiatives
5. **Leader** - AI-native organization

**Model Files**:
- `v5_kmeans.pkl` - Trained KMeans model
- `v5_scaler.pkl` - StandardScaler for normalization

---

### 2. Strategic Gap Analyzer (`StrategicGapAnalyzer`)

**Purpose**: Identify critical weaknesses and structural imbalances

**Algorithm**: Rule-based heuristics

**Detection Logic**:

#### A. Structural Imbalance
```python
if std_dev(dimension_scores) > 1.0:
    # High variance indicates uneven development
    # Example: Strong tech (4.5) but weak governance (1.5)
    return "Structural Imbalance: [High Dims] vs [Low Dims]"
```

#### B. Critical Gaps
```python
for dimension in dimensions:
    if score < 2.5 and strategic_importance == "high":
        impact_score = (5.0 - score) * importance_weight
        critical_gaps.append({
            "dimension": dimension,
            "score": score,
            "impact": impact_score
        })
```

**Output**:
- Top 2 strategic findings
- Impact scores (0-15 scale)
- Contextual descriptions
- Executive briefing narrative

**No Model Files** (rule-based, no training required)

---

### 3. Roadmap Generator (`RoadmapGenerator`)

**Purpose**: Generate personalized 3-phase transformation roadmap

**Algorithm**: K-Nearest Neighbors (k=15) + Template-based generation

**KNN Usage**:
- Find 15 most similar companies (global dataset)
- Compare their dimension scores to identify "Growth Opportunities"
- Recommend actions based on peer success patterns

**Roadmap Phases**:

#### Phase 1: Foundation (0-3 months)
- **Focus**: Address strategic gaps
- **Source**: Strategic Gap Analyzer findings
- **Actions**: 2 recommendations per gap

#### Phase 2: Growth (3-9 months)
- **Focus**: Build on strengths, close peer gaps
- **Source**: KNN peer comparison
- **Actions**: Dimension-specific improvements

#### Phase 3: Advanced (9+ months)
- **Focus**: Innovation and differentiation
- **Source**: Template-based advanced capabilities
- **Actions**: Cutting-edge AI initiatives

**Model Files**:
- `v5_roadmap_gen.pkl` - Trained KNN model (NearestNeighbors)
- `v5_scaler.pkl` - StandardScaler for normalization (shared with clustering)
- `v5_industry_data.pkl` - Training data with industry labels

---

### 4. Peer Benchmark Calculator

**Purpose**: Provide realistic peer comparison for Radar Chart

**Algorithm**: Industry-Aware Aggregation

**Process**:
1. Check if sufficient peers (>5) exist in the same **Industry**.
2. If yes: Average dimension scores of that industry group.
3. If no: Fallback to **Global** average of all companies.

**Scope**: **Industry-Specific** (with Global fallback)

**Output**: Dictionary of peer dimension scores

---

## Training Pipeline

### Prerequisites

**Training Data Requirements**:
- Historical company assessments: **499 companies** (verified from database)
- 7 dimension scores per company
- Industry labels
- Questionnaire responses

**Data Format**:
```python
# Dimension Data
dim_data = pd.DataFrame({
    'Strategy & Business Vision': [3.5, 2.1, ...],
    'Data Readiness & Literacy': [2.8, 3.9, ...],
    # ... other dimensions
    'total_maturity': [3.2, 2.9, ...]  # Average of all dimensions
})

# Industry Data
industry_data = pd.DataFrame({
    'industry': ['Technology', 'Finance', ...],
    'total_maturity': [3.2, 2.9, ...]
})
```

---

### Training Steps

#### Step 1: Data Preparation

```python
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Load historical data
dim_data = pd.read_csv('historical_assessments.csv')

# Calculate total maturity
dim_data['total_maturity'] = dim_data[dimension_columns].mean(axis=1)

# Prepare features (exclude total_maturity for training)
X = dim_data.drop(columns=['total_maturity'])
```

#### Step 2: Train Cluster Model

```python
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pickle

# Initialize and fit scaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train KMeans
kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
kmeans.fit(X_scaled)

# Assign cluster names based on average maturity
cluster_labels = {
    0: "1 - Traditionalist",
    1: "2 - Explorer",
    2: "3 - Builder",
    3: "4 - Scaler",
    4: "5 - Leader"
}

# Save models
with open('model_artifacts/v5_kmeans.pkl', 'wb') as f:
    pickle.dump(kmeans, f)
    
with open('model_artifacts/v5_scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)
```

#### Step 3: Train Roadmap KNN

```python
from sklearn.neighbors import NearestNeighbors

# Initialize and fit scaler
roadmap_scaler = StandardScaler()
X_scaled = roadmap_scaler.fit_transform(X)

# Train KNN
knn = NearestNeighbors(n_neighbors=15, metric='euclidean')
knn.fit(X_scaled)

# Save models and data
with open('model_artifacts/v5_roadmap_gen.pkl', 'wb') as f:
    pickle.dump(knn, f)
    
# Note: v5_scaler.pkl is shared with clustering
    
# Save industry data for percentile calculations
with open('model_artifacts/v5_industry_data.pkl', 'wb') as f:
    pickle.dump(dim_data[['company_id', 'industry', 'total_maturity']], f)
```

#### Step 4: Prepare Industry Benchmarks

```python
# Calculate industry statistics
industry_stats = dim_data.groupby('industry')['total_maturity'].describe()

# Industry data already saved in Step 3 as v5_industry_data.pkl
```

---

## Inference Pipeline

### Initialization

```python
from benchmarking_ai.ml_v5.inference import InferenceEngine

# Initialize engine (loads all models)
engine = InferenceEngine()
```

### Running Analysis

```python
# Input data
company_dim_series = pd.Series({
    'Strategy & Business Vision': 3.5,
    'Data Readiness & Literacy': 2.8,
    'Governance & Compliance': 3.1,
    'People & Culture': 2.9,
    'Processes & Scaling': 3.2,
    'Tech Infrastructure': 3.0,
    'Use Cases & Business Value': 3.3
})

company_question_df = pd.DataFrame({
    'question_id': [1, 2, 3, ...],
    'dimension': ['Strategy', 'Data', ...],
    'score': [4, 3, 5, ...]
})

company_industry = "Technology"

# Run inference
results = engine.run_analysis(
    company_dim_series,
    company_question_df,
    company_industry
)
```

### Output Structure

```python
{
    "cluster": {
        "cluster_id": 3,
        "cluster_name": "3 - Builder",
        "coordinates": [0.5, 0.3, 0.7, 0.4, 0.6, 0.5, 0.6]
    },
    "percentile": {
        "percentage": 65,
        "industry": "Technology",
        "total_companies": 150
    },
    "benchmark_scores": {
        "Strategy & Business Vision": 3.45,
        "Data Readiness & Literacy": 2.95,
        # ... other dimensions
    },
    "strategic_findings": [
        {
            "title": "Critical Gap: Data Readiness",
            "score": 14.2,
            "context": "Low score (2.8) in high-impact dimension",
            "theme": "Data Readiness & Literacy"
        },
        {
            "title": "Structural Imbalance: Tech vs Governance",
            "score": 12.5,
            "context": "High variance (σ=1.2) across dimensions",
            "theme": "Balanced Development"
        }
    ],
    "executive_briefing": "Our analysis identifies **Critical Gap: Data Readiness**...",
    "roadmap": {
        "phase_1": [
            {
                "theme": "Data Readiness & Literacy",
                "explanation": "**Analysis**: Current score 2.8...\n- **Action 1**: Implement data governance framework...\n- **Action 2**: Train teams on data literacy..."
            }
        ],
        "phase_2": [...],
        "phase_3": [...]
    },
    "roadmap_briefing": "Your 3-phase roadmap prioritizes..."
}
```

---

## Complete Workflow

### End-to-End User Journey

```text
┌─────────────────────────────────────────────────────────────────┐
│                    USER INTERACTION                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 1: Company Snapshot (Frontend)                            │
│  - User enters company details (name, industry, size)           │
│  - POST /api/v1/companies                                       │
│  - POST /api/v1/responses                                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 2: Questionnaire (Frontend)                               │
│  - User answers 35 questions across 7 dimensions                │
│  - Each answer: 1-5 scale                                       │
│  - PUT /api/v1/responses/{id}/answers (batch update)            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 3: Score Calculation (Backend)                            │
│  - Aggregate answers by dimension                               │
│  - Calculate dimension scores (average per dimension)           │
│  - Store in database                                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 4: ML Inference (Backend - InferenceEngine)               │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ 4.1 Cluster Prediction (ClusterEngine)                    │  │
│  │     - Load v5_scaler.pkl, v5_kmeans.pkl                   │  │
│  │     - Scale dimension scores                              │  │
│  │     - Predict cluster (1-5)                               │  │
│  │     - Output: Cluster ID, Name, Coordinates               │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ 4.2 Percentile Calculation (ClusterEngine)                │  │
│  │     - Load v5_industry_data.pkl                           │  │
│  │     - Compare total_maturity to industry peers            │  │
│  │     - Output: Percentile rank (e.g., "Top 35%")           │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ 4.3 Peer Benchmark (RoadmapGenerator)                     │  │
│  │     - Load v5_scaler.pkl, v5_roadmap_gen.pkl              │  │
│  │     - Find 15 nearest neighbors (global)                  │  │
│  │     - Average their dimension scores                      │  │
│  │     - Output: Peer benchmark scores                       │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ 4.4 Strategic Gap Analysis (StrategicGapAnalyzer)         │  │
│  │     - Detect structural imbalances (variance > 1.0)       │  │
│  │     - Identify critical gaps (score < 2.5)                │  │
│  │     - Calculate impact scores                             │  │
│  │     - Output: Top 2 findings with context                 │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ 4.5 Executive Briefing (StrategicGapAnalyzer)             │  │
│  │     - Synthesize narrative from findings                  │  │
│  │     - Template-based text generation                      │  │
│  │     - Output: Markdown-formatted briefing                 │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ 4.6 Roadmap Generation (RoadmapGenerator)                 │  │
│  │     - Phase 1: Address strategic gaps (0-3 months)        │  │
│  │     - Phase 2: Growth opportunities (3-9 months)          │  │
│  │     - Phase 3: Advanced capabilities (9+ months)          │  │
│  │     - Output: 3-phase roadmap with actions                │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 5: API Response (Backend)                                 │
│  - GET /api/v1/responses/{id}/results                           │
│  - Return JSON with all analysis results                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 6: Results Display (Frontend)                             │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ ResultsHero.jsx                                           │  │
│  │ - Display total_score, cluster_name                       │  │
│  │ - Show percentile rank                                    │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ MaturityProfile.jsx (Radar Chart)                         │  │
│  │ - Plot dimension_scores (user)                            │  │
│  │ - Plot benchmark_scores (peers)                           │  │
│  │ - Interactive visualization                               │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ ExecutiveBriefing.jsx                                     │  │
│  │ - Render executive_briefing (markdown)                    │  │
│  │ - Premium card design                                     │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ GapAnalysis.jsx                                           │  │
│  │ - Display strategic_findings                              │  │
│  │ - Show impact scores, context                             │  │
│  │ - Priority badges                                         │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ Roadmap.jsx                                               │  │
│  │ - Display phase_1, phase_2, phase_3                       │  │
│  │ - Expandable action items                                 │  │
│  │ - Timeline visualization                                  │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## File Structure

```
benchmarking_ai/ml_v5/
├── README.md                    # This file
├── models.py                    # Core ML classes
│   ├── ClusterEngine            # KMeans clustering
│   ├── StrategicGapAnalyzer     # Gap detection
│   └── RoadmapGenerator         # KNN + roadmap generation
├── inference.py                 # Inference orchestrator
├── utils.py                     # Helper functions
├── train_models.py              # Training script
└── model_artifacts/             # Trained models (v5_ prefix)
    ├── v5_kmeans.pkl            # KMeans model (5 clusters)
    ├── v5_scaler.pkl            # StandardScaler (shared)
    ├── v5_roadmap_gen.pkl       # KNN model (15 neighbors)
    ├── v5_industry_data.pkl     # Industry data (499 companies)
    ├── v5_pca.pkl               # PCA transformer
    ├── v5_gap_analyzer.pkl      # Gap analyzer config
    └── v5_labels.json           # Cluster labels
```

---

## API Integration

### Backend Entry Point

**File**: `Application_Prototype/mvp_v1/backend/routers/results.py`

```python
from benchmarking_ai.ml_v5.inference import InferenceEngine

# Initialize engine once (singleton pattern recommended)
engine = InferenceEngine()

@router.get("/api/v1/responses/{response_id}/results")
async def get_results(response_id: int, db: Session = Depends(get_db)):
    # 1. Fetch response and company data
    response = db.query(Response).filter_by(response_id=response_id).first()
    company = db.query(Company).filter_by(company_id=response.company_id).first()
    
    # 2. Calculate dimension scores
    dimension_scores = calculate_dimension_scores(response_id, db)
    
    # 3. Prepare data for ML
    company_dim_series = pd.Series(dimension_scores)
    company_question_df = get_question_details(response_id, db)
    company_industry = company.industry
    
    # 4. Run ML inference
    analysis = engine.run_analysis(
        company_dim_series,
        company_question_df,
        company_industry
    )
    
    # 5. Format and return response
    return {
        "company_id": company.company_id,
        "response_id": response_id,
        "total_score": round(company_dim_series.mean(), 2),
        "cluster": analysis["cluster"],
        "dimension_scores": dimension_scores,
        "benchmark_scores": analysis["benchmark_scores"],
        "percentiles": analysis["percentile"],
        "gap_analysis": {
            "strategic_findings": analysis["strategic_findings"],
            "executive_briefing": analysis["executive_briefing"]
        },
        "roadmap": analysis["roadmap"]
    }
```

---

## Frontend Integration

### Data Fetching

**File**: `frontend/src/pages/ResultsDashboard.jsx`

```javascript
useEffect(() => {
    const fetchResults = async () => {
        try {
            const data = await api.getResults(responseId);
            setResults(data);
        } catch (error) {
            console.error('Failed to fetch results:', error);
        }
    };
    fetchResults();
}, [responseId]);
```

### Component Mapping

| Component | Data Source | Purpose |
|-----------|-------------|---------|
| `ResultsHero.jsx` | `total_score`, `cluster.cluster_name`, `percentile` | Hero section with key metrics |
| `MaturityProfile.jsx` | `dimension_scores`, `benchmark_scores` | Radar chart visualization |
| `ExecutiveBriefing.jsx` | `gap_analysis.executive_briefing` | Executive summary narrative |
| `GapAnalysis.jsx` | `gap_analysis.strategic_findings` | Strategic gap cards |
| `Roadmap.jsx` | `roadmap.phase_1/2/3` | 3-phase transformation roadmap |
| `ClusterInsight.jsx` | `cluster` | Cluster description and insights |

---

## Data Schemas

### Input Schema (Questionnaire Response)

```python
{
    "response_id": 123,
    "company_id": 456,
    "answers": [
        {
            "question_id": 1,
            "dimension": "Strategy & Business Vision",
            "score": 4
        },
        # ... 35 questions total
    ]
}
```

### Dimension Scores (Calculated)

```python
{
    "Strategy & Business Vision": 3.5,
    "Data Readiness & Literacy": 2.8,
    "Governance & Compliance": 3.1,
    "People & Culture": 2.9,
    "Processes & Scaling": 3.2,
    "Tech Infrastructure": 3.0,
    "Use Cases & Business Value": 3.3
}
```

### ML Output Schema

```python
{
    "cluster": {
        "cluster_id": 3,
        "cluster_name": "3 - Builder",
        "coordinates": [0.5, 0.3, 0.7, 0.4, 0.6, 0.5, 0.6]
    },
    "percentile": {
        "percentage": 65,
        "industry": "Technology",
        "total_companies": 150
    },
    "benchmark_scores": {
        "Strategy & Business Vision": 3.45,
        # ... other dimensions
    },
    "strategic_findings": [
        {
            "title": "Critical Gap: Data Readiness",
            "score": 14.2,
            "context": "...",
            "theme": "Data Readiness & Literacy"
        }
    ],
    "executive_briefing": "Markdown text...",
    "roadmap": {
        "phase_1": [...],
        "phase_2": [...],
        "phase_3": [...]
    }
}
```

---

## Deployment

### Model Loading

Models are loaded once at application startup:

```python
# backend/main.py
from benchmarking_ai.ml_v5.inference import InferenceEngine

@app.on_event("startup")
async def startup_event():
    global ml_engine
    ml_engine = InferenceEngine()
    print("ML Inference Engine Loaded Successfully")
```

### Performance Considerations

- **Model Loading**: ~2-3 seconds at startup
- **Inference Time**: ~100-200ms per request
- **Memory Usage**: ~50MB for loaded models
- **Concurrency**: Thread-safe (models are read-only)

### Scaling

For high-traffic scenarios:
1. Use model caching (already implemented)
2. Consider async inference with queue
3. Deploy models separately as microservice
4. Use model versioning for A/B testing

---

## Troubleshooting

### Common Issues

#### 1. Model Files Not Found
```
Error: FileNotFoundError: model_artifacts/v5_kmeans.pkl
```
**Solution**: Ensure model files exist in `benchmarking_ai/ml_v5/model_artifacts/` with `v5_` prefix

#### 2. Dimension Mismatch
```
Error: ValueError: X has 6 features, but KMeans is expecting 7
```
**Solution**: Verify all 7 dimensions are present in input data

#### 3. Empty Peer Benchmark
```
Warning: Peer Benchmark Calc Error: ...
```
**Solution**: Check that `v5_industry_data.pkl` contains training data (499 companies)

---

## Future Enhancements

### Planned Improvements

1. **Industry-Specific Peer Benchmarking**
   - Filter KNN by industry before averaging
   - Provide industry-specific recommendations

2. **Dynamic Roadmap Templates**
   - Train recommendation model on historical success patterns
   - Personalize actions based on company size/industry

3. **Confidence Scores**
   - Add uncertainty quantification to predictions
   - Highlight low-confidence recommendations

4. **Model Retraining Pipeline**
   - Automated retraining with new assessment data
   - A/B testing framework for model versions

5. **Explainability**
   - SHAP values for cluster assignments
   - Feature importance for gap detection

---

## Contact & Support

For questions or issues related to the ML v5 system:
- **Documentation**: This README
- **Architecture**: See `doc/ml_model_architecture.md`
- **Code**: `benchmarking_ai/ml_v5/`

---

## Version History

- **v5.0** (Current) - Production system with KMeans clustering, gap analysis, and KNN roadmap generation
- **v4.x** (Legacy) - Previous iteration (deprecated)

---

## License

Proprietary - AI Compass Platform
