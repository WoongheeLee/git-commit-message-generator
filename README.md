# Commit Message Generator

[README (English)](./README.md) | [README (한국어)](./README_KOR.md)

Generate concise, conventional commit messages using GPT, directly from your staged `git diff`.

> Powered by OpenAI API and built with Python 3.12. Supports any language supported by GPT (e.g., English, Korean, French, etc.)

---

## Features

- Auto-generate commit messages using LLM
- Supports [Conventional Commit](https://www.conventionalcommits.org/) format
- Multilingual support (language is GPT-dependent, use --language <lang>)
- PyInstaller-compatible for single-file binary distribution

---

## Requirements

If using source code:

```bash
pip install -r requirements.txt
```

Developed in a Python 3.12 environment. Recommended to use Conda:
> `conda create -n commit-message python=3.12`

---

## Usage (from source)

```bash
# Generate and apply commit message
python main.py

# Specify language
python main.py --language english
```

---

## Setup API Key

OpenAI API key is required. Create the following file:

```
.api_keys/openai.json
```

```json
{
  "api_key": "your-openai-api-key-here"
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

PyInstaller is used to create a `.exe`:

```bash
pyinstaller --onefile --add-data "prompt_template.yml;." main.py
```

- Executable is saved in `dist/main.exe`
- Supports Windows (tested)

---

## Example Output

```text
🤖 Generating commit message in english...

✅ Generated commit message:

feat: add CLI option to specify commit message language

Would you like to commit with this message? [Y/n]:
```

---

## License

[MIT License](./LICENSE)