from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    name: str
    email: str


class BusinessBase(BaseModel):
    name: str
    industry: Optional[str] = None
    objective: Optional[str] = None
    brand_tone: Optional[str] = None
    resources_status: Optional[str] = None
    product_description: Optional[str] = None


class BusinessCreate(BusinessBase):
    owner_name: str
    owner_email: str


class BusinessResponse(BusinessBase):
    id: int

    class Config:
        orm_mode = True


class StrategyResponse(BaseModel):
    id: int
    budget: int
    posting_frequency: str
    platforms: dict
    content_plan: dict
    created_at: datetime

    class Config:
        orm_mode = True


class ContentGenerateRequest(BaseModel):
    business_id: int
    platform: str
    content_type: str = Field(..., description="video, carousel, story, etc.")
    topic: str
    persona: Optional[str] = None
    pillar: Optional[str] = None
    funnel_stage: Optional[str] = None


class ContentResponse(BaseModel):
    id: int
    platform: str
    text: str
    media_prompt: Optional[str]
    status: str
    scheduled_at: Optional[datetime]
    persona: Optional[str]
    pillar: Optional[str]
    funnel_stage: Optional[str]

    class Config:
        orm_mode = True


class ContentStatusUpdate(BaseModel):
    post_id: int
    status: str


class SchedulePostRequest(BaseModel):
    post_id: int
    scheduled_at: datetime


class DmTriggerRequest(BaseModel):
    business_id: int
    handle: str
    source: str
    event_type: str
    message: Optional[str] = None


class DmSendRequest(BaseModel):
    lead_id: int
    message: str
    author: str = Field(..., description="ai or user")


class PipelineLead(BaseModel):
    id: int
    name: str
    pipeline_stage: str
    lead_score: int
    source: str
    conversation_history: list

    class Config:
        orm_mode = True


class BrainQueryRequest(BaseModel):
    business_id: int
    query: str


class BrainQueryResponse(BaseModel):
    answer: str
    references: List[str] = Field(default_factory=list)


class AnalysisResponse(BaseModel):
    business_id: int
    summary: str
    recommendations: List[str]

