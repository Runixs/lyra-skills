## Show a file or page in Projects

Inside a Lyra-launched `Projects` agent Session (a floating agent and its
children included), queue a target in that Session's execution pane. Use
`lyra open <file-or-url>`, not a bare `open` or `xdg-open`: those open the
target outside Lyra, where the person working with you does not see it.

```text
lyra open ./preview.html --json
lyra open https://example.test/page --json
lyra open ./src/main.ts --request-id preview-one --json
```

A relative file resolves against the calling process's folder on its Host. The
result says `queued`: the desktop may not be showing `Projects` yet. After an
unknown result, repeat the same target with the same request ID; another target
with that ID is refused. Lyra sets `BROWSER=lyra open %s` for the agent
sessions it launches, when no browser is configured, so tools that open a
browser land here too: every agent session on the person's own machine, and on
a remote Host while its route to Lyra is live. Plain shell tabs and `Lyra`
screen conversations do not get it, and a remote Host's localhost is not
forwarded. A sign-in page opened through `BROWSER` lands in a Lyra tab: tell
the person to press the tab's open-in-browser button (브라우저에서 열기,
beside reload) to finish signing in in their own browser.

## Read a Workspace's files and Git state

All read only, through the Workspace's Host:

```text
lyra file list <workspace-id> --dir src --json
lyra file read <workspace-id> src/main.rs --json
lyra git status <workspace-id> --line-stats --json
lyra git diff <workspace-id> src/main.rs --area unstaged --json
```

Paths are relative to the Workspace. A cut-off listing says so; a file too large
or not text is named, not printed. `git status` tells "not a repository" apart
from "Git unavailable". `git diff` shows one file, `--area staged` or `unstaged`.

## Terminals

```text
lyra terminal list --workspace <workspace-id> --json
lyra terminal show <execution-terminal-id> --json
lyra terminal attach <execution-terminal-id>
lyra terminal split <execution-terminal-id> --direction right --json
lyra terminal detach <execution-terminal-id> --view-ref <view-ref> --json
```

- `terminal attach` (and its alias `reopen`) shows the running terminal. If the
  terminal no longer runs, nothing new is started. Only a person at a foreground
  terminal can type into it; piped or `--json` use only watches, and `--json`
  streams events instead of returning one answer. Ctrl-C detaches the view and
  does not stop the terminal.
- `terminal split` opens a separate shell on the same Host (`--direction right`
  or `down`); it never starts a second copy of the agent.
- `terminal detach` closes one attached view named by its view reference; the
  terminal keeps running.
- Keep a finished Worker's terminal open for reuse by its session ID with
  the `lyra-orchestration` skill. Report how many are kept; `lyra terminal release`
  frees them only on the person's request, or with their agreement when reuse
  is impossible.

### Plain shells: start, type, read, stop

```text
lyra terminal create --workspace <workspace-id> --title runner --json
lyra terminal read <terminal-id> --json
cat command.txt | lyra terminal send <terminal-id> --stdin --enter --json
lyra terminal send <terminal-id> --text <command> --enter --json
lyra terminal send <terminal-id> --interrupt --json
lyra terminal read <terminal-id> --cursor <cursor> --json
lyra terminal close <terminal-id> --yes --json
```

- `terminal create` starts a shell in the Workspace's folder on the Workspace's
  Host (this computer, WSL/Linux, Windows or a remote server). On Windows,
  `--shell cmd|powershell|git-bash` picks the shell (`terminal shells` lists
  them); elsewhere the login shell starts. The shell also appears in the app's
  New terminal list. If the answer is lost (exit 3), run the same command again
  with the `--request-id` it printed: the same shell comes back, never a second.
- Read until the prompt shows before the first send: text typed before the
  shell is ready can be cut by the operating system.
- `terminal send` types text from `--stdin`, `--file` or `--text` (one of
  them); a final newline of stdin or the file is dropped, `--enter` presses
  Enter and `--interrupt` presses Ctrl-C (it stops a running command). `--text`
  is typed exactly, so `--text " "` is a space; it shows in the process list, so
  never put a secret in it. Success means every byte reached the shell. It is
  plain typing, not taking over a Worker, and never starts anything else.
  - `terminal.send-rejected` (exit 1): nothing was typed because someone else
    took the input first; send again when they are done.
  - `terminal.send-unavailable` (exit 1): that Host's Lyra is too old to confirm
    typing; nothing was typed.
  - Exit 3: Lyra cannot tell how much arrived. Nothing more arrives later:
    part of the text may be typed, the rest (and the Enter) never is. Read the
    screen before sending again; sending again types it again.
  - A line longer than the screen is slow to type, because the shell redraws
    it for every key. Send long text in parts, or write a script file and run it.
- `terminal read` returns the screen and scrollback as text lines, last 120 by
  default (`--limit` up to 2000), plus a `seq` cursor. Pass that cursor back with
  `--cursor`: if nothing was printed since, the answer is `changed: false` with
  no lines; otherwise it is the latest lines again (Lyra keeps the screen, not
  every byte, so it cannot cut out only the new part). Typical loop: send,
  wait, `read --cursor` until the prompt is back.
- `terminal close` stops the shell's process (`--yes` confirms). Closing a tab
  in the app only hides it; this ends the shell. An agent terminal's ID is not a
  shell ID (`not-found`): close an agent with `session close`.
- `terminal rename` sets `--title`, or clears it without `--title`;
  `terminal list` shows each shell's state and title.
