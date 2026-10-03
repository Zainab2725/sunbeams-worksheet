import json

def build_flashcards_prompt(settings, analysis):
    return f"""
Create concise educational flashcards from this source material.

Settings:
{json.dumps(settings, ensure_ascii=False)}

Source:
{json.dumps(analysis, ensure_ascii=False)}

Return ONLY JSON:
{{"title":"...", "cards":[{{"front":"...","back":"..."}}]}}

Rules:
- Create exactly {settings.get("count", 10)} cards.
- Cards must be directly supported by the source.
- Keep fronts and backs concise.
- Use the requested language.
"""
