import React, { useEffect } from 'react';
import { Navigation } from '../components/Navigation';
import { PageBackground } from '@/components/ui/PageBackground';
import { PageHeader } from '../components/PageHeader';
import { Footer } from '../components/Footer';
import { useTranslation } from 'react-i18next';

export default function ImprintPage() {
    const { t } = useTranslation();

    useEffect(() => {
        document.title = `${t('pages.imprint.title')} | AI Compass`;
    }, [t]);

    return (
        <div className="min-h-screen flex flex-col relative overflow-hidden bg-slate-50">
            <PageBackground />
            <Navigation />

            <main className="flex-grow w-full max-w-[80rem] mx-auto px-6 pt-28 pb-16 relative z-10">

                <PageHeader
                    title={t('pages.imprint.title')}
                    subtitle={t('pages.imprint.subtitle')}
                />

                <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-8 md:p-12">
                    <div className="grid md:grid-cols-2 gap-x-12 gap-y-6 text-sm text-gray-700">
                        <section>
                            <h2 className="text-sm font-bold text-gray-900 mb-1 uppercase tracking-wide text-xs">{t('pages.imprint.info')}</h2>
                            <p className="leading-relaxed">
                                Christian Miething<br />
                                Görschstraße 10A<br />
                                13187 Berlin, Germany
                            </p>
                        </section>

                        <section>
                            <h2 className="text-sm font-bold text-gray-900 mb-1 uppercase tracking-wide text-xs">{t('pages.imprint.contact')}</h2>
                            <p className="leading-relaxed">
                                {t('pages.contact.phone.title')}: {t('pages.contact.phone.val')}<br />
                                E-Mail: info@the-ai-compass.de<br />
                                Website: www.the-ai-compass.de
                            </p>
                        </section>

                        <section>
                            <h2 className="text-sm font-bold text-gray-900 mb-1 uppercase tracking-wide text-xs">{t('pages.imprint.responsible')}</h2>
                            <p className="leading-relaxed">
                                Christian Miething<br />
                                Görschstraße 10A<br />
                                13187 Berlin, Germany
                            </p>
                        </section>

                        <section>
                            <h2 className="text-sm font-bold text-gray-900 mb-1 uppercase tracking-wide text-xs">{t('pages.imprint.eu')}</h2>
                            <p className="leading-relaxed">
                                {t('pages.imprint.euText')}{' '}
                                <a href="https://ec.europa.eu/consumers/odr" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
                                    ec.europa.eu/consumers/odr
                                </a>.
                            </p>
                        </section>

                        <section className="md:col-span-2">
                            <h2 className="text-sm font-bold text-gray-900 mb-1 uppercase tracking-wide text-xs">{t('pages.imprint.consumer')}</h2>
                            <p className="leading-relaxed">
                                {t('pages.imprint.consumerText')}
                            </p>
                        </section>

                        <section className="md:col-span-2 bg-gray-50 p-4 rounded-lg border border-gray-200 mt-2">
                            <h2 className="text-xs font-bold text-gray-900 mb-1 uppercase tracking-wide">
                                {t('pages.imprint.disclaimer')}
                            </h2>
                            <p className="text-xs text-gray-600 leading-relaxed">
                                {t('pages.imprint.disclaimerText')}
                            </p>
                        </section>
                    </div>
                </div>
            </main>

            <Footer />
        </div>
    );
}
