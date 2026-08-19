import re, pathlib

SRC = pathlib.Path('/Users/won.ha/Downloads/allstar_fleet_manager_quiz_v8_mobile.html')
OUT = pathlib.Path('/Users/won.ha/allstar-quiz-preview/index.html')

frag = SRC.read_text()

# Strip every Marketo dependency: the forms2 loader, the loadForm call and the
# Munchkin tracker. Nothing in the published preview may reference the real
# Marketo instance or create real leads.
frag = frag.replace('<script src="https://498-FVF-702.mktoweb.com/js/forms2/js/forms2.min.js"></script>\n', '')
frag = frag.replace('<script>MktoForms2.loadForm("https://498-FVF-702.mktoweb.com", "498-FVF-702", 3131);</script>\n', '')
frag = re.sub(r'<script type="text/javascript">\n\(function\(\) \{\n  var didInit.*?\}\)\(\);\n</script>\n', '', frag, flags=re.S)

assert 'mktoweb.com' not in frag, 'Marketo host still present'
assert 'munchkin' not in frag.lower(), 'Munchkin still present'
assert '498-FVF-702' not in frag, 'Marketo instance id still present'

PAGE = """<!doctype html>
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
  /* Preview-only badge. Makes it obvious this is not the live form. */
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
  var f = document.getElementById('mktoForm_3131');
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
  function tick(){
    if(!qr) return;
    out.textContent = Math.round(qr.getBoundingClientRect().width) + ' css px';
  }
  tick();
  addEventListener('resize', tick);
  addEventListener('orientationchange', function(){ setTimeout(tick, 250); });
})();
</script>

</body>
</html>
"""

OUT.write_text(PAGE.replace('__FRAGMENT__', frag))
print('wrote', OUT, OUT.stat().st_size, 'bytes')
