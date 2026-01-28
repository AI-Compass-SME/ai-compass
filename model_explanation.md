# AI-Compass: ML v5 Intelligence Engine

This document explains the logic behind the **ML v5** system, the core intelligence engine of AI-Compass. It combines the rigorous **Hybrid Clustering** of previous versions with new **Gap Analysis** and **Predictive Roadmapping** capabilities.

## 1. System Components
The v5 engine consists of three specialized components working in parallel:

```text
┌─────────────────────────────────────────────────────────────┐
│                       ML v5 System                          │
│                                                             │
│  ┌────────────────┐   ┌─────────────────┐   ┌─────────────┐ │
│  │ Cluster Engine │   │  Strategic Gap  │   │ Roadmap Gen │ │
│  │    (K-Means)   │   │ Analyzer (Rule) │   │    (KNN)    │ │
│  └───────┬────────┘   └────────┬────────┘   └──────┬──────┘ │
│          │                     │                   │        │
│          ▼                     ▼                   ▼        │
│    [Segmentation]      [Risk Detection]    [Transformation] │
└─────────────────────────────────────────────────────────────┘
```

## 2. Cluster Engine (Segmentation & Bias Control)
**Logic**: Hybrid Unsupervised-Supervised Clustering
*   **Algorithm**: K-Means (k=5) + PCA (Visualization).
*   **Why it works**: Finds natural "centers of gravity" in the data.

### Important: Zero Bias Design
> *"Do the cluster names (e.g., 'Leader') affect the K-Means outcome?"*

**No.** The clustering process is strictly unsupervised. The K-Means algorithm only sees the **raw numerical scores** to determine how companies should be grouped.

The labels ("Traditionalist" -> "Leader") are applying using **Rank-Based Profile Mapping** only *after* the clusters are defined. This ensures groupings are scientifically objective and not biased by pre-conceived categories.

### Rank-Based Labeling Logic
| Step | Logic | Impact |
| :--- | :--- | :--- |
| **1. Score Calculation** | Mean of all 7 dimension scores for each cluster centroid. | Converts complex data into a single 'Maturity' value. |
| **2. Global Ranking** | The 5 clusters are ranked from 1 (lowest maturity) to 5 (highest maturity). | Distinguishes relative performance levels. |
| **3. Profile Assignment** | The 5 archetypes are assigned sequentially to the ranked clusters. | **Guarantees all 5 levels are represented dynamically.** |

## 3. Why Use ML instead of Rules?
The "Hybrid ML" approach offers distinct advantages over simple rule-based scoring:

1.  **Multi-Dimensional Density (Nuance)**: A simple rule average obscures details. ML looks at the *shape* of the profile. It can distinguish a "Strong Strategy/Weak Tech" company from a "Weak Strategy/Strong Tech" one even if their averages are identical.
2.  **Dynamic Benchmarking (The Peer Effect)**: In a static system, if the industry improves, everyone becomes a "Leader". In our ML system, benchmarks shift *with the data*. "Leader" status is always relative to the top 20% of the *current* real-world dataset.
3.  **Natural Sub-Groups**: ML finds where users actually congregate (e.g., a "Stuck in Pilot" trap) rather than forcing them into arbitrary buckets.

## 4. Strategic Gap Analyzer (Risk Detection)
**Logic**: Statistical Anomaly Detection
Uses Z-Scores to detect "Structural Imbalances" where one dimension significantly lags behind others (e.g., High Tech Investment but Low Staff Proficiency). This identifies hidden risks that simple averages miss.

## 5. Roadmap Generator (Transformation)
**Logic**: K-Nearest Neighbors (KNN)
Finds "Next-Level Peers" (companies chemically similar to you but 15-30% more mature) and recommends the specific actions *they* took to succeed, creating a roadmap based on proven paths rather than theoretical templates.

