#!/usr/bin/env python3
"""Validate a whole release and build a reproducible, offline ZIP."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import stat
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
LIMIT = 1024 * 1024
NAMES = {"lyra-cli", "lyra-orchestration", "lyra-workflow"}
SEMVER = re.compile(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?\Z")


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def version(text, stable=False):
    match = SEMVER.fullmatch(text)
    require(match is not None, f"invalid SemVer: {text}")
    require(all(int(match[i]) <= 2**64 - 1 for i in (1, 2, 3)), "SemVer component exceeds u64")
    if match[4]:
        require(not any(p.isdigit() and len(p) > 1 and p[0] == "0" for p in match[4].split(".")), "numeric prerelease has leading zero")
    require(not stable or (not match[4] and "+" not in text), "bundle version must be stable")


def safe_path(name):
    require(isinstance(name, str) and 0 < len(name) <= 240, "invalid path length")
    require(name.isascii(), f"non-ASCII path: {name}")
    for part in name.split("/"):
        require(part not in ("", ".", "..") and not part.endswith((".", " ")), f"unsafe path: {name}")
        require(not any(ord(c) < 32 or c in '\\:<>\"|?*' for c in part), f"unsafe path: {name}")
        stem = part.split(".")[0].upper()
        require(not re.fullmatch(r".+~[0-9]+", stem), f"Windows short-name alias path: {name}")
        require(stem not in {"CON", "PRN", "AUX", "NUL", "CLOCK$", "CONIN$", "CONOUT$"} and not re.fullmatch(r"(?:COM|LPT)[0-9]", stem), f"Windows device path: {name}")
    return name


def unique_object(pairs):
    obj = {}
    for key, value in pairs:
        require(key not in obj, f"duplicate JSON field: {key}")
        obj[key] = value
    return obj


def sha(data):
    return hashlib.sha256(data).hexdigest()


def validate(files):
    require(len(files) <= 64 and sum(map(len, files.values())) <= 4 * LIMIT, "release expansion over limit")
    folded = set()
    for name, data in files.items():
        safe_path(name)
        require(name.lower() not in folded, f"case-colliding path: {name}")
        folded.add(name.lower())
        require(len(data) <= LIMIT, f"file over limit: {name}")
        text = data.decode("utf-8")
        require("\r" not in text and "\0" not in text, f"text must be UTF-8/LF: {name}")
    require("manifest.json" in files and "VERSION" in files, "missing release metadata")
    manifest = json.loads(files["manifest.json"], object_pairs_hook=unique_object)
    require(set(manifest) == {"formatVersion", "skillsVersion", "tag", "skills", "files"}, "unknown/missing manifest field")
    require(type(manifest["formatVersion"]) is int and manifest["formatVersion"] == 1, "unsupported formatVersion")
    release = manifest["skillsVersion"]
    version(release, stable=True)
    require(files["VERSION"] == (release + "\n").encode() and manifest["tag"] == "v" + release, "VERSION/tag mismatch")
    entries = manifest["skills"]
    require(len(entries) == len(NAMES) and {e["name"] for e in entries} == NAMES, "unknown/duplicate/missing skill")
    expected = {"VERSION"}
    for entry in entries:
        require(set(entry) == {"name", "description", "minimumLyraVersion", "pointer", "guide", "references"}, "unknown/missing skill field")
        name = entry["name"]
        version(entry["minimumLyraVersion"])
        require(isinstance(entry["description"], str) and entry["description"].strip(), "empty description")
        prefix = f"skills/{name}/"
        require(entry["pointer"] == prefix + "SKILL.md" and entry["guide"] == prefix + "guide.md", "pointer/guide path mismatch")
        refs = entry["references"]
        require(isinstance(refs, list) and len(refs) == len(set(refs)), "duplicate references")
        require(all(r.startswith(prefix + "references/") and r.endswith(".md") and r.count("/") == 3 for r in refs), "invalid reference path")
        paths = [entry["pointer"], entry["guide"], *refs]
        for name in paths:
            safe_path(name)
        expected.update(paths)
        require(all(p in files for p in paths), "missing skill file")
        pointer = files[entry["pointer"]].decode()
        require(pointer.startswith("---\n") and "\n---\n" in pointer[4:], "pointer front matter is incomplete")
        front = pointer[4:].split("\n---\n", 1)[0]
        require([line for line in front.splitlines() if line.startswith("name:")] == [f"name: {entry['name']}"], "pointer name differs from manifest")
        require(len(files[entry["pointer"]]) <= 4096 and len(files[entry["guide"]]) <= 15 * 1024, "pointer/guide budget")
        require(all(p.endswith("/commands.md") or len(files[p]) <= 8 * 1024 for p in refs), "reference budget")
        require(all(not files[p].startswith(b"---") for p in [entry["guide"], *refs]), "only pointer has front matter")
        if release != "0.1.11":
            require([line for line in front.splitlines() if line.startswith("skillsVersion:")] == [f"skillsVersion: {release}"] and [line for line in front.splitlines() if line.startswith("minimumLyraVersion:")] == [f"minimumLyraVersion: {entry['minimumLyraVersion']}"] , "pointer version metadata mismatch")
    table = manifest["files"]
    paths = [e["path"] for e in table]
    require(paths == sorted(expected), "file table missing, extra, duplicated or unsorted")
    require(set(files) == expected | {"manifest.json"}, "missing or extra release member")
    for entry in table:
        require(set(entry) == {"path", "size", "sha256"}, "unknown/missing file field")
        data = files[entry["path"]]
        require(type(entry["size"]) is int and entry["size"] == len(data), f"size mismatch: {entry['path']}")
        require(entry["sha256"] == sha(data), f"SHA-256 mismatch: {entry['path']}")
    return manifest


def source_files():
    files = {}
    for path in [ROOT / "VERSION", ROOT / "manifest.json", *(ROOT / "skills").rglob("*")]:
        require(not path.is_symlink(), f"symlink: {path}")
        if path.is_dir():
            continue
        require(path.is_file() and path.stat().st_size <= LIMIT, f"invalid/oversized source: {path}")
        files[path.relative_to(ROOT).as_posix()] = path.read_bytes()
    return files


def zip_files(path):
    require(path.stat().st_size <= LIMIT, "zip over 1 MiB")
    files = {}
    total = 0
    with path.open("rb") as stream:
        zip_bytes = stream.read(LIMIT + 1)
    require(len(zip_bytes) <= LIMIT, "zip over 1 MiB")
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as archive:
        require(len(archive.infolist()) <= 64, "zip has more than 64 files")
        for info in archive.infolist():
            safe_path(info.filename)
            header = zip_bytes[info.header_offset:info.header_offset + 30]
            require(len(header) == 30 and header[:4] == b"PK\x03\x04", f"invalid local header: {info.filename}")
            word = lambda at: int.from_bytes(header[at:at+2], "little")
            dword = lambda at: int.from_bytes(header[at:at+4], "little")
            raw_name = zip_bytes[info.header_offset+30:info.header_offset+30+word(26)]
            require(raw_name == info.filename.encode("ascii"), f"local header name differs from central name: {info.filename}")
            for field, found, needed in (("size", dword(22), info.file_size), ("compressed size", dword(18), info.compress_size), ("CRC32", dword(14), info.CRC), ("flags", word(6), info.flag_bits), ("compression", word(8), info.compress_type)):
                require(found == needed, f"local header {field} for {info.filename} is {found}; central value {needed} is required")
            mode = info.external_attr >> 16
            require(not info.is_dir() and stat.S_IFMT(mode) in (0, stat.S_IFREG) and not (info.external_attr & 0x410), "link/reparse/directory entry")
            require(not info.flag_bits & 1, "encrypted entry")
            require(info.filename not in files, "duplicate zip member")
            total += info.file_size
            require(info.file_size <= LIMIT and total <= 4 * LIMIT, "zip expansion over limit")
            with archive.open(info) as stream:
                data = stream.read(LIMIT + 1)
            require(len(data) == info.file_size, "zip entry size mismatch")
            files[info.filename] = data
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("validate", "package", "tag"))
    parser.add_argument("archive", nargs="?", type=Path)
    args = parser.parse_args()
    try:
        files = zip_files(args.archive) if args.archive else source_files()
        manifest = validate(files)
        if args.command == "tag":
            require(args.archive is None, "tag accepts source files only")
            artifact = ROOT / "dist" / f"lyra-skills-{manifest['skillsVersion']}.zip"
            packaged = zip_files(artifact)
            validate(packaged)
            require(packaged == files, "packaged bytes differ from source")
            state = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, check=True, capture_output=True, text=True)
            require(not state.stdout, "commit the validated source before tagging")
            subprocess.run(["git", "tag", "--no-sign", manifest["tag"]], cwd=ROOT, check=True)
        if args.command == "package":
            require(args.archive is None, "package accepts source files only")
            output = ROOT / "dist" / f"lyra-skills-{manifest['skillsVersion']}.zip"
            output.parent.mkdir(exist_ok=True)
            with output.open("xb") as stream, zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
                for name, data in sorted(files.items()):
                    info = zipfile.ZipInfo(name, (2026, 1, 1, 0, 0, 0))
                    info.create_system = 3
                    info.external_attr = (stat.S_IFREG | 0o644) << 16
                    info.compress_type = zipfile.ZIP_DEFLATED
                    archive.writestr(info, data, compresslevel=9)
            validate(zip_files(output))
            print(f"{output}: sha256={sha(output.read_bytes())}")
        print(f"validated {manifest['tag']}: {len(files)} files")
    except (OSError, ValueError, KeyError, TypeError, UnicodeError, zipfile.BadZipFile, RuntimeError, AttributeError, IndexError, subprocess.CalledProcessError) as error:
        print(f"Could not {args.command} Lyra skills: {error}. Correct the named release files and run the command again.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
