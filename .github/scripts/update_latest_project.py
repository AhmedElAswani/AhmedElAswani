import json
import os
import urllib.request

USERNAME = "AhmedElAswani"
README = "README.md"

START = "<!-- LATEST_PROJECT:START -->"
END = "<!-- LATEST_PROJECT:END -->"

url = (
    f"https://api.github.com/users/{USERNAME}/repos"
    "?sort=pushed&direction=desc&per_page=100&type=owner"
)

request = urllib.request.Request(
    url,
    headers={
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {os.environ['GH_TOKEN']}",
        "X-GitHub-Api-Version": "2022-11-28",
    },
)

with urllib.request.urlopen(request) as response:
    repos = json.loads(response.read())

repos = [
    repo for repo in repos
    if not repo["fork"]
    and not repo["private"]
    and not repo["archived"]
    and repo["name"].lower() != USERNAME.lower()
]

if not repos:
    raise SystemExit("No eligible public repositories found.")

repo = repos[0]

name = repo["name"]
description = (repo.get("description") or "A project I'm working on.").replace("|", "\\|")
language = repo.get("language") or "Not specified"
link = repo["html_url"]

content = f"""### 🚀 {name}

{description}

**Primary Language:** `{language}`

[<img src="https://img.shields.io/badge/VIEW%20PROJECT-19264B?style=for-the-badge&logo=github&logoColor=22D3EE" alt="View Project"/>]({link})

<sub>Last pushed: {repo["pushed_at"][:10]}</sub>
"""

with open(README, "r", encoding="utf-8") as file:
    readme = file.read()

if START not in readme or END not in readme:
    raise SystemExit("Latest project markers not found in README.")

before, remaining = readme.split(START, 1)
_, after = remaining.split(END, 1)

updated = before + START + "\n" + content + END + after

with open(README, "w", encoding="utf-8") as file:
    file.write(updated)

print(f"Updated latest project: {name}")
