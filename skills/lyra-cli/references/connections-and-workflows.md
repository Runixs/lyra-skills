## Jira and GitHub connections

A connection is one Jira (Cloud, Server or Data Center) or GitHub (github.com
or Enterprise Server) account. Lyra polls it for the open issues assigned to
it; workflows start runs from those issues, and their steps comment on them.
Its password or token stays in this computer's credential store, never in an
argument, a file or a log.

```text
lyra connection list --json
lyra connection add work-jira --kind jira --url https://jira.example.com --auth jira-token --token-stdin --json
lyra connection poll-now work-jira --json
lyra issue show ABC-123 --json
lyra issue comment ABC-123 --body-file notes.md --json
```

- Adding is the person's step. `connection add` reads the password or token
  at a hidden prompt, or as one line from standard input with
  `--token-stdin`, and checks it before keeping it. Never put a token on a
  command line or in a file; ask the person to run the add.
- `--auth` is `jira-basic` (with `--user`), `jira-token` or `github-token`.
  `--poll-seconds` sets the interval: 30 or more, 60 when left out.
- `connection list` shows each connection's account, last poll and last
  error, never a token. `connection poll-now` polls at once and lists the
  open issues assigned to the account.
- Issue keys: `ABC-123` for Jira, `owner/repo#12` for GitHub. On
  `connection.ambiguous` more than one connection fits the key: repeat with
  `--connection` and the connection's name.
- `issue comment` posts plain text with the connection's account. Give
  exactly one of `--body` and `--body-file` (a dash reads standard input).
  From a Lyra session the comment is recorded for that session.

### When a connection refuses

- `connection.auth-refused`: the server refused the stored sign-in, and Lyra
  stops asking it so the account is not locked. Do not retry, and do not run
  `connection check`: only a person checks a connection, after fixing the
  password or token (`connection.check-by-person`). Tell the person.
- `connection.busy`: the server asked Lyra to wait; the line says how long.
  Ask again after that, not before.
- `issue.forbidden`: the account lacks a permission on that issue, which the
  line names. Tell the person.
- `issue.outside-run`: a workflow step comments only on its run's issue,
  through its run's connection. Comment there, or leave the other comment to
  a person.
- `connection.app-closed`: the Lyra app sends the Jira and GitHub requests
  and is not open, so nothing was sent. Tell the person.
- `connection.app-lost` on a comment: whether it was posted is unknown. Do
  not post it again; a person checks the issue's comments.

## Workflows

A workflow is a saved file: a trigger (an issue assigned on a connection, or a
person starting it) and the steps after it, each an agent Session or a
terminal command. A run records each step's state, reason and outputs.

```text
lyra workflow save --file triage.yaml --json
lyra workflow list --json
lyra workflow run triage --issue ABC-123 --json
lyra workflow runs --workflow triage --json
lyra workflow run-show <run-id> --json
lyra workflow run-output <run-id> --step fix --name notes --json
```

- `workflow save` takes the whole file; a name that exists becomes that
  workflow's next version. A refused file names each problem and its place.
- `workflow list` shows each trigger as on or off. `workflow enable` and
  `workflow disable` turn it on and off, and are the person's decision; a
  `workflow run` started by hand works either way.
- `workflow run-show` gives each step's state, reason, workspace, session or
  terminal, outputs and links. `workflow run-output` prints one kept output in
  full, also after its workspace is gone.
- `workflow run-stop` stops a run. `workflow run-clean` deletes the
  workspaces an ended run made, and `workflow remove` deletes a workflow with
  its versions and runs; pass `--yes` to either only on the person's word.
- A step working for an issue comments with `issue comment`. When its file
  asks for a comment, the step does not pass without one.
