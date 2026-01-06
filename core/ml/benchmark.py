"""
ML benchmarking service using K-Means clustering.
Pure optics for peer grouping - does NOT influence scoring.
"""
import numpy as np
import os
from typing import List, Dict, Any, Tuple
from sklearn.cluster import KMeans
from core.ml.synthetic_data import SyntheticDataGenerator


class BenchmarkService:
    """
    Benchmarks a user's assessment against synthetic peers using K-Means.
    Provides cluster label, percentile, and mismatch detection.
    """
    
    # Cluster labels ordered by maturity (low to high)
    CLUSTER_LABELS = [
        "AI Laggards",
        "AI Curious",
        "AI Experimenters",
        "AI Scalers"
    ]
    
    def __init__(
        self,
        question_ids: List[str],
        num_clusters: int = None,
        random_state: int = None
    ):
        """
        Initialize benchmark service.
        
        Args:
            question_ids: Ordered list of question IDs (defines feature order)
            num_clusters: Number of K-Means clusters (default from env or 4)
            random_state: Random seed for reproducibility
        """
        self.question_ids = question_ids
        self.num_clusters = num_clusters or int(os.getenv("KMEANS_CLUSTERS", "4"))
        self.random_state = random_state or int(os.getenv("KMEANS_RANDOM_STATE", "42"))
        
        # Generate synthetic dataset
        generator = SyntheticDataGenerator(random_state=self.random_state)
        self.synthetic_profiles = generator.generate(question_ids)
        self.synthetic_scores = generator.compute_overall_scores(self.synthetic_profiles)
        
        # Train K-Means model
        self.kmeans = KMeans(
            n_clusters=self.num_clusters,
            random_state=self.random_state,
            n_init=10
        )
        self.kmeans.fit(self.synthetic_profiles)
        
        # Compute cluster labels based on centroid maturity
        self.cluster_label_map = self._compute_cluster_labels()
    
    def _compute_cluster_labels(self) -> Dict[int, str]:
        """
        Map cluster IDs to human-readable labels based on centroid maturity.
        
        Returns:
            Dict mapping cluster_id (int) to label (str)
        """
        # Compute average maturity for each cluster centroid
        centroid_scores = []
        for i in range(self.num_clusters):
            centroid = self.kmeans.cluster_centers_[i]
            avg_points = centroid.mean()
            centroid_scores.append((i, avg_points))
        
        # Sort by maturity (low to high)
        sorted_clusters = sorted(centroid_scores, key=lambda x: x[1])
        
        # Assign labels
        label_map = {}
        for rank, (cluster_id, _) in enumerate(sorted_clusters):
            if rank < len(self.CLUSTER_LABELS):
                label_map[cluster_id] = self.CLUSTER_LABELS[rank]
            else:
                label_map[cluster_id] = f"Cluster {cluster_id}"
        
        return label_map
    
    def benchmark(
        self,
        user_responses: List[Dict[str, Any]],
        user_overall_score: float
    ) -> Dict[str, Any]:
        """
        Benchmark user's responses against synthetic peers.
        
        Args:
            user_responses: List of user response dicts (dimension_id, question_id, points_snapshot)
            user_overall_score: User's overall score (0-100)
            
        Returns:
            Benchmark result dict:
            {
                "cluster_id": int,
                "cluster_label": str,
                "percentile": float,
                "mismatch_flag": bool,
                "mismatch_note": str or None
            }
        """
        # Build user feature vector
        user_vector = self._build_feature_vector(user_responses)
        
        # Predict cluster
        cluster_id = int(self.kmeans.predict([user_vector])[0])
        cluster_label = self.cluster_label_map.get(cluster_id, f"Cluster {cluster_id}")
        
        # Compute percentile vs synthetic peers (based on overall score)
        percentile = self._compute_percentile(user_overall_score, self.synthetic_scores)
        
        # Detect mismatch (high score but low cluster, or vice versa)
        mismatch_flag, mismatch_note = self._detect_mismatch(
            cluster_id,
            cluster_label,
            user_overall_score,
            percentile
        )
        
        return {
            "cluster_id": cluster_id,
            "cluster_label": cluster_label,
            "percentile": round(percentile, 1),
            "mismatch_flag": mismatch_flag,
            "mismatch_note": mismatch_note
        }
    
    def _build_feature_vector(
        self,
        responses: List[Dict[str, Any]]
    ) -> np.ndarray:
        """
        Build feature vector from user responses.
        Must match order of self.question_ids.
        
        Args:
            responses: List of response dicts
            
        Returns:
            Numpy array of shape (num_questions,)
        """
        # Build lookup dict
        response_dict = {r["question_id"]: r["points_snapshot"] for r in responses}
        
        # Build ordered feature vector
        feature_vector = []
        for q_id in self.question_ids:
            points = response_dict.get(q_id, 0.0)  # Default to 0 if missing
            feature_vector.append(points)
        
        return np.array(feature_vector)
    
    def _compute_percentile(
        self,
        user_score: float,
        peer_scores: np.ndarray
    ) -> float:
        """
        Compute user's percentile vs peer scores.
        
        Args:
            user_score: User's overall score (0-100)
            peer_scores: Array of peer scores
            
        Returns:
            Percentile (0-100)
        """
        # Count how many peers have lower score
        lower_count = np.sum(peer_scores < user_score)
        total_count = len(peer_scores)
        
        if total_count == 0:
            return 50.0  # Fallback
        
        percentile = (lower_count / total_count) * 100.0
        return percentile
    
    def _detect_mismatch(
        self,
        cluster_id: int,
        cluster_label: str,
        user_score: float,
        percentile: float
    ) -> Tuple[bool, str]:
        """
        Detect mismatch between score and cluster.
        
        Examples:
        - High overall score (80+) but clustered with "AI Laggards"
        - Low overall score (30-) but clustered with "AI Scalers"
        
        Args:
            cluster_id: Predicted cluster ID
            cluster_label: Cluster label
            user_score: Overall score (0-100)
            percentile: Percentile vs peers
            
        Returns:
            Tuple of (mismatch_flag, mismatch_note)
        """
        # Find cluster rank (0 = lowest maturity, 3 = highest)
        cluster_rank = None
        for label_rank, label in enumerate(self.CLUSTER_LABELS):
            if cluster_label == label:
                cluster_rank = label_rank
                break
        
        if cluster_rank is None:
            return False, None
        
        # Detect high score + low cluster
        if user_score >= 70 and cluster_rank <= 1:  # Scalers/Experimenters score but Laggards/Curious cluster
            return True, "Hoher Score, aber niedrigeres Cluster – ungleichmäßige Reife in einzelnen Bereichen."
        
        # Detect low score + high cluster
        if user_score <= 40 and cluster_rank >= 2:  # Laggards/Curious score but Experimenters/Scalers cluster
            return True, "Niedriger Score, aber höheres Cluster – einzelne starke Bereiche, aber insgesamt Nachholbedarf."
        
        return False, None
    
    def get_model_version(self) -> str:
        """
        Get model version identifier.
        
        Returns:
            Model version string
        """
        return f"kmeans_c{self.num_clusters}_s{self.random_state}"
