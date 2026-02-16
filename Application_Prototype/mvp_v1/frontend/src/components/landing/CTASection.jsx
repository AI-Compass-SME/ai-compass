import React from 'react';
import { motion } from 'framer-motion';
import { ArrowRight, Loader2 } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Link } from 'react-router-dom';

export function CTASection({ onStart, isStarting }) {
    return (
        <section className="py-20 px-6 bg-gradient-to-r from-blue-600 to-purple-600">
            <div className="max-w-4xl mx-auto text-center">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6 }}
                    viewport={{ once: true }}
                >
                    <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
                        Ready to discover your AI Maturity?
                    </h2>
                    <p className="text-xl text-blue-100 mb-8">
                        Join 500+ organizations that have already mapped their AI journey
                    </p>
                    <Button
                        onClick={onStart}
                        disabled={isStarting}
                        className="group bg-white text-blue-600 px-10 py-6 h-auto rounded-lg text-lg font-semibold hover:shadow-2xl hover:bg-slate-50 transition-all inline-flex items-center gap-3 border-none"
                    >
                        {isStarting ? (
                            <>
                                <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                                Starting...
                            </>
                        ) : (
                            <>
                                Start Now
                                <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
                            </>
                        )}
                    </Button>
                </motion.div>
            </div>
        </section>
    );
}
