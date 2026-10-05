from dataclasses import dataclass

@dataclass(frozen=True)
class SafetyDecision:
    urgent: bool
    matched_terms: tuple[str, ...]

RED_FLAG_TERMS = (
    "difficulty breathing",
    "cannot breathe",
    "can't breathe",
    "severe chest pain",
    "unconscious",
    "fainted and not waking",
    "seizure",
    "heavy bleeding",
    "suicidal",
    "හුස්ම ගන්න අමාරු",
    "හුස්ම ගන්න බැහැ",
    "තද පපුවේ වේදනාව",
    "සිහි නැති",
    "අධික රුධිර වහනය",
)

def evaluate_safety(message: str) -> SafetyDecision:
    normalized = " ".join(message.lower().split())
    matched = tuple(term for term in RED_FLAG_TERMS if term in normalized)
    return SafetyDecision(urgent=bool(matched), matched_terms=matched)
