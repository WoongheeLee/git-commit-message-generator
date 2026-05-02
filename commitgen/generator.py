import time

import requests

from commitgen.config import (
    load_anthropic_api_key,
    load_openai_api_key,
    load_prompt_template,
)

# --- constants
# Prices are in USD per 1M tokens
MODEL_PRICING = {
    # OpenAI
    "gpt-5.4": {"prompt": 2.50, "completion": 15.00},
    "gpt-5.4-mini": {"prompt": 0.75, "completion": 4.50},
    # Anthropic
    "claude-opus-4-7": {"prompt": 5.00, "completion": 25.00},
    "claude-sonnet-4-6": {"prompt": 3.00, "completion": 15.00},
    "claude-haiku-4-5": {"prompt": 1.00, "completion": 5.00},
}


LLM_MODEL = "gpt-5.4"

MAX_RETRIES = 5
RETRY_DELAY = 1  # seconds


# --- provider dispatch
def get_provider(model: str) -> str:
    if model.startswith("gpt-"):
        return "openai"
    if model.startswith("claude-"):
        return "anthropic"
    raise ValueError(f"❌ 알 수 없는 provider — 모델명: {model}")


# --- OpenAI call
def call_openai(system_prompt, user_prompt, model, max_retries, retry_delay):
    api_key = load_openai_api_key()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "max_completion_tokens": 4096,
        "temperature": 0,
        "top_p": 0.7,
    }

    for attempt in range(max_retries):
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
        )
        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            usage = result.get("usage", {})
            prompt_tokens = usage.get("prompt_tokens", 0)
            completion_tokens = usage.get("completion_tokens", 0)
            total_tokens = usage.get("total_tokens", prompt_tokens + completion_tokens)
            return content, prompt_tokens, completion_tokens, total_tokens

        if attempt < max_retries - 1:
            time.sleep(retry_delay)
        else:
            print(f"❌ OpenAI API 호출 실패 (status {response.status_code})")
            print(f"   모델: {model}")
            print(f"   응답: {response.text}")
            return "", 0, 0, 0


# --- Anthropic call
def call_anthropic(system_prompt, user_prompt, model, max_retries, retry_delay):
    api_key = load_anthropic_api_key()
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
    }
    payload = {
        "model": model,
        "max_tokens": 4096,
        "system": system_prompt,
        "messages": [
            {"role": "user", "content": user_prompt},
        ],
    }

    for attempt in range(max_retries):
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json=payload,
        )
        if response.status_code == 200:
            result = response.json()
            content = ""
            for block in result.get("content", []):
                if block.get("type") == "text":
                    content = block.get("text", "")
                    break
            usage = result.get("usage", {})
            prompt_tokens = usage.get("input_tokens", 0)
            completion_tokens = usage.get("output_tokens", 0)
            total_tokens = prompt_tokens + completion_tokens
            return content, prompt_tokens, completion_tokens, total_tokens

        if attempt < max_retries - 1:
            time.sleep(retry_delay)
        else:
            print(f"❌ Anthropic API 호출 실패 (status {response.status_code})")
            print(f"   모델: {model}")
            print(f"   응답: {response.text}")
            return "", 0, 0, 0


# --- unified entrypoint
def get_api_result(
    system_prompt="",
    user_prompt="",
    llm_model=LLM_MODEL,
    max_retries=MAX_RETRIES,
    retry_delay=RETRY_DELAY,
):
    provider = get_provider(llm_model)
    if provider == "openai":
        content, prompt_tokens, completion_tokens, total_tokens = call_openai(
            system_prompt, user_prompt, llm_model, max_retries, retry_delay
        )
    else:
        content, prompt_tokens, completion_tokens, total_tokens = call_anthropic(
            system_prompt, user_prompt, llm_model, max_retries, retry_delay
        )

    pricing = MODEL_PRICING.get(llm_model, {"prompt": 30.0, "completion": 60.0})
    input_cost = (prompt_tokens / 1_000_000) * pricing["prompt"]
    output_cost = (completion_tokens / 1_000_000) * pricing["completion"]
    total_cost = input_cost + output_cost

    return content, {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
        "input_cost": input_cost,
        "output_cost": output_cost,
        "total_cost": total_cost,
    }


def generate_commit_message(
    git_diff_text: str, llm_model=LLM_MODEL, max_retries=1, language="english"
):
    commit_format, commit_type = load_prompt_template()

    system_prompt = f"""
당신은 git diff로부터 간결하고 의미있는 Git 커밋 메시지를 생성하는 어시스턴트입니다.
커밋 메시지는 {language}로 작성하세요.
Conventional Commit 형식을 따르세요: {commit_format}

사용 가능한 타입:
{commit_type}
커밋 메시지만 반환하고, 설명이나 추가 출력은 하지 마세요.
"""
    user_prompt = f"""
다음의 staged git diff를 기반으로 커밋 메시지를 생성하세요:

{git_diff_text}
"""

    message, usage = get_api_result(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        llm_model=llm_model,
        max_retries=max_retries,
    )

    return message, usage
