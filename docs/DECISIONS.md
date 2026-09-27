# Decisions

This document records why non-obvious choices were made. See [SYSTEM.md](SYSTEM.md) for mechanisms, [DOMAIN.md](DOMAIN.md) for shared language, [ROADMAP.md](ROADMAP.md) for unfinished commitments, and [CHANGELOG.md](CHANGELOG.md) for shipped changes.

### Review prep explains before it judges — 2026-09-27

**Decision:** review prep opens with a glance line (the problem and the fix, one plain sentence each), then plain-language context (what the project does, what this code is responsible for, and why the change matters) and a glossary of the terms the lead needs. The verdict comes after that. The coaching question comes with the points a strong answer covers, which are for the lead only. Notes for the lead are in plain language. The draft comment, which is written for the fellow, stays technical but casual.

**Why:** the lead mentors across ten stacks as a generalist. After running review prep on three real pull requests, the lead asked to understand the system before reading a verdict, and asked for a slightly more casual draft (v2). After v2, the lead asked for something readable at a glance, and for an answer to the coaching question so they can guide the conversation (v3).

**Ruled out / alternatives:** a separate explanation call, which would cost more and add latency for the same content; and a fixed, shared glossary, which wouldn't fit because the terms change with every stack.

**Status:** Settled. Tone will keep being tuned from the lead's edits to real drafts.

### Rules in code, judgment in Claude — 2026-09-27

**Decision:** Timers, coverage checks, ordering, and state changes are plain, tested code. Claude only produces judgment: review notes, drafts, and pattern proposals. Its output goes through structured outputs and Pydantic validation, and it is never trusted if it's malformed or cut off. Prompts are versioned files.

**Why:** the lead has to trust the system without re-checking it. Deterministic rules give the same answer every time and can be unit-tested. Validated outputs make failures loud instead of silent, and versioned prompts make every note traceable and every change testable against evals.

**Ruled out / alternatives:** a free-running agent that decides what to check. It is harder to test, and it could skip a promise without anyone noticing.

**Status:** Settled.

### Review prep on Claude Opus 5.5 at high effort — 2026-09-27

**Decision:** review prep uses `claude-opus-5-5` with effort `high`. Both can be changed through the `REVIEW_MODEL` and `REVIEW_EFFORT` settings.

**Why:** the lead asked for the strongest reviewer. The 24-hour review window makes latency cheap compared with missed issues.

**Ruled out / alternatives:** a cheaper model or lower effort by default. That's possible later, but only if evals show equal catch rates.

**Status:** Open. Revisit once the practice-PR scorecard compares effort levels on cost and catch rate.

### Pilot on fake fellows and real public PRs — 2026-09-27

**Decision:** the pilot maps made-up fellows to real contributors' public pull requests in open-source projects run by mission-driven organizations. The app reads those pull requests and never comments on them.

**Why:** real code and real reviewers test the system honestly: the maintainers' later reviews become the answer key. Synthetic fellows keep real employee data out until CodePath approves data use.

**Ruled out / alternatives:** fully synthetic pull requests, which are too clean to reveal real failures; and waiting for real fellows, which is too late to earn trust before Foundations.

**Status:** Settled.

### Nothing is deleted — 2026-09-27

**Decision:** the app has no delete. Completed items move to an archive organized by week, by fellow, and by plan deliverable. A weekly export is kept outside Notion.

**Why:** the record doubles as the lead's performance evidence, and history must survive mistakes.

**Ruled out / alternatives:** clearing completed items, which loses the evidence.

**Status:** Settled, with one exception: deletion that CodePath policy requires, such as raw recordings after a retention window. In that case the app keeps the summary.

### Talk to it through Claude with the Notion connector — 2026-09-27

**Decision:** the lead asks questions and requests changes in Claude, connected to the Notion workspace, guided by a "Guide for Claude" page. Changes Claude makes count as the lead's own edits.

**Why:** it works from day one with nothing to build, including on the phone and by voice.

**Ruled out / alternatives:** a custom chat connector now. It stays an option if answers need data that isn't in Notion.

**Status:** Settled for v1.

### Python over TypeScript — 2026-09-27

**Decision:** build in Python 3.14 with uv, Pydantic, and the official Anthropic SDK.

**Why:** the lead reviews every change and reads Python more easily. The hardest parts of the project are evals and scorecards, where Python is strongest.

**Ruled out / alternatives:** TypeScript, the lead's main language, which has official Notion and GitHub SDKs. It was closely matched on everything else.

**Status:** Settled.

### Pilot on the lead's Railway plan, production on CodePath accounts — 2026-09-27

**Decision:** host the pilot on the lead's Railway Hobby plan. Move Railway, the Anthropic key, the GitHub app, and Notion to CodePath-owned accounts before any real fellow data.

**Why:** the pilot handles only public code and synthetic fellows. The spec requires organization-owned accounts for production.

**Ruled out / alternatives:** waiting for CodePath accounts before building, which would stall the 30-day deliverable.

**Status:** Settled for the pilot.

### Recording 1:1s — 2026-09-27

**Decision:** 1:1s are recorded in Zoom. A transcript turns into a drafted debrief only after CodePath approves recording, storage, retention, and AI processing, and after each fellow opts in in writing. Each fellow has a switch, and there is an "off the record" control.

**Why:** the spec says consent alone is not enough. Fellows are employees, some states require all-party consent, host NDAs may apply, and the mentor's authority makes a verbal "yes" weak. Zoom's own consent prompt and transcript webhook make the approved path fully automatic.

**Ruled out / alternatives:** recording on by default with a verbal notice, which is what the lead wants. It is not ruled out: it is pending CodePath's answer.

**Status:** Open until CodePath and Legal respond.

### Calendar source — 2026-09-27

**Decision:** read 1:1 bookings from Calendly, and other meetings through Google access approved by CodePath's admin. Don't share the work calendar to a personal account.

**Why:** personal-account sharing moves fellow data outside organization-owned accounts, and Workspace often limits external sharing to free/busy.

**Ruled out / alternatives:** sharing to a personal account; the calendar's private iCal link, which is kept as a fallback if CodePath allows it.

**Status:** Open until CodePath's Google admin answers.

### Build our own service instead of Claude Code routines — 2026-09-26

**Decision:** a Python service in this repository, hosted on Railway.

**Why:** routines were in research preview and capped at 15 or 25 runs a day. They run without approval prompts, act as the lead's personal identity, and belong to a personal account. An own service can make "never sends" structural, give the app its own identity in Notion, and run on CodePath-owned accounts.

**Ruled out / alternatives:** Claude Code routines, and Managed Agents, which remain a hosting option if Railway ever falls short.

**Status:** Settled.

### Decision support only: the app drafts and never sends — 2026-09-26

**Decision:** the app never posts reviews, messages fellows or hosts, makes performance determinations, or escalates. It drafts, and the lead decides and sends.

**Why:** it's the project spec. The lead stays accountable for everything that reaches a person.

**Ruled out / alternatives:** auto-posting reviews or messages, even with human review afterwards.

**Status:** Settled. See [how it's enforced](SYSTEM.md#why-cant-the-app-post-or-send-anything).
