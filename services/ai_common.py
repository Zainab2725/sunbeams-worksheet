import json
import re
import time
from config.gemini import get_client, MODEL_NAME


def _extract_json(text: str):
    """Extract a JSON object/array from Gemini output and tolerate markdown fences."""
    text = (text or "").strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.I)
    text = re.sub(r"\s*```$", "", text)

    # First try the complete response.
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Then locate the first JSON object/array and use raw_decode so trailing
    # commentary from the model does not break parsing.
    decoder = json.JSONDecoder()
    starts = [i for i, ch in enumerate(text) if ch in "[{]"]
    for start in starts:
        try:
            value, _ = decoder.raw_decode(text[start:])
            return value
        except json.JSONDecodeError:
            continue

    raise ValueError("Gemini returned malformed JSON after cleanup.")


def ask_json(prompt, images=None):
    client = get_client()
    contents = [prompt]
    if images:
        for image_bytes in images:
            contents.append({
                "inline_data": {
                    "mime_type": "image/jpeg",
                    "data": image_bytes,
                }
            })

    last_error = None
    for attempt in range(2):
        current_prompt = prompt
        if attempt == 1:
            current_prompt += """

IMPORTANT RETRY INSTRUCTION:
Your previous response could not be parsed as JSON. Return ONLY one valid JSON object.
Do not use markdown fences. Do not add commentary before or after the JSON.
Escape all quotation marks inside string values. Do not put raw line breaks inside
JSON string values. Check commas, brackets, quotes, and JSON syntax before responding.
"""
            contents = [current_prompt] + contents[1:]

        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=contents,
                config={
                    "temperature": 0.2,
                    "response_mime_type": "application/json",
                },
            )
            return _extract_json(response.text)
        except Exception as exc:
            last_error = exc
            if attempt == 0:
                time.sleep(0.5)

    raise ValueError(f"Gemini returned unusable JSON after retry: {last_error}")
