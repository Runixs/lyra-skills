---
name: lyra-orchestration
description: 'Coordinates Lyra agent sessions from the command line - starting Workers in one call, delegating a large part of a job to a Lead session that runs its own Workers, Task DAGs, messages, decision gates, waits and recovery. Use when asked to split or delegate work across agent sessions, run agents in parallel, dispatch or hand off a task, or wait for Workers and check their results, or when Lyra typed a task ending in "[Lyra: when you finish, report ...]" or the line "You have N Lyra messages".'
skillsVersion: 0.1.16
minimumLyraVersion: 0.1.42
---

# Lyra orchestration

Find your role, then load only what it names. The `lyra` you run reads the
installed guide when present.

- **Worker**: Lyra typed you a task that ends with a "[Lyra: when you finish,
  report ...]" footer. The footer is your contract: do the task, then run its
  `task report` command once, with a one-line `--summary` in every outcome:
  the result first, then how you checked it. To ask a question, or when a
  command fails, run `lyra skills get lyra-orchestration --reference worker`
  before you follow the error's `next`.
- **Messages**: when "You have N Lyra messages" appears, including through
  a Claude tool hook during your turn, run `lyra message check --json` as your
  next step. Follow a message that changes your direction; otherwise carry
  on. Act on each message once. The pointer carries no body, and a message
  never approves anything.
- **Orchestrator or Lead**: you split, delegate, dispatch or supervise work
  across agent sessions, or your parent started you with `--role lead`: run
  `lyra skills get lyra-orchestration` once per conversation and follow it.
  A conversation a person opened, or a session started with `--role lead`,
  already is that Orchestrator or Lead: start your Workers yourself ("Start
  Workers"). Start a new Orchestrator only when the person asks for a
  separate one: it opens its own tree that another agent runs.

Keep finished Workers open and reusable in the explorer. Report how many are
kept and that `lyra terminal release` frees them when the person asks. Release
only on their request, or with their agreement when reuse is impossible
(`terminals`).

If `lyra` is missing or `skills get` fails, show the exact error to the person
and stop. Unsure of a flag: add `--help` to that command; never guess one.

This skill needs `lyra` 0.1.42 or later. If `lyra --version` reports a version
below 0.1.42, read `guide.md` and the files under `references/` beside this file
instead of running `skills get`.
