import json

def build_quiz_prompt(settings, analysis):
    return f"""
Create an interactive multiple-choice quiz from the source material.

Settings:
{json.dumps(settings, ensure_ascii=False)}

Source:
{json.dumps(analysis, ensure_ascii=False)}

Return ONLY JSON:
{{"title":"...", "questions":[
  {{"question":"...","options":["...","...","...","..."],"answer_index":0,"explanation":"..."}}
]}}

Rules:
- Exactly {settings.get("count", 10)} questions.
- One unambiguous correct option.
- Stay within the source.
- Match grade and difficulty.
"""
