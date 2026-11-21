#!/usr/bin/env python3
"""Build installable .skill archives from the canonical plugin skills."""

from __future__ import annotations

import shutil
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
OUTPUT = ROOT / "packages" / "standalone"
SHARED = SKILLS / "_shared" / "references"


def add_tree(archive: zipfile.ZipFile, source: Path, prefix: str) -> None:
    for path in sorted(source.rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts:
            name = f"{prefix}/{path.relative_to(source).as_posix()}"
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            # Stored entries are byte-for-byte reproducible across Python and zlib versions.
            # The complete package set is small enough that compression is not worth CI drift.
            info.compress_type = zipfile.ZIP_STORED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())


def main() -> int:
    skill_dirs = sorted(path for path in SKILLS.iterdir() if (path / "SKILL.md").exists())
    OUTPUT.mkdir(parents=True, exist_ok=True)

    expected = {f"jrs-{path.name}.skill" for path in skill_dirs}
    for old in OUTPUT.glob("jrs-*.skill"):
        if old.name not in expected:
            old.unlink()

    for source in skill_dirs:
        package_name = f"jrs-{source.name}"
        target = OUTPUT / f"{package_name}.skill"
        with tempfile.TemporaryDirectory(prefix="jrs-skill-") as temp:
            staged = Path(temp) / package_name
            shutil.copytree(source, staged)

            skill_path = staged / "SKILL.md"
            text = skill_path.read_text()
            if "../_shared/references/" in text:
                references = staged / "references"
                references.mkdir(exist_ok=True)
                for shared in SHARED.glob("*.md"):
                    if f"../_shared/references/{shared.name}" in text:
                        shutil.copy2(shared, references / shared.name)
                text = text.replace("../_shared/references/", "references/")
                skill_path.write_text(text)

            with zipfile.ZipFile(target, "w", zipfile.ZIP_STORED) as archive:
                add_tree(archive, staged, package_name)

    print(f"Built {len(skill_dirs)} standalone skill packages in {OUTPUT.relative_to(ROOT)}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
