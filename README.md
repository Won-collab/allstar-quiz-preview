# Fleet manager quiz - mobile layout preview

A throwaway preview used to check a quiz component's responsive layout on real
phones. Published with GitHub Pages purely so it can be opened on a handset.

## What this is

`index.html` is the quiz component wrapped in stand-in page chrome, so it is
scrolled inside a page rather than sitting alone in the viewport.

## What is stubbed

The marketing-automation form is **not** wired up. It is replaced with a visual
stand-in that reproduces the fixed pixel widths the real embed injects, which is
the thing that breaks mobile layouts. Nothing is submitted anywhere, and no
tracking script is loaded.

That means this preview is valid for checking:

- layout, type scale and reflow from 320px upward
- tap target sizes and touch states
- scroll behaviour between screens
- the six-option question and the long result screen

It is **not** valid for checking the real form's own rendering or its
submission behaviour. Those need a staging page with the live integration.

## Regenerating

`index.html` is generated from the component source, it is not hand-edited.
Rebuild it with the generator script rather than editing it in place.
