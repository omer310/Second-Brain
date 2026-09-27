# System

This document explains how the Second Brain works. See [DECISIONS.md](DECISIONS.md) for trade-offs, [DOMAIN.md](DOMAIN.md) for shared language, [ROADMAP.md](ROADMAP.md) for unfinished commitments, and [CHANGELOG.md](CHANGELOG.md) for shipped changes.

## How does review prep work?

One command turns a pull request into review prep: `second-brain review <PR URL>`. It reads the pull request from GitHub, asks Claude for notes in a fixed shape, and prints them. It returns validated notes or an error, never partial notes.

1. The GitHub client fetches the pull request and every changed file, following pagination.
2. `render_pull_request` wraps the title, description, and diff in tags so the prompt can treat them as untrusted material. It includes patches until a 120,000-character budget is spent, then lists the remaining files by name so Claude knows what it didn't see.
3. The system prompt in `src/second_brain/prompts/review_prep.md` carries the lead's review format and priorities. It is cached, so reviewing several pull requests in a row costs less.
4. Claude Opus 5.5 answers at high effort through structured outputs, and the SDK validates the answer against the `ReviewPrep` schema. The request streams because long thinking plus long notes can exceed the SDK's ten-minute limit for non-streaming calls.
5. If the answer is cut off, refused, or doesn't validate, `prepare_review` raises `ReviewPrepError` instead of returning partial notes, and the command tells the lead to review that pull request manually.

The notes open with the problem and the fix in one sentence each, then context and a glossary, then the verdict, so a generalist lead understands the change before judging it. The coaching question comes with the points a strong answer covers, and those points never appear in the draft comment. See [that decision](DECISIONS.md#review-prep-explains-before-it-judges--2026-09-27).

Every result names the prompt version, the model, and the commit it reviewed, so any note can be traced back to what produced it. See [the design decision](DECISIONS.md#rules-in-code-judgment-in-claude--2026-09-27).

## Why does the review prompt ban double quotes inside fields?

Review notes come back as JSON. In one early review, a sentence stopped right after a double quote. The most likely cause is an unescaped quote closing the text early. Asking for backticks around code and literal values avoids the problem, and backticks render better in GitHub and Notion anyway. Keep that instruction unless the scorecard shows it's no longer needed.

## Why can't the app post or send anything?

The guarantee comes from the code, not the prompt. The GitHub client has no methods that write, and the token it uses is read-only. There are no messaging or email integrations. A prompt injection in a pull request can at worst change the notes the lead reads, and the lead checks those before anything leaves their hands. See [the decision](DECISIONS.md#decision-support-only-the-app-drafts-and-never-sends--2026-09-26).

## Where do secrets live?

`Settings` reads configuration from environment variables, or from a local `.env` file that git ignores. Keys are held as `SecretStr`, so they don't appear in logs or error messages. In deployment they are sealed Railway variables: the app receives them, but nobody can read them back from the dashboard, and swapping a key is a variable change plus a redeploy.
