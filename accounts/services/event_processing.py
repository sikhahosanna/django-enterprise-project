"""Versioned upload-event contract and lifecycle state machine."""

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class UploadState(StrEnum):
    SELECTED = "selected"
    STAGED = "staged"
    UPLOADING = "uploading"
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    RETRY_PENDING = "retry_pending"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(frozen=True)
class EventEnvelope:
    schema_version: str
    event_id: str
    event_type: str
    correlation_id: str
    upload_id: str
    occurred_at: str
    status: str
    attempt: int
    error: str | None = None

    EVENT_TYPES = {
        "upload.started",
        "upload.accepted",
        "upload.processing.started",
        "upload.processing.completed",
        "upload.processing.failed",
        "upload.retry.scheduled",
    }

    @classmethod
    def from_dict(cls, payload):
        if not isinstance(payload, dict):
            raise ValueError("Event payload must be an object.")

        required = (
            "schema_version", "event_id", "event_type",
            "correlation_id", "upload_id", "occurred_at",
            "status", "attempt",
        )
        missing = [key for key in required if key not in payload]
        if missing:
            raise ValueError(f"Missing event fields: {', '.join(missing)}")

        for key in required:
            if key != "attempt" and (
                not isinstance(payload[key], str) or not payload[key].strip()
            ):
                raise ValueError(f"{key} must be a non-empty string.")

        if payload["schema_version"] != "1.0":
            raise ValueError("Unsupported event schema version.")

        if payload["event_type"] not in cls.EVENT_TYPES:
            raise ValueError("Unknown event type.")

        try:
            datetime.fromisoformat(payload["occurred_at"].replace("Z", "+00:00"))
        except (ValueError, TypeError):
            raise ValueError("occurred_at must be an ISO-8601 timestamp.") from None

        attempt = payload["attempt"]
        if isinstance(attempt, bool) or not isinstance(attempt, int) or attempt < 1:
            raise ValueError("attempt must be a positive integer.")

        return cls(**{key: payload.get(key) for key in (
            *required, "error"
        )})


class EventProcessor:
    """In-memory reference processor; persistence belongs to a durable adapter."""

    MAX_ATTEMPTS = 3

    ALLOWED_TRANSITIONS = {
        UploadState.SELECTED: {UploadState.STAGED},
        UploadState.STAGED: {UploadState.UPLOADING},
        UploadState.UPLOADING: {
            UploadState.UPLOADED, UploadState.RETRY_PENDING, UploadState.FAILED,
        },
        UploadState.UPLOADED: {UploadState.PROCESSING},
        UploadState.PROCESSING: {
            UploadState.COMPLETED, UploadState.RETRY_PENDING, UploadState.FAILED,
        },
        UploadState.RETRY_PENDING: {
            UploadState.UPLOADING, UploadState.PROCESSING, UploadState.FAILED,
        },
        UploadState.COMPLETED: set(),
        UploadState.FAILED: set(),
    }

    def __init__(self):
        self.states = {}
        self.processed_event_ids = set()
        self.attempts = {}

    def register(self, upload_id):
        if not isinstance(upload_id, str) or not upload_id.strip():
            raise ValueError("upload_id must be a non-empty string.")
        if upload_id in self.states:
            raise ValueError("Upload already registered.")
        self.states[upload_id] = UploadState.SELECTED
        self.attempts[upload_id] = 0
        return self.states[upload_id]

    def stage(self, upload_id):
        self._transition(upload_id, UploadState.STAGED)
        return self.states[upload_id]

    def _transition(self, upload_id, target):
        if upload_id not in self.states:
            raise ValueError("Unknown upload_id.")
        current = self.states[upload_id]
        if target not in self.ALLOWED_TRANSITIONS[current]:
            raise ValueError(f"Invalid transition: {current.value} -> {target.value}")
        self.states[upload_id] = target

    def handle(self, payload):
        event = EventEnvelope.from_dict(payload)

        if event.event_id in self.processed_event_ids:
            return {
                "duplicate": True,
                "upload_id": event.upload_id,
                "state": self.states.get(event.upload_id),
            }

        if event.upload_id not in self.states:
            raise ValueError("Unknown upload_id.")

        current = self.states[event.upload_id]
        kind = event.event_type

        if kind == "upload.retry.scheduled":
            if current != UploadState.RETRY_PENDING:
                raise ValueError("Retry can only be scheduled while retry is pending.")
            target = current
        elif kind == "upload.started":
            target = UploadState.UPLOADING
        elif kind == "upload.accepted":
            target = UploadState.UPLOADED
        elif kind == "upload.processing.started":
            target = UploadState.PROCESSING
        elif kind == "upload.processing.completed":
            target = UploadState.COMPLETED
        elif kind == "upload.processing.failed":
            if current != UploadState.PROCESSING:
                raise ValueError("Processing failure requires processing state.")
            target = (
                UploadState.RETRY_PENDING
                if event.attempt < self.MAX_ATTEMPTS
                else UploadState.FAILED
            )
        else:
            raise ValueError("Unsupported event.")

        if target != current:
            self._transition(event.upload_id, target)

        self.attempts[event.upload_id] = max(
            self.attempts[event.upload_id], event.attempt
        )
        self.processed_event_ids.add(event.event_id)

        return {
            "duplicate": False,
            "upload_id": event.upload_id,
            "state": self.states[event.upload_id].value,
        }
