from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import JSON, Column, DateTime, Enum, ForeignKey, Integer, String, Text
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


class LeadNote(Base):
    __tablename__ = "lead_notes"

    id = Column(Integer, primary_key=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)
    note = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class BrainMemory(Base):
    __tablename__ = "brain_memory"

    id = Column(Integer, primary_key=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)
    label = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

