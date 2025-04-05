import subprocess

def get_git_diff():
    result = subprocess.run(["git", "diff", "--cached"], capture_output=True, text=True, encoding='utf-8')
    return result.stdout