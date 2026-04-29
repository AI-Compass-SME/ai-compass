
import { Mountain } from 'lucide-react';

export function Footer() {
    return (
        <footer className="bg-slate-900 text-white py-12 mt-20">
            <div className="max-w-7xl mx-auto px-6 grid grid-cols-1 md:grid-cols-4 gap-8">
                <div className="col-span-1 md:col-span-2">
                    <div className="flex items-center gap-2 mb-4">
                        <Mountain className="h-6 w-6 text-blue-400" />
                        <span className="text-xl font-semibold tracking-tight">AI Compass</span>
                    </div>
                    <p className="text-slate-400 max-w-sm">
                        Helping Mittelstand companies navigate the AI revolution with data-driven insights and actionable roadmaps.
                    </p>
                </div>

                <div>
                    <h3 className="font-semibold mb-4 text-slate-200">Product</h3>
                    <ul className="space-y-2 text-slate-400 text-sm">
                        <li><a href="#" className="hover:text-blue-400 transition-colors">Assessment</a></li>
                        <li><a href="#" className="hover:text-blue-400 transition-colors">Methodology</a></li>
                        <li><a href="#" className="hover:text-blue-400 transition-colors">Case Studies</a></li>
                        <li><a href="#" className="hover:text-blue-400 transition-colors">Pricing</a></li>
                    </ul>
                </div>

                <div>
                    <h3 className="font-semibold mb-4 text-slate-200">Legal</h3>
                    <ul className="space-y-2 text-slate-400 text-sm">
                        <li><a href="#" className="hover:text-blue-400 transition-colors">Privacy Policy</a></li>
                        <li><a href="#" className="hover:text-blue-400 transition-colors">Terms of Service</a></li>
                        <li><a href="#" className="hover:text-blue-400 transition-colors">Imprint</a></li>
                    </ul>
                </div>
            </div>
            <div className="max-w-7xl mx-auto px-6 mt-12 pt-8 border-t border-slate-800 text-center text-slate-500 text-sm">
                &copy; {new Date().getFullYear()} AI Compass. All rights reserved. Made in Germany.
            </div>
        </footer>
    );
}
