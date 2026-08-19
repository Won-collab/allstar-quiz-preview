#!/usr/bin/env python3
"""
Build the Allstar fleet manager quiz from src/quiz-embed.html.

    python3 build.py --preview     -> index.html      (GitHub Pages, form stubbed)
    python3 build.py --handover    -> dist/embed.html (real Marketo IDs injected)

src/quiz-embed.html is the source of truth and carries __MKTO_*__ placeholders,
so the whole component can live in a public repo. Real identifiers live only in
mkto.config.json, which is gitignored and never published.
"""

import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "src" / "quiz-embed.html"
CONFIG = ROOT / "mkto.config.json"

# Marketo blocks, stripped wholesale for the preview build.
FORMS2_SRC = re.compile(r'<script src="__MKTO_HOST__/js/forms2/js/forms2\.min\.js"></script>\s*')
LOADFORM = re.compile(r'<script>MktoForms2\.loadForm\([^\n]*\);</script>\s*')
MUNCHKIN = re.compile(r'<script type="text/javascript">\s*\(function\(\) \{\s*var didInit.*?\}\)\(\);\s*</script>\s*', re.S)

PREVIEW_FORM_ID = "0000"


def read_source() -> str:
    if not SRC.exists():
        sys.exit(f"missing source: {SRC}")
    return SRC.read_text()


def build_preview() -> pathlib.Path:
    frag = read_source()

    # Strip every Marketo dependency. Nothing in the published preview may
    # reference the real instance or create real leads.
    frag = FORMS2_SRC.sub("", frag)
    frag = LOADFORM.sub("", frag)
    frag = MUNCHKIN.sub("", frag)
    frag = frag.replace("__MKTO_FORM_ID__", PREVIEW_FORM_ID)
    frag = frag.replace("__MKTO_HOST__", "about:blank")
    frag = frag.replace("__MKTO_MUNCHKIN_ID__", "preview")

    for leak in ("mktoweb.com", "munchkin.marketo.net"):
        if leak in frag:
            sys.exit(f"refusing to publish: {leak} still present in preview build")

    page = PREVIEW_PAGE.replace("__FRAGMENT__", frag).replace("__FORM_ID__", PREVIEW_FORM_ID)
    out = ROOT / "index.html"
    out.write_text(page)
    return out


def build_handover() -> pathlib.Path:
    if not CONFIG.exists():
        sys.exit(
            f"missing {CONFIG.name}. Create it with:\n"
            '  {"host": "https://....mktoweb.com", "munchkinId": "...", "formId": "..."}'
        )
    cfg = json.loads(CONFIG.read_text())
    for key in ("host", "munchkinId", "formId"):
        if not cfg.get(key):
            sys.exit(f"{CONFIG.name} is missing '{key}'")

    frag = read_source()
    frag = frag.replace("__MKTO_HOST__", cfg["host"].rstrip("/"))
    frag = frag.replace("__MKTO_MUNCHKIN_ID__", cfg["munchkinId"])
    frag = frag.replace("__MKTO_FORM_ID__", str(cfg["formId"]))

    if "__MKTO_" in frag:
        sys.exit("unresolved placeholder remains in handover build")

    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    out = dist / "embed.html"
    out.write_text(frag)
    return out


PREVIEW_PAGE = """<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Fleet manager quiz - mobile layout preview</title>
<style>
  html,body{margin:0;padding:0}
  body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;background:#fff;color:#1a1a1a}
  /* Stand-in site chrome, so the quiz is scrolled inside a page the way it
     will be on the real site rather than sitting alone in the viewport. */
  .mock-header{height:52px;background:#111;color:#fff;display:flex;align-items:center;justify-content:space-between;padding:0 16px;font-size:11px;letter-spacing:.1em;text-transform:uppercase}
  .mock-intro{max-width:680px;margin:0 auto;padding:28px 20px 8px;font-size:15px;line-height:1.6;color:#3d3d3d}
  .mock-intro h1{font-size:22px;line-height:1.25;margin:0 0 10px;color:#000}
  .embed-shell{max-width:1200px;margin:0 auto;padding:12px 0 0}
  .mock-footer{margin-top:40px;padding:28px 20px 60px;background:#f2f2f0;font-size:12px;color:#878787;text-align:center}
  .pv-badge{position:fixed;z-index:9999;right:8px;bottom:8px;background:rgba(0,0,0,.86);color:#fff;font-size:10px;line-height:1.35;padding:7px 9px;border-radius:8px;font-variant-numeric:tabular-nums;pointer-events:none;max-width:46vw}
  .pv-badge b{color:#F2D400;font-weight:700}
</style>
</head>
<body>

<div class="mock-header"><span>Allstar</span><span>Preview</span></div>

<div class="mock-intro">
  <h1>Mobile layout preview</h1>
  <p>Stand-in page chrome. The quiz below is the real component. The email form is a visual stand-in, so nothing is submitted anywhere.</p>
</div>

<div class="embed-shell">
__FRAGMENT__
</div>

<div class="mock-footer">Stand-in site footer</div>

<div class="pv-badge" id="pvb">preview<br>form <b>stubbed</b><br><span id="pvw"></span></div>

<script>
/* Reproduces what Marketo forms2 actually injects: fixed pixel widths written
   straight onto the form and its rows. If the layout survives this, it will
   survive the real form. */
(function(){
  var f = document.getElementById('mktoForm___FORM_ID__');
  if(!f) return;
  f.className = 'mktoForm';
  f.setAttribute('style','width:1600px;font-family:Helvetica,Arial,sans-serif;padding:20px 20px 0');
  function row(label, type, name){
    return '<div class="mktoFormRow" style="width:1600px">'
      + '<div class="mktoFieldDescriptor mktoFormCol" style="width:1600px">'
      + '<div class="mktoOffset" style="width:10px;height:1px"></div>'
      + '<div class="mktoFieldWrap" style="width:1590px">'
      + '<label class="mktoLabel" style="width:100px;padding-left:10px">' + label + '</label>'
      + '<div class="mktoGutter" style="width:10px;height:1px"></div>'
      + '<input type="' + type + '" name="' + name + '" class="mktoField" style="width:1470px" placeholder="' + label + '">'
      + '<div class="mktoClear"></div></div><div class="mktoClear"></div></div></div>';
  }
  f.innerHTML = row('Business email','email','Email')
    + row('Company name','text','Company')
    + '<div class="mktoButtonRow"><span class="mktoButtonWrap mktoNative" style="margin-left:110px">'
    + '<button type="button" class="mktoButton" id="pv-submit">Keep me posted</button></span></div>';

  /* Stubbed submit still drives the thank-you screen so that screen can be
     checked on a phone too. */
  document.getElementById('pv-submit').addEventListener('click', function(){
    if (typeof show === 'function') { show('s-thankyou'); }
    if (typeof scrollToQuiz === 'function') { scrollToQuiz(); }
  });
})();

/* Live width readout, so a layout note can name the width it happened at. */
(function(){
  var out = document.getElementById('pvw'), qr = document.getElementById('qr');
  function tick(){ if(!qr) return; out.textContent = Math.round(qr.getBoundingClientRect().width) + ' css px'; }
  tick();
  addEventListener('resize', tick);
  addEventListener('orientationchange', function(){ setTimeout(tick, 250); });
})();
</script>

</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--preview", action="store_true", help="build index.html with the form stubbed")
    g.add_argument("--handover", action="store_true", help="build dist/embed.html with real Marketo IDs")
    args = ap.parse_args()

    out = build_preview() if args.preview else build_handover()
    print(f"wrote {out.relative_to(ROOT)} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
