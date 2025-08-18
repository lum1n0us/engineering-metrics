import os
import sys
from datetime import datetime, timedelta, timezone
from github3 import login


TOKEN_PATH = './token'
REPO = 'bytecodealliance/wasm-micro-runtime'

def get_token():
    """
    Retrieve the GitHub token from a file or prompt the user to input it.
    """
    if not os.path.exists(TOKEN_PATH):
        token = input("Token file not found. Please enter your token: ").strip()
        with open(TOKEN_PATH, 'w') as f:
            f.write(token)
        print("Token saved to ./token. Please restart the program.")
        sys.exit(1)

    with open(TOKEN_PATH, 'r') as f:
        return f.read().strip()

def get_recent_issues(repo_full_name, days=90):
    """
    Fetch recent open issues from the specified GitHub repository.

    Args:
        repo_full_name (str): The full name of the repository (e.g., 'owner/repo').
        days (int): The number of days to look back for issues.

    Returns:
        list: A list of recent open issues.
    """
    token = get_token()
    gh = login(token=token)
    repo = gh.repository(*repo_full_name.split('/'))
    now = datetime.now(timezone.utc)
    since = now - timedelta(days=days)
    return [
        issue for issue in repo.issues(state='open', since=since)
        if issue.created_at >= since
    ]

def main():
    """
    Main function to fetch and display recent issues.
    """
    try:
        issues = get_recent_issues(REPO)
        for issue in issues:
            print(f'#{issue.number}: {issue.title} (created at {issue.created_at})')
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
