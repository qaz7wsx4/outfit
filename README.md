# 穿搭本

手機打開就知道今天怎麼穿。純靜態網站，放在 GitHub Pages。

## 檔案

- `index.html` — 整個網站
- `data/items.json` — 衣櫃，每件一筆（分類、品牌、型號、顏色、尺寸、價格、購入、用途、備註、插圖設定）
- `data/outfits.json` — 穿搭公式與規則
- `data/shopping.json` — 每月待買清單與預算
- `photos/items/*.svg` — 單品插圖，由 `tools/make_illustrations.py` 產生，不要手改
- `tools/make_illustrations.py` — 插圖產生器

## 新增一件衣服

1. 在 `data/items.json` 加一筆，`shape` 選版型、`colors.main` 填顏色（hex）
2. `python3 tools/make_illustrations.py`
3. `git add -A && git commit -m "..." && git push`

版型：`tshirt` `shirt` `pants` `shorts` `sneaker` `hightop` `runner` `sandal` `slide` `flipflop` `watch`

## 插圖（Gemini 手繪風）

- 人物穿搭圖 `photos/outfits/<id>.jpg`、單品圖 `photos/items-gen/<id>.jpg`，都是在 Gemini 網頁版同一個對話生成（角色定稿 `photos/ref/character.jpg`）
- 新單品：叫 Gemini「Same flat-lay illustration style… 2x2 grid…」一次畫四件再裁；新穿搭：「Same character as the previous images… Only the clothes change. Outfit: …」
- `tools/make_illustrations.py` 的 SVG 只是備援，有手繪圖時不會覆蓋
