"""
Questionnaire loader and validator.
Loads questions.json at runtime and validates structure.
"""
import json
import hashlib
import os
from typing import Dict, Any, Optional
from pathlib import Path


class QuestionnaireLoader:
    """
    Loads and caches the questions.json schema.
    Computes hash for version tracking.
    """
    
    def __init__(self, file_path: Optional[str] = None):
        """
        Initialize loader with questionnaire file path.
        
        Args:
            file_path: Path to questions.json. If None, uses default from env or fallback.
        """
        if file_path is None:
            file_path = os.getenv(
                "QUESTIONNAIRE_PATH",
                "../../data/questionnaire/questions.json"
            )
        
        self.file_path = Path(file_path)
        self._schema: Optional[Dict[str, Any]] = None
        self._hash: Optional[str] = None
        
    def load(self, force_reload: bool = False) -> Dict[str, Any]:
        """
        Load questionnaire schema from JSON file.
        Uses cached version if already loaded unless force_reload=True.
        
        Args:
            force_reload: Force reload from disk even if cached
            
        Returns:
            Parsed questionnaire schema dict
            
        Raises:
            FileNotFoundError: If questionnaire file doesn't exist
            json.JSONDecodeError: If file contains invalid JSON
            ValueError: If schema validation fails
        """
        if self._schema is not None and not force_reload:
            return self._schema
        
        if not self.file_path.exists():
            raise FileNotFoundError(f"Questionnaire file not found: {self.file_path}")
        
        with open(self.file_path, "r", encoding="utf-8") as f:
            content = f.read()
            self._schema = json.loads(content)
            
        # Compute hash for version tracking
        self._hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
        
        # Validate structure (basic checks)
        self._validate_schema(self._schema)
        
        return self._schema
    
    def _validate_schema(self, schema: Dict[str, Any]) -> None:
        """
        Validate questionnaire schema structure.
        
        Args:
            schema: Loaded schema dict
            
        Raises:
            ValueError: If schema is invalid
        """
        required_keys = ["questionnaire_id", "questionnaire_version", "dimensions", "scoring"]
        for key in required_keys:
            if key not in schema:
                raise ValueError(f"Missing required key in schema: {key}")
        
        if not isinstance(schema["dimensions"], list):
            raise ValueError("'dimensions' must be a list")
        
        if len(schema["dimensions"]) == 0:
            raise ValueError("Schema must contain at least one dimension")
        
        # Validate each dimension
        for dim in schema["dimensions"]:
            if "id" not in dim or "title" not in dim or "questions" not in dim:
                raise ValueError(f"Invalid dimension structure: {dim}")
            
            if not isinstance(dim["questions"], list) or len(dim["questions"]) == 0:
                raise ValueError(f"Dimension {dim['id']} must have at least one question")
            
            # Validate each question
            for q in dim["questions"]:
                if "id" not in q or "text" not in q or "options" not in q:
                    raise ValueError(f"Invalid question structure in dimension {dim['id']}: {q}")
                
                if not isinstance(q["options"], list) or len(q["options"]) == 0:
                    raise ValueError(f"Question {q['id']} must have at least one option")
    
    def get_hash(self) -> str:
        """
        Get SHA-256 hash of loaded questionnaire.
        
        Returns:
            Hex digest of questionnaire content hash
            
        Raises:
            RuntimeError: If questionnaire not loaded yet
        """
        if self._hash is None:
            raise RuntimeError("Questionnaire not loaded. Call load() first.")
        return self._hash
    
    def get_metadata(self) -> Dict[str, Any]:
        """
        Get questionnaire metadata (id, version, hash, counts).
        
        Returns:
            Metadata dict
            
        Raises:
            RuntimeError: If questionnaire not loaded yet
        """
        if self._schema is None:
            raise RuntimeError("Questionnaire not loaded. Call load() first.")
        
        questions_count = sum(len(dim["questions"]) for dim in self._schema["dimensions"])
        
        return {
            "questionnaire_id": self._schema["questionnaire_id"],
            "questionnaire_version": self._schema["questionnaire_version"],
            "questionnaire_hash": self.get_hash(),
            "title": self._schema.get("title", ""),
            "language": self._schema.get("language", "en"),
            "estimated_time_minutes": self._schema.get("estimated_time_minutes", 0),
            "dimensions_count": len(self._schema["dimensions"]),
            "questions_count": questions_count,
        }
    
    def get_question_by_id(self, question_id: str) -> Optional[Dict[str, Any]]:
        """
        Find a question by its ID across all dimensions.
        
        Args:
            question_id: Question ID to search for
            
        Returns:
            Question dict if found, None otherwise
        """
        if self._schema is None:
            return None
        
        for dim in self._schema["dimensions"]:
            for q in dim["questions"]:
                if q["id"] == question_id:
                    return q
        
        return None
    
    def get_dimension_by_id(self, dimension_id: str) -> Optional[Dict[str, Any]]:
        """
        Find a dimension by its ID.
        
        Args:
            dimension_id: Dimension ID to search for
            
        Returns:
            Dimension dict if found, None otherwise
        """
        if self._schema is None:
            return None
        
        for dim in self._schema["dimensions"]:
            if dim["id"] == dimension_id:
                return dim
        
        return None
    
    def get_option_by_id(self, question_id: str, option_id: str) -> Optional[Dict[str, Any]]:
        """
        Find an option within a question.
        
        Args:
            question_id: Question ID
            option_id: Option ID
            
        Returns:
            Option dict if found, None otherwise
        """
        question = self.get_question_by_id(question_id)
        if question is None:
            return None
        
        for opt in question.get("options", []):
            if opt["id"] == option_id:
                return opt
        
        return None
    
    def get_scoring_config(self) -> Dict[str, Any]:
        """
        Get scoring configuration from schema.
        
        Returns:
            Scoring config dict
            
        Raises:
            RuntimeError: If questionnaire not loaded yet
        """
        if self._schema is None:
            raise RuntimeError("Questionnaire not loaded. Call load() first.")
        
        return self._schema.get("scoring", {})


# Global singleton instance
_loader_instance: Optional[QuestionnaireLoader] = None


def get_questionnaire_loader() -> QuestionnaireLoader:
    """
    Get global questionnaire loader instance (singleton).
    
    Returns:
        QuestionnaireLoader instance
    """
    global _loader_instance
    if _loader_instance is None:
        _loader_instance = QuestionnaireLoader()
        _loader_instance.load()
    return _loader_instance
