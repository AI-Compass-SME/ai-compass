"""
LLM enrichment service using Groq.
LLMs generate TEXT ONLY - never influence scoring or levels.
Results are cached to reduce API calls.
"""
import os
import json
import hashlib
from typing import Dict, Any, Optional, List
from groq import Groq
from tenacity import retry, stop_after_attempt, wait_exponential
from sqlalchemy.orm import Session
from models.assessment import LLMEnrichmentCache
from datetime import datetime


class LLMService:
    """
    Service for generating executive-readable recommendations using LLM.
    Includes caching and fallback to deterministic templates.
    """
    
    DETERMINISTIC_TEMPLATE = {
        "executive_summary": "Ihre Organisation zeigt eine durchschnittliche KI-Reife. Es gibt Potenzial zur Verbesserung in mehreren Bereichen.",
        "quick_wins": [
            "KI-Strategie klären und kommunizieren",
            "Datenqualität in Kernsystemen verbessern",
            "Pilotprojekt mit klarem ROI starten"
        ],
        "roadmap": {
            "days_90": [
                "Executive Sponsorship sicherstellen",
                "Initiale Use Cases identifizieren",
                "Governance-Grundlagen definieren"
            ],
            "months_6": [
                "Data Governance etablieren",
                "Erste Piloten in Produktion bringen",
                "Team-Enablement starten"
            ],
            "months_12": [
                "KI-Betriebsmodell skalieren",
                "Messbare Business-Ergebnisse nachweisen",
                "Kontinuierliche Verbesserung etablieren"
            ]
        },
        "risks": [
            "Fehlende Executive-Unterstützung",
            "Datenqualität und -zugriff",
            "Mangelnde KI-Kompetenz im Team"
        ]
    }
    
    def __init__(self, db: Session = None):
        """
        Initialize LLM service.
        
        Args:
            db: Database session for caching (optional)
        """
        self.db = db
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")
        self.temperature = float(os.getenv("GROQ_TEMPERATURE", "0.2"))
        self.max_tokens = int(os.getenv("GROQ_MAX_TOKENS", "2048"))
        self.cache_enabled = os.getenv("LLM_CACHE_ENABLED", "true").lower() == "true"
        
        if self.api_key:
            self.client = Groq(api_key=self.api_key)
        else:
            self.client = None
    
    def generate_recommendations(
        self,
        company_meta: Dict[str, Any],
        dimension_scores: List[Dict[str, Any]],
        overall_score: float,
        overall_level: int,
        benchmark: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate executive recommendations using LLM.
        Falls back to deterministic template if LLM fails.
        
        Args:
            company_meta: Company metadata
            dimension_scores: List of dimension score dicts
            overall_score: Overall maturity score (0-100)
            overall_level: Overall maturity level (1-5)
            benchmark: Benchmark result dict
            
        Returns:
            Recommendations dict with keys:
            - executive_summary (str)
            - quick_wins (list of str)
            - roadmap (dict with days_90, months_6, months_12)
            - risks (list of str)
        """
        # Build cache key
        cache_key = self._build_cache_key(
            company_meta,
            dimension_scores,
            overall_score,
            benchmark
        )
        
        # Try cache first
        if self.cache_enabled and self.db:
            cached = self._get_from_cache(cache_key)
            if cached:
                return cached
        
        # Generate with LLM
        if self.client:
            try:
                recommendations = self._generate_with_llm(
                    company_meta,
                    dimension_scores,
                    overall_score,
                    overall_level,
                    benchmark
                )
                
                # Cache result
                if self.cache_enabled and self.db:
                    self._save_to_cache(cache_key, recommendations)
                
                return recommendations
            except Exception as e:
                print(f"LLM generation failed: {e}. Falling back to template.")
                return self.DETERMINISTIC_TEMPLATE.copy()
        else:
            # No API key - use template
            return self.DETERMINISTIC_TEMPLATE.copy()
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def _generate_with_llm(
        self,
        company_meta: Dict[str, Any],
        dimension_scores: List[Dict[str, Any]],
        overall_score: float,
        overall_level: int,
        benchmark: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate recommendations using Groq LLM with retries.
        
        Returns:
            Recommendations dict
        """
        # Build prompt
        prompt = self._build_prompt(
            company_meta,
            dimension_scores,
            overall_score,
            overall_level,
            benchmark
        )
        
        # Call Groq API
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "Du bist ein erfahrener KI-Strategieberater. Generiere klare, umsetzbare Empfehlungen auf Deutsch. Antworte ausschließlich mit validem JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            response_format={"type": "json_object"}
        )
        
        # Parse response
        content = response.choices[0].message.content
        recommendations = json.loads(content)
        
        # Validate structure
        required_keys = ["executive_summary", "quick_wins", "roadmap", "risks"]
        for key in required_keys:
            if key not in recommendations:
                raise ValueError(f"LLM response missing key: {key}")
        
        return recommendations
    
    def _build_prompt(
        self,
        company_meta: Dict[str, Any],
        dimension_scores: List[Dict[str, Any]],
        overall_score: float,
        overall_level: int,
        benchmark: Dict[str, Any]
    ) -> str:
        """
        Build LLM prompt from assessment data.
        
        Returns:
            Prompt string
        """
        # Find top 3 weakest dimensions
        sorted_dims = sorted(dimension_scores, key=lambda x: x["score_0_100"])
        weakest = sorted_dims[:3]
        
        weak_areas = ", ".join([d["title"] for d in weakest])
        
        # Build context
        industry = company_meta.get("industry", "unbekannt")
        employee_band = company_meta.get("employee_band", "unbekannt")
        cluster_label = benchmark.get("cluster_label", "N/A")
        
        prompt = f"""Generiere umsetzbare KI-Empfehlungen für ein Unternehmen mit folgenden Eigenschaften:

**Unternehmen:**
- Branche: {industry}
- Mitarbeiter: {employee_band}

**Reifegrad:**
- Gesamtscore: {overall_score}/100 (Level {overall_level}/5)
- Benchmark-Cluster: {cluster_label}
- Schwächste Bereiche: {weak_areas}

**Dimensions-Details:**
{self._format_dimensions(dimension_scores)}

Erstelle eine JSON-Antwort mit:
1. executive_summary: Max 2 Sätze, strategisch, keine Buzzwords
2. quick_wins: 3-5 konkrete Maßnahmen für 0-30 Tage
3. roadmap: Objekt mit days_90, months_6, months_12 (jeweils 3-5 Punkte)
4. risks: 3-5 Hauptrisiken

Fokus: Praktisch, priorisiert, umsetzbar. Keine generischen Phrasen.

JSON-Format:
{{
  "executive_summary": "...",
  "quick_wins": ["...", "..."],
  "roadmap": {{
    "days_90": ["...", "..."],
    "months_6": ["...", "..."],
    "months_12": ["...", "..."]
  }},
  "risks": ["...", "..."]
}}
"""
        return prompt
    
    def _format_dimensions(self, dimension_scores: List[Dict[str, Any]]) -> str:
        """Format dimension scores for prompt."""
        lines = []
        for dim in dimension_scores:
            lines.append(f"- {dim['title']}: {dim['score_0_100']}/100 (Level {dim['level_1_5']})")
        return "\n".join(lines)
    
    def _build_cache_key(
        self,
        company_meta: Dict[str, Any],
        dimension_scores: List[Dict[str, Any]],
        overall_score: float,
        benchmark: Dict[str, Any]
    ) -> str:
        """
        Build deterministic cache key from inputs.
        
        Returns:
            SHA-256 hex digest
        """
        # Build stable string representation
        cache_input = {
            "company_meta": company_meta,
            "dimension_scores": [{
                "dimension_id": d["dimension_id"],
                "score": d["score_0_100"],
                "level": d["level_1_5"]
            } for d in dimension_scores],
            "overall_score": round(overall_score, 2),
            "cluster_label": benchmark.get("cluster_label", "")
        }
        
        cache_str = json.dumps(cache_input, sort_keys=True)
        return hashlib.sha256(cache_str.encode("utf-8")).hexdigest()
    
    def _get_from_cache(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve from cache if exists.
        
        Args:
            cache_key: Cache key
            
        Returns:
            Cached payload dict or None
        """
        try:
            cached = self.db.query(LLMEnrichmentCache).filter(
                LLMEnrichmentCache.cache_key == cache_key
            ).first()
            
            if cached:
                return cached.payload
        except Exception as e:
            print(f"Cache read error: {e}")
        
        return None
    
    def _save_to_cache(self, cache_key: str, payload: Dict[str, Any]) -> None:
        """
        Save to cache.
        
        Args:
            cache_key: Cache key
            payload: Recommendations dict
        """
        try:
            cache_entry = LLMEnrichmentCache(
                cache_key=cache_key,
                payload=payload,
                created_at=datetime.utcnow()
            )
            self.db.add(cache_entry)
            self.db.commit()
        except Exception as e:
            print(f"Cache save error: {e}")
            self.db.rollback()
