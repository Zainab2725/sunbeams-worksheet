def clean_text(value):
    return str(value or "").strip()

def ensure_list(value):
    return value if isinstance(value, list) else []

def normalize_worksheet(data):
    if not isinstance(data, dict):
        raise ValueError("AI did not return a valid worksheet object.")
    questions = ensure_list(data.get("questions"))
    normalized = []
    for i, q in enumerate(questions, 1):
        if not isinstance(q, dict):
            continue
        normalized.append({
            "id": i,
            "type": clean_text(q.get("type") or "short_answer"),
            "question": clean_text(q.get("question")),
            "options": ensure_list(q.get("options")),
            "answer": clean_text(q.get("answer")),
            "explanation": clean_text(q.get("explanation")),
            "marks": int(q.get("marks") or 1),
        })
    data["questions"] = normalized
    data["title"] = clean_text(data.get("title") or "Sunbeams Worksheet")
    data["instructions"] = clean_text(data.get("instructions") or "Answer all questions carefully.")
    return data
