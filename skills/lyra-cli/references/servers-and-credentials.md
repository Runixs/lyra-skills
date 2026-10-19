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
  `home` process memory and never stores it; it is asked for when connecting:
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
