"""
Database models for AI-Compass assessment system.

Follows EAV (Entity-Attribute-Value) pattern for dynamic question storage.
All question/dimension IDs are read from questions.json at runtime.
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Integer, Numeric, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from db.database import Base


class CompanyAssessment(Base):
    """
    Main assessment record. One per company assessment session.
    """
    __tablename__ = "company_assessment"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_meta = Column(JSONB, nullable=False, comment="Industry, size, etc.")
    questionnaire_id = Column(String(100), nullable=False, comment="From questions.json")
    questionnaire_version = Column(String(50), nullable=False, comment="From questions.json")
    questionnaire_hash = Column(String(64), nullable=False, comment="SHA-256 of schema")
    status = Column(String(20), nullable=False, default="draft", comment="draft|completed")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    responses = relationship("QuestionnaireResponse", back_populates="assessment", cascade="all, delete-orphan")
    scores = relationship("MaturityScores", back_populates="assessment", uselist=False, cascade="all, delete-orphan")
    benchmark = relationship("BenchmarkClusterResult", back_populates="assessment", uselist=False, cascade="all, delete-orphan")


class QuestionnaireResponse(Base):
    """
    EAV-style answer storage. One row per answered question.
    Supports single-choice, multi-choice, and tag-like selections.
    """
    __tablename__ = "questionnaire_response"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    assessment_id = Column(UUID(as_uuid=True), ForeignKey("company_assessment.id", ondelete="CASCADE"), nullable=False)
    dimension_id = Column(String(100), nullable=False, index=True, comment="From questions.json")
    question_id = Column(String(100), nullable=False, index=True, comment="From questions.json")
    answer_type = Column(String(50), nullable=False, comment="single_choice|multi_choice|tags")
    selected_option_ids = Column(JSONB, nullable=False, comment="Array of option IDs selected")
    points_snapshot = Column(Numeric(10, 2), nullable=False, comment="Aggregated points at answer time")
    weight_snapshot = Column(Numeric(10, 2), nullable=False, comment="Question weight at answer time")
    answered_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    assessment = relationship("CompanyAssessment", back_populates="responses")


class MaturityScores(Base):
    """
    Computed maturity scores for an assessment.
    Stored as JSONB for flexibility (dimension scores structure is dynamic).
    """
    __tablename__ = "maturity_scores"

    assessment_id = Column(UUID(as_uuid=True), ForeignKey("company_assessment.id", ondelete="CASCADE"), primary_key=True)
    overall_score = Column(Numeric(5, 2), nullable=False, comment="0-100 scale")
    overall_level = Column(Integer, nullable=False, comment="1-5 maturity level")
    dimension_scores = Column(JSONB, nullable=False, comment="{dimension_id: {title, score, level, drivers[]}}")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    assessment = relationship("CompanyAssessment", back_populates="scores")


class BenchmarkClusterResult(Base):
    """
    ML benchmarking results from K-Means clustering.
    """
    __tablename__ = "benchmark_cluster_result"

    assessment_id = Column(UUID(as_uuid=True), ForeignKey("company_assessment.id", ondelete="CASCADE"), primary_key=True)
    model_version = Column(String(50), nullable=False, comment="e.g., kmeans_v1")
    cluster_id = Column(Integer, nullable=False, comment="0-based cluster index")
    cluster_label = Column(String(100), nullable=False, comment="AI Laggards, AI Scalers, etc.")
    percentile = Column(Numeric(5, 2), nullable=False, comment="Percentile vs synthetic peers (0-100)")
    mismatch_flag = Column(Boolean, nullable=False, default=False, comment="High score but low cluster (or vice versa)")
    mismatch_note = Column(Text, nullable=True, comment="Explanation of mismatch")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    assessment = relationship("CompanyAssessment", back_populates="benchmark")


class LLMEnrichmentCache(Base):
    """
    Cache for LLM-generated text (executive summaries, recommendations).
    Key is deterministic hash of inputs (company_meta + scores + benchmark).
    """
    __tablename__ = "llm_enrichment_cache"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cache_key = Column(String(64), nullable=False, unique=True, index=True, comment="SHA-256 of LLM input")
    payload = Column(JSONB, nullable=False, comment="LLM output JSON")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
