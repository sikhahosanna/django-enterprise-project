# Day 5 — Workflow Capstone

**Date:** 23 October 2026

## Objective
Verify the upload-to-result workflow, including validation, event processing, retry/recovery, security boundaries, and test evidence.

## Work Completed
- Added image validation for JPG, JPEG, and PNG uploads.
- Tested rejection of corrupted images and files exceeding the allowed size.
- Verified authenticated profile image upload.
- Tested duplicate-event prevention and invalid event transitions.
- Verified Celery retry and notification recovery after simulated failures and timeouts.
- Tested WebSocket authentication and unauthorized access rejection.

## Workflow
1. Authenticate the upload request.
2. Validate image format, size, and content.
3. Accept valid uploads and reject invalid files.
4. Process workflow events and validate state transitions.
5. Retry eligible transient failures within the retry limit.
6. Record success or reject/report terminal failure.

## Test Evidence

| Test group | Result |
|---|---|
| Image validation | 4 passed |
| Profile image upload API | 2 passed |
| Event processing, retry/recovery, WebSockets | 20 passed |
| Profile and service regression | 64 passed |

These results are from separate test runs. The full regression suite remains to be verified.

## Security Boundaries
- Require authentication for protected image uploads.
- Reject unsupported, oversized, or corrupted images.
- Reject invalid event transitions and unsupported schema versions.
- Verify WebSocket authentication and authorization.
- Keep credentials and secret keys out of source control.

## Troubleshooting
- **Upload rejected:** Check image type, size, and integrity.
- **Authentication failed:** Verify the token and permissions.
- **Event rejected:** Check the upload ID, schema version, and expected state.
- **Task retrying:** Review logs for the underlying transient error.
- **WebSocket denied:** Verify authentication and authorization.

## Remaining Checks
- Run the full regression suite.
- Review changes using `git diff --check`.
- Commit and push the final documentation.
