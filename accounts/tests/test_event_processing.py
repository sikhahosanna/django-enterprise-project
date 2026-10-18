from django.test import SimpleTestCase

from accounts.services.event_processing import EventProcessor, UploadState


class EventProcessorTests(SimpleTestCase):
    def setUp(self):
        self.processor = EventProcessor()
        self.processor.register("upload-1")
        self.processor.stage("upload-1")

    def event(self, event_id, event_type, attempt=1):
        return {
            "schema_version": "1.0",
            "event_id": event_id,
            "event_type": event_type,
            "correlation_id": "req-123",
            "upload_id": "upload-1",
            "occurred_at": "2026-10-19T10:00:00Z",
            "status": event_type,
            "attempt": attempt,
        }

    def test_successful_upload_lifecycle(self):
        events = [
            ("evt-1", "upload.started"),
            ("evt-2", "upload.accepted"),
            ("evt-3", "upload.processing.started"),
            ("evt-4", "upload.processing.completed"),
        ]

        for event_id, event_type in events:
            self.processor.handle(self.event(event_id, event_type))

        self.assertEqual(
            self.processor.states["upload-1"],
            UploadState.COMPLETED,
        )

    def test_duplicate_event_is_not_processed_twice(self):
        payload = self.event("evt-duplicate", "upload.started")

        first = self.processor.handle(payload)
        second = self.processor.handle(payload)

        self.assertFalse(first["duplicate"])
        self.assertTrue(second["duplicate"])
        self.assertEqual(
            self.processor.states["upload-1"],
            UploadState.UPLOADING,
        )

    def test_invalid_transition_is_rejected(self):
        payload = self.event("evt-invalid", "upload.accepted")

        with self.assertRaises(ValueError):
            self.processor.handle(payload)

        self.assertEqual(
            self.processor.states["upload-1"],
            UploadState.STAGED,
        )

    def test_processing_failure_retries_then_fails_at_limit(self):
        self.processor.handle(
            self.event("evt-start", "upload.started")
        )
        self.processor.handle(
            self.event("evt-accepted", "upload.accepted")
        )

        for attempt in (1, 2):
            self.processor.handle(
                self.event(
                    f"evt-processing-{attempt}",
                    "upload.processing.started",
                    attempt,
                )
            )
            result = self.processor.handle(
                self.event(
                    f"evt-failed-{attempt}",
                    "upload.processing.failed",
                    attempt,
                )
            )
            self.assertEqual(result["state"], UploadState.RETRY_PENDING.value)

        self.processor.handle(
            self.event("evt-processing-3", "upload.processing.started", 3)
        )
        result = self.processor.handle(
            self.event("evt-failed-3", "upload.processing.failed", 3)
        )

        self.assertEqual(result["state"], UploadState.FAILED.value)

    def test_unknown_upload_is_rejected(self):
        payload = self.event("evt-unknown", "upload.started")
        payload["upload_id"] = "missing-upload"

        with self.assertRaises(ValueError):
            self.processor.handle(payload)

    def test_unsupported_schema_version_is_rejected(self):
        payload = self.event("evt-version", "upload.started")
        payload["schema_version"] = "99.0"

        with self.assertRaises(ValueError):
            self.processor.handle(payload)

    def test_invalid_attempt_is_rejected(self):
        payload = self.event("evt-attempt", "upload.started")
        payload["attempt"] = 0

        with self.assertRaises(ValueError):
            self.processor.handle(payload)
