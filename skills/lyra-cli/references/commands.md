## Command reference

Every command of this Lyra build, in the order of `lyra --help`. Agents: add
`--help` to the one command you need instead of reading this list (for example
`lyra git diff --help`); it also lists each flag's allowed values. Brackets mark
optional input; angle brackets are values to replace.

**open**

- `lyra open <file-or-url> [--request-id <request-id>] [--json]`: queue a file or HTTP(S) URL in Projects, instead of open or xdg-open; Lyra-launched agent sessions only

**doctor**

- `lyra doctor [--json]`: run read-only health checks with a five-second deadline per check; fix nothing automatically

**version**

- `lyra version [--json]`: print the product and bundled skills versions (also --version)

**host**

- `lyra host list [--json]`: list every machine in the execution map
- `lyra host show <host> [--json]`: show one machine and its execution locations

**credential**

- `lyra credential ssh-cleanup-status [--json]`: show resumable legacy SSH password cleanup
- `lyra credential ssh-cleanup-classify <credential> --method <method> --revision <revision> [--json]`: classify unknown SSH metadata without reading its secret
- `lyra credential ssh-cleanup-retry --revision <revision> [--json]`: retry the displayed unfinished SSH password cleanup
- `lyra credential add-ssh --name <name> --method <method> [--host <host>] [--key-file <path>] [--json]`: store an SSH credential; the key comes from --key-file, a passphrase or password from standard input
- `lyra credential add-model-endpoint --name <name> [--host <host>] [--json]`: store the key for a gateway or on-premises model endpoint; the key comes from standard input
- `lyra credential list [--json]`: list stored credentials (no secret values)
- `lyra credential show <credential> [--json]`: show one credential (no secret value)
- `lyra credential remove <credential> [--yes] [--json]`: delete a credential and its secret from the OS credential store

**server**

- `lyra server list [--json]`: list registered servers with the last observed connection state
- `lyra server show <server> [--json]`: show one server with the last observed connection state and when
- `lyra server add --name <name> [--address <address>] [--port <port>] --user <user> [--host-key-policy <policy>] [--credential <credential>] [--password] [--json]`: register a remote server and attach it to the execution map
- `lyra server update <server> [--expected-revision <revision>] [--name <name>] [--address <address>] [--port <port>] [--user <user>] [--host-key-policy <policy>] [--credential <credential>] [--password] [--password-stdin] [--json]`: change a server's name, address, user, host key policy or credential
- `lyra server remove <server> [--yes] [--json]`: remove a server from the registry
- `lyra server attach <server> [--json]`: attach a registered server to the execution map again (after server-not-attached)
- `lyra server ssh-hosts [--json]`: list the Host aliases in your ~/.ssh/config (Include expanded, wildcards left out)
- `lyra server import <alias> [--name <name>] [--host-key-policy <policy>] [--password] [--json]`: register an SSH config alias; optionally select a memory password with --password
- `lyra server connect <server> [--password-stdin] [--retry-password] [--json]`: connect and hold the connection, one line per state change; Ctrl-C closes it
- `lyra server key <action> <target> [--json]`: your SSH key on a server: `status <server>`, `register <server> [--yes]` (on the current connection), `switch on|off` (register automatically after a password connect)

**runtime**

- `lyra runtime list [--host <host>] [--json]`: list detected agent runtimes per host
- `lyra runtime detect --host <host> [--json]`: detect agent runtimes on a host (a remote host is reached over its server)

**profile**

- `lyra profile list [--host <host>] [--json]`: list profiles on every host
- `lyra profile show <profile> [--json]`: show one profile
- `lyra profile add --from <profile> --name <name> [--provider <provider>] [--address <https-url>] [--location <location>] [--credential <credential>] [--json]`: derive a profile from a canonical one
- `lyra profile update <profile> [--name <name>] [--enabled <true|false>] [--provider <provider>] [--address <https-url>] [--runtime-default] [--location <location>] [--credential <credential>] [--no-credential] [--json]`: change a profile (a canonical profile changes only its name and enabled flag)
- `lyra profile remove <profile> [--json]`: remove a derived profile

**update**

