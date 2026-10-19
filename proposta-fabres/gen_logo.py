"""Gera o logo Fabres Auto Detail (SVG) com arcos orbitais da boina."""
import math, sys

CX, CY, RX, RY, ROT = 350, 158, 312, 124, -9  # elipse da órbita


def pt(theta_deg, scale, off=0.0):
    t = math.radians(theta_deg)
    x = (RX * scale + off) * math.cos(t)
    y = (RY * scale + off) * math.sin(t)
    r = math.radians(ROT)
    return CX + x * math.cos(r) - y * math.sin(r), CY + x * math.sin(r) + y * math.cos(r)


def arc(t0, t1, scale, w, skew=0.5, n=90):
    """Faixa curva que engrossa no meio e afina nas pontas (pincelada)."""
    outer, inner = [], []
    for i in range(n + 1):
        u = i / n
        th = t0 + (t1 - t0) * u
        # perfil assimétrico: pico em 'skew'
        k = math.sin(math.pi * (u ** (math.log(0.5) / math.log(skew))))
        outer.append(pt(th, scale, w * k / 2))
        inner.append(pt(th, scale, -w * k / 2))
    pts = outer + inner[::-1]
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z"


def endpoint(t, scale):
    return pt(t, scale)


VARIANTS = {
    # nome: (cor texto topo, texto base, prata ini, prata fim, vermelho, fundo p/ recorte, sub)
    "light": dict(t1="#FFFFFF", t2="#B9C0C7", s1="#3A4048", s2="#FFFFFF", red="#E3262B", red2="#8E1216", bg="#0B0D10", sub="#C9CED3", spark="#FFFFFF"),
    "dark": dict(t1="#0B0D10", t2="#2E353D", s1="#C9CED3", s2="#4A525B", red="#E3262B", red2="#E3262B", bg="#FFFFFF", sub="#4A525B", spark="#0B0D10"),
    "mono": dict(t1="#FFFFFF", t2="#FFFFFF", s1="#FFFFFF", s2="#FFFFFF", red="#0B0D10", red2="#0B0D10", bg="#E3262B", sub="#FFFFFF", spark="#FFFFFF"),
}


def logo_symbol(name, v, uid="0"):
    g = f"lg-{name}-{uid}"
    sx0, sy0 = endpoint(185, 1.0)
    sx1, sy1 = endpoint(325, 1.0)
    bx0, by0 = endpoint(165, 0.94)
    bx1, by1 = endpoint(20, 0.94)
    spx, spy = endpoint(331, 1.0)
    return f'''
    <svg viewBox="0 0 700 320" width="100%" style="display:block;overflow:visible">
      <linearGradient id="{g}-sil" gradientUnits="userSpaceOnUse" x1="{sx0:.0f}" y1="{sy0:.0f}" x2="{sx1:.0f}" y2="{sy1:.0f}">
        <stop offset="0" stop-color="{v['s1']}"/><stop offset=".55" stop-color="{v['s2']}" stop-opacity=".85"/><stop offset="1" stop-color="{v['s2']}"/>
      </linearGradient>
      <linearGradient id="{g}-silb" gradientUnits="userSpaceOnUse" x1="{bx0:.0f}" y1="{by0:.0f}" x2="{bx1:.0f}" y2="{by1:.0f}">
        <stop offset="0" stop-color="{v['s2']}"/><stop offset="1" stop-color="{v['s1']}"/>
      </linearGradient>
      <linearGradient id="{g}-red" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0" stop-color="{v['red2']}"/><stop offset=".6" stop-color="{v['red']}"/><stop offset="1" stop-color="{v['red']}"/>
      </linearGradient>
      <!-- órbita da boina: arcos de cima (antes = fosco → depois = brilho) -->
      <path d="{arc(182, 326, 1.0, 17, 0.62)}" fill="url(#{g}-sil)"/>
      <path d="{arc(206, 338, 0.86, 22, 0.55)}" fill="url(#{g}-red)"/>
      <!-- arcos de baixo -->
      <path d="{arc(84, 174, 0.95, 18, 0.35)}" fill="url(#{g}-silb)"/>
      <path d="{arc(94, 160, 0.81, 13, 0.4)}" fill="url(#{g}-red)"/>
      <!-- brilho revelado no fim do traço -->
      <use href="#spark" x="{spx-26:.0f}" y="{spy-34:.0f}" width="52" height="52" fill="{v['spark']}"/>
      <use href="#spark" x="{spx+14:.0f}" y="{spy+6:.0f}" width="18" height="18" fill="{v['spark']}" opacity=".75"/>
      <!-- nome: contorno na cor do fundo faz os arcos passarem por trás -->
      <clipPath id="{g}-low"><rect x="0" y="150" width="700" height="60"/></clipPath>
      <text x="343" y="196" text-anchor="middle" font-family="Inter Display, Inter" font-weight="900" font-style="italic" font-size="128" letter-spacing="-2"
            fill="{v['bg']}" stroke="{v['bg']}" stroke-width="13" stroke-linejoin="round">FABRES</text>
      <text x="343" y="196" text-anchor="middle" font-family="Inter Display, Inter" font-weight="900" font-style="italic" font-size="128" letter-spacing="-2" fill="{v['t1']}">FABRES</text>
      <text x="343" y="196" text-anchor="middle" font-family="Inter Display, Inter" font-weight="900" font-style="italic" font-size="128" letter-spacing="-2" fill="{v['t2']}" clip-path="url(#{g}-low)">FABRES</text>
      <text x="604" y="229" text-anchor="end" font-family="Inter" font-weight="700" font-style="italic" font-size="25" letter-spacing="11"
            fill="{v['bg']}" stroke="{v['bg']}" stroke-width="9" stroke-linejoin="round">AUTO DETAIL</text>
      <text x="604" y="229" text-anchor="end" font-family="Inter" font-weight="700" font-style="italic" font-size="25" letter-spacing="11" fill="{v['sub']}">AUTO DETAIL</text>
    </svg>'''


