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
