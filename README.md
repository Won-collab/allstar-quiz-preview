# Fleet manager quiz

A quiz component for a fleet event, built to be embedded in a page on the
Allstar site. This repo holds the component source and publishes a preview so
the layout can be checked on real phones.

## Layout

```
src/quiz-embed.html   the component. Source of truth. Hand-edit this.
build.py              generates the two builds below
index.html            generated preview, served by GitHub Pages
dist/embed.html       generated handover build (gitignored)
mkto.config.json      real marketing-automation identifiers (gitignored)
```

## Builds

```
python3 build.py --preview     -> index.html      form stubbed, safe to publish
python3 build.py --handover    -> dist/embed.html real identifiers injected
```

`src/quiz-embed.html` carries `__MKTO_*__` placeholders, so the whole component
can live in a public repo. Real identifiers exist only in `mkto.config.json`,
which is gitignored. The preview build strips the marketing-automation scripts
entirely and asserts that no identifier survived before writing the file.

`index.html` is generated. Do not hand-edit it, the next build overwrites it.

## Design source

Figma file `4hG6HmgGe9p2ZtbeF1vTzF`, page **Design**. Five frames at 390 wide:
intro, question, question with six options, result, thank you.

Colour, radius, spacing and type in the CSS are the resolved values of Fluxus
semantic tokens with the Allstar brand collection pinned on that page. Token
names are preserved in the CSS custom-property names so provenance survives.
Do not hand-tune them, re-resolve from Figma if the design system moves.

Buttons follow the DS `Button` component: `radius/button` is 12px, sizes are the
Large 56 / Medium 48 ladder, and the disabled state uses DS colours rather than
fading the whole control.

## What is stubbed in the preview

The email form is a visual stand-in that reproduces the fixed pixel widths the
real embed injects, which is the thing that breaks mobile layouts. Nothing is
submitted and no tracking script loads. Submitting advances to the thank-you
screen so that screen can be checked too.

Valid for: layout and reflow from 320px up, tap target sizes, touch states,
scroll behaviour between screens, the six-option question, the long result
screen.

Not valid for: the real form's own rendering or its submission behaviour. Those
need a staging page with the live integration.

## Verified

320 / 360 / 390 / 480 / 560 / 720 / 900 / 1200px container widths, all screens:
no horizontal overflow, no vertical clipping, no tap target under 44px, inputs
at 16px so iOS does not zoom on focus. Options reflow 1 to 2 columns at 560, and
the six-option question goes to 3 columns at 900.

## Open items

- **Typeface.** The DS font tokens resolve to Google Sans Flex, which is
  proprietary and not on Google Fonts. It is first in the stack so it wins where
  installed, but most visitors get the Inter fallback until web licensing is
  confirmed. Self-hosting it is a one-line change.
- **Logo on the accent screen.** Neither approved variant works on yellow: the
  standalone mark's star is the same yellow, and the inverted mark is white. The
  mark is deliberately not recoloured. Needs a mono variant from the DAM, or the
  thank-you screen stops being full-bleed accent.
- **Persona illustrations.** All six personas currently show the same star
  placeholder. Swapping in sourced artwork means replacing the `<svg>` inside
  `.persona-art` and adding entries to `ART`.
- **Gating.** The result screen is split into Block A (persona and painpoint) and
  Block B (product fit and capture) with an empty `#gate-slot` between them.
  Gating later means moving the form into that slot and hiding Block B until
  submit. No redesign needed.
