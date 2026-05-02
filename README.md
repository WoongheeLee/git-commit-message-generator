# Git Commit Message Generator

[README (English)](./README.md) | [README (한국어)](./README_KOR.md)

Generate concise, conventional commit messages using GPT, directly from your staged `git diff`.

> Powered by OpenAI API and built with Python 3.13. Supports any language supported by GPT (e.g., English, Korean, French, etc.)

---

## Features

- Auto-generate commit messages using LLM (default model: `gpt-5.4`)
- Supports [Conventional Commit](https://www.conventionalcommits.org/) format
- Multilingual support (language is GPT-dependent, use `--language <lang>`)
- Token usage and estimated USD cost reporting per call
- Auto-confirm mode (`--yes`) for non-interactive workflows
- PyInstaller-compatible for single-file binary distribution, with build-time configurable defaults

## Supported Models

Provider is auto-detected from the model name prefix (`gpt-*` → OpenAI, `claude-*` → Anthropic).

| Model | Provider | Input ($/1M) | Output ($/1M) | Context |
| ----- | -------- | ------------ | ------------- | ------- |
| `gpt-5.4` (default) | OpenAI | $2.50 | $15.00 | 1.05M |
| `gpt-5.4-mini` | OpenAI | $0.75 | $4.50 | 400K |
| `claude-opus-4-7` | Anthropic | $5.00 | $25.00 | 1M |
| `claude-sonnet-4-6` | Anthropic | $3.00 | $15.00 | 1M |
| `claude-haiku-4-5` | Anthropic | $1.00 | $5.00 | 200K |

---

## Requirements

This project uses [uv](https://docs.astral.sh/uv/) for environment and dependency management. Install uv first, then sync dependencies:

```bash
uv sync
```

Python 3.13+ is required (uv will install it automatically based on `.python-version`).

If you need a `requirements.txt` for compatibility, generate it with:

```bash
uv export --no-hashes -o requirements.txt
```

---

## Usage (from source)

```bash
# Generate and apply commit message
uv run python main.py

# Specify language
uv run python main.py --language english

# Specify model
uv run python main.py --model gpt-5.4-mini

# Auto-confirm (skip the [Y/n] prompt)
uv run python main.py --yes

# Force confirm even when --yes is the baked-in default
uv run python main.py --confirm
```

### CLI Options

| Flag | Description |
| ---- | ----------- |
| `-l, --language LANG` | Output language (default: `korean`, or build-baked default) |
| `-m, --model MODEL` | LLM model (default: `gpt-5.4`, or build-baked default) |
| `-y, --yes` | Skip the commit confirmation prompt |
| `--confirm` | Force confirmation prompt (overrides build-baked auto-yes) |

---

## Setup API Key

API keys are loaded lazily — only the provider matching your selected model is required.

For OpenAI models (`gpt-*`):

```
~/.api_keys/openai.json
```

```json
{
  "api_key": "sk-..."
}
```

For Anthropic models (`claude-*`):

```
~/.api_keys/anthropic.json
```

```json
{
  "api_key": "sk-ant-..."
}
```

---

## Prompt Template

You can customize the commit format via:

```
prompt_template.yml
```

It defines the Conventional Commit format and supported types (e.g., `feat`, `fix`, `docs`...).

---

## Build Standalone Executable (Optional)

Use the helper script — it bakes default behavior (model, language, auto-yes) into the binary via a bundled `build_defaults.json`:

```bash
# Default: model=gpt-5.4, language=korean, auto_yes=true
./build.sh

# Choose a different default model
./build.sh --model gpt-5.4-mini

# Build a binary that always asks for confirmation
./build.sh --no-yes

# Build for English commit messages by default
./build.sh --language english

# All build options
./build.sh --help
```

Or invoke PyInstaller directly (Windows uses `;` as `--add-data` separator, Linux/macOS uses `:`):

```bash
uv run --group dev pyinstaller --onefile --add-data "prompt_template.yml:." main.py
```

- Executable is saved as `git-commit-gen` (or `git-commit-gen.exe` on Windows)
- Build-baked defaults can always be overridden at runtime via CLI flags
- Tested on Windows (Git Bash / WSL) and Linux

---

## Example Output

```text
🤖 GPT로 korean 커밋 메시지 생성 중 (모델명: gpt-5.4)...


📊 토큰 사용량:
   - 프롬프트 토큰     : 412
   - 생성 토큰         : 38
   - 총 토큰           : 450
💰 예상 비용           : $0.00160 USD


✅ 생성된 커밋 메시지:

feat: add CLI option to specify commit message language

이 메시지로 커밋하시겠습니까? [Y/n]:
```

---

## License

[MIT License](./LICENSE)

--- 

## Contributing

Gladly welcoming contributors!  
Feel free to fork, improve, and send a pull request.
