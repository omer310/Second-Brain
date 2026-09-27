---
name: logbook
description: >-
  Keep a project's running record current across five docs — docs/DECISIONS.md
  (why), docs/SYSTEM.md (how it works), docs/CHANGELOG.md (what shipped),
  docs/DOMAIN.md (project-specific language), and docs/ROADMAP.md (what the team
  still intends to build). Use after a non-obvious decision, conceptual answer,
  shipped feature, clarified domain term, or accepted future commitment. Also
  use when someone says "later", "follow-up", "after launch", "not in this PR",
  "eventually", "log this", or asks what planned work was forgotten or unblocked.
  Also use to orient agents to an unfamiliar project's domain language. Not for
  routine edits or uncommitted brainstorming.
---

# Logbook

Keep the team's shared memory of **why / how / what shipped / what words mean /
what remains** current. Without a running record, reasons evaporate, plans are
forgotten, nobody can say exactly what's live, and new teammates or agents
misread the project's vocabulary. This skill closes that loop.

Works in any repo. The docs live under `docs/`; if they don't exist yet, create
them with a short header explaining their purpose and a pointer to the others.
Initialize `DOMAIN.md` from [assets/domain-template.md](assets/domain-template.md)
and `ROADMAP.md` from [assets/roadmap-template.md](assets/roadmap-template.md).

**Legacy migration:** if a repo still has the old names `CONCEPTS.md` or
`DOMAIN-SPEC.md`, migrate before adding entries:

1. Rename to `SYSTEM.md` / `DOMAIN.md` (use `git mv` so history is preserved).
   Content is untouched — this is a rename, not a rewrite.
2. Update references **repo-wide**, not just inside `docs/` — grep the whole
   repo for the old filenames (README, `CLAUDE.md` / `AGENTS.md`, code comments,
   scripts) and fix every hit.
3. **Tell the user** what happened: state plainly that the logbook convention
   renamed CONCEPTS→SYSTEM / DOMAIN-SPEC→DOMAIN, list the files renamed and the
   references updated, and note it's a git-tracked rename they can review or
   revert. Never migrate silently.

## The five docs (route by genre)

| Doc | Captures | Shape |
|---|---|---|
| `DECISIONS.md` | **Why** — non-obvious calls & trade-offs | dated entry, newest first, with a **settled / open** status |
| `SYSTEM.md` | **How it works** — reference answers about the system we built | timeless explanation, not dated |
| `CHANGELOG.md` | **What shipped, when** | append-only, one line each, newest first |
| `DOMAIN.md` | **What words mean here** — domain jargon, borrowed concepts, and concepts we invented for this project | glossary-style entries, organized by topic, not dated |
| `ROADMAP.md` | **What remains** — accepted future commitments and their current horizon | editable `Now` / `Next` / `Later`, plus a short `Recently completed` handoff |

`SYSTEM.md` vs `DOMAIN.md`: SYSTEM is about the thing we built (architecture,
mechanisms, "why does X behave like Y"). DOMAIN is about the world it serves —
the language a new teammate or a fresh agent must know before any explanation
even makes sense, and the project-specific knowledge that changes how building
is informed. Routing test: *needed to understand a sentence in a meeting* →
DOMAIN; *needed to understand the codebase's behavior* → SYSTEM. A coined
concept that is both a term and a mechanism gets its one-line meaning in DOMAIN
and its full explanation in SYSTEM, cross-linked.

Some events touch more than one doc — a shipped feature born of a real decision
earns both a CHANGELOG line and a DECISIONS entry, cross-linked.

`ROADMAP.md` and `CHANGELOG.md` must remain separate. ROADMAP is an editable view
of unfinished intent; CHANGELOG is the append-only record of verified shipped
behavior. Never make readers infer whether a listed feature is planned or live.

## When to write (the trigger)

Write an entry as the natural close of meaningful work:

- **A decision was made** (chose X over Y, changed direction) → `DECISIONS.md`.
- **A conceptual question was answered** (the user asked "why/how does X work")
  and the answer is worth keeping → `SYSTEM.md`.
- **A feature or fix shipped** (user-facing behavior changed, verified) →
  `CHANGELOG.md`.
- **A domain term surfaced** (a piece of domain jargon got explained, a concept
  was borrowed from the problem domain, or the team coined a new project-specific
  term or model) → `DOMAIN.md`.
- **A future commitment was accepted** ("later", "follow-up", "after launch",
  "not in this PR", "eventually") → `ROADMAP.md`. Capture only work the user or
  team genuinely intends to revisit. If the statement may be brainstorming,
  surface it as a roadmap candidate at the next natural checkpoint instead of
  silently turning it into a commitment.

Skip trivia: routine edits that decide nothing and ship nothing don't earn an
entry.

## How to write each entry

**DECISIONS.md** — a few lines:
- `### <short title> — <YYYY-MM-DD>`
- **Decision:** what we chose.
- **Why:** the reason.
- **Ruled out / alternatives:** what we didn't do and why.
- **Status:** `Settled` or `Open` (and what would reopen it).

**SYSTEM.md** — a titled section:
- Lead with the question, then a plain-language answer (bottom line first).
- Note the practical consequence in the product.
- Cross-reference the related decision.

