
# Risk Pairs for Z-Score Analysis
RISK_PAIRS = [
    ('Tech Infrastructure', 'People & Culture'),
    ('Tech Infrastructure', 'Strategy & Business Vision'),
    ('Data Readiness & Literacy', 'Use Cases & Business Value'),
    ('Processes & Scaling', 'Governance & Compliance')
]

# Phase Mapping for Roadmap
PHASE_MAPPING = {
    'Strategy & Business Vision': 'Phase 1: Foundation',
    'Data Readiness & Literacy': 'Phase 1: Foundation',
    'People & Culture': 'Phase 1: Foundation',
    'Tech Infrastructure': 'Phase 2: Implementation',
    'Use Cases & Business Value': 'Phase 2: Implementation',
    'Processes & Scaling': 'Phase 3: Scale & Governance',
    'Governance & Compliance': 'Phase 3: Scale & Governance'
}

def generate_narrative_template(findings, benchmarks, company_scores, lang="en"):
    """
    Generates the Executive Briefing narrative based on findings.
    """
    if lang == "de":
        header = f"### 🎖️ AI-Compass Strategisches Briefing"
        narrative = f"{header}\n\n"
        narrative += "Unsere Analyse Ihres aktuellen KI-Reifegrads identifiziert zwei wesentliche strukturelle Risiken, die sofortige Aufmerksamkeit des Managements erfordern.\n\n"
        
        if len(findings) > 0:
            f1 = findings[0]
            narrative += f"Erstens haben wir **{f1['title']}** als Lücke identifiziert. {f1['context']} Dies deutet darauf hin, dass Ihre aktuelle organisatorische Entwicklung 'strategische Schulden' verursacht – wo technische Fähigkeiten der Führungsvision voraus sind oder umgekehrt.\n\n"
            
        if len(findings) > 1:
            f2 = findings[1]
            narrative += f"Zweitens deutet **{f2['title']}** auf eine kritische Lücke in Ihrer grundlegenden Bereitschaft hin. Derzeit wirkt diese Reife (Impact-Score {f2['score']:.1f}) als erheblicher Engpass. Die Behebung dieses spezifischen Bereichs wird einen höheren ROI für bestehende und zukünftige KI-Anwendungsfälle erschließen.\n\n"
            
        narrative += "**Strategisches Fazit**: Ihr Profil zeigt hohes Potenzial, ist aber derzeit entkoppelt. Eine Priorisierung dieser beiden Bereiche in den nächsten 3 Monaten wird Ihre KI-Initiativen von der experimentellen Phase zur Skalierbarkeit führen."
    else:
        header = f"### 🎖️ AI-Compass Strategic Briefing"
        
        narrative = f"{header}\n\n"
        narrative += "Our analysis of your current AI maturity profile identifies two primary structural risks that require immediate executive attention.\n\n"
        
        if len(findings) > 0:
            f1 = findings[0]
            narrative += f"Firstly, we have identified a **{f1['title']}**. {f1['context']} This suggests that your current organizational trajectory may be creating 'Strategic Debt'—where technical capabilities outpace leadership alignment or vice versa.\n\n"
            
        if len(findings) > 1:
            f2 = findings[1]
            narrative += f"Secondly, the **{f2['title']}** indicates a critical gap in your foundational readiness. Currently, this maturity level ({f2['score']:.1f} impact score) acts as a significant bottleneck. Addressing this specific area will unlock higher ROI for your existing and future AI use cases.\n\n"
            
        narrative += "**Strategic Verdict**: Your profile shows high potential but is currently decoupled. Prioritizing these two areas over the next 3 months will transform your AI initiatives from experimental to scalable."
        
    return narrative
