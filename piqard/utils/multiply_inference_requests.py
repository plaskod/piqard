from piqard.language_models.language_model import LanguageModel


def multiply_inference_requests(
    prompt: str, language_model: LanguageModel, stop_token: str
) -> str:
    generated_answer = ""
    while generated_answer.find(stop_token) == -1:
        generated_text = language_model.query(prompt + generated_answer)[0][
            "generated_text"
        ]
        generated_answer += generated_text.split(prompt)[1]
    return generated_answer.split(stop_token)[0]