def avatar(uid="a"):
    # órbita própria, centrada em 100,100
    global CX, CY, RX, RY, ROT
    saved = (CX, CY, RX, RY, ROT)
    CX, CY, RX, RY, ROT = 100, 102, 78, 52, -12
    a1 = arc(185, 330, 1.0, 9, 0.62)
    a2 = arc(198, 340, 0.84, 11, 0.55)
    a3 = arc(18, 168, 0.96, 9, 0.45)
    a4 = arc(34, 150, 0.8, 7, 0.5)
    spx, spy = pt(334, 1.0)
    CX, CY, RX, RY, ROT = saved
    return f'''
    <svg viewBox="0 0 200 200" width="100%" height="100%" style="display:block">
      <linearGradient id="av-sil-{uid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#3A4048"/><stop offset="1" stop-color="#FFFFFF"/></linearGradient>
      <circle cx="100" cy="100" r="98" fill="#0B0D10"/>
      <path d="{a1}" fill="url(#av-sil-{uid})"/>
      <path d="{a2}" fill="#E3262B"/>
      <path d="{a3}" fill="#9AA3AC"/>
      <path d="{a4}" fill="#E3262B"/>
      <use href="#spark" x="{spx-14:.0f}" y="{spy-18:.0f}" width="26" height="26" fill="#FFF"/>
      <clipPath id="av-low-{uid}"><rect x="0" y="100" width="200" height="40"/></clipPath>
      <text x="98" y="125" text-anchor="middle" font-family="Inter Display, Inter" font-weight="900" font-style="italic" font-size="70" letter-spacing="-3" fill="#0B0D10" stroke="#0B0D10" stroke-width="8" stroke-linejoin="round">FD</text>
      <text x="98" y="125" text-anchor="middle" font-family="Inter Display, Inter" font-weight="900" font-style="italic" font-size="70" letter-spacing="-3" fill="#FFFFFF">FD</text>
      <text x="98" y="125" text-anchor="middle" font-family="Inter Display, Inter" font-weight="900" font-style="italic" font-size="70" letter-spacing="-3" fill="#B9C0C7" clip-path="url(#av-low-{uid})">FD</text>
    </svg>'''


SPARK = '<symbol id="spark" viewBox="-10 -10 20 20"><path d="M0-10 C1-2 2-1 10 0 C2 1 1 2 0 10 C-1 2 -2 1 -10 0 C-2 -1 -1 -2 0-10Z"/></symbol>'


def defs():
    body = SPARK + "".join(logo_symbol(k, v) for k, v in VARIANTS.items()) + avatar()
    return f'<svg width="0" height="0" style="position:absolute"><defs>{body}\n</defs></svg>'


if __name__ == "__main__":
    out = sys.argv[1]
    html = open(out).read()
    a, b = "<!-- LOGO-START -->", "<!-- LOGO-END -->"
    i, j = html.index(a) + len(a), html.index(b)
    html = html[:i] + "\n" + f'<svg width="0" height="0" style="position:absolute"><defs>{SPARK}</defs></svg>' + "\n" + html[j:]
    import re, itertools
    c = itertools.count()
    html = re.sub(r'<svg viewBox="0 0 700 320"[^>]*><use href="#logo-(\w+)"/></svg>', lambda m: logo_symbol(m.group(1), VARIANTS[m.group(1)], str(next(c))), html)
    html = re.sub(r'<svg viewBox="0 0 200 200"[^>]*><use href="#avatar"/></svg>', lambda m: '<div style="'+'width:100%;aspect-ratio:1">'+avatar(str(next(c)))+'</div>', html)
    open(out.replace(".html", ".build.html"), "w").write(html)
    if len(sys.argv) > 2:  # exporta logos avulsos
        d = sys.argv[2]
        bgs = {"light": "#0B0D10", "dark": "#FFFFFF", "mono": "#E3262B"}
        for k, v in VARIANTS.items():
            open(f"{d}/logo-{k}.svg", "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="-40 -30 780 380"><rect x="-40" y="-30" width="780" height="380" fill="{bgs[k]}"/><defs>{SPARK}</defs>' + logo_symbol(k, v, "x").replace('<svg viewBox="0 0 700 320" width="100%" style="display:block;overflow:visible">', '<g>').replace("</svg>", "</g>") + "</svg>")
        open(f"{d}/avatar.svg", "w").write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200"><defs>' + SPARK + "</defs>" + avatar("x").replace('<svg viewBox="0 0 200 200" width="100%" height="100%" style="display:block">', "<g>").replace("</svg>", "</g>") + "</svg>")
