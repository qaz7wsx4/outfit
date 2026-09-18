#!/usr/bin/env python3
"""依 data/items.json 的 `shape` 與 `colors` 產生扁平風 SVG 插圖到 photos/items/<id>.svg。

用法：python3 tools/make_illustrations.py
新增衣服時在 items.json 加上：
  "shape": "tshirt" | "shirt" | "pants" | "shorts" | "sneaker" | "hightop" | "runner" | "sandal" | "slide" | "flipflop" | "watch"
  "colors": {"main": "#hex", ...}   各版型可用的鍵見下方各函式
"""
import json, os, colorsys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ITEMS = os.path.join(ROOT, "data", "items.json")
OUT = os.path.join(ROOT, "photos", "items")


def darken(hexcolor, f=0.72):
    h = hexcolor.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    hh, ll, ss = colorsys.rgb_to_hls(r, g, b)
    r, g, b = colorsys.hls_to_rgb(hh, max(0, ll * f), ss)
    return "#%02x%02x%02x" % (round(r * 255), round(g * 255), round(b * 255))


def svg(body):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400">'
            '<rect width="400" height="400" fill="#ece9e2"/>'
            f'{body}</svg>')


SW = 'stroke-width="6" stroke-linejoin="round" stroke-linecap="round"'


def tshirt(c):
    m, o = c["main"], darken(c["main"])
    body = (f'<path d="M120,95 L162,72 Q200,100 238,72 L280,95 L332,155 L286,186 L270,166 L270,330 '
            f'L130,330 L130,166 L114,186 L68,155 Z" fill="{m}" stroke="{o}" {SW}/>'
            f'<path d="M162,72 Q200,100 238,72" fill="none" stroke="{o}" {SW}/>')
    g = c.get("graphic")
    if g == "circle-mountain":  # Fjällräven 那件：橘圓＋白山
        body += (f'<circle cx="200" cy="215" r="42" fill="{c.get("accent", "#d97a3a")}"/>'
                 f'<path d="M165,240 L185,205 L200,225 L215,198 L238,240 Z" fill="#f4f2ee"/>')
    elif g == "mountain":  # Smartwool：小白山
        body += f'<path d="M172,200 L190,172 L202,188 L216,166 L234,200 Z" fill="#f4f2ee"/>'
    elif g == "logo":  # 胸口小 logo
        body += f'<rect x="222" y="150" width="30" height="8" rx="4" fill="{c.get("accent", "#f4f2ee")}"/>'
    return svg(body)


def shirt(c):
    m, o = c["main"], darken(c["main"])
    btn = c.get("button", "#f4f2ee")
    body = (f'<path d="M120,95 L166,70 L200,110 L234,70 L280,95 L332,155 L286,186 L270,166 L270,330 '
            f'L130,330 L130,166 L114,186 L68,155 Z" fill="{m}" stroke="{o}" {SW}/>'
            # 領子
            f'<path d="M166,70 L200,110 L186,62 Z" fill="{o}" stroke="{o}" {SW}/>'
            f'<path d="M234,70 L200,110 L214,62 Z" fill="{o}" stroke="{o}" {SW}/>'
            # 門襟＋鈕扣
            f'<line x1="200" y1="110" x2="200" y2="330" stroke="{o}" stroke-width="3"/>'
            + "".join(f'<circle cx="200" cy="{y}" r="5" fill="{btn}"/>' for y in (140, 180, 220, 260, 300))
            # 口袋
            + f'<path d="M132,160 L176,160 L176,205 L154,212 L132,205 Z" fill="none" stroke="{o}" stroke-width="3"/>')
    return svg(body)


