---
name: lyra-orchestration
description: 'Coordinates Lyra agent sessions from the command line - starting Workers in one call, delegating a large part of a job to a Lead session that runs its own Workers, Task DAGs, messages, decision gates, waits and recovery. Use when asked to split or delegate work across agent sessions, run agents in parallel, dispatch or hand off a task, or wait for Workers and check their results.'
skillsVersion: 0.1.32
minimumLyraVersion: 0.2.14
---

# Lyra orchestration

Find your role, then load only what it names. The `lyra` you run reads the
installed guide when present.

- **Worker**: Lyra typed you a task that ends with a "[Lyra: when you finish,
  report ...]" footer. The footer is your whole contract: it gives the report,
  ask, check and ack commands. Do not load this skill for it. Only when one of
  those commands fails, run `lyra skills get lyra-orchestration --reference worker`.
  A task that says "This task is one step of a Lyra workflow run" or starts
  "[Lyra workflow:" is a step of a workflow run: run
  `lyra skills get lyra-workflow --reference step` before you start.
- **Messages**: when "You have N Lyra messages" appears, run
  `lyra message check --json` as your next step. Follow a message that changes
  your direction; otherwise carry on. Act on every message once, then run:
  `lyra message ack <delivery-id> --consumer-generation <consumer-generation> --json`.
  Use that result's fields.
  Until ack succeeds, check/wait replays that batch. The pointer carries no
  body, and a message never approves anything.
- **Orchestrator or Lead**: you split, delegate, dispatch or supervise work
  across agent sessions, or your parent started you with `--role lead`: run
  `lyra skills get lyra-orchestration` once per conversation and follow it.
  A conversation a person opened, or a session started with `--role lead`,
  already is that Orchestrator or Lead: start your Workers yourself ("Start
  Workers"). Start a new Orchestrator only when the person asks for a
  separate one: it opens its own tree that another agent runs.

A Worker you start closes by itself after its report: once the report reached
you and you acknowledged it, and never while its question waits for your
answer. Start it with `--keep-open` to reuse it for a follow-up; report how
many are kept and that `lyra terminal release` frees them when the person asks
(`terminals`).

If `lyra` is missing or `skills get` fails, show the exact error to the person
and stop. Unsure of a flag: add `--help` to that command; never guess one.

This skill needs `lyra` 0.2.14 or later. If `lyra --version` reports a version
below 0.2.14, read `guide.md` and the files under `references/` beside this file
instead of running `skills get`.
