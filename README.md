# Paimon Codex Pet

A custom Codex desktop pet inspired by Paimon, simplified into the Codex digital pet sprite style.

This repository contains the packaged pet files, generation prompts, and QA artifacts used to validate the final animated spritesheet.

## Install

Copy the packaged pet folder into your Codex pets directory:

```powershell
Copy-Item -Recurse -Force .\pet\paimon "$env:USERPROFILE\.codex\pets\paimon"
```

Then restart Codex, or use the command menu action `Force Reload Skills` / reload assets if available in your build.

The installed package should contain:

```text
%USERPROFILE%\.codex\pets\paimon\
  pet.json
  spritesheet.png
```

## Files

- `pet/paimon/pet.json` - Codex pet manifest.
- `pet/paimon/spritesheet.png` - Final 1536x1872 RGBA spritesheet used by `pet.json`.
- `pet/paimon/spritesheet.webp` - WebP export kept as a secondary artifact.
- `qa/contact-sheet.png` - Visual contact sheet for all animation rows.
- `qa/review.json` - Frame extraction and component QA.
- `qa/validation.json` - Atlas validation result.
- `qa/videos/*.mp4` - Per-state preview loops.
- `source/prompts/` - Base and row prompts used for generation.
- `source/imagegen-jobs.json` - Image generation provenance manifest.

## Animation Rows

The spritesheet follows the Codex 8x9 atlas layout with 192x208 cells:

| Row | State | Frames |
| --- | --- | ---: |
| 0 | idle | 6 |
| 1 | running-right | 8 |
| 2 | running-left | 8 |
| 3 | waving | 4 |
| 4 | jumping | 5 |
| 5 | failed | 8 |
| 6 | waiting | 6 |
| 7 | running | 6 |
| 8 | review | 6 |

## QA Summary

Final validation passed:

- `qa/review.json`: `ok: true`, no errors, no warnings.
- `qa/validation-png.json`: `ok: true`, 1536x1872 RGBA PNG, no errors, no warnings.
- `qa/validation.json`: `ok: true`, 1536x1872 RGBA WebP, no errors, no warnings.
- Preview videos were rendered for all nine states.
- `pet.json` and `spritesheet.png` were packaged together under `pet/paimon`.

The pet package uses PNG for the active spritesheet because some Codex desktop builds list WebP-backed custom pets in Settings but fail to load them at selection time. The WebP version remains in the repository only for comparison/archive.

## Notes

This is a fan-made Codex pet inspired by Paimon. It is not official, endorsed, sponsored, or affiliated with HoYoverse, miHoYo, Genshin Impact, or OpenAI.

No license is granted for the underlying character identity or any third-party trademarks. Use this repository as a personal custom pet package unless you have the rights needed for broader distribution.
