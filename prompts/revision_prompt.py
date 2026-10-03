import json

def build_revision_prompt(settings, analysis):
    return f"""
Create concise revision notes from this source.

Settings:
{json.dumps(settings, ensure_ascii=False)}

Source:
{json.dumps(analysis, ensure_ascii=False)}

Return ONLY JSON:
{{
  "title":"...",
  "summary":"...",
  "key_concepts":["..."],
  "vocabulary":[{{"term":"...","meaning":"..."}}],
  "quick_questions":["..."]
}}

Use only source-supported information and match the selected grade/language.
"""
