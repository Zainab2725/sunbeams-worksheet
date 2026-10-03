import json

def build_worksheet_prompt(settings, analysis, existing_questions=None):
    existing_questions = existing_questions or []
    return f"""
Create a classroom worksheet from the supplied analyzed material.

SETTINGS:
{json.dumps(settings, ensure_ascii=False, indent=2)}

SOURCE ANALYSIS:
{json.dumps(analysis, ensure_ascii=False, indent=2)}

EXISTING QUESTIONS TO AVOID:
{json.dumps(existing_questions, ensure_ascii=False, indent=2)}

Return ONLY valid JSON:
{{
  "title": "...",
  "instructions": "...",
  "questions": [
    {{
      "type": "mcq|fill_blank|true_false|short_answer|matching|application",
      "question": "...",
      "options": ["..."],
      "answer": "...",
      "explanation": "...",
      "marks": 1
    }}
  ]
}}

Rules:
- Generate exactly the requested number of questions.
- Follow the requested question-type distribution.
- Stay within the supplied material and selected topics.
- Match grade and difficulty.
- Avoid duplicate or near-duplicate questions.
- MCQs must have one unambiguous correct answer.
- For fill_blank, use a clear blank.
- For true_false, provide answer as True or False.
- For matching, put pairs in the question data as readable text if needed.
- Application questions must still be answerable from the supplied concepts.
- Use the requested language.
- Do not include markdown fences.
"""
