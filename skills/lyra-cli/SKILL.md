---
name: lyra-cli
description: Operates Lyra from the command line - Projects, Workspaces, agent Sessions, terminals, workspace files and Git, the Inbox, Hosts, servers, credentials and Profiles - and installs Lyra's bundled skills. Use when asked to register a project, create or remove a workspace, open, prompt or close an agent session, read a workspace's files or Git state, start, type into, read or stop a shell terminal, attach to or split a terminal, connect a remote server, or install a Lyra skill for an agent.
---

# Lyra CLI

The `lyra` command prints the guide that matches its own commands. Before your
first Lyra command in a conversation, run `lyra skills get lyra-cli` and follow
it. When it names a reference for your next step, load only that one with
`lyra skills get lyra-cli --reference <name>`.

A task Lyra typed into your terminal with a report footer, a "You have N Lyra
messages" line, or several agent sessions to coordinate belong to the
`lyra-orchestration` skill.

If `lyra` is missing or `skills get` fails, show the exact error to the person
and stop. Unsure of a flag: add `--help` to that command; never guess one.
