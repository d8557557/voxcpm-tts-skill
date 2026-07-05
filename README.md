# 🎤 voxcpm-tts — VoxCPM2 語音克隆技能

> VoxCPM2 語音克隆 — 用自然語言描述創造聲音、語音生成、雙人對話、錄製新聲音。

---

## 📌 簡介

**voxcpm-tts** 是 [OpenCode](https://github.com/d8557557/opencode) / Claude Code 專用的**語音克隆與 TTS 技能**。基於 VoxCPM2 模型，支援用文字描述創造全新聲音（不需參考音檔）、語音克隆、雙人對話等多種功能。

---

## ✨ 特色

| 特色 | 說明 |
|------|------|
| 🎨 **Voice Design** | 用自然語言描述創造聲音（如「年輕女性、溫柔甜美」） |
| 🗣️ **語音克隆** | 用已錄製的聲音生成任意文字 |
| 💬 **雙人對話** | 兩個聲音自然對話 |
| 🎙️ **錄音介面** | 內建網頁錄音工具 |
| 📋 **聲音管理** | 列出所有已錄製的聲音 |

---

## 🚀 使用方法

### 在 OpenCode / Claude Code 中使用

直接說關鍵詞即可載入技能：

> 「**用 XX 的聲音說一段話**」「**生成語音**」「**語音克隆**」
> 「**讓 A 跟 B 對話**」「**錄製新聲音**」「**有哪些可用的聲音**」

### 指令列快速入門

```bash
# 列出所有已錄製的聲音
python voxcpm-tts.py list

# 用描述創造聲音（不需音檔）
python voxcpm-tts.py design "年輕女性、溫柔甜美" "你好，歡迎來到 VoxCPM2 的世界。" --output output/hello.wav

# 用已錄製的聲音生成語音
python voxcpm-tts.py clone "今天天氣真好" --voice 我的聲音 -o output/result.wav

# 雙人對話
python voxcpm-tts.py dialogue --voice1 聲音A --voice2 聲音B -o output/dialogue.wav

# 播放音檔
python voxcpm-tts.py play output/result.wav

# 錄製新聲音
python voxcpm-tts.py record --voice 新聲音名稱
```

---

## 📂 專案結構

```
voxcpm-tts-skill/
├── SKILL.md                    # 🧠 核心技能定義
├── voxcpm-tts.py               # 🐍 主腳本（CLI 入口）
├── config.json                  # ⚙️ 設定檔（VoxCPM2 專案路徑）
├── README.md                   # 📖 本文件
├── LICENSE                     # ⚖️ MIT 授權
├── .gitignore                  # 🙈 忽略規則
├── .github/workflows/
│   └── ci.yml                  # 🔄 GitHub Actions CI
└── examples/
    └── usage.md                # 📝 使用範例
```

---

## 📦 系統需求

- **Python 3.10+**
- **NVIDIA GPU（8GB+ VRAM）** — 推薦，CPU 模式較慢
- **VoxCPM2 專案** — 需下載模型（約 4.7GB）
- **安裝相依套件**：

```bash
pip install voxcpm soundfile
```

### 設定檔

建立或編輯 `config.json`：

```json
{"project_dir": "D:\\path\\to\\voxcpm2-voice-cloner"}
```

---

## 🎨 Voice Design 範例描述詞

| 描述 | 適合場景 |
|:----|:---------|
| 年輕女性、溫柔甜美 | 客服、導覽、有聲書 |
| 中年男性、沉穩專業、略帶沙啞 | 新聞播報、旁白 |
| 活潑開朗的少女、語速偏快 | 遊戲角色、Podcast |
| 老奶奶、慈祥和藹、語速緩慢 | 故事朗讀 |
| 科幻電影預告片旁白、低沉有磁性的男聲 | 預告片、廣告 |

---

## 🔧 指令參數總覽

### `design` — 用描述創造聲音

| 參數 | 必填 | 說明 |
|:----|:----:|:------|
| `description` | ✅ | 聲音的自然語言描述 |
| `text` | ✅ | 要說的文字內容 |
| `--output` / `-o` | | 輸出 WAV 路徑 |
| `--device` / `-d` | | 強制裝置 (cuda/xpu/cpu) |

### `clone` — 語音克隆

| 參數 | 必填 | 說明 |
|:----|:----:|:------|
| `text` | ✅ | 要生成的文字 |
| `--voice` / `-v` | ✅ | 聲音名稱 |
| `--output` / `-o` | | 輸出 WAV 路徑 |
| `--device` / `-d` | | 強制裝置 |

### `dialogue` — 雙人對話

| 參數 | 必填 | 說明 |
|:----|:----:|:------|
| `--voice1` | ✅ | 聲音 A |
| `--voice2` | ✅ | 聲音 B |
| `--output` / `-o` | | 輸出 WAV 路徑 |
| `--device` / `-d` | | 強制裝置 |

---

## ⚙️ 技術細節

- **模型**：openbmb/VoxCPM2
- **輸出格式**：16kHz 單聲道 WAV
- **快取路徑**：`D:\.cache\huggingface`（可透過 `HF_HOME` 環境變數修改）
- **GPU 需求**：NVIDIA GPU 8GB+ VRAM（CUDA）
- **CPU 模式**：10 字約需 45 分鐘

---

## 🔄 GitHub Actions CI

每次 Push 會自動：
1. ✅ 檢查 SKILL.md 格式
2. ✅ 驗證 voxcpm-tts.py Python 語法

---

## ⚖️ 授權

[MIT License](./LICENSE) — 歡迎自由使用、改寫、分享！
