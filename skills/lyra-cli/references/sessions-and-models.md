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
  `modelEfforts`. A missing or null list cannot be checked, so Lyra refuses an
  effort for that model.
- `session configure` reads launch-template JSON that carries `expectedRevision`
  from `session configuration`. A Profile's model default and `home`'s global
  default (`session defaults` / `set-default`) are separate; `set-default`
  without `--model` clears the global default.
