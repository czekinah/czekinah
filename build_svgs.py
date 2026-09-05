#!/usr/bin/env python3
"""Generate the animated SVG set for github.com/czekinah in both render modes.

Palettes are lifted straight from czekinah.github.io CSS variables.
Every SVG is self contained (inline <style>, no external fonts) so it
animates when GitHub serves it through an <img> tag.
"""
import os, html

OUT = os.path.join(os.path.dirname(__file__), "assets")
os.makedirs(OUT, exist_ok=True)

MONO = "'JetBrains Mono','Fira Code','Cascadia Code','SFMono-Regular',Consolas,'Courier New',monospace"

THEMES = {
    "dark": dict(  # engineer render mode
        bg="#0A1120", bg_alt="#0B142A", bg_soft="#0D1830", card="#101B33",
        line="#1D2C4D", ink="#E9F1FF", ink_soft="#8FA3C7", accent="#2BE3DF",
        accent_deep="#2BE3DF", pop="#5DFF87", third="#4A82FF", on_accent="#062326",
        shadow="#03282D", comment="#5DFF87", mode="data-engineer", prompt_user="czekinah@purrfolio",
        display=MONO, body="'IBM Plex Sans','Segoe UI',Arial,sans-serif",
        radius=10, blob=False,
    ),
    "light": dict(  # writer render mode
        bg="#FFFAF0", bg_alt="#F3ECFF", bg_soft="#FFEDF6", card="#FFFFFF",
        line="#F2D3E3", ink="#43223B", ink_soft="#82627B", accent="#FF69B4",
        accent_deep="#D81B7F", pop="#FFC61A", third="#A98BFF", on_accent="#FFFFFF",
        shadow="#FFC9E2", comment="#D81B7F", mode="creative-writer", prompt_user="czekinah@purrfolio",
        display="Fraunces,Georgia,'Times New Roman',serif",
        body="'Baloo 2','Trebuchet MS','Segoe UI',sans-serif",
        radius=18, blob=True,
    ),
}

def esc(s):
    return html.escape(s, quote=False)

def svg(w, h, body, style, t, title):
    # per-item animation-delay rules must come AFTER the shorthand `animation:` rules,
    # otherwise the shorthand resets the delay to 0 and every stagger is lost.
    lines = style.splitlines()
    generic = [l for l in lines if "animation-delay" not in l]
    delays = [l for l in lines if "animation-delay" in l]
    style = "\n".join(generic + delays)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-labelledby="t">
<title id="t">{esc(title)}</title>
<style>
  text {{ font-family: {t['body']}; }}
  .mono {{ font-family: {MONO}; }}
  .disp {{ font-family: {t['display']}; }}
  {style}
</style>
{body}
</svg>
"""

def card_rect(t, x, y, w, h, extra=""):
    if t["blob"]:
        # slightly wonky corners like the portfolio's --r-a
        return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{t["radius"]}" ry="{t["radius"]+6}" fill="{t["card"]}" stroke="{t["line"]}" stroke-width="2" {extra}/>'
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{t["radius"]}" fill="{t["card"]}" stroke="{t["line"]}" stroke-width="1.5" {extra}/>'

def paw(x, y, s, fill, cls=""):
    # simple paw print: one pad + three toes
    return (f'<g class="{cls}" transform="translate({x},{y}) scale({s})" fill="{fill}">'
            f'<ellipse cx="0" cy="6" rx="7" ry="5.5"/>'
            f'<circle cx="-7" cy="-2" r="2.8"/><circle cx="0" cy="-5" r="2.8"/><circle cx="7" cy="-2" r="2.8"/></g>')

def cat(t, x, y, scale=1.0):
    """Pixel-ish cat, tail wags, ears twitch, eyes blink."""
    ink, acc, pop = t["ink"], t["accent"], t["pop"]
    body_fill = t["ink"] if t["blob"] else t["accent"]
    face = t["bg"] if not t["blob"] else t["bg"]
    return f"""
