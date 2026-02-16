import { Compass, Linkedin, Twitter, Mail } from 'lucide-react';
import { Link } from 'react-router-dom';

export function Footer() {
    return (
        <footer className="bg-slate-900 text-slate-300 py-12 px-6 mt-auto relative z-50 border-t border-slate-800">
            <div className="max-w-7xl mx-auto">
                <div className="grid md:grid-cols-4 gap-8 mb-8">
                    <div className="col-span-2">
                        <div className="flex items-center gap-3 mb-4">
                            <div className="bg-gradient-to-br from-blue-600 to-purple-600 p-2 rounded-lg">
                                <Compass className="w-6 h-6 text-white" />
                            </div>
                            <span className="text-xl font-semibold text-white">AI Compass</span>
                        </div>
                        <p className="text-slate-400 mb-4">
                            Navigate the AI Evolution with confidence. Professional AI maturity assessment for modern organizations.
                        </p>
                        <div className="flex gap-4">
                            <a href="#" className="hover:text-blue-400 transition-colors">
                                <Linkedin className="w-5 h-5" />
                            </a>
                            <a href="#" className="hover:text-blue-400 transition-colors">
                                <Twitter className="w-5 h-5" />
                            </a>
                            <a href="#" className="hover:text-blue-400 transition-colors">
                                <Mail className="w-5 h-5" />
                            </a>
                        </div>
                    </div>

                    <div>
                        <h4 className="font-semibold text-white mb-4">Product</h4>
                        <ul className="space-y-2">
                            <li><Link to="/methodology" className="hover:text-blue-400 transition-colors">Methodology</Link></li>
                            <li><Link to="/how-it-works" className="hover:text-blue-400 transition-colors">How it works</Link></li>
                        </ul>
                    </div>

                    <div>
                        <h4 className="font-semibold text-white mb-4">Company</h4>
                        <ul className="space-y-2">
                            <li><Link to="/about" className="hover:text-blue-400 transition-colors">About Us</Link></li>
                            <li><Link to="/contact" className="hover:text-blue-400 transition-colors">Contact</Link></li>
                            <li><Link to="/privacy" className="hover:text-blue-400 transition-colors">Privacy Policy</Link></li>
                            <li><Link to="/imprint" className="hover:text-blue-400 transition-colors">Imprint</Link></li>
                        </ul>
                    </div>
                </div>

                <div className="border-t border-slate-800 pt-8">
                    <div className="flex flex-col md:flex-row justify-between items-center gap-4">
                        <p className="text-slate-400 text-sm">
                            © 2026 AI Compass. All rights reserved.
                        </p>
                        <div className="flex gap-4 text-sm">
                            <span className="flex items-center gap-2">
                                <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                                Trusted by 500+ Organizations
                            </span>
                        </div>
                    </div>

                </div>
            </div>
        </footer>
    );
}
