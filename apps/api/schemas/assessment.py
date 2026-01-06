"""Pydantic schemas for API request/response validation."""
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field, UUID4


# ============================================================================
# Company Assessment Schemas
# ============================================================================

class CompanyMetaInput(BaseModel):
    """Company metadata for assessment creation."""
    industry: str = Field(..., description="Industry sector")
    employee_band: str = Field(..., description="Employee count range")
    revenue_band: Optional[str] = Field(None, description="Revenue range")
    country: Optional[str] = Field(None, description="Country/region")
    additional_info: Optional[Dict[str, Any]] = Field(default_factory=dict)


class CreateAssessmentRequest(BaseModel):
    """Request to create a new assessment."""
    company_meta: CompanyMetaInput


class CreateAssessmentResponse(BaseModel):
    """Response after creating assessment."""
    assessment_id: UUID4
    questionnaire_id: str
    questionnaire_version: str
    status: str
    created_at: datetime


# ============================================================================
# Questionnaire Response Schemas
# ============================================================================

class AnswerInput(BaseModel):
    """Single answer to a question."""
    dimension_id: str = Field(..., description="Dimension ID from schema")
    question_id: str = Field(..., description="Question ID from schema")
    selected_option_ids: List[str] = Field(..., description="List of selected option IDs")


class SubmitResponsesRequest(BaseModel):
    """Request to submit answers."""
    responses: List[AnswerInput]


class SubmitResponsesResponse(BaseModel):
    """Response after submitting answers."""
    assessment_id: UUID4
    responses_saved: int
    message: str


# ============================================================================
# Scoring & Results Schemas
# ============================================================================

class DriverDetail(BaseModel):
    """Detail of a low-scoring driver (explainability)."""
    question_id: str
    question_text: str
    selected_label: str
    points: float


class DimensionScore(BaseModel):
    """Score for a single dimension."""
    dimension_id: str
    title: str
    score_0_100: float
    level_1_5: int
    drivers: List[DriverDetail] = Field(default_factory=list, description="Top 2-3 lowest-scoring questions")


class OverallScore(BaseModel):
    """Overall maturity score."""
    score_0_100: float
    level_1_5: int


class ChartDataRadar(BaseModel):
    """Radar chart data (ready for Plotly)."""
    labels: List[str] = Field(..., description="Dimension titles")
    values: List[float] = Field(..., description="Dimension scores")
    min_value: float = 0
    max_value: float = 100


class ChartDataBars(BaseModel):
    """Bar chart data (sorted low to high, ready for Plotly)."""
    labels: List[str] = Field(..., description="Dimension titles sorted by score")
    values: List[float] = Field(..., description="Dimension scores sorted")
    min_value: float = 0
    max_value: float = 100


class ChartData(BaseModel):
    """Chart data bundle."""
    radar: ChartDataRadar
    bars: ChartDataBars


class BenchmarkResult(BaseModel):
    """Benchmark clustering result."""
    cluster_label: str
    percentile: float
    mismatch_flag: bool
    mismatch_note: Optional[str] = None


class RoadmapItem(BaseModel):
    """Single roadmap recommendation."""
    title: str
    description: Optional[str] = None


class Recommendations(BaseModel):
    """LLM-generated recommendations."""
    executive_summary: str
    quick_wins: List[str] = Field(default_factory=list)
    roadmap: Dict[str, List[str]] = Field(
        default_factory=lambda: {"days_90": [], "months_6": [], "months_12": []}
    )
    risks: List[str] = Field(default_factory=list)


class CompleteAssessmentResponse(BaseModel):
    """Full results after completing assessment."""
    assessment_id: UUID4
    overall: OverallScore
    dimension_scores: List[DimensionScore]
    chart_data: ChartData
    benchmark: BenchmarkResult
    recommendations: Recommendations


# ============================================================================
# Questionnaire Schema Response
# ============================================================================

class QuestionnaireMetadata(BaseModel):
    """Metadata about loaded questionnaire."""
    questionnaire_id: str
    questionnaire_version: str
    questionnaire_hash: str
    title: str
    language: str
    estimated_time_minutes: int
    dimensions_count: int
    questions_count: int


class GetQuestionnaireResponse(BaseModel):
    """Response with full questionnaire schema."""
    metadata: QuestionnaireMetadata
    schema: Dict[str, Any] = Field(..., description="Full questions.json content")


# ============================================================================
# Assessment Retrieval Schemas
# ============================================================================

class GetAssessmentResponse(BaseModel):
    """Full assessment details."""
    assessment_id: UUID4
    company_meta: Dict[str, Any]
    questionnaire_id: str
    questionnaire_version: str
    status: str
    created_at: datetime
    completed_at: Optional[datetime] = None
    responses: List[Dict[str, Any]] = Field(default_factory=list)
    results: Optional[CompleteAssessmentResponse] = None


# ============================================================================
# Health Check Schema
# ============================================================================

class HealthCheckResponse(BaseModel):
    """Health check response."""
    status: str
    timestamp: datetime
    database: str
    questionnaire_loaded: bool
