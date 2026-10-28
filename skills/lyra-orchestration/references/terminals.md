## Finished Workers: reuse or release

A still-open Worker whose task has a result keeps its terminal, process and context. Reuse
it for a follow-up on the same code (review fixes, the next step): it needs no
new start and remembers what it did. Otherwise leave it open and reusable in
the explorer, even when nothing follows. Never release a Worker on your own.
Release only when the person asks, or when reuse is impossible and the person
agrees after you explain why.

```text
lyra terminal list --terminal-state reclaimable --json
lyra task create --spec-file followup.md --json
lyra terminal reuse --worker-session <worker-session-id> --task <new-task-id> --reuse-mode continue --request-id <new-request-id> --json
```

Tell the person how many finished Workers are kept in the filtered list's
scope, including zero, and that `lyra terminal release` frees them when they
want. If the list fails, report the count as unknown. Only after the person's
request or agreement above:

```text
lyra terminal release --worker-session <worker-session-id> --request-id <new-request-id> --yes --json
lyra terminal release --task <task-id> --request-id <new-request-id> --yes --json
```

- The filtered list shows each settled attempt whose Worker terminal remains
  retained: `sessionId`, `taskId`, `attemptId`, `outcome`, `settledAt`,
  `ownerSessionId` and `next`. `next` is an exact release command only when you
  own the task or its plan; otherwise it is `null`: `ownerSessionId` names who
  can release it. A returned command is not the person's permission to run it.
  It includes older failed attempts after a retry; running
  and released terminals, and releases already `checking` or `closing`, are
  excluded. An agent sees its own tree; a person sees all. The list changes nothing. `--workspace` narrows it further.
  An older home refuses the new read operation as `bridge.unknown-operation`;
  it never silently shows an unfiltered shell list.
- Name the Worker by its session ID (`sessionId` from `worker start`,
  `workerSessionId` from `task show --brief`). The CLI finds its retained
  terminal and current fences itself. `terminal-stale`: the Worker changed in
  between; read `lyra terminal show --worker-session <worker-session-id> --json`,
  and if the step still applies, run it again with a new request ID.
- `terminal release --task` releases that task's one retained terminal. With
  several, `terminal-selector-ambiguous` lists `choices` (`workerSessionId`):
  release by session. None: `terminal-not-found`.
- Agent reuse needs prompt rights over the session or current task custody of
  its terminal. Adoption grants custody without prompt rights or tree changes.
  Detach/move fence old outside custody even for finished tasks. The old terminal
  cannot be reused through remaining starter prompt rights; detach and a move
  into another tree end old starter rights; a new dispatch is refused only
  when a detach or move took the session out of your tree (`tasks`). Owners moving with their branch
  or remaining in its tree retain custody. A handoff giver cannot
  reuse the handed-off terminal when it retains neither right. On
  `dispatch-outside-tree`, use `worker start --task <id>`, or
  `terminal reuse` with an owned idle Worker.
- Reuse works across Workspaces: the task runs in the Worker's own Workspace.
  It needs a recorded result, the same Host and process, and a Worker other
  than you; a busy Worker is refused. `continue` is the only mode this build
  runs (`clear` is refused with `reuse-clear-unsupported`).
- A reused Worker's context keeps growing. For unrelated work, start a fresh
  Worker instead.
- `terminal-not-settled`: no result yet; wait. A release first checks that the
  conversation and result are kept: `checking` or `closing` is not finished,
  `release-unknown` → tell the person. After a release, `terminal show` answering
  `terminal.session-pty-absent` is expected. Never close the session instead of
  a failed release.

## Force-stop

A person may irreversibly end any session with
`lyra session force-stop <session-id> --yes --json`. An Orchestrator or Lead
may do this only to sessions below it in its tree; a Worker may stop none,
and an agent cannot stop itself. `session-force-stop-above` (the session
directs you), `session-force-stop-not-below` (another branch of your tree) and
`session-force-stop-outside-tree` each name who may stop it instead. `--yes` uses the ordinary irreversible-command
confirmation; omit it only on an interactive terminal to answer `y/N`.

On `stopped`, the agent process is proven gone. Its active attempt is `failed`
with reason `force-stopped`, and its task stays with its owner. Read
`lyra task show <task-id> --brief --json`, then explicitly retry or reassign;
there is no automatic retry. A fixed `lyra-supervisor` notice with
`kind: force-stopped`, `state: failed` and `reason: force-stopped` reaches the owner
through `task wait`; treat it as the outcome, not a Worker report or an escalation.
Unread mail to the stopped session yields the
existing `message-held` event for its sender.

On exit 3 / `session-force-stop-unconfirmed`, process death is unproven.
Inspect the original session and task; do not retry or reassign that task.
The same `--request-id` replays its first receipt without another stop. After
restoring the host connection, explicitly force-stop with a new request key
if another process check is needed. Overlapping force-stops of one session
share one outcome. Lyra fails the task as `force-stopped` by itself once the
process is proven gone, also after a restart; until then only a person can end
it sooner with `lyra task cancel <task-id> --abandon-unproven`
(`force-stop-abandoned-by-person`), accepting that the old process may still run. `session-force-stop-unavailable` means
update Lyra on the execution host; `bridge.unknown-operation` means update home.
There is no fallback to cooperative cancel or ordinary close.

A force-stopped Lead's children keep running and their tasks keep that Lead's
recorded ownership. Explicitly adopt its plan and tasks using recovery.md, "Your own session ended";
force-stop does not cascade, move children or invent a new owner.

## Checkouts on another host

A Workspace (Git worktree) is made from a checkout on the same host. If the
project has none there, use its remote URL without asking the person:
`lyra project clone <remote-url> <parent-path> --host <host> --project <project-id>`.
For an existing checkout, use `lyra project location add <project-id> <native-path> --host <host> --expected-revision <revision>` (get the revision from
`lyra project show <project-id> --json`). Then run `lyra worker start --project <project-id> --name <workspace-name> --spec-file <spec-file> --host <host> --agent <name>`.

In Windows Git Bash, set `MSYS_NO_PATHCONV=1` before passing a POSIX path for a
remote host. Apply it to that command only:

```sh
MSYS_NO_PATHCONV=1 \
lyra project clone <remote-url> <parent-path> --host <host> --project <project-id>
```

Otherwise Git Bash rewrites
`/home/...` to `C:/Program Files/Git/home/...`.