- `lyra update status [--json]`: refused by this build; it shows no engine status
- `lyra update check [--json]`: explain that the Lyra app owns update checks and downloads
- `lyra update apply [--yes] [--json]`: refused by this build; a person applies an update with Update now in the Lyra app
- `lyra update rollback [--server <id>] --engine <app|ssh> [--yes] [--json]`: restore the selected engine's recorded previous snapshot; this build runs it only with --engine app on localhost and refuses other engines and servers
- `lyra update remote-status [--server <id>] [--json]`: refused by this build; no command here lists engine roles or a transition ID
- `lyra update recover [--server <id>] --engine <app|ssh|resource> --transition <id> --resolution <finish|restore-recorded> [--yes] [--json]`: finish or restore the original interrupted engine transition; this build runs it only with --engine app on localhost and refuses other engines and servers

**process**

- `lyra process list [--json]`: list the processes Lyra started on this machine
- `lyra process stop <process> [--yes] [--json]`: stop a process Lyra started, after checking its OS identity

**trace**

- `lyra trace list [--project <project>] [--cursor <cursor>] [--limit <count>] [--json]`: list executions, newest first, with where they stopped and on which hosts
- `lyra trace show <subject> --kind <kind> [--project <project>] [--cursor <cursor>] [--limit <count>] [--json]`: show every recorded step of one execution with its host

**home**

- `lyra home start [--json]`: start the home runtime if it is not running and wait until it answers
- `lyra home stop [--force] [--json]`: stop the home runtime; refused while work runs unless --force; on an engine install it refuses with app.unit-unavailable: use `daemon stop`
- `lyra home status [--json]`: show whether the home runtime runs, without starting it

**daemon**

- `lyra daemon start [--json]`: start this computer's lyra-daemon and wait until it answers
- `lyra daemon stop [--json]`: stop this computer's idle lyra-daemon engine and keeper

**project**

- `lyra project location add <project-id> <native-path> --host <host> [--location <execution-location>] --expected-revision <revision> [--json]`: attach a matching repository checkout on the selected host, including another root on the same host
- `lyra project add <native-path> --host <host> [--json]`: register a folder on a host as a project and open its primary workspace (the path is spelled as that host spells it)
- `lyra project list [--host <host>] [--cursor <cursor>] [--limit <count>] [--json]`: list projects; a host that could not be read is shown as unreadable, never as zero projects
- `lyra project show <project-id> [--refresh-branch-cleanups] [--json]`: show one project with its host, kind, path and revision, and its kept branches; --refresh-branch-cleanups first checks unsettled branch deletions on their hosts (it never deletes)
- `lyra project update <project-id> --expected-revision <revision> [--name <name>] [--host <host>] [--location <execution-location>] [--root <source-root>] [--worktree-base <host-path>] [--worktree-base-default] [--json]`: rename a project or set one checkout's worktree base (checked on its host; only future workspaces use it); --worktree-base-default returns to ~/lyra/workspaces
- `lyra project remove <project-id> [--yes] [--json]`: take a project off the list: its folders, worktrees and branches stay on every host; refused while Lyra worktrees or live sessions remain
- `lyra project prepare-status <project-id> [--host <host>] [--location <execution-location>] [--root <source-root>] [--json]`: read one checkout's prepare commands (.lyra/config.yaml, or the commands typed at add when the file is absent) and whether you approved them; a host that cannot be read is an error
- `lyra project prepare-trust <project-id> --fingerprint <fingerprint> --expected-trust-revision <revision> [--host <host>] [--location <execution-location>] [--root <source-root>] [--always] [--json]`: approve exactly the prepare commands prepare-status showed (by fingerprint); --always also approves future valid changes on every checkout of this project; there is no revoke — removing and re-adding the project clears it
- `lyra project clone <url> <parent-path> --host <host> [--location <execution-location>] [--name <folder>] [--project <project-id>] [--expected-revision <revision>] [--json]`: clone a repository into a folder on a host and add it as a project (or, with --project, as another checkout of that project); the host's own keys and credential helper are used and nothing prompts
- `lyra project create <parent-path> <name> --host <host> [--location <execution-location>] [--no-git] [--json]`: make a new folder on a host (with git init unless --no-git) and add it as a project
- `lyra project find-repositories <path> --host <host> [--location <execution-location>] [--depth <levels>] [--json]`: list the Git repositories under a folder on a host (1-5 levels, default 3), with the project that already has each
- `lyra project branches <project-id> [--host <host>] [--location <execution-location>] [--root <source-root>] [--json]`: list the local and remote branches of one project checkout, read on its host now
- `lyra project scan --host <host> [--path <native-dir>] [--limit <count>] [--json]`: list the folders under a directory on a host and whether each is a Git repository

