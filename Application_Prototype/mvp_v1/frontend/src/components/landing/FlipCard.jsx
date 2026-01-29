import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { CornerDownRight } from 'lucide-react';

export function FlipCard({ title, icon: Icon, what, why, index }) {
    const [isFlipped, setIsFlipped] = useState(false);

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
            viewport={{ once: true }}
            className="h-[175px]"
            style={{ perspective: '1000px' }}
        >
            <motion.div
                className="relative w-full h-full cursor-pointer group"
                style={{ transformStyle: 'preserve-3d' }}
                animate={{ rotateY: isFlipped ? 180 : 0 }}
                transition={{ duration: 0.6 }}
                onClick={() => setIsFlipped(!isFlipped)}
            >
                {/* Front */}
                <div
                    className="absolute inset-0 bg-white rounded-xl shadow-lg border border-gray-200 p-2 flex flex-col items-center justify-center text-center h-full overflow-hidden"
                    style={{ backfaceVisibility: 'hidden', WebkitBackfaceVisibility: 'hidden' }}
                >
                    <div className="bg-gradient-to-br from-blue-100 to-purple-100 p-3 rounded-full mb-3">
                        <Icon className="w-6 h-6 text-blue-600" />
                    </div>
                    <h3 className="text-sm font-bold text-gray-900 leading-tight px-2">{title}</h3>

                    <div className="absolute bottom-2 right-2 text-gray-400 group-hover:text-blue-500 transition-colors">
                        <CornerDownRight className="w-3 h-3" />
                    </div>
                </div>

                {/* Back */}
                <div
                    className="absolute inset-0 bg-gradient-to-br from-blue-600 to-purple-600 rounded-xl shadow-lg border border-transparent p-2 text-white flex flex-col justify-center overflow-hidden"
                    style={{
                        backfaceVisibility: 'hidden',
                        WebkitBackfaceVisibility: 'hidden',
                        transform: 'rotateY(180deg)',
                    }}
                >
                    <div className="space-y-1.5">
                        <div>
                            <h4 className="font-bold text-[9px] uppercase tracking-wider text-blue-200 mb-0.5">What it is</h4>
                            <p className="text-xs leading-tight">{what}</p>
                        </div>
                        <div>
                            <h4 className="font-bold text-[9px] uppercase tracking-wider text-blue-200 mb-0.5">Why needed</h4>
                            <p className="text-xs leading-tight">{why}</p>
                        </div>
                    </div>
                </div>
            </motion.div>
        </motion.div>
    );
}
