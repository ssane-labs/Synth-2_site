# Builds /learn/index.html for sanelabs.org from the three curated JSON parts.
# The page is a static index: no framework, no animation library, no build step.
import json, os, html, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("LEARN_OUT", os.path.join(HERE, "index.html"))

cats = []
for p in ("part1.json", "part2.json", "part3.json"):
    cats.extend(json.load(open(os.path.join(HERE, "links", p), encoding="utf-8")))

TOTAL = sum(len(c["items"]) for c in cats)
NCATS = len(cats)
TODAY = datetime.date.today().isoformat()

KINDS = [
    ("course", "Course"), ("video", "Video"), ("book", "Book"),
    ("docs", "Docs"), ("code", "Code"), ("notebook", "Notebook"),
    ("paper", "Paper"), ("article", "Article"),
    ("interactive", "Interactive"), ("reference", "Reference"),
    ("blog", "Blog"), ("tool", "Tool"),
]
KIND_LABEL = dict(KINDS)

TRACKS = [
    ("You have never trained anything",
     "Start at the bottom and do not skip the maths. Three to six months, honestly.",
     [("Foundations", "#foundations"), ("Python & tooling", "#python"),
      ("Classical ML", "#classical-ml"), ("Deep learning", "#deep-learning")]),
    ("You can code and want to fine-tune this week",
     "Skip the theory for now. Run one fine-tune end to end, then come back for the parts that broke.",
     [("Fine-tuning", "#finetuning"), ("Data & datasets", "#data"),
      ("Evaluation", "#evaluation"), ("Free compute", "#practice")]),
    ("You want to understand a model, not just use one",
     "Write one. Everything after that reads differently.",
     [("Build an LLM from scratch", "#from-scratch"), ("NLP & transformers", "#nlp"),
      ("Pretraining & scale", "#pretraining"), ("Interpretability", "#interp")]),
]

e = html.escape


def row(it):
    k = it.get("k", "reference")
    return (
        f'<a class="row" href="{e(it["u"])}" target="_blank" rel="noopener noreferrer" '
        f'data-k="{e(k)}" data-s="{e((it["t"] + " " + it["by"] + " " + it["m"] + " " + KIND_LABEL.get(k, k)).lower())}">'
        f'<span class="kind k-{e(k)}">{e(KIND_LABEL.get(k, k))}</span>'
        f'<span class="t">{e(it["t"])}</span>'
        f'<span class="by">{e(it["by"])}</span>'
        f'<span class="m">{e(it["m"])}</span>'
        f'<svg class="arw" width="12" height="12" viewBox="0 0 13 13" fill="none" aria-hidden="true">'
        f'<path d="M3 10 10 3M10 3H4.5M10 3v5.5" stroke="currentColor" stroke-width="1.5" '
        f'stroke-linecap="round" stroke-linejoin="round"/></svg></a>'
    )


nav = "\n      ".join(
    f'<a href="#{c["id"]}"><i>{c["n"]}</i><span>{e(c["title"])}</span></a>' for c in cats
)

chips = "\n        ".join(
    f'<button class="chip" data-kind="{k}" type="button">{lab}</button>' for k, lab in KINDS
)

tracks_html = "\n      ".join(
    '<div class="track"><h3>{}</h3><p>{}</p><div class="jump">{}</div></div>'.format(
        e(t), e(d), "".join(f'<a href="{u}">{e(n)}</a>' for n, u in links)
    )
    for t, d, links in TRACKS
)

sections = []
for c in cats:
    rows = "\n        ".join(row(it) for it in c["items"])
    sections.append(
        f'''    <section id="{c["id"]}" data-sec>
      <div class="sec-mark"><i>{c["n"]}</i><h2>{e(c["title"])}</h2><span class="bar"></span>'''
        f'<span class="tally"><b data-count>{len(c["items"])}</b></span></div>\n'
        f'      <p class="sec-note">{e(c["note"])}</p>\n'
        f'      <div class="rows">\n        {rows}\n      </div>\n'
        f'      <p class="empty" hidden>Nothing in this section matches the filter.</p>\n'
        f'    </section>'
    )
sections = "\n\n".join(sections)