A Workspace (Git worktree) needs a checkout on the same host. If the project
has none there, first run `lyra project clone <remote-url> <parent-path> --host <host>
--project <project-id>`; for an existing checkout use `lyra project location add`
above. Then run `lyra worker start … --host <host>`. With a remote URL, do not ask
the person. In Windows Git Bash, set `MSYS_NO_PATHCONV=1` (for example
`export MSYS_NO_PATHCONV=1`) before passing remote POSIX paths: otherwise
`/home/...` becomes `C:/Program Files/Git/home/...`.

**workspace**

- `lyra workspace create <project-id> <name> [--agent <name>] [--host <host>] [--location <execution-location>] [--root <source-root>] [--base <branch>] [--branch <new-branch>] [--reuse-branch] [--setup <run|skip>] [--trust] [--json]`: create and prepare a workspace, then open its first session (the two results are reported separately); --base starts from a branch, --branch names the new branch, --reuse-branch checks out the existing local --base branch; prepare commands come from the project folder's .lyra/config.yaml (or the commands typed when it was added) and run only with your consent: --trust approves exactly the commands read now, --setup skip runs none
- `lyra workspace register <project-id> <native-path> --host <host> [--location <execution-location>] [--root <source-root>] [--json]`: register one existing Git worktree you chose; its setup is not run
- `lyra workspace list <project-id> [--cursor <cursor>] [--limit <count>] [--json]`: list the workspaces of a project
- `lyra workspace show <workspace-id> [--json]`: show one workspace with its kind, host, path and revision
- `lyra workspace rename <workspace-id> <display-name> [--expected-revision <revision>] [--json]`: change only the display name; the id, path and branch stay
- `lyra workspace remove <workspace-id> [--expected-revision <revision>] [--force] [--yes] [--json]`: remove or unregister a workspace; running sessions and terminals in the workspace are stopped first, and an unproven stop is refused and keeps the folder; a dirty one is refused before anything stops unless --force discards its uncommitted changes and new files (--force waives nothing else); a root or unknown one, or one a Lyra screen conversation uses, is always refused
- `lyra workspace remove-branch <cleanup-ref> --expected-head <commit> [--yes] [--json]`: force-delete a created branch that was kept when its workspace was removed; unmerged commits may be lost; refused if the branch moved or is checked out

**file**

- `lyra file list <workspace-id> [--dir <relative-dir>] [--limit <count>] [--json]`: list a directory of a workspace; a cut-off listing says so
- `lyra file read <workspace-id> <relative-path> [--max-bytes <bytes>] [--json]`: print a text file of a workspace as it is; unsupported and too-large files are named, not printed
- `lyra file write <workspace-id> <relative-path> [--create] [--expected-revision <revision>] [--file <file>] [--stdin] [--json]`: create (--create) or save (--expected-revision from `file read --json`) one Markdown file of a workspace; other files are refused and an existing file is never overwritten by --create

**git**

- `lyra git status <workspace-id> [--limit <count>] [--line-stats] [--json]`: show the Git state of a workspace (read only); not a repository and Git unavailable are told apart
- `lyra git diff <workspace-id> <relative-path> --area <area> [--expected-git-revision <revision>] [--max-bytes <bytes>] [--json]`: show one file's staged or unstaged diff (read only); a comparison that changed is not shown as current

**session**

