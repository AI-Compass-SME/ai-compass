# AI-Compass API Reference

## Base URL
```
http://localhost:8000
```

## Authentication
**Currently:** None (MVP uses no authentication)  
**Future:** Add JWT tokens or API keys for production

---

## Endpoints

### 1. Health Check

**GET** `/health`

Check API health and dependencies status.

**Response Example:**
```json
{
  "status": "healthy",
  "timestamp": "2026-01-06T10:30:00.000000",
  "database": "connected",
  "questionnaire_loaded": true
}
```

---

### 2. Get Questionnaire Schema

**GET** `/api/v1/questionnaire`

Returns the full questionnaire schema with metadata.

**Response:**
```json
{
  "metadata": {
    "questionnaire_id": "ai-compass-mvp",
    "questionnaire_version": "2026-01-06",
    "questionnaire_hash": "abc123...",
    "title": "AI-Compass – AI Maturity Assessment",
    "language": "de",
    "estimated_time_minutes": 12,
    "dimensions_count": 7,
    "questions_count": 21
  },
  "schema": {
    "questionnaire_id": "ai-compass-mvp",
    "dimensions": [...],
    "scoring": {...}
  }
}
```

---

### 3. Create Assessment

**POST** `/api/v1/assessments`

Create a new assessment session.

**Request Body:**
```json
{
  "company_meta": {
    "industry": "IT & Software",
    "employee_band": "51-250",
    "revenue_band": "10-50 Mio €",
    "country": "Deutschland"
  }
}
```

**Response:**
```json
{
  "assessment_id": "550e8400-e29b-41d4-a716-446655440000",
  "questionnaire_id": "ai-compass-mvp",
  "questionnaire_version": "2026-01-06",
  "status": "draft",
  "created_at": "2026-01-06T10:30:00.000000"
}
```

---

### 4. Submit Responses

**POST** `/api/v1/assessments/{assessment_id}/responses`

Submit answers to questions. Supports upsert (can update existing answers).

**Request Body:**
```json
{
  "responses": [
    {
      "dimension_id": "strategy_business_vision",
      "question_id": "sbv_01_strategy_defined",
      "selected_option_ids": ["sbv_01_o3"]
    },
    {
      "dimension_id": "data_maturity",
      "question_id": "dm_01_data_access",
      "selected_option_ids": ["dm_01_o2"]
    }
  ]
}
```

**Response:**
```json
{
  "assessment_id": "550e8400-e29b-41d4-a716-446655440000",
  "responses_saved": 2,
  "message": "Successfully saved 2 responses"
}
```

**Validation:**
- All `question_id` and `option_id` values must exist in schema
- Invalid IDs will return `400 Bad Request`

---

### 5. Complete Assessment

**POST** `/api/v1/assessments/{assessment_id}/complete`

Compute final results (scoring, benchmarking, recommendations).

**Required:** All questions must be answered.

**Response:**
```json
{
  "assessment_id": "550e8400-e29b-41d4-a716-446655440000",
  "overall": {
    "score_0_100": 58.5,
    "level_1_5": 3
  },
  "dimension_scores": [
    {
      "dimension_id": "strategy_business_vision",
      "title": "Strategy & Business Vision",
      "score_0_100": 62.5,
      "level_1_5": 4,
      "drivers": [
        {
          "question_id": "sbv_03_value_prioritization",
          "question_text": "Wie bewertet und priorisiert ihr KI-Initiativen nach Nutzen/ROI?",
          "selected_label": "Grobe Nutzen-Schätzung",
          "points": 2.0
        }
      ]
    }
  ],
  "chart_data": {
    "radar": {
      "labels": ["Strategy & Business Vision", "Data Maturity", ...],
      "values": [62.5, 55.0, ...],
      "min_value": 0,
      "max_value": 100
    },
    "bars": {
      "labels": ["Tech Infrastructure", "Data Maturity", ...],
      "values": [45.0, 55.0, ...],
      "min_value": 0,
      "max_value": 100
    }
  },
  "benchmark": {
    "cluster_label": "AI Experimenters",
    "percentile": 64.5,
    "mismatch_flag": false,
    "mismatch_note": null
  },
  "recommendations": {
    "executive_summary": "Ihre Organisation zeigt solide Grundlagen...",
    "quick_wins": [
      "KI-Strategie klären und kommunizieren",
      "Datenqualität in Kernsystemen verbessern"
    ],
    "roadmap": {
      "days_90": ["Executive Sponsorship sicherstellen", ...],
      "months_6": ["Data Governance etablieren", ...],
      "months_12": ["KI-Betriebsmodell skalieren", ...]
    },
    "risks": [
      "Fehlende Executive-Unterstützung",
      "Datenqualität und -zugriff"
    ]
  }
}
```

**Processing Steps:**
1. **Deterministic Scoring**: Computes dimension and overall scores using weighted averages
2. **ML Benchmarking**: Clusters user against 500 synthetic peers using K-Means
3. **LLM Recommendations**: Generates German recommendations via Groq (or uses template as fallback)
4. **Persistence**: Saves all results to database

