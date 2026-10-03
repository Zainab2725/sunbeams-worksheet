from prompts.material_analysis import build_material_prompt
from services.ai_common import ask_json

def analyze_material(images, grade, subject):
    prompt = build_material_prompt(grade, subject)
    return ask_json(prompt, images=images)
