def build_worksheet_prompt(
    material,
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
    language_rules = {
        "English": """
Generate the complete worksheet in English.
All questions, instructions, options, explanations, and answers must be in English.
""",

        "Urdu": """
Generate the COMPLETE worksheet in Urdu.

STRICT URDU REQUIREMENTS:
- Write the actual worksheet content in Urdu script.
- Use natural, grammatically correct Urdu.
- Do NOT use Roman Urdu.
- Do NOT write Urdu using English letters.
- Questions must be in Urdu.
- Instructions must be in Urdu.
- Multiple-choice options must be in Urdu where appropriate.
- Answers must be in Urdu where appropriate.
- Explanations must be in Urdu where appropriate.
- Keep numbers, mathematical symbols, formulas, units, and scientific notation where appropriate.
- Common technical terms may include their English term in parentheses when necessary.
- Make the language appropriate for the selected grade.

Example:

WRONG:
Photosynthesis kya hai?

CORRECT:
ضیائی تالیف کیا ہے؟

WRONG:
Explain water cycle.

CORRECT:
آبی چکر کی وضاحت کریں۔

The final worksheet must NOT contain Roman Urdu.
""",

        "English + Urdu": """
Generate the worksheet bilingually.

For every question:
1. Write the English version first.
2. Write the Urdu version immediately below it.

Use this format:

English:
What is photosynthesis?

Urdu:
ضیائی تالیف کیا ہے؟

Do not use Roman Urdu.
The Urdu version must use proper Urdu script.
Instructions and answer choices should also be bilingual where appropriate.
""",
    }

    language_instruction = language_rules.get(
        language,
        language_rules["English"]
    )

    return f"""
You are an expert school worksheet designer for Sunbeams School.

Your job is to create a high-quality educational worksheet from the
provided learning material.

IMPORTANT:
The selected language is: {language}

{language_instruction}

WORKSHEET SETTINGS

Grade:
{grade}

Subject:
{subject}

Difficulty:
{difficulty}

Cognitive Level:
{cognitive_level}

Number of Questions:
{question_count}

Question Types:
{question_types}

Topics:
{topics}

Teacher Instructions:
{teacher_instructions}

LEARNING MATERIAL

{material}

QUALITY REQUIREMENTS

1. Questions must be directly related to the provided learning material.
2. Do not invent facts that are not supported by the material unless they
   are basic educational knowledge necessary to form the question.
3. Match the selected grade level.
4. Match the requested difficulty.
5. Use the requested cognitive level.
6. Avoid repetitive questions.
7. Create meaningful questions rather than simple wording changes.
8. Make questions clear and suitable for a school worksheet.
9. Make sure every question has a correct answer.
10. Make the answer key correspond exactly to the questions.
11. Respect the requested question types.
12. Follow the teacher's additional instructions.

QUESTION DESIGN

Use a mixture of thinking skills when appropriate:
- recall
- understanding
- application
- analysis
- reasoning
- problem solving

Do not make every question a simple definition.

JSON OUTPUT

Return ONLY valid JSON.

Do not use Markdown.
Do not use ```json.
Do not add explanations before or after the JSON.

Return exactly this structure:

{{
    "title": "Worksheet title",
    "instructions": "Worksheet instructions",
    "questions": [
        {{
            "number": 1,
            "type": "MCQ",
            "question": "Question text",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "answer": "Correct answer",
            "marks": 1
        }}
    ]
}}

Make sure the JSON is syntactically valid.
Escape quotation marks inside strings.
Do not put raw line breaks inside JSON string values.
"""
