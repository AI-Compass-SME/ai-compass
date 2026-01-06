# AI-Compass Development Guide

## For Developers Working on This Codebase

This guide helps you understand the architecture and make changes safely.

---

## Architecture Overview

### Layers (Strict Separation)

```
┌─────────────────────────────────────────┐
│         Streamlit UI (apps/web)         │  ← User Interface
└─────────────────┬───────────────────────┘
                  │ HTTP
┌─────────────────▼───────────────────────┐
│       FastAPI Backend (apps/api)        │  ← API Layer
└─────────────────┬───────────────────────┘
                  │ Import
┌─────────────────▼───────────────────────┐
│     Core Business Logic (core/)         │  ← Pure Logic
│  • Questionnaire Loader                 │
│  • Scoring Engine (deterministic)       │
│  • ML Benchmarking (K-Means)            │
│  • LLM Service (Groq + cache)           │
│  • PDF Generator                        │
└─────────────────┬───────────────────────┘
                  │ SQLAlchemy
┌─────────────────▼───────────────────────┐
│       PostgreSQL Database               │  ← Persistence
└─────────────────────────────────────────┘
```

**Rules:**
1. **UI never calls core directly** → Always via API
2. **Core is pure** → No FastAPI/Streamlit dependencies
3. **API is thin** → Orchestrates core services

---

## Making Changes

### 1. Adding a New Question

**File:** `data/questionnaire/questions.json`

```json
{
  "id": "new_dimension",
  "title": "New Dimension",
  "order": 8,
  "weight": 1.0,
  "questions": [
    {
      "id": "nd_01_new_question",
      "text": "Your question text?",
      "type": "single_choice",
      "render": "radio",
      "required": true,
      "weight": 1.0,
      "options": [
        {"id": "nd_01_o1", "label": "Option 1", "points": 0, "tags": []},
        {"id": "nd_01_o2", "label": "Option 2", "points": 2, "tags": []},
        {"id": "nd_01_o3", "label": "Option 3", "points": 4, "tags": []}
      ]
    }
  ]
}
```

**Steps:**
1. Edit `questions.json`
2. Restart API (auto-reloads schema)
3. Test via `/questionnaire` endpoint
4. No code changes needed ✓

---

### 2. Modifying Scoring Logic

**File:** `core/scoring/engine.py`

**Example:** Change level thresholds

```python
# In questions.json, edit:
"levels_1_to_5_thresholds": [
  { "level": 1, "min_score_inclusive": 0, "max_score_inclusive": 15 },
  { "level": 2, "min_score_inclusive": 16, "max_score_inclusive": 35 },
  ...
]
```

**Or modify aggregation:**

```python
# In ScoringEngine._compute_dimension_score()
# Change from weighted average to median:
dimension_score = statistics.median(question_scores)
```

**Testing:**
```bash
cd apps/api
python tests/test_scoring.py
```

---

### 3. Adjusting ML Benchmarking

**File:** `core/ml/synthetic_data.py`

**Change peer distribution:**

```python
# In SyntheticDataGenerator.generate()
num_laggards = int(self.num_profiles * 0.30)  # Was 0.20
num_curious = int(self.num_profiles * 0.30)   # Was 0.30
num_experimenters = int(self.num_profiles * 0.25)  # Was 0.35
num_scalers = ...  # Remainder
```

**Change cluster count:**

```env
# In .env
KMEANS_CLUSTERS=5  # Was 4
```

**Add cluster label:**

```python
# In BenchmarkService.CLUSTER_LABELS
CLUSTER_LABELS = [
    "AI Laggards",
    "AI Curious",
    "AI Experimenters",
    "AI Adopters",      # New!
    "AI Scalers"
]
```

---

### 4. Customizing LLM Prompts

**File:** `core/llm/groq_service.py`

**Modify prompt template:**

```python
# In LLMService._build_prompt()
prompt = f"""Generiere umsetzbare KI-Empfehlungen...

**Your custom instructions here**

Erstelle eine JSON-Antwort mit:
...
"""
```

**Change model:**

