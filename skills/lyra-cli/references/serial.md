## Serial ports

The `serial` commands use the serial ports of the Host your Session runs on,
such as a board's USB-serial adapter plugged into that machine. A board plugged
into another computer cannot be reached from your Session.

```text
lyra serial list --json
lyra serial open <port> --baud 115200 --json
lyra serial write <port> $'\r' --json
lyra serial expect <port> "login:" --timeout 30 --offset <end-offset> --json
lyra serial read <port> --lines 50 --json
lyra serial read <port> --offset <next-offset> --max-bytes 8192 --json
lyra serial close <port> --json
```

1. **Open.** `serial list` prints each port's name; pass one exactly.
   `serial open` needs `--baud`: use the rate your task, the person or the
   board's documentation gives; if none does, ask. The defaults are 8 data
   bits, no parity, 1 stop bit and no flow control. An open refused with "an
   endpoint already exists or its start is unsettled" means an endpoint holds
   the port, or an earlier open or close of it has not settled. Use the port
   only after a `serial read` of it succeeds; if the read fails, follow its
   message. Close it to reopen with other settings only on the person's word.
2. **Write, then expect.** `serial write` sends the text byte for byte: no
   line ending is added, and `\r` inside quotes stays two characters. In bash
   or zsh send Enter as `$'\r'`, as in `$'uname -a\r'`. Its `result.endOffset`
   is the log end when the write started: pass it to `serial expect --offset`,
   so a fast reply is not missed. Without `--offset`, `expect` sees only
   output logged after it starts. It matches the text literally (no
   patterns), never across lost output, for 1 to 60 seconds (`--timeout`).
   Output from just before your write, such as an earlier prompt, can be
   logged after `endOffset`, and the board usually echoes your input: expect
   text that only the reply contains. A match returns `result.nextOffset`, the
   offset just after the text. No match in time is a failure (exit 1) naming
   the offset it reached; to wait longer, repeat it with the same `--offset`.
   If the output it searched crossed lost bytes (step 4), the timeout's
   `error.detail` has their `gaps` and `missing`, as a match's `result` does,
   and the `nextOffset` it reached; the text may have been in the lost bytes,
   so never conclude the board did not send it. A timeout with no lost bytes
   has no `error.detail`. Plain output prints the missing range and a line
   for each gap before the match or the error.
3. **Read.** `--lines <n>` shows the last lines (100 by default); `--offset`
   reads from that byte instead. Read with `--json`, and check `result.gaps`
   before you treat `result.text` as continuous: a gap at or after
   `result.offset` lies in the text or at its edge, `offset` minus
   `result.offset` bytes into the raw `result.bytes`, and the output on its
   two sides is not continuous, even where the text runs on (step 4). Plain
   output prints any capture failure and missing range first, then the text,
   with a line "Serial port <port>: ... lost at log offset <n> (...)" where
   each such gap falls. `--json` also has `result.nextOffset`,
   `result.endOffset`, `result.missing`, `result.failure` and
   `result.lastWriter`; the raw `bytes` come as numbers, several times the
   size of the text: keep `--max-bytes` small. Continue from
   `result.nextOffset` until it equals `result.endOffset`.
4. **Missing bytes.** Lyra keeps the newest 256 MiB of a port's output. A read
   or expect from an older offset first reports "bytes missing from X to Y"
   (`result.missing`) and goes on from the oldest kept byte. `result.gaps`
   marks each place output was lost. When Lyra dropped a counted number of
   bytes (`droppedBytes`), their offsets are missing too: a read stops before
   them, and the next read reports them in `result.missing`, then goes on. A
   `--lines` read whose newest bytes were dropped shows the last lines before
   them, with that range. A gap whose `droppedBytes` is null, as after a
   reopen, lost an unknown amount between two kept bytes, and a read does not
   stop there: the text runs on across it. Those bytes are gone: never guess
   what they held. If you need them, make the board print that output again
   when your task allows, or report the missing range.
5. **Capture stopped.** A `result.failure` (plain output: "Capture stopped:")
   names a fault and its next step: the log disk fell behind or failed, the
   adapter failed or was unplugged, or a write may be partial. Kept output
   stays readable, but `serial write` is refused. When capture has stopped,
   `expect` fails (exit 1) once it has read all kept output, instead of
   waiting. That failure carries what it read in `error.detail`: `missing`,
   `gaps`, `failure` and `nextOffset`; a timeout's `error.detail` (step 2)
   never has `failure`. Writing and recording resume only after
   `serial close` and `serial open`; the log keeps its bytes and offsets. Do
   that only for a port you opened; otherwise tell the person.
6. **Close.** When your task no longer needs a port you opened, stop it with
   `serial close`. Read what you need first: `read` and `expect` need an open
   port. A port someone else opened stays open unless the person asks.

## Rules

- Nothing locks the port: people and agents can all write. `result.lastWriter`
  in `open`, `read` and `write` names who wrote last; `"agent": false` is a
  person. When a person wrote recently (`atMs`), they may be typing: write
  only when your task needs it, and tell the person first.
- Trust only bytes you read. A write's success means the bytes were sent, not
  what the board did: check with `expect` or `read`.
- Never send a password or token: the text is a command-line argument. If the
  board asks for one, stop and ask the person.
- A write that Lyra refuses before its first byte exits 1: nothing was sent.
  Its message names the cause and next step, such as output still queued in
  the device (wait for it to drain, or check flow control), a text too long
  for the line speed (split it), another write in progress, or a stopped
  capture.
- Exit 3 on `open`, `write` or `close`: the outcome is unknown. Never repeat a
  write blindly: `read` first, then follow `error.next`.
