#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import os
import re
import shutil
import urllib.parse
from dataclasses import dataclass
from pathlib import Path


DOCS_ROOT = Path("docs")
ORPHAN_DIRNAME = "_orphaned-assets"
ASSET_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".svg",
}

MARKDOWN_IMAGE_RE = re.compile(r"(!\[[^\]]*\]\()([^)]+)(\))")
HTML_IMAGE_RE = re.compile(r'(<img\b[^>]*?\bsrc=)(["\'])(.*?)\2', re.IGNORECASE)


@dataclass(frozen=True)
class RefOccurrence:
    kind: str
    raw_path: str
    resolved_source: Path | None


def is_asset_file(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() in ASSET_EXTENSIONS


def slugify(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug or "doc"


def decode_path(raw_path: str) -> str:
    return urllib.parse.unquote(raw_path.strip())


def clean_markdown_destination(inner: str) -> tuple[str, str]:
    stripped = inner.strip()
    if stripped.startswith("<"):
        end = stripped.find(">")
        if end != -1:
            return stripped[1:end], stripped[end + 1 :]
    if not stripped:
        return "", ""
    match = re.match(r"(\S+)(.*)", stripped, re.DOTALL)
    if match:
        return match.group(1), match.group(2)
    return stripped, ""


def is_external(raw_path: str) -> bool:
    lowered = raw_path.lower()
    return lowered.startswith(("http://", "https://", "data:")) or raw_path.startswith("/")


def remove_leading_relative_parts(path_text: str) -> Path:
    parts = list(Path(path_text).parts)
    while parts and parts[0] in (".", ".."):
        parts.pop(0)
    return Path(*parts) if parts else Path(Path(path_text).name)


def build_basename_index(docs_root: Path) -> dict[str, list[Path]]:
    index: dict[str, list[Path]] = {}
    for path in docs_root.rglob("*"):
        if ORPHAN_DIRNAME in path.parts:
            continue
        if is_asset_file(path):
            index.setdefault(path.name, []).append(path)
    return index


def candidate_score(candidate: Path, md_path: Path) -> tuple[int, int, int, str]:
    md_parent = md_path.parent.resolve()
    try:
        rel = candidate.resolve().relative_to(md_parent)
        rel_depth = len(rel.parts)
    except ValueError:
        rel_depth = 999

    md_stem_dir = md_path.parent / md_path.stem
    in_stem_dir = 0 if md_stem_dir in candidate.parents else 1
    try:
        common = os.path.commonpath([str(candidate.resolve()), str(md_parent)])
        common_depth = -len(Path(common).parts)
    except ValueError:
        common_depth = 0
    return (in_stem_dir, rel_depth, common_depth, str(candidate))


def resolve_source(
    md_path: Path,
    raw_path: str,
    basename_index: dict[str, list[Path]],
) -> Path | None:
    if not raw_path or is_external(raw_path):
        return None

    decoded = decode_path(raw_path)
    raw_rel = Path(decoded)
    stripped_rel = remove_leading_relative_parts(decoded)

    candidates: list[Path] = []
    candidates.append((md_path.parent / raw_rel).resolve())
    candidates.append((md_path.parent / stripped_rel).resolve())
    candidates.append((md_path.parent / md_path.stem / raw_rel).resolve())
    candidates.append((md_path.parent / md_path.stem / stripped_rel).resolve())
    candidates.append((DOCS_ROOT / raw_rel).resolve())
    candidates.append((DOCS_ROOT / stripped_rel).resolve())

    name = raw_rel.name or stripped_rel.name
    if name:
        candidates.extend(path.resolve() for path in basename_index.get(name, []))

    seen: set[Path] = set()
    filtered: list[Path] = []
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        if is_asset_file(candidate):
            filtered.append(candidate)

    if not filtered:
        return None

    filtered.sort(key=lambda candidate: candidate_score(candidate, md_path))
    return filtered[0]


def extract_occurrences(
    md_path: Path,
    text: str,
    basename_index: dict[str, list[Path]],
) -> list[RefOccurrence]:
    occurrences: list[RefOccurrence] = []

    for match in MARKDOWN_IMAGE_RE.finditer(text):
        raw_path, _ = clean_markdown_destination(match.group(2))
        source = resolve_source(md_path, raw_path, basename_index)
        occurrences.append(RefOccurrence("markdown", raw_path, source))

    for match in HTML_IMAGE_RE.finditer(text):
        raw_path = match.group(3).strip()
        source = resolve_source(md_path, raw_path, basename_index)
        occurrences.append(RefOccurrence("html", raw_path, source))

    return occurrences


def assign_targets(
    md_path: Path,
    occurrences: list[RefOccurrence],
) -> tuple[dict[str, str], dict[Path, Path], list[str]]:
    asset_dir = md_path.parent / f"{md_path.stem}-assets"
    slug = slugify(md_path.stem)
    raw_to_new: dict[str, str] = {}
    source_to_target: dict[Path, Path] = {}
    unresolved: list[str] = []
    counter = 1

    for occurrence in occurrences:
        if not occurrence.raw_path or is_external(occurrence.raw_path):
            continue
        if occurrence.resolved_source is None:
            unresolved.append(occurrence.raw_path)
            continue

        if occurrence.resolved_source not in source_to_target:
            suffix = occurrence.resolved_source.suffix.lower()
            target = asset_dir / f"{slug}-{counter:02d}{suffix}"
            counter += 1
            source_to_target[occurrence.resolved_source] = target

        target = source_to_target[occurrence.resolved_source]
        raw_to_new[occurrence.raw_path] = target.relative_to(md_path.parent).as_posix()

    return raw_to_new, source_to_target, unresolved


def rewrite_markdown_images(text: str, replacements: dict[str, str]) -> str:
    def replace(match: re.Match[str]) -> str:
        original_inner = match.group(2)
        raw_path, suffix = clean_markdown_destination(original_inner)
        if raw_path in replacements:
            return f"{match.group(1)}{replacements[raw_path]}{suffix}{match.group(3)}"
        return match.group(0)

    return MARKDOWN_IMAGE_RE.sub(replace, text)


def rewrite_html_images(text: str, replacements: dict[str, str]) -> str:
    def replace(match: re.Match[str]) -> str:
        raw_path = match.group(3).strip()
        if raw_path in replacements:
            return f"{match.group(1)}{match.group(2)}{replacements[raw_path]}{match.group(2)}"
        return match.group(0)

    return HTML_IMAGE_RE.sub(replace, text)


def gather_markdown_files(docs_root: Path) -> list[Path]:
    return sorted(path for path in docs_root.rglob("*.md") if ORPHAN_DIRNAME not in path.parts)


def referenced_assets_from_docs(docs_root: Path) -> set[Path]:
    referenced: set[Path] = set()
    basename_index = build_basename_index(docs_root)

    for md_path in gather_markdown_files(docs_root):
        text = md_path.read_text(encoding="utf-8", errors="ignore")
        occurrences = extract_occurrences(md_path, text, basename_index)
        _, source_to_target, _ = assign_targets(md_path, occurrences)
        referenced.update(path.resolve() for path in source_to_target.values())

    return referenced


def move_orphans(docs_root: Path, keep_files: set[Path], dry_run: bool) -> list[tuple[Path, Path]]:
    moved: list[tuple[Path, Path]] = []
    orphan_root = (docs_root / ORPHAN_DIRNAME).resolve()

    for path in sorted(docs_root.rglob("*")):
        if not is_asset_file(path):
            continue
        resolved = path.resolve()
        if orphan_root in resolved.parents:
            continue
        if resolved in keep_files:
            continue

        target = docs_root / ORPHAN_DIRNAME / path.relative_to(docs_root)
        moved.append((path, target))
        if not dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(path), str(target))

    return moved


def remove_empty_dirs(root: Path) -> None:
    for current_root, dirnames, _ in os.walk(root, topdown=False):
        current = Path(current_root)
        if current == root:
            continue
        if any(current.iterdir()):
            continue
        current.rmdir()


def write_manifest(report_path: Path, rows: list[dict[str, str]]) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["doc", "source", "target"]
    with report_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    docs_root = DOCS_ROOT.resolve()
    basename_index = build_basename_index(docs_root)

    manifest_rows: list[dict[str, str]] = []
    unresolved_refs: list[tuple[Path, str]] = []
    kept_targets: set[Path] = set()

    for md_path in gather_markdown_files(docs_root):
        text = md_path.read_text(encoding="utf-8", errors="ignore")
        occurrences = extract_occurrences(md_path, text, basename_index)
        replacements, source_to_target, unresolved = assign_targets(md_path, occurrences)

        for raw_path in unresolved:
            unresolved_refs.append((md_path, raw_path))

        if replacements:
            updated = rewrite_markdown_images(text, replacements)
            updated = rewrite_html_images(updated, replacements)
            if not args.dry_run:
                md_path.write_text(updated, encoding="utf-8")

        for source, target in source_to_target.items():
            kept_targets.add(target.resolve())
            manifest_rows.append(
                {
                    "doc": str(md_path.relative_to(docs_root)),
                    "source": str(source.relative_to(docs_root)),
                    "target": str(target.relative_to(docs_root)),
                }
            )
            if not args.dry_run:
                target.parent.mkdir(parents=True, exist_ok=True)
                if source.resolve() != target.resolve():
                    shutil.copy2(source, target)

    if unresolved_refs:
        print("UNRESOLVED REFERENCES")
        for md_path, raw_path in unresolved_refs:
            print(f"{md_path.relative_to(docs_root)} :: {raw_path}")
        return 1

    orphan_moves = move_orphans(docs_root, kept_targets, args.dry_run)

    if not args.dry_run:
        write_manifest(docs_root / ORPHAN_DIRNAME / "reorg-manifest.csv", manifest_rows)
        remove_empty_dirs(docs_root)

    print(f"documents={len(gather_markdown_files(docs_root))}")
    print(f"copied_assets={len(manifest_rows)}")
    print(f"orphaned_assets={len(orphan_moves)}")
    if args.dry_run:
        print("dry_run=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
