#!/bin/bash
set -e

EXE_NAME=git-commit-gen
DEFAULT_MODEL="gpt-5.4"
DEFAULT_LANGUAGE="korean"
AUTO_YES="true"

usage() {
  cat <<EOF
Usage: ./build.sh [options]

Bake default behavior into the built binary.

Options:
  -y, --yes              빌드된 바이너리가 자동 yes 모드로 동작 (기본값)
  --no-yes               빌드된 바이너리가 항상 확인 프롬프트 표시
  -m, --model MODEL      바이너리의 기본 LLM 모델 (기본값: ${DEFAULT_MODEL})
  -l, --language LANG    바이너리의 기본 메시지 언어 (기본값: ${DEFAULT_LANGUAGE})
  -h, --help             이 도움말을 표시하고 종료
EOF
}

while [[ $# -gt 0 ]]; do
  case $1 in
    -y|--yes) AUTO_YES="true"; shift ;;
    --no-yes) AUTO_YES="false"; shift ;;
    -m|--model) DEFAULT_MODEL="$2"; shift 2 ;;
    -l|--language) DEFAULT_LANGUAGE="$2"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "❌ Unknown argument: $1" >&2; usage >&2; exit 1 ;;
  esac
done

case "$(uname -s)" in
  CYGWIN*|MINGW*|MSYS*) SEP=";" ;;
  *) SEP=":" ;;
esac

echo "🛠️  빌드 설정: model=${DEFAULT_MODEL}, language=${DEFAULT_LANGUAGE}, auto_yes=${AUTO_YES}"

cat > build_defaults.json <<EOF
{
  "model": "${DEFAULT_MODEL}",
  "language": "${DEFAULT_LANGUAGE}",
  "auto_yes": ${AUTO_YES}
}
EOF

cleanup() {
  rm -f build_defaults.json
}
trap cleanup EXIT

echo "🚧 Building executable with uv..."
uv run --group dev pyinstaller --onefile \
  --name "$EXE_NAME" \
  --add-data "prompt_template.yml${SEP}." \
  --add-data "build_defaults.json${SEP}." \
  main.py

echo "📦 Moving executable to current directory..."
mv -f "dist/$EXE_NAME"* ./

echo "🧹 Cleaning up..."
rm -rf build dist "$EXE_NAME"*.spec

echo "✅ Done! (model=${DEFAULT_MODEL}, language=${DEFAULT_LANGUAGE}, auto_yes=${AUTO_YES})"
