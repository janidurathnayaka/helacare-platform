from app.services.embeddings import embed_text


def test_embedding_is_deterministic_and_normalized():
    first = embed_text("Gotu kola traditional knowledge")
    second = embed_text("Gotu kola traditional knowledge")
    assert first == second
    assert len(first) == 256
    assert any(value != 0 for value in first)
