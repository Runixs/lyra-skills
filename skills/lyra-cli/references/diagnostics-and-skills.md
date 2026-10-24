## Diagnostics and updates

```text
lyra doctor --json
lyra version --json
lyra process list --json
lyra trace list --json
lyra update status --json
lyra update check --json
```

- `doctor` runs read-only health checks through home, concurrently with a five-second deadline per check. Unavailable checks stay `unread`; it never connects hosts or fixes anything automatically.
- `version` prints the Lyra and bundled skills versions, without `home`.
- `process list` shows processes Lyra started on this machine; `process stop`
  stops one after checking its OS identity.
- `trace list` / `trace show` show recorded executions step by step.
- `update apply`, `update rollback` and `update recover` change a lyra-daemon's
  installed version or its work data; run them only on the person's decision.
  An unknown result is not permission to run them again.
- Before another Lyra version is installed on this computer, the person stops
  its idle lyra-daemon engine and keeper with `lyra daemon stop --json`;
  `lyra daemon start --json` starts it again. Both are a person's commands:
  an agent that Lyra started is refused (`home.guest-not-allowed`).
  `daemon-stop-busy` means work still runs: finish it and stop again; there
  is no force. An unknown result (exit 3) is not a stop: inspect both
  processes before installing.

## Install a Lyra skill for an agent

Run these only when the person asks; Lyra never installs skills by itself.

```text
lyra skills list --installed --json
lyra skills status --json
lyra skills install --from <release.zip> --agent codex --json
lyra skills get lyra-orchestration
lyra skills install lyra-orchestration --agent claude --json
lyra skills install lyra-cli --agent antigravity --json
lyra skills update --json
lyra skills update --repair-links --json
```

`skills status` is the read-only alias of `skills list --installed`.
`skills install --from <release.zip>` verifies a local release zip and installs
both whole skill folders; give a skill name to select only that skill. It never
downloads a release. Edited, extra and newer files stay protected. A failed
publication retains and names its old, new and staged paths for inspection.
`get` reads and verifies installed guide/reference files only when a whole-file
installation record is present. Until seed migration ships, all other layouts
use the compiled guide, including old or edited pointers and linked folders.
If a recorded whole installation has missing or changed guide/reference files,
`get` refuses and keeps the files.
The minimum Lyra version is advisory: stderr and JSON name the found and needed
versions, while an intact guide remains available. The shared folder is
`~/.agents/skills/<name>`; agents reach it so:

| `--agent` | Reads the shared copy | `install` also makes |
|---|---|---|
| `codex`, `opencode` | Directly | Nothing |
| `claude` | Through a link | The folder link `~/.claude/skills/<name>`, or under `CLAUDE_CONFIG_DIR` when set |
| `antigravity` | Through a link | The folder link `~/.gemini/config/skills/<name>` |

On Windows, `~` is `%USERPROFILE%` and the links are junctions. Lyra writes
nowhere else (not `CODEX_HOME` or OpenCode's own folders). The same file
already there is success (`result.installed: false`); the result names the
agent's `path` and the `realPath` behind its link. Without `--agent`, install
picks the one agent whose configuration folder exists (`~/.claude` or
`CLAUDE_CONFIG_DIR`, `~/.codex` or `CODEX_HOME`, OpenCode's configuration
folders, `~/.gemini/config` or `~/.gemini/antigravity-cli`); none or several →
`skill-agent-required`, with what it found in `error.detail.detected`.

`skills list --installed` changes nothing. Its `shared` row is `current` (a
newer marked copy counts as current and is never downgraded), `outdated` (an
older mark), `not-installed`, `edited` (a file or link in its place, missing
or invalid marks, or other content) or `unknown`. Each agent row reads
`direct`, `linked`, `link-missing`, `old-copy` (an older Lyra copy in the
agent's own folder), `own-folder` (someone's folder), `other-link` (a link
elsewhere), `not-installed` (no such agent here) or `unknown`. `needsAction`
and `repairable` count the rows.

`skills update` rewrites an `outdated` shared copy once for every agent;
`--skill <name>` limits it to one skill. `edited` or `unknown` copies stay as
they are and are listed in `result.skipped`; missing copies are not installed.
`--repair-links` also installs a missing shared copy and, for each Claude Code
or Antigravity found here, makes a missing link or turns an `old-copy` into a
link, moving that folder to the OS trash first (the person can restore it);
it stops with `skill-install-conflict` on an `edited` or `unknown` shared copy.
`skills install --replace-old-copy` does the same for one agent's `old-copy`.
Moving a copy to the trash is the person's decision. A folder the person made
and a link Lyra did not make are never touched. `result.updated` lists shared
copies only: read the links with `skills list --installed`.

`install` never overwrites different content; every refusal names the path in
`error.detail.path`:

| Code / `detail.reason` | Meaning | What the person can do |
|---|---|---|
| `skill-install-conflict` / `other-version` | Another version of this Lyra skill: in the shared folder, or an `old-copy` in the agent's folder | Shared: `skills update` for an older copy; keep a newer one. Agent folder: install again with `--replace-old-copy` |
| `skill-install-conflict` / `different` | Someone else's skill with the same name | Keep it, or move it away |
| `skill-install-conflict` / `incomplete` | A folder without a complete `SKILL.md`, for example an interrupted install | Remove that folder, then install again |
| `skill-install-conflict` / `not-a-folder` | A file sits where the skill folder belongs | Move the file away |
| `skill-install-linked` | A link Lyra did not make (another folder or skill, a linked file or parent, a broken link); `error.detail.target` names its target | Keep it, or have the person change the layout |
| `skill-trash-failed`, `skill-link-failed` | The old copy could not go to the trash, or the link could not be made; nothing was substituted | Look at that folder, then run the command again |
| `skill-home-unavailable` | `HOME` (`USERPROFILE` on Windows), or a variable such as `CLAUDE_CONFIG_DIR`, is empty or relative | Set it to an absolute folder |

Do not delete or replace the person's files yourself to get past a refusal.
