MAX_PROMPT_CHARS = 50000


def apply_prompt_guardrail(prompt: str) -> tuple[str, bool]:
    if len(prompt) > MAX_PROMPT_CHARS:
        return prompt[:MAX_PROMPT_CHARS], True
    return prompt, False
