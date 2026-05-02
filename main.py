import argparse
import subprocess
from commitgen.config import load_build_defaults
from commitgen.gitdiff import get_git_diff
from commitgen.generator import generate_commit_message, LLM_MODEL


# --- build-time defaults (baked into binary by build.sh, empty when run from source)
build_defaults = load_build_defaults()
DEFAULT_LANGUAGE = build_defaults.get("language", "korean")
DEFAULT_MODEL = build_defaults.get("model", LLM_MODEL)
DEFAULT_AUTO_YES = build_defaults.get("auto_yes", False)


# --- constant
parser = argparse.ArgumentParser(description="GPT를 사용하여 커밋 메시지를 생성합니다.")
parser.add_argument(
    "-l", "--language",
    default=DEFAULT_LANGUAGE,
    help=f"커밋 메시지의 언어를 지정합니다 (기본값: {DEFAULT_LANGUAGE})"
)
parser.add_argument(
    "-m", "--model",
    default=DEFAULT_MODEL,
    help=f"사용할 LLM 모델을 지정합니다 (기본값: {DEFAULT_MODEL})"
)
parser.add_argument(
    "-y", "--yes",
    action="store_true",
    default=DEFAULT_AUTO_YES,
    help="확인 프롬프트 없이 자동으로 커밋합니다"
)
parser.add_argument(
    "--confirm",
    action="store_true",
    help="자동 yes 모드여도 확인 프롬프트를 강제로 표시합니다"
)
args = parser.parse_args()


# --- utils
def prompt_yes_no(message: str) -> bool:
    try:
        response = input(f"{message} [Y/n]: ").strip().lower()
        return response in ("", "y", "yes")
    except KeyboardInterrupt:
        print("\n❌ 작업이 취소되었습니다.")
        return False


def commit_with_message(message: str):
    result = subprocess.run(["git", "commit", "-m", message])
    if result.returncode == 0:
        print("✅ 커밋이 성공적으로 완료되었습니다!")
    else:
        print("❌ 커밋에 실패했습니다. 수동으로 확인해주세요.")


# --- main
def main():
    git_diff_text = get_git_diff()
    if not git_diff_text.strip():
        print("⚠️ 커밋할 변경사항이 없습니다. 먼저 `git add`를 실행해주세요.")
        return

    print(f"🤖 GPT로 {args.language} 커밋 메시지 생성 중 (모델명: {args.model})...\n")
    message, usage = generate_commit_message(
        git_diff_text=git_diff_text,
        language=args.language,
        llm_model=args.model,
    )

    print("\n📊 토큰 사용량:")
    print(f"   - 프롬프트 토큰     : {usage['prompt_tokens']}")
    print(f"   - 생성 토큰         : {usage['completion_tokens']}")
    print(f"   - 총 토큰           : {usage['total_tokens']}")
    print(f"💰 예상 비용           : ${usage['total_cost']:.5f} USD")
    print()

    print("\n✅ 생성된 커밋 메시지:\n")
    print(message)
    print()

    if not message.strip():
        print("❎ 메시지가 비어있어 커밋할 수 없습니다.")
        return

    needs_confirm = args.confirm or not args.yes
    if needs_confirm and not prompt_yes_no("이 메시지로 커밋하시겠습니까?"):
        print("❎ 커밋이 취소되었습니다.")
        return

    commit_with_message(message)


if __name__ == "__main__":
    main()
