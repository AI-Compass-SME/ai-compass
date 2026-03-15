
import pandas as pd
import numpy as np
import pickle
import json
import os
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from scipy.stats import zscore
from benchmarking_ai.ml_v5.utils import RISK_PAIRS, PHASE_MAPPING

class ClusterEngine:
    def __init__(self, n_clusters=5):
        self.n_clusters = n_clusters
        self.model = None
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=2)
        self.profiles = None 
        self.labels_map = {}
        self.industry_data = None  # Store for percentile calculation

    def fit(self, data, cluster_profiles=None, industry_data=None):
        """
        Fit the clustering model.
        
        Args:
            data: DataFrame with dimension scores
            cluster_profiles: Optional cluster profile metadata
            industry_data: Optional DataFrame with company_id, industry, total_maturity columns
        """
        self.profiles = cluster_profiles
        self.industry_data = industry_data  # Store for percentile calculation
        
        X = self.scaler.fit_transform(data.fillna(0))
        
        self.model = KMeans(n_clusters=self.n_clusters, random_state=42)
        self.model.fit(X)
        self.pca.fit(X)
        
        self._build_label_map(data, self.model.labels_)

    def _build_label_map(self, data, labels):
        df = data.copy()
        df['Cluster'] = labels
        means = df.groupby('Cluster').mean().mean(axis=1)
        sorted_clusters = means.sort_values().index.tolist()
        
        self.labels_map = {}
        hybrid_names = [
            "1 - The Traditionalist",
            "2 - The Experimental Explorer", 
            "3 - The Structured Builder",
            "4 - The Operational Scaler",
            "5 - The AI-Driven Leader"
        ]
        
        if self.profiles is not None and not self.profiles.empty:
             sorted_profiles = self.profiles.sort_values('cluster_id').to_dict('records')
             for rank_idx, cluster_idx in enumerate(sorted_clusters):
                 p_idx = min(rank_idx, len(sorted_profiles)-1)
                 p = sorted_profiles[p_idx]
                 self.labels_map[cluster_idx] = f"{p['cluster_id']} - {p['cluster_name']}"
        else:
             for rank_idx, cluster_idx in enumerate(sorted_clusters):
                 name = hybrid_names[min(rank_idx, 4)]
                 self.labels_map[cluster_idx] = name

    def predict(self, company_df):
        X_new = self.scaler.transform(company_df.fillna(0))
        cluster_ids = self.model.predict(X_new)
        coords = self.pca.transform(X_new)
        
        names = [self.labels_map.get(c, f"Cluster {c}") for c in cluster_ids]
        
        return cluster_ids, names, coords
    
    def calculate_industry_percentile(self, company_total_maturity, company_industry):
        """
        Calculate industry-specific percentile ranking.
        
        Args:
            company_total_maturity: Company's total maturity score
            company_industry: Company's industry
            
        Returns:
            dict with percentile_value, percentage, industry, and industry_sample_size
        """
        if self.industry_data is None:
            return None
        
        # Filter to same industry
        industry_companies = self.industry_data[
            self.industry_data['industry'] == company_industry
        ]
        
        benchmark_group = company_industry
        
        # Fallback to Global if industry sample is too small (< 5)
        if len(industry_companies) < 5:
            industry_companies = self.industry_data
            benchmark_group = "Global"
        
        if len(industry_companies) == 0:
            return None
        
        # Calculate percentile (percentage of companies with lower score)
        lower_count = (industry_companies['total_maturity'] < company_total_maturity).sum()
        percentile = (lower_count / len(industry_companies)) * 100
        
        return {
            'percentile_value': f"{percentile:.2f}",
            'percentage': f"{max(1, 100 - percentile):.0f}",  # Inverted for "Top X%" logic
            'industry': benchmark_group,
            'industry_sample_size': len(industry_companies)
        }

    def save_model(self, path_prefix):
        with open(f"{path_prefix}_kmeans.pkl", 'wb') as f:
            pickle.dump(self.model, f)
        with open(f"{path_prefix}_scaler.pkl", 'wb') as f:
            pickle.dump(self.scaler, f)
        with open(f"{path_prefix}_pca.pkl", 'wb') as f:
            pickle.dump(self.pca, f)
        with open(f"{path_prefix}_labels.json", 'w') as f:
            json.dump(self.labels_map, f)
        # Save industry data for percentile calculation
        if self.industry_data is not None:
            self.industry_data.to_pickle(f"{path_prefix}_industry_data.pkl")

    def load_model(self, path_prefix):
        with open(f"{path_prefix}_kmeans.pkl", 'rb') as f:
            self.model = pickle.load(f)
        with open(f"{path_prefix}_scaler.pkl", 'rb') as f:
            self.scaler = pickle.load(f)
        with open(f"{path_prefix}_pca.pkl", 'rb') as f:
            self.pca = pickle.load(f)
        with open(f"{path_prefix}_labels.json", 'r') as f:
            loaded_map = json.load(f)
            self.labels_map = {int(k): v for k, v in loaded_map.items()}
        # Load industry data if available
        industry_path = f"{path_prefix}_industry_data.pkl"
        if os.path.exists(industry_path):
            self.industry_data = pd.read_pickle(industry_path)

