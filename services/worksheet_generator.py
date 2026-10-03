from prompts.worksheet_prompt import build_worksheet_prompt
from services.ai_common import ask_json
from utils.validators import normalize_worksheet

def generate_worksheet(settings, analysis, existing_questions=None):
    prompt = build_worksheet_prompt(settings, analysis, existing_questions)
    return normalize_worksheet(ask_json(prompt))

def regenerate_question(settings, analysis, question, all_questions):
    focused = dict(settings)
    focused["count"] = 1
    prompt = build_worksheet_prompt(
        focused,
        analysis,
        existing_questions=[q for q in all_questions if q.get("id") != question.get("id")]
    )
    result = normalize_worksheet(ask_json(prompt))
    return result["questions"][0] if result["questions"] else None
