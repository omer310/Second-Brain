import json
from typing import Any

import httpx2 as httpx
import pytest
from anthropic import Anthropic

from second_brain.github import ChangedFile, PullRequest
from second_brain.review import (
    DIFF_BUDGET_CHARS,
    ReviewPrepError,
    Tier,
    prepare_review,
    render_pull_request,
)

NOTES = {
    "problem": "Merging duplicate donor records silently lost some memberships.",
    "fix": "Memberships and their payments now move to the surviving record.",
    "context": "CiviCRM is a shared donor database. Merging contacts combines their records.",
    "glossary": [
        {"term": "UPDATE IGNORE", "meaning": "A database update that skips rows it can't change."}
    ],
    "verdict": "Approve after the must-fix change: merges drop memberships.",
    "what_changed": "Merging two contacts now keeps both contacts' memberships.",
    "findings": [
        {
            "tier": "must_fix",
            "location": "CRM/Dedupe/Merger.php",
            "question": "What happens to a membership both contacts share?",
            "risk": "UPDATE IGNORE silently skips it, so the membership is lost.",
            "suggested_change": "Merge duplicate memberships explicitly and add a test for it.",
        }
    ],
    "praise": "The reproduction test pins down the real bug.",
    "coaching_question": "How would you check a merge path you can't run locally?",
    "coaching_answer": ["List the options that reach the path", "Write a test for each"],
    "draft_comment": "Nice reproduction test! One question before we merge...",
    "estimated_minutes": 15,
}


def make_pr(*files: ChangedFile) -> PullRequest:
    return PullRequest(
        repo="acme/app",
        number=7,
        url="https://github.com/acme/app/pull/7",
        title="Keep memberships when merging contacts",
        body="Fixes #12",
        author="fellow",
        head_sha="abc1234def",
        files=files,
    )


def streamed_message(text: str, stop_reason: str) -> str:
    events: list[dict[str, Any]] = [
        {
            "type": "message_start",
            "message": {
                "id": "msg_1",
                "type": "message",
                "role": "assistant",
                "model": "claude-opus-5-5",
                "content": [],
                "stop_reason": None,
                "stop_sequence": None,
                "usage": {"input_tokens": 10, "output_tokens": 1},
            },
        },
        {"type": "content_block_start", "index": 0, "content_block": {"type": "text", "text": ""}},
        {
            "type": "content_block_delta",
            "index": 0,
            "delta": {"type": "text_delta", "text": text},
        },
        {"type": "content_block_stop", "index": 0},
        {
            "type": "message_delta",
            "delta": {"stop_reason": stop_reason, "stop_sequence": None},
            "usage": {"output_tokens": 50},
        },
        {"type": "message_stop"},
    ]
    return "".join(f"event: {event['type']}\ndata: {json.dumps(event)}\n\n" for event in events)


def fake_client(text: str, stop_reason: str) -> Anthropic:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            text=streamed_message(text, stop_reason),
            headers={"content-type": "text/event-stream"},
        )

    return Anthropic(
        api_key="test", http_client=httpx.Client(transport=httpx.MockTransport(handler))
    )


def test_render_marks_first_artifact_and_omits_files_over_budget() -> None:
    small = ChangedFile("small.py", "modified", 1, 0, "+ok")
    huge = ChangedFile("huge.py", "added", 9000, 0, "+" * (DIFF_BUDGET_CHARS + 1))

    text = render_pull_request(make_pr(small, huge), first_artifact=True)

    assert text.startswith("This pull request is the fellow's first piece of work.")
    assert '<file path="small.py"' in text
    assert "<omitted_files>\nhuge.py\n</omitted_files>" in text


def test_prepare_review_returns_validated_notes() -> None:
    client = fake_client(json.dumps(NOTES), "end_turn")

    prep = prepare_review(client, make_pr(), first_artifact=False, model="m", effort="high")

    assert prep.glossary[0].term == "UPDATE IGNORE"
    assert prep.findings[0].tier is Tier.MUST_FIX
    assert prep.estimated_minutes == 15


def test_prepare_review_rejects_truncated_output() -> None:
    client = fake_client('{"verdict": "Approve', "max_tokens")

    with pytest.raises(ReviewPrepError):
        prepare_review(client, make_pr(), first_artifact=False, model="m", effort="high")
