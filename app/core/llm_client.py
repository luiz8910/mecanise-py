import os
import json
from pathlib import Path
from typing import Any, Dict, Optional

from openai import OpenAI

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Carrega o JSON Schema a partir do arquivo para evitar duplicação
_SCHEMA_PATH = (
    Path(__file__)
    .resolve()
    .parents[1]
    / "domain"
    / "schemas"
    / "part_request.schema.json"
)
with _SCHEMA_PATH.open("r", encoding="utf-8") as f:
    JSON_SCHEMA: Dict[str, Any] = json.load(f)

SYSTEM = """You are the intake AI for Mecanice.
Extract a PartRequestCreate JSON from the user's Portuguese text.
- Infer category/subcategory when obvious (e.g., 'pastilha' -> Freios / Pastilha de freio).
- Vehicle may be plate OR brand/model/year; fill known fields, omit unknowns.
- Normalize urgency to: ALTA, NORMAL, ORCAMENTO.
Return ONLY JSON that validates against the provided schema.
"""


def extract_part_request(text: str, hints: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    hint_str = f"\nHINTS: {json.dumps(hints, ensure_ascii=False)}" if hints else ""
    prompt = f"{SYSTEM}\nUSER: {text}{hint_str}"

    resp = client.responses.create(
        model=MODEL,
        input=prompt,
        response_format={
            "type": "json_schema",
            "json_schema": {"name": "PartRequestCreate", "schema": JSON_SCHEMA, "strict": True}
        },
        temperature=0
    )
    return json.loads(resp.output_text)