- `lyra session configuration <profile-id> [--json]`: read the saved launch template and profile model default
- `lyra session configure <profile-id> [--stdin] [--json]`: save the launch template JSON from stdin with expectedRevision
- `lyra session models <workspace-id> [--agent <name>] [--json]`: read the actual model catalog with the saved native invocation
- `lyra session defaults <harness-kind> [--json]`: read the separate home global model default
- `lyra session set-default <harness-kind> [--model <model>] --expected-revision <revision> [--json]`: save or clear the separate home global model default using CAS
- `lyra session open <workspace-id> [--agent <name>] [--model <model>] [--effort <level>] [--title <title>] [--json]`: open a session with --agent (a canonical kind or Profile name); it reports opening, active, failed or unknown; --title sets the title you chose, which a later model summary does not overwrite; an agent starts an Orchestrator tree under its role checks (Worker refused), while a person is unrestricted
- `lyra session list [--workspace <workspace-id>] [--cursor <cursor>] [--json]`: list sessions with host and state; a list that could not be read is a failure, never an empty list
- `lyra session show <session-id> [--json]`: show one session with its host, state and title
- `lyra session interrupt <session-id> [--json]`: stop the current conversation turn and keep its session open; idle is a no-op
- `lyra session prompt <session-id> [--stdin] [--expected-generation <generation>] [--json]`: send the text on standard input to a session (the text is never put on the command line or in a log); an agent may target its tree or sessions it started (until a detach or a move into another tree), while a person is unrestricted
- `lyra session read <session-id> [--since <cursor>] [--limit <count>] [--source <auto|transcript|terminal>] [--json]`: read what a session's agent did and said: a Claude Code transcript (the newest items, 20 unless --limit, or only those after --since <cursor>), or for other agents the text on its terminal screen (60 lines unless --limit); --source auto picks the transcript where one exists; an agent reads only sessions in its own tree, and nothing is sent to the session; a Worker reads no session (G16, V-348)
- `lyra session turns <session-id> [--cursor <cursor>] [--json]`: read the stored conversation cards of a session (starts no provider, terminal or tool)
- `lyra session model-calls <session-id> --since <epoch-ms> --until <epoch-ms> [--cursor <cursor>] [--limit <count>] [--json]`: read Lyra-caused model calls and purpose counts in an inclusive epoch-millisecond window; incomplete evidence is an error
- `lyra session rename <session-id> <title> [--expected-revision <revision>] [--json]`: set the title you chose; a later model summary does not overwrite it
- `lyra session retry <session-id> <turn-id> [--expected-attempt <attempt>] [--json]`: produce a turn's model output again, reusing saved side-effect receipts; an unsafe retry is refused
- `lyra session detach <session-id> [--request-id <request-id>] [--yes] [--json]`: irreversibly detach a live Lead and its branch as a new Orchestrator tree at depth 0; a person or its tree's Orchestrator may do it, never the session itself
- `lyra session move <session-id> --to <parent-session-id> [--request-id <request-id>] [--json]`: move a live Worker or Lead and its branch; a person, the tree's Orchestrator, or a Lead above both places may do it; old-parent tasks run by the moving branch transfer to the new parent with notices; a move into another tree ends the old tree's starter prompt rights
- `lyra session set-role <session-id> --role <lead|worker> [--request-id <request-id>] [--json]`: change a live session's role where depth, live children and owned open tasks allow; a person, its parent or the tree's Orchestrator may do it
- `lyra session force-stop <session-id> [--request-id <request-id>] [--yes] [--json]`: irreversibly end the agent process; a person may stop any session, an Orchestrator or Lead only a session below it, and a Worker none. Active attempts fail as force-stopped and stay with their owner for explicit retry or reassignment; unknown is exit 3, never process-death proof, and the task fails by itself once the process is proven gone (a person may end it sooner with `task cancel --abandon-unproven`). Requires support on the execution host; no ordinary-close fallback
- `lyra session close <session-id> [--expected-generation <generation>] [--yes] [--json]`: stop a session (not the same as closing a view); requested, closed and unknown are reported apart
- `lyra session resumable <session-id> [--json]`: tell whether a session can be attached or resumed, or why not (starts nothing)
- `lyra session continue <session-id> [--expected-binding-revision <revision>] [--json]`: attach to or resume a session on its original host and folder; it never starts a second writer; an agent must be allowed to start the predecessor's role and the target must be in its tree or directly started by it; a person is unrestricted (V-333)
- `lyra session reset <session-id> --resume-file <note-file> [--request-id <request-id>] [--yes] [--json]`: clear the same Claude Code session at its next rest and deliver the note as its first input (V-380)

**inbox**

- `lyra inbox list [--state <state>] [--kind <kind>] [--cursor <cursor>] [--json]`: list inbox items of one snapshot with its pending count; a list that could not be read is a failure, never zero pending
- `lyra inbox count [--json]`: count pending inbox items (the same snapshot count the screens show)
- `lyra inbox show <item-id> [--json]`: show one inbox item with its choices and the version an answer must carry
- `lyra inbox answer <item-id> [--answer-stdin] --expected-version <version> [--json]`: answer an item with a JSON object on standard input: kind approve/reject, choice/free with value, or grouped with answers; a stale version leaves the item as it was
- `lyra inbox modify <item-id> --file <path> --expected-version <version> [--json]`: replace a pending approval's proposal with the contents of a file; the new proposal needs a fresh approval

**status**

- `lyra status show [--session <session-id>] [--json]`: show the five status axes, observation times and aggregates from home
- `lyra status wait --session <session-id> --for <condition> [--wait] [--json]`: check a status condition, or wait with --wait; Ctrl-C cancels reception only

