#!/usr/bin/env python3
"""用 Gemini 圖片模型產生穿搭人物插圖。

金鑰讀 ~/.config/gemini/key（不要放進 repo）。

用法：
  python3 tools/gen_illustrations.py character [-n 3]        # 生角色定稿候選 → photos/gen/character-*.png
  python3 tools/gen_illustrations.py outfit a [b c ...]      # 依 outfits.json 生穿搭圖 → photos/gen/outfit-<id>.png
  python3 tools/gen_illustrations.py outfit all
選項：--model gemini-3.1-flash-image（預設）| gemini-2.5-flash-image | gemini-3-pro-image
      --ref photos/gen/character.png   人物參考圖（outfit 模式預設用這張）
"""
import argparse, base64, json, os, sys, time, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN = os.path.join(ROOT, "photos", "gen")
KEY = open(os.path.expanduser("~/.config/gemini/key")).read().strip()

STYLE = (
    "Cute chibi-style fashion illustration, single character, full body, standing straight, front view, "
    "head about one quarter of total height, simple dot eyes, no nose, tiny mouth, "
    "thin clean hand-drawn ink outlines, flat soft muted colors with a subtle paper-like texture, "
    "plain pure white background, no text, no labels, no watermark, no shadow on the ground. "
    "Instagram outfit-illustration style."
)

CHARACTER = (
    "The character is an East Asian man in his early 30s, slim athletic build, warm tan skin, "
    "short black hair in a textured crop with the fringe pushed forward and faded short sides, "
    "thick straight eyebrows, light 3mm stubble, calm neutral expression. "
    "He wears a black sports watch with an orange strap on his left wrist."
)


def call(model, parts, aspect="3:4"):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    body = {
        "contents": [{"parts": parts}],
        "generationConfig": {"responseModalities": ["IMAGE", "TEXT"], "imageConfig": {"aspectRatio": aspect}},
    }
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST",
                                 headers={"Content-Type": "application/json", "x-goog-api-key": KEY})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            msg = e.read().decode()[:300]
            if e.code in (429, 503) and attempt < 3:
                wait = 20 * (attempt + 1)
                print(f"  {e.code}，等 {wait}s 再試…", file=sys.stderr)
                time.sleep(wait)
                continue
            sys.exit(f"HTTP {e.code}: {msg}")


def save_images(resp, out_prefix):
    n = 0
    for cand in resp.get("candidates", []):
        for part in cand.get("content", {}).get("parts", []):
            if "inlineData" in part:
                data = base64.b64decode(part["inlineData"]["data"])
                path = f"{out_prefix}.png" if n == 0 else f"{out_prefix}-{n}.png"
                open(path, "wb").write(data)
                print("  →", os.path.relpath(path, ROOT))
                n += 1
            elif "text" in part:
                print("  model:", part["text"][:200].replace("\n", " "))
    if n == 0:
        print("  沒有拿到圖片；回應：", json.dumps(resp)[:400])
    return n


def img_part(path):
    mime = "image/png" if path.lower().endswith(".png") else "image/jpeg"
    return {"inlineData": {"mimeType": mime, "data": base64.b64encode(open(path, "rb").read()).decode()}}


def gen_character(model, n):
    prompt = (f"{STYLE}\n\n{CHARACTER}\n\n"
              "Outfit: plain white crew-neck t-shirt, slim black trousers with a single cuff, "
              "black canvas sneakers with white soles and white laces.")
    for i in range(n):
        print(f"角色候選 {i + 1}/{n}")
        save_images(call(model, [{"text": prompt}]), os.path.join(GEN, f"character-{i + 1}"))


def describe_outfit(o, items):
    by = {i["id"]: i for i in items}
    names = [by[i]["name"] for i in o["items"] if i in by]
    # 用顏色＋版型描述，避免品牌名影響
    desc = []
    for i in o["items"]:
        it = by.get(i)
        if not it:
            continue
        c = it.get("colors", {})
        desc.append(f"{it['name']}（{it.get('shape', '')} {c.get('main', '')}{' ' + c.get('fit', '') if c.get('fit') else ''}）")
    return names, desc


def gen_outfits(model, ids, ref):
    outfits = json.load(open(os.path.join(ROOT, "data", "outfits.json"), encoding="utf-8"))["outfits"]
    items = json.load(open(os.path.join(ROOT, "data", "items.json"), encoding="utf-8"))
    want = outfits if ids == ["all"] else [o for o in outfits if o["id"] in ids]
    for o in want:
        names, desc = describe_outfit(o, items)
        prompt = (f"{STYLE}\n\n{CHARACTER}\n\n"
                  "Draw the SAME character as in the reference image, same face, same hair, same proportions, same art style. "
                  "Only the clothes change.\n\nOutfit: " + "; ".join(desc) + ".\n"
                  + (f"Styling notes: {'; '.join(o.get('tips', []))}." if o.get("tips") else ""))
        print(f"穿搭 {o['id']}：{' ＋ '.join(names)}")
        parts = [img_part(ref), {"text": prompt}] if ref and os.path.exists(ref) else [{"text": prompt}]
        save_images(call(model, parts), os.path.join(GEN, f"outfit-{o['id']}"))
        time.sleep(3)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["character", "outfit"])
    ap.add_argument("ids", nargs="*")
    ap.add_argument("-n", type=int, default=3)
    ap.add_argument("--model", default="gemini-3.1-flash-image")
    ap.add_argument("--ref", default=os.path.join(GEN, "character.png"))
    a = ap.parse_args()
    os.makedirs(GEN, exist_ok=True)
    if a.mode == "character":
        gen_character(a.model, a.n)
    else:
        gen_outfits(a.model, a.ids or ["all"], a.ref)


if __name__ == "__main__":
    main()
