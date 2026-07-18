from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, HttpUrl
from app.domain.enums import SourceTier, AccessStatus, NoticeStage, RunStatus

class QueryIntent(BaseModel):
    raw_query: str
    topic: str
    synonyms: list[str] = []
    regions: list[str] = []
    start_at: datetime
    end_at: datetime
    stages: list[NoticeStage] = []
    schedule_cron: Optional[str] = None
    schedule_text: Optional[str] = None
    timezone: str = "Asia/Shanghai"
    confidence: float = 0.8
    clarification_needed: bool = False
    clarification_questions: list[str] = []

class Attachment(BaseModel):
    name: str
    url: str
    status: str = "available"
    failure_reason: Optional[str] = None

class Evidence(BaseModel):
    source_url: str
    quote: str
    selector: Optional[str] = None
    captured_at: datetime

class Notice(BaseModel):
    id: str
    title: str
    published_at: datetime
    region: str
    buyer: Optional[str] = None
    agency: Optional[str] = None
    project_no: Optional[str] = None
    notice_stage: NoticeStage = NoticeStage.UNKNOWN
    procurement_method: Optional[str] = None
    budget: Optional[str] = None
    deadline: Optional[datetime] = None
    source_url: str
    source_name: str
    source_tier: SourceTier
    access_status: AccessStatus
    core_content: str
    attachments: list[Attachment] = []
    evidence: list[Evidence] = []
    matched_terms: list[str] = []
    relevance_score: float = 0
    relevance_reason: str = ""
    content_hash: str = ""
    duplicate_of: Optional[str] = None
    related_project_id: Optional[str] = None
    restricted_fields: list[str] = []

class SourcePlan(BaseModel):
    source_id: str
    source_name: str
    tier: SourceTier
    access_status: AccessStatus
    mode: str
    note: str

class RunRequest(BaseModel):
    query: str = Field(..., min_length=2)
    include_sources: list[str] | None = None

class RunResult(BaseModel):
    run_id: str
    status: RunStatus
    intent: QueryIntent
    source_plan: list[SourcePlan]
    notices: list[Notice]
    duplicate_count: int
    restricted_count: int
    report_filename: Optional[str] = None
    report_download_url: Optional[str] = None
    messages: list[str] = []

class SourceHealth(BaseModel):
    source_id: str
    source_name: str
    tier: SourceTier
    access_status: AccessStatus
    healthy: bool
    mode: str
    note: str
