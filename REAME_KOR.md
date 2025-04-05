# 깃 커밋 메시지 생성기

[README (English)](./README.md) | [README_KOR (한국어)](./README_KOR.md)

스테이징된 `git diff`로부터 GPT를 사용하여 간결하고 표준화된 커밋 메시지를 자동 생성합니다.

> OpenAI API 기반, Python 3.12로 개발되어 다양한 언어를 지원합니다.

---

## 주요 기능

- LLM을 활용한 커밋 메시지 자동 생성  
- [Conventional Commit](https://www.conventionalcommits.org/ko/v1.0.0/) 형식 지원  
- 다국어 지원 (GPT 응답에 따라 결정, `--language <언어>` 옵션 사용)  
- PyInstaller로 단일 실행 파일(.exe) 배포 가능  

---

## 필수 조건

소스코드를 사용할 경우 다음 명령으로 패키지를 설치하세요:

```bash
pip install -r requirements.txt
```

Python 3.12 환경에서 개발되었으므로, Conda 환경 사용을 권장합니다:  
> `conda create -n commit-message python=3.12`

---

## 사용 방법 (소스 코드 기준)

```bash
# 커밋 메시지 생성 및 적용
python main.py

# 언어 지정 (예: 영어)
python main.py --language english
```

---

## API 키 설정

OpenAI API 키가 필요합니다. 다음과 같이 파일을 생성하세요:

```
.api_keys/openai.json
```

```json
{
  "api_key": "your-openai-api-key-here"
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

PyInstaller를 사용하여 `.exe` 파일로 빌드할 수 있습니다:

```bash
pyinstaller --onefile --add-data "prompt_template.yml;." main.py
```

- 실행 파일은 `dist/main.exe` 경로에 생성됩니다.  
- Windows에서 테스트 완료

---

## 출력 예시

```text
🤖 영어로 커밋 메시지를 생성 중...

✅ 생성된 커밋 메시지:

feat: add CLI option to specify commit message language

이 메시지로 커밋하시겠습니까? [Y/n]:
```

---

## 라이선스

[MIT 라이선스](./LICENSE) 기반으로 자유롭게 사용 가능합니다.
