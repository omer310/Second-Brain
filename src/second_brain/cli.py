import argparse

from anthropic import Anthropic

from second_brain.github import GitHub, parse_pr_url
from second_brain.review import PROMPT_VERSION, ReviewPrep, ReviewPrepError, Tier, prepare_review
from second_brain.settings import Settings

TIER_LABELS = {Tier.MUST_FIX: "Must fix", Tier.CLARIFY: "Clarify", Tier.LATER: "Later"}


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="second-brain")
    commands = parser.add_subparsers(dest="command", required=True)
    review = commands.add_parser("review", help="Prepare review notes for a GitHub pull request.")
    review.add_argument("url", help="Pull request URL, e.g. https://github.com/owner/repo/pull/1")
    review.add_argument(
        "--first-artifact", action="store_true", help="Use the first-piece-of-work format."
    )
    args = parser.parse_args(argv)

    settings = Settings()
    github_token = settings.github_token.get_secret_value() if settings.github_token else None
    pr = GitHub(github_token).pull_request(*parse_pr_url(args.url))
    client = Anthropic(api_key=settings.anthropic_api_key.get_secret_value())
    try:
        prep = prepare_review(
            client,
            pr,
            first_artifact=args.first_artifact,
            model=settings.review_model,
            effort=settings.review_effort,
        )
    except ReviewPrepError as error:
        raise SystemExit(f"{error}. Review this pull request manually.") from error
    footer = f"{PROMPT_VERSION} · {settings.review_model} · commit {pr.head_sha[:7]}"
    print(format_review(prep, footer))


def format_review(prep: ReviewPrep, footer: str) -> str:
    lines = [f"Problem: {prep.problem}", f"Fix: {prep.fix}", "", f"Context: {prep.context}", ""]
    if prep.glossary:
        lines += ["Terms:", *(f"- {term.term}: {term.meaning}" for term in prep.glossary), ""]
    lines += [f"Verdict: {prep.verdict}", "", prep.what_changed, ""]
    for number, finding in enumerate(prep.findings, start=1):
        lines += [
            f"{number}. [{TIER_LABELS[finding.tier]}] {finding.location}",
            f"   Question: {finding.question}",
            f"   Risk: {finding.risk}",
            f"   Suggested change: {finding.suggested_change}",
        ]
    lines += [
        "",
        f"Praise: {prep.praise}",
        f"Coaching question: {prep.coaching_question}",
        "What a strong answer covers:",
        *(f"- {point}" for point in prep.coaching_answer),
        "",
        f"Estimated time: {prep.estimated_minutes} min",
        "",
        "Draft comment (not posted):",
        prep.draft_comment,
        "",
        footer,
    ]
    return "\n".join(lines)
