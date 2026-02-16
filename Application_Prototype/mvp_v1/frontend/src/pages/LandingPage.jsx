import React, { useEffect, useState } from 'react';
import { api } from '../lib/api';
import { useNavigate } from 'react-router-dom';
import { initializeVisitorSession } from '../lib/assessment';
import { toast } from "sonner";
import { HeroSection } from '@/components/landing/HeroSection';
import { ValueProposition } from '@/components/landing/ValueProposition';
import { ProcessSection } from '@/components/landing/ProcessSection';
import { OutcomePreview } from '@/components/landing/OutcomePreview';
import { CTASection } from '@/components/landing/CTASection';
import { Footer } from '@/components/Footer';
import { Navigation } from '@/components/Navigation';
import { PageBackground } from '@/components/ui/PageBackground';

export default function LandingPage() {
    const navigate = useNavigate();
    const [isStarting, setIsStarting] = useState(false);

    // Background prefetch of questionnaire data
    useEffect(() => {
        const prefetchData = async () => {
            try {
                if (!sessionStorage.getItem('cached_questionnaire_data')) {
                    console.log("LANDING: Starting background prefetch of questionnaire...");
                    const data = await api.getQuestionnaire();
                    if (data) {
                        try {
                            const stringified = JSON.stringify(data);
                            sessionStorage.setItem('cached_questionnaire_data', stringified);
                            console.log(`LANDING: Prefetch complete. Cached ${stringified.length} bytes.`);
                        } catch (e) {
                            console.error("LANDING: Failed to cache data", e);
                        }
                    }
                } else {
                    console.log("LANDING: Data already in cache.");
                }
            } catch (error) {
                console.warn("LANDING: Prefetch failed", error);
            }
        };
        prefetchData();
    }, []);

    // Set page title
    useEffect(() => {
        document.title = "AI Compass";
    }, []);

    // Function to handle start
    const handleStartAssessment = async () => {
        try {
            setIsStarting(true);
            const session = await initializeVisitorSession();
            toast.success("Assessment started!");
            navigate(`/assessment/${session.responseId}`);
        } catch (error) {
            toast.error("Failed to start assessment. Please try again.");
            console.error(error);
            setIsStarting(false);
        }
    };

    return (
        <div className="min-h-screen flex flex-col font-sans relative overflow-x-hidden">
            <PageBackground />
            <Navigation />
            <main className="flex-grow">
                <HeroSection onStart={handleStartAssessment} isStarting={isStarting} />
                <ValueProposition />
                <ProcessSection />
                <OutcomePreview />
                <CTASection onStart={handleStartAssessment} isStarting={isStarting} />
            </main>
            <Footer />
        </div>
    );
}
