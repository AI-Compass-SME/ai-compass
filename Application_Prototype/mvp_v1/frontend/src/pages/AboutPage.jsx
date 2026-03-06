import React, { useEffect } from 'react';
import { Navigation } from '../components/Navigation';
import { PageBackground } from '@/components/ui/PageBackground';
import { PageHeader } from '../components/PageHeader';
import { Footer } from '../components/Footer';
import { useTranslation, Trans } from 'react-i18next';

// Team Member Component for cleaner code
function TeamMember({ name, role, description, linkedInUrl, portfolioUrl, imageUrl }) {
    const { t } = useTranslation();
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
                                {t('pages.about.team.linkedin')}
                            </a>
                        )}
                        {portfolioUrl && (
                            <a
                                href={portfolioUrl}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-600 hover:text-slate-900 transition-colors"
                            >
                                <svg className="w-3.5 h-3.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                                {t('pages.about.team.portfolio')}
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
    const { t } = useTranslation();

    useEffect(() => {
        document.title = `${t('pages.about.title')} | AI Compass`;
    }, [t]);

    return (
        <div className="min-h-screen flex flex-col relative overflow-hidden bg-slate-50">
            <PageBackground />
            <Navigation />

            <main className="flex-grow w-full max-w-[80rem] mx-auto px-6 pt-28 pb-16 relative z-10">

                <PageHeader
                    title={t('pages.about.title')}
                    subtitle={t('pages.about.subtitle')}
                />

                <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-8 md:p-12">
                    <div className="grid md:grid-cols-2 gap-x-12 gap-y-6 text-sm text-gray-700">
                        {/* Row 1: Accountability Intro */}
                        <section className="md:col-span-2 mb-8">
                            <h2 className="text-sm font-bold text-gray-900 mb-2 uppercase tracking-wide text-xs">{t('pages.about.accountability.title')}</h2>
                            <p className="leading-relaxed text-lg font-medium text-gray-800">
                                {t('pages.about.accountability.text')}
                            </p>
                        </section>

                        {/* Row 2: Team (Full Width, Horizontal Cards) */}
                        <section className="md:col-span-2 mt-4">
                            <h2 className="text-sm font-bold text-gray-900 mb-6 uppercase tracking-wide text-xs">{t('pages.about.partners.title')}</h2>
                            <div className="grid md:grid-cols-2 gap-12">
                                {/* Role: Christian Miething */}
                                <TeamMember
                                    name="Christian Miething"
                                    role={t('pages.about.cm.role')}
                                    description={
                                        <span className="space-y-4 block">
                                            <span className="block">
                                                <strong className="block text-gray-900 mb-1">{t('pages.about.cm.p1Heading')}</strong>
                                                {t('pages.about.cm.p1')}
                                            </span>
                                            <span className="block">
                                                {t('pages.about.cm.p2')}
                                            </span>
                                            <span className="block">
                                                <strong className="block text-gray-900 mb-1 mt-2">{t('pages.about.cm.p3Heading')}</strong>
                                                {t('pages.about.cm.p3')}
                                            </span>
                                            <span className="block">
                                                {t('pages.about.cm.p4')}
                                            </span>
                                        </span>
                                    }
                                    linkedInUrl="https://www.linkedin.com/in/christian-miething-ai-strategy-execution/"
                                    imageUrl="/team/profile_image_cm.jpg"
                                />

                                {/* Role: Hamza Latif */}
                                <TeamMember
                                    name="Hamza Latif"
                                    role={t('pages.about.hl.role')}
                                    description={
                                        <span className="space-y-4 block">
                                            <span className="block">
                                                <strong className="block text-gray-900 mb-1">{t('pages.about.hl.p1Heading')}</strong>
                                                {t('pages.about.hl.p1')}
                                            </span>
                                            <span className="block">
                                                {t('pages.about.hl.p2')}
                                            </span>
                                            <span className="block">
                                                <strong className="block text-gray-900 mb-1 mt-2">{t('pages.about.hl.p3Heading')}</strong>
                                                {t('pages.about.hl.p3')}
                                            </span>
                                            <span className="block">
                                                {t('pages.about.hl.p4')}
                                            </span>
                                        </span>
                                    }
                                    linkedInUrl="https://www.linkedin.com/in/mhlatif207/"
                                    portfolioUrl="https://www.hamzalatif.com"
                                    imageUrl="/team/profile_image_mhl.jpg"
                                />
                            </div>
                        </section>

                        <section className="md:col-span-2 bg-purple-50 p-4 rounded-lg border border-purple-100 mt-2">
                            <h2 className="text-xs font-bold text-purple-900 mb-1 uppercase tracking-wide">
                                {t('pages.about.location.title')}
                            </h2>
                            <p className="text-xs text-purple-800 leading-relaxed">
                                {t('pages.about.location.l1')}<br />
                                {t('pages.about.location.l2')}
                            </p>
                        </section>
                    </div>
                </div>
            </main>

            <Footer />
        </div>
    );
}
