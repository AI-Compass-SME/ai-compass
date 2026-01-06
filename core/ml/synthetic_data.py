"""
Synthetic peer dataset generator for benchmarking.
Creates realistic AI maturity profiles with controlled distributions.
"""
import numpy as np
import os
from typing import List, Dict, Any


class SyntheticDataGenerator:
    """
    Generates synthetic company assessment profiles for benchmarking.
    Uses realistic distributions across maturity levels (Laggards → Scalers).
    """
    
    def __init__(
        self,
        num_profiles: int = None,
        random_state: int = None
    ):
        """
        Initialize synthetic data generator.
        
        Args:
            num_profiles: Number of profiles to generate (default from env or 500)
            random_state: Random seed for reproducibility (default from env or 42)
        """
        self.num_profiles = num_profiles or int(os.getenv("SYNTHETIC_PEER_COUNT", "500"))
        self.random_state = random_state or int(os.getenv("KMEANS_RANDOM_STATE", "42"))
        self.rng = np.random.RandomState(self.random_state)
    
    def generate(
        self,
        question_ids: List[str]
    ) -> np.ndarray:
        """
        Generate synthetic answer profiles.
        
        Each profile is a vector of points (0-4) for each question,
        following realistic distributions:
        - 20% AI Laggards (mostly 0-1 points)
        - 30% AI Curious (mostly 1-2 points)
        - 35% AI Experimenters (mostly 2-3 points)
        - 15% AI Scalers (mostly 3-4 points)
        
        Args:
            question_ids: List of question IDs (determines feature vector length)
            
        Returns:
            Numpy array of shape (num_profiles, num_questions) with values 0-4
        """
        num_questions = len(question_ids)
        profiles = np.zeros((self.num_profiles, num_questions))
        
        # Define segment sizes
        num_laggards = int(self.num_profiles * 0.20)
        num_curious = int(self.num_profiles * 0.30)
        num_experimenters = int(self.num_profiles * 0.35)
        num_scalers = self.num_profiles - num_laggards - num_curious - num_experimenters
        
        # Generate AI Laggards (low maturity)
        profiles[:num_laggards, :] = self._generate_segment(
            count=num_laggards,
            num_questions=num_questions,
            mean_points=0.8,
            std_dev=0.6
        )
        
        # Generate AI Curious
        profiles[num_laggards:num_laggards+num_curious, :] = self._generate_segment(
            count=num_curious,
            num_questions=num_questions,
            mean_points=1.5,
            std_dev=0.7
        )
        
        # Generate AI Experimenters
        profiles[num_laggards+num_curious:num_laggards+num_curious+num_experimenters, :] = self._generate_segment(
            count=num_experimenters,
            num_questions=num_questions,
            mean_points=2.5,
            std_dev=0.7
        )
        
        # Generate AI Scalers (high maturity)
        profiles[num_laggards+num_curious+num_experimenters:, :] = self._generate_segment(
            count=num_scalers,
            num_questions=num_questions,
            mean_points=3.4,
            std_dev=0.5
        )
        
        # Shuffle profiles
        self.rng.shuffle(profiles)
        
        return profiles
    
    def _generate_segment(
        self,
        count: int,
        num_questions: int,
        mean_points: float,
        std_dev: float
    ) -> np.ndarray:
        """
        Generate profiles for a single maturity segment.
        
        Args:
            count: Number of profiles to generate
            num_questions: Number of questions (features)
            mean_points: Mean point value for this segment
            std_dev: Standard deviation
            
        Returns:
            Numpy array of shape (count, num_questions)
        """
        # Generate from normal distribution
        raw = self.rng.normal(loc=mean_points, scale=std_dev, size=(count, num_questions))
        
        # Clip to valid range [0, 4] and round to nearest integer
        clipped = np.clip(raw, 0, 4)
        rounded = np.round(clipped)
        
        return rounded
    
    def compute_overall_scores(
        self,
        profiles: np.ndarray
    ) -> np.ndarray:
        """
        Compute simple overall scores for synthetic profiles.
        Uses average of all questions, normalized to 0-100.
        
        Args:
            profiles: Numpy array of shape (num_profiles, num_questions)
            
        Returns:
            Numpy array of overall scores (0-100), shape (num_profiles,)
        """
        # Average across questions
        avg_points = profiles.mean(axis=1)
        
        # Normalize to 0-100 (points are 0-4)
        scores = (avg_points / 4.0) * 100.0
        
        return scores
