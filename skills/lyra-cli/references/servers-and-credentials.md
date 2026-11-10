## Remote servers and credentials

```text
lyra server ssh-hosts --json
lyra server import <ssh-alias> --json
lyra server connect <server-id> --json
lyra runtime detect --host <host-id> --json
```

- `server ssh-hosts` lists the Host aliases in `~/.ssh/config`; import only the
  alias the person chose. An imported server follows the person's SSH settings.
- `server add` needs either `--credential <credential-id>` (a stored key) or
  `--password`. With `--password`, Lyra keeps the SSH password only in the
  `lyra-daemon` process memory and never stores it (a company ID password
  differs: see below); it is asked for when connecting:
  `printf '%s\n' "$PASSWORD" | lyra server connect <server-id> --password-stdin`.
  Never write a password into a file, log or argument.
- `credential add-ssh` stores keys in the OS credential store: `--method agent`,
  `key` (with `--key-file`) or `key-with-passphrase` (passphrase on stdin).
  `--method password` is refused; use a password server as above.
- `server connect` holds the connection and prints one line per state change;
  Ctrl-C closes it. A failed or unknown state is not connected.
- `runtime detect` looks for agent runtimes on a Host (a remote Host over its
  server); `runtime list` shows what was found. An unreadable remote runtime is
  not an empty result.

## Workspaces on a server

After `server connect`, the server's Host is in `host list` (`host-<server-id>`).

```text
lyra project add <server-path> --host <host> --json
lyra project create <server-parent-path> <name> --host <host> --json
lyra workspace create <project-id> <name> --host <host> --root <source-root> --base <branch> --setup skip --json
```

- `project add` registers a checkout already on the server; `project create`
  makes a new, empty one there (a Git repository with no commit yet; `--no-git`
  for a plain folder).
- Pass `--base`: without it, a Workspace on another host starts from your own
  current Git branch, which the server has only after you push it and fetch it
  there (`workspace-base-ref-not-found`). `lyra project branches <project-id>`
  lists the branches the checkout has.
- A checkout with no commit has no branch to start from: make a first commit
  in it on the server (in a shell there, or in a terminal of the primary
  Workspace that `project add` opens), then create the Workspace. A plain
  folder has only that primary Workspace.
- A Workspace whose creation failed is kept as `failed`; remove it with
  `lyra workspace remove <workspace-id> --yes` before trying the same name.

## Company gateway sign-in

A company gateway in front of a server may ask a one-time code (OTP) after the
company ID password. Only a person types it. The company ID password is kept
in the OS credential store after a successful sign-in; a code never is.

- On a server registered with a company ID login (not an `~/.ssh/config` alias
  or a saved vault password), `lyra server connect <server-id>` at a terminal
  asks on the hidden line `One-time code (OTP) for <server> (not saved): ` and
  waits up to 300 seconds; Connect in the app asks too. The code goes once into
  the same sign-in. On other servers Lyra does not ask:
  `link-authentication-otp-needed`.
- When the gateway asks a code, a connect with `--password-stdin` (it carries
  the company ID password only), with piped input or from an agent session
  ends with `login-input-needs-person`; a piped connect with no saved password
  stops earlier, at `password-needed`. Do not run it again: each run sends the
  company ID password and makes the gateway ask again. Quote the message to the
  person and wait; never take a code from them to type it yourself.
- Lyra's own reconnect never asks: it stops with
  `link-reconnect-needs-one-time-code`, and a person connects.
- On a password server, `server list --json` rows carry `loginInput`:
  `"one-time-code"` while a sign-in waits for the code, otherwise `null`.

An agent quotes the code's row to the person and runs only its read commands.

| Code | Meaning | What the person can do |
|---|---|---|
| `login-input-required` | The sign-in waits for a code from the person who started the connection | Type it at that terminal, or in the app window that asks |
| `login-input-needs-person` | This command cannot ask: its input is not a terminal, `--password-stdin` was given, or it runs in an agent session. The sign-in was canceled; no code was sent | Run `lyra server connect <server-id>` in a terminal without `--password-stdin`, or press Connect in the app |
| `login-input-pending` | A sign-in with a code is in progress; its code may be asked on another screen (the app or a terminal) | Wait for it to end, or type or cancel the code there, then try again |
| `login-input-not-origin` | Only the screen that started the connection can answer its code | Type the code on that screen, or connect again here |
| `login-input-canceled` | No code was entered, so the sign-in was canceled; no code was sent | `server connect` again with the code at hand |
| `login-input-expired` | No code arrived within 300 seconds; no code was sent | `server connect` again and type the code when asked |
| `login-input-stale` | The wait stopped because the server settings changed or lyra-daemon is stopping | `server connect` again |
| `login-input-unavailable` | lyra-daemon could not keep track of the waiting sign-in | `lyra daemon status --json`, then `server connect` again |
| `login-input-outcome-unknown` | The code was sent, but lyra-daemon stopped following the sign-in: the result is not known | `lyra server list --json`; if not connected, `server connect` again with a new code |
| `link-one-time-code-refused` | The gateway did not accept the code | Check the new code in the authenticator app, then `server connect` again |
| `link-one-time-code-not-accepted` | The gateway closed the sign-in once the code was sent: the code was wrong or expired, the gateway stopped waiting, or the network dropped; Lyra cannot tell which | `server connect` again with a new code |
| `link-company-login-asked-after-code` | The gateway asked for a password after the code: the code was wrong and the sign-in started over, or the target server asks its own password | `server connect` again with a new code; if it repeats, connect with `ssh` in a terminal to see what it asks |
| `link-login-closed-while-waiting` | The gateway closed the sign-in while the code was being asked; no code was sent | `server connect` again and type a new code soon after it is asked |
| `link-reconnect-needs-one-time-code` | The gateway asked a code during Lyra's own reconnect; none was sent | Run `lyra server connect <server-id>` in a terminal, or press Connect in the app |
| `link-authentication-otp-needed` | A code was asked where Lyra does not ask a person for one: the server is not registered with a company ID login, or a second code was asked in one step; none was sent | Connect with `ssh` in a terminal and type the code there; `lyra server show <server-id> --json` shows the address |
| `password-needed` | Lyra needs a person's password first; nothing was sent. For example this command has no terminal and no `--password-stdin`, the server refused the password (`passwordState` is `paused` in `server list --json`), or another screen is asking (`input-pending`) | Run `lyra server connect <server-id>` in a terminal where you can type the password, or press Connect in the app; it asks, also for a paused company ID password, which is never sent again (`--retry-password` asks for a new value there too). A paused ordinary SSH password does not ask: first `lyra server update <server-id> --password`, or reuse it with `--retry-password`. Another screen: finish or cancel it there |
