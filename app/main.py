from __future__ import annotations

from datetime import datetime
from typing import Dict, List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from . import models, schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Boring Marketing MVP", version="1.0.0")


@app.post("/onboarding/start", response_model=schemas.BusinessResponse)
def onboarding_start(payload: schemas.BusinessCreate, db: Session = Depends(get_db)):
    user = db.execute(select(models.User).where(models.User.email == payload.owner_email)).scalar_one_or_none()
    if not user:
        user = models.User(name=payload.owner_name, email=payload.owner_email)
        db.add(user)
        db.flush()

    business = models.Business(
        owner_id=user.id,
        name=payload.name,
        industry=payload.industry,
        objective=payload.objective,
        brand_tone=payload.brand_tone,
        resources_status=payload.resources_status,
        product_description=payload.product_description,
    )
    db.add(business)
    db.commit()
    db.refresh(business)

    _memorize(db, business.id, "onboarding", f"Brand tone: {business.brand_tone or 'calm'}")

    return business


@app.post("/onboarding/answer", response_model=schemas.BusinessResponse)
def onboarding_answer(business: schemas.BusinessResponse, db: Session = Depends(get_db)):
    db_business = db.get(models.Business, business.id)
    if not db_business:
        raise HTTPException(status_code=404, detail="Business not found")

    for field, value in business.dict(exclude={"id"}).items():
        setattr(db_business, field, value)

    db.commit()
    db.refresh(db_business)

    _memorize(db, db_business.id, "profile", f"Updated objectives: {db_business.objective}")

    return db_business


