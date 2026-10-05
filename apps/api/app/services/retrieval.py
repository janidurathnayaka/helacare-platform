import re
import unicodedata

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.plant import Plant
from app.services.embeddings import embed_text

STOP_WORDS = {"tell", "me", "about", "please", "what", "is", "are", "the", "a", "an", "can", "you", "explain", "give", "information", "info"}

PLANT_ALIASES = {
    "gotukola": ["gotukola", "gotu kola", "ගොටුකොළ", "ගොටුකොල"],
    "koththamalli": ["koththamalli", "kothamalli", "coriander", "කොත්තමල්ලි", "කොතමල්ලි"],
    "inguru": ["inguru", "ginger", "ඉඟුරු", "ඉගුරු"],
    "kaha": ["kaha", "turmeric", "කහ"],
    "iramusu": ["iramusu", "ඉරමුසු"],
    "polpala": ["polpala", "පොල්පලා"],
    "mukunuwenna": ["mukunuwenna", "මුකුණුවැන්න", "මුකුනුවැන්න"],
    "hathawariya": ["hathawariya", "hathawaria", "හාතාවාරිය"],
    "komarika": ["komarika", "aloe vera", "කොමාරිකා"],
    "ranawara": ["ranawara", "රණවරා"],
    "kathurumurunga": ["kathurumurunga", "කතුරුමුරුංගා"],
    "kohomba": ["kohomba", "neem", "කොහොඹ"],
    "veniwelgata": ["veniwelgata", "veniwelgeta", "වෙනිවැල්ගැට"],
    "murunga": ["murunga", "moringa", "මුරුංගා"],
    "bulath": ["bulath", "betel", "බුලත්"],
    "beli": ["beli", "bael", "බෙලි"],
    "dehi": ["dehi", "lime", "දෙහි"],
    "karapincha": ["karapincha", "curry leaf", "කරපිංචා", "කරපින්චා"],
    "kohila": ["kohila", "කොහිල"],
    "sudulunu": ["sudulunu", "garlic", "සුදුලූනු", "සුදු ලූනු"],
}


def normalize_text(value: str) -> str:
    value = unicodedata.normalize("NFC", value).casefold()
    return "".join(char for char in value if unicodedata.category(char)[0] in {"L", "M", "N"})


def resolve_alias(query: str) -> str | None:
    nq = normalize_text(query)
    for canonical, aliases in PLANT_ALIASES.items():
        if any(normalize_text(alias) in nq for alias in aliases):
            return canonical
    return None


def extract_search_terms(query: str) -> list[str]:
    cleaned = re.sub(r"[^\w\s]", " ", query.lower(), flags=re.UNICODE)
    useful = [word for word in cleaned.split() if word not in STOP_WORDS and len(word) >= 2]
    return useful or [query.strip().lower()]


async def retrieve_verified_plants(db: AsyncSession, query: str, limit: int = 5) -> list[Plant]:
    canonical = resolve_alias(query)
    if canonical:
        pattern = f"%{canonical}%"
        stmt = select(Plant).where(
            Plant.is_verified.is_(True),
            or_(
                func.replace(func.lower(Plant.sinhala_name), " ", "").like(pattern),
                func.replace(func.lower(Plant.common_name), " ", "").like(pattern),
                func.replace(func.lower(Plant.scientific_name), " ", "").like(pattern),
            ),
        ).limit(limit)
        plants = list((await db.execute(stmt)).scalars().all())
        if plants:
            return plants

    terms = extract_search_terms(query)
    conditions = []
    for term in terms:
        pattern = f"%{term}%"
        compact = f"%{term.replace(' ', '')}%"
        conditions.extend([
            Plant.sinhala_name.ilike(pattern), Plant.common_name.ilike(pattern), Plant.scientific_name.ilike(pattern),
            Plant.traditional_use.ilike(pattern), Plant.part_used.ilike(pattern),
            func.replace(func.lower(Plant.sinhala_name), " ", "").like(compact),
            func.replace(func.lower(Plant.common_name), " ", "").like(compact),
        ])
    lexical = select(Plant).where(Plant.is_verified.is_(True), or_(*conditions)).limit(limit)
    plants = list((await db.execute(lexical)).scalars().all())
    if plants:
        return plants

    # pgvector fallback: ranks only curated, verified records that have embeddings.
    query_vector = embed_text(query)
    vector_stmt = (
        select(Plant)
        .where(Plant.is_verified.is_(True), Plant.embedding.is_not(None))
        .order_by(Plant.embedding.cosine_distance(query_vector))
        .limit(min(limit, 3))
    )
    return list((await db.execute(vector_stmt)).scalars().all())
