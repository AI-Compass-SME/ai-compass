import React, { useEffect } from 'react';
import { api } from '../lib/api';
import { HeroSection } from '@/components/landing/HeroSection';
import { ValueProposition } from '@/components/landing/ValueProposition';
import { ProcessSection } from '@/components/landing/ProcessSection';
import { OutcomePreview } from '@/components/landing/OutcomePreview';
import { CTASection } from '@/components/landing/CTASection';
import { Footer } from '@/components/Footer';
import { Navigation } from '@/components/Navigation';

import { PageBackground } from '@/components/ui/PageBackground';

export default function LandingPage() {
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

    // Navigation is fixed at the top, content starts below
    return (
        <div className="min-h-screen flex flex-col font-sans relative overflow-x-hidden">
            <PageBackground />
            <Navigation />
            <main className="flex-grow">
                <HeroSection />
                <ValueProposition />
                <ProcessSection />
                <OutcomePreview />
                <CTASection />
            </main>
            <Footer />
        </div>
    );
}
