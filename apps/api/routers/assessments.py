"""
Assessment API router.
Handles all assessment-related endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import uuid

from db.database import get_db
from models.assessment import (
    CompanyAssessment,
    QuestionnaireResponse,
    MaturityScores,
    BenchmarkClusterResult
)
from schemas.assessment import (
    CreateAssessmentRequest,
    CreateAssessmentResponse,
    SubmitResponsesRequest,
    SubmitResponsesResponse,
    CompleteAssessmentResponse,
    GetAssessmentResponse,
    GetQuestionnaireResponse,
    QuestionnaireMetadata,
    OverallScore,
    DimensionScore,
    ChartData,
    BenchmarkResult,
    Recommendations
)

from core.questionnaire.loader import get_questionnaire_loader
from core.scoring.engine import ScoringEngine
from core.ml.benchmark import BenchmarkService
from core.llm.groq_service import LLMService
from core.reporting.pdf_generator import PDFReportGenerator

router = APIRouter()


@router.get("/questionnaire", response_model=GetQuestionnaireResponse)
async def get_questionnaire():
    """
    Get full questionnaire schema with metadata.
    """
    loader = get_questionnaire_loader()
    schema = loader.load()
    metadata = loader.get_metadata()
    
    return GetQuestionnaireResponse(
        metadata=QuestionnaireMetadata(**metadata),
        schema=schema
    )


@router.post("/assessments", response_model=CreateAssessmentResponse)
async def create_assessment(
    request: CreateAssessmentRequest,
    db: Session = Depends(get_db)
):
    """
    Create a new assessment.
    """
    loader = get_questionnaire_loader()
    metadata = loader.get_metadata()
    
    # Create assessment record
    assessment = CompanyAssessment(
        id=uuid.uuid4(),
        company_meta=request.company_meta.model_dump(),
        questionnaire_id=metadata["questionnaire_id"],
        questionnaire_version=metadata["questionnaire_version"],
        questionnaire_hash=metadata["questionnaire_hash"],
        status="draft",
        created_at=datetime.utcnow()
    )
    
    db.add(assessment)
    db.commit()
    db.refresh(assessment)
    
    return CreateAssessmentResponse(
        assessment_id=assessment.id,
        questionnaire_id=assessment.questionnaire_id,
        questionnaire_version=assessment.questionnaire_version,
        status=assessment.status,
        created_at=assessment.created_at
    )


@router.post("/assessments/{assessment_id}/responses", response_model=SubmitResponsesResponse)
async def submit_responses(
    assessment_id: uuid.UUID,
    request: SubmitResponsesRequest,
    db: Session = Depends(get_db)
):
    """
    Submit answers to assessment questions.
    Supports upsert (update existing answers).
    """
    # Verify assessment exists
    assessment = db.query(CompanyAssessment).filter(
        CompanyAssessment.id == assessment_id
    ).first()
    
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    if assessment.status == "completed":
        raise HTTPException(status_code=400, detail="Assessment already completed")
    
    # Load questionnaire for validation
    loader = get_questionnaire_loader()
    schema = loader.load()
    
    # Process each response
    saved_count = 0
    for answer in request.responses:
        # Validate question exists
        question = loader.get_question_by_id(answer.question_id)
        if not question:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid question_id: {answer.question_id}"
            )
        
        # Validate options and compute points
        total_points = 0.0
        for opt_id in answer.selected_option_ids:
            option = loader.get_option_by_id(answer.question_id, opt_id)
            if not option:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid option_id: {opt_id} for question {answer.question_id}"
                )
            total_points += option.get("points", 0)
        
        # Aggregate points (average for multi-choice)
        if len(answer.selected_option_ids) > 0:
            aggregated_points = total_points / len(answer.selected_option_ids)
        else:
            aggregated_points = 0.0
        
        question_weight = question.get("weight", 1.0)
        
        # Check if response already exists (upsert)
        existing = db.query(QuestionnaireResponse).filter(
            QuestionnaireResponse.assessment_id == assessment_id,
            QuestionnaireResponse.question_id == answer.question_id
        ).first()
        
        if existing:
            # Update existing
            existing.selected_option_ids = answer.selected_option_ids
            existing.points_snapshot = aggregated_points
            existing.weight_snapshot = question_weight
            existing.answered_at = datetime.utcnow()
        else:
            # Create new
            response = QuestionnaireResponse(
                id=uuid.uuid4(),
                assessment_id=assessment_id,
                dimension_id=answer.dimension_id,
                question_id=answer.question_id,
                answer_type=question.get("type", "single_choice"),
                selected_option_ids=answer.selected_option_ids,
                points_snapshot=aggregated_points,
                weight_snapshot=question_weight,
                answered_at=datetime.utcnow()
            )
            db.add(response)
        
        saved_count += 1
    
    db.commit()
    
    return SubmitResponsesResponse(
        assessment_id=assessment_id,
        responses_saved=saved_count,
        message=f"Successfully saved {saved_count} responses"
    )


@router.post("/assessments/{assessment_id}/complete", response_model=CompleteAssessmentResponse)
async def complete_assessment(
    assessment_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """
    Complete assessment and compute all results:
    - Deterministic scoring
    - ML benchmarking
    - LLM recommendations
    """
    # Get assessment
    assessment = db.query(CompanyAssessment).filter(
        CompanyAssessment.id == assessment_id
    ).first()
    
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    # Get all responses
    responses = db.query(QuestionnaireResponse).filter(
        QuestionnaireResponse.assessment_id == assessment_id
    ).all()
    
    if len(responses) == 0:
        raise HTTPException(status_code=400, detail="No responses found for this assessment")
    
    # Load questionnaire
    loader = get_questionnaire_loader()
    schema = loader.load()
    
    # 1. DETERMINISTIC SCORING
    scoring_engine = ScoringEngine(schema)
    
    # Convert responses to dict format for scoring
    response_dicts = [
        {
            "dimension_id": r.dimension_id,
            "question_id": r.question_id,
            "selected_option_ids": r.selected_option_ids,
            "points_snapshot": float(r.points_snapshot),
            "weight_snapshot": float(r.weight_snapshot)
        }
        for r in responses
    ]
    
    dimension_scores_dict, overall_score, overall_level = scoring_engine.compute_scores(response_dicts)
    
    # Prepare chart data
    chart_data_dict = scoring_engine.prepare_chart_data(dimension_scores_dict)
    
    # Convert to list for response
    dimension_scores_list = list(dimension_scores_dict.values())
    
    # 2. ML BENCHMARKING
    # Get all question IDs in stable order
    all_questions = []
    for dim in schema["dimensions"]:
        for q in dim["questions"]:
            all_questions.append(q["id"])
    all_questions.sort()  # Stable ordering
    
    benchmark_service = BenchmarkService(question_ids=all_questions)
    benchmark_result = benchmark_service.benchmark(response_dicts, overall_score)
    
    # 3. LLM RECOMMENDATIONS
    llm_service = LLMService(db=db)
    recommendations = llm_service.generate_recommendations(
        company_meta=assessment.company_meta,
        dimension_scores=dimension_scores_list,
        overall_score=overall_score,
        overall_level=overall_level,
        benchmark=benchmark_result
    )
    
    # 4. SAVE RESULTS TO DB
    # Save maturity scores
    maturity_scores = MaturityScores(
        assessment_id=assessment_id,
        overall_score=overall_score,
        overall_level=overall_level,
        dimension_scores=dimension_scores_dict,
        created_at=datetime.utcnow()
    )
    
    # Check if already exists (upsert)
    existing_scores = db.query(MaturityScores).filter(
        MaturityScores.assessment_id == assessment_id
    ).first()
    
    if existing_scores:
        existing_scores.overall_score = overall_score
        existing_scores.overall_level = overall_level
        existing_scores.dimension_scores = dimension_scores_dict
    else:
        db.add(maturity_scores)
    
    # Save benchmark results
    benchmark_record = BenchmarkClusterResult(
        assessment_id=assessment_id,
        model_version=benchmark_service.get_model_version(),
        cluster_id=benchmark_result["cluster_id"],
        cluster_label=benchmark_result["cluster_label"],
        percentile=benchmark_result["percentile"],
        mismatch_flag=benchmark_result["mismatch_flag"],
        mismatch_note=benchmark_result["mismatch_note"],
        created_at=datetime.utcnow()
    )
    
    existing_benchmark = db.query(BenchmarkClusterResult).filter(
        BenchmarkClusterResult.assessment_id == assessment_id
    ).first()
    
    if existing_benchmark:
        existing_benchmark.model_version = benchmark_record.model_version
        existing_benchmark.cluster_id = benchmark_record.cluster_id
        existing_benchmark.cluster_label = benchmark_record.cluster_label
        existing_benchmark.percentile = benchmark_record.percentile
        existing_benchmark.mismatch_flag = benchmark_record.mismatch_flag
        existing_benchmark.mismatch_note = benchmark_record.mismatch_note
    else:
        db.add(benchmark_record)
    
    # Update assessment status
    assessment.status = "completed"
    assessment.completed_at = datetime.utcnow()
    
    db.commit()
    
    # 5. BUILD RESPONSE
    return CompleteAssessmentResponse(
        assessment_id=assessment_id,
        overall=OverallScore(
            score_0_100=overall_score,
            level_1_5=overall_level
        ),
        dimension_scores=[DimensionScore(**d) for d in dimension_scores_list],
        chart_data=ChartData(**chart_data_dict),
        benchmark=BenchmarkResult(**benchmark_result),
        recommendations=Recommendations(**recommendations)
    )


@router.get("/assessments/{assessment_id}", response_model=GetAssessmentResponse)
async def get_assessment(
    assessment_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """
    Get assessment details including responses and results (if completed).
    """
    assessment = db.query(CompanyAssessment).filter(
        CompanyAssessment.id == assessment_id
    ).first()
    
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    # Get responses
    responses = db.query(QuestionnaireResponse).filter(
        QuestionnaireResponse.assessment_id == assessment_id
    ).all()
    
    response_dicts = [
        {
            "dimension_id": r.dimension_id,
            "question_id": r.question_id,
            "selected_option_ids": r.selected_option_ids,
            "points": float(r.points_snapshot)
        }
        for r in responses
    ]
    
    # Get results if completed
    results = None
    if assessment.status == "completed":
        scores = db.query(MaturityScores).filter(
            MaturityScores.assessment_id == assessment_id
        ).first()
        
        benchmark = db.query(BenchmarkClusterResult).filter(
            BenchmarkClusterResult.assessment_id == assessment_id
        ).first()
        
        if scores and benchmark:
            # Reconstruct results (simplified - could also regenerate recommendations)
            loader = get_questionnaire_loader()
            schema = loader.load()
            scoring_engine = ScoringEngine(schema)
            
            dimension_scores_list = list(scores.dimension_scores.values())
            chart_data_dict = scoring_engine.prepare_chart_data(scores.dimension_scores)
            
            # Use deterministic template for recommendations (or fetch from cache)
            llm_service = LLMService(db=db)
            recommendations = llm_service.DETERMINISTIC_TEMPLATE
            
            results = CompleteAssessmentResponse(
                assessment_id=assessment_id,
                overall=OverallScore(
                    score_0_100=float(scores.overall_score),
                    level_1_5=scores.overall_level
                ),
                dimension_scores=[DimensionScore(**d) for d in dimension_scores_list],
                chart_data=ChartData(**chart_data_dict),
                benchmark=BenchmarkResult(
                    cluster_label=benchmark.cluster_label,
                    percentile=float(benchmark.percentile),
                    mismatch_flag=benchmark.mismatch_flag,
                    mismatch_note=benchmark.mismatch_note
                ),
                recommendations=Recommendations(**recommendations)
            )
    
    return GetAssessmentResponse(
        assessment_id=assessment.id,
        company_meta=assessment.company_meta,
        questionnaire_id=assessment.questionnaire_id,
        questionnaire_version=assessment.questionnaire_version,
        status=assessment.status,
        created_at=assessment.created_at,
        completed_at=assessment.completed_at,
        responses=response_dicts,
        results=results
    )


@router.get("/assessments/{assessment_id}/pdf")
async def download_pdf(
    assessment_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """
    Download PDF report for completed assessment.
    """
    assessment = db.query(CompanyAssessment).filter(
        CompanyAssessment.id == assessment_id
    ).first()
    
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    if assessment.status != "completed":
        raise HTTPException(status_code=400, detail="Assessment not completed yet")
    
    # Get scores and benchmark
    scores = db.query(MaturityScores).filter(
        MaturityScores.assessment_id == assessment_id
    ).first()
    
    benchmark = db.query(BenchmarkClusterResult).filter(
        BenchmarkClusterResult.assessment_id == assessment_id
    ).first()
    
    if not scores or not benchmark:
        raise HTTPException(status_code=500, detail="Results not found")
    
    # Prepare data for PDF
    loader = get_questionnaire_loader()
    schema = loader.load()
    scoring_engine = ScoringEngine(schema)
    
    dimension_scores_list = list(scores.dimension_scores.values())
    chart_data_dict = scoring_engine.prepare_chart_data(scores.dimension_scores)
    
    # Get recommendations (from cache or template)
    llm_service = LLMService(db=db)
    recommendations = llm_service.DETERMINISTIC_TEMPLATE
    
    results_dict = {
        "overall": {
            "score_0_100": float(scores.overall_score),
            "level_1_5": scores.overall_level
        },
        "dimension_scores": dimension_scores_list,
        "chart_data": chart_data_dict,
        "benchmark": {
            "cluster_label": benchmark.cluster_label,
            "percentile": float(benchmark.percentile),
            "mismatch_flag": benchmark.mismatch_flag,
            "mismatch_note": benchmark.mismatch_note
        },
        "recommendations": recommendations
    }
    
    assessment_dict = {
        "company_meta": assessment.company_meta,
        "questionnaire_id": assessment.questionnaire_id,
        "created_at": assessment.created_at
    }
    
    # Generate PDF
    pdf_generator = PDFReportGenerator()
    pdf_bytes = pdf_generator.generate(assessment_dict, results_dict)
    
    # Return as downloadable file
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=ai-compass-report-{assessment_id}.pdf"
        }
    )
