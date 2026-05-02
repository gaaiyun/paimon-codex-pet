# QA Notes

Generated with the `hatch-pet` Codex skill.

## Result

The final package passed deterministic validation and visual contact-sheet review.

Important generated files:

- Final package: `pet/paimon/pet.json`
- Final active spritesheet: `pet/paimon/spritesheet.png`
- Secondary WebP spritesheet: `pet/paimon/spritesheet.webp`
- Contact sheet: `qa/contact-sheet.png`
- Frame QA: `qa/review.json`
- PNG atlas validation: `qa/validation-png.json`
- WebP atlas validation: `qa/validation.json`
- State preview videos: `qa/videos/*.mp4`

## Generation Notes

The base pet was generated first and recorded as the canonical identity reference. Animation row generation was delegated to subagents:

- `idle`
- `running-right`
- `running-left`
- `waving`
- `jumping`
- `failed`
- `waiting`
- `running`
- `review`

`running-left` was generated as its own grounded row instead of mirroring `running-right`, because the character design has side-specific visual elements.

One `running-left` attempt failed with a tool-layer `Bad Request` when using four input images. The successful retry used the layout guide, canonical base, and approved base pet only.

`ffmpeg` was not available on PATH, so `imageio-ffmpeg` was installed locally and its bundled ffmpeg binary was passed to the video renderer.

After initial packaging, Codex Settings could discover the pet but failed to load it when selected. The active package was changed from `spritesheet.webp` to `spritesheet.png`, because the PNG atlas validates cleanly and avoids WebP compatibility issues in desktop pet loading.
