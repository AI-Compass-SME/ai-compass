def get_cluster_content(cluster_name: str) -> dict:
    """
    Returns static content for clusters.
    """
    content = {
        "Passive": {
            "description": "AI is non-existent or ad-hoc. Awareness is low, and no formal strategy exists.",
            "characteristics": [
                "No dedicated AI budget or team",
                "Skepticism or lack of awareness among leadership",
                "Data is siloed and often inaccessible"
            ],
            "roadmap": [
                {"step": "Education", "description": "Conduct executive workshops on AI potential."},
                {"step": "Data Audit", "description": "Map existing data sources and quality."},
                {"step": "Pilot", "description": "Identify one high-value, low-risk use case."}
            ]
        },
        "Reactive": {
            "description": "AI is used experimentally in isolated pockets. Focus is on efficiency, not strategy.",
            "characteristics": [
                "Ad-hoc experiments by individual teams",
                "Focus on cost-cutting or efficiency",
                "Lack of standardized tools or governance"
            ],
            "roadmap": [
                {"step": "Standardize", "description": "Establish basic tool guidelines."},
                {"step": "Strategy", "description": "Define a coherent AI vision."},
                {"step": "Governance", "description": "Create a preliminary AI risk framework."}
            ]
        },
        "Active": {
            "description": "AI strategy is defined and pilots are scaling. Governance is emerging.",
            "characteristics": [
                "Formal AI strategy in place",
                "Dedicated budget and resources",
                "Governance framework established"
            ],
            "roadmap": [
                {"step": "Scale High-Value", "description": "Move successful pilots to production."},
                {"step": "Talent", "description": "Upskill internal teams or hire specialists."},
                {"step": "Platform", "description": "Invest in scalable MLOps infrastructure."}
            ]
        },
        "Strategic": {
            "description": "AI is integrated into core business processes. Focus is on differentiation and value.",
            "characteristics": [
                "AI drives key product differentiators",
                "Cross-functional AI teams",
                "Automated MLOps pipelines"
            ],
            "roadmap": [
                {"step": "Innovation", "description": "Explore generative AI for new revenue streams."},
                {"step": "Culture", "description": "Democratize AI access across the organization."},
                {"step": "Ecosystem", "description": "Partner with AI startups or research labs."}
            ]
        },
        "Transformative": {
            "description": "AI is the core of the business model. Continuous innovation and market leadership.",
            "characteristics": [
                "AI-first business model",
                "Self-optimizing systems",
                "Industry leadership in AI ethics"
            ],
            "roadmap": [
                {"step": "Disrupt", "description": "Reinvent industry standards with AI."},
                {"step": "Ethical AI", "description": "Lead industry in responsible AI practices."},
                {"step": "Moonshots", "description": "Invest in R&D for next-gen AI capabilities."}
            ]
        }
    }
    
    # Normalize name (remove numbers if present e.g. "1 - Passive")
    name_clean = cluster_name.split('-')[-1].strip()
    return content.get(name_clean, {
        "description": "Analyzing cluster characteristics...",
        "characteristics": [],
        "roadmap": []
    })