```env
# In .env
GROQ_MODEL=llama-3.1-8b-instant  # Faster
GROQ_TEMPERATURE=0.3              # More creative
```

**Fallback template:**

```python
# In LLMService.DETERMINISTIC_TEMPLATE
DETERMINISTIC_TEMPLATE = {
    "executive_summary": "Your custom summary",
    "quick_wins": ["Custom win 1", "Custom win 2"],
    ...
}
```

---

### 5. Adding a New API Endpoint

**File:** `apps/api/routers/assessments.py`

**Example:** Get all assessments for a company

```python
@router.get("/assessments/by-industry/{industry}")
async def get_assessments_by_industry(
    industry: str,
    db: Session = Depends(get_db)
):
    """Get all assessments for a specific industry."""
    assessments = db.query(CompanyAssessment).filter(
        CompanyAssessment.company_meta['industry'].astext == industry
    ).all()
    
    return [
        {
            "id": a.id,
            "created_at": a.created_at,
            "status": a.status
        }
        for a in assessments
    ]
```

**Add Pydantic schema if needed:**

```python
# In apps/api/schemas/assessment.py
class AssessmentListItem(BaseModel):
    id: UUID4
    created_at: datetime
    status: str
```

---

### 6. Modifying Streamlit UI

**Add new page:**

```python
# apps/web/pages/4_Analytics.py
import streamlit as st

st.title("📊 Analytics Dashboard")
# Your custom analytics
```

**Modify existing page:**

```python
# apps/web/pages/3_Results.py
# Add custom visualization
st.plotly_chart(custom_chart, use_container_width=True)
```

---

### 7. Database Schema Changes

**Create migration:**

```bash
cd apps/api
alembic revision --autogenerate -m "Add new_field to company_assessment"
```

**Edit migration:**

```python
# apps/api/alembic/versions/002_add_field.py
def upgrade():
    op.add_column('company_assessment', 
                  sa.Column('new_field', sa.String(100)))

def downgrade():
    op.drop_column('company_assessment', 'new_field')
```

**Apply:**

```bash
alembic upgrade head
```

**Rollback (if needed):**

```bash
alembic downgrade -1
```

---

### 8. Adding PDF Sections

**File:** `core/reporting/pdf_generator.py`

**Add new section:**

```python
# In PDFReportGenerator.generate()
story.extend(self._build_custom_section(results))

# Add method:
def _build_custom_section(self, results: Dict[str, Any]) -> List:
    elements = []
    elements.append(Paragraph("Custom Section", self.styles['CustomHeading']))
    elements.append(Paragraph("Content here", self.styles['CustomBody']))
    return elements
```

---

## Testing Strategy

### 1. Unit Tests

**Scoring Engine:**

```python
# tests/test_scoring.py
def test_perfect_score():
    """Test that all maximum answers = 100 score."""
    responses = [/* all options with points=4 */]
    _, overall, level = engine.compute_scores(responses)
    assert overall == 100.0
    assert level == 5
```

**Questionnaire Loader:**

```python
def test_invalid_schema():
    """Test that invalid JSON raises error."""
    with pytest.raises(ValueError):
        loader.load_from_string('{"invalid": true}')
```

### 2. Integration Tests

**API End-to-End:**

```python
def test_full_assessment_flow():
    # Create
    response = client.post("/api/v1/assessments", json={...})
    assessment_id = response.json()["assessment_id"]
    
    # Submit
    client.post(f"/api/v1/assessments/{assessment_id}/responses", ...)
    
    # Complete
    result = client.post(f"/api/v1/assessments/{assessment_id}/complete")
    assert result.status_code == 200
    assert "overall" in result.json()
```

### 3. Manual Testing

**Checklist:**
- [ ] Create assessment via UI
- [ ] Answer all 21 questions
- [ ] View results (all charts render)
- [ ] Download PDF (opens correctly)
- [ ] Check database tables populated
- [ ] Restart API (persistent data)

---

## Debugging

### API Issues

**Enable debug logging:**

```python
# apps/api/main.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Check request/response:**

```bash
# Watch API logs in terminal
# All endpoints log to stdout
```

### Database Issues

**Inspect tables:**

```sql
-- Connect to DB
psql -U postgres -d aicompass

