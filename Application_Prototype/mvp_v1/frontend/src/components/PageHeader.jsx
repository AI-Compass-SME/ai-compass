import React from 'react';

export function PageHeader({ title, subtitle, centered = true }) {
    return (
        <div className={`mb-8 ${centered ? 'text-center' : ''} relative`}>
            {/* Subtle decorative background blur */}
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-blue-100/50 rounded-full blur-3xl -z-10" />

            {/* Overline */}
            <p className="text-sm font-bold tracking-[0.2em] text-blue-600 uppercase mb-3 px-4">
                {subtitle}
            </p>

            {/* Main Title */}
            <h1 className="text-2xl md:text-3xl lg:text-4xl font-extrabold text-slate-900 tracking-tight leading-tight mb-6">
                <span className="bg-clip-text text-transparent bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900">
                    {title}
                </span>
            </h1>

            {/* Decorative Separator */}
            <div className="flex items-center justify-center gap-2">
                <div className="h-px w-12 bg-gradient-to-r from-transparent to-blue-200" />
                <div className="w-1.5 h-1.5 rounded-full bg-blue-600" />
                <div className="h-px w-12 bg-gradient-to-l from-transparent to-blue-200" />
            </div>
        </div>
    );
}