<g transform="translate({x},{y}) scale({scale})">
  <g class="tail" transform="translate(-34,26)">
    <path d="M0 0 C -22 -6, -30 -30, -8 -40" fill="none" stroke="{body_fill}" stroke-width="7" stroke-linecap="round"/>
  </g>
  <rect x="-30" y="0" width="60" height="44" rx="14" fill="{body_fill}"/>
  <g class="head">
    <rect x="-26" y="-34" width="52" height="42" rx="12" fill="{body_fill}"/>
    <polygon class="ear" points="-24,-30 -24,-48 -8,-34" fill="{body_fill}"/>
    <polygon class="ear ear2" points="24,-30 24,-48 8,-34" fill="{body_fill}"/>
    <g class="eyes">
      <rect x="-15" y="-20" width="7" height="8" rx="2" fill="{face}"/>
      <rect x="8" y="-20" width="7" height="8" rx="2" fill="{face}"/>
    </g>
    <path d="M-3 -8 L3 -8 L0 -4 Z" fill="{pop}"/>
    <path d="M-9 -3 Q-4 1 0 -3 Q4 1 9 -3" fill="none" stroke="{face}" stroke-width="1.8" stroke-linecap="round"/>
    <g stroke="{t['ink_soft']}" stroke-width="1.4" stroke-linecap="round">
      <line x1="-34" y1="-8" x2="-22" y2="-7"/><line x1="-34" y1="-2" x2="-22" y2="-4"/>
      <line x1="34" y1="-8" x2="22" y2="-7"/><line x1="34" y1="-2" x2="22" y2="-4"/>
    </g>
  </g>
  <rect x="-24" y="38" width="14" height="10" rx="4" fill="{body_fill}"/>
  <rect x="10" y="38" width="14" height="10" rx="4" fill="{body_fill}"/>
</g>"""

CAT_CSS = """
  .tail { transform-origin: 0px 0px; animation: wag 1.6s ease-in-out infinite; }
  @keyframes wag { 0%,100% { transform: translate(-34px,26px) rotate(-8deg);} 50% { transform: translate(-34px,26px) rotate(14deg);} }
  .eyes { animation: blink 4.5s infinite; transform-origin: center; }
  @keyframes blink { 0%,92%,100% { transform: scaleY(1);} 95% { transform: scaleY(0.1);} }
  .ear2 { transform-origin: 24px -30px; animation: twitch 5s infinite; }
  @keyframes twitch { 0%,88%,100% { transform: rotate(0);} 91% { transform: rotate(-14deg);} 94% { transform: rotate(0);} }
"""

# ----------------------------------------------------------------------------
def hero(t, name):
    W, H = 900, 270
    typed = "SELECT * FROM czekinah;"
    n = len(typed)
    ch = 13.2  # approx mono char width at 22px
    typed_w = int(n * ch) + 6
    # background decoration
    deco = ""
    if t["blob"]:
        deco += f'<ellipse cx="760" cy="40" rx="150" ry="90" fill="{t["bg_soft"]}"/>'
        deco += f'<ellipse cx="120" cy="250" rx="180" ry="70" fill="{t["bg_alt"]}"/>'
        deco += f'<circle class="fl fl1" cx="640" cy="200" r="7" fill="{t["pop"]}"/>'
        deco += f'<circle class="fl fl2" cx="820" cy="150" r="5" fill="{t["third"]}"/>'
        deco += paw(690, 60, 0.9, t["accent"], "fl fl3")
        deco += paw(850, 230, 0.7, t["third"], "fl fl1")
    else:
        deco += f'<defs><pattern id="grid" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="{t["line"]}"/></pattern></defs>'
        deco += f'<rect width="{W}" height="{H}" fill="url(#grid)"/>'
        deco += f'<rect class="scan" x="0" y="0" width="{W}" height="2" fill="{t["accent"]}" opacity="0.12"/>'
        deco += f'<circle class="fl fl1" cx="640" cy="200" r="4" fill="{t["pop"]}"/>'
        deco += f'<circle class="fl fl2" cx="820" cy="150" r="3" fill="{t["third"]}"/>'
        deco += paw(690, 60, 0.9, t["accent"], "fl fl3")
        deco += paw(850, 230, 0.7, t["third"], "fl fl1")

    chip = f'render_mode: {t["mode"]}'
    chip_w = len(chip) * 8.2 + 26
    body = f"""
<rect width="{W}" height="{H}" rx="{t['radius']+4}" fill="{t['bg']}"/>
{deco}
<rect x="{W-chip_w-22}" y="22" width="{chip_w}" height="26" rx="13" fill="{t['accent']}"/>
<text x="{W-chip_w-22+13}" y="39" class="mono" font-size="12.5" fill="{t['on_accent']}" font-weight="700">{esc(chip)}</text>

