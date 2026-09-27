import httpx2 as httpx
import pytest

from second_brain.github import GitHub, parse_pr_url

PR = {
    "html_url": "https://github.com/acme/app/pull/7",
    "title": "Keep memberships when merging contacts",
    "body": None,
    "user": {"login": "fellow"},
    "head": {"sha": "abc1234def"},
}


def changed_file(path: str) -> dict[str, object]:
    return {"filename": path, "status": "modified", "additions": 1, "deletions": 0, "patch": "+ok"}


def test_parse_pr_url() -> None:
    assert parse_pr_url("https://github.com/acme/app/pull/7/files") == ("acme/app", 7)
    with pytest.raises(ValueError):
        parse_pr_url("https://github.com/acme/app/issues/7")


def test_pull_request_follows_file_pagination() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/repos/acme/app/pulls/7":
            return httpx.Response(200, json=PR)
        if request.url.params.get("page") == "2":
            return httpx.Response(200, json=[changed_file("b.py")])
        page_two = "https://api.github.com/repos/acme/app/pulls/7/files?per_page=100&page=2"
        return httpx.Response(
            200, json=[changed_file("a.py")], headers={"Link": f'<{page_two}>; rel="next"'}
        )

    pr = GitHub(transport=httpx.MockTransport(handler)).pull_request("acme/app", 7)

    assert [file.path for file in pr.files] == ["a.py", "b.py"]
    assert pr.body == ""
    assert pr.author == "fellow"
