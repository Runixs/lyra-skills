---
name: lyra-cli
description: Operates Lyra from the command line - Projects, Workspaces, agent Sessions, terminals, workspace files and Git, the Inbox, Hosts, servers, credentials and Profiles, Jira and GitHub connections and issues, workflows, and serial ports - and installs Lyra's bundled skills. Use when asked to register a project, create or remove a workspace, open, prompt or close an agent session, read a workspace's files or Git state, start, type into, read or stop a shell terminal, attach to or split a terminal, connect a remote server, add or poll a Jira or GitHub connection, show or comment on an issue, save, run or inspect a workflow, open, read, write or wait on a board's serial port, or install a Lyra skill for an agent.
skillsVersion: 0.1.27
minimumLyraVersion: 0.2.8
---

# Lyra CLI

The `lyra` command reads the installed guide when present. Before your
first Lyra command in a conversation, run `lyra skills get lyra-cli` and follow
it. When it names a reference for your next step, load only that one with
`lyra skills get lyra-cli --reference <name>`.

A task Lyra typed into your terminal with a report footer, a "You have N Lyra
messages" line, or several agent sessions to coordinate belong to the
`lyra-orchestration` skill. A step of a workflow run, watching a run, and
writing or drawing a workflow file belong to the `lyra-workflow` skill.

If `lyra` is missing or `skills get` fails, show the exact error to the person
and stop. Unsure of a flag: add `--help` to that command; never guess one.

This skill needs `lyra` 0.2.8 or later. If `lyra --version` reports a version
below 0.2.8, read `guide.md` and the files under `references/` beside this file
instead of running `skills get`.