@app.get("/analysis/run", response_model=schemas.AnalysisResponse)
def run_analysis(business_id: int, db: Session = Depends(get_db)):
    business = db.get(models.Business, business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")

    tone = business.brand_tone or "calm"
    recommendations = [
        f"Lean into a {tone} voice to stay consistent.",
        "Post short-form video 3x per week to build awareness.",
        "Collect at least two testimonial clips for social proof.",
    ]

    summary = (
        f"{business.name} operates in {business.industry or 'an emerging space'} and focuses on {business.objective or 'organic growth'}."
    )
    return schemas.AnalysisResponse(business_id=business.id, summary=summary, recommendations=recommendations)


@app.post("/strategy/generate", response_model=schemas.StrategyResponse)
def generate_strategy(business_id: int, budget: int, db: Session = Depends(get_db)):
    business = db.get(models.Business, business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")

    plan = _build_content_plan(budget)
    strategy = models.Strategy(
        business_id=business.id,
        budget=budget,
        content_plan=plan["plan"],
        platforms=plan["platforms"],
        posting_frequency=plan["cadence"],
    )
    db.add(strategy)
    db.commit()
    db.refresh(strategy)

    _memorize(db, business.id, "strategy", f"Budget {budget}€ cadence {strategy.posting_frequency}")

    return strategy


@app.post("/content/generate", response_model=schemas.ContentResponse)
def generate_content(payload: schemas.ContentGenerateRequest, db: Session = Depends(get_db)):
    business = db.get(models.Business, payload.business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")

    tone = business.brand_tone or "calm"
    caption = _craft_caption(payload, business, tone)
    media_prompt = f"Create a {payload.content_type} highlighting {payload.topic} in a {tone} voice."

    post = models.ContentPost(
        business_id=business.id,
        platform=payload.platform,
        text=caption,
        media_prompt=media_prompt,
        status="draft",
        persona=payload.persona,
        pillar=payload.pillar,
        funnel_stage=payload.funnel_stage,
    )
    db.add(post)
    db.commit()
    db.refresh(post)

    return post


@app.put("/content/update-status", response_model=schemas.ContentResponse)
def update_content_status(payload: schemas.ContentStatusUpdate, db: Session = Depends(get_db)):
    post = db.get(models.ContentPost, payload.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    post.status = payload.status
    db.commit()
    db.refresh(post)
    return post


@app.post("/schedule/post", response_model=schemas.ContentResponse)
def schedule_post(payload: schemas.SchedulePostRequest, db: Session = Depends(get_db)):
    post = db.get(models.ContentPost, payload.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    post.scheduled_at = payload.scheduled_at
    post.status = "scheduled"
    db.commit()
    db.refresh(post)
    return post


@app.post("/dm/trigger", response_model=schemas.PipelineLead)
def trigger_dm(payload: schemas.DmTriggerRequest, db: Session = Depends(get_db)):
    business = db.get(models.Business, payload.business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")

    lead = (
        db.execute(
            select(models.Lead).where(
                models.Lead.business_id == business.id, models.Lead.name == payload.handle
            )
        ).scalar_one_or_none()
    )

    if not lead:
        lead = models.Lead(
            business_id=business.id,
            name=payload.handle,
            source=payload.source,
            pipeline_stage="new",
            conversation_history=[
                {
                    "author": "lead",
                    "message": payload.message or payload.event_type,
                    "timestamp": datetime.utcnow().isoformat(),
                }
            ],
        )
        db.add(lead)
    else:
        lead.conversation_history.append(
            {
                "author": "lead",
                "message": payload.message or payload.event_type,
                "timestamp": datetime.utcnow().isoformat(),
            }
        )

    _score_lead(lead, payload.event_type)

    db.commit()
    db.refresh(lead)
    return lead


@app.post("/dm/send", response_model=schemas.PipelineLead)
def send_dm(payload: schemas.DmSendRequest, db: Session = Depends(get_db)):
    lead = db.get(models.Lead, payload.lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    lead.conversation_history.append(
        {
            "author": payload.author,
            "message": payload.message,
            "timestamp": datetime.utcnow().isoformat(),
        }
    )

    if payload.author == "ai":
        lead.lead_score = min(100, lead.lead_score + 2)
    else:
        lead.lead_score = min(100, lead.lead_score + 5)
        if lead.lead_score > 70:
            lead.pipeline_stage = "hot"

    db.commit()
    db.refresh(lead)
    return lead


@app.get("/pipeline", response_model=List[schemas.PipelineLead])
def pipeline(business_id: int, db: Session = Depends(get_db)):
    leads = db.execute(select(models.Lead).where(models.Lead.business_id == business_id)).scalars().all()
    return leads


@app.post("/brain/query", response_model=schemas.BrainQueryResponse)
def brain_query(payload: schemas.BrainQueryRequest, db: Session = Depends(get_db)):
    business = db.get(models.Business, payload.business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")

    references = (
        db.execute(
            select(models.BrainMemory).where(models.BrainMemory.business_id == business.id).order_by(
                models.BrainMemory.created_at.desc()
            )
        )
        .scalars()
        .all()
    )

    context = ", ".join(memory.content for memory in references[:3]) or "calm tone"
    answer = _respond_to_brain_query(payload.query, business, context)
    return schemas.BrainQueryResponse(answer=answer, references=[memory.label for memory in references[:3]])


def _build_content_plan(budget: int) -> Dict[str, Dict]:
    if budget < 300:
        cadence = "3 posts/week"
        platforms = {"tiktok": 2, "instagram": 2}
    elif budget < 800:
        cadence = "5 posts/week"
        platforms = {"tiktok": 3, "instagram": 3, "facebook": 2}
    else:
        cadence = "7 posts/week"
        platforms = {"tiktok": 4, "instagram": 4, "youtube_shorts": 2, "linkedin": 2}

    plan = {
        "plan": {
            "education": 0.4,
            "brand": 0.3,
            "social_proof": 0.2,
            "sales": 0.1,
        },
        "platforms": platforms,
        "cadence": cadence,
    }
    return plan


def _craft_caption(payload: schemas.ContentGenerateRequest, business: models.Business, tone: str) -> str:
    persona = payload.persona or "community"
    hook = f"Pentru {persona}, {payload.topic} poate schimba jocul."
    narrative = (
        f"{business.name} arată cum un brand {tone} poate transforma {payload.topic} într-o poveste reală."
    )
    cta = "Scrie-ne în DM pentru detalii autentice."
    return f"{hook}\n{narrative}\n{cta}"


def _score_lead(lead: models.Lead, event_type: str) -> None:
    score_delta = {
        "comment": 5,
        "message": 10,
        "follow": 3,
        "story_reply": 7,
    }.get(event_type, 2)

    lead.lead_score = min(100, lead.lead_score + score_delta)
    if lead.lead_score > 75:
        lead.pipeline_stage = "hot"
    elif lead.lead_score > 55:
        lead.pipeline_stage = "warm"
    else:
        lead.pipeline_stage = "new"


def _respond_to_brain_query(query: str, business: models.Business, context: str) -> str:
    tone = business.brand_tone or "calm"
    if "strategie" in query.lower():
        return (
            f"Strategia actuală pentru {business.name} rămâne ancorată în {context}. "
            f"Păstrăm un ton {tone} și creștem accentul pe short-form video."
        )
    if "lead" in query.lower():
        return (
            f"Lead-urile fierbinți au nevoie de dovadă vizuală. Trimite un video scurt cu procesul pentru {business.name}."
        )
    return f"Îți răspund pe un ton {tone}: {context}."


def _memorize(db: Session, business_id: int, label: str, content: str) -> None:
    memory = models.BrainMemory(business_id=business_id, label=label, content=content)
    db.add(memory)
    db.commit()

