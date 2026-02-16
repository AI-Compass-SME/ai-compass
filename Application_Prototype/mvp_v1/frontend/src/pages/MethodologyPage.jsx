import React, { useEffect } from 'react';
import { Navigation } from '../components/Navigation';
import { PageBackground } from '@/components/ui/PageBackground';
import { PageHeader } from '../components/PageHeader';
import { Footer } from '../components/Footer';
import { ShieldCheck, Database, Cpu, BarChart3, Binary, Network, Lock, Fingerprint } from 'lucide-react';

const TechCard = ({ icon: Icon, title, subtitle, children }) => (
    <div className="bg-white p-6 rounded-lg border border-gray-100 shadow-sm hover:shadow-md transition-shadow">
        <div className="flex items-start gap-4">
            <div className="p-3 bg-blue-50 text-blue-600 rounded-lg flex-shrink-0">
                <Icon className="w-6 h-6" />
            </div>
            <div>
                <h3 className="font-bold text-gray-900 text-lg mb-1">{title}</h3>
                <p className="text-xs font-mono text-blue-600 uppercase tracking-widest mb-3">{subtitle}</p>
                <div className="text-sm text-gray-600 leading-relaxed space-y-2">
                    {children}
                </div>
            </div>
        </div>
    </div>
);

export default function MethodologyPage() {
    useEffect(() => {
        document.title = "Methodology | AI Compass";
    }, []);

    return (
        <div className="min-h-screen flex flex-col relative overflow-hidden bg-slate-50">
            <PageBackground />
            <Navigation />

            <main className="flex-grow w-full max-w-[80rem] mx-auto px-6 pt-28 pb-16 relative z-10">

                {/* Header Section */}
                {/* Header Section */}
                <PageHeader
                    title="Technical Methodology & AI Architecture"
                    subtitle="DOCUMENTATION FOR TECHNICAL STAKEHOLDERS"
                />

                {/* Main Grid */}
                <div className="grid md:grid-cols-2 gap-6">

                    {/* 1. Data Normalization */}
                    <TechCard
                        icon={Binary}
                        title="Data Standardization"
                        subtitle="Preprocessing Loop"
                    >
                        <p>
                            Raw assessment data is ingested via our ETL pipeline and normalized using <strong>Z-Score Standardization</strong> (StandardScaler).
                        </p>
                        <p>
                            This transforms all dimension scores into a standard normal distribution (μ=0, σ=1), ensuring that outliers don't skew the clustering distance metrics and allowing for fair comparison across diverse industries.
                        </p>
                    </TechCard>

                    {/* 2. Unsupervised Learning */}
                    <TechCard
                        icon={Network}
                        title="Archetype Clustering"
                        subtitle="Unsupervised Learning"
                    >
                        <p>
                            We utilize <strong>K-Means Clustering</strong> (k=5) to categorize organizations into distinct maturity archetypes.
                        </p>
                        <p>
                            The model is trained on our proprietary dataset of 500+ profiles. Your organization is assigned to a cluster based on the Euclidean distance to the nearest centroid, providing an objective classification from "Traditionalist" to "AI-Driven Leader".
                        </p>
                    </TechCard>

                    {/* 3. Predictive Roadmapping */}
                    <TechCard
                        icon={Cpu}
                        title="Predictive Roadmapping"
                        subtitle="k-Nearest Neighbors (k-NN)"
                    >
                        <p>
                            Our recommendation engine uses a <strong>k-Nearest Neighbors</strong> algorithm with <strong>Cosine Similarity</strong> to identify your "Next-Level Peers".
                        </p>
                        <p>
                            By locating organizations that are statistically similar to you but 15-30% more mature, we reverse-engineer their capabilities to generate a high-probability roadmap for your specific growth path.
                        </p>
                    </TechCard>

                    {/* 4. Anomaly Detection */}
                    <TechCard
                        icon={ShieldCheck}
                        title="Strategic Risk Analysis"
                        subtitle="Statistical Anomaly Detection"
                    >
                        <p>
                            The <strong>Strategic Gap Analyzer</strong> scans for structural imbalances across 7 dimensions using a Z-Score threshold (&gt; 1.5σ).
                        </p>
                        <p>
                            We explicitly detect decoupling between "Strategy" and "Execution" (e.g., high Tech score but low People score), flagging these as critical risks that could lead to project failure or "shelf-ware".
                        </p>
                    </TechCard>

                </div>

                {/* Technical Stack Footer */}
                <div className="mt-12 pt-8 border-t border-gray-200">
                    <div className="flex flex-wrap items-center justify-between gap-6">
                        <div>
                            <h3 className="text-sm font-bold text-gray-900 uppercase tracking-wide mb-1">
                                Core Technology Stack
                            </h3>
                            <p className="text-xs text-gray-500">
                                Built for security, scalability, and interpretability.
                            </p>
                        </div>

                        <div className="flex gap-3">
                            <span className="px-3 py-1 bg-gray-100 text-gray-600 text-xs font-mono rounded">Python 3.11</span>
                            <span className="px-3 py-1 bg-gray-100 text-gray-600 text-xs font-mono rounded">Scikit-Learn</span>
                            <span className="px-3 py-1 bg-gray-100 text-gray-600 text-xs font-mono rounded">Pandas / NumPy</span>
                            <span className="px-3 py-1 bg-gray-100 text-gray-600 text-xs font-mono rounded">FastAPI</span>
                        </div>
                    </div>
                </div>

                <div className="mt-8 bg-blue-50 border border-blue-100 rounded-lg p-4 flex items-start gap-3">
                    <Lock className="w-5 h-5 text-blue-600 mt-0.5" />
                    <div>
                        <h4 className="text-sm font-bold text-blue-900">Data Privacy & Security</h4>
                        <p className="text-xs text-blue-800 mt-1">
                            All assessment data is processed in-memory for inference. We strictly adhere to GDPR principles and do not use customer data for training public LLMs. Your unique IP remains yours.
                        </p>
                    </div>
                </div>

            </main>

            <Footer />
        </div>
    );
}
