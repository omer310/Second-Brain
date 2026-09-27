import re
from dataclasses import dataclass
from typing import Any

import httpx2 as httpx

API_URL = "https://api.github.com"
PR_URL = re.compile(r"https://github\.com/(?P<repo>[\w.-]+/[\w.-]+)/pull/(?P<number>\d+)")


@dataclass(frozen=True)
class ChangedFile:
    path: str
    status: str
    additions: int
    deletions: int
    patch: str | None


@dataclass(frozen=True)
class PullRequest:
    repo: str
    number: int
    url: str
    title: str
    body: str
    author: str
    head_sha: str
    files: tuple[ChangedFile, ...]


def parse_pr_url(url: str) -> tuple[str, int]:
    match = PR_URL.match(url.strip())
    if match is None:
        raise ValueError(f"Not a GitHub pull request URL: {url}")
    return match["repo"], int(match["number"])


class GitHub:
    """Read-only GitHub client. It has no methods that write, by design."""

    def __init__(self, token: str | None = None, transport: httpx.BaseTransport | None = None):
        headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        self._http = httpx.Client(
            base_url=API_URL, headers=headers, timeout=30, transport=transport
        )

    def pull_request(self, repo: str, number: int) -> PullRequest:
        data = self._get(f"/repos/{repo}/pulls/{number}")
        files = self._get_all(f"/repos/{repo}/pulls/{number}/files?per_page=100")
        return PullRequest(
            repo=repo,
            number=number,
            url=data["html_url"],
            title=data["title"],
            body=data["body"] or "",
            author=data["user"]["login"],
            head_sha=data["head"]["sha"],
            files=tuple(
                ChangedFile(
                    path=file["filename"],
                    status=file["status"],
                    additions=file["additions"],
                    deletions=file["deletions"],
                    patch=file.get("patch"),
                )
                for file in files
            ),
        )

    def _get(self, url: str) -> Any:
        response = self._http.get(url)
        response.raise_for_status()
        return response.json()

    def _get_all(self, url: str) -> list[Any]:
        items: list[Any] = []
        next_url: str | None = url
        while next_url:
            response = self._http.get(next_url)
            response.raise_for_status()
            items.extend(response.json())
            next_url = response.links.get("next", {}).get("url")
        return items
