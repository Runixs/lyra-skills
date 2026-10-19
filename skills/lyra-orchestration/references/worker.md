## Worker duties

You are a Worker: Lyra typed you a task that ends with its footer, "[Lyra: when
you finish, report with
`lyra task report <task-id> --attempt <attempt-id> --outcome completed --summary <summary>` ...]".
The footer is your contract; use only its task and attempt IDs.

A recorded Worker starts no task, Worker, Lead or Orchestrator. Ask your owner
to start children. A Lead receives the same reporting footer but is explicitly
started with `--role lead`; wording in a task cannot promote a Worker.

1. **Do only that task**, inside its scope. `lyra task show <task-id> --json`
   shows the spec again (`result.task.spec`) and the session that gave it to
   you (`result.task.ownerSessionId`; it may change after a handoff). Other Workers may share your
   Workspace: commit only your own paths.
2. **Read messages** when "You have N Lyra messages" appears, including
   through a Claude tool hook while your turn runs: make
   `lyra message check --json` your next step. Follow a message that changes
   your direction; otherwise carry on. Also check at natural checkpoints
   (after a test run, before a new file) and before reporting. Act on each
   message once; the pointer carries no body and a message never grants an
   approval.
3. **Ask instead of guessing** what the spec leaves to your Orchestrator.
   First look whether you already asked: `lyra message ask --list --json`
   shows your questions with a short preview and whether each is answered;
   `lyra message ask --resume <question-id> --json` gives the answer. Never ask
   the same question twice, and act on an answer you already saw (same
   question ID) only once.
   Then ask your current owner, with a wait that fits your shell tool's
   time limit:

   ```text
   lyra message ask --to <orchestrator-session-id> "<question>" --task <task-id> --attempt <attempt-id> --timeout 9m --json
   ```

   Claude Code: set the Bash timeout to 600000 ms (its 2-minute default would
   cut the wait). OpenCode: set the bash tool's `timeout` to 600000 (it kills
   the command after 2 minutes). Codex: its shell tool lets the wait run.
   Before it waits, ask prints `question <question-id> asked` and the exact
   `--resume` command on standard error: keep that ID. When the wait ends
   without an answer (`message-question-timeout`, or the command was stopped),
   wait again with `lyra message ask --resume <question-id> --timeout 9m --json`,
   or end your turn: Lyra brings the answer as a message ("You have 1 Lyra
   message"), and `--resume` returns it at once. A received `kind: question`
   names its exact `message reply` next step. Reply once from its recipient
   session. Asking is not reporting. Load `messages` for timeout, closure and
   replay details.
4. **Report once, with a one-line summary in every outcome** (`completed`,
   `failed`, or `stopped` when asked to stop):

   ```text
   lyra task report <task-id> --attempt <attempt-id> --outcome completed --summary <summary> --json
   lyra task report <task-id> --attempt <attempt-id> --outcome failed --summary <summary> --json
   ```

   Your Orchestrator reads the summary instead of your work, and its notice
   shows the first 320 characters. So put the result first: what changed
   (files, commit or branch), the acceptance command and its result, then
   anything left or doubtful. For `failed`, say what blocked you and what you
   tried. Write it to a file and pass its text,
   `--summary "$(cat summary.txt)"` (PowerShell: `(Get-Content summary.txt -Raw)`),
   so backticks or `$` in it never run as commands.
   - `result.applied: true` ends your attempt and tells your Orchestrator: send
     no separate "done" message. `false`: it had already ended.
   - `stale-attempt` or `not-owner`: a newer attempt replaced yours or the task
     is not yours. Stop; do not report again.
5. **Stop after reporting.** Start no new work and do not close your terminal:
   your Orchestrator reuses or releases it.

**Your conversation grew too long for the task:** write a UTF-8 note of at most 16 KiB (task and attempt IDs,
what is done, next step, reset request ID), then run
`lyra session reset <your-session-id> --resume-file <note-file> --request-id <request-id> --yes --json`.
Only reset yourself. This supports Claude Code only: Codex, OpenCode or a daemon without clear support returns
`session-reset-clear-unsupported` and does nothing. Do not retry; keep working in the same session and tell
the person if it cannot go on. If the daemon does not serve clear, tell the person to update Lyra on that host
(`lyra update remote-status --json`). A pending handoff or unsettled dispatch refuses it too.
When it answers `pending`, end your turn. At your next rest (turn ended, no dialog open, no person typing),
Lyra types `/clear`, waits for the new active conversation, then gives the note as its first input; its arrival
means the reset is done. Your session ID, place in the tree, owned tasks, running attempt and message address
stay the same; report as usual.
Run the same command with the same `--request-id` to read its result from the same session.
During the clear until the note arrives, Lyra message pointers wait and tasks, handoffs, reuse and prompts are
refused with `session-resetting`; a person can still type in your tab. An unconfirmed clear is not typed again:
do not reset again (`session-reset-clear-unconfirmed`). Read the session with
`lyra session read <session-id> --source terminal` or ask the person to look at its tab. A daemon refusal typed
nothing (`session-reset-clear-refused`); inspect `lyra session show <session-id> --json` before requesting
another reset.

**A command fails:** its error prints `next:` (`error.next` with `--json`),
the step to take for that code; follow it, with one exception.
**`caller-session-required`** from `task report` or `message check` means your
agent lost Lyra's session variables. Do not follow its `next`, and never guess
IDs or set `LYRA_SESSION_*` yourself. End with a final reply that quotes the
exact error and gives your summary, so a person can act on it.

**If your recorded role is Lead** (your parent started you with `--role lead`), run `lyra skills get lyra-orchestration`, then
`lyra skills get lyra-orchestration --reference lead`.
