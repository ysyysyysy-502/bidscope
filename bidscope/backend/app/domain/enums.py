from enum import Enum

class SourceTier(str, Enum):
    T0_CANONICAL = "T0_CANONICAL"
    T1_AUTHORITY = "T1_AUTHORITY"
    T2_DISCOVERY = "T2_DISCOVERY"
    T3_SIGNAL = "T3_SIGNAL"

class AccessStatus(str, Enum):
    PUBLIC_FREE = "public_free"
    ACCOUNT_REQUIRED = "account_required"
    AUTHORIZED_ACCOUNT = "authorized_account"
    LICENSED_PAID = "licensed_paid"
    ACCESS_RESTRICTED = "access_restricted"
    AUTOMATION_PROHIBITED = "automation_prohibited"

class NoticeStage(str, Enum):
    PRE_MARKET = "PRE_MARKET"
    QUALIFICATION = "QUALIFICATION"
    PROCUREMENT = "PROCUREMENT"
    CHANGE = "CHANGE"
    TERMINATION = "TERMINATION"
    EVALUATION = "EVALUATION"
    AWARD = "AWARD"
    CONTRACT = "CONTRACT"
    ACCEPTANCE = "ACCEPTANCE"
    UNKNOWN = "UNKNOWN"

class RunStatus(str, Enum):
    PARSING = "PARSING"
    PLAN_READY = "PLAN_READY"
    RUNNING = "RUNNING"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    COMPLETED = "COMPLETED"
    PARTIAL_FAILED = "PARTIAL_FAILED"
    FAILED = "FAILED"
