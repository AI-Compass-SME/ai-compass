import React, { useEffect, useState } from 'react';
import { PageBackground } from '@/components/ui/PageBackground';
import { useParams, Link } from 'react-router-dom';
import { api } from '../lib/api';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import { Navigation } from '../components/Navigation';
import { Footer } from '../components/Footer';
import { ResultsHero } from '../components/results/ResultsHero';
import { ClusterProfile } from '../components/results/ClusterProfile';
import { MaturityProfile } from '../components/results/MaturityProfile';
import { ExecutiveBriefing } from '../components/results/ExecutiveBriefing';
import { Roadmap } from '../components/results/Roadmap';
import { ExpertConsultation } from '../components/results/ExpertConsultation';
import { DownloadCTA } from '../components/results/DownloadCTA';

export default function ResultsPage() {
    const { responseId } = useParams();
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        async function fetchResults() {
            try {
                const result = await api.getResults(responseId);
                setData(result);
            } catch (err) {
                console.error("Failed to load results", err);
                setError(err.message || "Failed to generate analysis.");
                toast.error("Analysis failed.");
            } finally {
                setLoading(false);
            }
        }
        fetchResults();
    }, [responseId]);

    // Set page title
    useEffect(() => {
        document.title = "AI Compass: Executive Results";
    }, []);

    if (loading) {
        return (
            <div className="flex flex-col items-center justify-center min-h-screen relative overflow-hidden">
                <PageBackground />
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mb-4 z-10"></div>
                <h2 className="text-xl font-semibold text-slate-800 z-10">Finalizing your strategic AI roadmap...</h2>
                <p className="text-slate-600 z-10">Verifying your industry benchmarks</p>
            </div>
        );
    }

    if (error || !data) {
        return (
            <div className="flex flex-col items-center justify-center min-h-screen p-6 relative overflow-hidden">
                <PageBackground />
                <Card className="w-full max-w-md shadow-xl border-red-100 z-10 glass">
                    <CardHeader className="text-center">
                        <CardTitle className="text-red-600">Analysis Error</CardTitle>
                        <CardDescription>{error || "No data available"}</CardDescription>
                    </CardHeader>
                    <CardContent className="flex justify-center">
                        <Button asChild variant="outline">
                            <Link to="/">Return Home</Link>
                        </Button>
                    </CardContent>
                </Card>
            </div>
        );
    }

    return (
        <div className="min-h-screen flex flex-col font-sans relative">
            <PageBackground />
            <Navigation />

            <main className="flex-grow w-full max-w-[80rem] mx-auto px-4 sm:px-6 pt-24 pb-12 space-y-8 md:space-y-12 z-10 relative">
                <ResultsHero data={data} responseId={responseId} />
                <ClusterProfile data={data} />
                <MaturityProfile data={data} />
                <ExecutiveBriefing data={data} />
                <Roadmap data={data} />
                <div className="space-y-5 md:space-y-7">
                    <ExpertConsultation />
                    <DownloadCTA responseId={responseId} />
                </div>


            </main>

            <Footer />
        </div>
    );
}