class StrategicGapAnalyzer:
    def __init__(self):
        self.pair_stats = {} # {pair_key: {mean, std}}
        self.dim_benchmarks = {} # {dim_name: mean_score}

    def fit(self, dim_data):
        """
        Learns population statistics for Risk Pairs and Benchmark Averages.
        dim_data: DataFrame (index=company_id, cols=Dimensions)
        """
        df = dim_data.copy().fillna(0)
        
        # 1. Benchmark Averages
        self.dim_benchmarks = df.mean().to_dict()
        
        # 2. Risk Pair Stats
        for p1, p2 in RISK_PAIRS:
            if p1 in df.columns and p2 in df.columns:
                gap_vals = (df[p1] - df[p2]).abs() # Magnitude of imbalance
                self.pair_stats[f"{p1}|{p2}"] = {
                    'mean': float(gap_vals.mean()),
                    'std': float(gap_vals.std())
                }

    def analyze(self, company_dim_series, company_question_df, lang="en"):
        """
        Analyzes a single company for Strategic Gaps.
        company_dim_series: Series of dimension scores.
        company_question_df: DataFrame with ('question_id', 'question_text', 'question_weight', 'score_1to5', 'question_type')
                             filtered for THIS company.
        lang: str, 'en' or 'de' for localization.
        """
        findings = []
        
        # --- Stage 1: Z-Score Anomalies ---
        for pair_key, stat in self.pair_stats.items():
            p1, p2 = pair_key.split('|')
            if p1 in company_dim_series and p2 in company_dim_series:
                gap = abs(company_dim_series[p1] - company_dim_series[p2])
                z = (gap - stat['mean']) / (stat['std'] + 1e-9)
                
                if z > 1.5:
                    dim_de_map = {
                        "Strategy & Business Vision": "Strategie & Vision",
                        "People & Culture": "Menschen & Kultur",
                        "Data Readiness & Literacy": "Datenkompetenz",
                        "Use Cases & Business Value": "Anwendungsfälle & Geschäftswert",
                        "Processes & Scaling": "Prozesse & Skalierbarkeit",
                        "Governance & Compliance": "Governance & Compliance",
                        "Tech Infrastructure": "Technologie & Infrastruktur",
                    }
                    
                    p1_out = dim_de_map.get(p1, p1) if lang == 'de' else p1
                    p2_out = dim_de_map.get(p2, p2) if lang == 'de' else p2
                    
                    title = f"Structural Imbalance: {p1_out} vs {p2_out}" if lang == 'en' else f"Strukturelles Ungleichgewicht: {p1_out} vs {p2_out}"
                    context = f"Gap of {gap:.1f} points (Z={z:.1f}). Disconnect between {p1_out} ({company_dim_series[p1]:.1f}) and {p2_out} ({company_dim_series[p2]:.1f})." if lang == 'en' else f"Lücke von {gap:.1f} Punkten (Z={z:.1f}). Unstimmigkeit zwischen {p1_out} ({company_dim_series[p1]:.1f}) und {p2_out} ({company_dim_series[p2]:.1f})."

                    findings.append({
                        "type": "Anomaly",
                        "title": title,
                        "score": z, # Use Z as severity
                        "context": context,
                        "source_dim": p1 if company_dim_series[p1] < company_dim_series[p2] else p2, # The lower one is the bottleneck usually, but anomaly is the relationship
                        "strategic_risk": self._get_strategic_risk("Structural Imbalance", z, f"{p1} vs {p2}", lang)
                    })

        # --- Stage 2: Weighted Impact Gaps ---
        # Calculate Weighted Impact for ALL questions
        # Need: question_weight, score (converted to gap), type
        
        # We process the company_question_df to get high impact items
        # assuming company_question_df has 'question_weight', 'score_1to5', 'question_type', 'tactical_theme', 'dimension_name'
        
        impact_candidates = []
        if not company_question_df.empty:
            for _, row in company_question_df.iterrows():
                w = row.get('question_weight', 0)
                s = row.get('score_1to5', 1)
                q_type = row.get('question_type', 'Slider')
                
                if q_type == 'Checklist':
                    # If score is low (e.g. < 3), impact is high
                    impact = (w * 2) if s < 3.0 else 0
                else:
                    impact = w * (5.0 - s)
                
                if impact > 0:
                    theme_en = row.get('tactical_theme', 'Unknown Theme')
                    theme_de = row.get('tactical_theme_de', theme_en)
                    dim_name_en = row.get('dimension_name')
                    dim_name_de = row.get('dimension_name_de', dim_name_en)
                    
                    title = f"Critical Gap: {theme_en}" if lang == 'en' else f"Kritische Lücke: {theme_de}"
                    context = f"High Strategic Impact ({w}). Current Maturity: {s:.1f}. Theme: {theme_en}." if lang == 'en' else f"Hohe strategische Relevanz ({w}). Aktuelle Reife: {s:.1f}. Thema: {theme_de}."
                    
                    impact_candidates.append({
                        "type": "Weakness",
                        "title": title,
                        "score": impact,
                        "context": context,
                        "dimension_name": dim_name_en, # Kept for internal matching
                        "dimension_name_out": dim_name_en if lang == 'en' else dim_name_de,
                        "tactical_theme": theme_en, # Kept for deduplication
                        "tactical_theme_out": theme_en if lang == 'en' else theme_de,
                        "question_id": row.get('question_id'),
                        "strategic_risk": self._get_strategic_risk(theme_en, impact, dim_name_en, lang)
                    })
        
        # Sort by Impact
        impact_candidates.sort(key=lambda x: x['score'], reverse=True)
        
        # Fill Findings (Target: 2)
        final_findings = findings[:2]
        
        if len(final_findings) < 2:
            needed = 2 - len(final_findings)
            # Filter candidates to avoid effective duplicates if needed, or just take top N
            # For simplicity, take top N not already covered (though anomaly covers dimension, this is specific)
            
            for item in impact_candidates:
                if len(final_findings) >= 2: break
                final_findings.append(item)
                
        return final_findings
    
    def _get_strategic_risk(self, theme, score, dimension, lang="en"):
        """
        Returns theme-specific strategic risk text.
        """
        if not theme:
            if lang == "de":
                return f"Diese Lücke in {dimension} birgt potenzielle Skalierbarkeitsrisiken."
            return f"This gap in {dimension} creates potential liabilities in scalability."
            
        theme_lower = theme.lower()
        
        # Structural Imbalance logic
        if "structural imbalance" in theme_lower:
            if lang == "de":
                return f"Die Diskrepanz in {dimension} erzeugt organisatorische Reibungsverluste, die die Geschwindigkeit der KI-Einführung verlangsamen."
            return f"The disconnect between {dimension} creates organizational friction that will slow down AI adoption velocity."
            
        # Specific Themes
        if 'staff' in theme_lower or 'proficiency' in theme_lower:
            if lang == "de":
                return "Ohne gezielte Weiterbildung der Belegschaft fehlt spezifischen technischen Tools die nötige Akzeptanz für einen ROI, was zu ungenutzten Systemen und Fehlinvestitionen führt."
            return "Without addressing workforce upskilling, specific technical tools will lack the adoption needed for ROI, leading to 'shelf-ware' and wasted investment."
            
        if 'leadership' in theme_lower or 'alignment' in theme_lower:
            if lang == "de":
                return "Die Diskrepanz zwischen technischen Fähigkeiten und der Vision der Geschäftsführung schafft 'stategische Schulden' und riskiert den Projektabbruch mangels klarem Geschäftswert."
            return "The disconnect between technical capabilities and executive vision creates 'Strategic Debt', risking project cancellation due to lack of clear business value."
            
        if 'budget' in theme_lower or 'allocation' in theme_lower:
             if lang == "de":
                 return "Unzureichende oder falsch zugewiesene Budgets für KI-Initiativen verhindern, dass das Unternehmen über die Pilotphase hinauskommt."
             return "Insufficient or misaligned funding for AI initiatives will stall progress, preventing the organization from moving beyond pilot phases to production-grade deployment."
             
        if 'data' in theme_lower and ('privacy' in theme_lower or 'governance' in theme_lower):
            if lang == "de":
                return "Mangelhafte Data Governance birgt kritische rechtliche und Reputationsrisiken, insbesondere im Hinblick auf kommende Regulierungen wie den EU AI Act."
            return "Lack of robust data governance poses critical legal and reputational risks, especially with upcoming regulations like the EU AI Act."
            
        if 'standardization' in theme_lower or 'scaling' in theme_lower:
            if lang == "de":
                return "Ad-hoc-Prozesse ohne Standardisierung führen zu technischen Schulden und mangelnder Skalierbarkeit, was die Wartung von KI exponentiell verteuert."
            return "Ad-hoc processes without standardization will result in technical debt and inability to scale, making AI maintenance exponentially expensive."
            
        if 'infrastructure' in theme_lower or 'tooling' in theme_lower:
            if lang == "de":
                return "Unzureichende Infrastruktur schafft Leistungsengpässe, die die Komplexität und Geschwindigkeit der einsetzbaren KI-Modelle einschränken."
            return "Inadequate infrastructure creates performance bottlenecks that limit the complexity and speed of AI models you can deploy effectively."
            
        if 'adoption' in theme_lower or 'culture' in theme_lower:
            if lang == "de":
                return "Eine Unternehmenskultur, die sich gegen KI sträubt, untergräbt die technische Umsetzung, da Anwender den neuen Systemen nicht vertrauen."
            return "A culture resistant to AI adoption will undermine technical implementation, as users fail to trust or integrate new systems into their daily workflows."

        if 'strategy' in theme_lower or 'vision' in theme_lower:
            if lang == "de":
                return "Ein Vorgehen ohne klare KI-Strategie riskiert fragmentierte Bemühungen, die nicht zu den übergeordneten Geschäftszielen beitragen."
            return "Proceeding without a clear AI strategy risks fragmented efforts that fail to contribute to overarching business goals."

        if 'use case' in theme_lower or 'business value' in theme_lower:
            if lang == "de":
                return "Eine Fokussierung rein auf die Technologie statt auf den Mehrwert birgt das Risiko, dass Lösungen für die falschen Probleme entwickelt werden (geringer ROI)."
            return "Focusing on technology over business value risks deploying solutions that solve the wrong problems, leading to low impact and poor ROI."

        # Default fallback
        if lang == "de":
            return f"Diese Lücke in {dimension} führt zu potenziellen Risiken bezüglich Skalierbarkeit und langfristiger Wertschöpfung."
        return f"This gap in {dimension} creates potential liabilities in scalability and long-term value realization."

    def synthesize_narrative(self, findings, company_scores, lang="en"):
        """
        Generates the consultant narrative.
        """
        header = "### 🎖️ AI-Compass Strategic Briefing" if lang == 'en' else "### 🎖️ AI-Compass Strategisches Briefing"
        narrative = f"{header}\n\n"
        
        if len(findings) >= 2:
             f1_name = findings[0]['title']
             f2_name = findings[1]['title']
             if lang == 'de':
                 narrative += f"Unsere Analyse Ihres aktuellen KI-Reifegrads identifiziert **{f1_name}** und **{f2_name}** als strukturelle Hauptrisiken, die sofortige Aufmerksamkeit des Managements erfordern.\n\n"
             else:
                 narrative += f"Our analysis of your current AI maturity profile identifies **{f1_name}** and **{f2_name}** as primary structural risks that require immediate executive attention.\n\n"
        elif len(findings) == 1:
             f1_name = findings[0]['title']
             if lang == 'de':
                  narrative += f"Unsere Analyse Ihres aktuellen KI-Reifegrads identifiziert **{f1_name}** als ein strukturelles Hauptrisiko, das sofortige Aufmerksamkeit des Managements erfordert.\n\n"
             else:
                  narrative += f"Our analysis of your current AI maturity profile identifies **{f1_name}** as a primary structural risk that requires immediate executive attention.\n\n"
        else:
             if lang == 'de':
                  narrative += "Unsere Analyse Ihres aktuellen KI-Reifegrads zeigt eine ausgewogene Struktur, auch wenn Optimierungsmöglichkeiten bestehen.\n\n"
             else:
                  narrative += "Our analysis of your current AI maturity profile shows a balanced structure, though optimization opportunities exist.\n\n"
        
        if lang == 'de':
            narrative += "**Strategisches Fazit**: Ihr Profil zeigt hohes Potenzial, ist aber derzeit entkoppelt. Eine Priorisierung dieser beiden Bereiche in den nächsten 3 Monaten wird Ihre KI-Initiativen von der experimentellen Phase zur Skalierbarkeit führen."
        else:
            narrative += "**Strategic Verdict**: Your profile shows high potential but is currently decoupled. Prioritizing these two areas over the next 3 months will transform your AI initiatives from experimental to scalable."
        return narrative

    def save_model(self, path_prefix):
        state = {'pair_stats': self.pair_stats, 'dim_benchmarks': self.dim_benchmarks}
        with open(f"{path_prefix}_gap_analyzer.pkl", 'wb') as f:
            pickle.dump(state, f)

    def load_model(self, path_prefix):
        with open(f"{path_prefix}_gap_analyzer.pkl", 'rb') as f:
            state = pickle.load(f)
            self.pair_stats = state['pair_stats']
            self.dim_benchmarks = state['dim_benchmarks']


