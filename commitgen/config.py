import json
import os
import sys

import yaml


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def _load_api_key(filename: str, provider: str):
    path = os.path.join(os.path.expanduser("~/.api_keys"), filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ {provider} API 키 파일을 찾을 수 없습니다: {path}")
    with open(path, "r") as f:
        data = json.load(f)
        return data["api_key"]


def load_openai_api_key():
    return _load_api_key("openai.json", "OpenAI")


def load_anthropic_api_key():
    return _load_api_key("anthropic.json", "Anthropic")


def load_prompt_template(path: str = "prompt_template.yml"):
    full_path = resource_path(path)
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"❌ 프롬프트 템플릿을 찾을 수 없습니다: {path}")
    with open(full_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        return config["commit_format"], config["commit_type"]


def load_build_defaults(path: str = "build_defaults.json"):
    full_path = resource_path(path)
    if not os.path.exists(full_path):
        return {}
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}