PAGE = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Learn — Sane Labs</title>
<meta name="description" content="{TOTAL} free resources for learning to train and fine-tune language models, sorted into {NCATS} sections. Courses, books, papers and code from universities, labs and the people who wrote the libraries. Every link goes to the original.">
<meta name="color-scheme" content="light dark">
<link rel="canonical" href="https://sanelabs.org/learn/">
<meta name="theme-color" content="#EFECE3" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#191816" media="(prefers-color-scheme: dark)">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Sane Labs">
<meta property="og:locale" content="en">
<meta property="og:url" content="https://sanelabs.org/learn/">
<meta property="og:title" content="Learn — Sane Labs">
<meta property="og:description" content="{TOTAL} free resources for learning to train and fine-tune language models, in {NCATS} sections. Every link goes to the original.">
<meta property="og:image" content="https://sanelabs.org/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Learn — Sane Labs">
<meta name="twitter:description" content="{TOTAL} free resources for learning to train and fine-tune language models.">
<meta name="twitter:image" content="https://sanelabs.org/og.png">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Cstyle%3E.r{{stroke:%23141413}}%40media(prefers-color-scheme:dark){{.r{{stroke:%23F0EDE4}}}}%3C/style%3E%3Ccircle class='r' cx='16' cy='16' r='13' fill='none' stroke-width='2.4' stroke-dasharray='5 4'/%3E%3Ccircle cx='16' cy='16' r='5' fill='%23C46849'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300..600&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">

<style>
/* Same family as the lab register: one accent, the same three faces, the left
   rail and a single column. Different object though — this page is a catalogue,
   so the rows are tight, there is a filter, and nothing animates on scroll. */
:root{{
  --paper:#EFECE3;--paper-2:#E7E3D8;--ink:#141413;--ink-2:#3A3A37;--ink-3:#6F6E68;--ink-4:#9C9A92;
  --rule:rgba(20,20,19,.13);--rule-soft:rgba(20,20,19,.07);
  --accent:#C46849;--accent-soft:rgba(196,104,73,.10);--glow:rgba(196,104,73,.13);
  --good:#3C6B4F;
  --serif:"Fraunces","Iowan Old Style",Georgia,"Times New Roman",serif;
  --sans:"Inter",ui-sans-serif,system-ui,"Segoe UI",Helvetica,Arial,sans-serif;
  --mono:"IBM Plex Mono",ui-monospace,SFMono-Regular,Consolas,monospace;
}}
@media (prefers-color-scheme:dark){{
  :root:not([data-theme="light"]){{
    --paper:#191816;--paper-2:#211F1C;--ink:#F0EDE4;--ink-2:#CFCBC1;--ink-3:#928E85;--ink-4:#66635C;
    --rule:rgba(240,237,228,.14);--rule-soft:rgba(240,237,228,.07);
    --accent:#DE9070;--accent-soft:rgba(222,144,112,.13);--glow:rgba(222,144,112,.12);
    --good:#7FBF9A;
  }}
}}
:root[data-theme="dark"]{{
  --paper:#191816;--paper-2:#211F1C;--ink:#F0EDE4;--ink-2:#CFCBC1;--ink-3:#928E85;--ink-4:#66635C;
  --rule:rgba(240,237,228,.14);--rule-soft:rgba(240,237,228,.07);
  --accent:#DE9070;--accent-soft:rgba(222,144,112,.13);--glow:rgba(222,144,112,.12);
  --good:#7FBF9A;
}}

*{{box-sizing:border-box}}
body{{margin:0}}
/* the filter hides rows with the `hidden` property, and an author `display`
   rule beats the user-agent's [hidden] one — so say it here, explicitly */
[hidden]{{display:none!important}}
html{{overflow-x:clip;scroll-behavior:smooth}}
body{{background:var(--paper);color:var(--ink);font-family:var(--sans);font-size:16.5px;line-height:1.65;-webkit-font-smoothing:antialiased;overflow-x:clip}}
:focus-visible{{outline:2px solid var(--accent);outline-offset:3px}}
p{{margin:0}}
a{{color:inherit}}
h1,h2,h3{{margin:0;font-weight:400}}
.mono{{font-family:var(--mono);font-variant-numeric:tabular-nums}}

.glow{{position:fixed;width:58vw;height:58vw;right:-18vw;top:-14vw;border-radius:50%;
  background:radial-gradient(circle,var(--glow),transparent 66%);filter:blur(80px);
  pointer-events:none;z-index:0}}

