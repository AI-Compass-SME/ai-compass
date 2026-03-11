import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Shield, Clock, Award } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { ImageWithFallback } from './ImageWithFallback';

export function HeroSection() {
    return (
        <section className="pt-32 pb-20 px-6">
            <div className="max-w-7xl mx-auto">
                <div className="grid lg:grid-cols-2 gap-12 items-center">
                    <div>
                        <h1 className="text-5xl lg:text-6xl font-bold text-gray-900 mb-6 leading-tight">
                            Strategische Orientierung in der KI-Transformation: Der AI Compass
                        </h1>
                        <p className="text-xl text-gray-600 mb-8 leading-relaxed">
                            Ersetzen Sie Annahmen durch fundierte Erkenntnisse. Erlangen Sie innerhalb von 10–15 Minuten strategische Klarheit über Ihren Status quo. Durch ein Benchmarking mit über 500 Vergleichsunternehmen erhalten Sie eine datenbasierte Roadmap zur Steigerung Ihres KI-Reifegrades. Diese fundierte Selbstanalyse ist für Sie kostenfrei.
                        </p>

                        <Button asChild className="group bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-6 rounded-lg text-lg font-semibold hover:shadow-xl transition-all h-auto">
                            <Link to="/snapshot" className="flex items-center gap-2">
                                Kostenlose Analyse starten
                                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                            </Link>
                        </Button>

                        <div className="flex items-center gap-6 mt-8 text-sm text-gray-600 flex-wrap">
                            <div className="flex items-center gap-2">
                                <Clock className="w-4 h-4" />
                                <span>Takes 10-15 mins</span>
                            </div>
                            <div className="flex items-center gap-2">
                                <Shield className="w-4 h-4" />
                                <span>GDPR Compliant</span>
                            </div>
                            <div className="flex items-center gap-2">
                                <Award className="w-4 h-4" />
                                <span>Professional Framework</span>
                            </div>
                        </div>
                    </div>
                    <div className="relative">
                        <div className="absolute inset-0 bg-gradient-to-br from-blue-600/20 to-purple-600/20 rounded-2xl blur-3xl"></div>
                        <ImageWithFallback
                            src="https://images.unsplash.com/photo-1697577418970-95d99b5a55cf?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxhcnRpZmljaWFsJTIwaW50ZWxsaWdlbmNlJTIwdGVjaG5vbG9neXxlbnwxfHx8fDE3NjgyMDU3MDZ8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral"
                            alt="AI Technology"
                            className="relative rounded-2xl shadow-2xl w-full h-auto"
                        />
                    </div>
                </div>
            </div>
        </section>
    );
}
