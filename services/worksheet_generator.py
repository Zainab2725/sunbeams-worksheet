from services.ai_common import ask_json
from prompts.worksheet_prompt import build_worksheet_prompt


def generate_worksheet(
    material_analysis,
    grade,
    subject,
    difficulty,
    language,
    cognitive_level,
    question_count,
    question_types,
    topics,
    teacher_instructions,
):
    """
    Generate a worksheet using Gemini.

    The selected language is passed directly into the prompt so that
    Urdu generation is controlled explicitly.
    """

    if not material_analysis:
        raise ValueError("No learning material has been analyzed.")

    if not language:
        language = "English"

    if not grade:
        grade = "Not specified"

    if not subject:
        subject = "General"

    if not difficulty:
        difficulty = "Medium"

    if not cognitive_level:
        cognitive_level = "Understanding"

    if not question_count:
        question_count = 5

    if not question_types:
        question_types = ["MCQ"]

    if not topics:
        topics = "Use the important topics from the provided material."

    if not teacher_instructions:
        teacher_instructions = "Create a clear and age-appropriate worksheet."

    # Convert material analysis into text that Gemini can understand.
    if isinstance(material_analysis, dict):
        material = "\n".join(
            f"{key}: {value}"
            for key, value in material_analysis.items()
        )
    else:
        material = str(material_analysis)

    prompt = build_worksheet_prompt(
        material=material,
        grade=grade,
        subject=subject,
        difficulty=difficulty,
        language=language,
        cognitive_level=cognitive_level,
        question_count=question_count,
        question_types=question_types,
        topics=topics,
        teacher_instructions=teacher_instructions,
    )

    result = ask_json(prompt)

    if not isinstance(result, dict):
        raise ValueError("Worksheet generator returned an invalid response.")

    if "questions" not in result:
        raise ValueError("Generated worksheet does not contain questions.")

    questions = result["questions"]

    if not isinstance(questions, list):
        raise ValueError("Generated questions are not in the expected format.")

    # Make sure every question has a number.
    for index, question in enumerate(questions, start=1):
        if isinstance(question, dict):
            question.setdefault("number", index)
            question.setdefault("marks", 1)

    result.setdefault(
        "title",
        f"{subject} Worksheet"
    )

    result.setdefault(
        "instructions",
        "Answer all questions carefully."
    )

    return result


def regenerate_question(
    material_analysis,
    original_question,
    grade,
    subject,
    difficulty,
    language,
    cognitive_level,
    question_type,
    teacher_instructions="",
):
    """
    Regenerate one worksheet question while keeping the same
    educational requirements and selected language.
    """

    if isinstance(material_analysis, dict):
        material = "\n".join(
            f"{key}: {value}"
            for key, value in material_analysis.items()
        )
    else:
        material = str(material_analysis)

    if language == "Urdu":
        language_instruction = """
The new question MUST be written completely in proper Urdu script.

Do NOT use Roman Urdu.

Do NOT write:
Photosynthesis kya hai?

Write:
ضیائی تالیف کیا ہے؟

The answer and options must also follow the Urdu requirement.
"""

    elif language == "English + Urdu":
        language_instruction = """
Create the question bilingually.

English:
[English question]

Urdu:
[Urdu question]

The Urdu version MUST use proper Urdu script.
Do NOT use Roman Urdu.
"""

    else:
        language_instruction = """
Write the question completely in English.
"""

    prompt = f"""
You are an expert school worksheet designer for Sunbeams School.

Regenerate ONE question.

Grade:
{grade}

Subject:
{subject}

Difficulty:
{difficulty}

Cognitive Level:
{cognitive_level}

Question Type:
{question_type}

Selected Language:
{language}

{language_instruction}

Learning Material:
{material}

Original Question:
{original_question}

Teacher Instructions:
{teacher_instructions}

Requirements:

1. Create a genuinely different question.
2. Keep it related to the learning material.
3. Keep the same question type.
4. Match the grade level.
5. Match the difficulty.
6. Match the cognitive level.
7. Make sure the answer is correct.
8. Do not reveal unsupported information.
9. Follow the language requirement exactly.

Return ONLY valid JSON.

Return:

{{
    "number": 1,
    "type": "{question_type}",
    "question": "New question",
    "options": [],
    "answer": "Correct answer",
    "marks": 1
}}
"""

    result = ask_json(prompt)

    if not isinstance(result, dict):
        raise ValueError("Question regeneration returned invalid data.")

    result.setdefault("number", 1)
    result.setdefault("marks", 1)
    result.setdefault("options", [])

    return result
