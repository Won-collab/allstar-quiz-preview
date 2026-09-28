#!/usr/bin/env python3
"""
Build the Allstar fleet manager quiz from src/quiz-embed.html.

    python3 build.py --preview     -> index.html      (GitHub Pages, form stubbed)
    python3 build.py --handover    -> dist/embed.html (real Marketo IDs injected)
    python3 build.py --lp          -> dist/marketo-lp.html (paste into a Marketo LP)

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


def read_config() -> dict:
    if not CONFIG.exists():
        sys.exit(
            f"missing {CONFIG.name}. Create it with:\n"
            '  {"host": "https://....mktoweb.com", "munchkinId": "...", "formId": "..."}'
        )
    cfg = json.loads(CONFIG.read_text())
    for key in ("host", "munchkinId", "formId"):
        if not cfg.get(key):
            sys.exit(f"{CONFIG.name} is missing '{key}'")
    return cfg


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
    cfg = read_config()
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


def build_lp() -> pathlib.Path:
    """
    Build for pasting into a Marketo landing page.

    A Marketo LP already serves munchkin itself, and it serves forms2 whenever
    the page carries a form. Loading either a second time is what breaks: two
    munchkin inits double-count the page view, and a second forms2 re-registers
    the form. So the munchkin block goes entirely, and forms2 is loaded only if
    the page has not already provided it.
    """
    cfg = read_config()
    frag = read_source()

    frag = MUNCHKIN.sub("", frag)
    frag = FORMS2_SRC.sub("", frag)
    frag = LOADFORM.sub(LP_FORMS2, frag)

    frag = frag.replace("__MKTO_HOST__", cfg["host"].rstrip("/"))
    frag = frag.replace("__MKTO_MUNCHKIN_ID__", cfg["munchkinId"])
    frag = frag.replace("__MKTO_FORM_ID__", str(cfg["formId"]))

    if "__MKTO_" in frag:
        sys.exit("unresolved placeholder remains in landing page build")
    if "munchkin.marketo.net" in frag:
        sys.exit("munchkin survived the landing page build")

    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    out = dist / "marketo-lp.html"
    out.write_text(frag)
    return out


LP_FORMS2 = """<script>
/* Reuse the landing page's own forms2 if it has one, otherwise fetch it. */
(function(){
  var host = "__MKTO_HOST__", mid = "__MKTO_MUNCHKIN_ID__", fid = __MKTO_FORM_ID__;
  function load(){ MktoForms2.loadForm(host, mid, fid); }
  if (window.MktoForms2) { load(); return; }
  var s = document.createElement('script');
  s.src = host + '/js/forms2/js/forms2.min.js';
  s.onload = load;
  document.head.appendChild(s);
})();
</script>
"""


PREVIEW_PAGE = """<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Fleet manager quiz - mobile layout preview</title>
<style>
  html,body{margin:0;padding:0}
  /* No stand-in page chrome: it broke immersion when judging the design.
     Scroll-in-page behaviour was verified while the chrome existed. The page
     ground matches the quiz so there is no seam at the edges. */
  body{background:#000;color:#fff;-webkit-font-smoothing:antialiased}
  .embed-shell{max-width:1200px;margin:0 auto}
</style>
</head>
<body>

<div class="embed-shell">
__FRAGMENT__
</div>

<script>
/* Reproduces what Marketo forms2 actually injects: fixed pixel widths written
   straight onto the form and its rows. If the layout survives this, it will
   survive the real form. */
(function(){
  var f = document.getElementById('mktoForm___FORM_ID__');
  if(!f) return;
  f.className = 'mktoForm';
  f.setAttribute('style','width:1600px;font-family:Helvetica,Arial,sans-serif;padding:20px 20px 0');
  function row(label, type, name, hint){
    return '<div class="mktoFormRow" style="width:1600px">'
      + '<div class="mktoFieldDescriptor mktoFormCol" style="width:1600px">'
      + '<div class="mktoOffset" style="width:10px;height:1px"></div>'
      + '<div class="mktoFieldWrap" style="width:1590px">'
      + '<label class="mktoLabel" style="width:100px;padding-left:10px">' + label + '</label>'
      + '<div class="mktoGutter" style="width:10px;height:1px"></div>'
      + '<input type="' + type + '" name="' + name + '" class="mktoField" style="width:1470px"' + (hint ? ' placeholder="' + hint + '"' : '') + '>'
      + '<div class="mktoClear"></div></div><div class="mktoClear"></div></div></div>';
  }
  /* Field order is the real form 3131's (First name, Last name, Company,
     Email). Only the email field carries its own hint, as in the design; the
     other three are left without one so the label-to-placeholder fallback in
     the component is exercised too. */
  f.innerHTML = row('First name','text','FirstName')
    + row('Last name','text','LastName')
    + row('Company name','text','Company')
    + row('Email address','email','Email','you@company.co.uk')
    + '<div class="mktoButtonRow"><span class="mktoButtonWrap mktoNative" style="margin-left:110px">'
    + '<button type="button" class="mktoButton" id="pv-submit">Keep me informed</button></span></div>';
  if (typeof usePlaceholders === 'function') { usePlaceholders(f); }

  /* Validation, reproducing forms2: every field is required and the email
     must look like one. Like forms2, only the first failing field is flagged
     at a time: it gets .mktoInvalid, an injected .mktoError message and
     focus. Typing into it clears the error. Copy is the proposed wording for
     the real form's validation messages. */
  var MSG_REQUIRED = 'Please fill in this field.';
  var MSG_EMAIL = 'Please enter a valid email address.';
  function clearError(inp){
    inp.classList.remove('mktoInvalid');
    inp.removeAttribute('aria-invalid');
    var e = inp.parentNode.querySelector('.mktoError');
    if (e) e.parentNode.removeChild(e);
  }
  function flag(inp, msg){
    inp.classList.add('mktoInvalid');
    inp.setAttribute('aria-invalid','true');
    var e = document.createElement('div');
    e.className = 'mktoError';
    e.setAttribute('role','alert');
    e.innerHTML = '<div class="mktoErrorArrowWrap"><div class="mktoErrorArrow"></div></div><div class="mktoErrorMsg"></div>';
    e.querySelector('.mktoErrorMsg').textContent = msg;
    inp.parentNode.insertBefore(e, inp.nextSibling);
    inp.focus();
  }
  var fields = [].slice.call(f.querySelectorAll('input.mktoField'));
  fields.forEach(function(inp){ inp.addEventListener('input', function(){ clearError(inp); }); });

  /* Stubbed submit still drives the thank-you screen so that screen can be
     checked on a phone too, but only once the form validates. */
  document.getElementById('pv-submit').addEventListener('click', function(){
    fields.forEach(clearError);
    for (var i = 0; i < fields.length; i++) {
      var v = fields[i].value.trim();
      if (!v) { flag(fields[i], MSG_REQUIRED); return; }
      if (fields[i].type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) { flag(fields[i], MSG_EMAIL); return; }
    }
    if (typeof show === 'function') { show('s-thankyou'); }
    if (typeof scrollToQuiz === 'function') { scrollToQuiz(); }
  });
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
    g.add_argument("--lp", action="store_true", help="build dist/marketo-lp.html to paste into a Marketo landing page")
    args = ap.parse_args()

    out = build_preview() if args.preview else build_lp() if args.lp else build_handover()
    print(f"wrote {out.relative_to(ROOT)} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
