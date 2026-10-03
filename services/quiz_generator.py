from prompts.quiz_prompt import build_quiz_prompt
from services.ai_common import ask_json

def generate_quiz(settings, analysis):
    return ask_json(build_quiz_prompt(settings, analysis))
