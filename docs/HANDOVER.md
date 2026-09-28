# Fleet Personality Quiz · web handover

A self-contained quiz component for allstarcard.co.uk: six questions, six
fleet manager personas, a result per persona with a product match and email
capture, and an "all personality types" screen.

- **Live preview (reference for every behaviour below):**
  https://won-collab.github.io/allstar-quiz-preview/
  Add `?result=cost-hawk` (or any slug below) to open straight on a result.
- **Design:** Figma, Spark-GTM, section "Fleet personality quiz - full page".
- **Owner / questions:** Won Ha (Brand, Corpay UK).

---

## 1. What is in this package

| File | What it is |
|---|---|
| `embed.html` | The whole component: markup, CSS and script in one fragment. Paste it into an HTML / custom-code block. The Marketo form identifiers are already injected. |
| `assets/` | Eight images the component loads (see section 4). |
| `HANDOVER.md` | This document. |

The component has no build step and no dependencies to install. Everything is
scoped under `#qr`, so its CSS does not leak into the page and the page's CSS
should not reach into it.

---

## 2. Page setup in Contentful

**Template: a bare page with no site header, navigation or footer.** The quiz
fills the page and carries its own footer (the copyright line). If the site
header or footer appears, the copyright line is shown twice and the quiz stops
feeling like one continuous experience. Please confirm the template has
neither.

**Seven pages, all with the same embed:**

| Page | URL |
|---|---|
| Quiz | `https://allstarcard.co.uk/yourfleetpersonality` |
| The Cost Hawk | `https://allstarcard.co.uk/yourfleetpersonality/cost-hawk` |
| The Mileage Detective | `https://allstarcard.co.uk/yourfleetpersonality/mileage-detective` |
| The Fleet Firefighter | `https://allstarcard.co.uk/yourfleetpersonality/fleet-firefighter` |
| The Value Defender | `https://allstarcard.co.uk/yourfleetpersonality/value-defender` |
| The Accidental Pioneer | `https://allstarcard.co.uk/yourfleetpersonality/accidental-pioneer` |
| The Burned Out Manager | `https://allstarcard.co.uk/yourfleetpersonality/burned-out-manager` |

The results are screens inside the one component, not separate designs, so
every result page carries the identical embed. The component reads its own
URL:

- On a result path it opens straight on that result (shared links, refresh).
- When someone finishes the quiz it moves the address bar to their result's
  path with `history.pushState`. "Take the quiz again" moves it back to
  `/yourfleetpersonality`. Browser back and forward work between them.
- Any other path under `/yourfleetpersonality/` opens the quiz start. It is
  fine for the site to return a 404 for unknown slugs instead.

A single catch-all route serving the same page for all seven paths works just
as well, if that is easier than seven Contentful entries.

**Embed container:** full width, no padding or max-width from the page around
it, page background `#000000`. The component sizes itself from its own width
(CSS container queries), so any column width works, but the design assumes it
has the full viewport width on a phone.

**Page titles and meta:** suggest "What kind of fleet manager are you? |
Allstar" for the quiz page and "The Cost Hawk | Fleet Personality Quiz |
Allstar" (and so on) for the result pages. Result pages are shareable, so an
Open Graph image per persona would help; the persona images in `assets/`
can be used.

---

## 3. Fonts: self-host Google Sans Flex

The component is set in **Google Sans Flex** (OFL, free to self-host). The
embed does **not** load it from Google Fonts, so no visitor data goes to
Google. The site already self-hosts ITC Avant Garde the same way.

Please add it to the site's global CSS **under the exact family name
`"Google Sans Flex"`**, because that is the name the component asks for:

```css
@font-face {
  font-family: "Google Sans Flex";
  src: url("/fonts/GoogleSansFlex-Variable.woff2") format("woff2");
  font-weight: 400 700;
  font-style: normal;
  font-display: swap;
}
```

Weights used: 400, 500, 600. Files: the variable font from Google Fonts
(download) or the `@fontsource-variable/google-sans-flex` package.

Note: `next/font/google` also self-hosts, but it renames the family (for
example `__Google_Sans_Flex_1a2b3c`), which the component would not find. If
you use it, expose the generated family through a CSS variable and tell us,
and we will point the component at that variable instead.

Without the font the quiz still works and falls back to Inter, then the
system font.

---

## 4. Images

Eight PNGs, all loaded by the script (none are CSS backgrounds):

| File | Used on |
|---|---|
| `assets/persona/cost-hawk.png` | Result, all types screen |
| `assets/persona/mileage-detective.png` | Result, all types screen |
| `assets/persona/fleet-firefighter.png` | Result, all types screen |
| `assets/persona/value-defender.png` | Result, all types screen |
| `assets/persona/accidental-pioneer.png` | Result, all types screen |
| `assets/persona/burned-out-manager.png` | Result, all types screen |
| `assets/intro/accidental-pioneer.png` | Quiz start |
| `assets/intro/mileage-detective.png` | Quiz start |

As delivered, the paths are relative (`assets/...`), which will not resolve
from a result path such as `/yourfleetpersonality/cost-hawk`. **Please host the
`assets/` folder and send us the folder URL.** We rebuild `embed.html` with
absolute paths (one setting). Keep the folder structure and file names.

All eight have transparent corners (they are circles) and are palette-
optimised, 15 to 30 KB each. The component preloads the persona images as
soon as it loads, so the result never waits on the network.

---

## 5. Third-party scripts and security

- **Marketo Forms 2.0** (`forms2.min.js`) is loaded by the embed from the
  Marketo instance, and renders the email capture form.