class RoadmapGenerator:
    def __init__(self):
        self.knn = None
        self.scaler = StandardScaler()
        self.dim_data_train = None # Store for looking up peers
        self.question_data_train = None # Store for looking up peer question scores (aggregated)
        
    def fit(self, dim_data, question_data_agg):
        """
        dim_data: Index=Company, Cols=Dimensions (may include 'industry' column)
        question_data_agg: Index=Company, Cols=Questions (Scores) - Used to find peer strengths
        """
        self.dim_data_train = dim_data.copy().fillna(0)
        self.dim_data_train['total_maturity'] = self.dim_data_train[[c for c in self.dim_data_train.columns if c != 'industry']].mean(axis=1)
        
        # Store peer dimension averages for explanation generation (exclude industry and total_maturity)
        dim_cols = [c for c in self.dim_data_train.columns if c not in ['total_maturity', 'industry']]
        self.peer_dim_averages = self.dim_data_train[dim_cols].mean().to_dict()
        
        self.question_data_train = question_data_agg.copy().fillna(0)
        
        # Prepare features for KNN (exclude total_maturity and industry)
        X = self.scaler.fit_transform(self.dim_data_train[dim_cols])
        
        self.knn = NearestNeighbors(n_neighbors=15, metric='cosine')
        self.knn.fit(X)

    def _generate_explanation(self, theme, theme_out, dimension, source, company_dim_series, impact_score, lang="en"):
        """
        Generates a business-focused explanation for a roadmap recommendation.
        Format: Brief analysis (1 bullet) + Detailed recommendations (2 bullets)
        
        Args:
            theme: The tactical theme (e.g., "Staff Proficiency") used for logic matching
            theme_out: Localized theme for output reading
            dimension: The localized dimension name
            source: "Strategic Gap (Critical)" or "Growth Opportunity"
            company_dim_series: Current company dimension scores
            impact_score: The calculated impact score
            lang: Language parameter
        """
        # Get company's current score for this dimension
        # Note: mapping back to English dimension for score lookup if dimension is German
        dim_key = dimension
        if lang == 'de':
             dim_de_map_rev = {
                  "Strategie & Vision": "Strategy & Business Vision",
                  "Menschen & Kultur": "People & Culture",
                  "Datenkompetenz": "Data Readiness & Literacy",
                  "Anwendungsfälle & Geschäftswert": "Use Cases & Business Value",
                  "Prozesse & Skalierbarkeit": "Processes & Scaling",
                  "Governance & Compliance": "Governance & Compliance",
                  "Technologie & Infrastruktur": "Tech Infrastructure"
             }
             dim_key = dim_de_map_rev.get(dimension, dimension)
             
        company_score = company_dim_series.get(dim_key, 0)
        peer_avg = self.peer_dim_averages.get(dim_key, company_score)
        
        # Calculate gap
        gap_pct = 0
        if company_score > 0:
            gap_pct = ((peer_avg - company_score) / company_score) * 100
        
        # Theme-specific recommendations
        theme_actions = self._get_theme_specific_actions(theme, source, gap_pct, lang)
        
        # Generate analysis
        if source == "Strategic Gap (Critical)":
            if gap_pct > 10:
                if lang == 'de':
                    analysis = f"**Analyse**: Ihre Kompetenz bezüglich {theme_out} (Score: {company_score:.1f}) liegt {gap_pct:.0f}% unter dem Branchendurchschnitt ({peer_avg:.1f}) und stellt einen kritischen Engpass dar."
                else:
                    analysis = f"**Analysis**: Your {theme_out} capability (score: {company_score:.1f}) is {gap_pct:.0f}% below industry average ({peer_avg:.1f}), creating a critical bottleneck."
            else:
                if lang == 'de':
                     analysis = f"**Analyse**: Obwohl {theme_out} eine moderate Leistung zeigt (Score: {company_score:.1f}), wird dies als hochprioritäres handlungsfeld identifiziert."
                else:
                     analysis = f"**Analysis**: While {theme_out} shows moderate performance (score: {company_score:.1f}), strategic analysis identifies this as a high-impact priority."
        else:  # Growth Opportunity
            if gap_pct > 15:
                if lang == 'de':
                    analysis = f"**Analyse**: Top-Performer glänzen in {theme_out} (Vergleichswert: {peer_avg:.1f} vs. Ihr {company_score:.1f}), was eine Chance von {gap_pct:.0f}% bedeutet."
                else:
                    analysis = f"**Analysis**: Top performers excel in {theme_out} (peer average: {peer_avg:.1f} vs your {company_score:.1f}), representing a {gap_pct:.0f}% opportunity gap."
            else:
                if lang == 'de':
                     analysis = f"**Analyse**: Ihre Leistung in {theme_out} (Score: {company_score:.1f}) ist wettbewerbsfähig, aber gezielte Verbesserungen werden Ihren KI-Reifegrad differenzieren."
                else:
                     analysis = f"**Analysis**: Your {theme_out} performance (score: {company_score:.1f}) is competitive, but targeted improvements will differentiate your AI maturity."
        
        action1_label = "**Action 1:**" # Frontend regex strictly looks for 'Action'
        action2_label = "**Action 2:**"
        return f"{analysis}\n\n{action1_label} {theme_actions['action1']}\n\n{action2_label} {theme_actions['action2']}"
    
    def _get_theme_specific_actions(self, theme, source, gap_pct, lang="en"):
        """
        Generate theme-specific actionable recommendations.
        
        Args:
            theme: The tactical theme
            source: Strategic Gap or Growth Opportunity
            gap_pct: Gap percentage
            
        Returns:
            dict with action1 and action2
        """
        # Theme-specific action mapping
        theme_lower = theme.lower()
        
        # Default actions as fallback
        if source == "Strategic Gap (Critical)" and gap_pct > 10:
            action1 = f"Launch a focused {theme} improvement initiative with executive sponsorship and dedicated resources to close the performance gap."
            action2 = f"Implement monthly progress tracking with clear KPIs and accountability measures to ensure sustained improvement in {theme}."
        elif source == "Strategic Gap (Critical)":
            action1 = f"Conduct a comprehensive assessment of current {theme} practices and identify quick wins for immediate implementation."
            action2 = f"Develop a 90-day action plan with specific milestones to strengthen {theme} capabilities and build organizational momentum."
        elif gap_pct > 15:
            action1 = f"Benchmark {theme} practices against industry leaders and adopt proven frameworks to accelerate capability development."
            action2 = f"Consider strategic partnerships or external expertise in {theme} to fast-track implementation and achieve competitive parity within 6 months."
        else:
            action1 = f"Optimize existing {theme} processes through continuous improvement cycles and innovation initiatives."
            action2 = f"Establish knowledge-sharing programs and best practice documentation to maintain competitive advantage in {theme}."
        
        # Theme-specific customizations
        if 'staff' in theme_lower or 'proficiency' in theme_lower:
            action1 = "Design and deploy comprehensive AI literacy programs for all staff levels, including hands-on workshops and certification tracks."
            action2 = "Create internal AI champions network and mentorship programs to accelerate skill development and knowledge transfer across teams."
        
        elif 'leadership' in theme_lower or 'alignment' in theme_lower:
            action1 = "Conduct executive AI strategy workshops to align leadership vision, establish clear AI governance, and secure C-suite commitment."
            action2 = "Implement quarterly AI steering committee meetings with defined decision-making authority and resource allocation frameworks."
        
        elif 'data' in theme_lower and 'privacy' in theme_lower:
            action1 = "Establish comprehensive data governance framework with clear privacy policies, consent management, and compliance protocols."
            action2 = "Deploy privacy-by-design principles across all AI initiatives and conduct regular privacy impact assessments with legal review."
        
        elif 'data' in theme_lower or 'types' in theme_lower:
            action1 = "Audit current data infrastructure and implement data quality improvement programs with automated validation and cleansing pipelines."
            action2 = "Expand data collection capabilities to include diverse data types (structured, unstructured, real-time) with proper cataloging and metadata management."
        
        elif 'strategic' in theme_lower or 'priority' in theme_lower:
            action1 = "Define clear AI strategic priorities aligned with business objectives and establish a prioritization framework for AI initiatives."
            action2 = "Create a strategic AI roadmap with measurable outcomes and regular review cycles to ensure alignment with evolving business needs."
        
        elif 'standardization' in theme_lower or 'process' in theme_lower:
            action1 = "Develop and document standardized AI development processes, including MLOps practices, testing protocols, and deployment procedures."
            action2 = "Implement process automation tools and establish centers of excellence to ensure consistent quality and scalability across AI projects."
        
        elif 'governance' in theme_lower or 'compliance' in theme_lower:
            action1 = "Build robust AI governance structure with clear roles, responsibilities, and escalation paths for ethical and compliance issues."
            action2 = "Establish regular compliance audits, risk assessments, and policy updates to maintain regulatory alignment and ethical AI practices."
        
        elif 'infrastructure' in theme_lower or 'tech' in theme_lower:
            action1 = "Modernize technical infrastructure with cloud-native AI platforms, scalable compute resources, and MLOps tooling."
            action2 = "Implement infrastructure-as-code practices and establish DevOps pipelines to enable rapid experimentation and deployment."
        
        elif 'execution' in theme_lower or 'maturity' in theme_lower:
            action1 = "Strengthen project management capabilities with agile AI delivery frameworks and cross-functional team structures."
            action2 = "Establish success metrics, post-implementation reviews, and continuous improvement processes to enhance execution maturity."
        
        elif 'tooling' in theme_lower or 'stack' in theme_lower:
            action1 = "Evaluate and standardize AI tooling stack with enterprise-grade platforms for development, deployment, and monitoring."
            action2 = "Provide comprehensive training on selected tools and establish internal support structures for technical enablement."
        
        elif 'competitive' in theme_lower or 'ambition' in theme_lower:
            action1 = "Define competitive AI positioning strategy and identify differentiation opportunities through advanced AI capabilities."
            action2 = "Foster innovation culture with dedicated time for experimentation, hackathons, and recognition programs for AI-driven initiatives."
        
        return {'action1': action1, 'action2': action2}

    def get_peer_benchmark(self, company_dim_series, company_industry=None):
        """
        Calculates the average dimension scores of industry peers.
        If industry is provided, filters to same industry before averaging.
        Returns dict {dimension: score}.
        """
        if self.dim_data_train is None:
             return {}
        
        try:
            # Identify training columns (dimensions only)
            train_cols = [c for c in self.dim_data_train.columns if c not in ['total_maturity', 'industry']]
            
            # Filter by industry if provided and industry column exists
            if company_industry and 'industry' in self.dim_data_train.columns:
                industry_peers = self.dim_data_train[
                    self.dim_data_train['industry'] == company_industry
                ]
                
                # Fallback to global if industry sample is too small (< 5 companies)
                if len(industry_peers) < 5:
                    print(f"Industry '{company_industry}' has only {len(industry_peers)} companies. Using global benchmark.")
                    peers = self.dim_data_train
                else:
                    peers = industry_peers
                    print(f"Using industry-specific benchmark: {company_industry} ({len(peers)} companies)")
            else:
                # No industry filtering - use all peers
                peers = self.dim_data_train
                print(f"Using global benchmark ({len(peers)} companies)")
            
            # Calculate mean of peers for each dimension
            peer_means = peers[train_cols].mean()
            
            return peer_means.round(2).to_dict()
        except Exception as e:
            print(f"Peer Benchmark Calc Error: {e}")
            return {}

    def generate(self, company_id, company_dim_series, company_question_df, strategic_gaps, lang='en'):
        """
        Generates 3-Phase Roadmap.
        company_id: ID for reference (if needed for exclusionary logic, though we use vector lookup)
        company_dim_series: Current scores.
        company_question_df: Current question details (for "Growth Opps").
        strategic_gaps: Input from GapAnalyzer.
        lang: Language code ('en' or 'de').
        """
        
        # 1. Identify Peers (Strategy A: 15-30% better)
        current_total = company_dim_series.mean()
        X_in = self.scaler.transform(company_dim_series.values.reshape(1, -1))
        
        distances, indices = self.knn.kneighbors(X_in)
        peer_indices = indices[0]
        
        peers = self.dim_data_train.iloc[peer_indices]
        
        # Filter for "Next Level"
        next_level_peers = peers[
            (peers['total_maturity'] > current_total * 1.15) & 
            (peers['total_maturity'] <= current_total * 1.30)
        ]
        
        if next_level_peers.empty:
            # Fallback: Just better peers
            next_level_peers = peers[peers['total_maturity'] > current_total]
            
        # Get Peer Question Averages (if any peers found)
        peer_q_avg = None
        if not next_level_peers.empty:
            peer_ids = next_level_peers.index
            # Intersect with available question data
            valid_pids = [p for p in peer_ids if p in self.question_data_train.index]
            if valid_pids:
                peer_q_avg = self.question_data_train.loc[valid_pids].mean()

        # 2. Initialize Roadmap
        phase1_key = 'Phase 1: Foundation' if lang == 'en' else 'Phase 1: Fundament'
        phase2_key = 'Phase 2: Implementation' if lang == 'en' else 'Phase 2: Implementierung'
        phase3_key = 'Phase 3: Scale & Governance' if lang == 'en' else 'Phase 3: Skalierung & Governance'
        
        roadmap = {
            phase1_key: [],
            phase2_key: [],
            phase3_key: []
        }
        
        # Helps check for duplication (use English themes for dupes)
        added_themes = set()
        
        # 3. Add Mandatory Strategic Gaps
        for gap in strategic_gaps:
            # If gap has explicit theme/dim, map it
            d_name = gap.get('dimension_name')
            # If anomaly, it might have 'source_dim' or just title.
            if not d_name and 'source_dim' in gap:
                d_name = gap['source_dim']
            
            if not d_name: 
                 if ":" in gap['title']:
                     maybe_dim = gap['title'].split(":")[-1].split("vs")[0].strip()
                     d_name = maybe_dim
            
            # Map standard English dimension to Phase
            eng_phase = PHASE_MAPPING.get(d_name, 'Phase 1: Foundation')
            phase = phase1_key if 'Phase 1' in eng_phase else (phase2_key if 'Phase 2' in eng_phase else phase3_key)
            
            # Construct item
            item_theme = gap.get('tactical_theme', f"Fix {d_name} Gaps")
            item_theme_out = gap.get('tactical_theme_out', item_theme)
            
            if item_theme not in added_themes:
                explanation = self._generate_explanation(
                    theme=item_theme,
                    theme_out=item_theme_out,
                    dimension=gap.get('dimension_name_out', d_name),
                    source="Strategic Gap (Critical)",
                    company_dim_series=company_dim_series,
                    impact_score=gap['score'],
                    lang=lang
                )
                roadmap[phase].append({
                    "theme": item_theme_out,
                    "source": "Strategic Gap (Critical)", # Always keep English for frontend categorization logic
                    "impact_score": gap['score'],
                    "dimension": gap.get('dimension_name_out', d_name),
                    "explanation": explanation
                })
                added_themes.add(item_theme)

        # 4. Fill Empty Phases (Constraint: Every Phase must have content)
        # We need a candidate list of "Growth Opportunities" from the user's data
        # Prioritize by: Impact Score * (Peer Gap Bonus)
        
        candidates = []
        if not company_question_df.empty:
            for _, row in company_question_df.iterrows():
                theme = row.get('tactical_theme')
                theme_de = row.get('tactical_theme_de', theme)
                if theme in added_themes: continue
                
                qid = row.get('question_id')
                user_score = row.get('score_1to5', 1)
                
                # Base Impact
                w = row.get('question_weight', 0)
                base_impact = w * (5.0 - user_score)
                
                # Peer Bonus
                peer_bonus = 1.0
                if peer_q_avg is not None and qid in peer_q_avg:
                    peer_score = peer_q_avg[qid]
                    if peer_score > user_score + 0.5: # Significant peer advantage
                        peer_bonus = 1.5
                
                candidates.append({
                    "theme": theme,
                    "theme_out": theme if lang == 'en' else theme_de,
                    "dimension": row.get('dimension_name'),
                    "dimension_out": row.get('dimension_name') if lang == 'en' else row.get('dimension_name_de', row.get('dimension_name')),
                    "impact": base_impact * peer_bonus,
                    "final_score": base_impact * peer_bonus
                })
        
        # Sort candidates
        candidates.sort(key=lambda x: x['final_score'], reverse=True)
        
        # Fill logic — iterate over the localized phase keys
        phases = [phase1_key, phase2_key, phase3_key]
        en_phases = ['Phase 1: Foundation', 'Phase 2: Implementation', 'Phase 3: Scale & Governance']
        
        for phase, en_phase in zip(phases, en_phases):
            if not roadmap[phase]:
                # Find best candidate for this phase
                found = None
                for c in candidates:
                    c_phase = PHASE_MAPPING.get(c['dimension'], 'Phase 1: Foundation')
                    if c_phase == en_phase and c['theme'] not in added_themes:
                        found = c
                        break
                
                if found:
                    explanation = self._generate_explanation(
                        theme=found['theme'],
                        theme_out=found['theme_out'],
                        dimension=found['dimension_out'],
                        source="Growth Opportunity",
                        company_dim_series=company_dim_series,
                        impact_score=found['final_score'],
                        lang=lang
                    )
                    roadmap[phase].append({
                        "theme": found['theme_out'],
                        "source": "Growth Opportunity", # Keep English for frontend categorization
                        "impact_score": found['final_score'],
                        "dimension": found['dimension_out'],
                        "explanation": explanation
                    })
                    added_themes.add(found['theme'])
                else:
                    # Fallback if no specific candidate fits the phase (rare, but possible if data is sparse)
                    # Force a generic item or pick next best regardless of mapping?
                    # Let's pick the next best available candidate and force it (Strategic necessity)
                    for c in candidates:
                        if c['theme'] not in added_themes:
                            explanation = self._generate_explanation(
                                theme=c['theme'],
                                theme_out=c['theme_out'],
                                dimension=c['dimension_out'],
                                source="Growth Opportunity",
                                company_dim_series=company_dim_series,
                                impact_score=c['final_score'],
                                lang=lang
                            )
                            roadmap[phase].append({
                                "theme": c['theme_out'],
                                "source": "Accelerated Growth", # Keep English for frontend categorization
                                "impact_score": c['final_score'],
                                "dimension": c['dimension_out'],
                                "explanation": explanation
                            })
                            added_themes.add(c['theme'])
                            break

        return roadmap

    def synthesize_briefing(self, roadmap, lang="en"):
        """
        Synthesizes the textual 3-phase roadmap.
        """
        phase1_key = 'Phase 1: Foundation' if lang == 'en' else 'Phase 1: Fundament'
        phase2_key = 'Phase 2: Implementation' if lang == 'en' else 'Phase 2: Implementierung'
        phase3_key = 'Phase 3: Scale & Governance' if lang == 'en' else 'Phase 3: Skalierung & Governance'
        
        p1 = [i['theme'] for i in roadmap[phase1_key]]
        p2 = [i['theme'] for i in roadmap[phase2_key]]
        p3 = [i['theme'] for i in roadmap[phase3_key]]
        
        p1_text = ", ".join(p1) if p1 else ("Foundation" if lang == 'en' else "Fundament")
        p2_text = ", ".join(p2) if p2 else ("Implementation" if lang == 'en' else "Implementierung")
        p3_text = ", ".join(p3) if p3 else ("Optimization" if lang == 'en' else "Optimierung")
        
        if lang == 'de':
             briefing = f"""
### 🗺️ AI-Compass: Ihre 3-Phasen Transformations-Roadmap

Um eine nachhaltige und ROI-starke Reise in die KI zu gewährleisten, empfehlen wir einen phasenweisen Ansatz, der die grundlegende Stabilität vor komplexer technischer Skalierung priorisiert.

**Phase 1: Fundament legen**
Ihre oberste Priorität ist **{p1_text}**. Mit dem Fokus auf diesen Bereich stellen wir sicher, dass Ihre organisatorischen Daten und Ihre Kultur robust genug sind, um Automatisierung ohne Reibungsverluste zu unterstützen.

**Phase 2: Gezielte Implementierung**
Sobald das Fundament gesichert ist, gehen wir über zu **{p2_text}**. Diese Bereiche wurden als Ihre stärksten Hebel identifiziert, um die Lücke zwischen Ihrem aktuellen Status und der Leistung von Branchenführern direkt zu schließen.

**Phase 3: Strategische Skalierung**
Die letzte Phase konzentriert sich auf **{p3_text}**. Hier vollziehen wir den Übergang von isolierten Anwendungsfällen zu einem KI-gesteuerten Betriebsmodell und gewährleisten langfristige Resilienz und Governance.

**Erfolgsmetrik**: Die Umsetzung dieser Roadmap wird Ihre Gesamtreife vom aktuellen Niveau in die oberen 20 % Ihrer Branchenvergleichsgruppe heben.
"""
        else:
             briefing = f"""
### 🗺️ AI-Compass: Your 3-Phase Transformation Roadmap

To ensure a sustainable and high-ROI journey into AI, we recommend a phased approach that prioritizes foundational stability before complex technical scaling.

**Phase 1: Laying the Foundation**
Your first priority is **{p1_text}**. By focusing here, we ensure that your organizational data and culture are robust enough to support automation without creating friction.

**Phase 2: Targeted Implementation**
Once the foundation is secure, we move to **{p2_text}**. These areas have been identified as your highest-leverage opportunities, directly bridging the gap between your current status and the performance of industry leaders.

**Phase 3: Strategic Scaling**
The final phase focuses on **{p3_text}**. This is where we transition from single use-cases to an AI-driven operational model, ensuring long-term resilience and governance.

**Success Metric**: Completion of this roadmap will move your total maturity from its current level into the top 20% of your industry peer group.
"""
        return briefing

    def save_model(self, path_prefix):
        state = {
            'dim_data_train': self.dim_data_train,
            'question_data_train': self.question_data_train,
            'peer_dim_averages': self.peer_dim_averages,
            'knn': self.knn,
            'scaler': self.scaler
        }
        with open(f"{path_prefix}_roadmap_gen.pkl", 'wb') as f:
            pickle.dump(state, f)

    def load_model(self, path_prefix):
        with open(f"{path_prefix}_roadmap_gen.pkl", 'rb') as f:
            state = pickle.load(f)
            self.dim_data_train = state['dim_data_train']
            self.question_data_train = state['question_data_train']
            self.peer_dim_averages = state.get('peer_dim_averages', {})
            self.knn = state['knn']
            self.scaler = state['scaler']
