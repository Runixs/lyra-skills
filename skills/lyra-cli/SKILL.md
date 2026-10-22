---
name: lyra-cli
description: Operates Lyra from the command line - Projects, Workspaces, agent Sessions, terminals, workspace files and Git, the Inbox, Hosts, servers, credentials and Profiles - and installs Lyra's bundled skills. Use when asked to register a project, create or remove a workspace, open, prompt or close an agent session, read a workspace's files or Git state, start, type into, read or stop a shell terminal, attach to or split a terminal, connect a remote server, or install a Lyra skill for an agent.
skillsVersion: 0.1.16
minimumLyraVersion: 0.1.44
---

# Lyra CLI

The `lyra` command reads the installed guide when present. Before your
first Lyra command in a conversation, run `lyra skills get lyra-cli` and follow
it. When it names a reference for your next step, load only that one with
`lyra skills get lyra-cli --reference <name>`.

A task Lyra typed into your terminal with a report footer, a "You have N Lyra
messages" line, or several agent sessions to coordinate belong to the
`lyra-orchestration` skill.

If `lyra` is missing or `skills get` fails, show the exact error to the person
and stop. Unsure of a flag: add `--help` to that command; never guess one.

This skill needs `lyra` 0.1.44 or later. If `lyra --version` reports a version
below 0.1.42, read `guide.md` and the files under `references/` beside this file
instead of running `skills get`.
