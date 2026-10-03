from services.ai_common import ask_json
import json

def quality_check(worksheet, analysis, settings):
    prompt = f"""
Review this worksheet against the source.

SOURCE:
{json.dumps(analysis, ensure_ascii=False)}

SETTINGS:
{json.dumps(settings, ensure_ascii=False)}

WORKSHEET:
{json.dumps(worksheet, ensure_ascii=False)}

Return ONLY JSON:
{{
  "source_supported": true,
  "no_duplicates": true,
  "grade_appropriate": true,
  "difficulty_aligned": true,
  "answers_present": true,
  "issues": ["..."]
}}

Only flag real issues. Do not invent problems.
"""
    return ask_json(prompt)