.shell{{position:relative;z-index:1;display:grid;grid-template-columns:300px 1fr;max-width:1360px;margin:0 auto}}
.rail{{
  position:sticky;top:0;height:100vh;padding:44px 36px 32px 40px;
  border-right:1px solid var(--rule);display:flex;flex-direction:column;gap:24px;overflow:hidden;
}}
.brand{{display:flex;align-items:center;gap:10px;text-decoration:none;font-size:17px;font-weight:500;letter-spacing:-.01em;flex:none}}
.glyph{{width:20px;height:20px;flex:none}}
.glyph .ring{{transform-origin:50% 50%;animation:spin 34s linear infinite}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
.rail .said{{font-size:14px;color:var(--ink-3);line-height:1.55;max-width:30ch;flex:none}}
.rail nav{{display:grid;gap:0;overflow-y:auto;min-height:0;margin-right:-10px;padding-right:10px;
  scrollbar-width:thin;scrollbar-color:var(--rule) transparent}}
.rail nav a{{
  display:grid;grid-template-columns:26px 1fr;gap:9px;align-items:baseline;
  padding:7px 0;border-top:1px solid var(--rule-soft);text-decoration:none;
  font-size:13.5px;color:var(--ink-2);transition:color .25s ease;
}}
.rail nav a:last-of-type{{border-bottom:1px solid var(--rule-soft)}}
.rail nav a i{{font-family:var(--mono);font-style:normal;font-size:10.5px;color:var(--ink-4);transition:color .25s ease}}
.rail nav a:hover,.rail nav a:hover i,.rail nav a.on,.rail nav a.on i{{color:var(--accent)}}
.rail .foot{{font-family:var(--mono);font-size:10.5px;color:var(--ink-4);line-height:1.7;letter-spacing:.02em;flex:none}}
.rail .foot a{{color:var(--ink-3);text-decoration:none;border-bottom:1px solid var(--rule)}}
.rail .foot a:hover{{color:var(--accent)}}

.col{{padding:0 clamp(28px,5vw,86px)}}
.masthead{{padding:110px 0 56px;border-bottom:1px solid var(--rule)}}
.crumb{{font-family:var(--mono);font-size:10.5px;letter-spacing:.18em;text-transform:uppercase;color:var(--ink-4);
  text-decoration:none;display:inline-flex;gap:8px;align-items:center;margin-bottom:26px}}
.crumb:hover{{color:var(--accent)}}
.masthead h1{{font-family:var(--serif);font-weight:330;font-size:clamp(44px,6.2vw,82px);line-height:1.03;letter-spacing:-.03em;max-width:14ch}}
.masthead .lede{{margin-top:28px;font-size:clamp(17px,1.5vw,20px);color:var(--ink-3);max-width:60ch;line-height:1.6}}
.masthead .facts{{display:flex;flex-wrap:wrap;gap:0;margin-top:40px}}
.masthead .facts div{{padding-right:34px;margin-right:34px;border-right:1px solid var(--rule-soft)}}
.masthead .facts div:last-child{{border-right:0;margin-right:0;padding-right:0}}
.masthead .facts dt{{font-family:var(--mono);font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--ink-4)}}
.masthead .facts dd{{margin:6px 0 0;font-family:var(--mono);font-size:15px;font-variant-numeric:tabular-nums}}

section{{padding:76px 0 0;scroll-margin-top:124px}}   /* clears the sticky filter */
.sec-mark{{display:flex;align-items:baseline;gap:16px;margin-bottom:20px}}
.sec-mark i{{font-family:var(--mono);font-style:normal;font-size:11.5px;color:var(--accent);letter-spacing:.14em}}
.sec-mark h2{{font-family:var(--mono);font-size:12px;font-weight:500;letter-spacing:.2em;text-transform:uppercase;color:var(--ink-3);white-space:nowrap}}
.sec-mark .bar{{flex:1;height:1px;background:var(--rule)}}
.sec-mark .tally{{font-family:var(--mono);font-size:11px;color:var(--ink-4);font-variant-numeric:tabular-nums}}
.sec-note{{font-size:16.5px;color:var(--ink-3);max-width:64ch;margin:0 0 26px;line-height:1.6}}

/* ---------- start here ---------- */
.tracks{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:0;margin-top:2px}}
.track{{padding:26px 26px 26px 0;border-top:1px solid var(--rule);border-right:1px solid var(--rule-soft);margin-right:26px}}
.track:last-child{{border-right:0;margin-right:0;padding-right:0}}
.track h3{{font-family:var(--serif);font-weight:330;font-size:21px;letter-spacing:-.02em;line-height:1.25}}
.track p{{margin-top:10px;font-size:14.5px;color:var(--ink-3);line-height:1.55}}
.track .jump{{display:flex;flex-direction:column;gap:0;margin-top:16px}}
.track .jump a{{font-family:var(--mono);font-size:11.5px;letter-spacing:.04em;color:var(--ink-2);text-decoration:none;
  padding:6px 0;border-top:1px solid var(--rule-soft);transition:color .25s ease}}