**message**

- `lyra message send --to <to> [--stdin] [--file <file>] [--thread <thread>] [--task <task>] [--attempt <attempt>] [--request-id <request-id>] [--urgent] [--json]`: accept a message body from stdin or file; closed or failed recipients refuse new mail with message-recipient-closed; same-request replay preserves the first receipt; acceptance is separate from acknowledgement; --urgent ends the recipient's wait at once instead of being held
- `lyra message ask [<question>] [--to <to>] [--resume <question-id>] [--timeout <duration>] [--thread <thread>] [--task <task>] [--attempt <attempt>] [--request-id <request-id>] [--list] [--json]`: create question mail and block for its paired reply; default 10m, maximum 30m; the question ID and resume command go to standard error before the wait; resume reads the same question without creating mail; list shows your own questions and their state
- `lyra message reply <question-id> <answer> [--request-id <request-id>] [--json]`: recipient-only answer, once; identical request and body replay
- `lyra message check [--wait] [--type <type>] [--consumer-generation <consumer-generation>] [--json]`: claim and print the current recipient batch; act on it, then run message ack; an unacknowledged batch is replayed; --wait holds non-urgent mail up to the Settings interval
- `lyra message ack <delivery-id> --consumer-generation <consumer-generation> [--request-id <request-id>] [--json]`: acknowledge a claimed batch after acting on every message; a handoff in it transfers ownership; repeats answer duplicate
- `lyra message show <message-id> [--json]`: read an original message without claiming or acknowledging it
- `lyra message thread <thread-id> [--cursor <cursor>] [--json]`: read original messages and delivery states in one thread

**task**

- `lyra task create [--orchestrator-session <orchestrator-session>] --spec-file <spec-file> [--depends-on <depends-on>] [--kind <kind>] [--deadline <time|none>] [--max-attempts <n|none>] [--on-disconnect <on-disconnect>] [--request-id <request-id>] [--json]`: create a task from a file; comma-separated dependencies form its DAG; --deadline accepts RFC3339 or Unix milliseconds and only notifies; --max-attempts caps failed attempts, none disables the cap, omission captures the Settings default (initially 3)
- `lyra task set <task-id> [--deadline <time|none>] [--max-attempts <n|none>] [--expected-owner-generation <generation>] [--expected-revision <revision>] [--request-id <request-id>] [--json]`: change a task deadline or failed-attempt cap; owner or person moves deadlines and lowers caps, only a person raises or removes a finite cap; none clears a value; no automatic action
- `lyra task list [--ready] [--cursor <cursor>] [--json]`: read tasks, readiness, deadline, overdue flag and failed/allowed attempts without starting work
- `lyra task wait [--all] [--timeout <duration>] [--json]`: wait for a message, held outgoing mail or changed Worker condition; --all returns one message batch, then message-held events in acceptance order, then task-overdue events in task-list order, then Worker conditions (including worker-wait-too-long) in task-list order; approval/tool limits default to 10/60 minutes, apply after home restarts, and only show/tell; overdue events are recorded once per task deadline; wait-limit events are recorded once per wait; held IDs are recorded while listed; a positive omitted count is reported once until an observed zero re-arms it; --timeout (15m, 900s) returns a checkpoint; otherwise wait without a time limit; print one result and exit 0; after acting on every message event, explicitly ack its delivery and consumer generation before re-arming
- `lyra task show <task-id> [--brief] [--json]`: read current ownership, attempts, handoff and result
- `lyra task dispatch <task-id> --worker-session <worker-session> [--host <host>] [--on-disconnect <on-disconnect>] [--expected-owner-generation <generation>] [--request-id <request-id>] [--reuse-mode <reuse-mode>] [--expected-terminal-owner-attempt <expected-terminal-owner-attempt>] [--expected-incarnation <expected-incarnation>] [--expected-terminal-task-owner-generation <expected-terminal-task-owner-generation>] [--json]`: supervised dispatch; an agent is refused (also on retry) only when a detach or move took the selected session out of its tree and it holds neither prompt rights nor current task custody of the session terminal, so a never-linked session a person opened takes the task as before; detach/move fence old outside custody even for finished tasks; old-terminal reuse refuses its re-link fence even if starter prompt rights remain; this admission rule adds no restriction to calls without V-55 context and existing caller-context requirements remain; dispatch-outside-tree repairs are `worker start --task <id>`, or `terminal reuse` with an owned idle Worker; accepted is separate from completed, unknown exits 3
- `lyra task handoff <task-id> [--worker-session <worker-session>] [--abandon] [--attempt <attempt>] [--expected-owner-generation <generation>] [--request-id <request-id>] [--reuse-mode <reuse-mode>] [--expected-terminal-owner-attempt <expected-terminal-owner-attempt>] [--expected-incarnation <expected-incarnation>] [--expected-terminal-task-owner-generation <expected-terminal-task-owner-generation>] [--yes] [--json]`: transfer ownership on receipt; --abandon requires confirmation and proven closure
- `lyra task retry <task-id> [--expected-owner-generation <generation>] [--request-id <request-id>] [--abandon-unproven] [--yes] [--json]`: make a failed or stopped task ready for another dispatch; --abandon-unproven is for a person only (an agent caller is refused): it first ends an unconfirmed dispatch, accepting that it may still run
- `lyra task settle <task-id> --outcome <outcome> --reason <one-line-reason> [--expected-owner-generation <generation>] [--request-id <request-id>] [--json]`: as the task owner or a person, settle a closed Worker's task with a required one-line reason
- `lyra task report <task-id> --attempt <attempt-id> --outcome <outcome> [--summary <text>] [--request-id <request-id>] [--json]`: report the result of the attempt you were given, with --summary saying why when it failed; stopping to talk is not a report
- `lyra task remove <task-id> [--request-id <request-id>] [--yes] [--json]`: remove a task from its DAG; retained records remain in home
- `lyra task cancel <task-id> [--expected-owner-generation <generation>] [--attempt <attempt>] [--request-id <request-id>] [--abandon-unproven] [--yes] [--json]`: request a stop; acceptance does not confirm execution termination; --abandon-unproven is for a person only (an agent caller is refused): it ends an unconfirmed dispatch, accepting that it may still run
- `lyra task adopt --from <session-id> [--request-id <request-id>] [--yes] [--json]`: as a new session, take over the plan and tasks of a session that ended (failed, closed or gone)

