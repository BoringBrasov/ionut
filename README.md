# BORING Marketing MVP Backend

A FastAPI-based MVP implementation that covers onboarding, automated analysis, strategy planning, content generation, DM automation, a lightweight lead pipeline, and the AI Brain endpoints described in `BORING_MARKETING_MVP.md`.

## Requirements
- Python 3.11+
- pip

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running the API
```bash
uvicorn app.main:app --reload
```

The interactive docs are available at `http://127.0.0.1:8000/docs` once the server is running.

## Quick workflow
1. `POST /onboarding/start` to create a business profile.
2. `GET /analysis/run?business_id=...` to see instant recommendations.
3. `POST /strategy/generate` to produce a budget-calibrated plan.
4. `POST /content/generate` to create scheduled-ready posts.
5. `POST /dm/trigger` / `POST /dm/send` to record DM automation events.
6. `GET /pipeline` to inspect the generated leads.
7. `POST /brain/query` to ask the agent for insights.

All persisted data is stored in `boring_marketing.db` (SQLite) for easy local development.