.track .jump a:hover{{color:var(--accent)}}
.track .jump a::before{{content:"→ ";color:var(--ink-4)}}

/* ---------- filter ---------- */
.filter{{position:sticky;top:0;z-index:30;padding:16px 0 14px;background:var(--paper);
  border-bottom:1px solid var(--rule);margin-top:64px}}
.filter .fline{{display:flex;gap:12px;align-items:center;flex-wrap:wrap}}
.filter input{{
  flex:1;min-width:220px;background:var(--paper-2);border:1px solid var(--rule);color:var(--ink);
  font-family:var(--sans);font-size:15px;padding:11px 14px;border-radius:2px;
}}
.filter input::placeholder{{color:var(--ink-4)}}
.filter input:focus{{outline:none;border-color:var(--accent)}}
.chips{{display:flex;flex-wrap:wrap;gap:6px;margin-top:11px}}
.chip{{
  font-family:var(--mono);font-size:10.5px;letter-spacing:.13em;text-transform:uppercase;
  color:var(--ink-3);background:transparent;border:1px solid var(--rule);border-radius:2px;
  padding:5px 9px;cursor:pointer;transition:color .2s ease,border-color .2s ease,background .2s ease;
}}
.chip:hover{{color:var(--ink);border-color:var(--ink-4)}}
.chip.on{{color:var(--accent);border-color:var(--accent);background:var(--accent-soft)}}
.fcount{{font-family:var(--mono);font-size:11px;color:var(--ink-4);font-variant-numeric:tabular-nums;white-space:nowrap}}
.fclear{{font-family:var(--mono);font-size:10.5px;letter-spacing:.13em;text-transform:uppercase;color:var(--ink-4);
  background:none;border:0;cursor:pointer;padding:5px 0}}
.fclear:hover{{color:var(--accent)}}

/* ---------- the rows ---------- */
.rows{{display:grid}}
.row{{
  display:grid;grid-template-columns:80px minmax(0,1.35fr) minmax(0,.72fr) minmax(0,1.25fr) 13px;
  gap:18px;align-items:baseline;padding:13px 0;border-top:1px solid var(--rule-soft);
  text-decoration:none;color:inherit;
}}
.rows .row:last-of-type{{border-bottom:1px solid var(--rule-soft)}}
.row .kind{{font-family:var(--mono);font-size:9.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink-4)}}
.row .t{{font-size:15.5px;color:var(--ink);line-height:1.4;transition:color .2s ease}}
.row .by{{font-size:13.5px;color:var(--ink-3);line-height:1.4}}
.row .m{{font-size:13.5px;color:var(--ink-4);line-height:1.45}}
.row .arw{{color:transparent;transition:transform .3s cubic-bezier(.22,1,.36,1),color .2s ease;align-self:center}}
.row:hover{{background:var(--accent-soft)}}
.row:hover .t{{color:var(--accent)}}
.row:hover .arw{{color:var(--accent);transform:translate(2px,-2px)}}
.row:hover .kind{{color:var(--accent)}}
.k-course,.k-video,.k-book{{color:var(--ink-3)!important}}
.empty{{font-family:var(--mono);font-size:12px;color:var(--ink-4);padding:14px 0}}

/* between the rail appearing and the column being genuinely wide, four columns
   squeeze every title onto three lines — stack the description instead */
@media (min-width:981px) and (max-width:1299px){{
  .row{{grid-template-columns:76px minmax(0,1fr) 13px;gap:3px 16px}}
  .row .kind{{grid-column:1;grid-row:1/4}}
  .row .t{{grid-column:2;grid-row:1}}
  .row .by{{grid-column:2;grid-row:2}}
  .row .m{{grid-column:2;grid-row:3}}
  .row .arw{{grid-column:3;grid-row:1/4;align-self:start;margin-top:4px;color:var(--ink-4)}}
}}

.tail{{padding:70px 0 90px;font-family:var(--mono);font-size:11.5px;color:var(--ink-4);line-height:1.8;letter-spacing:.02em;border-top:1px solid var(--rule);margin-top:76px}}
.tail a{{color:var(--ink-3);text-decoration:none;border-bottom:1px solid var(--rule)}}
.tail a:hover{{color:var(--accent)}}
.totop{{display:inline-block;margin-top:18px;font-family:var(--mono);font-size:10.5px;letter-spacing:.16em;
  text-transform:uppercase;color:var(--ink-4);text-decoration:none}}
