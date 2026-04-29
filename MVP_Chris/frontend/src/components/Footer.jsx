import { Compass, Linkedin, Twitter, Mail } from 'lucide-react';

export function Footer() {
    return (
        <footer className="bg-gray-900 text-gray-300 py-12 px-6 mt-auto">
            <div className="max-w-7xl mx-auto">
                <div className="grid md:grid-cols-4 gap-8 mb-8">
                    <div className="col-span-2">
                        <div className="flex items-center gap-3 mb-4">
                            <div className="bg-gradient-to-br from-blue-600 to-purple-600 p-2 rounded-lg">
                                <Compass className="w-6 h-6 text-white" />
                            </div>
                            <span className="text-xl font-semibold text-white">AI Compass</span>
                        </div>
                        <p className="text-gray-400 mb-4">
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
                            <li><a href="#" className="hover:text-blue-400 transition-colors">Features</a></li>
                            <li><a href="#" className="hover:text-blue-400 transition-colors">How it works</a></li>
                            <li><a href="#" className="hover:text-blue-400 transition-colors">Pricing</a></li>
                            <li><a href="#" className="hover:text-blue-400 transition-colors">FAQ</a></li>
                        </ul>
                    </div>

                    <div>
                        <h4 className="font-semibold text-white mb-4">Company</h4>
                        <ul className="space-y-2">
                            <li><a href="#" className="hover:text-blue-400 transition-colors">About</a></li>
                            <li><a href="#" className="hover:text-blue-400 transition-colors">Privacy Policy</a></li>
                            <li><a href="#" className="hover:text-blue-400 transition-colors">Terms of Service</a></li>
                            <li><a href="#" className="hover:text-blue-400 transition-colors">Contact</a></li>
                        </ul>
                    </div>
                </div>

                <div className="border-t border-gray-800 pt-8">
                    <div className="flex flex-col md:flex-row justify-between items-center gap-4">
                        <p className="text-gray-400 text-sm">
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
