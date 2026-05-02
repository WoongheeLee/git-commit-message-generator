# 깃 커밋 메시지 생성기

[README (English)](./README.md) | [README_KOR (한국어)](./README_KOR.md)

스테이징된 `git diff`로부터 GPT를 사용하여 간결하고 표준화된 커밋 메시지를 자동 생성합니다.

> OpenAI API 기반, Python 3.13으로 개발되어 다양한 언어를 지원합니다.

---

## 주요 기능

- LLM을 활용한 커밋 메시지 자동 생성 (기본 모델: `gpt-5.4`)
- [Conventional Commit](https://www.conventionalcommits.org/ko/v1.0.0/) 형식 지원
- 다국어 지원 (GPT 응답에 따라 결정, `--language <언어>` 옵션 사용)
- 호출 단위 토큰 사용량 및 USD 예상 비용 출력
- 자동 확인 모드 (`--yes`) 지원
- PyInstaller로 단일 실행 파일(.exe) 배포 가능, 빌드 시 기본값 설정 가능

## 지원 모델

모델명 prefix로 provider가 자동 감지됩니다 (`gpt-*` → OpenAI, `claude-*` → Anthropic).

| 모델 | Provider | Input ($/1M) | Output ($/1M) | Context |
| ----- | -------- | ------------ | ------------- | ------- |
| `gpt-5.4` (기본) | OpenAI | $2.50 | $15.00 | 1.05M |
| `gpt-5.4-mini` | OpenAI | $0.75 | $4.50 | 400K |
| `claude-opus-4-7` | Anthropic | $5.00 | $25.00 | 1M |
| `claude-sonnet-4-6` | Anthropic | $3.00 | $15.00 | 1M |
| `claude-haiku-4-5` | Anthropic | $1.00 | $5.00 | 200K |

---

## 필수 조건

본 프로젝트는 환경 및 의존성 관리를 위해 [uv](https://docs.astral.sh/uv/)를 사용합니다. uv 설치 후 다음 명령으로 의존성을 동기화하세요:

```bash
uv sync
```

Python 3.13 이상이 필요하며, `.python-version`을 기반으로 uv가 자동 설치합니다.

호환성 목적의 `requirements.txt`가 필요하면 다음 명령으로 생성할 수 있습니다:

```bash
uv export --no-hashes -o requirements.txt
```

---

## 사용 방법 (소스 코드 기준)

```bash
# 커밋 메시지 생성 및 적용
uv run python main.py

# 언어 지정 (예: 영어)
uv run python main.py --language english

# 모델 지정
uv run python main.py --model gpt-5.4-mini

# 자동 yes (확인 프롬프트 스킵)
uv run python main.py --yes

# 빌드 시 auto-yes가 박혀있어도 강제로 확인
uv run python main.py --confirm
```

### CLI 옵션

| 플래그 | 설명 |
| ----- | ----- |
| `-l, --language LANG` | 출력 언어 (기본: `korean` 또는 빌드 시 설정값) |
| `-m, --model MODEL` | LLM 모델 (기본: `gpt-5.4` 또는 빌드 시 설정값) |
| `-y, --yes` | 커밋 확인 프롬프트 스킵 |
| `--confirm` | 빌드된 auto-yes 무시하고 강제로 확인 표시 |

---

## API 키 설정

API 키는 lazy하게 로드됩니다 — 선택한 모델의 provider 키만 있으면 됩니다.

OpenAI 모델 (`gpt-*`)용:

```
~/.api_keys/openai.json
```

```json
{
  "api_key": "sk-..."
}
```

Anthropic 모델 (`claude-*`)용:

```
~/.api_keys/anthropic.json
```

```json
{
  "api_key": "sk-ant-..."
}
```

---

## 프롬프트 템플릿 설정

커밋 메시지 형식은 다음 파일을 통해 자유롭게 수정 가능합니다:

```
prompt_template.yml
```

`feat`, `fix`, `docs` 등 Conventional Commit에서 지원하는 타입과 포맷을 정의합니다.

---

## 단일 실행 파일(.exe)로 빌드 (선택 사항)

`build.sh` 스크립트를 사용하면 모델/언어/auto-yes 같은 기본값을 바이너리에 박아넣을 수 있습니다 (`build_defaults.json`을 PyInstaller 번들에 포함):

```bash
# 기본값: model=gpt-5.4, language=korean, auto_yes=true
./build.sh

# 다른 기본 모델로 빌드
./build.sh --model gpt-5.4-mini

# 항상 확인 프롬프트를 표시하는 바이너리로 빌드
./build.sh --no-yes

# 영어 커밋 메시지 기본값으로 빌드
./build.sh --language english

# 모든 옵션
./build.sh --help
```

직접 PyInstaller로 빌드도 가능합니다 (Windows는 `--add-data` 구분자가 `;`, Linux/macOS는 `:`):

```bash
uv run --group dev pyinstaller --onefile --add-data "prompt_template.yml:." main.py
```

- 실행 파일은 `git-commit-gen` (Windows에서는 `git-commit-gen.exe`)으로 생성됩니다.
- 빌드 시 박은 기본값은 런타임 CLI 플래그로 항상 override 가능합니다.
- Windows (Git Bash / WSL) 및 Linux에서 테스트 완료

---

## 출력 예시

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

## 라이선스

[MIT 라이선스](./LICENSE) 기반으로 자유롭게 사용 가능합니다.

--- 

# 기여 안내
기여자를 항상 환영합니다! 

자유롭게 포크(fork)하여 개선한 뒤, 풀 리퀘스트(pull request)를 보내주세요.