.totop:hover{{color:var(--accent)}}

/* mobile: the rail becomes a plain header */
.topbar{{display:none}}
@media (max-width:980px){{
  .shell{{grid-template-columns:minmax(0,1fr)}}
  .rail{{display:none}}
  .topbar{{
    display:flex;align-items:center;justify-content:space-between;gap:16px;
    position:sticky;top:0;z-index:40;padding:14px 24px;
    background:color-mix(in srgb,var(--paper) 88%,transparent);
    backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);
    border-bottom:1px solid var(--rule);
  }}
  .topbar a{{text-decoration:none;font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink-3)}}
  .col{{padding:0 22px}}
  .masthead{{padding:52px 0 44px}}
  .masthead h1{{font-size:clamp(33px,9.2vw,46px)}}
  .masthead .lede{{font-size:16.5px;margin-top:20px}}
  .masthead .facts{{margin-top:28px}}
  .masthead .facts div{{padding-right:18px;margin-right:18px;margin-bottom:12px}}
  .tracks{{grid-template-columns:minmax(0,1fr)}}
  .track{{padding:22px 0;border-right:0;margin-right:0}}
  .filter{{top:51px;margin-top:48px}}
  section{{padding:54px 0 0;scroll-margin-top:170px}}
  .sec-mark{{margin-bottom:16px}}
  .sec-note{{font-size:15.5px;margin-bottom:20px}}
  .row{{grid-template-columns:minmax(0,1fr) 13px;gap:4px 12px;padding:15px 0}}
  .row .kind{{grid-column:1;order:1}}
  .row .t{{grid-column:1;order:2;font-size:16px}}
  .row .by{{grid-column:1;order:3}}
  .row .m{{grid-column:1;order:4}}
  .row .arw{{grid-column:2;grid-row:1/5;align-self:start;margin-top:4px;color:var(--ink-4)}}
  .tail{{padding:50px 0 64px;margin-top:54px}}
}}
.shell>*{{min-width:0}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important;transition:none!important}}
  html{{scroll-behavior:auto}}}}
</style>

<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"CollectionPage",
 "name":"Learn — Sane Labs","url":"https://sanelabs.org/learn/",
 "inLanguage":"en","isPartOf":{{"@type":"WebSite","url":"https://sanelabs.org/","name":"Sane Labs"}},
 "description":"{TOTAL} free resources for learning to train and fine-tune language models, sorted into {NCATS} sections.",
 "about":["machine learning","deep learning","language models","fine-tuning"]}}
</script>
</head>

<body>

<div class="glow" aria-hidden="true"></div>

<div class="topbar">
  <a href="/">← Sane Labs</a>
  <a href="#foundations">Sections</a>
</div>

<div class="shell" id="top">
  <aside class="rail">
    <a class="brand" href="/">
      <svg class="glyph" viewBox="0 0 22 22" aria-hidden="true"><circle class="ring" cx="11" cy="11" r="9" fill="none" stroke="currentColor" stroke-width="1.4" stroke-dasharray="3.4 2.8"></circle><circle cx="11" cy="11" r="3.4" fill="var(--accent)"></circle></svg>
      Sane Labs
    </a>
    <p class="said">A reading list. Everything on it is free to read or watch, and every link goes to the original.</p>
    <nav>
      {nav}
    </nav>
    <div class="foot">{TOTAL} links · {NCATS} sections<br>Checked {TODAY}<br><a href="mailto:ssanelabs@gmail.com?subject=learn%20—%20a%20broken%20or%20missing%20link">Report a dead link</a></div>
  </aside>

  <main class="col">
    <header class="masthead">
      <a class="crumb" href="/">← The lab</a>
      <h1>Learn to train the thing yourself.</h1>
      <p class="lede">Everything below was written or taught by someone else — universities, research labs, and the people who wrote the libraries you will import. None of it costs money, and none of it is summarised here: each row is a link to the original, with one line saying what it is and how long it takes. Sorted so you can start anywhere and know what you are skipping.</p>
      <dl class="facts">
        <div><dt>Links</dt><dd>{TOTAL}</dd></div>
        <div><dt>Sections</dt><dd>{NCATS}</dd></div>
        <div><dt>Behind a paywall</dt><dd>0</dd></div>
        <div><dt>Last checked</dt><dd>{TODAY}</dd></div>
      </dl>
    </header>

    <section id="start" data-skip>
      <div class="sec-mark"><i>00</i><h2>Start here</h2><span class="bar"></span></div>
      <p class="sec-note">Three honest routes in. Pick the one that describes you now, not the one that describes who you want to be.</p>
      <div class="tracks">
      {tracks_html}
      </div>
    </section>

    <div class="filter" id="filter">
      <div class="fline">
        <input id="q" type="search" placeholder="Filter {TOTAL} links — try lora, karpathy, tokenizer, free gpu" aria-label="Filter the list" autocomplete="off">
        <span class="fcount" id="count">{TOTAL} shown</span>
        <button class="fclear" id="clear" type="button" hidden>Clear</button>
      </div>
      <div class="chips" id="chips">
        {chips}
      </div>
    </div>

