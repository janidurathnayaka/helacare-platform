# Admin / Curator Console

The curator console is available at `/admin/login` and uses JWT authentication from the FastAPI backend.

Capabilities:
- Plants: add, edit, verify and delete curated records.
- Sources: maintain evidence URLs and verification status.
- Practitioner Reviews: record qualified human review status and comments.
- User Feedback: review and resolve helpful/not-helpful feedback from chat.
- Safety Flags: urgent red-flag chats create reviewable safety events.
- Analytics: language, triage and recent-query summaries.
- Audit Logs: admin mutations are recorded for accountability.
- RAG Index: rebuild deterministic 256-dimension pgvector embeddings for verified retrieval.

The included local admin credentials are development defaults only. Change them before any deployment.
