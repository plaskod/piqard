from typing import Optional


def postprocess_answer(answer: str, fix_text: Optional[str]) -> str:
    if fix_text:
        answer = answer.split(fix_text, 1)[1]
    return answer.strip().strip("\n")
