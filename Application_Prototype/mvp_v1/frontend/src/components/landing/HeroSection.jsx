import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, Shield, Clock, Award, Loader2 } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { ImageWithFallback } from './ImageWithFallback';

export function HeroSection({ onStart, isStarting }) {
    return (
        <section className="pt-24 pb-12 px-6">
            <div className="max-w-[80rem] mx-auto">
                <div className="grid lg:grid-cols-2 gap-8 lg:gap-12 items-center">
                    <div>
                        <h1 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-4 leading-tight tracking-tight">
                            Navigate Your AI Evolution with the AI Compass.
                        </h1>
                        <p className="text-lg text-gray-600 mb-6 leading-relaxed">
                            Stop guessing. Gain strategic clarity in 10-15 minutes. Benchmark your Organization against 500+ peers and receive a data-driven roadmap to AI maturity. No costs attached, just your valuable time.
                        </p>

                        <div className="flex flex-col sm:flex-row gap-4">
                            <Button
                                onClick={onStart}
                                disabled={isStarting}
                                className="group bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-6 rounded-lg text-lg font-semibold hover:shadow-xl transition-all h-auto"
                            >
                                {isStarting ? (
                                    <>
                                        <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                                        Starting...
                                    </>
                                ) : (
                                    <>
                                        Start Free Assessment
                                        <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
                                    </>
                                )}
                            </Button>
                        </div>

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
                    <div className="relative flex justify-center lg:justify-end">
                        <div className="absolute inset-0 bg-gradient-to-br from-blue-600/20 to-purple-600/20 rounded-2xl blur-3xl transform scale-90"></div>
                        <ImageWithFallback
                            src="https://images.unsplash.com/photo-1697577418970-95d99b5a55cf?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxhcnRpZmljaWFsJTIwaW50ZWxsaWdlbmNlJTIwdGVjaG5vbG9neXxlbnwxfHx8fDE3NjgyMDU3MDZ8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral"
                            alt="AI Technology"
                            className="relative rounded-2xl shadow-2xl w-full max-w-md h-auto object-cover max-h-[400px]"
                        />
                    </div>
                </div>
            </div>
        </section>
    );
}
