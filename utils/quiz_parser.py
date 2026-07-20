import json
import re


def _remove_code_fence(text: str) -> str:
    if text.strip().startswith("```"):
        return re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.IGNORECASE)
    return text.strip()


def _validate_questions(data: object) -> list[dict]:
    if not isinstance(data, list):
        return []

    questions = []
    for item in data:
        if not isinstance(item, dict):
            continue
        options = item.get("options")
        answer = str(item.get("answer", "")).upper().strip()
        if (
            isinstance(options, dict)
            and set(options) == {"A", "B", "C", "D"}
            and answer in options
            and item.get("question")
        ):
            questions.append(
                {
                    "question": str(item["question"]),
                    "options": options,
                    "answer": answer,
                    "explanation": str(item.get("explanation", "")),
                }
            )
    return questions


def parse_quiz(text: str) -> list[dict]:
    """Parse Gemini's JSON output and return only complete questions."""
    try:
        return _validate_questions(json.loads(_remove_code_fence(text)))
    except json.JSONDecodeError:
        return []
