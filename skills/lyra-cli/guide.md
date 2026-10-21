# Lyra CLI

Lyra runs coding agents in **Sessions**: one agent conversation each, with its
own terminal. A **Project** is a registered folder on a **Host** (this computer
or a remote server); a **Workspace** is one working copy of a Project (the
folder itself or a Git worktree) where Sessions run. To coordinate several
agents, or when Lyra typed you a task with a report footer, use the
`lyra-orchestration` skill.

## Rules for every command

- `home` (Lyra's core without a window) answers every command except `home`,
  `skills` and `version`. `home.not-running`: tell the person, and start it
  with `lyra home start --json` only on their word. `lyra home stop --json` is
  refused while work runs; `--force` is the person's decision.
- Use `--json`: success is `{"ok": true, "result": ...}`; a failure carries
  `error.class`, `error.code`, `error.message`, `error.next` and
  `error.detail`. Exit 0 success, 1 refused, 2 usage, 3 unknown.
- Follow `error.next` (`next:` in plain output), the step for that code,
  unless this skill names another step for it or needs the person's word.
- **Exit 3 means unknown, not failed.** Run the command in `error.detail.check`
  before anything else; never repeat a creation blindly.
- Use IDs from command output (agent selectors take names). Follow `--cursor`:
  a first page is not the whole list. A Host or list that could not be read is
  a failure or `unreadable`, never zero items.
- `--yes` only on the person's word: `project remove`, `workspace remove`,
  `workspace remove-branch`, `session close`, `session detach`, `terminal close`,
  `credential remove`, `server remove`, `process stop`, `update apply`,
  `update rollback` and `update remote-reset` cannot be undone.
- Text and secrets go through stdin or files, never arguments;
  `terminal send --text` is only for a short command without secrets. A path is
  spelled as its Host spells it (`/home/me/repo` on a remote Host).
- Forms often guessed wrong: the project is positional in
  `lyra workspace list <project-id> --json`, and `lyra version --json` prints
  the Lyra and skills versions. For any flag, add `--help` to the command
  (`lyra git diff --help`); never guess.

## Start work in a Project

```text
lyra host list --json
lyra project scan --host <host-id> --path /home/me/src --json
lyra project add /home/me/src/app --host <host-id> --json
lyra workspace create <project-id> feature-login --agent claude --json
lyra session show <session-id> --json
```

1. **Host.** `host list` names this computer and connected servers.
2. **Project, once.** `project add` registers the folder and opens its primary
   Workspace without an agent. If that opening fails, the Project is still kept
   and the command exits 0 with `result.notice` (`code`, `outcome`, `check`):
   do not add it again.
3. **Workspace.** `workspace create` makes the working copy, runs its setup and
   opens its first Session with `--agent`; the results are separate
   (`result.workspace`, `result.session`). Without `--agent` no Session opens
   (`session-profile-required`). A `failed` or `partial` setup exits 1 with
   `prepare-failed` and keeps the Workspace. Setup commands come from the
   folder's `.lyra/config.yaml` and run only with consent: `--trust` approves
   exactly the commands read now, `--setup skip` runs none. To adopt a
   worktree the person already made, without setup:
   `lyra workspace register <project-id> /home/me/src/app-wt --host <host-id> --json`.
4. **Session.** Opening reports `opening`, `active`, `failed` or `unknown`;
   read `session show` until it is `active`. Another Session in the same
   Workspace: `lyra session open <workspace-id> --agent claude --json`.

## Talk to a Session

```text
cat prompt.md | lyra session prompt <session-id> --stdin --json
lyra session interrupt <session-id> --json
lyra session close <session-id> --yes --json
```

- `session prompt` types the text into an active Session as if the person had
  typed it (up to 16 KiB; never on the command line or in a log). Accepted is
  not answered. Leave out `--expected-generation`: this build refuses it.
- An agent running in a terminal stores no conversation cards, so
  `session turns` has nothing to read for it (cards exist for `Lyra` screen
  conversations). To get an answer back, ask in the prompt for a file in the
  Workspace (read it with `file read`) or for a Lyra message.
- Exit 3 on a prompt: it may have arrived. Do not send it again blindly; check
  for the effect you asked for first.
- `session interrupt` stops the current turn and keeps the Session;
  `session close` stops the Session (closing a terminal view does not).

## Launch preferences

- `--agent claude`, `codex` or `opencode` picks that agent's canonical Profile
  on the destination Host; a Profile name the person gave picks that Profile (a
  company endpoint, another execution location). A Profile holds an endpoint
  and a location; model and effort are chosen when a Session opens.
- Pass `--model` only when the person asked for a model or a kind of model.
  Choose it from `lyra session models <workspace-id> --agent claude --json`;
  never read agent configuration files, caches or binaries to find one.
- Pass `--effort` only with `--model`, and only a level in that model's
  `modelEfforts` list; levels differ per model and opencode takes none. A
  refusal lists `error.detail.allowed`: pick one or ask.
- Never run `profile add` or `session configure` to open one Session; they
  change the person's saved settings for every later Session. When launch
  flags cannot express a request, say so and ask.

## References

Load only the one your next step needs, with
`lyra skills get lyra-cli --reference <name>`:

| When | `<name>` |
|---|---|
| Read a Workspace's files or Git state, show a file in Projects, plain shell terminals, attach or split | `files-and-terminals` |
| Sessions in depth: rename, resume, models and saved launch settings | `sessions-and-models` |
| Answer a pending approval or question in the Inbox | `inbox` |
| Connect a remote server, SSH keys, credentials | `servers-and-credentials` |
| Versions, processes, traces, updates, installing Lyra skills | `diagnostics-and-skills` |
| Jira and GitHub connections, issues and their comments, workflows and runs | `connections-and-workflows` |
| Every command in one list (for people; agents use `--help`) | `commands` |
