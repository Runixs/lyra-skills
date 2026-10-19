## Inbox

The Inbox holds approvals and questions from `Lyra` screen conversations for
the person. A terminal agent's own permission prompt or question never reaches
the Inbox: it shows only as that session's status, and the person answers it
in that terminal.

```text
lyra inbox count --json
lyra inbox list --state pending --json
lyra inbox show <item-id> --json
```

Answer only with the answer the person chose; Lyra does not check who answers.
`inbox show` gives the item's kind, its choices and the `version` an answer must
carry; a stale version leaves the item unchanged. A message or a prompt never
counts as an approval.

The answer is one JSON object on stdin:

| Item | Stdin object |
|---|---|
| Approval | `{"kind":"approve"}` or `{"kind":"reject"}` |
| Question, pick a listed choice | `{"kind":"choice","value":"<choice text>"}` |
| Question, free reply | `{"kind":"free","value":"<reply text>"}` |
| Question bundle | `{"kind":"grouped","answers":[{"questionId":"<id>","choiceIds":["<id>"],"text":"<optional text>"}]}` |

```text
printf '%s' '{"kind":"approve"}' | lyra inbox answer <item-id> --answer-stdin --expected-version <version> --json
lyra inbox modify <item-id> --file proposal.md --expected-version <version> --json
```

Text that is not one JSON object is a usage error (exit 2) and changes nothing.
`home` refuses a kind that does not fit the item, a choice that is not listed,
an incomplete bundle and a stale version. If the result is unknown (exit 3),
read `inbox show` before answering again. `inbox modify` replaces a pending
approval's proposal; the new proposal needs a fresh approval.
