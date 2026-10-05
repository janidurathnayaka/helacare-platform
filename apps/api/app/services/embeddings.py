"""Small deterministic embedding helper.

This keeps the project self-contained for local development. It is not a clinical
language model. It only creates vectors used to rank already-curated records.
A hosted embedding model can replace this function later without changing the DB schema.
"""

import hashlib
import math
import re
import unicodedata

DIMENSIONS = 256


def _tokens(text: str) -> list[str]:
    normalized = unicodedata.normalize("NFC", text).casefold()
    return re.findall(r"[\w\u0D80-\u0DFF]+", normalized, flags=re.UNICODE)


def embed_text(text: str, dimensions: int = DIMENSIONS) -> list[float]:
    vector = [0.0] * dimensions
    for token in _tokens(text):
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        idx = int.from_bytes(digest[:4], "big") % dimensions
        sign = 1.0 if digest[4] % 2 == 0 else -1.0
        vector[idx] += sign
    norm = math.sqrt(sum(value * value for value in vector)) or 1.0
    return [value / norm for value in vector]


def plant_embedding_text(plant) -> str:
    return " ".join(
        str(value)
        for value in (
            plant.sinhala_name,
            plant.common_name,
            plant.scientific_name,
            plant.part_used,
            plant.traditional_use,
            plant.preparation,
            plant.safety_note,
        )
        if value
    )
