
import pandas as pd
import os
from benchmarking_ai.ml_v5.models import ClusterEngine, StrategicGapAnalyzer, RoadmapGenerator
from benchmarking_ai.ml_v5.utils import generate_narrative_template

class InferenceEngine:
    def __init__(self, artifacts_path="model_artifacts/v5"):
        # Resolve absolute path relative to this file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_dir, artifacts_path)
        
        # Strip extension or prefix logic is handled in load_model usually, 
        # but here we passed "model_artifacts/v4" so models append their suffixes.
        # But wait, load_model takes 'path_prefix'.
        # We need to ensure we pass the right prefix.
        
        self.ce = ClusterEngine()
        self.sga = StrategicGapAnalyzer()
        self.rg = RoadmapGenerator()
        
        try:
            self.ce.load_model(path)
            self.sga.load_model(path)
            self.rg.load_model(path)
            self.loaded = True
            
            # Debug: Print expected columns from RoadmapGenerator
            if self.rg.dim_data_train is not None:
                 cols = [c for c in self.rg.dim_data_train.columns if c not in ['total_maturity', 'industry']]
                 print(f"DEBUG: Model expects dimensions: {cols}")
                 
        except Exception as e:
            print(f"Warning: Models not loaded. {e}")
            self.loaded = False

    def run_analysis(self, company_dim_series, company_question_df, company_industry=None, lang="en"):
        """
        Runs full analysis for a single company.
        company_dim_series: pd.Series of dimension scores.
        company_question_df: pd.DataFrame of question details.
        company_industry: String, optional industry for percentile benchmarking.
        lang: str, 'en' or 'de' for localization.
        """
        if not self.loaded:
            return {"error": "Models not loaded"}
        
        # 1. Cluster Prediction
        # Series to DataFrame (row) for scaler
        df_input = company_dim_series.to_frame().T 
        c_ids, c_names, coords = self.ce.predict(df_input)
        
        # Extract Semantic ID from name (e.g. "5 - Leader" -> 5) to match frontend expectation
        raw_name = c_names[0]
        semantic_id = 0
        try:
             # Assuming format "N - Name"
             if " - " in raw_name:
                 semantic_id = int(raw_name.split(" - ")[0])
             else:
                 # Fallback if just "Cluster N"
                 semantic_id = int(c_ids[0]) + 1 
        except:
             semantic_id = int(c_ids[0]) + 1
             
        cluster_info = {
            "cluster_id": semantic_id, 
            "cluster_name": raw_name,
            "coordinates": coords[0].tolist()
        }
        
        if lang == "de":
            cluster_de_map = {
                "1 - The Traditionalist": "1 - Der Traditionalist",
                "2 - The Experimental Explorer": "2 - Der experimentelle Entdecker",
                "3 - The Structured Builder": "3 - Der strukturierte Aufbauer",
                "4 - The Operational Scaler": "4 - Der operative Skalierer",
                "5 - The AI-Driven Leader": "5 - Der KI-gesteuerte Vorreiter"
            }
            cluster_info["cluster_name"] = cluster_de_map.get(raw_name, raw_name)
        
        # 1.5 Percentile Calculation
        percentile_info = None
        if company_industry:
            total_score = company_dim_series.mean()
            percentile_info = self.ce.calculate_industry_percentile(total_score, company_industry)
        
        # 1.6 Peer Benchmark (Nearest Neighbors)
        peer_scores = self.rg.get_peer_benchmark(company_dim_series, company_industry)
        print(f"DEBUG Peer Scores: {peer_scores}")

        # 2. Strategic Gap Analysis
        findings = self.sga.analyze(company_dim_series, company_question_df, lang=lang)
        narrative = self.sga.synthesize_narrative(findings, company_dim_series, lang=lang)
        
        # 3. Roadmap Generation
        roadmap = self.rg.generate(
            company_id=None, # Not strictly needed if internal logic uses vector search on series
            company_dim_series=company_dim_series, 
            company_question_df=company_question_df,
            strategic_gaps=findings,
            lang=lang
        )
        briefing = self.rg.synthesize_briefing(roadmap, lang=lang)
        
        return {
            "cluster": cluster_info,
            "strategic_findings": findings,
            "executive_briefing": narrative,
            "roadmap": roadmap,
            "roadmap_briefing": briefing,
            "percentile": percentile_info,
            "benchmark_scores": peer_scores
        }

if __name__ == "__main__":
    # Test execution
    print("Inference Engine module.")
