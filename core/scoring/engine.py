"""
Deterministic scoring engine.
Pure rule-based computation with full explainability.
LLMs DO NOT influence scoring.
"""
from typing import Dict, List, Any, Tuple
import statistics


class ScoringEngine:
    """
    Deterministic scoring engine that computes:
    - Question scores (from option points)
    - Dimension scores (weighted average of questions)
    - Overall score (weighted average of dimensions)
    - Maturity levels (1-5 via thresholds)
    - Drivers (low-scoring questions for explainability)
    """
    
    def __init__(self, questionnaire_schema: Dict[str, Any]):
        """
        Initialize scoring engine with questionnaire schema.
        
        Args:
            questionnaire_schema: Loaded questions.json dict
        """
        self.schema = questionnaire_schema
        self.scoring_config = questionnaire_schema.get("scoring", {})
        self.dimensions = {dim["id"]: dim for dim in questionnaire_schema["dimensions"]}
    
    def compute_scores(
        self,
        responses: List[Dict[str, Any]]
    ) -> Tuple[Dict[str, Any], float, int]:
        """
        Compute all scores from responses.
        
        Args:
            responses: List of response dicts with keys:
                - dimension_id
                - question_id
                - selected_option_ids (list)
                - points_snapshot
                - weight_snapshot
        
        Returns:
            Tuple of (dimension_scores_dict, overall_score, overall_level)
            
            dimension_scores_dict format:
            {
                dimension_id: {
                    "dimension_id": str,
                    "title": str,
                    "score_0_100": float,
                    "level_1_5": int,
                    "drivers": [
                        {
                            "question_id": str,
                            "question_text": str,
                            "selected_label": str,
                            "points": float
                        }
                    ]
                }
            }
        """
        # Group responses by dimension
        responses_by_dimension = {}
        for resp in responses:
            dim_id = resp["dimension_id"]
            if dim_id not in responses_by_dimension:
                responses_by_dimension[dim_id] = []
            responses_by_dimension[dim_id].append(resp)
        
        # Compute dimension scores
        dimension_scores = {}
        for dim_id, dim in self.dimensions.items():
            dim_responses = responses_by_dimension.get(dim_id, [])
            
            if len(dim_responses) == 0:
                # No responses for this dimension - use 0 score
                score_0_100 = 0.0
                level = 1
                drivers = []
            else:
                score_0_100, drivers = self._compute_dimension_score(dim, dim_responses)
                level = self._score_to_level(score_0_100)
            
            dimension_scores[dim_id] = {
                "dimension_id": dim_id,
                "title": dim["title"],
                "score_0_100": round(score_0_100, 2),
                "level_1_5": level,
                "drivers": drivers
            }
        
        # Compute overall score (weighted average of dimensions)
        overall_score = self._compute_overall_score(dimension_scores)
        overall_level = self._score_to_level(overall_score)
        
        return dimension_scores, overall_score, overall_level
    
    def _compute_dimension_score(
        self,
        dimension: Dict[str, Any],
        responses: List[Dict[str, Any]]
    ) -> Tuple[float, List[Dict[str, Any]]]:
        """
        Compute score for a single dimension.
        
        Args:
            dimension: Dimension dict from schema
            responses: List of responses for this dimension
            
        Returns:
            Tuple of (score_0_100, drivers_list)
        """
        scale_min = self.scoring_config.get("scale_min", 0)
        scale_max = self.scoring_config.get("scale_max", 4)
        
        # Build question lookup
        questions = {q["id"]: q for q in dimension["questions"]}
        
        # Compute weighted scores
        weighted_sum = 0.0
        weight_sum = 0.0
        question_scores = []  # For driver analysis
        
        for resp in responses:
            q_id = resp["question_id"]
            points = resp["points_snapshot"]  # Already aggregated at answer time
            weight = resp["weight_snapshot"]
            
            # Normalize points to 0-100 scale
            normalized_score = (points / scale_max) * 100.0
            
            weighted_sum += normalized_score * weight
            weight_sum += weight
            
            # Store for driver analysis
            question = questions.get(q_id)
            if question:
                question_scores.append({
                    "question_id": q_id,
                    "question": question,
                    "score": normalized_score,
                    "points": points,
                    "selected_option_ids": resp["selected_option_ids"]
                })
        
        # Compute dimension score
        if weight_sum == 0:
            dimension_score = 0.0
        else:
            dimension_score = weighted_sum / weight_sum
        
        # Identify drivers (lowest 2-3 scoring questions)
        drivers = self._identify_drivers(question_scores)
        
        return dimension_score, drivers
    
    def _identify_drivers(
        self,
        question_scores: List[Dict[str, Any]],
        max_drivers: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Identify low-scoring questions as drivers for explainability.
        
        Args:
            question_scores: List of question score dicts
            max_drivers: Maximum number of drivers to return
            
        Returns:
            List of driver dicts with question_id, text, selected_label, points
        """
        if len(question_scores) == 0:
            return []
        
        # Sort by score (ascending)
        sorted_scores = sorted(question_scores, key=lambda x: x["score"])
        
        # Take bottom N
        drivers_raw = sorted_scores[:max_drivers]
        
        # Format drivers for output
        drivers = []
        for item in drivers_raw:
            question = item["question"]
            selected_option_ids = item["selected_option_ids"]
            
            # Get selected option labels
            option_labels = []
            for opt_id in selected_option_ids:
                for opt in question.get("options", []):
                    if opt["id"] == opt_id:
                        option_labels.append(opt["label"])
                        break
            
            selected_label = ", ".join(option_labels) if option_labels else "N/A"
            
            drivers.append({
                "question_id": item["question_id"],
                "question_text": question["text"],
                "selected_label": selected_label,
                "points": round(item["points"], 2)
            })
        
        return drivers
    
    def _compute_overall_score(
        self,
        dimension_scores: Dict[str, Dict[str, Any]]
    ) -> float:
        """
        Compute overall score as weighted average of dimension scores.
        
        Args:
            dimension_scores: Dict of dimension scores
            
        Returns:
            Overall score (0-100)
        """
        weighted_sum = 0.0
        weight_sum = 0.0
        
        for dim_id, dim_score in dimension_scores.items():
            dim_meta = self.dimensions.get(dim_id)
            if dim_meta is None:
                continue
            
            weight = dim_meta.get("weight", 1.0)
            score = dim_score["score_0_100"]
            
            weighted_sum += score * weight
            weight_sum += weight
        
        if weight_sum == 0:
            return 0.0
        
        return round(weighted_sum / weight_sum, 2)
    
    def _score_to_level(self, score: float) -> int:
        """
        Convert 0-100 score to 1-5 maturity level using thresholds.
        
        Args:
            score: Score (0-100)
            
        Returns:
            Maturity level (1-5)
        """
        thresholds = self.scoring_config.get("levels_1_to_5_thresholds", [])
        
        for threshold in thresholds:
            level = threshold["level"]
            min_score = threshold["min_score_inclusive"]
            max_score = threshold["max_score_inclusive"]
            
            if min_score <= score <= max_score:
                return level
        
        # Fallback (should not happen with valid schema)
        if score < 20:
            return 1
        elif score < 40:
            return 2
        elif score < 60:
            return 3
        elif score < 80:
            return 4
        else:
            return 5
    
    def prepare_chart_data(
        self,
        dimension_scores: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Prepare chart-ready data for UI (radar + bar charts).
        
        Args:
            dimension_scores: Dict of dimension scores
            
        Returns:
            Chart data dict with 'radar' and 'bars' keys
        """
        # Sort dimensions by order
        sorted_dims = sorted(
            dimension_scores.values(),
            key=lambda x: self.dimensions.get(x["dimension_id"], {}).get("order", 999)
        )
        
        # Radar chart data (ordered by dimension order)
        radar_labels = [d["title"] for d in sorted_dims]
        radar_values = [d["score_0_100"] for d in sorted_dims]
        
        # Bar chart data (sorted by score, low to high)
        sorted_by_score = sorted(sorted_dims, key=lambda x: x["score_0_100"])
        bar_labels = [d["title"] for d in sorted_by_score]
        bar_values = [d["score_0_100"] for d in sorted_by_score]
        
        return {
            "radar": {
                "labels": radar_labels,
                "values": radar_values,
                "min_value": 0,
                "max_value": 100
            },
            "bars": {
                "labels": bar_labels,
                "values": bar_values,
                "min_value": 0,
                "max_value": 100
            }
        }