def pants(c):
    m, o = c["main"], darken(c["main"])
    fit = c.get("fit", "slim")  # slim | straight | jogger
    # 褲腳寬度
    hem = {"slim": 40, "straight": 58, "jogger": 34}[fit]
    lx0, lx1 = 128, 197
    rx0, rx1 = 203, 272
    lb0, lb1 = lx0 + (lx1 - lx0 - hem) / 2 + 6, lx1 - (lx1 - lx0 - hem) / 2 + 6
    rb0, rb1 = rx0 + (rx1 - rx0 - hem) / 2 - 6, rx1 - (rx1 - rx0 - hem) / 2 - 6
    ybot = 320 if fit == "jogger" else 335
    body = (f'<path d="M{lx0},92 L{lx1},92 L{lx1},175 L{lb1},{ybot} L{lb0},{ybot} Z" fill="{m}" stroke="{o}" {SW}/>'
            f'<path d="M{rx0},92 L{rx1},92 L{rx1},175 L{rb1},{ybot} L{rb0},{ybot} Z" fill="{m}" stroke="{o}" {SW}/>'
            f'<rect x="{lx0}" y="70" width="{rx1 - lx0}" height="24" rx="4" fill="{m}" stroke="{o}" {SW}/>')
    if fit == "jogger":
        body += (f'<rect x="{lb0 - 3}" y="{ybot}" width="{lb1 - lb0 + 6}" height="16" fill="{o}"/>'
                 f'<rect x="{rb0 - 3}" y="{ybot}" width="{rb1 - rb0 + 6}" height="16" fill="{o}"/>'
                 # 抽繩
                 f'<path d="M190,94 L184,118 M210,94 L216,118" stroke="{o}" stroke-width="4" stroke-linecap="round"/>')
    else:
        body += f'<line x1="200" y1="94" x2="200" y2="175" stroke="{o}" stroke-width="3"/>'
    if c.get("belt"):
        body += f'<rect x="178" y="74" width="44" height="16" rx="3" fill="{c["belt"]}"/>'
    return svg(body)


def shorts(c):
    m, o = c["main"], darken(c["main"])
    body = (f'<path d="M118,102 L197,102 L197,175 L192,262 L120,262 Z" fill="{m}" stroke="{o}" {SW}/>'
            f'<path d="M203,102 L282,102 L280,262 L208,262 L203,175 Z" fill="{m}" stroke="{o}" {SW}/>'
            f'<rect x="118" y="80" width="164" height="24" rx="4" fill="{m}" stroke="{o}" {SW}/>')
    if c.get("cargo"):
        body += (f'<rect x="126" y="190" width="44" height="46" rx="4" fill="none" stroke="{o}" stroke-width="3"/>'
                 f'<rect x="230" y="190" width="44" height="46" rx="4" fill="none" stroke="{o}" stroke-width="3"/>')
    if c.get("belt"):
        body += f'<rect x="178" y="84" width="44" height="16" rx="3" fill="{c["belt"]}"/>'
    return svg(body)


def _sole(c, thick=28):
    s, so = c.get("sole", "#f4f2ee"), darken(c.get("sole", "#f4f2ee"), 0.8)
    y = 268
    return (f'<path d="M52,{y} L336,{y} Q362,{y} 358,{y + 18} L356,{y + thick} Q354,{y + thick + 8} 336,{y + thick + 8} '
            f'L64,{y + thick + 8} Q44,{y + thick + 8} 44,{y + thick - 8} Z" fill="{s}" stroke="{so}" {SW}/>')


def _laces(xs, y0, lace, n=3, dy=20):
    return "".join(f'<line x1="{xs}" y1="{y0 + i * dy}" x2="{xs + 40}" y2="{y0 + i * dy - 10}" '
                   f'stroke="{lace}" stroke-width="6" stroke-linecap="round"/>' for i in range(n))


def sneaker(c):
    m, o = c["main"], darken(c["main"])
    lace = c.get("lace", "#f4f2ee")
    body = _sole(c)
    body += (f'<path d="M62,268 L70,186 Q84,152 132,162 L174,156 Q222,152 262,184 Q312,206 348,248 L350,268 Z" fill="{m}" stroke="{o}" {SW}/>'
             f'<path d="M174,156 L196,268" fill="none" stroke="{o}" stroke-width="4"/>')
    body += _laces(176, 178, lace)
    if c.get("stripes"):  # Onitsuka 條紋
        st = c["stripes"]
        body += (f'<path d="M206,268 Q236,222 288,198" fill="none" stroke="{st}" stroke-width="10"/>'
                 f'<path d="M240,268 Q268,232 316,214" fill="none" stroke="{st}" stroke-width="10"/>')
    if c.get("foxing"):  # Vans 白邊
        body += f'<line x1="56" y1="270" x2="346" y2="270" stroke="{c["foxing"]}" stroke-width="8"/>'
    return svg(body)


