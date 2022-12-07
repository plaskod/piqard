from typing import Optional


def postprocess_answer(answer: str, fix_text: Optional[str]) -> str:
    if answer is not None:
        if fix_text:
            splitted_answer = answer.split(fix_text, 1)
            answer = splitted_answer[1] if len(splitted_answer) > 1 else answer
        return answer.strip().strip("\n")
    else:
        return "None"
