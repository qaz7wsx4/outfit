# 待辦（不在購物清單裡的）

## 角色插畫：6 套「穿外套」版本用錯角色

**狀態**：等 agy 額度，2026-11-29 之後才能做。

19 套穿搭裡有 8 套可以切換「穿外套／脫外套」。其中 **n、o、p、q、r、s 這 6 套的「穿外套」版本用的是另一個角色**：頭比較大、身形偏 Q 版、瀏海是往前垂的碎髮；而全部的 `-off`（脫外套）版本，以及其他 13 套，用的都是另一個角色：身形比較高瘦、頭身比正常、頭髮是往上抓的油頭、兩側有漸層推高。

所以在網站上按「脫外套」會整個人換掉，不只是換髮型。

**不能用去頭換頭補**：兩個角色的身體比例也不一樣，貼上去會接不起來。

**做法**：等 2026-11-29 agy 週額度重置後，用 `photos/outfits/n-off.jpg` 當 reference，重生 n、o、p、q、r、s 這 6 張。900×900。
參考腳本：`gen_ref3.sh`（在 scratchpad，含 md5 排除參考圖的修正）。
prompt 要短，太長會把 agy 推進子 agent 迴圈然後逾時沒產圖。

## About Companions 法蘭絨單品圖是上色的不是生成的

`photos/items-gen/shirt-flannel-blue.jpg` 目前是拿 `shirt-white-ls.jpg` 重新上色做的，所以跟白襯衫是同一張畫。
同樣等 11/29 額度回來後重生一張真的。
正確規格：窄領（不是扣領）、直筒身、圓弧下襬、左胸一個無蓋貼袋、素面。

## 雪地日常：三套穿搭還沒進網站

2026-11-27 做了雪地日常（不是滑雪時）的從頭到腳規劃，購物清單已經進 `shopping.json`
的「滑雪・雪地日常」那格，但**三套實際搭配還沒建成 outfit**。

沒建的原因有兩個：①裝備還沒買，把沒買的東西加進 `items.json` 會讓衣櫃出現其實沒有的衣服
②插畫要等 agy 額度（跟上面那兩件一起做）。

等雪靴、底層衣、配件買齊之後要做的事：
1. `items.json` 新增：`sh-columbia-snow`（雪靴）、`base-merino-top`、`base-merino-bottom`、
   `cap-beanie`、`gaiter-neck`、`glove-wp`
2. `outfits.json` 的 `scenes` 加一個「雪地」，三套 outfit 的 `scenes` 都填它、`temp` 用現有的「冷」
   （不要新增 temp 值，`.tt i.{溫度}` 的 CSS 只寫了熱／涼／冷）
3. 三套內容（以下是 2026-11-27 定好的，直接照抄）：

- **雪地 1・移動日**：美麗諾長袖 ＋ knit-grey ＋ Mammut 硬殼／底層褲 ＋ p-grey 深灰彈性長褲／
  Darn Tough 中筒厚襪 ＋ Columbia BUGABOOT CANYON。重點是好穿脫，機場、新幹線、旅館一直在脫外套脫鞋。
- **雪地 2・村裡吃飯逛街**：美麗諾長袖 ＋ shirt-flannel-blue 法蘭絨敞開 ＋ Mammut／
  底層褲 ＋ p-black／雪靴。帽子脖圍手套全上。
- **雪地 3・溫泉街拍照**：美麗諾長袖 ＋ Batoner 針織（12 月買）＋ oqLiq 炭灰（版型比 Mammut 乾淨、
  沒有袖子 logo）／底層褲 ＋ p-black／雪靴。這套是拍照用的，oqLiq 帽子較小、雪大的話還是換 Mammut。
