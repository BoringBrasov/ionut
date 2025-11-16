from __future__ import annotations

from datetime import datetime, timedelta

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=True)
    role = Column(String, default="owner", nullable=False)

    businesses = relationship("Business", back_populates="owner")


class Business(Base):
    __tablename__ = "businesses"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    industry = Column(String, nullable=True)
    objective = Column(String, nullable=True)
    brand_tone = Column(String, nullable=True)
    resources_status = Column(String, nullable=True)
    product_description = Column(Text, nullable=True)

    owner = relationship("User", back_populates="businesses")
    strategies = relationship("Strategy", back_populates="business")
    content_posts = relationship("ContentPost", back_populates="business")
    leads = relationship("Lead", back_populates="business")
    onboarding_sessions = relationship("OnboardingSession", back_populates="business")
    resource_assets = relationship("ResourceAsset", back_populates="business")
    personas = relationship("PersonaProfile", back_populates="business")
    dm_flows = relationship("DMFlow", back_populates="business")


class Strategy(Base):
    __tablename__ = "strategy"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)
    content_plan = Column(JSON, nullable=False)
    platforms = Column(JSON, nullable=False)
    posting_frequency = Column(String, nullable=False)
    budget = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    business = relationship("Business", back_populates="strategies")


class ContentPost(Base):
    __tablename__ = "content_posts"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)
    platform = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    media_prompt = Column(Text, nullable=True)
    status = Column(String, default="draft", nullable=False)
    scheduled_at = Column(DateTime, nullable=True)
    persona = Column(String, nullable=True)
    pillar = Column(String, nullable=True)
    funnel_stage = Column(String, nullable=True)
    feedback_reason = Column(String, nullable=True)
    feedback_notes = Column(Text, nullable=True)
    performance_score = Column(Integer, default=0)

    business = relationship("Business", back_populates="content_posts")


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)
    name = Column(String, nullable=False)
    source = Column(String, nullable=False)
    pipeline_stage = Column(
        Enum(
            "new",
            "cold",
            "warm",
            "hot",
            "booked",
            "no_show",
            "sale",
            "lost",
            name="pipeline_stage",
        ),
        default="new",
        nullable=False,
    )
    conversation_history = Column(JSON, default=list)
    lead_score = Column(Integer, default=10)

    business = relationship("Business", back_populates="leads")
    notes = relationship("LeadNote", back_populates="lead")


class LeadNote(Base):
    __tablename__ = "lead_notes"

    id = Column(Integer, primary_key=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)
    note = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    lead = relationship("Lead", back_populates="notes")


class BrainMemory(Base):
    __tablename__ = "brain_memory"

    id = Column(Integer, primary_key=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)
    label = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class SessionToken(Base):
    __tablename__ = "session_tokens"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)

    user = relationship("User")


class OnboardingSession(Base):
    __tablename__ = "onboarding_sessions"

    id = Column(Integer, primary_key=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)
    current_step = Column(Integer, default=1)
    total_steps = Column(Integer, default=7)
    responses = Column(JSON, default=dict)
    completed = Column(Boolean, default=False)
    questions_answered = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    business = relationship("Business", back_populates="onboarding_sessions")


class ResourceAsset(Base):
    __tablename__ = "resource_assets"

    id = Column(Integer, primary_key=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)
    asset_type = Column(String, nullable=False)
    label = Column(String, nullable=False)
    url = Column(String, nullable=True)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)

    business = relationship("Business", back_populates="resource_assets")


class PersonaProfile(Base):
    __tablename__ = "persona_profiles"

    id = Column(Integer, primary_key=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    motivations = Column(Text, nullable=True)
    pain_points = Column(Text, nullable=True)
    preferred_channels = Column(String, nullable=True)
    funnel_stage = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    business = relationship("Business", back_populates="personas")


class DMFlow(Base):
    __tablename__ = "dm_flows"

    id = Column(Integer, primary_key=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)
    name = Column(String, nullable=False)
    trigger = Column(String, nullable=False)
    script = Column(JSON, default=list)
    status = Column(String, default="draft")
    success_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    business = relationship("Business", back_populates="dm_flows")