**gate**

- `lyra gate create --task <task> --question-file <question-file> --options-file <options-file> [--expected-owner-generation <generation>] [--request-id <request-id>] [--json]`: create a decision gate through the authorized Orchestrator; option file contains a JSON array
- `lyra gate list [--task <task>] [--cursor <cursor>] [--json]`: read pending and resolved decisions without resolving them
- `lyra gate resolve <gate-id> [--choice-stdin] [--task <task>] [--expected-owner-generation <generation>] [--request-id <request-id>] [--json]`: resolve a decision using stdin and current Orchestrator authority

**terminal**

- `lyra terminal list [--workspace <workspace>] [--terminal-state <reclaimable>] [--json]`: list shell execution IDs, or --terminal-state reclaimable to count finished Workers kept for reuse, with their outcomes, settlement times, task owners and release commands for the task owner or plan Orchestrator; an agent sees its own tree; a listed release command is not permission to run it
- `lyra terminal show [<execution-terminal-id>] [--worker-session <worker-session-id>] [--json]`: read a shell by execution ID or a Worker by session; show ledger ID and fences
- `lyra terminal shells --workspace <workspace> [--json]`: list the shells a new terminal can use on the workspace's host (Windows only)
- `lyra terminal split <terminal-id> --direction <direction> [--expected-incarnation <expected-incarnation>] [--request-id <request-id>] [--shell <shell>] [--json]`: create a separate shell terminal on the source host; never duplicate an agent
- `lyra terminal attach <terminal-id> [--expected-incarnation <expected-incarnation>] [--json]`: view the existing PTY; only foreground TTY input can claim an input lease
- `lyra terminal reopen <terminal-id> [--expected-incarnation <expected-incarnation>] [--json]`: alias of attach; missing execution never spawns a replacement
- `lyra terminal detach <terminal-id> --view-ref <view-ref> [--expected-incarnation <expected-incarnation>] [--json]`: dismiss one attached view; do not stop or release the terminal
- `lyra terminal release [<worker-terminal-ledger-id>] [--task <task-id>] [--worker-session <worker-session-id>] [--execution-terminal <execution-terminal-id>] [--request-id <request-id>] [--expected-terminal-owner-attempt <expected-terminal-owner-attempt>] [--expected-incarnation <expected-incarnation>] [--expected-terminal-task-owner-generation <expected-terminal-task-owner-generation>] [--yes] [--json]`: release a settled Worker on the person's request, or with their agreement when reuse is impossible, only after home preservation verification; otherwise keep it open for reuse
- `lyra terminal reuse [<worker-terminal-ledger-id>] [--worker-session <worker-session-id>] [--execution-terminal <execution-terminal-id>] --task <task> [--expected-owner-generation <generation>] [--request-id <request-id>] [--reuse-mode <reuse-mode>] [--expected-terminal-owner-attempt <expected-terminal-owner-attempt>] [--expected-incarnation <expected-incarnation>] [--expected-terminal-task-owner-generation <expected-terminal-task-owner-generation>] [--json]`: reuse the same Worker terminal for a new task using all ownership fences; an agent needs prompt rights or current task custody, including custody granted by adoption without prompt rights; detach/move fence old outside custody even for finished tasks; fenced old-terminal reuse refuses even if starter prompt rights remain, while owners moving with their branch or remaining in its tree retain custody; this admission rule adds no restriction to calls without V-55 context and existing caller-context requirements remain
- `lyra terminal create --workspace <workspace> [--shell <shell>] [--title <title>] [--request-id <request-id>] [--json]`: start a shell terminal in a workspace on its host; the same --request-id returns the same shell
- `lyra terminal send <terminal-id> [--stdin] [--file <file>] [--text <text>] [--enter] [--interrupt] [--expected-incarnation <expected-incarnation>] [--json]`: type text from --stdin or --file into a running shell (--enter: Enter, --interrupt: Ctrl-C); --text shows in the process list, never secrets
- `lyra terminal read <terminal-id> [--limit <lines>] [--cursor <cursor>] [--json]`: read a shell's screen and scrollback as text (last 120 lines; --cursor: unchanged since that read?)
- `lyra terminal close <terminal-id> [--expected-incarnation <expected-incarnation>] [--yes] [--json]`: stop a shell terminal's process (closing an app tab only detaches)
- `lyra terminal rename <terminal-id> [--title <title>] [--json]`: set a shell terminal's title; without --title it is cleared

