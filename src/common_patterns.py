import re

STEP_RE = re.compile(r"^(?:Étape|Etape|Step)\s*:\s*(.*)", re.IGNORECASE)
ACTION_RESULT_RE = re.compile(
    r"^Action\s*:\s*(.*?)\s*(?:R[ée]sultat|Resultat)\s*:?\s*(.*)",
    re.IGNORECASE,
)
ACTION_ONLY_RE = re.compile(r"^Action\s*:\s*(.*)", re.IGNORECASE)
