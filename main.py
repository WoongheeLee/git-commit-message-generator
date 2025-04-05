import subprocess
from commitgen.gitdiff import get_git_diff
from commitgen.generator import generate_commit_message
from commitgen.config import load_config, load_prompt_template


# --- utils 
def prompt_yes_no(message: str) -> bool:
    try:
        response = input(f"{message} [Y/n]: ").strip().lower()
        return response in ("", "y", "yes")
    except KeyboardInterrupt:
        print("\n❌ 취소되었습니다.")
        return False


def commit_with_message(message: str):
    result = subprocess.run(["git", "commit", "-m", message])
    if result.returncode == 0:
        print("✅ 커밋 완료!")
    else:
        print("❌ 커밋 실패. 수동으로 확인해주세요.")


# --- main
def main():
    diff = get_git_diff()
    if not diff.strip():
        print("⚠️ 커밋할 변경 사항이 없습니다. 먼저 `git add` 하세요.")
        return

    config = load_config("config.json")
    prompt_template = load_prompt_template("prompt_template.txt")

    prompt = prompt_template.format(
        diff=diff,
        format=config["format"],
        types=", ".join(config["type"])
    )

    print("🤖 GPT로 커밋 메시지를 생성 중...\n")
    message = generate_commit_message(git_diff_text=prompt)

    print("\n✅ 생성된 커밋 메시지:\n")
    print(message)
    print()

    if prompt_yes_no("이 메시지로 커밋할까요?"):
        commit_with_message(message)
    else:
        print("❎ 커밋하지 않았습니다.")


if __name__ == "__main__":
    main()
