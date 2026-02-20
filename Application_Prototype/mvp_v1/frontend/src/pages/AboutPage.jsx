import React, { useEffect } from 'react';
import { Navigation } from '../components/Navigation';
import { PageBackground } from '@/components/ui/PageBackground';
import { PageHeader } from '../components/PageHeader';
import { Footer } from '../components/Footer';

// Team Member Component for cleaner code
function TeamMember({ name, role, description, linkedInUrl, imageUrl }) {
    return (
        <div className="flex flex-col gap-4">
            <div className="flex items-center gap-4">
                <div className="w-20 h-20 bg-gray-200 rounded-full flex-shrink-0 overflow-hidden relative group shadow-sm border border-gray-100">
                    {imageUrl ? (
                        <img
                            src={imageUrl}
                            alt={name}
                            className="w-full h-full object-cover"
                            onError={(e) => {
                                e.target.onerror = null;
                                e.target.style.display = 'none'; // Fallback to icon if image fails
                                e.target.nextSibling.style.display = 'flex';
                            }}
                        />
                    ) : null}

                    {/* Fallback Icon (shown if no image or image fails) */}
                    <div className="w-full h-full flex items-center justify-center bg-gray-100 text-gray-400 absolute top-0 left-0" style={{ display: imageUrl ? 'none' : 'flex' }}>
                        <svg className="w-8 h-8" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M24 20.993V24H0v-2.996A14.977 14.977 0 0112.004 15c4.904 0 9.26 2.354 11.996 5.993zM16.002 8.999a4 4 0 11-8 0 4 4 0 018 0z" />
                        </svg>
                    </div>
                </div>

                <div>
                    <h3 className="text-xl font-bold text-gray-900">{name}</h3>
                    <p className="text-sm font-medium text-gray-500 uppercase tracking-wide mb-2">{role}</p>
                    <div className="flex gap-4 items-center flex-wrap">
                        {linkedInUrl && (
                            <a
                                href={linkedInUrl}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="inline-flex items-center gap-1.5 text-xs font-semibold text-blue-600 hover:text-blue-700 transition-colors"
                            >
                                <svg className="w-3.5 h-3.5 flex-shrink-0" fill="currentColor" viewBox="0 0 24 24"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z" /></svg>
                                LinkedIn
                            </a>
                        )}
                        {portfolioUrl && (
                            <a
                                href={portfolioUrl}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="inline-flex items-center gap-1.5 text-xs font-semibold text-emerald-600 hover:text-emerald-700 transition-colors"
                            >
                                <svg className="w-3.5 h-3.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
                                </svg>
                                Personal Website
                            </a>
                        )}
                    </div>
                </div>
            </div>

            <div className="pl-1">
                <p className="text-base text-gray-600 mb-3 leading-relaxed">
                    {description}
                </p>
            </div>
        </div>
    );
}

