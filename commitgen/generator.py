import time 
import requests
from commitgen.config import load_api_key, load_prompt_template


# --- constants
LLM_MODEL = 'gpt-4o-mini'
OpenAI_API = load_api_key()

MAX_RETRIES = 5 
RETRY_DELAY = 1 # seconds 

HEADERS = {
    'Content-Type': "application/json", 
    'Authorization': f"Bearer {OpenAI_API}"
}


# --- utils 
def get_openai_api_result(
        system_prompt='', 
        user_prompt='', 
        llm_model=LLM_MODEL, 
        headers=HEADERS,
        max_retries=MAX_RETRIES, 
        retry_delay=RETRY_DELAY,
        ): 

    payload = {
        "model": llm_model, 
        "messages": [
            {
                "role": "system", 
                "content": system_prompt
            }, 
            {
                "role": "user", 
                "content": user_prompt
            }
        ], 
        "max_tokens": 4096, 
        "temperature": 0, 
        "top_p": .7,
    }

    for attempt in range(max_retries): 
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers, 
            json=payload, 
        )

        if response.status_code == 200: 
            result = response.json() 
            content = result['choices'][0]['message']['content'] 
            break 
        else: 
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                content = ''

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

    response = get_openai_api_result(system_prompt=system_prompt, user_prompt=user_prompt, llm_model=llm_model, max_retries=max_retries)
    return response