# Domain

This document defines the language a teammate or agent needs before interpreting requirements, product behavior, or implementation choices. Use these terms consistently. See [SYSTEM.md](SYSTEM.md) for how the system works, [DECISIONS.md](DECISIONS.md) for why trade-offs were made, [ROADMAP.md](ROADMAP.md) for unfinished commitments, and [CHANGELOG.md](CHANGELOG.md) for shipped changes.

## Domain map

- **What this product serves:** an AI Practice Lead in CodePath's Claude Corps program (run with Anthropic) who mentors about 20 early-career engineers at mission-driven host organizations and needs every fellow, pull request, promise, and pattern tracked without doing the bookkeeping.
- **Primary actors:** the lead (the user); fellows, grouped in pods; host supervisors; the Senior Manager of AI Practice (Mike covers the role until it is hired); CodePath's fellow comms owner (Kelly); the curriculum team; Anthropic CSMs and applied-AI engineers.
- **Core workflow:**
  1. Fellows open pull requests, write weekly reflections, and meet the lead in 1:1s.
  2. The app prepares review notes and checks the lead's promises every morning.
  3. The lead reviews, edits, and sends everything themselves.
  4. The app files the outcomes, drafts patterns weekly, and drafts hand-ups when rules trigger.
- **External standards:** the lead's 30-60-90 plan, which sets the formats and timers; CodePath's triage framework for escalations (pending); CodePath's data-use, consent, and recording rules (pending).

## People and places

### Fellow

**Meaning:** an early-career engineer in the program, employed by CodePath and placed at a host organization. The lead mentors about 20.

**Origin:** Claude Corps program language.

