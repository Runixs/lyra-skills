## Sessions in depth

```text
lyra session list --workspace <workspace-id> --json
lyra session rename <session-id> <title> --expected-revision <revision> --json
lyra session resumable <session-id> --json
lyra session continue <session-id> --json
```

- `session list` and `session show` give each Session's Host, state, title,
  `conditions` (Profile, model and where it came from), `parentSessionId` (the
  Orchestrator of the task its latest attempt ran) and `settlement`. A list
  that could not be read is a failure, never an empty list.
- Quote a title with spaces for your shell. `--expected-revision` (also on
  `workspace rename` and `workspace remove`) is the revision you read; a change
  made in between is refused instead of overwritten.
- `session resumable` says whether a Session can be attached or resumed, and
  why not; it starts nothing. `session continue` resumes on the original Host
  and folder and never starts a second writer; in this build it resumes `Lyra`
  screen conversations only.
- `session retry` is refused in this build
  (`session.retry-delivery-port-unavailable`). To repeat work, tell the person
  and open a new Session only if they ask.
- `session model-calls` lists the inputs Lyra itself typed into a Session
  (task dispatches, recovery "continue", message lines), not the person's.

## Models and saved launch settings

Change saved settings only when the person asks, never to open one Session:

```text
lyra session models <workspace-id> --agent claude --json
lyra session configuration <profile-id> --json
lyra session defaults <harness-kind> --json
lyra session set-default <harness-kind> --model <model-id> --expected-revision <revision> --json
cat launch.json | lyra session configure <profile-id> --stdin --json
```

- `session models` reads the real catalog for an agent, with each model's
  `modelEfforts`. On a Profile with no saved model name, a missing or null list
  cannot be checked, so Lyra refuses an effort for that model.
- `session configure` reads launch-template JSON that carries `expectedRevision`
  from `session configuration`. A Profile's model default and `home`'s global
  default (`session defaults` / `set-default`) are separate; `set-default`
  without `--model` clears the global default.
- The template's optional `preLaunchCommand` is POSIX shell text that prepares
  the environment on the Host. Each opening runs it once, before that opening's
  own model list read and the agent launch. It gets no input and has 30
  seconds; a failure stops the opening. Leaving it out keeps the saved command;
  null or a blank value clears it. A Windows Host refuses it. Its text is saved
  and `session configuration` prints it: never write a key or token into it;
  have the command fetch one.
- `session models` never runs that command. When the Profile has no saved model
  name, `session open` and `worker start` check an explicit `--model` or
  `--effort` against the `session models` list before the opening starts, so
  the check sees no prepared environment: if the list fails or lacks the model
  or level, nothing is created and the command does not run. With a saved model
  name, or with neither flag, there is no such check: the opening prepares,
  then reads its own list, or none for a saved model name. For a Profile whose
  models need the command, leave both flags out, or ask the person to save the
  model name on the Profile.
- A Profile takes no model endpoint: `profile add` and `profile update` have no
  endpoint flags, and connection settings go through the agent's own settings
  file and `preLaunchCommand`. A Profile saved with an endpoint by an older
  Lyra stays readable.
- `profile add --model <name>` and `profile update --model <name>` save a model
  name on a Profile; `profile update --auto-model` clears it, so the model is
  chosen automatically. The two flags cannot be combined, and leaving both out
  of an update keeps the saved name. A Session on that Profile runs `--model`
  if given, else the saved name, with no model list read, so Lyra does not
  check it and the agent may refuse it. `--effort` there is checked only as a
  known level for that agent; the agent itself reports a level its model does
  not support. A mistyped level is refused with `session-effort-unknown`, which
  names `--effort`, the typed value and the known levels
  (`error.detail.allowed`). No Session or task is made, but a Workspace
  `worker start` just made stays in `created`; the same command with a known
  level reuses it. `session-effort-unsupported` stays the model list check of
  a Profile with no saved model name. A `lyra-daemon` too old to apply a saved
  name refuses the opening with `session.profile-model-unavailable`: tell the
  person, who updates it on that machine or clears the name.