-- Check assessment
SELECT id, status, created_at FROM company_assessment;

-- Check responses
SELECT dimension_id, question_id, points_snapshot 
FROM questionnaire_response 
WHERE assessment_id = 'YOUR_ID';

-- Check scores
SELECT overall_score, overall_level 
FROM maturity_scores 
WHERE assessment_id = 'YOUR_ID';
```

**Clear test data:**

```sql
DELETE FROM company_assessment WHERE created_at < NOW() - INTERVAL '1 day';
```

### LLM Issues

**Check cache:**

```sql
SELECT cache_key, created_at FROM llm_enrichment_cache ORDER BY created_at DESC LIMIT 10;
```

**Clear cache:**

```sql
DELETE FROM llm_enrichment_cache;
```

**Test without Groq:**

```env
# Remove or invalidate GROQ_API_KEY in .env
# App will use deterministic template
```

---

## Code Style

### Python

- **PEP 8** compliant
- **Type hints** for all functions
- **Docstrings** for classes and public methods
- **Max line length**: 100 characters

```python
def compute_score(
    responses: List[Dict[str, Any]],
    weights: Dict[str, float]
) -> Tuple[float, int]:
    """
    Compute overall score from responses.
    
    Args:
        responses: List of answer dicts
        weights: Dimension weights
        
    Returns:
        Tuple of (score, level)
    """
    pass
```

### Imports

**Order:**

```python
# Standard library
import os
from typing import List, Dict

# Third-party
from fastapi import APIRouter
from sqlalchemy.orm import Session

# Local
from core.scoring.engine import ScoringEngine
from models.assessment import CompanyAssessment
```

---

## Performance Optimization

### Database

**Connection pooling (already configured):**

```python
# db/database.py
engine = create_engine(
    DATABASE_URL,
    pool_size=10,      # Default connections
    max_overflow=20    # Extra connections when needed
)
```

**Indexes (already added):**

- `company_assessment.status`
- `questionnaire_response.assessment_id`
- `questionnaire_response.dimension_id`
- `llm_enrichment_cache.cache_key` (unique)

### API

**Async endpoints:**

```python
@router.get("/slow-operation")
async def slow_operation():
    result = await some_async_function()
    return result
```

**Caching:**

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_calculation(x: int) -> int:
    return x ** 2
```

---

## Security Checklist (For Production)

- [ ] Add authentication (JWT tokens)
- [ ] Implement rate limiting
- [ ] Validate all inputs (currently Pydantic only)
- [ ] Use prepared statements (SQLAlchemy does this)
- [ ] Configure CORS properly (currently allow all)
- [ ] Enable HTTPS
- [ ] Hash sensitive data
- [ ] Add audit logging
- [ ] Implement CSRF protection
- [ ] Review dependency vulnerabilities

---

## Deployment

### Environment-Specific Configs

```env
# .env.production
DATABASE_URL=postgresql://user:pass@prod-db:5432/aicompass
GROQ_API_KEY=prod_key_here
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=WARNING
```

### Running with Gunicorn (Production WSGI)

```bash
pip install gunicorn
cd apps/api
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker (Future)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "apps.api.main:app", "--host", "0.0.0.0"]
```

---

## Gotchas & Common Issues

### Issue: Question IDs out of sync
**Symptom:** API returns "Invalid question_id"  
**Fix:** Restart API after editing questions.json

### Issue: LLM timeout
**Symptom:** Complete endpoint takes >30s  
**Fix:** Increase timeout or use faster Groq model

### Issue: Database locked
**Symptom:** "Database is locked" error  
**Fix:** Close other connections, check pool size

### Issue: Streamlit caching stale data
**Symptom:** Changes not reflected  
**Fix:** Clear cache with `st.cache_data.clear()`

---

## Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Streamlit Docs**: https://docs.streamlit.io
- **SQLAlchemy Docs**: https://docs.sqlalchemy.org
- **Plotly Docs**: https://plotly.com/python
- **Groq API Docs**: https://console.groq.com/docs

---

**Happy coding! Build responsibly.** 🚀
