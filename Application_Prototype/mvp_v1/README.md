# AI Compass - MVP v1

## Overview
AI Compass is a strategic AI maturity assessment tool designed to help organizations benchmark their AI adoption and receive a personalized roadmap.

## Project Structure
- `backend/`: FastAPI application handling assessments, scoring, and PDF generation.
- `frontend/`: React + Vite application for the user interface.
- `start.bat`: Windows startup script.
- `start.sh`: Unix/Mac startup script.

## Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL (Optional, uses SQLite by default for MVP)

## Quick Start

### Windows
Double-click `start.bat` or run:
```cmd
start.bat
```

### Mac/Linux
Run:
```bash
chmod +x start.sh
./start.sh
```

## Manual Setup

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Key Features
- **Visitor Session**: Start assessment immediately without login.
- **Dynamic Assessment**: 8 Dimensions of AI Maturity.
- **Real-time Scoring**: Weighted scoring algorithm.
- **Cluster Analysis**: 5 Maturity Clusters (Passive to Transformative).
- **PDF Report**: Downloadable executive summary.

## Tech Stack
- **Backend**: FastAPI, SQLAlchemy, Pydantic
- **Frontend**: React, Tailwind CSS, Shadcn UI, Recharts, Framer Motion
- **Database**: SQLite (Development)

## Disclaimer
Generative AI outputs are probabilistic and should be verified. The EU AI Act classification is an automated estimation.