**skills**

- `lyra skills list [--installed] [--json]`: list bundled skills with one-line descriptions; no runtime required
- `lyra skills status [--json]`: show local installed skills; alias of skills list --installed
- `lyra skills get <name> [--references] [--reference <name>] [--full] [--json]`: print the matching core guide, list references, read one reference or print the full manual; no runtime required
- `lyra skills install [<name>] [--agent <agent>] [--replace-old-copy] [--host-trash] [--from <zip>] [--json]`: install one shared skill or a verified local release zip; --replace-old-copy trashes a marked agent copy first
- `lyra skills update [--agent <agent>] [--repair-links] [--host-trash] [--skill <name>] [--json]`: update the shared folder once; --repair-links installs missing skills and repairs detected agents' links

**worker**

- `lyra worker start [--role <lead|worker>] [--spec-file <spec-file>] [--task <task-id>] [--project <project-id>] [--name <workspace-name>] [--workspace <workspace-id|current>] [--host <host>] [--agent <name>] [--model <model>] [--effort <level>] [--title <session-title>] [--depends-on <depends-on>] [--kind <kind>] [--on-disconnect <on-disconnect>] [--handoff] [--location <execution-location>] [--root <source-root>] [--base <branch>] [--branch <new-branch>] [--reuse-branch] [--setup <run|skip>] [--trust] [--json]`: start a fresh Worker under its task owner: use --task for an existing ready task or --spec-file to create a task; use --workspace current, an existing Workspace, or --project and --name; failed or stopped tasks need task retry first; it requires the current task owner as its Lyra caller session; --task refuses nonstartable or other-owned tasks before creation and cannot be combined with task-creation flags or --handoff; failed steps retain created resources

- `lyra orchestrator start --spec-file <brief> [--workspace <workspace-id|current>] [--agent <name>] [--json]`: person, Orchestrator or Lead starts a parentless tree; an agent retains its starter depth and inherits its Workspace when omitted, while a person supplies --workspace and --agent; an agent may omit --agent to inherit its recorded Profile; capability-checked brief delivery refuses older daemons and preserves the opened session.

Roles are recorded in home. `worker start` defaults to `worker`, which starts
nothing; use `--role lead` for a session that needs children within the depth
limit. `worker start --handoff` takes the giver's role and position. A running
task may be handed to another existing receiver: the receiver keeps its place,
the running Worker goes below it, and only the receiver hears the report. Role,
loop and whole-branch depth checks run before the message and again at receipt;
a failed receipt check returns the handoff. New receiving sessions take Ready
tasks only. Handoff, session move, adoption and ordinary messages are distinct.

