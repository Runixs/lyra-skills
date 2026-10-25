---
name: lyra-workflow
description: 'Works inside Lyra workflows - as one step of a workflow run, as a helper who watches a run for the person, or as the author of a workflow - moving on recorded evidence instead of questions. Use when a task Lyra typed says "This task is one step of a Lyra workflow run" or starts with "[Lyra workflow:", when asked to watch or explain a workflow run, or when asked to make, change, explain or draw a Lyra workflow from a description of the work or from the history of a finished project.'
skillsVersion: 0.1.23
minimumLyraVersion: 0.2.2
---

# Lyra workflow

A workflow is a file of steps saved in Lyra; each run of it walks the steps,
and every attempt, output and choice record stays with the run. Find your
part, then load only what it names:

- **Step**: Lyra typed you a task whose closing lines, after a line of three
  dashes, say "This task is one step of a Lyra workflow run", or whose first
  line starts "[Lyra workflow:". You are one step of a run.
  Before you start, run
  `lyra skills get lyra-workflow --reference step` and follow it. In a run
  nobody answers a question: that overrides asking in the `lyra-orchestration`
  Worker reference.
- **Watching a run**: a person asks you to follow, explain or check a run.
  Run `lyra skills get lyra-workflow`, then
  `lyra skills get lyra-workflow --reference orchestrator`.
- **Author**: a person asks you to make, change, explain or draw a workflow,
  from a description of the work or from a finished project's history. Run
  `lyra skills get lyra-workflow`, then
  `lyra skills get lyra-workflow --reference authoring`.

If `lyra` is missing or `skills get` fails, show the exact error to the person
and stop; as a step, follow the task's closing lines instead. Unsure of a
flag: add `--help` to that command; never guess one.

This skill needs `lyra` 0.2.2 or later. If `lyra --version` reports a version
below 0.2.2, read `guide.md` and the files under `references/` beside this
file instead of running `skills get`.
