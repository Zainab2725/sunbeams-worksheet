from prompts.revision_prompt import build_revision_prompt
from services.ai_common import ask_json

def generate_revision_notes(settings, analysis):
    return ask_json(build_revision_prompt(settings, analysis))
