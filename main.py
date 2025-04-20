import argparse
import subprocess
from commitgen.gitdiff import get_git_diff
from commitgen.generator import generate_commit_message, LLM_MODEL


# --- constant 
parser = argparse.ArgumentParser(description=f"Generate a commit message using GPT.")
parser.add_argument(
    "-l", "--language",
    default="korean",
    help="Specify the language for the commit message (default: english)"
)
parser.add_argument(
    "-m", "--model",
    default=LLM_MODEL,
    help=f"Specify the LLM model to use (default: {LLM_MODEL})"
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

    print(f"🤖 Generating commit message in {args.language} using GPT (model name: {args.model})...\n")
    message, usage = generate_commit_message(
        git_diff_text=git_diff_text,
        language=args.language, 
        llm_model=args.model,
    )

    print("\n📊 Token usage:")
    print(f"   - Prompt tokens     : {usage['prompt_tokens']}")
    print(f"   - Completion tokens : {usage['completion_tokens']}")
    print(f"   - Total tokens      : {usage['total_tokens']}")
    print(f"💰 Estimated cost      : ${usage['total_cost']:.5f} USD")
    print()

    print("\n✅ Generated commit message:\n")
    print(message)
    print()

    if prompt_yes_no("Would you like to commit with this message?"):
        commit_with_message(message)
    else:
        print("❎ Commit was canceled.")


if __name__ == "__main__":
    main()
