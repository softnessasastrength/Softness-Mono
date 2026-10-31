# Softness Mono — Build Pass & Draft Render

**Date:** 2026-10-31 · **Nature:** Scratch build pass. The GitHub repository
`softnessasastrength/Softness-Mono` was **not** modified, branched, or pushed.
All work happened in a local clone at `~/workspace/softness-mono-pass/scratch/`.
Everything produced is a **DRAFT**, not a release build.
**Source HEAD:** `481fc0b8f9743e944dfb2a5f5476913c8a7e038e` (matches the Phase 1 audit tip).
**Predecessor:** `~/workspace/softness-mono_muse/SOFTNESS_MONO_PHASE1_AUDIT_muse.md`.

---

## 1. Headline result

**A font that identifies itself as Softness Mono now exists** — the full build,
not a subset: 2 variable fonts, 11 static TTFs, 11 static OTFs, a 400:700 variable
subset, and the full webfont trees — **233 files**, exactly the file count of the
inherited upstream `fonts/` tree, every one Softness-named. The project's own
verifier passes for the first time on record (see §5). A draft specimen typeset
in the produced font is at:

- [SoftnessMono_DRAFT_RENDER_muse.pdf](sandbox://workspace/softness-mono-pass/render/SoftnessMono_DRAFT_RENDER_muse.pdf)
- [SoftnessMono_DRAFT_RENDER_muse-1.png](sandbox://workspace/softness-mono-pass/render/SoftnessMono_DRAFT_RENDER_muse-1.png) · [page 2](sandbox://workspace/softness-mono-pass/render/SoftnessMono_DRAFT_RENDER_muse-2.png)
- Built fonts: `~/workspace/softness-mono-pass/outputs/` (25 core binaries: 2 variable + subset + 11 TTF + 11 OTF; the remaining webfont files live in `scratch/fonts/`)

## 2. Toolchain (recorded, as installed 2026-10-31)

Python 3.12.3 venv inside the scratch clone, installed from the repo's own
`requirements.txt` → `requirements.in` (lower bounds only, as the audit noted):

| Tool | Version |
|---|---|
| fontmake | 3.12.2 |
| fontTools | 4.68.0 |
| gftools | 0.9.996 |
| ufo2ft | 3.10.0 |
| diffenator2 | 0.5.0 |
| drawbot-skia | 0.5.1 |
| bumpfontversion | 0.4.1 |
| fontspector | **1.9.0** (official release binary, fonttools/fontspector, run 2026-10-31) |
| reportlab (specimen only) | 5.1.0 |

## 3. The build AS COMMITTED — verdict: FAILS, as the audit predicted, in four moves

Reproduction of Phase 1's static findings, dynamically confirmed
(log: `build_as_committed.log`; `check-names` re-run first: exit 1, the same 14 files):

1. `make build` runs `prepare` (write mode) first. It reports
   *"Normalized Softness Mono naming in 14 files"* — and the 14 files include:
   - **`sources/config.yaml`** — its `sources:` list now points at
     `SoftnessMono.designspace`, a file that does not exist;
   - **both designspaces** — their `<source filename>` references now point at
     `SoftnessMono-*.ufo` directories, which do not exist;
   - **`scripts/prepareSoftnessMono.py` itself** — its own `REPLACEMENTS` table is
     rewritten to `("Softness Mono", "Softness Mono")` / `("SoftnessMono", "SoftnessMono")`:
     the tool silently disables itself;
   - **`scripts/verifySoftnessMono.py`** — its `FORBIDDEN_FAMILY` constant is rewritten
     from `"Ubuntu Sans Mono"` to `"Softness Mono"`: the verifier now forbids the
     *correct* name;
   - the five UFO `fontinfo.plist` files — familyName correctly becomes
     "Softness Mono" (the one genuine fix in the set);
   - README.md, `documentation/image1.py`, `scripts/fixTTHinting.py` — attribution/code
     strings rewritten.
2. `gftools builder` then dies immediately:
   `OSError: Error reading file 'SoftnessMono.designspace': No such file or directory`.
3. The recipe continues regardless (it is one `;`-chained line): `fixTTHinting.py`
   fails (`fonts/ttf` was deleted by `rm -rf fonts/` and never rebuilt), and the
   instancer fails (`fonts/variable/SoftnessMono[wght].ttf` does not exist).
4. `make build` exit code: **2**. No Softness font is produced. Note also that the
   recipe deletes the committed `fonts/` tree *before* building, so a failed
   as-committed build destroys the inherited binaries in the working tree
   (scratch only here; the committed tree is unaffected upstream).

All prepare changes were then reverted in scratch (`git checkout -- .`) and the
repair fork below was taken.

## 4. Repairs — minimal, itemised, scratch copy only

Full diff preserved at `repairs_diff_muse.txt` (10 files, 11 insertions, 11 deletions).
Each repair is the smallest change that completes the migration step the repo's
own tooling was trying to perform:

| # | Repair | Why |
|---|---|---|
| R1 | Undo prepare entirely (restore HEAD); **bypass `prepare`** and run the `build.stamp` recipe body directly | Prepare as committed is destructive (§3). Not a repair of the script — the script needs redesign (see §8); bypass is the honest minimum for a baseline build. |
| R2 | In the 5 UFO `fontinfo.plist` files: `familyName` `Ubuntu Sans Mono` → `Softness Mono` (1 line each) | The one genuine change prepare exists to make; configs/designspaces already carried the new name (commits 1–4). Copyright/trademark strings untouched. |
| R3 | `scripts/fixTTHinting.py`: reference-font paths `fonts/ttf/UbuntuSansMono-{Regular,Italic}.ttf` → `SoftnessMono-…` (2 lines) | A renamed build produces Softness-named statics; ttfautohint would have been pointed at nonexistent reference fonts. Found by reading, not by failure. |
| R4 | Rename the two designspace files to `SoftnessMono.designspace` / `SoftnessMono-Italic.designspace` (content unchanged) and point both configs' `sources:` lists at them (the exact edit prepare tried to make to the configs, completed properly) | Discovered by failure: with HEAD filenames, gftools built variable fonts named `UbuntuSansMono[wght].ttf` — output names derive from the designspace file stem — and then died with `ValueError: Filename UbuntuSansMono-Italic[wght].ttf not found in stat dictionary`, because `config.yaml`'s `stat:` keys expect the Softness names. Log: `build_repaired_step1_gftools.log` (failed at ninja step 49/71). UFO directory names were **not** renamed; the designspaces' `<source filename>` references still point at them, exactly as at HEAD. |

With R1–R4 the recipe completes end to end: `gftools builder` exit 0
(`build_repaired_step2_gftools.log`), `fixTTHinting.py` exit 0,
`makeWebfonts.py` exit 0, instancer subset exit 0 → **233 output files**.

## 5. Name-table evidence & the project's verifier

`scripts/verifySoftnessMono.py` (HEAD version, run against the real outputs):

```
Verified Softness Mono naming in 13 generated fonts.   (exit 0)
```

Name records read directly with fontTools (4.68.0):

| Font | ID 1 | ID 4 | ID 6 | ID 25 | ID 5 |
|---|---|---|---|---|---|
| `SoftnessMono[wght].ttf` | Softness Mono | Softness Mono Regular | SoftnessMono-Regular | SoftnessMono | Version 1.100 |
| `SoftnessMono-Italic[wght].ttf` | Softness Mono | Softness Mono Italic | SoftnessMono-Italic | SoftnessMonoItalic | Version 1.100 |
| `SoftnessMono-Regular.ttf` (static) | Softness Mono | Softness Mono Regular | SoftnessMono-Regular | — | Version 1.100; ttfautohint (v1.8.4.16-eb64) |

`fvar`: roman wght 100–700 default 400; italic wght 400–700 default 400 — the
upstream ranges, unchanged, as the sources specify.

## 6. Fontspector — run for real, result preserved, NOT swallowed

Fontspector 1.9.0 (official Linux release binary; no cargo/PyPI route exists in
this environment) run exactly as the Makefile's `test` target runs it
(`--profile googlefonts -l warn`, both variable fonts), *without* the Makefile's
`|| echo ::warning` escape hatch. Reports preserved:
`fontspector-report.md` / `fontspector-report.html` in this folder and in
`scratch/out/fontspector/`; console log `fontspector_run.log`.

- **True exit code: 1** (`make test` would have reported success-with-warning).
- **ERROR ×2** — `fontdata_namecheck` network failures (namecheck.fontdata.com
  unreachable from this sandbox). Environmental, not font defects.
- **FAILs** (12 FAIL lines across the two fonts + family-level variable checks).
  Character of the failures, stated plainly: they are overwhelmingly
  *inherited-upstream* properties or *Google Fonts policy* items, not build defects:
  - `googlefonts/name/license_url` FAIL [`ufl`] ×2 — GF accepts the Ubuntu Font
    Licence only for legacy families; new families must use Apache/OFL. This is a
    **distribution-policy** finding: per the Phase 1 audit §6, UFL 1.0 forbids
    relicensing, so this FAIL cannot be "fixed" by changing the licence — it
    bounds where the font can be distributed, not whether it is built correctly.
  - `case_mapping` FAILs (missing case counterparts for e.g. U+0181, U+0190,
    U+0245…), `dotted_circle` FAIL, `glyphsets/shape_languages` FAIL ×2 —
    character-set/coverage properties of the inherited Ubuntu Sans Mono design,
    identical in an upstream build.
  - `varfont/consistent_axes` + `family_axis_ranges` FAIL — the roman (100–700)
    vs italic (400–700) axis-range mismatch; the upstream italic design range,
    already documented in the audit.
  - `family/equal_codepoint_coverage` FAIL — italic carries 1,720 glyphs vs
    roman 1,718 (upstream contents, verified in the audit).
  - `googlefonts/font_copyright` FAIL — copyright notice format (GF style).
- **WARNs** (25 WARN lines) — including `interpolation_issues`, `opentype/monospace`
  [bad-numberOfHMetrics], `unreachable_glyphs`, `name/trailing_spaces`,
  `alt_caron`, `soft_hyphen`, `ligature_carets`. The full itemised list is in the
  preserved report; none was introduced by the rename (the glyph data is
  byte-identical to upstream's own build — §7).

**Reading of the QA result:** the build is sound; the font is not Google-Fonts-
submission-clean, and never could be without design/coverage work and a
distribution decision. That is a Phase 3+ question, not a baseline defect.

## 7. Glyph comparison vs the inherited binaries — the rename is name-deep only

Built-font comparison (fontTools) of the new variable fonts against the
inherited upstream binaries extracted from git HEAD
(`fonts/variable/UbuntuSansMono[wght].ttf` etc.), closing the one gap the
Phase 1 audit left open (its §5 verified sources; this verifies binaries):

- **Glyph counts:** roman 1,718 = 1,718; italic 1,720 = 1,720. unitsPerEm 1000 = 1000.
- **Outlines:** every glyph's drawn outline (RecordingPen digest) identical —
  1,718/1,718 roman, 1,720/1,720 italic, 1,718/1,718 static Regular.
  Glyph order identical. `hmtx` advances identical for all glyphs.
- **Table-level hashes** (roman variable pair): `glyf`, `gvar`, `hmtx`, `loca`,
  `cmap`, `GPOS`, `GDEF`, `fvar`, `STAT`, `avar`, `HVAR`, `MVAR`, `OS/2`, `gasp`,
  `maxp`, `post`, `prep` — **byte-identical**. Only two tables differ:
  `name` (the rename itself — the point of the exercise) and `GSUB`
  (serialisation-level only: same 14 features, same scripts DFLT/cyrl/latn,
  same 54 lookups — a build-tool-version artefact, no behavioural difference).

**Conclusion:** at binary level as at source level, Softness Mono as built is
Ubuntu Sans Mono's glyphs under Softness Mono's name — nothing drawn, spaced,
or kerned has changed. (Comparison data: `glyph_comparison.json`.)

## 8. The draft render

`render/SoftnessMono_DRAFT_RENDER_muse.pdf` (+ PNGs of both pages), set entirely
in the produced static instances (ReportLab): title "Softness Mono — Draft
Render", full alphabet/figures/punctuation, the four phrases
("Softness is a strength." / "I'm scared. Please hold me." / "Not arrived,
further along." in Italic / "Do the hard thing." in Bold), a weights strip
(Thin/Light/Regular/Bold), a paragraph block, and on page 2 a sample crate-sheet
apparatus block and a "what this render is" note. Build date, source commit,
tool versions, and **"DRAFT — NOT A RELEASE BUILD"** appear on the specimen
itself (red band, page 1; repeated in the footer and page 2 note). Layout was
visually QA'd; two spacing faults found in the first render (a DRAFT/italic
overlap, a rule grazing the alphabet's cap height) were fixed and re-rendered.

## 9. What remains for a real release (not done here)

1. **Fix the tooling properly, in the repo, with Branden's word:** redesign
   `prepareSoftnessMono.py` so it cannot rewrite its own code, the verifier's
   constants, attribution prose, or live path references (an allowlist of the
   `fontinfo.plist` familyName fields is all the current migration actually
   needs), and fix the `LICENSE.txt`/`LICENCE.txt` exemption typo. Apply R2–R4
   as a reviewed change set (the designspace rename completes the naming
   migration the July commits started; DERIVATIVE-NOTICE's naming policy
   already sanctions the SoftnessMono stem).
2. **Pin the toolchain** (requirements are lower-bounds only; this pass's
   versions are recorded in §2 as the first known-good set).
3. **Decide distribution** in light of the Fontspector `ufl` finding: the font
   can be released under UFL 1.0 from the project site/GitHub, but Google Fonts
   will not take a *new* UFL family. No licence change is legally available.
4. **QA triage:** decide which inherited WARN/FAIL items (interpolation issues,
   hMetrics count, trailing-space name records) are worth upstream-style fixes
   versus accepted inheritance — in a separate change set, per the
   DERIVATIVE-NOTICE change-recording policy.
5. **Then** the design questions the audit left open (A–F) — the Unarmored
   layer is still entirely unstarted; this pass changes none of that. It only
   proves the foundation builds and carries its own name.

## 10. Method / limits

Clone was public-repo HTTPS; nothing was pushed, branched, or committed — the
repairs exist only as an uncommitted diff in the scratch clone plus the preserved
`repairs_diff_muse.txt`. `make test` and `make proof` were not run as make
targets (fontspector was run directly to preserve its true exit code; diffenator2
proof was not run — the §7 table/outline comparison is the stronger instrument
for the equivalence question). The italic variable's `gvar`-level equivalence
was verified for the roman pair at table level and for both pairs at
default-instance outline level. Fontspector's two ERRORs are sandbox network
failures. Timestamps inside the built binaries are build-time values, as in any
fontmake build; binary hashes will therefore differ run to run even with
identical glyph data.
