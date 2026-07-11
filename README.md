# Softness Mono

**Softness Mono** is an experimental derivative of Ubuntu Sans Mono. The project begins with a rename-only baseline so the build, metadata, and quality checks can be stabilized before any glyph outlines are changed.

> Current status: naming and build migration in progress. No intentional glyph-shape changes have been made yet.

## Lineage and attribution

Softness Mono is based on **Ubuntu Sans Mono**, originally commissioned and funded by Canonical Ltd. The original technical font design and implementation credits include Dalton Maag, Type Network, DJR, and Dual Type.

This derivative is independent, is not affiliated with Canonical Ltd., and is not endorsed by Canonical Ltd.

The original upstream project is available at:

- https://github.com/canonical/Ubuntu-Sans-Mono-fonts

The upstream repository remains configured as the source of the original design history. See `DERIVATIVE-NOTICE.md` for the derivative naming and attribution policy.

## Design direction

Softness Mono will explore how a monospaced typeface can feel warmer, gentler, and more human without losing clarity, rhythm, or technical usefulness.

The first milestone is deliberately conservative:

- rename the family to Softness Mono
- generate distinct font and PostScript names
- preserve all original credits and licence terms
- keep glyph outlines unchanged
- establish a passing build and QA baseline

Only after that baseline passes will letterform experiments begin.

## Building

Fonts are built through the existing project toolchain.

```bash
make build
```

Development variable-font build:

```bash
make dev
```

Run quality checks:

```bash
make test
```

Generate proofs:

```bash
make proof
```

Expected variable font filenames include:

- `SoftnessMono[wght].ttf`
- `SoftnessMono-Italic[wght].ttf`

## Repository structure

- `sources/` — designspaces and UFO source data
- `scripts/` — build and post-processing utilities
- `documentation/` — specimens and project documentation
- `fonts/` — generated font binaries
- `out/` — generated tests and proofs

The source UFO directory names still retain their upstream filenames during the initial migration. This keeps the first change set focused on naming metadata and generated outputs rather than moving thousands of source files at once.

## Changelog

See `FONTLOG.txt` for upstream history. Softness Mono-specific changes should also be recorded in `DERIVATIVE-NOTICE.md` until a dedicated derivative changelog is established.

## Licence

This Font Software is distributed under the **Ubuntu Font Licence Version 1.0**.

The licence and original copyright notices must remain with redistributed or modified copies. Softness Mono is a derivative name and must not be presented as an official Ubuntu or Canonical font.

Licence information:

- https://ubuntu.com/legal/font-licence
