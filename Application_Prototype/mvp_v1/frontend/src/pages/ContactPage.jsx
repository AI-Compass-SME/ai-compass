import React, { useEffect } from 'react';
import { Navigation } from '../components/Navigation';
import { PageBackground } from '@/components/ui/PageBackground';
import { PageHeader } from '../components/PageHeader';
import { Footer } from '../components/Footer';
import { Shield, Mail, MapPin, Phone } from 'lucide-react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

export default function ContactPage() {
    const { t } = useTranslation();

    useEffect(() => {
        document.title = `${t('pages.contact.title')} | AI Compass`;
    }, [t]);

    return (
        <div className="min-h-screen flex flex-col relative overflow-hidden bg-slate-50">
            <PageBackground />
            <Navigation />

            <main className="flex-grow w-full max-w-[80rem] mx-auto px-6 pt-28 pb-16 relative z-10">

                <PageHeader
                    title={t('pages.contact.title')}
                    subtitle={t('pages.contact.subtitle')}
                />

                <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-8 md:p-12 mx-auto">

                    <div className="mb-10 text-left w-full">
                        <p className="text-lg text-gray-700 leading-relaxed">
                            {t('pages.contact.intro')}
                        </p>
                    </div>

                    <div className="grid md:grid-cols-2 gap-8 md:gap-12">

                        {/* Left Column: Direct Contact */}
                        <div className="space-y-8">
                            {/* Phone */}
                            <div className="flex items-start gap-4">
                                <div className="bg-blue-50 p-3 rounded-lg text-blue-600 mt-1">
                                    <Phone className="w-5 h-5" />
                                </div>
                                <div>
                                    <h3 className="text-base font-bold text-gray-900 mb-1">{t('pages.contact.phone.title')}</h3>
                                    <p className="text-sm font-medium text-gray-900">{t('pages.contact.phone.main')}: <span className="text-gray-500 font-normal">{t('pages.contact.phone.val')}</span></p>
                                    <p className="text-xs text-gray-500 mt-1">{t('pages.contact.phone.time')}</p>
                                </div>
                            </div>

                            {/* Email */}
                            <div className="flex items-start gap-4">
                                <div className="bg-purple-50 p-3 rounded-lg text-purple-600 mt-1">
                                    <Mail className="w-5 h-5" />
                                </div>
                                <div>
                                    <h3 className="text-base font-bold text-gray-900 mb-1">{t('pages.contact.email.title')}</h3>
                                    <p className="text-sm font-medium text-gray-900">{t('pages.contact.email.main')}: <span className="text-gray-500 font-normal">{t('pages.contact.email.val')}</span></p>
                                    <p className="text-xs text-gray-500 mt-1">{t('pages.contact.email.time')}</p>
                                </div>
                            </div>

                            {/* Office */}
                            <div className="flex items-start gap-4">
                                <div className="bg-emerald-50 p-3 rounded-lg text-emerald-600 mt-1">
                                    <MapPin className="w-5 h-5" />
                                </div>
                                <div>
                                    <h3 className="text-base font-bold text-gray-900 mb-1">{t('pages.contact.office.title')}</h3>
                                    <p className="text-sm text-gray-600 leading-relaxed">
                                        Christian Miething<br />
                                        Görschstrasse 10A<br />
                                        13187 Berlin, Germany
                                    </p>
                                </div>
                            </div>
                        </div>

                        {/* Right Column: Legal & Privacy */}
                        <div className="bg-gray-50 rounded-xl p-6 border border-gray-100 h-full">
                            <div className="flex items-center gap-2 mb-4">
                                <div className="relative w-5 h-5 flex-shrink-0 flex items-center justify-center">
                                    <Shield className="w-5 h-5 text-gray-600 absolute" />
                                    <Shield className="w-2.5 h-2.5 text-gray-600 fill-gray-600 absolute" />
                                </div>
                                <h3 className="text-base font-bold text-gray-900">{t('pages.contact.legal.title')}</h3>
                            </div>

                            <div className="space-y-6 text-sm text-gray-600">
                                <div>
                                    <strong className="block text-gray-900 mb-1 text-xs uppercase tracking-wide">{t('pages.contact.legal.privacy')}</strong>
                                    <p className="leading-relaxed">
                                        {t('pages.contact.legal.privacyText')}<Link to="/privacy" className="text-blue-600 hover:underline">{t('footer.privacy')}</Link>.
                                    </p>
                                </div>

                                <div>
                                    <strong className="block text-gray-900 mb-1 text-xs uppercase tracking-wide">{t('pages.contact.legal.imprint')}</strong>
                                    <p className="leading-relaxed">
                                        {t('pages.contact.legal.imprintText')}<Link to="/imprint" className="text-blue-600 hover:underline">{t('footer.imprint')}</Link>.
                                    </p>
                                </div>
                            </div>
                        </div>

                    </div>
                </div>
            </main>

            <Footer />
        </div>
    );
}