**Why it matters for building:** fellow records are sensitive employee data. Until CodePath approves data use, the app runs only on synthetic fellows (see [the pilot decision](DECISIONS.md#pilot-on-fake-fellows-and-real-public-prs--2026-09-27)).

### Pod

**Meaning:** the fellows placed together at one host organization, usually two.

**Origin:** Claude Corps program language.

**Why it matters for building:** trainings, demos, and supervisor updates happen per pod, and one fellow's absence shifts work to podmates.

### Host organization

**Meaning:** the nonprofit or public-interest organization where a pod works. Also "host".

**Origin:** Claude Corps program language.

**Why it matters for building:** fellows' code lives in host repositories, so reading it requires each host's approval of a read-only GitHub app.

### Host supervisor

**Meaning:** the person at a host who directs the pod's work. Each supervisor told the lead how and how often they want updates.

**Origin:** Claude Corps program language.

**Why it matters for building:** supervisor updates are drafted on each supervisor's own cadence and channel, never sent by the app.

### Bench fellow

**Meaning:** one of about five fellows who may be placed at an Anthropic office instead of a host, with a CSM as support buddy.

**Origin:** CodePath's fellow comms plan, 2026.

**Why it matters for building:** the data model can't assume every fellow has a host.

## Program timeline

### Foundations

**Meaning:** the two async weeks before Basecamp (Oct 19–30, 2026 for Cohort 1). The comms plan calls it pre-Basecamp.

**Origin:** the lead's 30-60-90 plan; CodePath's comms plan.

**Why it matters for building:** the first real checks run here: weekly contact, reflections answered within 48 hours, quiet fellows flagged by day 5.

### Basecamp

**Meaning:** the in-person week before fellows start at hosts (Nov 2–6, 2026), ending with a Day-5 panel where each pod presents.

**Origin:** Claude Corps program language.

**Why it matters for building:** the lead writes a calibration note on every fellow by its Friday night.

### Milestone check-in

**Meaning:** documented check-ins 30, 60, 90, and 120 days after a fellow's Day 1 at the host. The Day-30 check-in ends with an on-track or at-risk call and a 60-day plan.

**Origin:** CodePath's comms plan and the lead's 30-60-90 plan.

**Why it matters for building:** the lead makes the fellow-level call; the Senior Manager owns the roll-up and any formal decision. A fellow's "90-day" check-in is not the lead's own 90-day review.

## Reviewing work

### First piece of work

**Meaning:** a fellow's first real artifact at the host, usually a pull request. Also "first artifact".

**Origin:** the lead's 30-60-90 plan.

**Why it matters for building:** it gets the lead's written review within 24 hours, with exactly three structured points, one piece of real praise, and one open coaching question.

### Review prep

**Meaning:** the app's notes for a pull request: a one-line verdict, what changed, tiered findings, praise, a coaching question, and a draft comment the lead edits and posts.

**Origin:** coined for this project, 2026-09-26.

**Why it matters for building:** it is a draft for the lead, never posted by the app. See [how it works](SYSTEM.md#how-does-review-prep-work).

### Finding tier

**Meaning:** how much a finding matters: must fix (blocks merging), clarify (the fellow should explain before merging), or later (worth doing, doesn't block).

**Origin:** the lead's 30-60-90 plan, which separates must-fix from later.

**Why it matters for building:** each finding is written as question, then risk, then suggested change, so the review teaches instead of commanding.

### Practice PR

**Meaning:** a real, public, open-source pull request used to test the system before real fellows arrive.

**Origin:** the lead's 30-60-90 plan, whose first deliverable is the Second Brain used on at least five practice PRs.

**Why it matters for building:** practice PRs are read, never commented on. Their real reviewers' comments become the answer key.

### Answer key

**Meaning:** what the real maintainers said about a practice PR, used to score the app's review prep.

**Origin:** coined for the simulation, 2026-09-26.

**Why it matters for building:** it is the ground truth for evals. The app must be scored on the PR as it stood before the maintainers reviewed it.

## Coaching rhythm

### Debrief

**Meaning:** the lead's written note after a 1:1: wins, gap, next bet, and open question, written within 24 hours.

**Origin:** the lead's 30-60-90 plan.

**Why it matters for building:** a missing debrief after 24 hours is a safety-net failure, and promises made in a 1:1 become follow-ups.

### Pre-brief

**Meaning:** the app's two-minute summary before a 1:1: what happened since last time, the fellow's own words, questions to try, and what to avoid.

**Origin:** the lead's 30-60-90 plan names the template; the format was designed in the simulation.

**Why it matters for building:** it draws on everything the app knows about the fellow, so restricted items must never leak into it.

### Reflection

**Meaning:** a fellow's weekly written reflection. The lead answers each one within 48 hours.

**Origin:** the lead's 30-60-90 plan; CodePath's comms plan starts weekly reminders on Nov 9.

**Why it matters for building:** where fellows submit reflections is not confirmed yet (likely Commons), so the source is still an open input.

### Calibration note and baseline read

**Meaning:** the calibration note is the lead's written read on each fellow at Basecamp. The baseline read is logged in Sprint 1, after the first piece of work, so growth can be measured.

**Origin:** the lead's 30-60-90 plan.

**Why it matters for building:** both feed the Day-30 check-in and are evidence for the lead's own deliverables.

## Safety and escalation

### Quiet fellow

**Meaning:** a fellow with no contact or activity for five days. The plan wants them flagged by day five, not week three, and calls late detection "the simulation's clearest finding".

**Origin:** the lead's 30-60-90 plan.

**Why it matters for building:** day five triggers a drafted P2 hand-up with wellbeing-first wording. The lead decides whether to send it.

### Hand-up

**Meaning:** a deliberate escalation from the lead to the Senior Manager, written before the conversation and with a recommendation attached.

**Origin:** the lead's 30-60-90 plan.

**Why it matters for building:** the app drafts hand-ups and keeps the escalation log. It never escalates on its own.

### Escalation tier

**Meaning:** P0 to P3 severity for issues about a fellow. P2s are logged for the manager to see; P1 and P0 go only to the restricted route.

**Origin:** CodePath's triage framework, which is still pending.

**Why it matters for building:** thresholds must come from that framework, not be invented. Until then only the plan's stated rules apply.

### Restricted route

**Meaning:** the locked-down place for wellbeing, health, safety, and formal employment matters.

**Origin:** the project spec.

**Why it matters for building:** restricted items never appear in Today, digests, pre-briefs, or briefs, and never go to the model for general processing.

### Safety net

**Meaning:** the morning checks of the lead's promises: weekly contact, debriefs within 24 hours, reflections within 48 hours, quiet fellows, review deadlines, owners and due dates, and source health.

**Origin:** coined in the simulation, 2026-09-26.

**Why it matters for building:** these are deterministic rules in code, and any failure becomes an item on the Today list.

## Patterns and records

### Pattern

**Meaning:** a problem seen across fellows. Three fellows with the same problem make it systemic, and the plan routes it: curriculum to the curriculum team, technical depth to a partner expert or applied-AI engineer, host issues to the CSM, delivery or performance to the Senior Manager, program efficacy to Mike.

**Origin:** the lead's 30-60-90 plan.

**Why it matters for building:** the app drafts patterns weekly with evidence. The lead confirms each one and its owner.

### Roll call

**Meaning:** the Friday per-fellow check that every promise held that week.

**Origin:** coined in the simulation, 2026-09-26.

**Why it matters for building:** it feeds the weekly brief and the evidence for the lead's own deliverables.

### 🤖 field

**Meaning:** a Notion field the app owns and rewrites. Every other field belongs to the lead and is never overwritten.

**Origin:** coined for the Notion mockup, 2026-09-26.

**Why it matters for building:** the lead's changes always win, and it is always clear what the app wrote. See [the drafting decision](DECISIONS.md#decision-support-only-the-app-drafts-and-never-sends--2026-09-26).
