import sys 
import os
import json
import yaml


def resource_path(relative_path): 
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def load_api_key():
    path = os.path.join(os.path.expanduser("~/.api_keys"), "openai.json")
    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ API key file not found: {path}")
    with open(path, "r") as f:
        data = json.load(f) 
        return data["api_key"]


def load_prompt_template(path: str = 'prompt_template.yml'):
    full_path = resource_path(path)
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"❌ Prompt template not found: {path}")
    with open(full_path, "r", encoding='utf-8') as f:
        config = yaml.safe_load(f)
        return config['commit_format'], config['commit_type']