---

### 6. Get Assessment

**GET** `/api/v1/assessments/{assessment_id}`

Retrieve full assessment details including responses and results (if completed).

**Response:**
```json
{
  "assessment_id": "550e8400-e29b-41d4-a716-446655440000",
  "company_meta": {
    "industry": "IT & Software",
    "employee_band": "51-250"
  },
  "questionnaire_id": "ai-compass-mvp",
  "questionnaire_version": "2026-01-06",
  "status": "completed",
  "created_at": "2026-01-06T10:30:00.000000",
  "completed_at": "2026-01-06T10:45:00.000000",
  "responses": [
    {
      "dimension_id": "strategy_business_vision",
      "question_id": "sbv_01_strategy_defined",
      "selected_option_ids": ["sbv_01_o3"],
      "points": 3.0
    }
  ],
  "results": { /* Same as complete response */ }
}
```

---

### 7. Download PDF Report

**GET** `/api/v1/assessments/{assessment_id}/pdf`

Download PDF report for completed assessment.

**Response:**
- **Content-Type**: `application/pdf`
- **Content-Disposition**: `attachment; filename=ai-compass-report-{assessment_id}.pdf`

**Requirements:**
- Assessment must have `status = "completed"`
- Results must exist in database

**PDF Contents:**
1. Title page with company info
2. Executive summary
3. Overall score and level
4. Dimension scores table
5. Benchmark comparison
6. Recommendations (quick wins + roadmap + risks)

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid question_id: xyz123"
}
```

### 404 Not Found
```json
{
  "detail": "Assessment not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Data Models

### CompanyMeta
```typescript
{
  industry: string;
  employee_band: string;
  revenue_band?: string;
  country?: string;
  additional_info?: object;
}
```

### AnswerInput
```typescript
{
  dimension_id: string;
  question_id: string;
  selected_option_ids: string[];
}
```

### OverallScore
```typescript
{
  score_0_100: number;
  level_1_5: number;  // 1-5
}
```

### DimensionScore
```typescript
{
  dimension_id: string;
  title: string;
  score_0_100: number;
  level_1_5: number;
  drivers: DriverDetail[];
}
```

### DriverDetail
```typescript
{
  question_id: string;
  question_text: string;
  selected_label: string;
  points: number;
}
```

---

## Business Logic

### Scoring Algorithm

**Question Score:**
```
points = option.points (0-4)
```

**Dimension Score:**
```
dimension_score = Σ(question_score × weight) / Σ(weight)
normalized = (dimension_score / 4) × 100
```

**Overall Score:**
```
overall = Σ(dimension_score × dimension_weight) / Σ(dimension_weight)
```

**Level Mapping (Thresholds from schema):**
- Level 1: 0-19
- Level 2: 20-39
- Level 3: 40-59
- Level 4: 60-79
- Level 5: 80-100

### Benchmarking

**Feature Vector:**
```
[q1_points, q2_points, ..., q21_points]  # Ordered by question_id
```

**Clustering:**
- K-Means (k=4)
- Trained on 500 synthetic profiles
- Cluster labels assigned by centroid maturity (low → high)

**Percentile:**
```
percentile = (count of peers with score < user_score) / total_peers × 100
```

**Mismatch Detection:**
- High score (70+) + Low cluster (0-1) → Mismatch
- Low score (40-) + High cluster (2-3) → Mismatch

---

## Rate Limits

**Currently:** None

**Production Recommendation:**
- 100 requests/min per IP
- 10 assessment creations/hour per IP

---

## Caching

### LLM Cache
- **Key:** SHA-256 hash of (company_meta + dimension_scores + benchmark)
- **TTL:** Infinite (until manual cache clear)
- **Storage:** PostgreSQL `llm_enrichment_cache` table

---

## Testing

### Smoke Test
```bash
cd apps/api
python tests/test_scoring.py
```

### Manual Testing with cURL

**Create Assessment:**
```bash
curl -X POST http://localhost:8000/api/v1/assessments \
  -H "Content-Type: application/json" \
  -d '{"company_meta": {"industry": "IT", "employee_band": "51-250"}}'
```

**Submit Responses:**
```bash
curl -X POST http://localhost:8000/api/v1/assessments/{id}/responses \
  -H "Content-Type: application/json" \
  -d '{"responses": [{"dimension_id": "...", "question_id": "...", "selected_option_ids": ["..."]}]}'
```

**Complete:**
```bash
curl -X POST http://localhost:8000/api/v1/assessments/{id}/complete
```

---

## Interactive Docs

Access auto-generated OpenAPI docs:

**Swagger UI:**  
http://localhost:8000/docs

**ReDoc:**  
http://localhost:8000/redoc

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-06 | Initial MVP release |

---

*For implementation details, see source code in `apps/api/routers/assessments.py`*
