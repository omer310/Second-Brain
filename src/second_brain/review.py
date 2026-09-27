from enum import StrEnum
from importlib import resources

from anthropic import Anthropic
from pydantic import BaseModel, ValidationError

from second_brain.github import PullRequest
from second_brain.settings import Effort

PROMPT_VERSION = "review-prep-v3"
SYSTEM_PROMPT = (
    resources.files("second_brain").joinpath("prompts/review_prep.md").read_text(encoding="utf-8")
)
DIFF_BUDGET_CHARS = 120_000
MAX_TOKENS = 32_000


class Tier(StrEnum):
    MUST_FIX = "must_fix"
    CLARIFY = "clarify"
    LATER = "later"


class Finding(BaseModel):
    tier: Tier
    location: str
    question: str
    risk: str
    suggested_change: str


class Term(BaseModel):
    term: str
    meaning: str


class ReviewPrep(BaseModel):
    problem: str
    fix: str
    context: str
    glossary: list[Term]
    verdict: str
    what_changed: str
    findings: list[Finding]
    praise: str
    coaching_question: str
    coaching_answer: list[str]
    draft_comment: str
    estimated_minutes: int


class ReviewPrepError(RuntimeError):
    pass


def prepare_review(
    client: Anthropic, pr: PullRequest, *, first_artifact: bool, model: str, effort: Effort
) -> ReviewPrep:
    try:
        with client.messages.stream(
            model=model,
            max_tokens=MAX_TOKENS,
            system=[
                {"type": "text", "text": SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}}
            ],
            messages=[{"role": "user", "content": render_pull_request(pr, first_artifact)}],
            output_config={"effort": effort},
            output_format=ReviewPrep,
        ) as stream:
            message = stream.get_final_message()
    except ValidationError as error:
        raise ReviewPrepError(f"Review prep for {pr.url} did not match the notes format") from error
    if message.stop_reason != "end_turn" or message.parsed_output is None:
        raise ReviewPrepError(f"Review prep for {pr.url} stopped early: {message.stop_reason}")
    return message.parsed_output


def render_pull_request(pr: PullRequest, first_artifact: bool) -> str:
    kind = "the fellow's first piece of work" if first_artifact else "follow-up work"
    parts = [
        f"This pull request is {kind}.",
        f'<pull_request url="{pr.url}" author="{pr.author}">',
        f"<title>{pr.title}</title>",
        f"<description>\n{pr.body}\n</description>",
        "<diff>",
    ]
    budget = DIFF_BUDGET_CHARS
    omitted = []
    for file in pr.files:
        patch = file.patch or "(no text diff: binary, renamed, or too large)"
        if len(patch) > budget:
            omitted.append(file.path)
            continue
        budget -= len(patch)
        parts.append(
            f'<file path="{file.path}" status="{file.status}" '
            f'additions="{file.additions}" deletions="{file.deletions}">\n{patch}\n</file>'
        )
    parts.append("</diff>")
    if omitted:
        parts.append("<omitted_files>\n" + "\n".join(omitted) + "\n</omitted_files>")
    parts.append("</pull_request>")
    return "\n".join(parts)
