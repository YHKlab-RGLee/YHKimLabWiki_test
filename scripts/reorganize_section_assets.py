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
ASSET_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}

MARKDOWN_IMAGE_RE = re.compile(r"(!\[[^\]]*\]\()([^)]+)(\))")
HTML_IMAGE_RE = re.compile(r'(<img\b[^>]*?\bsrc=)(["\'])(.*?)\2', re.IGNORECASE)


@dataclass(frozen=True)
class RefOccurrence:
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


def gather_markdown_files(docs_root: Path) -> list[Path]:
    return sorted(path for path in docs_root.rglob("*.md") if ORPHAN_DIRNAME not in path.parts)


def build_asset_index(docs_root: Path) -> dict[str, list[Path]]:
    index: dict[str, list[Path]] = {}
    for path in docs_root.rglob("*"):
        if ORPHAN_DIRNAME in path.parts:
            continue
        if is_asset_file(path):
            index.setdefault(path.name, []).append(path.resolve())
    return index


def candidate_score(candidate: Path, md_path: Path) -> tuple[int, int, int, str]:
    md_parent = md_path.parent.resolve()
    try:
        rel = candidate.relative_to(md_parent)
        rel_depth = len(rel.parts)
    except ValueError:
        rel_depth = 999

    in_doc_asset = 0 if f"{md_path.stem}-assets" in candidate.parts else 1
    in_section_img = 0 if "img" in candidate.parts else 1
    return (in_doc_asset, in_section_img, rel_depth, str(candidate))


def resolve_source(md_path: Path, raw_path: str, asset_index: dict[str, list[Path]]) -> Path | None:
    if not raw_path or is_external(raw_path):
        return None

    decoded = decode_path(raw_path)
    rel = Path(decoded)
    candidates = [
        (md_path.parent / rel).resolve(),
        (DOCS_ROOT / rel).resolve(),
    ]
    if rel.name:
        candidates.extend(asset_index.get(rel.name, []))

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


def extract_occurrences(md_path: Path, text: str, asset_index: dict[str, list[Path]]) -> list[RefOccurrence]:
    occurrences: list[RefOccurrence] = []

    for match in MARKDOWN_IMAGE_RE.finditer(text):
        raw_path, _ = clean_markdown_destination(match.group(2))
        occurrences.append(RefOccurrence(raw_path, resolve_source(md_path, raw_path, asset_index)))

    for match in HTML_IMAGE_RE.finditer(text):
        raw_path = match.group(3).strip()
        occurrences.append(RefOccurrence(raw_path, resolve_source(md_path, raw_path, asset_index)))

    return occurrences


def section_img_dir(md_path: Path, docs_root: Path) -> Path:
    rel = md_path.relative_to(docs_root)
    if len(rel.parts) == 1:
        return docs_root / "img"
    return docs_root / rel.parts[0] / "img"


def site_absolute_ref(target: Path, docs_root: Path) -> str:
    return "/" + target.relative_to(docs_root).as_posix()


def assign_targets(md_path: Path, docs_root: Path, occurrences: list[RefOccurrence]) -> tuple[dict[str, str], dict[Path, Path], list[str]]:
    img_dir = section_img_dir(md_path, docs_root)
    prefix = slugify(md_path.stem)
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
            target = img_dir / f"{prefix}-{counter:02d}{suffix}"
            while target.exists() and target.resolve() != occurrence.resolved_source.resolve():
                counter += 1
                target = img_dir / f"{prefix}-{counter:02d}{suffix}"
            source_to_target[occurrence.resolved_source] = target
            counter += 1

        target = source_to_target[occurrence.resolved_source]
        raw_to_new[occurrence.raw_path] = site_absolute_ref(target, docs_root)

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


def remove_empty_dirs(root: Path) -> None:
    for current_root, _, _ in os.walk(root, topdown=False):
        current = Path(current_root)
        if current == root:
            continue
        if any(current.iterdir()):
            continue
        current.rmdir()


def move_doc_asset_dirs(docs_root: Path, dry_run: bool) -> list[tuple[Path, Path]]:
    moved: list[tuple[Path, Path]] = []
    for path in sorted(docs_root.rglob("*-assets")):
        if not path.is_dir():
            continue
        if ORPHAN_DIRNAME in path.parts:
            continue
        target = docs_root / ORPHAN_DIRNAME / "_doc-assets" / path.relative_to(docs_root)
        moved.append((path, target))
        if not dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists():
                shutil.rmtree(target)
            shutil.move(str(path), str(target))
    return moved


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
    asset_index = build_asset_index(docs_root)
    manifest_rows: list[dict[str, str]] = []
    unresolved_refs: list[tuple[Path, str]] = []

    for md_path in gather_markdown_files(docs_root):
        text = md_path.read_text(encoding="utf-8", errors="ignore")
        occurrences = extract_occurrences(md_path, text, asset_index)
        replacements, source_to_target, unresolved = assign_targets(md_path, docs_root, occurrences)

        for raw_path in unresolved:
            unresolved_refs.append((md_path, raw_path))

        if replacements:
            updated = rewrite_markdown_images(text, replacements)
            updated = rewrite_html_images(updated, replacements)
            if not args.dry_run:
                md_path.write_text(updated, encoding="utf-8")

        for source, target in source_to_target.items():
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

    moved_doc_assets = move_doc_asset_dirs(docs_root, args.dry_run)

    if not args.dry_run:
        write_manifest(docs_root / ORPHAN_DIRNAME / "section-reorg-manifest.csv", manifest_rows)
        remove_empty_dirs(docs_root)

    print(f"documents={len(gather_markdown_files(docs_root))}")
    print(f"copied_assets={len(manifest_rows)}")
    print(f"moved_doc_asset_dirs={len(moved_doc_assets)}")
    if args.dry_run:
        print("dry_run=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
