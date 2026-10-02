import requests
import os
from datetime import datetime, timedelta

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
REPO = "dekunlab/synaptoflow-Datahub"
DISCORD_WEBHOOK = os.environ["WEEKLY_REPORT_WEBHOOK_URL"]

since = (datetime.utcnow() - timedelta(days=7)).isoformat() + "Z"

def github_activity():
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    commits = requests.get(
        f"https://api.github.com/repos/{REPO}/commits",
        headers=headers, params={"since": since}
    ).json()
    issues = requests.get(
        f"https://api.github.com/repos/{REPO}/issues",
        headers=headers, params={"since": since, "state": "all"}
    ).json()
    # .get() with a default avoids crashing if the API returns an error object instead of a list
    return len(commits) if isinstance(commits, list) else 0, \
           len(issues) if isinstance(issues, list) else 0

def post_report():
    commit_count, issue_count = github_activity()
    message = (
        "** Weekly SynaptoFlow Signal Report**\n"
        f"- Commits this week: {commit_count}\n"
        f"- Issues/PRs touched: {issue_count}\n"
    )
    requests.post(DISCORD_WEBHOOK, json={"content": message})

if __name__ == "__main__":
    post_report()