def hightop(c):
    m, o = c["main"], darken(c["main"])
    lace = c.get("lace", "#f4f2ee")
    body = _sole(c)
    body += (f'<path d="M62,268 L66,122 Q84,92 136,104 L174,156 Q222,152 262,184 Q312,206 348,248 L350,268 Z" fill="{m}" stroke="{o}" {SW}/>'
             f'<path d="M136,104 L174,156 L196,268" fill="none" stroke="{o}" stroke-width="4"/>')
    body += _laces(124, 136, lace, n=5, dy=24)
    return svg(body)


def runner(c):
    m, o = c["main"], darken(c["main"])
    acc = c.get("accent", m)
    body = _sole(c, thick=42)
    body += (f'<path d="M62,268 L72,176 Q92,146 142,158 L182,150 Q242,146 292,190 Q332,214 350,248 L352,268 Z" fill="{m}" stroke="{o}" {SW}/>'
             f'<path d="M72,176 Q92,146 142,158 L156,268 L62,268 Z" fill="{acc}" stroke="{o}" {SW}/>'
             f'<path d="M292,190 Q332,214 350,248 L352,268 L290,268 Z" fill="{acc}" stroke="{o}" {SW}/>')
    body += _laces(184, 172, "#f4f2ee")
    return svg(body)


def sandal(c):
    m, o = c["main"], darken(c["main"])
    body = _sole(c, thick=26)
    body += (f'<path d="M110,268 Q150,150 250,190 Q290,205 330,268" fill="none" stroke="{m}" stroke-width="22" stroke-linecap="round"/>'
             f'<path d="M110,268 Q150,150 250,190 Q290,205 330,268" fill="none" stroke="{o}" stroke-width="4" stroke-dasharray="8 8"/>'
             f'<path d="M70,268 L90,180 Q120,170 130,200 L120,268" fill="{m}" stroke="{o}" {SW}/>')
    return svg(body)


def slide(c):
    m, o = c["main"], darken(c["main"])
    body = _sole(c, thick=26)
    body += f'<path d="M130,268 Q180,150 300,196 L318,268 Z" fill="{m}" stroke="{o}" {SW}/>'
    return svg(body)


def flipflop(c):
    m, o = c["main"], darken(c["main"])
    body = _sole(c, thick=22)
    body += (f'<path d="M110,268 Q170,190 250,210" fill="none" stroke="{m}" stroke-width="14" stroke-linecap="round"/>'
             f'<path d="M330,268 Q300,200 250,210" fill="none" stroke="{m}" stroke-width="14" stroke-linecap="round"/>'
             f'<circle cx="250" cy="210" r="11" fill="{m}" stroke="{o}" stroke-width="4"/>')
    return svg(body)


def watch(c):
    case, strap = c.get("case", "#1c1c1e"), c["main"]
    so = darken(strap)
    return svg(f'<rect x="164" y="40" width="72" height="330" rx="20" fill="{strap}" stroke="{so}" {SW}/>'
               f'<circle cx="200" cy="200" r="78" fill="{case}" stroke="{darken(case, 0.5)}" {SW}/>'
               f'<circle cx="200" cy="200" r="60" fill="#2a2a2e"/>'
               f'<circle cx="200" cy="200" r="50" fill="none" stroke="{c.get("accent", "#6fbf73")}" stroke-width="6" stroke-dasharray="230 100" transform="rotate(-90 200 200)"/>'
               f'<rect x="184" y="188" width="32" height="24" rx="4" fill="#f4f2ee" opacity=".85"/>')


SHAPES = dict(tshirt=tshirt, shirt=shirt, pants=pants, shorts=shorts, sneaker=sneaker, hightop=hightop,
              runner=runner, sandal=sandal, slide=slide, flipflop=flipflop, watch=watch)


def main():
    items = json.load(open(ITEMS, encoding="utf-8"))
    os.makedirs(OUT, exist_ok=True)
    n = 0
    for it in items:
        shape = it.get("shape")
        if not shape:
            continue
        path = os.path.join(OUT, f"{it['id']}.svg")
        with open(path, "w", encoding="utf-8") as f:
            f.write(SHAPES[shape](it.get("colors", {})))
        # 已有 Gemini 手繪圖（photos/items-gen/）就不覆蓋 photo 路徑，SVG 只當備援
        if not os.path.exists(os.path.join(ROOT, "photos", "items-gen", f"{it['id']}.jpg")):
            it["photo"] = f"photos/items/{it['id']}.svg"
        n += 1
    json.dump(items, open(ITEMS, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"{n} 張插圖已產生")


if __name__ == "__main__":
    main()
