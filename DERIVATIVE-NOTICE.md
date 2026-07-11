# Softness Mono Derivative Notice

## Project identity

**Softness Mono** is an independent derivative of **Ubuntu Sans Mono**.

It is maintained by the Softness as Strength project and is not affiliated with, sponsored by, or endorsed by Canonical Ltd.

## Upstream source

Original project:

- Ubuntu Sans Mono
- https://github.com/canonical/Ubuntu-Sans-Mono-fonts

Original development was commissioned and funded by Canonical Ltd. Original technical design and implementation credits include Dalton Maag, Type Network, DJR, and Dual Type, as documented by the upstream project.

## Licence

Softness Mono remains distributed under the **Ubuntu Font Licence Version 1.0**.

The original copyright, authorship, design, and licence notices must be preserved. Modified copies must use a distinct name and must not imply endorsement by Canonical Ltd.

## Rename-only baseline

The initial Softness Mono migration changes project and generated-font naming only:

- family name: `Softness Mono`
- generated filename stem: `SoftnessMono`
- designspace instance names
- build configuration
- repository documentation

This initial baseline does **not** intentionally modify glyph outlines, spacing, kerning, hinting, OpenType behavior, or language coverage.

The source UFO directories temporarily retain their upstream filenames to reduce the size and risk of the first migration. Their internal metadata and physical directory names should be audited in a later dedicated change set before the first public binary release.

## Change policy

Every future design change should record:

1. the glyphs or systems affected;
2. the reason for the change;
3. before-and-after proofs;
4. build and quality-test results;
5. any compatibility or interpolation concerns.

## Naming policy

Official derivative naming:

- Display family: `Softness Mono`
- Filename/PostScript stem: `SoftnessMono`

The words `Ubuntu` and `Canonical` may appear in attribution, historical notes, upstream links, and licence records, but not as the identity of the derivative family.
