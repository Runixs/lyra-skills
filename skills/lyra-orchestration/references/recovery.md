## Recovery

Act only on proof: a recorded result, an error code, a closed session, an
escalation. Silence, a timeout or an idle-looking Worker proves nothing. When a
person must act, tell them what, where, and the command you will run after.

### Starting

Here `next` is `error.detail.next`, the command a stopped `worker start`
printed; it comes before `error.next`.

| Signal | Do |
|---|---|
| `worker start` stopped (exit 1, 2 or 3) | Read `error.detail`: `failedStep`, `created` (kept, never rolled back) and `next`. Never run `worker start` again for it |
| `task-agent-dialog-<name>` or `task-agent-not-ready` | The Worker's agent shows a dialog (update, trust, directory, model, hooks, prompt) or never became ready; nothing was typed. Ask the person to answer it in that terminal, then run `next` with a new `--request-id` |
| `task-input-held-by-human` | The person typed into that Worker's view. Ask them to close the view, then run `next` with a new `--request-id` |
| `task-execution-refused` or another dispatch refusal | Nothing started and the task is still ready. Run `next` once with a new `--request-id`; the same code again → stop and report it. A spec over 16 KiB is refused this way: shorten it and point to files |
| `worker-depth-limit` | This Worker cannot start deeper Workers. Split the work with a Workflow, or ask the task owner with `lyra message send --to <owner-session-id> --task <task-id> --file <file>` |
| `task-not-startable` | Its dependencies have not completed; run `next` when they have |
| `session-not-active` | The session did not become active in 60 seconds; `next` is the `session show` to read it |
| `session-effort-unsupported`, `session-model-not-in-catalog`, `agent-selection-refused` | Nothing was created. Pick from `error.detail.allowed` or `candidates`, or ask |
| `turn` `not-started`, then no news (below) | The text may sit unsent in its input box, or its agent sends no turn signals. Look for its changes first; none → ask the person to check that terminal (Enter sends waiting text). Never dispatch it again or to a second Worker |

### Exit 3 (outcome unknown)

1. First read `lyra request show <request-id> --operation <operation> --json`
   (`message ask` and `message reply`: go to step 2): the stored receipt or not
   found; it applies nothing (an agent reads its own scope; a person may add
   `--session <session-id>`). Then `error.detail.check` or
   `lyra task show <task-id> --brief --json`.
2. Commands that keep a receipt (`task` create, dispatch, handoff, set,
   settle, report, retry, remove, cancel, adopt; `gate` create, resolve;
   `message` ack, send, ask, reply; `terminal` reuse, release): repeat the
   exact arguments with
   `--request-id <error.detail.requestId>` to get the first result back
   (some mark it `replayed: true`).
3. Not found may still be in flight: keep the key and arguments, never invent
   a new key. Changed arguments return `request-conflict`: read the task or
   gate first.
4. A dispatch still `unknown` stays unknown: attempt `returned` → a new
   dispatch may use a new key; `dispatching` → stop and tell the person, never
   a second Worker.
5. `bridge.unknown-operation`: home is older; ask the person to update it.
6. `task wait` or `message check` exit 3 (`home.connection-lost`,
   `message-claim-unconfirmed`) loses nothing: run it again. A tool timeout is
   unknown too: read `lyra daemon status --json`, then step 1.

### Worker conditions

**No news** means a `running` task shows the same `state` and `progress` (or
null) at two checkpoints in a row. The first time, look once: its `turn` in
`lyra status show --session <worker-session-id> --json`, what it last did in
`lyra session read <worker-session-id>`, and its changes in
`lyra git status <workspace-id> --json`. No news again at the next checkpoint:
tell the person what you saw. Never cancel, retry or re-dispatch on silence.

| Proven state | Do |
|---|---|
| `worker-stopped` right after its question | Answer the question if you have not; send nothing else |
| `worker-stopped`, nothing asked | One message: report your result or name your blocker. Stops again → tell the person what it last said; only the Worker can report its attempt |
| `turn` `awaiting-human` in `status show` | It waits for a person's approval or answer in its terminal; Lyra never escalates that. Tell the person |
| `worker-wait-too-long` | Tell the person what is waiting (`progress.waitingTooLong`); it authorizes no escalation, stop, retry or dispatch |
| `worker-suspect` | Look once as above. A long build or test → wait; then the no-news rule |
| `worker-unobservable` | Lyra cannot see it (OpenCode 1.x, a lost link): only the no-news rule and its report tell you anything |
| A message from `lyra-supervisor` with `"kind":"escalation"` | Read `confirmedCause` and `neededDecision`; Lyra retries Claude rate limits first. `process-exited`, `budget-exhausted`, billing or login → tell the person. On their word: `task cancel` (an exited Worker then reads `stopped`), `task retry`, then `lyra worker start --task <task-id> --workspace <workspace-id> --agent <name> --json` in the same Workspace (partial changes stay), or `terminal reuse` with one of your own idle Workers (`tasks`). The stored spec stays: add context by message, or create a new task when its scope changes. Quota → another agent |
| `worker-closed` | Closed with no result. Tell the person; on their word the same cancel, retry and new Worker |
| `message-held` | Your mail cannot be delivered. `message-recipient-closed` → hand work to a live session; unknown → inspect and ask the person before any resend; unsupported/version → update the recipient host or pick a compatible live session; terminal, fence or store → tell the person what needs repair (`messages`) |
| `message-conditions-omitted` | Over 256 outgoing items: tell the person total/omitted, route known stranded work to live sessions and re-arm |

### Stopping work

Keep finished Workers open for reuse (`terminals`).

`lyra task cancel <task-id> --yes --json` types one Ctrl-C into the Worker: a
request, not a stop. The task reads `stopped` only when the Worker reports it
(ask it by message to report `stopped`) or Lyra proves its process ended; keep
waiting for a checkpoint to list it. A task left `stop-requested`
cannot be retried until termination is proven. Tell the person; do not start a duplicate task.

`lyra session force-stop <session-id> --yes --json` ends an agent for good;
who may use it, its receipts and when to retry: **Force-stop** in `terminals`.

For `task cancel` and `task retry`, `--abandon-unproven` is person-only.
An agent gets `task-abandon-person-only`: ask your person to decide in their
own terminal, since the original dispatch may still run.

`lyra task remove <task-id> --yes --json` (a ready, failed or stopped task)
takes it out of the plan and blocks its dependents for good.

### Your own session ended

When the daemon (it runs agent sessions) stops, every
session it ran ends, yours too, and your commands fail with
`caller-session-stale`. On the person's word, a new session takes over. A new
session's `task list` is empty until adoption. Find the ended session with
`lyra session list --json` (`failed`/`closed`, by title), or ask the person:

```text
lyra session show <ended-session-id> --json
lyra task adopt --from <ended-session-id> --yes --json
lyra task list --json
```

- Require `failed` or `closed`; `adopt-owner-open` means still running.
- You get its plan, owned tasks and unread/claimed mail; later sends to its
  address forward to you. Act on replayed mail, then `message ack` its batch.
  Live Workers report to you; adopt `result.inFlight` after handoff.
- A `running` task whose Worker died with the daemon: cancel it, retry it once
  it reads `stopped`, and run
  `worker start --task <task-id> --workspace <workspace-id>` with the
  previous attempt's `workspaceId` from `task show`, the Workspace that holds
  the partial changes.
- Messages sent to the old session stay there; read results with
  `task show --brief`.
- Adopt a Lead's plan the same way, one ended session at a time.