**connection**

The open Lyra app sends Jira and GitHub requests. Adding, checking and removing
connections are person-only; an agent asks the person to use Settings → Issue connections.

- `lyra connection list [--json]`: list Jira and GitHub connections with the account, the last poll and the last error (no tokens)
- `lyra connection add <name> --kind <kind> --url <base-url> --auth <auth> [--user <name-or-email>] [--poll-seconds <seconds>] [--token-stdin] [--json]`: person only; add a connection and check it; jira-basic needs --user; the password or token is typed at a hidden prompt, or read as one line from standard input with --token-stdin; polls every 60 seconds unless --poll-seconds (30 or more)
- `lyra connection check <connection> [--json]`: person only; check a connection's address and sign-in now; exits 1 and prints the reason when it fails
- `lyra connection poll-now <connection> [--json]`: poll a connection now and list the open issues assigned to its account; exits 1 and prints the reason when the poll fails
- `lyra connection remove <connection> [--yes] [--json]`: person only, with their consent; delete the connection and its stored password or token

**issue**

- `lyra issue list [--connection <name>] [--json]`: list open issues assigned to the connected account on one or every connection
- `lyra issue show <key> [--connection <connection>] [--json]`: show one issue by key (ABC-123 for Jira, owner/repo#12 for GitHub); --connection names the connection when the key alone is not enough
- `lyra issue comment <key> [--body <text>] [--body-file <path|->] [--connection <connection>] [--json]`: post a plain-text comment with the connection's account; from a Lyra session the comment is recorded for that session; give exactly one of --body and --body-file (`-` reads standard input)

**workflow**

- `lyra workflow save --file <file> [--json]`: save a workflow file; a new workflow is saved off, and a file whose name exists becomes that workflow's next version and keeps its on or off
- `lyra workflow list [--json]`: list saved workflows with their trigger, on or off, and last run
- `lyra workflow show <workflow> [--json]`: show a workflow and its current file, by id or name
- `lyra workflow enable <workflow> [--json]`: turn a workflow's trigger on
- `lyra workflow disable <workflow> [--json]`: turn a workflow's trigger off; a manual run still works
- `lyra workflow remove <workflow> [--yes] [--json]`: delete a workflow, its versions and its runs; the workspaces runs made stay
- `lyra workflow run <workflow> [--issue <key>] [--issue-file <file>] [--connection <name>] [--request-id <request-id>] [--json]`: start a run by hand, with an issue key or an issue as a JSON file
- `lyra workflow runs [--workflow <workflow>] [--limit <n>] [--json]`: list recent runs, newest first
- `lyra workflow run-show <run-id> [--json]`: show a run: each step's state, reason, workspace, session or terminal, outputs and links
- `lyra workflow run-output <run-id> --step <step> --name <output> [--json]`: print one output a run's step kept, in full; it stays readable after the workspace is gone
- `lyra workflow run-stop <run-id> [--no-wait] [--json]`: stop a run: its running step's session or terminal is stopped and the run ends stopped; waits until the end is confirmed, or with --no-wait answers once the stop is requested
- `lyra workflow run-clean <run-id> [--yes] [--json]`: delete the workspaces an ended run made, with their folders and the files left uncommitted in them; without --yes it lists them and asks first, and deletes nothing if they changed since; --yes deletes without showing a list first; a branch with commits is kept, and the run and its outputs stay
- `lyra workflow record [--kind <kind>] [--about <question>] [--option <option>]... [--chose <choice>] --why <reason> [--evidence <kind>:<value>]... [--skip <item>] [--request-id <request-id>] [--json]`: from a running workflow step: keep a choice record (what you chose, why, on what evidence: file:, output:, check:, command:, link:, quote:), or skip a requested item (records, output:<name>) with its reason
- `lyra workflow records <run-id> [--step <step>] [--writer <writer>] [--json]`: list a run's choice records in order, each evidence marked observed, kept or stated

**search**

- `lyra search <query> [--json]`: find workspaces, conversation sessions, profiles and projects whose name contains the text (put several words in quotes); no match is said plainly, and a source that could not be read is named, never counted as zero

## Request receipts

- `lyra request show <request-id> --operation <operation> [--session <session-id>] [--json]`: read a stored request receipt without retrying; a person may select --session, an agent reads its own scope
