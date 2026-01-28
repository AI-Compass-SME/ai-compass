# AI Compass - Frontend (MVP v1)

The frontend for the AI Compass application, built with **React** and **Vite**.

## 🚀 Overview

This application provides the user interface for the AI Maturity Assessment. It is designed to be fast, responsive, and visually extremely premium ("High-End Consultant" feel).

### Key Technologies
- **Framework:** React 18
- **Build Tool:** Vite
- **Styling:** Tailwind CSS + `shadcn/ui`
- **Routing:** React Router DOM v6
- **State Management:** React Context + SessionStorage (Persistence)
- **Visuals:** Recharts, Lucide React, Framer Motion

---

## 📂 Project Structure

```text
src/
├── assets/          # Static images and global assets
├── components/      # Reusable UI components
│   ├── ui/          # Generic UI atoms (Buttons, Cards - shadcn)
│   ├── landing/     # Landing page specific sections
│   ├── results/     # Results page charts and widgets
│   └── Navigation.jsx
├── context/         # Global state (AssessmentContext)
├── hooks/           # Custom hooks (useAssessment, useAutosave)
├── lib/             # Utilities (api.js, utils.js)
├── pages/           # Main route views
│   ├── LandingPage.jsx
│   ├── QuestionnaireWizard.jsx
│   └── ResultsPage.jsx
└── App.jsx          # Root component & Routing
```

---

## 🛠 Available Scripts

> **Note:** For daily development, we recommend using the root `start.sh` (or `start.bat`) script to launch the full stack (Backend + Frontend) simultaneously. Use the commands below for specific frontend-only tasks or production builds.

In the project directory, you can run:

### `npm run dev`
Runs the app in the development mode.\
Open [http://localhost:5173](http://localhost:5173) to view it in your browser.

### `npm run build`
Builds the app for production to the `dist` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

### `npm run preview`
Locally preview the production build.

---

## 🔌 API Integration

The frontend expects the Backend API to be running at `http://localhost:8000` (default).
Configuration is handled in `.env`:
```env
VITE_API_URL=http://localhost:8000
```
