import os
import json
import yaml

def load_api_key():
    path = os.path.join(os.getcwd(), ".api_keys", "openai.json")
    if not os.path.exists(path):
        raise FileNotFoundError("❌ API key file not found: .api_keys/openai.json")
    with open(path, "r") as f:
        data = json.load(f) 
        return data["api_key"]


def load_prompt_template(path: str = './prompt_template.yml'):
    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ Prompt template not found: {path}")
    with open(path, "r", encoding='utf-8') as f:
        config = yaml.safe_load(f)
        return config['commit_format'], config['commit_type']