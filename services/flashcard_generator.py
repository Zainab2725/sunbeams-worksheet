from prompts.flashcards_prompt import build_flashcards_prompt
from services.ai_common import ask_json

def generate_flashcards(settings, analysis):
    return ask_json(build_flashcards_prompt(settings, analysis))
