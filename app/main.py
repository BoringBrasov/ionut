from __future__ import annotations

import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from . import models, schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Boring Marketing MVP", version="1.0.0")

ONBOARDING_QUESTIONS: List[schemas.OnboardingQuestion] = [
    schemas.OnboardingQuestion(
        key="identity",
        prompt="Hai să începem. Cum se numește brandul tău și ce vinzi?",
        qtype="text",
        options=[],
    ),
    schemas.OnboardingQuestion(
        key="goals",
        prompt="În industria ta, scopurile obișnuite sunt acestea. Alege-le pe ale tale.",
        qtype="multi-select",
        options=[
            "Crestere vânzări directe",
            "Atragere distribuitori",
            "Lansare produs nou",
            "Brand awareness",
        ],
    ),
    schemas.OnboardingQuestion(
        key="channels",
        prompt="Care sunt canalele principale de vânzare?",
        qtype="select",
        options=[
            "Direct către clienți",
            "Distribuitori",
            "Magazine locale",
            "Online store",
        ],
    ),
    schemas.OnboardingQuestion(
        key="tone",
        prompt="Ce ton ar trebui să aibă brandul?",
        qtype="multi-select",
        options=[
            "Cald",
            "Premium",
            "Serios",
            "Amuzant",
            "Rustic",
            "Urban",
        ],
    ),
    schemas.OnboardingQuestion(
        key="media",
        prompt="Ce resurse media ai acum?",
        qtype="multi-select",
        options=[
            "Logo",
            "Poze produs",
            "Testimoniale",
            "Video fondator",
            "Nimic încă",
        ],
    ),
]


@app.post("/auth/signup", response_model=schemas.AuthResponse)
def signup(payload: schemas.SignUpRequest, db: Session = Depends(get_db)):
    existing = db.execute(select(models.User).where(models.User.email == payload.email)).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = models.User(name=payload.name, email=payload.email, password_hash=_hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)

    token = _issue_token(db, user.id)
    return schemas.AuthResponse(user_id=user.id, token=token.token, expires_at=token.expires_at)