<text x="40" y="52" class="mono" font-size="14" fill="{t['ink_soft']}">~/czekinah/purr-folio $ whoami</text>
<text x="40" y="104" class="disp name" font-size="46" font-weight="800" fill="{t['ink']}">{esc(name)}</text>

<g transform="translate(40,140)">
  <text x="0" y="0" class="mono" font-size="22" fill="{t['accent_deep']}" font-weight="700" clip-path="url(#typeclip)">{esc(typed)}</text>
  <clipPath id="typeclip"><rect class="typer" x="0" y="-22" width="0" height="30"/></clipPath>
  <rect class="caret" x="0" y="-19" width="11" height="24" fill="{t['accent_deep']}"/>
</g>

<text x="40" y="190" class="sub" font-size="17" fill="{t['ink']}">One life, two render modes:</text>
<text x="40" y="214" class="sub" font-size="17" fill="{t['ink']}">creative writer <tspan fill="{t['ink_soft']}">&amp;</tspan> data engineer in training.</text>
<text x="40" y="246" class="mono sub2" font-size="12.5" fill="{t['ink_soft']}">// psst. I also speak SQL.  //  7+ yrs copy  ·  FTW Batch 12  ·  AWS re/Start  ·  45 DataCamp courses</text>

{cat(t, 760, 150, 1.25)}
"""
    style = CAT_CSS + f"""
  .typer {{ animation: typing 2.2s steps({n}, end) 0.6s forwards; }}
  @keyframes typing {{ from {{ width: 0; }} to {{ width: {typed_w}px; }} }}
  .caret {{ animation: caretmove 2.2s steps({n}, end) 0.6s forwards, caretblink 0.9s step-end infinite; }}
  @keyframes caretmove {{ from {{ transform: translateX(0); }} to {{ transform: translateX({typed_w}px); }} }}
  @keyframes caretblink {{ 50% {{ opacity: 0; }} }}
  .sub {{ opacity: 0; animation: rise 0.7s ease-out 2.9s forwards; }}
  .sub2 {{ opacity: 0; animation: rise 0.7s ease-out 3.4s forwards; }}
  @keyframes rise {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: translateY(0); }} }}
  .name {{ animation: rise 0.6s ease-out 0.1s both; }}
  .fl {{ animation: floaty 4s ease-in-out infinite; }}
  .fl2 {{ animation-delay: -1.3s; }} .fl3 {{ animation-delay: -2.4s; }}
  @keyframes floaty {{ 0%,100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-10px); }} }}
  .scan {{ animation: scan 6s linear infinite; }}
  @keyframes scan {{ from {{ transform: translateY(0); }} to {{ transform: translateY({H}px); }} }}
"""
    return svg(W, H, body, style, t, f"{name}. One life, two render modes.")

# ----------------------------------------------------------------------------
def receipts(t):
    W, H = 900, 210
    items = [("291%", "sales growth", "on my best campaign", 0.92),
             ("884%", "reach vs. KPI", "overdelivered", 1.0),
             ("#1", "Google rankings", "from search ad copy", 0.78),
             ("7+", "years", "agencies + B2B SaaS", 0.66)]
    cw, gap, x0, y0 = 198, 16, 40, 58
    body = f'<rect width="{W}" height="{H}" rx="{t["radius"]+4}" fill="{t["bg"]}"/>'
    body += f'<text x="40" y="34" class="mono" font-size="14" fill="{t["ink_soft"]}">$ psql -c "SELECT metric, value FROM writer_era WHERE brag = TRUE;"  <tspan fill="{t["comment"]}">-- the receipts</tspan></text>'
    style = ""
    for i, (big, lab, note, pct) in enumerate(items):
        x = x0 + i * (cw + gap)
        body += card_rect(t, x, y0, cw, 128)
        body += f'<text class="num n{i} disp" x="{x+18}" y="{y0+52}" font-size="38" font-weight="800" fill="{t["accent_deep"]}" style="font-family:{t["display"]}">{esc(big)}</text>'
        body += f'<text x="{x+18}" y="{y0+76}" font-size="14" font-weight="600" fill="{t["ink"]}">{esc(lab)}</text>'
        body += f'<text x="{x+18}" y="{y0+94}" class="mono" font-size="11.5" fill="{t["ink_soft"]}">{esc(note)}</text>'
        body += f'<rect x="{x+18}" y="{y0+108}" width="{cw-36}" height="7" rx="3.5" fill="{t["line"]}"/>'
        body += f'<rect class="bar b{i}" x="{x+18}" y="{y0+108}" width="{int((cw-36)*pct)}" height="7" rx="3.5" fill="{t["accent"]}"/>'
        style += f"  .b{i} {{ animation-delay: {0.3 + i*0.25:.2f}s; }} .n{i} {{ animation-delay: {0.5 + i*0.25:.2f}s; }}\n"
    body += f'<text x="40" y="{H-12}" class="mono" font-size="12" fill="{t["ink_soft"]}">(4 rows)  -- proof that I have been optimizing for metrics all along</text>'
    style += f"""
  .bar {{ transform-origin: left center; transform: scaleX(0); animation: grow 1.1s cubic-bezier(.2,.8,.2,1) forwards; }}
  @keyframes grow {{ to {{ transform: scaleX(1); }} }}
  .num {{ opacity: 0; animation: pop 0.6s ease-out forwards; }}
  @keyframes pop {{ 0% {{ opacity: 0; transform: translateY(10px); }} 70% {{ transform: translateY(-3px); }} 100% {{ opacity: 1; transform: translateY(0); }} }}
