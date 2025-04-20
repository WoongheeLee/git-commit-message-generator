import time 
import requests
import tiktoken
from commitgen.config import load_api_key, load_prompt_template


# --- constants
MODEL_PRICING = {
    "gpt-4": {"prompt": 0.03, "completion": 0.06},
    "gpt-4.0": {"prompt": 0.03, "completion": 0.06},
    "gpt-4.1": {"prompt": 0.03, "completion": 0.06},
    "gpt-3.5-turbo": {"prompt": 0.0015, "completion": 0.002},
}

LLM_MODEL = 'gpt-4.1'
OpenAI_API = load_api_key()

MAX_RETRIES = 5 
RETRY_DELAY = 1 # seconds 

HEADERS = {
    'Content-Type': "application/json", 
    'Authorization': f"Bearer {OpenAI_API}"
}


# --- utils 
def count_tokens(messages, model="gpt-4"):
    """Estimate number of tokens used in messages for a chat completion."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")  # fallback

    num_tokens = 0
    for message in messages:
        num_tokens += 4  # role, name overhead
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
    num_tokens += 2  # reply priming
    return num_tokens


def get_openai_api_result(
        system_prompt='', 
        user_prompt='', 
        llm_model=LLM_MODEL, 
        headers=HEADERS,
        max_retries=MAX_RETRIES, 
        retry_delay=RETRY_DELAY,
        return_usage=True
    ): 

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    payload = {
        "model": llm_model, 
        "messages": messages,
        "max_tokens": 4096, 
        "temperature": 0, 
        "top_p": 0.7,
    }

    # retry loop
    for attempt in range(max_retries): 
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers, 
            json=payload, 
        )

        if response.status_code == 200: 
            result = response.json()
            content = result['choices'][0]['message']['content']
            usage = result.get("usage", {})
            prompt_tokens = usage.get("prompt_tokens", 0)
            completion_tokens = usage.get("completion_tokens", 0)
            total_tokens = usage.get("total_tokens", prompt_tokens + completion_tokens)
            break
        else: 
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                content = ''
                prompt_tokens = completion_tokens = total_tokens = 0

    if return_usage:
        pricing = MODEL_PRICING.get(llm_model, {"prompt": 0.03, "completion": 0.06})
        input_cost = (prompt_tokens / 1000) * pricing["prompt"]
        output_cost = (completion_tokens / 1000) * pricing["completion"]
        total_cost = input_cost + output_cost

        return content, {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "input_cost": input_cost,
            "output_cost": output_cost,
            "total_cost": total_cost
        }
    else:
        return content


def generate_commit_message(
        git_diff_text: str, 
        llm_model=LLM_MODEL, 
        max_retries=1,
        language='english'
        ):
    
    commit_format, commit_type = load_prompt_template()

    system_prompt = f"""
You are an assistant that generates concise and meaningful Git commit messages from git diffs.
Write the commit message in {language}.
Follow the Conventional Commit format: {commit_format}

Available types:
{commit_type}
Return only the commit message, no explanation or extra output.
"""
    user_prompt = f"""
Generate a commit message based on the following staged git diff:

{git_diff_text}
"""

    message, usage = get_openai_api_result(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        llm_model=llm_model,
        max_retries=max_retries,
        return_usage=True
    )

    return message, usage

