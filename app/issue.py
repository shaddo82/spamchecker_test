# app/issue.py
import os
import requests

def create_github_issue(title: str, body: str, logger) -> None:
    repo = os.getenv("GH_REPO")
    token = os.getenv("GH_TOKEN")
    if not repo or not token:
        logger.warning("GH_REPO/GH_TOKEN not set; skipping GitHub issue creation.")
        return

    url = f"https://api.github.com/repos/{repo}/issues"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }
    payload = {"title": title, "body": body}

    logger.info(f"GitHub issue target repo={repo}")  # 디버깅 핵심

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=10)
    except Exception:
        logger.exception("GitHub API request failed")
        return

    if r.status_code >= 300:
        logger.warning(f"Failed to create issue: {r.status_code} {r.text[:300]}")
    else:
        logger.info(f"Issue created: {r.status_code}")