- **Marketo Munchkin** is loaded by the embed. **If the site already loads
  Munchkin globally, remove the Munchkin block from `embed.html`** (the
  `<script>` that calls `Munchkin.init`), or page views are counted twice.
- **CSP:** the site currently sends only `upgrade-insecure-requests`, so
  nothing needs allow-listing. If a stricter policy is added, it needs the
  Marketo instance host (`script-src`, `connect-src`, `form-action`, `img-src`)
  and `munchkin.marketo.net` (`script-src`).
- No cookies are set by the component itself. Marketo sets its own.

---

## 6. Behaviour spec

Every behaviour below is live on the preview. When in doubt, the preview is the
reference.

**Screens:** quiz start → six questions (one at a time, Back / Next, Next is
disabled until an option is chosen) → result → optional all types screen →
thank you (after the form is submitted).

**Result logic:** each option maps to one persona; question 6 counts 1.5×. On
a tie, the persona that reached the winning score first wins.

**Scroll:** every screen change scrolls the top of the quiz into view (the quiz
may sit below other content). On the all types screen, opening a card scrolls
it to 40% of the viewport.

**Share the quiz:** copies `https://allstarcard.co.uk/yourfleetpersonality` to
the clipboard and shows "Link copied". Needs HTTPS (it falls back to an older
copy method elsewhere).

**Email capture (Marketo form):** four fields, placeholder-only as designed.
The script copies each field's label into its placeholder (unless the form
sets its own hint text) and hides the label visually (it stays for screen
readers). Rows holding only hidden fields are collapsed. Styled states: default, typing (violet
rim), error (red rim, icon and message under the field). On a successful
submit the thank-you screen shows; the form's own thank-you page or redirect
is not used.

**Motion (all CSS transforms, no layout animation except the card list):**

| Where | What |
|---|---|
| Quiz start | The two coins flip once into place, then float gently. Tap one to flip it again. |
| Option pick | The card springs once. Press sinks it slightly. |
| Result | The persona coin turns once and settles; the copy rises in. Tap the coin to spin it. |
| All types | Coins slide up one after another. Press lifts a coin (more for coins in front). Opening one lifts the screen as a whole, parts the coins below for the description, and scrolls it into view. |

**Reduced motion:** with the OS "reduce motion" setting on, every animation
collapses to its end state and nothing floats or spins.

**Accessibility:** options, coins and links are real buttons or have button
semantics, all keyboard-operable with a visible focus ring. Minimum touch
target 44px. Result coin is announced as "Spin your card".

**Responsive:** verified at 320, 360, 390, 480, 560, 720, 900 and 1200px wide
with no horizontal overflow. Options go to two columns at 560px and the
six-option question to three at 900px.

**Touch devices:** iOS Safari only applies `:active` when a touch listener is
present; the component adds one. Please do not strip it.

---

## 7. Analytics

- **Results in GA4:** each result has its own URL, so results appear as page
  views. The component changes the URL with `history.pushState`, which GA4
  records only with **Enhanced measurement → Page views → "Page changes based
  on browser history events"** switched on. Please confirm it is on for the
  site's GA4 property.
- **UTMs:** the "Discover more" link on each result goes to the product page
  with `utm_source=content&utm_medium=website&utm_campaign=fy26-09-uk-as-fleet-manager-quiz-<persona>`.
- The persona is **not** sent to Marketo by the form today. Saving it as a
  lead field (for Salesforce) is agreed separately and will need a hidden
  field on the form plus one line in the component.

---

## 8. QA checklist before launch

- [ ] Template shows no site header or footer; the quiz footer is visible.
- [ ] All seven URLs load; a result URL opens on that result.
- [ ] Finish the quiz: the address bar moves to the result URL; refresh keeps
      the result; "Take the quiz again" returns to `/yourfleetpersonality`.
- [ ] Google Sans Flex renders (not Inter or the system font).
- [ ] All eight images load from their hosted URLs on a result page.
- [ ] Email form: empty submit is blocked with an error; a valid submit shows
      the thank-you screen and creates a lead in Marketo.
- [ ] Munchkin fires once per page view (not twice).
- [ ] GA4 records a page view on the result URL after finishing the quiz.
- [ ] "Share the quiz" copies the link on iPhone Safari and Android Chrome.
- [ ] On a phone: the start coins flip in smoothly; pressing a coin on the all
      types screen lifts it.
- [ ] "Discover more" opens the right product page with its UTM.

---

## 9. Open items and owners

| Item | Owner |
|---|---|
| **The form in the embed is a general "Request Callback" form, not the quiz form.** Checked live on 2026-09-28: its button reads "Request Callback" (design: "Keep me informed"), it carries its own callback consent next to the quiz's research consent (two different consents on one form), and its hints read "Email Address" (design: "you@company.co.uk"). Recommended: clone it as a dedicated quiz form, set the button, one agreed consent line and the hint text there, and send us the new form ID. We rebuild `embed.html`. | Marketo builder + Legal (consent) |
| Host `assets/` and send the folder URL | Web team → we rebuild `embed.html` |
| Self-host Google Sans Flex under that family name | Web team |
| Bare template, seven pages (or catch-all), GA4 history setting | Web team |
| Marketo form: all four fields Required; validation messages "Please fill in this field." / "Please enter a valid email address." | Marketo builder |
| Privacy policy link (`https://allstarcard.co.uk/privacy-policy`) in the result emails | Marketo builder |
| Persona saved as a lead field for Salesforce | Agreed, scoped separately |