@app.post("/auth/login", response_model=schemas.AuthResponse)
def login(payload: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.execute(select(models.User).where(models.User.email == payload.email)).scalar_one_or_none()
    if not user or not user.password_hash or not _verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = _issue_token(db, user.id)
    return schemas.AuthResponse(user_id=user.id, token=token.token, expires_at=token.expires_at)


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


@app.get("/onboarding/questions", response_model=List[schemas.OnboardingQuestion])
def onboarding_questions() -> List[schemas.OnboardingQuestion]:
    return ONBOARDING_QUESTIONS


@app.post("/onboarding/session", response_model=schemas.OnboardingSessionResponse)
def onboarding_session(payload: schemas.OnboardingSessionCreate, db: Session = Depends(get_db)):
    business = db.get(models.Business, payload.business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")

    session = models.OnboardingSession(business_id=business.id, total_steps=payload.total_steps)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


@app.post("/onboarding/session/{session_id}/answer", response_model=schemas.OnboardingSessionResponse)
def onboarding_answer_step(
    session_id: int, payload: schemas.OnboardingAnswerRequest, db: Session = Depends(get_db)
):
    session = db.get(models.OnboardingSession, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    responses = dict(session.responses or {})
    responses[payload.step_key] = payload.answer
    session.responses = responses
    session.questions_answered = len(responses)
    session.current_step = max(session.current_step, payload.step_index)
    if payload.is_final:
        session.completed = True
        _memorize(
            db,
            session.business_id,
            "onboarding_session",
            _summarize_onboarding(session),
        )

    db.commit()
    db.refresh(session)
    return session


@app.get("/onboarding/session/{session_id}", response_model=schemas.OnboardingSessionResponse)
def get_onboarding_session(session_id: int, db: Session = Depends(get_db)):
    session = db.get(models.OnboardingSession, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


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


@app.post("/content/batch", response_model=List[schemas.ContentResponse])
def batch_content(payload: schemas.ContentBatchRequest, db: Session = Depends(get_db)):
    business = db.get(models.Business, payload.business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")

    posts: List[models.ContentPost] = []
    for topic in payload.topics:
        for platform in payload.platforms:
            request = schemas.ContentGenerateRequest(
                business_id=payload.business_id,
                platform=platform,
                content_type="auto",
                topic=topic,
                persona=payload.persona,
                pillar=payload.pillar,
                funnel_stage=payload.funnel_stage,
            )
            posts.append(generate_content(request, db))
    return posts


@app.post("/content/feedback", response_model=schemas.ContentResponse)
def review_content(payload: schemas.ContentFeedbackRequest, db: Session = Depends(get_db)):
    post = db.get(models.ContentPost, payload.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    decision_to_status = {
        "accept": "approved",
        "modify": "needs_revision",
        "reject": "rejected",
    }
    post.status = decision_to_status.get(payload.decision, post.status)
    post.feedback_reason = payload.reason
    post.feedback_notes = payload.notes

    if payload.decision == "accept":
        post.performance_score = min(100, post.performance_score + 12)
    elif payload.decision == "reject":
        post.performance_score = max(0, post.performance_score - 8)

    db.commit()
    db.refresh(post)

    _memorize(
        db,
        post.business_id,
        "feedback",
        f"{payload.decision}::{payload.reason or 'general'}",
    )

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


@app.post("/schedule/auto", response_model=List[schemas.ContentResponse])
def auto_schedule(payload: schemas.AutoScheduleRequest, db: Session = Depends(get_db)):
    business = db.get(models.Business, payload.business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")

    posts = (
        db.execute(
            select(models.ContentPost)
            .where(models.ContentPost.business_id == business.id)
            .where(models.ContentPost.scheduled_at.is_(None))
            .where(models.ContentPost.status.in_(["approved", "draft"]))
            .order_by(models.ContentPost.id.asc())
        )
        .scalars()
        .all()
    )

    start = payload.start_date or datetime.utcnow()
    scheduled_posts: List[models.ContentPost] = []
    for idx, post in enumerate(posts):
        slot = start + timedelta(minutes=payload.interval_minutes * idx)
        post.scheduled_at = slot
        post.status = "scheduled"
        scheduled_posts.append(post)

    db.commit()
    return scheduled_posts


@app.get("/content/calendar", response_model=List[schemas.ContentCalendarEntry])
def content_calendar(
    business_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
):
    business = db.get(models.Business, business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")

    query = select(models.ContentPost).where(models.ContentPost.business_id == business.id)
    if start_date:
        query = query.where(models.ContentPost.scheduled_at >= start_date)
    if end_date:
        query = query.where(models.ContentPost.scheduled_at <= end_date)

    posts = db.execute(query.order_by(models.ContentPost.scheduled_at.asc())).scalars().all()
    entries: List[schemas.ContentCalendarEntry] = []
    for post in posts:
        base = schemas.ContentCalendarEntry.from_orm(post)
        entries.append(base.copy(update={"scheduled_day": post.scheduled_at}))
    return entries


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
    _apply_dm_flow(db, business, lead, payload.event_type)

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


@app.post("/leads/stage", response_model=schemas.PipelineLead)
def update_lead_stage(payload: schemas.LeadStageUpdate, db: Session = Depends(get_db)):
    lead = db.get(models.Lead, payload.lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    lead.pipeline_stage = payload.stage
    if payload.stage == "lost":
        lead.lead_score = max(0, lead.lead_score - 15)
    elif payload.stage in {"hot", "booked"}:
        lead.lead_score = min(100, lead.lead_score + 10)

    db.commit()
    db.refresh(lead)
    return lead


@app.post("/leads/note", response_model=schemas.LeadNoteResponse)
def add_lead_note(payload: schemas.LeadNoteCreate, db: Session = Depends(get_db)):
    lead = db.get(models.Lead, payload.lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    note = models.LeadNote(lead_id=lead.id, note=payload.note)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


@app.get("/leads/{lead_id}/notes", response_model=schemas.LeadNoteListResponse)
def list_lead_notes(lead_id: int, db: Session = Depends(get_db)):
    lead = db.get(models.Lead, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    notes = (
        db.execute(select(models.LeadNote).where(models.LeadNote.lead_id == lead.id).order_by(models.LeadNote.created_at))
        .scalars()
        .all()
    )
    return schemas.LeadNoteListResponse(items=notes)


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


@app.get("/dashboard/overview", response_model=schemas.DashboardOverview)
def dashboard_overview(business_id: int, db: Session = Depends(get_db)):
    business = db.get(models.Business, business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")

    posts = db.execute(select(models.ContentPost).where(models.ContentPost.business_id == business.id)).scalars().all()
    leads = db.execute(select(models.Lead).where(models.Lead.business_id == business.id)).scalars().all()

    today = datetime.utcnow().date()
    posts_today = sum(1 for post in posts if post.scheduled_at and post.scheduled_at.date() == today)
    new_leads = sum(1 for lead in leads if lead.pipeline_stage == "new")
    active_conversations = sum(1 for lead in leads if lead.pipeline_stage in {"warm", "hot", "booked"})

    actions = _derive_automation_actions(posts, leads)
    recommendation = _build_dashboard_recommendation(business, posts, leads)

    return schemas.DashboardOverview(
        business_id=business.id,
        posts_scheduled_today=posts_today,
        new_leads=new_leads,
        active_conversations=active_conversations,
        automation_actions=actions,
        recommendation=recommendation,
    )


@app.get("/analytics/performance", response_model=schemas.AnalyticsResponse)
def analytics_performance(business_id: int, db: Session = Depends(get_db)):
    business = db.get(models.Business, business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")

    posts = db.execute(select(models.ContentPost).where(models.ContentPost.business_id == business.id)).scalars().all()
    leads = db.execute(select(models.Lead).where(models.Lead.business_id == business.id)).scalars().all()

    total_posts = len(posts)
    approved_posts = sum(1 for post in posts if post.status == "approved")
    scheduled_posts = sum(1 for post in posts if post.status == "scheduled")
    posted_posts = sum(1 for post in posts if post.status == "posted")
    platform_breakdown: Dict[str, int] = {}
    for post in posts:
        platform_breakdown[post.platform] = platform_breakdown.get(post.platform, 0) + 1

    total_leads = len(leads)
    hot_leads = sum(1 for lead in leads if lead.pipeline_stage == "hot")
    avg_lead_score = round(sum(lead.lead_score for lead in leads) / total_leads, 2) if leads else 0.0
    recommendations = _build_analytics_recommendations(total_posts, scheduled_posts, hot_leads, avg_lead_score)

    return schemas.AnalyticsResponse(
        business_id=business.id,
        total_posts=total_posts,
        approved_posts=approved_posts,
        scheduled_posts=scheduled_posts,
        posted_posts=posted_posts,
        total_leads=total_leads,
        hot_leads=hot_leads,
        avg_lead_score=avg_lead_score,
        platform_breakdown=platform_breakdown,
        funnel_recommendations=recommendations,
    )


@app.get("/analytics/insights", response_model=schemas.AnalyticsInsightResponse)
def analytics_insights(business_id: int, db: Session = Depends(get_db)):
    business = db.get(models.Business, business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")

    posts = db.execute(select(models.ContentPost).where(models.ContentPost.business_id == business.id)).scalars().all()
    leads = db.execute(select(models.Lead).where(models.Lead.business_id == business.id)).scalars().all()
    personas = db.execute(select(models.PersonaProfile).where(models.PersonaProfile.business_id == business.id)).scalars().all()
    assets = db.execute(select(models.ResourceAsset).where(models.ResourceAsset.business_id == business.id)).scalars().all()

    insights = _build_insights(posts, leads)
    gaps = _derive_resource_gaps(assets)
    persona_focus = personas[0].name if personas else None

    return schemas.AnalyticsInsightResponse(
        business_id=business.id,
        insights=insights,
        resource_gaps=gaps,
        persona_focus=persona_focus,
    )


@app.post("/media/assets", response_model=schemas.ResourceAssetResponse)
def create_asset(payload: schemas.ResourceAssetCreate, db: Session = Depends(get_db)):
    business = db.get(models.Business, payload.business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")

    asset = models.ResourceAsset(
        business_id=business.id,
        asset_type=payload.asset_type,
        label=payload.label,
        url=payload.url,
        status=payload.status or "pending",
    )
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset


@app.get("/media/assets", response_model=List[schemas.ResourceAssetResponse])
def list_assets(business_id: int, db: Session = Depends(get_db)):
    assets = (
        db.execute(select(models.ResourceAsset).where(models.ResourceAsset.business_id == business_id))
        .scalars()
        .all()
    )
    return assets


@app.post("/personas/generate", response_model=List[schemas.PersonaResponse])
def generate_personas(payload: schemas.PersonaGenerateRequest, db: Session = Depends(get_db)):
    business = db.get(models.Business, payload.business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")

    personas: List[models.PersonaProfile] = []
    for idx in range(payload.count):
        persona = _build_persona(business, payload.focus, idx)
        db.add(persona)
        personas.append(persona)

    db.commit()
    return personas


@app.get("/personas", response_model=List[schemas.PersonaResponse])
def list_personas(business_id: int, db: Session = Depends(get_db)):
    personas = (
        db.execute(select(models.PersonaProfile).where(models.PersonaProfile.business_id == business_id))
        .scalars()
        .all()
    )
    return personas


@app.post("/dm/flows", response_model=schemas.DMFlowResponse)
def create_dm_flow(payload: schemas.DMFlowCreate, db: Session = Depends(get_db)):
    business = db.get(models.Business, payload.business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")

    flow = models.DMFlow(
        business_id=business.id,
        name=payload.name,
        trigger=payload.trigger,
        script=payload.script,
        status=payload.status or "draft",
    )
    db.add(flow)
    db.commit()
    db.refresh(flow)
    return flow


@app.get("/dm/flows", response_model=List[schemas.DMFlowResponse])
def list_dm_flows(business_id: int, db: Session = Depends(get_db)):
    flows = db.execute(select(models.DMFlow).where(models.DMFlow.business_id == business_id)).scalars().all()
    return flows


@app.post("/dm/flows/{flow_id}/activate", response_model=schemas.DMFlowResponse)
def activate_flow(flow_id: int, db: Session = Depends(get_db)):
    flow = db.get(models.DMFlow, flow_id)
    if not flow:
        raise HTTPException(status_code=404, detail="Flow not found")

    flow.status = "active"
    db.commit()
    db.refresh(flow)
    return flow


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


def _derive_automation_actions(posts: List[models.ContentPost], leads: List[models.Lead]) -> List[str]:
    actions: List[str] = []
    draft_posts = sum(1 for post in posts if post.status == "draft")
    scheduled_posts = sum(1 for post in posts if post.status == "scheduled")
    actions.append(f"{draft_posts} postări în revizie")
    actions.append(f"{scheduled_posts} postări gata de publicare")
    hot_leads = sum(1 for lead in leads if lead.pipeline_stage == "hot")
    actions.append(f"{hot_leads} lead-uri fierbinți așteaptă follow-up")
    return actions


def _build_dashboard_recommendation(
    business: models.Business, posts: List[models.ContentPost], leads: List[models.Lead]
) -> str:
    scheduled_posts = sum(1 for post in posts if post.status == "scheduled")
    hot_leads = sum(1 for lead in leads if lead.pipeline_stage == "hot")
    if scheduled_posts < 3:
        return "Calendarul este subțire. Approvează sau generează noi postări pentru a ține ritmul."
    if hot_leads == 0 and leads:
        return "Nu există lead-uri hot. Mută câteva postări spre dovezi sociale și CTA-uri directe."
    if not leads:
        return "Pornește DM automation pentru a transforma reach-ul în conversații."
    return f"{business.name} respiră bine azi. Continuă ritmul și du lead-urile calde spre call-uri."


def _build_analytics_recommendations(
    total_posts: int, scheduled_posts: int, hot_leads: int, avg_lead_score: float
) -> List[str]:
    recommendations: List[str] = []
    if total_posts == 0:
        recommendations.append("Generează primul val de conținut pentru a popula calendarul.")
    if scheduled_posts < max(2, total_posts // 2):
        recommendations.append("Approvează mai multe postări pentru a avea buffer de o săptămână.")
    if hot_leads == 0:
        recommendations.append("Folosește DM automation pentru follow-up rapid cu lead-urile noi.")
    if avg_lead_score < 40 and total_posts:
        recommendations.append("Încearcă mai multe piese educaționale pentru a încălzi audiența.")
    if not recommendations:
        recommendations.append("Mixul actual funcționează — păstrează-l și testează un format nou săptămâna viitoare.")
    return recommendations


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def _verify_password(password: str, hashed: str) -> bool:
    return _hash_password(password) == hashed


def _issue_token(db: Session, user_id: int) -> models.SessionToken:
    token_value = secrets.token_hex(24)
    expires = datetime.utcnow() + timedelta(hours=12)
    token = models.SessionToken(user_id=user_id, token=token_value, expires_at=expires)
    db.add(token)
    db.commit()
    db.refresh(token)
    return token


def _summarize_onboarding(session: models.OnboardingSession) -> str:
    responses = session.responses or {}
    identity = responses.get("identity", "Brand anonim")
    goals = responses.get("goals", "scopuri deschise")
    tone = responses.get("tone", "calm")
    return f"{identity} urmărește {goals} cu un ton {tone}."


def _build_persona(business: models.Business, focus: Optional[str], idx: int) -> models.PersonaProfile:
    focus_area = focus or business.objective or "growth"
    name = f"Persona {idx + 1}: {focus_area.title()}"
    description = (
        f"{business.name} atrage un profil axat pe {focus_area}. Îi place conținutul sincer și rapid."
    )
    motivations = "Caută un partener stabil și transparență în livrare."
    pain_points = "Nu are timp de agenții lente, vrea răspunsuri concrete."
    preferred_channels = "TikTok, Instagram"
    funnel_stage = "mofu"
    return models.PersonaProfile(
        business_id=business.id,
        name=name,
        description=description,
        motivations=motivations,
        pain_points=pain_points,
        preferred_channels=preferred_channels,
        funnel_stage=funnel_stage,
    )


def _build_insights(posts: List[models.ContentPost], leads: List[models.Lead]) -> List[str]:
    insights: List[str] = []
    if not posts:
        insights.append("Nu există încă postări publicate. Generează un prim val pentru a colecta date.")
    else:
        scheduled = sum(1 for post in posts if post.status == "scheduled")
        insights.append(f"{scheduled} postări sunt deja programate — calendarul respiră.")
    hot_leads = sum(1 for lead in leads if lead.pipeline_stage == "hot")
    if hot_leads:
        insights.append(f"Ai {hot_leads} lead-uri hot. Creează un flow DM scurt pentru închidere rapidă.")
    else:
        insights.append("Nu există lead-uri hot. Pune accent pe social proof și CTA direct.")
    return insights


def _derive_resource_gaps(assets: List[models.ResourceAsset]) -> List[str]:
    if not assets:
        return ["Încarcă logo, poze și testimoniale pentru a ajuta generatorul vizual."]
    asset_types = {asset.asset_type for asset in assets}
    gaps: List[str] = []
    for needed in {"logo", "photo", "video"}:
        if needed not in asset_types:
            gaps.append(f"Lipsește un {needed}. Îl putem genera automat.")
    return gaps or ["Resursele actuale sunt suficiente pentru MVP."]


def _apply_dm_flow(db: Session, business: models.Business, lead: models.Lead, event_type: str) -> None:
    flow = (
        db.execute(
            select(models.DMFlow)
            .where(models.DMFlow.business_id == business.id)
            .where(models.DMFlow.status == "active")
            .where(or_(models.DMFlow.trigger == event_type, models.DMFlow.trigger == "any"))
        )
        .scalars()
        .first()
    )
    if not flow or not flow.script:
        return

    lead.conversation_history.append(
        {
            "author": "ai",
            "message": flow.script[0],
            "timestamp": datetime.utcnow().isoformat(),
        }
    )
    lead.lead_score = min(100, lead.lead_score + 4)
    flow.success_count += 1



