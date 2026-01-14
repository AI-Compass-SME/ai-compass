"""
Basic smoke tests for scoring engine.
Tests deterministic scoring with known inputs.
"""
import sys
from pathlib import Path

# Add project root to path (one level up from tests/)
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.questionnaire.loader import QuestionnaireLoader
from core.scoring.engine import ScoringEngine


def test_scoring_engine_basic():
    """
    Test scoring engine with known answers.
    Ensures deterministic scoring works correctly.
    """
    # Load questionnaire
    loader = QuestionnaireLoader()
    schema = loader.load()
    
    # Create scoring engine
    engine = ScoringEngine(schema)
    
    # Build sample responses (all questions answered with first option - lowest points)
    responses = []
    for dim in schema["dimensions"]:
        for question in dim["questions"]:
            q_id = question["id"]
            dim_id = dim["id"]
            options = question["options"]
            
            # Select first option
            first_option = options[0]
            
            responses.append({
                "dimension_id": dim_id,
                "question_id": q_id,
                "selected_option_ids": [first_option["id"]],
                "points_snapshot": first_option["points"],
                "weight_snapshot": question.get("weight", 1.0)
            })
    
    # Compute scores
    dimension_scores, overall_score, overall_level = engine.compute_scores(responses)
    
    # Assertions
    assert isinstance(dimension_scores, dict)
    assert len(dimension_scores) == len(schema["dimensions"])
    assert 0 <= overall_score <= 100
    assert 1 <= overall_level <= 5
    
    print("[PASS] Basic scoring test passed")
    print(f"  Overall score: {overall_score:.2f}")
    print(f"  Overall level: {overall_level}")
    print(f"  Dimensions scored: {len(dimension_scores)}")
    
    return True


def test_chart_data_generation():
    """
    Test chart data preparation.
    Ensures UI-ready format is generated.
    """
    loader = QuestionnaireLoader()
    schema = loader.load()
    engine = ScoringEngine(schema)
    
    # Create sample dimension scores
    dimension_scores = {}
    for dim in schema["dimensions"]:
        dimension_scores[dim["id"]] = {
            "dimension_id": dim["id"],
            "title": dim["title"],
            "score_0_100": 50.0,
            "level_1_5": 3,
            "drivers": []
        }
    
    # Generate chart data
    chart_data = engine.prepare_chart_data(dimension_scores)
    
    # Assertions
    assert "radar" in chart_data
    assert "bars" in chart_data
    assert len(chart_data["radar"]["labels"]) == len(schema["dimensions"])
    assert len(chart_data["radar"]["values"]) == len(schema["dimensions"])
    assert len(chart_data["bars"]["labels"]) == len(schema["dimensions"])
    assert len(chart_data["bars"]["values"]) == len(schema["dimensions"])
    
    print("[PASS] Chart data generation test passed")
    print(f"  Radar labels count: {len(chart_data['radar']['labels'])}")
    print(f"  Bar labels count: {len(chart_data['bars']['labels'])}")
    
    return True


def test_questionnaire_loading():
    """
    Test questionnaire loader.
    """
    loader = QuestionnaireLoader()
    schema = loader.load()
    
    # Assertions
    assert "questionnaire_id" in schema
    assert "dimensions" in schema
    assert len(schema["dimensions"]) > 0
    
    metadata = loader.get_metadata()
    assert metadata["questionnaire_id"] == schema["questionnaire_id"]
    assert metadata["questions_count"] > 0
    
    print("[PASS] Questionnaire loading test passed")
    print(f"  Questionnaire ID: {metadata['questionnaire_id']}")
    print(f"  Dimensions: {metadata['dimensions_count']}")
    print(f"  Questions: {metadata['questions_count']}")
    
    return True


if __name__ == "__main__":
    print("Running AI-Compass smoke tests...\n")
    
    try:
        test_questionnaire_loading()
        print()
        test_scoring_engine_basic()
        print()
        test_chart_data_generation()
        print()
        print("=" * 50)
        print("[PASS] All tests passed!")
        print("=" * 50)
    
    except Exception as e:
        print(f"\n[FAIL] Tests failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
