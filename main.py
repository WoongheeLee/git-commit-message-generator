import argparse
import subprocess
from commitgen.gitdiff import get_git_diff
from commitgen.generator import generate_commit_message


# --- constant 
parser = argparse.ArgumentParser(description="Generate a commit message using GPT.")
parser.add_argument(
    "-l", "--language",
    default="english",
    choices=["english", "korean"],
    help="Specify the language for the commit message (default: english)"
)
args = parser.parse_args()


# --- utils 
def prompt_yes_no(message: str) -> bool:
    try:
        response = input(f"{message} [Y/n]: ").strip().lower()
        return response in ("", "y", "yes")
    except KeyboardInterrupt:
        print("\n❌ Operation canceled.")
        return False


def commit_with_message(message: str):
    result = subprocess.run(["git", "commit", "-m", message])
    if result.returncode == 0:
        print("✅ Commit completed successfully!")
    else:
        print("❌ Commit failed. Please check manually.")


# --- main
def main():
    git_diff_text = get_git_diff()
    if not git_diff_text.strip():
        print("⚠️ No changes to commit. Please run `git add` first.")
        return

    print(f"🤖 Generating commit message in {args.language}...\n")
    message = generate_commit_message(
        git_diff_text=git_diff_text,
        language=args.language
        )

    print("\n✅ Generated commit message:\n")
    print(message)
    print()

    if prompt_yes_no("Would you like to commit with this message?"):
        commit_with_message(message)
    else:
        print("❎ Commit was canceled.")


if __name__ == "__main__":
    main()
