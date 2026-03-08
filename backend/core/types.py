from enum import StrEnum


class JobState(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class CalcLevel(StrEnum):
    RAW = "raw"
    VALIDATED = "validated"
    INTERMEDIATE = "intermediate"
    POLICY_SUMMARY = "policy_summary"
    FINAL = "final"
