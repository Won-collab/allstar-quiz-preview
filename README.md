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

## Assets

Icons are the DS `Icon` set from `0002 Graphics library`, **exported as SVG from
Figma, not redrawn**. They are filled paths, so `fill` is `currentColor` and the
roundel sets `color`. Logos are the approved `allstar` and `allstar_inverted`
marks, exported the same way and never recoloured in CSS.

## Selection and rules

The selected option card reads as a fill step plus a rim. The rim uses the
default border token; on a dark ground that is the `-inverted` member of the
family, `color/border/default-inverted` (#FFFFFF at 19%). Plain
`color/border/default` resolves to #000000 at 7%, which is invisible on black.
Accent yellow is deliberately not used for selection, though the DS does have a
token for it (`color/border/active-subdued`, accent at 56%).

The base state carries a transparent border of the same width, so selecting a
card causes no layout shift.

The vertical rule on the result quote stays accent yellow: it is a brand
device rather than a state affordance.

## Input fields

They follow the DS `Input/S` component (set key `e6d0c0b5…`):

| part | value | token |
|---|---|---|
| label | Medium 14/16, sentence case | `color/content/primary-inverted` #F7F7F7 |
| box | 40px tall, 16px inset, radius 12 | `radius/input` |
| box fill | #0F0F0F | `color/bg/default`, Allstar **Dark** |
| box border | 1px #A8A8A8 | `color/border/input` |
| placeholder | Regular 14/16 #7D7D7D | `color/content/tertiary` |

The dark fill comes from a mode pin **inside** the component instance: the
`Input` frame carries `Allstar = Dark`, which is why the same
`color/bg/default` token reads #0F0F0F there and #FFFFFF elsewhere on the page.
New fields are cloned from an existing instance so that pin and the label
override travel with them.

Two DS values are overridden on coarse pointers only, and left intact on
desktop: 14px input text (iOS Safari zooms the page on focus below 16px) and the
40px box (under the 44px minimum touch target). Both become 16px / 44px on
touch.

## Footer

Removed from all screens for now. The `.fbar` CSS is kept so it can be restored
by putting the markup back. The screens carry their own bottom inset in its
absence.

## Open items

- **Typeface.** The DS font tokens resolve to Google Sans Flex, which is
  proprietary and not on Google Fonts. It is first in the stack so it wins where
  installed, but most visitors get the Inter fallback until web licensing is
  confirmed. Self-hosting it is a one-line change.
- **Question spot illustrations.** Only two exist in the design, so the six
  questions alternate between them. Four more are needed; add them to `QGFX` in
  question order and the alternation stops.
- **Persona illustrations.** All six personas still show the same star. Swapping
  in sourced artwork means replacing the `<svg>` in `ART` per persona.
- **Logo on the accent screen.** Neither approved variant works on yellow: the
  standalone mark's star is the same yellow, and the inverted mark is white. The
  mark is deliberately not recoloured. Needs a mono variant from the DAM, or the
  thank-you screen stops being full-bleed accent.
- **Intro logo is 82px wide**, matching the design. The brand book minimum
  digital width is 120px, so this is under it. Flagged rather than silently
  corrected.
- **Product-fit panel** is `#F7F7F7`, which has no confirmed Fluxus background
  token, so it is a named literal. The mark on that panel is the **plain** black
  variant: the design specifies `allstar_inverted`, which is white and would be
  invisible on a light surface.
- **Gating.** The result screen is split into Block A (persona and painpoint) and
  Block B (product fit and capture) with an empty `#gate-slot` between them.
  Gating later means moving the form into that slot and hiding Block B until
  submit. No redesign needed.