"""
    return svg(W, H, body, style, t, "The receipts: 291% sales growth, 884% reach vs KPI, #1 Google rankings, 7+ years.")

# ----------------------------------------------------------------------------
def skills(t):
    W, H = 900, 250
    tiles = [("Copywriting", "TVC, social, print, scripts", "w"),
             ("SQL", "joins, windows, modeling", "d"),
             ("Brand voice", "finding it, then keeping it", "w"),
             ("Python", "pandas, scripts, tools", "d"),
             ("SEO & search", "copy that ranks + clicks", "w"),
             ("Databricks", "lakehouse, Spark SQL, ETL", "d"),
             ("Content strategy", "calendars, series, funnels", "w"),
             ("AWS Cloud", "re/Start scholar, hands-on", "d")]
    awake = "d" if not t["blob"] else "w"   # engineer mode wakes data tiles first
    cw, chh, gap, x0, y0 = 198, 78, 16, 40, 56
    body = f'<rect width="{W}" height="{H}" rx="{t["radius"]+4}" fill="{t["bg"]}"/>'
    body += f'<text x="40" y="34" class="mono" font-size="14" fill="{t["ink_soft"]}">$ ls skills/ --sort=passion   <tspan fill="{t["comment"]}">// dimmed tiles are not gone. they are napping.</tspan></text>'
    style = ""
    for i, (name, sub, kind) in enumerate(tiles):
        r, c = divmod(i, 4)
        x, y = x0 + c * (cw + gap), y0 + r * (chh + gap)
        first = (kind == awake)
        delay = (0.2 + (i // 2) * 0.35) if first else (1.8 + (i // 2) * 0.35)
        body += f'<g class="tile t{i}">'
        body += card_rect(t, x, y, cw, chh)
        body += f'<rect x="{x}" y="{y+chh-6}" width="{cw}" height="6" rx="3" fill="{t["accent"] if first else t["third"]}"/>'
        body += f'<text x="{x+16}" y="{y+32}" font-size="16" font-weight="700" fill="{t["ink"]}">{esc(name)}</text>'
        body += f'<text x="{x+16}" y="{y+54}" class="mono" font-size="10.2" fill="{t["ink_soft"]}">{esc(sub)}</text>'
        body += f'<text class="zz z{i} mono" x="{x+cw-40}" y="{y+26}" font-size="13" fill="{t["ink_soft"]}" style="font-family:{MONO}">zzz</text>'
        body += '</g>'
        style += f"  .t{i} {{ animation-delay: {delay:.2f}s; }} .z{i} {{ animation-delay: {delay:.2f}s; }}\n"
    style += """
  .tile { opacity: 0.35; animation: wake 0.8s ease-out forwards; }
  @keyframes wake { to { opacity: 1; } }
  .zz { animation: zzz 0.8s ease-out forwards; }
  @keyframes zzz { to { opacity: 0; transform: translateY(-10px); } }
