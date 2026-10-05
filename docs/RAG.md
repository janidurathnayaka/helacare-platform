# Grounded retrieval / pgvector

HelaCare v0.2 uses a layered retrieval strategy:
1. exact multilingual plant aliases,
2. lexical search over verified records,
3. pgvector cosine-distance fallback over verified records.

The bundled embedding function is deterministic and local. It is intentionally not a medical language model and does not generate medical advice. It only ranks curator-controlled records. Answers are still composed from retrieved database fields and source links.

A hosted embedding model can later replace `app/services/embeddings.py` while preserving the `vector(256)` database field (or with a migration to a different dimension).
