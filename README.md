# Lyra skills

English guides for Lyra commands and agent orchestration, released independently
from the Lyra application. Each immutable tag has a manifest and one release zip.

Supply a release zip locally (Lyra 0.1.42 or later):

```sh
lyra skills install --from ./lyra-skills-0.1.13.zip --agent codex
lyra skills status
lyra skills get lyra-cli
```

The CLI does not download skills. Each skill declares `minimumLyraVersion` in
the manifest. An older Lyra prints an advisory and still serves an intact guide.
Keep the minimum for the computer running the command, including SSH computers.

Validate with `python3 tools/release.py validate`; build the deterministic zip
with `python3 tools/release.py package`. Validate a supplied zip with
`python3 tools/release.py validate path/to/release.zip`. These tools need only
Python's standard library and never access the network. The manifest hashes
VERSION and all skill files; it excludes itself and the enclosing zip. Checksums
check integrity; this unsigned release trusts the publishing account.

After validation and packaging, commit the source and run
`python3 tools/release.py tag`. This command stops on validation, package or
Git failure and never replaces an existing tag. Stop the publication sequence
when any command fails; upload only a successfully checked tag and artifact.

Never replace a used tag. Edit here, increment VERSION and pointer version marks,
update the manifest, validate against the matching Lyra CLI, then cut a new tag.
Publish its zip before updating the discovery manifest on main. Lyra's private
repository explicitly promotes an exact tag into its offline test snapshot.

MIT License; see LICENSE.
