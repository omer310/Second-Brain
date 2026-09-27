# Changelog

This append-only document records verified shipped changes, newest first. See [ROADMAP.md](ROADMAP.md) for unfinished commitments and [DECISIONS.md](DECISIONS.md) for why changes were chosen.

## 2026-09-27 — local build, not deployed

- Review prep v3 opens with a one-sentence problem and fix you can take in at a glance, and adds what a strong answer to the coaching question covers, for the lead only. Unit tests pass; not yet run live.
- Review prep v2 opens with plain-language context and a glossary of the terms the lead needs, before the verdict. The draft comment is a little more casual, and the prompt asks for backticks instead of double quotes to stop text being cut off. The lead ran it live on civicrm-core #36857 and found it much better than v1. See [the decision](DECISIONS.md#review-prep-explains-before-it-judges--2026-09-27).
- Added on-demand review prep: `second-brain review <PR URL>` reads a pull request read-only and asks Claude Opus 5.5 for a verdict, tiered findings, praise, a coaching question, and a draft comment that is never posted. The lead ran it live on three practice PRs (kaapi-backend #1193, civicrm-core #36857, kpi #7627). All three returned complete notes, and #7627 caught the same DNS-rebinding risk the simulation had flagged. See [how it works](SYSTEM.md#how-does-review-prep-work).
- Added the project logbook (these five docs), the logbook skill, and agent instructions in `CLAUDE.md`.
