import os
from datetime import datetime, timedelta, UTC
from github3 import login


TOKEN_PATH = './token'
REPO = 'bytecodealliance/wasm-micro-runtime'

def get_token():
    if not os.path.exists(TOKEN_PATH):
        token = input("Token file not found. Please enter your token: ").strip()
        with open(TOKEN_PATH, 'w') as f:
            f.write(token)
        print("Token saved to ./token. Please restart the program.")
        sys.exit(0)

    with open(TOKEN_PATH, 'r') as f:
        return f.read().strip()

def get_recent_issues(repo_full_name, days=90):
    token = get_token()
    gh = login(token=token)
    repo = gh.repository(*repo_full_name.split('/'))
    now = datetime.now(UTC)
    since = now - timedelta(days=days)
    issues = [issue for issue in repo.issues(state='open', since=since) if issue.created_at >= since]
    return issues

def main():
    issues = get_recent_issues(REPO)
    for issue in issues:
        print(f'#{issue.number}: {issue.title} (created at {issue.created_at})')

if __name__ == '__main__':
    main()
