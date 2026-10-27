"""Offline rejection tests for the public release tools."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from contextlib import redirect_stderr
import io
import warnings
import zipfile

import release


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.files = release.source_files()

    def manifest(self, change):
        files = copy.deepcopy(self.files)
        value = json.loads(files["manifest.json"])
        change(value)
        files["manifest.json"] = (json.dumps(value) + "\n").encode()
        return files

    def test_pointer_condition_is_observable_and_covers_references(self):
        for name in release.NAMES:
            pointer = self.files[f"skills/{name}/SKILL.md"].decode()
            self.assertIn("`lyra --version`", pointer)
            self.assertIn("below", pointer)
            self.assertIn("`references/`", pointer)
            body = pointer[4:].split("\n---\n", 1)[1]
            self.assertTrue(all(len(line) <= 88 for line in body.splitlines()), name)

    def test_complete_release(self):
        self.assertEqual(release.validate(self.files)["skillsVersion"], "0.1.25")

    def test_manifest_and_content_rejections(self):
        cases = [
            self.manifest(lambda m: m.update(formatVersion=2)),
            self.manifest(lambda m: m["skills"].append(m["skills"][0])),
            self.manifest(lambda m: m["skills"][0].update(name="foreign")),
            self.manifest(lambda m: m["skills"][0].update(minimumLyraVersion="1.2.3-01")),
            self.manifest(lambda m: m["skills"][0].update(minimumLyraVersion="wrong")),
            self.manifest(lambda m: m["files"].reverse()),
            self.manifest(lambda m: m["files"][0].update(size=123)),
            self.manifest(lambda m: m["files"][0].update(sha256="0" * 64)),
            self.manifest(lambda m: m["files"].append(m["files"][0])),
            self.manifest(lambda m: m["skills"][0].update(pointer="../SKILL.md")),
            {**self.files, "extra.md": b"extra\n"},
            {**self.files, "skills/LYRA-CLI/guide.md": b"extra\n"},
            {**self.files, "VERSION": b"\xff"},
            {**self.files, "VERSION": b"0.1.12\r\n"},
        ]
        missing = copy.deepcopy(self.files)
        del missing["skills/lyra-cli/guide.md"]
        cases.append(missing)
        for index, files in enumerate(cases):
            with self.subTest(case=index), self.assertRaises((ValueError, UnicodeError)):
                release.validate(files)

    def test_a_release_without_lyra_workflow_is_refused(self):
        workflow = "skills/lyra-workflow/"
        files = {name: data for name, data in self.files.items() if not name.startswith(workflow)}
        value = json.loads(files["manifest.json"])
        value["skills"] = [entry for entry in value["skills"] if entry["name"] != "lyra-workflow"]
        value["files"] = [entry for entry in value["files"] if not entry["path"].startswith(workflow)]
        files["manifest.json"] = (json.dumps(value) + "\n").encode()
        with self.assertRaisesRegex(ValueError, "unknown/duplicate/missing skill"):
            release.validate(files)

    def test_device_and_escaping_paths(self):
        for name in ("/absolute", "../escape", "C:/drive", "a\\b", "CON.md", "a/LPT9.md", "a/COM0", "a/..", "a//b", "a/trailing.", "a/name:stream", "references/server~1.md", "a\0b"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                release.safe_path(name)

    def test_zip_duplicate_symlink_reparse_and_expansion(self):
        for mode in ("duplicate", "symlink", "reparse", "expansion", "unsafe"):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as temp:
                path = Path(temp) / "release.zip"
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", UserWarning)
                    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                        info = zipfile.ZipInfo("file.md")
                        if mode == "symlink":
                            info.create_system = 3
                            info.external_attr = 0o120777 << 16
                        if mode == "reparse":
                            info.create_system = 0
                            info.external_attr = 0x400
                        if mode == "unsafe":
                            info.filename = "../escape"
                        archive.writestr(info, b"text")
                        if mode == "duplicate":
                            archive.writestr(info, b"other")
                        if mode == "expansion":
                            archive.writestr("large.md", b"x" * (release.LIMIT + 1))
                with self.assertRaises(ValueError):
                    release.zip_files(path)

    def test_local_header_name_and_sizes_must_match_the_central_directory(self):
        for field in ("name", "size"):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as temp:
                path = Path(temp) / "local.zip"
                with zipfile.ZipFile(path, "w") as archive:
                    archive.writestr("guide.md", b"text")
                    archive.writestr("reference.md", b"reference")
                self.assertEqual(len(release.zip_files(path)), 2)
                data = bytearray(path.read_bytes())
                if field == "name":
                    data[30] = ord("G")
                else:
                    data[22:26] = (999).to_bytes(4, "little")
                path.write_bytes(data)
                with self.assertRaisesRegex(ValueError, "local header.*guide.md"):
                    release.zip_files(path)

    def test_tag_stops_before_git_on_failed_validation(self):
        with patch("sys.argv", ["release.py", "tag"]), patch("release.source_files", return_value={}), patch("release.subprocess.run") as git, redirect_stderr(io.StringIO()):
            self.assertEqual(release.main(), 1)
            git.assert_not_called()

    def test_duplicate_json_fields(self):
        files = copy.deepcopy(self.files)
        files["manifest.json"] = files["manifest.json"].replace(b'"formatVersion": 1', b'"formatVersion": 1, "formatVersion": 1')
        with self.assertRaises(ValueError):
            release.validate(files)


if __name__ == "__main__":
    unittest.main()
