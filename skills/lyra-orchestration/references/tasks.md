## Tasks by hand: DAG, gates, handoff

`worker start --spec-file` makes one task and one Worker per call.
`worker start --task <task-id>` starts a fresh Worker for an existing ready task. Build tasks by hand when
Lyra should hold the order of a staged plan (the status board then draws it),
when one session takes several tasks in turn, or to give a task to a session
that already exists.

### A Task DAG

```text
lyra task create --spec-file api.md --kind <kind> --json
lyra task create --spec-file ui.md --kind <kind> --json
lyra task create --spec-file docs.md --depends-on <api-task-id>,<ui-task-id> --kind <kind> --json
lyra task list --ready --json
lyra worker start --task <task-id> --workspace current --agent claude --json
lyra task dispatch <task-id> --worker-session <owned-worker-session-id> --request-id <new-request-id> --json
```

- Create independent tasks first; `--depends-on` only for real order. Prefer a
  wide plan over a long chain. Dependencies stay inside your own plan.
- `task list --ready` lists what can start now. A completed task starts
  nothing by itself: dispatch its dependents.
- Keep finished Workers open for reuse (`terminals`).
- A failed or stopped task blocks its dependents (`blockCauses`
  `predecessor-ended`) until you retry it; removing it blocks them for good.
- `worker start --task` requires the task's current owner as its Lyra caller
  session, like `worker start` and `task dispatch`. In a plain shell, use
  `task show` to find the owner and run the start from that session.
- Without placement flags, `--task` uses the owner's current Workspace. For a
  retry whose partial changes live elsewhere, pass that preserved Workspace
  explicitly with `--workspace <workspace-id>`.
- For each ready task, use `worker start --task` to open a fresh Worker under
  its owner, with the usual role and depth checks. It reads the stored spec;
  do not pass `--spec-file`, `--depends-on`, `--kind`, `--on-disconnect` or
  `--handoff`. Running, settled, dependency-blocked and other-owned tasks are
  refused before creating resources. Retry failed or stopped tasks first
  with `lyra task retry <task-id> --json`.
- Dispatch only into a Worker you control. An existing session takes a
  dispatch or retry dispatch unless a detach or move took it out of your tree
  and you hold neither prompt rights nor current task custody of its terminal;
  one a person opened takes it as before. A plain `session open` creates a
  separate Orchestrator tree. `terminal reuse` (`terminals`) needs prompt
  rights or current task custody. Adoption grants custody, not prompt rights or
  a tree change. Detach/move fence old outside custody, finished tasks
  included; owners moving inside the branch or staying in its tree keep it. A
  fenced old terminal is not reusable even with starter prompt rights; detach
  and a move into another tree end those rights. `dispatch-outside-tree` names
  two repairs: `worker start --task <id>`, or `terminal reuse` with your own
  idle Worker. Calls without V-55 context gain no restriction.
- `accepted` means the Worker has it (`result.attemptId`); `result.reason`
  `task-turn-started` means its turn began. `returned` or `rejected`: nothing
  started, `error.code` says why. Exit 3: `recovery`.
- A session works on one task at a time. Give it the next one after it reports,
  through reuse (`terminals`).
- `--on-disconnect while-connected` at create stops the task when its Host's
  link drops; the default keeps it running.

### Deadlines and failed-attempt caps

```text
lyra task create --spec-file api.md --deadline 2026-10-16T18:00:00+09:00 --max-attempts 3 --json
lyra task set <task-id> --deadline 2026-10-17T18:00:00+09:00 --max-attempts 2 --json
```

- An omitted cap takes Settings → Orchestration's default (initially 3) once,
  at creation; `--max-attempts none` disables it. `--deadline` takes RFC3339
  with an offset or Unix milliseconds; `none` clears it.
- Failed, cancelled, force-stopped and abandoned-unknown attempts count, failed
  pre-acceptance dispatches too; success and handoff do not (`failedAttempts`,
  `maxAttempts` in show/list). At the cap, dispatch, retry and
  `worker start --task` refuse `task-attempts-exhausted`: tell the person;
  never create another task to bypass it.
- Owners move or clear deadlines and lower caps with `task set`; only a person
  raises or removes a finite cap. Never unset your caller context to act as
  the person.
- `task-overdue` wakes the wait once per task and deadline: read the task and
  decide with the person. Neither limit authorizes an automatic stop, retry,
  escalation or mail.
- A Lead's child tasks inherit no deadline: keep each child's no later than
  yours.

### Decision gates

A gate holds a ready task and everything after it until the person decides.
Only you, the plan's Orchestrator, create and resolve it. It is not in the
Inbox and the screens cannot answer it: the person tells you.

```text
printf '%s\n' '["Keep the REST API", "Move to gRPC"]' > options.json
lyra gate create --task <task-id> --question-file question.md --options-file options.json --json
lyra gate list --task <task-id> --json
printf '%s\n' 'Keep the REST API' | lyra gate resolve <gate-id> --choice-stdin --json
```

The options are a JSON array of at least two different strings; the choice
must equal one exactly. Resolve only with the person's decision; time passing
is not a choice. After exit 3, read `request show` (`recovery`) and
`gate list`; the same request ID and arguments return the original receipt.
Never use a gate to answer a running Worker's question: answer by message.

### Settle a task yourself

When the Worker's session has closed and you can judge the result, the task's
owner (Orchestrator or Lead), or a person in a plain shell, may record it:

```sh
lyra task settle <task-id> --outcome <completed|failed> --reason <one-line-reason> --request-id <request-id> --json
```

Give the result and its evidence in the reason. A Worker uses `task report`
for its own work. An open Worker refuses settlement: finish or explicitly
stop/close it first; never settle automatically on silence. Unknown closure
also refuses. Completed releases dependencies as a normal completed report
does; failed keeps the existing dependent failure rule.

### Handoff

A handoff makes its receiver the task's owner. An existing receiver keeps its
place and becomes the parent of the running Worker and its branch. Reports
go only to that receiver; the giver gets no copy. When the running Worker
receives its own task, or `worker start --handoff` creates a receiver, it takes
the giver's place and role instead. Handoff transfers one task; move changes a
session's parent, adoption takes an ended owner's work, and messages move nothing.

```text
lyra task handoff <task-id> --worker-session <session-id> --request-id <new-request-id> --json
lyra task show <task-id> --json
```

- The task travels as a message, and ownership moves only when the receiver's
  `message check` or `task wait` takes it within 60 seconds. Otherwise it ends
  `not_delivered` and stays yours. A receiver idle at its prompt, or a fresh
  agent once its prompt box reads ready, gets the "You have N Lyra messages"
  line.
- `result.handoff.status`: `requested` or `delivering` (still yours),
  `delivered`, `not_delivered`, `rejected`. A ready task can go to any
  session, a running supervised task only to an existing one. Before sending and
  again at receipt, Lyra refuses a loop (`handoff-loop`), a Worker receiving a
  child (`handoff-worker-receives-child`), or a moving branch past the depth
  limit (`handoff-depth-limit`). A failed receipt check returns the handoff.
- The receiver sees ownership in its receipt (`transfers`). When another Worker
  keeps running the task, that Worker still reports its original attempt and
  binding; the receiver supervises it and gets its result. When the receiver
  is the execution, it reports with the attempt in the task's footer.
- Abandon only a handoff whose receiver is confirmed closed, on the person's
  word:
  `lyra task handoff <task-id> --abandon --attempt <attempt-id> --request-id <new-request-id> --yes --json`.
