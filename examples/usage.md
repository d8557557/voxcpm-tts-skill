# 🎤 voxcpm-tts 使用範例

## 基本設定

先確認 `config.json` 中的 VoxCPM2 專案路徑正確：

```json
{"project_dir": "D:\\path\\to\\voxcpm2-voice-cloner"}
```

---

## 🎨 Voice Design — 用描述創造聲音

不需要任何參考音檔，直接用文字描述聲音特質：

```bash
# 溫柔女聲
python voxcpm-tts.py design "年輕女性、溫柔甜美" "你好，歡迎來到 VoxCPM2 的世界。" -o output/溫柔女聲.wav

# 沉穩男聲
python voxcpm-tts.py design "中年男性、沉穩專業、略帶沙啞" "各位來賓早安，今天為您報導最新科技趨勢。" -o output/沉穩男聲.wav

# 活潑少女
python voxcpm-tts.py design "活潑開朗的少女、語速偏快" "耶！今天天氣超好，我們一起去野餐吧！" -o output/活潑少女.wav

# 慈祥老奶奶
python voxcpm-tts.py design "老奶奶、慈祥和藹、語速緩慢" "小朋友，過來阿婆這邊，我講故事給你聽。" -o output/老奶奶.wav

# 電影預告旁白
python voxcpm-tts.py design "科幻電影預告片旁白、低沉有磁性的男聲" "在一個遙遠的星系，一場前所未有的冒險即將展開。" -o output/預告片旁白.wav
```

---

## 🗣️ 語音克隆 — 用已錄製的聲音

```bash
# 列出所有可用聲音
python voxcpm-tts.py list

# 用指定聲音生成
python voxcpm-tts.py clone "親愛的顧客您好，您的訂單已經出貨囉！" --voice 客服聲音 -o output/order.wav
```

---

## 💬 雙人對話

```bash
python voxcpm-tts.py dialogue --voice1 客服女聲 --voice2 顧客男聲 -o output/對話.wav
```

對話內容可在 VoxCPM2 專案的 `dialogue.py` 中編輯。

---

## 🎙️ 錄製新聲音

開啟網頁錄音介面：

```bash
python voxcpm-tts.py record --voice 我的新聲音
```

---

## ▶️ 播放音檔

```bash
python voxcpm-tts.py play output/result.wav
```

---

## ⚙️ 指定運算裝置

```bash
# 強制使用 GPU
python voxcpm-tts.py design "年輕女性、溫柔甜美" "你好" -d cuda

# 強制使用 Intel XPU
python voxcpm-tts.py clone "你好" --voice 我的聲音 -d xpu

# 強制使用 CPU（非常慢）
python voxcpm-tts.py clone "你好" --voice 我的聲音 -d cpu
```

---

## 📝 注意事項

- 首次執行會自動下載 VoxCPM2 模型（約 4.7GB）
- CPU 模式極慢（10 字約 45 分鐘），建議使用 NVIDIA GPU
- 輸出為 16kHz 單聲道 WAV 格式
- 若遇 `UnicodeEncodeError`，請設定：`$env:PYTHONIOENCODING='utf-8'`