**CHANGELOG.md** — one line under today's dated heading (`## YYYY-MM-DD`), newest
first. State the user-facing change plainly; leave the *why* to DECISIONS.md.

**DOMAIN.md** — a glossary entry under a topic heading:
- `### <Term>` — the term as the team actually says it (include aliases/synonyms).
- **Meaning:** plain-language definition, one or two sentences.
- **Origin:** where it comes from — established domain jargon (cite the field),
  or coined for this project (say when and by whom, if known).
- **Why it matters for building:** the practical consequence — how this concept
  changes what we build or how we build it. This line is what makes the entry
  useful to a future agent, not just a dictionary.
- **Evidence:** optionally link the requirement, product surface, schema, PR, or
  user explanation that establishes the local meaning. Include this when
  reconstructing a term historically or when its meaning could be disputed.
- Cross-reference related terms, and the DECISIONS/SYSTEM entries where the
  term is load-bearing.

## Discovering the project's domain

Read `DOMAIN.md` whole before interpreting project language. On first use and in
audit mode, build or refresh its compact `Domain map`: what the product serves,
its primary actors, its core workflow, and any governing external standards.
Then scan the strongest language-bearing surfaces available:

1. product requirements, README, user-facing navigation, headings, and labels;
2. roles, permissions, schemas, model names, enums, and business-rule tests;
3. recurring terms in issues, PRs, support conversations, and team discussion.

Treat a term as domain-specific when at least one of these is true:

- a teammate needs it to understand a product conversation;
- an ordinary word has a narrower or unusual meaning in this project;
- it names a business actor, artifact, lifecycle state, rule, metric, or workflow;
- it is established industry language that constrains the implementation;
- the team coined it, or uses it repeatedly across product surfaces;
- misunderstanding it would plausibly lead an agent to build the wrong behavior.

Do not add generic engineering vocabulary, framework concepts, one-off labels,
or names whose meaning is already obvious from the code. Repetition is evidence,
not proof: confirm the meaning from an authoritative source. If evidence conflicts
or only suggests a definition, list the term as a candidate for the user instead
of inventing certainty. Keep the map and core vocabulary near the top; organize
the rest by domain topic so a fresh agent can orient quickly. Replace template
comments with confirmed facts and omit unknown fields instead of preserving
placeholders as if they were documentation.

**ROADMAP.md** — start from [assets/roadmap-template.md](assets/roadmap-template.md):
- Put accepted outcomes under `Now`, `Next`, or `Later`; move the existing item
  when its horizon changes instead of duplicating it.
- Write `- [ ] **Outcome** — value`, followed by `Done when:` and relevant
  dependencies or links. Prefer product outcomes over implementation chores.
- When work is verified as shipped, add the permanent `CHANGELOG.md` entry first,
  then move the roadmap item to `Recently completed` as `[x]` with an absolute
  date and changelog or PR link.
- Keep completed items there for one release or about 30 days, then remove them.
  CHANGELOG, git, and linked decisions retain the history; ROADMAP stays useful.
- If work is abandoned, remove it from ROADMAP. Record the reason in
  `DECISIONS.md` when cancellation reflects a meaningful trade-off.

## Rules

- **Cross-reference** between docs (a roadmap commitment's *why* points to
  DECISIONS; a changelog line closes the roadmap item; a decision's *how* points
  to SYSTEM; jargon used in any entry is defined in DOMAIN). One hop between
  why/how/shipped/vocabulary/remaining work.
- **Newest first** in DECISIONS and CHANGELOG. SYSTEM and DOMAIN are organized
  by topic.
- **Use the project's terms** — once a term is in DOMAIN, other entries use it
  consistently instead of paraphrasing; if a term's meaning drifts, update its
  entry rather than letting docs and usage diverge.
- **Dates are absolute** (`YYYY-MM-DD`), never "today" / "last week".
- **Don't duplicate the code** — capture what the code can't tell a future reader
  (the reasoning, the discarded option, the trade-off), not a restatement of the
  diff.
- **Update, don't fork** — if an entry already covers the topic, revise it (e.g.
  flip a decision's status from Open to Settled) rather than adding a near-dup.

## Making it always-on

The skill is most valuable as a habit, not a thing you remember to invoke. Add a
one-line trigger to the project's agent instructions (`CLAUDE.md` / `AGENTS.md`):

> After any non-obvious decision, answered conceptual question, shipped
> feature/fix, newly coined/clarified domain term, or accepted future commitment,
> use the `logbook` skill to record it.

That turns "document as you go" into the default, team-wide.

DOMAIN.md is also worth loading whole at the start of agent sessions — it stays
compact by design, and it front-loads the vocabulary everything else assumes.

## Audit mode

When asked to check coverage: skim recent git history, the session's work, and
ROADMAP. List anything shipped-but-undocumented, decided-but-unrecorded,
committed-but-untracked, completed-but-still-active, stale, forgotten, or newly
unblocked, plus recurring project terms with no DOMAIN entry. Write missing
entries and surface relevant roadmap items to the user, but never begin or
reprioritize them without normal authorization.