"""
    return svg(W, H, body, style, t, "Skills: copywriting, SQL, brand voice, Python, SEO, Databricks, content strategy, AWS.")

# ----------------------------------------------------------------------------
def gitlog(t):
    W, H = 900, 262
    commits = [("f00dcat", "(HEAD -> data-engineering)", "feat: FTW Foundation Batch 12 + AWS re/Start Batch 29"),
               ("ac1dbee", "", "learn: 45 DataCamp courses and counting"),
               ("c0ffee7", "", "refactor: campaigns/ -> pipelines/ (breaking change, worth it)"),
               ("b1gp1v0", "", "fix: stop calling it a career change, call it a schema migration"),
               ("7yrs4go", "", "init: seven years of agency + B2B SaaS copywriting")]
    body = f'<rect width="{W}" height="{H}" rx="{t["radius"]+4}" fill="{t["bg"]}"/>'
    body += f'<text x="40" y="34" class="mono" font-size="14" fill="{t["ink_soft"]}">$ git log --oneline careers/czekinah   <tspan fill="{t["comment"]}">// the plot twist, rendered as a commit history</tspan></text>'
    y0, step, lx = 70, 36, 56
    body += f'<line class="trunk" x1="{lx}" y1="{y0}" x2="{lx}" y2="{y0+step*(len(commits)-1)}" stroke="{t["line"]}" stroke-width="3"/>'
    style = ""
    for i, (h, ref, msg) in enumerate(commits):
        y = y0 + i * step
        d = 0.3 + i * 0.45
        body += f'<circle class="dot d{i}" cx="{lx}" cy="{y}" r="7" fill="{t["accent"] if i == 0 else t["card"]}" stroke="{t["accent"]}" stroke-width="3"/>'
        body += f'<g class="row r{i}">'
        body += f'<text x="{lx+24}" y="{y+5}" class="mono" font-size="14" font-weight="700" fill="{t["comment"]}">{esc(h)}</text>'
        xx = lx + 24 + 76
        if ref:
            body += f'<text x="{xx}" y="{y+5}" class="mono" font-size="13" fill="{t["accent_deep"]}">{esc(ref)}</text>'
            xx += len(ref) * 8 + 10
        body += f'<text x="{xx}" y="{y+5}" class="mono" font-size="14" fill="{t["ink"]}">{esc(msg)}</text>'
        body += '</g>'
        style += f"  .d{i} {{ animation-delay: {d:.2f}s; }} .r{i} {{ animation-delay: {d+0.1:.2f}s; }}\n"
    body += f'<text x="40" y="{H-14}" class="mono" font-size="12" fill="{t["ink_soft"]}">// same curiosity. stricter syntax.</text>'
    style += """
  .dot { transform-box: fill-box; transform-origin: center; transform: scale(0); animation: bump 0.5s cubic-bezier(.3,1.6,.5,1) forwards; }
  @keyframes bump { to { transform: scale(1); } }
  .row { opacity: 0; animation: slide 0.5s ease-out forwards; }
  @keyframes slide { from { opacity: 0; transform: translateX(-10px);} to { opacity: 1; transform: translateX(0);} }
  .trunk { stroke-dasharray: 400; stroke-dashoffset: 400; animation: draw 2.4s ease-out 0.3s forwards; }
  @keyframes draw { to { stroke-dashoffset: 0; } }
