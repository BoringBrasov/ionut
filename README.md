# BORING Marketing MVP Backend

A FastAPI-based MVP implementation that covers onboarding, automated analysis, strategy planning, content generation, DM automation, a lightweight lead pipeline, the AI Brain, and brand resources described in `BORING_MARKETING_MVP.md`.

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
1. `POST /auth/signup` + `POST /auth/login` to manage access tokens.
2. `POST /onboarding/start` followed by `/onboarding/session` + `/onboarding/session/{id}/answer` to capture the multi-step onboarding flow (see `/onboarding/questions`).
3. `GET /analysis/run?business_id=...` to see instant recommendations.
4. `POST /strategy/generate` to produce a budget-calibrated plan.
5. `POST /content/generate` or `POST /content/batch` to create scheduled-ready posts, then `POST /content/feedback` + `POST /schedule/auto` to review and schedule.
6. `GET /content/calendar` to fetch a ready-to-use posting calendar.
7. `POST /media/assets` + `GET /media/assets` to keep track of brand resources, and `POST /personas/generate` to build persona libraries.
8. `POST /dm/flows` + `/dm/flows/{id}/activate` to define automation flows, while `POST /dm/trigger` / `POST /dm/send` log actual conversations.
9. `GET /pipeline`, `POST /leads/stage`, and `POST /leads/note` to manage the pipeline.
10. `GET /dashboard/overview`, `GET /analytics/performance`, and `GET /analytics/insights` to power the overview and analytics widgets.
11. `POST /brain/query` to ask the agent for insights.

All persisted data is stored in `boring_marketing.db` (SQLite) for easy local development.
