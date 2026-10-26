## Leads and peers

A **Lead** is a session working for an Orchestrator or Lead on a whole part of the job. It plans that
part, runs its own Workers, integrates and checks their work, and reports one
result. Its parent supervises one task; the Lead's Workers, messages and waits
stay in the Lead's own plan and conversation, so both conversations stay small.
Home records its `lead` role and parent. A Worker cannot start children.
Start a Lead with `--role lead`; a task description alone cannot change a role.
A Lead may start another Lead only where that new Lead's children still fit
within the configured depth limit. A new Orchestrator retains the Lead's depth.

### Give a part to a Lead (parent side)

Use a Lead for a part that needs several Workers or hours, or when you would
otherwise supervise more than about five Workers at once. A Lead is a full
session of its own, so never use one for what a single Worker can do. Start it
in its own Workspace, so its Workers share one branch the Lead owns:

```text
lyra worker start --role lead --project <project-id> --name <workspace-name> --spec-file lead.md --agent claude --title <title> --kind <kind> --json
```

Its spec adds these lines to the usual Goal, Scope and Acceptance:

```text
Role: You are a Lead. Run `lyra skills get lyra-orchestration`, read its lead reference, and run this part with your own Workers.
Budget: at most <N> Workers at once; agents <...>; about <time>
Decide yourself: <implementation choices>. Ask me first: <scope, behaviour, anything irreversible>
Deliver: one branch in your Workspace with the part integrated and the acceptance passing; your summary names the commit, the checks and what is left
Peers: <other Leads' session IDs and what to agree with them>, or "ask me"
```

Anything the parts share (an interface, a schema) goes on the base branch
before the Leads start, as a task of yours, so every Lead's Workspace has it
(on another host, once pushed and fetched there: the guide's Start Workers);
changes to it go through you. Start every Lead before you wait, then send each
one its peers' session IDs if they must agree on something. When the Leads
have reported, you (or one integration Worker) merge their branches and run the
acceptance across the parts. Wait and act as for any Worker: a Lead waiting on
its Workers sits in a running tool, so it reads as waiting, not stopped. A
`worker-stopped` from a Lead means its turn really ended.

If a Lead's session ends, its Workers keep running in its plan. On the person's
word a live session (yours, or a new Lead) takes them over, then decides each
task by its state (`recovery`):

```text
lyra task adopt --from <lead-session-id> --yes --json
lyra task list --json
```

### Be a Lead

You report to your parent like any Worker (the `worker` reference: footer,
summary, questions) and run your part like an Orchestrator (the guide). Also:

1. **Plan, then start.** Read your own task with `lyra task show <task-id> --json`; child tasks inherit no deadline. Explicitly keep each child deadline no later than yours, and respect its failed-attempt cap (`tasks`). Split your part by the guide's rule and start its
   Workers in your own Workspace (`--workspace current`), one writer per file set.
2. **Wait in the foreground, always:** loop
   `lyra task wait --all --timeout 9m --json` with your shell tool's time limit above
   it. Act on every message, then `message ack` its delivery/generation before
   waiting again. Until ack, it replays. Never end your turn while Workers run:
   your parent sees `worker-stopped`, then `worker-suspect`; after an hour a
   stall escalation holds dependent tasks. `worker-wait-too-long` after the
   tool limit (default 60 minutes) only tells the parent; it never acts.
3. **Ask your parent** what your spec does not let you decide: `message send`
   to the `result.task.ownerSessionId` of your own task, with your
   footer's task and attempt IDs. Keep waiting on your Workers; the answer
   arrives as a `message` event.
4. **Keep to your budget and authority.** Start no Leads of your own unless your
   spec allows it, and never more Workers at once than it allows.
5. **Integrate and check** in your Workspace: bring in each Worker's result,
   run the acceptance, and fix or re-dispatch what fails.
6. **Settle, then report once.** Keep finished Workers for reuse (`terminals`),
   report their count and `lyra terminal release` for the person's request.
   When `task wait` answers `idle`, report your own attempt with a summary,
   result first (your parent's notice shows its first 320 characters): the
   branch and commit, the checks and their results, one line per Worker task,
   and what is left.

### Peers

Sessions that work as equals (two Leads sharing an interface, or two
Orchestrators) each keep their own tasks and talk by message:
`message send --to <session-id>`. Write the agreement into a file both read
(an interface, a schema) rather than into long messages; a message wakes an
idle peer for a full turn, and a busy peer reads it at its next check. Your
`task wait` does not cover a peer's tasks, and Lyra does not link plans: a task
cannot depend on another session's task. Bring a conflict to the parent or the
person; never settle it by editing the other side's files.

## Re-link a session

Agents stay in their tree and never re-link themselves.

- `lyra session detach <session-id> --yes --json`: person or tree's Orchestrator.
  Irreversibly make a Lead's branch a new tree at depth 0; old starter/prompt
  ties end. Finish externally owned work first.
- `lyra session move <session-id> --to <parent-session-id> --json`: person,
  tree's Orchestrator, or Lead above both places. The branch must fit.
  Old-parent work transfers with a new owner generation; notices and waits follow.
  A person's move into another tree ends old starter/prompt ties as detach does;
  the old tree then sends it messages instead.
- `lyra session set-role <session-id> --role lead --json`: person, parent or
  tree's Orchestrator. Promotion needs child room; demotion no live children/open owned tasks.

Pending handoffs or ended targets refuse re-linking; adopt ended work (`recovery`).

## Reset a long session (V-289, V-380)

When your conversation grows long, write a note (the goal, decisions, task and attempt IDs, reset request ID,
and next step) to a file and run `lyra session reset <session-id> --resume-file <note-file> --request-id <request-id> --yes --json`.
The note must be UTF-8 and at most 16 KiB. At the session's next rest (its turn ended, no dialog open, no person
typing), Lyra types Claude Code's `/clear`, waits until the active conversation is the new one, then delivers
the note as its first input; its arrival means the reset is done. The same session keeps its ID, place in
the tree, owned tasks, running attempt and message address. Nothing moves.

Only Claude Code sessions support this: Codex, OpenCode and a daemon that does not serve clear are refused with
`session-reset-clear-unsupported`; nothing was done. Do not retry; keep working in the same session and tell
the person if it cannot go on. If the daemon does not serve clear, tell the person to update Lyra on that host.
From the clear until the note arrives, Lyra message
pointers wait; tasks, handoffs, reuse and prompts are refused with `session-resetting`. A person can still type
in the session's tab. If the clear is unconfirmed (`session-reset-clear-unconfirmed`), it is not typed again:
do not reset again. Read the session with `lyra session read <session-id> --source terminal` or ask the person
to look at its tab. A daemon refusal (`session-reset-clear-refused`) typed nothing because the execution
changed; inspect `lyra session show <session-id> --json` before requesting another reset.

Resetting yourself answers `pending`: end your turn. Run the same command with the same `--request-id` to read
the result; your session ID stays the same, so you can still read it. You may reset yourself or, as a Lead or
Orchestrator, a session in your tree; a Worker resets only itself. A pending handoff or an unsettled dispatch
refuses the reset: settle it first.
