# QA Notes

The package passed atlas validation and a visual contact-sheet check before release.

## Validated files

- Loadable manifest: `pet/paimon/pet.json`
- Loadable spritesheet: `pet/paimon/spritesheet.png`
- Archived WebP spritesheet: `pet/paimon/spritesheet.webp`
- Contact sheet: `qa/contact-sheet.png`
- Per-frame report: `qa/review.json`
- PNG atlas validation: `qa/validation-png.json`
- WebP atlas validation: `qa/validation.json`
- State preview videos: `qa/videos/*.mp4`

The `qa/*.json` reports were produced on the original build machine, so the
absolute paths inside them point at that machine. They are kept as a record of
the original validation run. To re-validate the package on any machine, use the
bundled checker instead:

```powershell
python tools\validate_atlas.py
```

It confirms the spritesheet is a 1536x1872 RGBA PNG laid out as an 8x9 atlas of
192x208 cells, and that every extracted frame and expression listed in
`assets/manifest.json` is present. Expected output ends with `Result: ok`.

## Design choices worth keeping

- `running-left` is its own row, not a horizontal mirror of `running-right`,
  because the character has side-specific details that look wrong when flipped.
- The active spritesheet is PNG rather than WebP. Some Codex desktop builds can
  discover a WebP pet in Settings but fail to load it when selected; the PNG
  atlas loads reliably. The WebP file is retained only as an archive copy.