"""
    return svg(W, H, body, style, t, "git log: from copywriting to data engineering, rendered as a commit history.")

# ----------------------------------------------------------------------------
def catalytics(t):
    W, H = 900, 242
    rows = [("coffee_today", "3.5 cups", 0.7), ("words_written", "2,400", 0.8), ("queries_run", "17", 0.34),
            ("purr_level", "58%", 0.58), ("datacamp_courses", "45", 0.9), ("cats_petted", "∞", 1.0)]
    body = f'<rect width="{W}" height="{H}" rx="{t["radius"]+4}" fill="{t["bg"]}"/>'
    body += card_rect(t, 40, 20, W-80, H-40)
    body += f'<circle class="led" cx="64" cy="44" r="5" fill="{t["comment"]}"/>'
    body += f'<text x="78" y="49" class="mono" font-size="14" font-weight="700" fill="{t["ink"]}">cat_alytics --live</text>'
    body += f'<text x="{W-56}" y="49" text-anchor="end" class="mono" font-size="12" fill="{t["ink_soft"]}">$ tail -f cat_metrics.log</text>'
    style = ""
    y0, step = 78, 24
    lx, bx, bw = 64, 250, 520
    for i, (k, v, pct) in enumerate(rows):
        y = y0 + i * step
        body += f'<text x="{lx}" y="{y+5}" class="mono" font-size="13" fill="{t["ink_soft"]}">{esc(k)}</text>'
        body += f'<rect x="{bx}" y="{y-6}" width="{bw}" height="12" rx="6" fill="{t["line"]}"/>'
        body += f'<rect class="bar b{i}" x="{bx}" y="{y-6}" width="{int(bw*pct)}" height="12" rx="6" fill="{t["accent"] if i % 2 == 0 else t["third"]}"/>'
        body += f'<text class="val v{i} mono" x="{bx+bw+16}" y="{y+5}" font-size="13" font-weight="700" fill="{t["ink"]}" style="font-family:{MONO}">{esc(v)}</text>'
        style += f"  .b{i} {{ animation-delay: {0.2+i*0.18:.2f}s; }} .v{i} {{ animation-delay: {0.6+i*0.18:.2f}s; }}\n"
    style += """
  .bar { transform-origin: left center; transform: scaleX(0); animation: grow 1s cubic-bezier(.2,.8,.2,1) forwards, breathe 3s ease-in-out 2s infinite; }
  @keyframes grow { to { transform: scaleX(1); } }
  @keyframes breathe { 0%,100% { opacity: 1; } 50% { opacity: 0.72; } }
  .val { opacity: 0; animation: fin 0.5s ease-out forwards; }
  @keyframes fin { to { opacity: 1; } }
  .led { animation: led 1.2s step-end infinite; }
  @keyframes led { 50% { opacity: 0.25; } }
"""
    return svg(W, H, body, style, t, "Cat-alytics: a very serious dashboard of very serious numbers.")

# ----------------------------------------------------------------------------
def divider(t):
    W, H = 900, 44
    body = f'<rect width="{W}" height="{H}" fill="none"/>'
    style = ""
    n = 9
    for i in range(n):
        x = 60 + i * 97
        y = 24 + (6 if i % 2 else -4)
        body += paw(x, y, 0.85, t["accent"] if i % 2 == 0 else t["third"], f"p p{i}")
        style += f"  .p{i} {{ animation-delay: {i*0.45:.2f}s; }}\n"
    style += """
  .p { opacity: 0; animation: step 6s ease-in-out infinite; }
  @keyframes step { 0% { opacity: 0; } 6% { opacity: 1; } 55% { opacity: 1; } 68% { opacity: 0; } 100% { opacity: 0; } }
"""
    return svg(W, H, body, style, t, "paw prints")

# ----------------------------------------------------------------------------
def footer(t):
    W, H = 900, 64
    line = "Czekinah Tolentino  //  one life, two render modes  //  uptime: 7 years and counting  //  powered by strawberry milkshake  //  "
    body = f'<rect width="{W}" height="{H}" rx="{t["radius"]+4}" fill="{t["bg"]}"/>'
    body += f'<clipPath id="fc"><rect x="0" y="0" width="{W}" height="{H}"/></clipPath>'
    body += f'<g clip-path="url(#fc)"><g class="marq">'
    body += f'<text x="0" y="39" class="mono" font-size="14" fill="{t["ink_soft"]}">{esc(line)}<tspan fill="{t["accent"]}">{esc(line)}</tspan></text>'
    body += '</g></g>'
    style = """
  .marq { animation: slide 22s linear infinite; }
  @keyframes slide { from { transform: translateX(0); } to { transform: translateX(-900px); } }
"""
    return svg(W, H, body, style, t, "Czekinah Tolentino. One life, two render modes.")

# ----------------------------------------------------------------------------
builders = {"hero": lambda t: hero(t, "Czekinah Tolentino"), "receipts": receipts, "skills": skills,
            "gitlog": gitlog, "catalytics": catalytics, "divider": divider, "footer": footer}

for mode, t in THEMES.items():
    for name, fn in builders.items():
        p = os.path.join(OUT, f"{name}-{mode}.svg")
        with open(p, "w") as f:
            f.write(fn(t))
        print("wrote", p)
