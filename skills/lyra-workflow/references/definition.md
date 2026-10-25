## The workflow file

What `lyra workflow save --file <file> --json` reads in this Lyra (format 1).
Save refuses a field or a kind it does not read, by name and with its path,
so a file written for another Lyra is never misread. Quote a text value that
holds `: `, `#` or `${`.

```yaml
lyraWorkflow: 1                  # the format; required
name: fix-issue                  # saving a saved name makes its next version
description: What it does, in the person's words
orchestrator: lyra
limits: { maxTime: 2h }          # optional: s, m, h, d or mixed (1h30m)
policy: { outputs: requested, records: requested, checks: required }
floor: { records: requested }    # optional: the lowest level anything may set
nodes:                           # the steps, the trigger first
  - id: assigned
    kind: trigger
    on: signal                   # or manual: only by hand
    signal:
      connection: company-jira   # a connection's name
      event: issue-assigned      # the only event
      match: { project: ABC }    # or { repository: owner/name }
    project: billing             # the Lyra Project every step works in
  - id: fix
    kind: agent
    after: [assigned]            # earlier steps only
    agent: claude-code           # or codex, opencode
    model: opus                  # optional
    effort: medium               # optional: the agent's reasoning effort
    where: { workspace: { new: "${assigned.issue.key}" } }
    prompt: |
      Fix ${assigned.issue.key}: ${assigned.issue.title}
      ${assigned.issue.body}
    outputs:
      - { name: summary, type: text }
      - { name: notes, type: file, path: out/notes.md, level: required }
    timeout: 1h                  # optional: one attempt's limit
    pass:
      checks: [ { run: [cargo, test, --workspace], timeout: 10m } ]
      onFail: { retry: 2 }
```

- **`id`**: a letter, then letters, digits, `-` or `_`; unique in the file.
  `orchestrator` may only be `lyra`: the engine walks the run.
- **The trigger**: exactly one, with no `after`. `on: manual` runs only by
  hand (`--issue <key>` gives it an issue); `on: signal` starts a run for
  each issue newly assigned to the person on that connection. `project`
  names a registered Lyra Project. Its outputs are `issue` (`key`, `title`,
  `body`, `url`, `project`, `connection`, `connectionName`, `kind`) and
  `cause`.
- **An agent step** runs as a session (`launch: session`, the default) that
  gets `prompt` as its task, or as one command in a terminal
  (`launch: terminal` with `command: [program, arg, ...]`, one argument per
  item). In a terminal step `agent` is only a label, and `model`, `effort`,
  `profile`, `prompt`, a `text` output and its own records level are
  refused. `profile` names a saved Profile; `effort` asks the agent for a
  reasoning effort, as `--effort` does on `session open`, which refuses one
  its model does not offer. A build or a test is a terminal step or a
  step's checks: this Lyra has no `command` kind.
- **Its Workspace**: `where: { workspace: { new: <name> } }` makes a new
  Workspace in the trigger's Project, with its own branch; a taken name
  gets `-2`, `-3`. `where: { workspace: { step: <step> } }` works in the
  Workspace of an earlier agent step this one waits for, so a test sees the
  fix. Every attempt of a step works in the Workspace its first attempt
  made.
- **Outputs**: at most one `text` (the report's `--summary`) and up to 8
  `file` outputs, each a relative path to text up to 1 MB, kept in the run.
- **Bindings** `${<step>.<output>}`, `${<trigger>.issue.<field>}` and
  `${<trigger>.cause}` fill `prompt`, `command` items, check arguments and
  `where.workspace.new`. They name only steps this one waits for through
  `after`, and only declared outputs; a value still empty at the start fails
  the step. A bound file is pasted whole: keep documents short. The whole
  task, with Lyra's closing lines, must fit the agent's input (16 KiB), or
  the attempt fails (`workflow.step.task-too-long`).

## Levels

`policy: { outputs, records, checks }` at the top and on a step, `level` on
one output or one check, each `required`, `requested` (the default) or
`off`; the most specific wins. `floor: { outputs, records, checks }` at the
top is the lowest level anything runs at: save refuses a step's `policy` or
a `level` below it, with its path, and raises the top `policy` to it. An
output a later step binds, and the comment of
`pass: { comment: true }`, are `required` by themselves; a lower `level` on
a bound output is refused.

## Passing and failing

| Field | Means |
|---|---|
| `pass: { comment: true }` | the attempt passes only after it posts a comment on the run's issue |
| `pass: { checks: [ ... ] }` | up to 8; each `[program, arg, ...]` or `{ run: [program, arg, ...], timeout: 10m, level: required }`; Lyra runs them in order in the step's Workspace after the report, as a terminal step runs its command; `timeout` defaults to 10 minutes; a `required` one that does not exit 0 fails the attempt with the end of its own output, a `requested` one only warns |
| `pass: { onFail: { retry: <1 to 4> } }` | that many more attempts, counted again after each send-back into the step; there is no `pass.retry` |
| `pass: { onFail: { goto: { node: <step>, max: <1 to 10> } } }` | send the work back to an earlier agent step this one waits for; it starts again in its Workspace with a new session, and the steps after it that had started run again; `max` counts every send-back into that step in the run, from any step, a denial's included, and every `goto` into one step gives the same `max` |
| `needsApproval: true` (or `{}`) | the step asks the person in `Inbox` before it starts; a denial stops the run |
| `needsApproval: { onDeny: { goto: <step> } }` | a denial sends the work and the person's note to that step (the gated step itself, or an agent step it waits for); the gated step asks again in a new round when it comes up |
| `timeout: <time>` on a step | an attempt past it fails |

`onFail` serves every work failure of its step: a missing `required` item,
a failed `required` check, a `failed` report, a timeout. Without `onFail`
(or with `onFail: stop`), or with nothing automatic left, the attempt waits
in `Inbox` for the person: waive, one more attempt (at a reached `max`, one
more send-back, counted), or stop the run. A denial never goes through
`onFail`. A session that dies is started again once in the step's
Workspace, without counting as an attempt.

## The drawing (`layout`)

The Lyra app's workflow editor keeps how it drew the file in a top-level
`layout`. Drawing only: the engine never reads it, arrows come from `after`,
and the editor's end box is drawn by itself (the file has no end step).

```text
layout:
  direction: LR
  nodes: { assigned: { x: 0, y: 0 }, fix: { x: 280, y: 0 } }
  edges: { "assigned->fix": { from: r2, to: l2 } }
```

- `direction` is `LR` or `TB`; `nodes.<step>: { x, y }` places a step's box,
  two numbers; `edges."<from>-><to>": { from, to }` names the connection
  point at each end of an arrow, a side `l`, `r`, `t` or `b` and a number
  1 to 3. Every part is optional.
- Save refuses a `layout` of the wrong shape, by its path
  (`layout.nodes.fix.y`). An entry naming a step or an arrow the file does
  not have is only one of the save answer's `warnings`; the file saves.
- Writing a new file, leave `layout` out: the editor lays the steps out.
  Changing a file, keep it, and rename or remove the entries of a step you
  rename or remove.

## Not in this Lyra

The kinds `command`, `avatar`, `decide`, `workflow`, `loop` and `ask`, and
`each`, workflow `inputs` and `outputs`, `join`, schedule triggers
and `irreversible`. When the person needs
one, write the nearest shape and keep the wish as a YAML comment, so that
the file still saves.
