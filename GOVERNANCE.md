# Governance

This document describes how the Formation schemas project is governed.

The goal of governance is to keep the standard stable, neutral, and useful across implementations.

---

## Roles

### Maintainers
Maintainers are responsible for the health of the project and the integrity of the standard.

They:

- Review and merge pull requests.
- Cut releases.
- Enforce compatibility and versioning rules.
- Facilitate community discussions.

### Reviewers
Reviewers are trusted contributors who regularly review PRs and help maintain quality.

They:

- Provide technical feedback on schema and spec changes.
- Help ensure fixture and tooling coverage.

### Contributors
Anyone who participates by filing issues, opening PRs, improving docs or tooling.

---

## Decision making

### Default: lazy consensus
Most decisions are made by **lazy consensus**:

- A change is accepted if no maintainer objects within a reasonable window (usually 3–5 days for minor changes).

### When a vote is required
A vote is required for:

- Breaking changes (major version bumps).
- Governance updates.
- Maintainer additions/removals.
- Changes to the extension policy.

Voting rule:

- Simple majority of maintainers.
- In the event of a tie, the lead maintainer breaks the tie.

---

## Proposing changes

1. Open an issue describing the change and motivation.
2. Include:
   - problem statement
   - proposed schema/spec diff
   - compatibility impact
   - examples / fixtures
3. Submit a PR once there is rough agreement on direction.

---

## Adding maintainers

A contributor can become a maintainer if they:

- Have a sustained history of high-quality contributions.
- Demonstrate understanding of portability and compatibility goals.
- Are willing to review PRs and participate in releases.

Process:

1. Any maintainer may nominate a contributor.
2. Maintainers vote.
3. On approval, the nominee is added to `MAINTAINERS.md`.

---

## Removing maintainers

Maintainers can step down voluntarily at any time.

Inactivity process:

- If a maintainer is inactive for ~3 months, another maintainer may propose moving them to “emeritus.”
- Maintainers vote.
- Emeritus maintainers may return at any time with a maintainer vote.

---

## Project scope

In scope:

- Formation schemas and templates.
- Spec and versioning policy.
- Conformance fixtures.
- Validator / linter tooling.

Out of scope:

- Any specific runtime implementation.
- Commercial or restricted components from other ecosystems.
