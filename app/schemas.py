from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional

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
    feedback_reason: Optional[str]
    feedback_notes: Optional[str]
    performance_score: int

    class Config:
        orm_mode = True


class ContentStatusUpdate(BaseModel):
    post_id: int
    status: str


class SchedulePostRequest(BaseModel):
    post_id: int
    scheduled_at: datetime


class ContentFeedbackRequest(BaseModel):
    post_id: int
    decision: str = Field(..., description="accept | modify | reject")
    reason: Optional[str] = None
    notes: Optional[str] = None


class ContentCalendarEntry(ContentResponse):
    scheduled_day: Optional[datetime]


class ContentBatchRequest(BaseModel):
    business_id: int
    platforms: List[str]
    topics: List[str]
    persona: Optional[str] = None
    pillar: Optional[str] = None
    funnel_stage: Optional[str] = None


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


class LeadStageUpdate(BaseModel):
    lead_id: int
    stage: str


class LeadNoteCreate(BaseModel):
    lead_id: int
    note: str


class LeadNoteResponse(BaseModel):
    id: int
    lead_id: int
    note: str
    created_at: datetime

    class Config:
        orm_mode = True


class LeadNoteListResponse(BaseModel):
    items: List[LeadNoteResponse]


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


class DashboardOverview(BaseModel):
    business_id: int
    posts_scheduled_today: int
    new_leads: int
    active_conversations: int
    automation_actions: List[str]
    recommendation: str


class AnalyticsResponse(BaseModel):
    business_id: int
    total_posts: int
    approved_posts: int
    scheduled_posts: int
    posted_posts: int
    total_leads: int
    hot_leads: int
    avg_lead_score: float
    platform_breakdown: dict
    funnel_recommendations: List[str]


class AnalyticsInsightResponse(BaseModel):
    business_id: int
    insights: List[str]
    resource_gaps: List[str]
    persona_focus: Optional[str] = None


class SignUpRequest(BaseModel):
    name: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class AuthResponse(BaseModel):
    user_id: int
    token: str
    expires_at: datetime


class OnboardingSessionCreate(BaseModel):
    business_id: int
    total_steps: int = 7


class OnboardingSessionResponse(BaseModel):
    id: int
    business_id: int
    current_step: int
    total_steps: int
    responses: Dict[str, str]
    completed: bool
    questions_answered: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class OnboardingAnswerRequest(BaseModel):
    step_key: str
    answer: str
    step_index: int
    is_final: bool = False


class OnboardingQuestion(BaseModel):
    key: str
    prompt: str
    qtype: str
    options: List[str]


class ResourceAssetCreate(BaseModel):
    business_id: int
    asset_type: str
    label: str
    url: Optional[str] = None
    status: Optional[str] = "pending"


class ResourceAssetResponse(BaseModel):
    id: int
    business_id: int
    asset_type: str
    label: str
    url: Optional[str]
    status: str
    created_at: datetime

    class Config:
        orm_mode = True


class PersonaGenerateRequest(BaseModel):
    business_id: int
    count: int = 2
    focus: Optional[str] = None


class PersonaResponse(BaseModel):
    id: int
    business_id: int
    name: str
    description: str
    motivations: Optional[str]
    pain_points: Optional[str]
    preferred_channels: Optional[str]
    funnel_stage: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True


class DMFlowCreate(BaseModel):
    business_id: int
    name: str
    trigger: str
    script: List[str]
    status: Optional[str] = "draft"


class DMFlowResponse(BaseModel):
    id: int
    business_id: int
    name: str
    trigger: str
    script: List[str]
    status: str
    success_count: int
    created_at: datetime

    class Config:
        orm_mode = True


class AutoScheduleRequest(BaseModel):
    business_id: int
    start_date: Optional[datetime] = None
    interval_minutes: int = 180

