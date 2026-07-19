#!/usr/bin/env python3
"""Validate the Paimon Codex pet package.

Checks that the loadable spritesheet matches the atlas spec recorded in
assets/manifest.json, and that the extracted single frames under
assets/frames/ match the per-state frame counts the manifest declares.

PNG validation can run with the Python standard library alone. WebP validation
uses Pillow, which is available in the Codex workspace runtime.

Usage:
    python tools/validate_atlas.py            # validate the repo package
    python tools/validate_atlas.py PATH       # validate a specific PNG or WebP

Exit code is 0 when everything passes and 1 when any check fails.
"""

import json
import struct
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "assets" / "manifest.json"
PET_MANIFEST_PATH = REPO_ROOT / "pet" / "paimon" / "pet.json"

OK = "[OK]"
FAIL = "[FAIL]"

# PNG color type 6 is truecolor with alpha, i.e. RGBA.
PNG_COLOR_TYPE_RGBA = 6


def default_spritesheet_path():
    """Resolve the loadable spritesheet declared by the pet manifest."""
    pet_manifest = json.loads(PET_MANIFEST_PATH.read_text(encoding="utf-8"))
    return PET_MANIFEST_PATH.parent / pet_manifest["spritesheetPath"]


def read_png_header(path):
    """Return (width, height, color_type) by parsing the PNG IHDR chunk."""
    with open(path, "rb") as handle:
        signature = handle.read(8)
        if signature != b"\x89PNG\r\n\x1a\n":
            raise ValueError("not a PNG file")
        handle.read(4)  # IHDR length
        chunk_type = handle.read(4)
        if chunk_type != b"IHDR":
            raise ValueError("first chunk is not IHDR")
        width, height, _bit_depth, color_type = struct.unpack(">IIBB", handle.read(10))
    return width, height, color_type


def describe_mode(path):
    """Return a human-readable color mode, preferring Pillow when available."""
    try:
        from PIL import Image
    except ImportError:
        _, _, color_type = read_png_header(path)
        return "RGBA" if color_type == PNG_COLOR_TYPE_RGBA else "type-%d" % color_type
    with Image.open(path) as image:
        return image.mode


def read_image_info(path):
    """Return (width, height, mode, format) for a supported spritesheet."""
    try:
        from PIL import Image
    except ImportError:
        if path.suffix.lower() != ".png":
            raise ValueError("Pillow is required to validate WebP spritesheets")
        width, height, color_type = read_png_header(path)
        mode = "RGBA" if color_type == PNG_COLOR_TYPE_RGBA else "type-%d" % color_type
        return width, height, mode, "PNG"

    with Image.open(path) as image:
        return image.width, image.height, image.mode, image.format


def validate(spritesheet_path):
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    atlas = manifest["loadable_pet"]["atlas"]
    expected_width = atlas["width"]
    expected_height = atlas["height"]

    errors = []
    checks = []

    # 1. Spritesheet exists and is a readable transparent PNG or WebP.
    if not spritesheet_path.is_file():
        print("%s spritesheet not found: %s" % (FAIL, spritesheet_path))
        return False

    try:
        width, height, mode, image_format = read_image_info(spritesheet_path)
    except ValueError as exc:
        print("%s cannot read spritesheet (%s): %s" % (FAIL, exc, spritesheet_path))
        return False

    if (width, height) == (expected_width, expected_height):
        checks.append("dimensions %dx%d" % (width, height))
    else:
        errors.append(
            "dimensions %dx%d, expected %dx%d"
            % (width, height, expected_width, expected_height)
        )

    if image_format in {"PNG", "WEBP"}:
        checks.append("%s format" % image_format)
    else:
        errors.append("format %s, expected PNG or WEBP" % image_format)

    if mode == "RGBA":
        checks.append("RGBA color")
    else:
        errors.append("mode %s, expected RGBA" % mode)

    # 2. Atlas cell geometry is internally consistent.
    if atlas["columns"] * atlas["cell_width"] == expected_width:
        checks.append("%d columns x %dpx" % (atlas["columns"], atlas["cell_width"]))
    else:
        errors.append(
            "columns(%d) x cell_width(%d) != width(%d)"
            % (atlas["columns"], atlas["cell_width"], expected_width)
        )

    if atlas["rows"] * atlas["cell_height"] == expected_height:
        checks.append("%d rows x %dpx" % (atlas["rows"], atlas["cell_height"]))
    else:
        errors.append(
            "rows(%d) x cell_height(%d) != height(%d)"
            % (atlas["rows"], atlas["cell_height"], expected_height)
        )

    # 3. Extracted single frames match the declared per-state counts.
    total_frames = 0
    for state in manifest["states"]:
        name = state["name"]
        declared = state["frame_count"]
        listed = len(state["frames"])
        if listed != declared:
            errors.append("state '%s' lists %d frames but frame_count is %d" % (name, listed, declared))
        missing = [rel for rel in state["frames"] if not (REPO_ROOT / rel).is_file()]
        if missing:
            errors.append("state '%s' missing %d frame file(s): %s" % (name, len(missing), missing[0]))
        else:
            total_frames += listed
    if not errors:
        checks.append("%d extracted frames across %d states" % (total_frames, len(manifest["states"])))

    # 4. Expression frames referenced by the manifest exist.
    missing_expr = [e["path"] for e in manifest["expressions"] if not (REPO_ROOT / e["path"]).is_file()]
    if missing_expr:
        errors.append("missing expression frame(s): %s" % missing_expr[0])
    else:
        checks.append("%d expression frames" % len(manifest["expressions"]))

    for line in checks:
        print("%s %s" % (OK, line))
    for line in errors:
        print("%s %s" % (FAIL, line))

    return not errors


def main():
    if len(sys.argv) > 1:
        spritesheet_path = Path(sys.argv[1]).expanduser().resolve()
    else:
        spritesheet_path = default_spritesheet_path()

    print("Validating: %s" % spritesheet_path)
    passed = validate(spritesheet_path)
    print("\nResult: %s" % ("ok" if passed else "FAILED"))
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
