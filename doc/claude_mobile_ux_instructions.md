# Mobile UX/UI Improvement Instructions

## Project Context for Claude Code
- **Working Directory:** The frontend codebase is located in `Application_Prototype/mvp_v1/frontend/`. You should run commands and look for files relative to this directory.
- **Tech Stack:** React, Vite, Tailwind CSS (v4), and Recharts. 
- **Dev Server:** You can run `npm run dev` inside the frontend directory to preview your changes.
- **Styling approach:** Use Tailwind CSS responsive utility classes (like `max-md:`, `md:`, `sm:`) to apply the requested mobile fixes.


**IMPORTANT Constraints for Claude Code:**
- Apply these styling changes **ONLY** to the mobile layout using Tailwind's responsive prefixes (like `md:` or `max-md:`).
- **DO NOT** alter the core logic, translation keys, or desktop designs. Only apply CSS/layout tweaks.

## 1. Landing Page (`src/components/landing/HeroSection.jsx`)
- **Hero Section Font Size:** In the `h1` tag, reduce the mobile font size. Change `text-4xl` to `text-3xl md:text-4xl`.
- **Hero Headline Padding:** In the parent `<section>` tag, the padding is currently `pt-32`. Change this to `pt-20 md:pt-32` to reduce the excessive top whitespace on mobile.
- **Radar Chart:** (Handled in the Results section below as the component logic is similar or shared).

## 2. Results Page
- **Hero Section Padding (`src/pages/ResultsPage.jsx` or `ResultsHero.jsx`):** 
  - Look at the `<main>` tag in `ResultsPage.jsx` which has `pt-24`. Change it to `pt-16 md:pt-24` to reduce the top padding before the hero component on mobile.
- **Positioning Component (`src/components/results/ClusterProfile.jsx`):** 
  - The cluster names displayed below the chart in the `<h4>` tags are squishing together. Implement a line break or separator strategy so the long names wrap nicely instead of breaking awkwardly mid-word.
- **Multi-Dimensional Maturity Profile (`src/components/results/MaturityProfile.jsx`):** 
  - The `RadarChart` labels (especially long German words like "Tech Infrastructure") rendered by `renderCustomTick` are overflowing their container and being cut off. 
  - **Fix:** Decrease the `outerRadius` of the `RadarChart` on mobile (e.g., to `60%` or `65%`) or adjust the wrapping `ResponsiveContainer` styles so the text is fully visible. It is acceptable if the text overlaps slightly with the radar chart itself.
- **Roadmap Component (`src/components/results/Roadmap.jsx`):** 
  - Currently, the step numbers (`01`, `02`, `03`) are rendered in a separate `flex` column (`{phaseDef.step}`). 
  - **Fix:** On mobile, move the step number so it sits directly on top of the Phase Title (`h3`) inside the left column's card, with **zero padding/margin** between the number and the title.
- **Translations (`de.json`):** 
  - There is some English mixed into the German localization strings. If you spot obvious missing keys or quick fixes, apply them. Otherwise, leave as is.
- **Contact Section (`src/components/results/ExpertConsultation.jsx`):** 
  - Update the hardcoded placeholder phone number (`+1 (234) 567-890`) to `+493086319343` in both the `href` and the display text.
  - Slightly reduce the font sizes for mobile (e.g., change `text-lg` to `text-base md:text-lg`) to prevent the contact boxes from stretching vertically.
- **PDF Download Section (`src/components/results/DownloadCTA.jsx`):** 
  - Slightly reduce the font sizes (e.g., `text-3xl` to `text-2xl md:text-3xl`) and adjust the padding of the bounding boxes to match the new text size on mobile screens.