export default function AboutPage() {
    useEffect(() => {
        document.title = "About Us | AI Compass";
    }, []);

    return (
        <div className="min-h-screen flex flex-col relative overflow-hidden bg-slate-50">
            <PageBackground />
            <Navigation />

            <main className="flex-grow w-full max-w-[80rem] mx-auto px-6 pt-28 pb-16 relative z-10">

                <PageHeader
                    title="About Us"
                    subtitle="TEAM & MISSION"
                />

                <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-8 md:p-12">
                    <div className="grid md:grid-cols-2 gap-x-12 gap-y-6 text-sm text-gray-700">
                        {/* Row 1: Accountability Intro */}
                        <section className="md:col-span-2 mb-8">
                            <h2 className="text-sm font-bold text-gray-900 mb-2 uppercase tracking-wide text-xs">Accountability Behind the Algorithm</h2>
                            <p className="leading-relaxed text-lg font-medium text-gray-800">
                                The AI Compass isn't a "Black Box." It is a tool built by experts to bring transparency and structure to AI transformation.
                            </p>
                        </section>

                        {/* Row 2: Team (Full Width, Horizontal Cards) */}
                        <section className="md:col-span-2 mt-4">
                            <h2 className="text-sm font-bold text-gray-900 mb-6 uppercase tracking-wide text-xs">Your Partners in AI Transformation</h2>
                            <div className="grid md:grid-cols-2 gap-12">
                                {/* Role: Christian Miething */}
                                <TeamMember
                                    name="Christian Miething"
                                    role="Product Owner & Strategist"
                                    description={
                                        <span className="space-y-4 block">
                                            <span className="block">
                                                <strong className="block text-gray-900 mb-1">Leadership meets Strategy and Execution</strong>
                                                With over 14 years of leadership experience, I have built a career on a proven track record of fostering strong professional relationships, leading complex projects, and driving sustainable business growth. My expertise sits at the intersection of strategic consulting, project management, and high-level client relations.
                                            </span>
                                            <span className="block">
                                                I am deeply passionate about digital transformation and the evolution of Artificial Intelligence. Driven by a desire to create long-term value, I thrive on collaborating with diverse teams to solve problems through effective communication and strategic insight.
                                            </span>
                                            <span className="block">
                                                <strong className="block text-gray-900 mb-1 mt-2">The Architect of the AI Compass</strong>
                                                I conceived the AI Compass because I recognized a critical gap in the market. While AI is evolving rapidly, its relevance to the German Mittelstand is often lost in technical complexity.
                                            </span>
                                            <span className="block">
                                                As the Product Owner, I see my role as a bridge-builder: translating complex AI capabilities into actionable business logic. My goal is to serve businesses with the clarity and precision needed to master the AI landscape, ensuring every technological milestone is anchored in measurable, ROI-driven business value.
                                            </span>
                                        </span>
                                    }
                                    linkedInUrl="https://www.linkedin.com/in/christian-miething-ai-strategy-execution/"
                                    imageUrl="/team/profile_image_cm.jpg"
                                />

                                {/* Role: Hamza Latif */}
                                <TeamMember
                                    name="Hamza Latif"
                                    role="Lead Data Scientist & ML Engineer"
                                    description={
                                        <span className="space-y-4 block">
                                            <span className="block">
                                                <strong className="block text-gray-900 mb-1">Architecture meets Intelligence and Explainability</strong>
                                                With over 8 years of experience across enterprise systems and AI-driven product development, I have built my career at the intersection of structured engineering, statistical modeling, and scalable SaaS architecture. My expertise lies in transforming complex business challenges into robust data systems that are transparent, measurable, and production-ready.
                                            </span>
                                            <span className="block">
                                                I approach the evolution of AI not as abstract experimentation, but as a disciplined engineering practice. My work focuses on building ML systems that balance predictive intelligence with deterministic logic, ensuring every algorithmic output is grounded in statistical rigor.
                                            </span>
                                            <span className="block">
                                                <strong className="block text-gray-900 mb-1 mt-2">The Intelligence Architect Behind AI Compass</strong>
                                                I built the ML v5 engine powering AI Compass. Unlike generic scoring tools, I engineered a system combining deterministic models with advanced clustering to create structured, explainable roadmaps.
                                            </span>
                                            <span className="block">
                                                My goal is simple: building AI systems that leaders can trust. By aligning statistical modeling with clean architecture, I transform machine learning from a black-box into a strategic instrument for measurable progress, ensuring that every insight is backed by robust performance and long-term engineering reliability.
                                            </span>
                                        </span>
                                    }
                                    linkedInUrl="https://www.linkedin.com/in/mhlatif207/"
                                    imageUrl="/team/profile_image_mhl.jpg"
                                />
                            </div>
                        </section>

                        <section className="md:col-span-2 bg-purple-50 p-4 rounded-lg border border-purple-100 mt-2">
                            <h2 className="text-xs font-bold text-purple-900 mb-1 uppercase tracking-wide">
                                Location & Roots
                            </h2>
                            <p className="text-xs text-purple-800 leading-relaxed">
                                Based in the heart of Berlin's tech ecosystem.<br />
                                Görschstrasse 10A, 13187 Berlin, Germany
                            </p>
                        </section>
                    </div>
                </div>
            </main>

            <Footer />
        </div>
    );
}