{sections}

    <div class="tail">
      Nothing on this page is hosted here and nothing has been copied from it: every row links
      to its source, and the one-line notes are ours. Licences belong to the original authors —
      several items are Apache-2.0, MIT or CC BY-NC-SA, and that is stated where it matters.<br><br>
      Found something dead, or something missing that should be here?
      <a href="mailto:ssanelabs@gmail.com?subject=learn%20—%20a%20broken%20or%20missing%20link">Tell us</a>.<br>
      Sane Labs · {TODAY[:4]} · <a href="/">the lab</a> · <a href="/synth-2/">Synth-2</a>
      <br><a class="totop" href="#top">↑ Back to top</a>
    </div>
  </main>
</div>

<script>
(function(){{
  var q=document.getElementById('q'),chips=document.getElementById('chips'),
      count=document.getElementById('count'),clear=document.getElementById('clear'),
      rows=Array.prototype.slice.call(document.querySelectorAll('.row')),
      secs=Array.prototype.slice.call(document.querySelectorAll('section[data-sec]')),
      kinds={{}};

  function apply(){{
    var term=q.value.trim().toLowerCase(),
        words=term?term.split(/\\s+/):[],
        active=Object.keys(kinds).filter(function(k){{return kinds[k];}}),
        shown=0;

    rows.forEach(function(r){{
      var hit=(!active.length||active.indexOf(r.dataset.k)>-1);
      if(hit&&words.length){{
        var s=r.dataset.s;
        for(var i=0;i<words.length;i++){{ if(s.indexOf(words[i])<0){{hit=false;break;}} }}
      }}
      r.hidden=!hit;
      if(hit)shown++;
    }});

    secs.forEach(function(s){{
      var n=s.querySelectorAll('.row:not([hidden])').length;
      s.hidden=(n===0&&(words.length||active.length));
      var tally=s.querySelector('[data-count]');
      if(tally)tally.textContent=n;
      var empty=s.querySelector('.empty');
      if(empty)empty.hidden=true;
    }});

    count.textContent=shown+(shown===1?' link':' links')+' shown';
    clear.hidden=!(words.length||active.length);
  }}

  q.addEventListener('input',apply);
  chips.addEventListener('click',function(ev){{
    var b=ev.target.closest('.chip'); if(!b)return;
    var k=b.dataset.kind;
    kinds[k]=!kinds[k];
    b.classList.toggle('on',kinds[k]);
    apply();
  }});
  clear.addEventListener('click',function(){{
    q.value='';
    Object.keys(kinds).forEach(function(k){{kinds[k]=false;}});
    chips.querySelectorAll('.chip').forEach(function(b){{b.classList.remove('on');}});
    apply(); q.focus();
  }});
  q.addEventListener('keydown',function(ev){{ if(ev.key==='Escape'){{clear.click();}} }});

  /* mark the section the reader is in, in the rail */
  var links={{}};
  document.querySelectorAll('.rail nav a').forEach(function(a){{
    links[a.getAttribute('href').slice(1)]=a;
  }});
  if('IntersectionObserver' in window){{
    var io=new IntersectionObserver(function(entries){{
      entries.forEach(function(en){{
        var a=links[en.target.id];
        if(!a)return;
        if(en.isIntersecting){{
          Object.keys(links).forEach(function(k){{links[k].classList.remove('on');}});
          a.classList.add('on');
        }}
      }});
    }},{{rootMargin:'-10% 0px -80% 0px'}});
    secs.forEach(function(s){{io.observe(s);}});
  }}
}})();
</script>
<script src="/beacon.js" defer></script>
</body>
</html>
'''

os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
open(OUT, "w", encoding="utf-8").write(PAGE)
print(f"wrote {OUT}  ({len(PAGE)//1024} KB, {TOTAL} links, {NCATS} sections)")
