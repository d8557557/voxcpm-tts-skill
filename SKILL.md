---
name: voxcpm-tts
description: VoxCPM2 語音克隆技能（全域可用）。當使用者要求「用 XX 的聲音說一段話」、「生成語音」、「語音克隆」、「讓 A 跟 B 對話」、「錄製新聲音」、「有哪些可用的聲音」等任何需要文字轉語音或語音克隆的情境時使用。此技能依賴 VoxCPM2 專案目錄來執行 clone.py / dialogue.py，支援 NVIDIA CUDA、Intel Arc XPU 與 CPU 模式。
---

# VoxCPM2 TTS 語音克隆技能

## 觸發情境
使用者說出：
- 「用 XX 的聲音說⋯⋯」
- 「生成語音／語音克隆」
- 「讓 A 跟 B 對話」
- 「錄製新聲音／錄音」
- 「有哪些可用的聲音」
- 「播放剛剛生成的聲音」

## 腳本位置
`~/.config/opencode/skills/voxcpm-tts/voxcpm-tts.py`

## Voice Design（核心功能）

VoxCPM2 支援**用自然語言描述創造全新聲音**，不需任何參考音檔。

範例描述詞：
- `年輕女性、溫柔甜美`
- `中年男性、沉穩專業、略帶沙啞`
- `活潑開朗的少女、語速偏快`
- `老奶奶、慈祥和藹、語速緩慢`
- `科幻電影預告片旁白、低沉有磁性的男聲`

## 使用方式

### 用描述創造新聲音（不需音檔）
```bash
python ~/.config/opencode/skills/voxcpm-tts/voxcpm-tts.py design "聲音描述" "要說的文字" --output output/voice.wav
```

範例：
```bash
python ~/.config/opencode/skills/voxcpm-tts/voxcpm-tts.py design "年輕女性、溫柔甜美" "你好，歡迎來到VoxCPM2的世界。" --output output/溫柔女聲.wav
```

```bash
python ~/.config/opencode/skills/voxcpm-tts/voxcpm-tts.py design "中年男性、沉穩專業" "各位來賓早安，今天為您報導最新科技趨勢。" --output output/沉穩男聲.wav
```

### 列出所有已錄製的聲音
```bash
python ~/.config/opencode/skills/voxcpm-tts/voxcpm-tts.py list
```

### 用指定聲音生成語音
```bash
python ~/.config/opencode/skills/voxcpm-tts/voxcpm-tts.py clone "要生成的文字" --voice 聲音名稱 --output output/result.wav
```

### 兩個聲音對話
```bash
python ~/.config/opencode/skills/voxcpm-tts/voxcpm-tts.py dialogue --voice1 聲音A --voice2 聲音B --output output/dialogue.wav
```

### 播放已生成的音檔
```bash
python ~/.config/opencode/skills/voxcpm-tts/voxcpm-tts.py play output/result.wav
```

### 錄製新聲音（開啟網頁介面）
```bash
python ~/.config/opencode/skills/voxcpm-tts/voxcpm-tts.py record --voice 新聲音名稱
```

## 參數說明

### design (用描述創造聲音)
| 參數 | 必填 | 說明 |
|------|------|------|
| `description` | 是 | 聲音的自然語言描述（如：年輕女性、溫柔甜美） |
| `text` | 是 | 要說的文字內容 |
| `--output` / `-o` | 否 | 輸出 WAV 路徑（預設: output/designed_voice.wav） |
| `--device` / `-d` | 否 | 強制裝置 (cuda/xpu/cpu) |

### clone (單一語音)
| 參數 | 必填 | 說明 |
|------|------|------|
| `text` | 是 | 要生成的文字內容 |
| `--voice` / `-v` | 是 | 聲音名稱（對應 voices/ 目錄） |
| `--output` / `-o` | 否 | 輸出 WAV 路徑（預設: output/cloned_voice.wav） |
| `--device` / `-d` | 否 | 強制裝置 (cuda/xpu/cpu) |

### dialogue (雙人對話)
| 參數 | 必填 | 說明 |
|------|------|------|
| `--voice1` | 是 | 第一個聲音 |
| `--voice2` | 是 | 第二個聲音 |
| `--output` / `-o` | 否 | 輸出 WAV 路徑 |
| `--device` / `-d` | 否 | 強制裝置 |

### record (錄音)
| 參數 | 必填 | 說明 |
|------|------|------|
| `--voice` / `-v` | 是 | 新聲音的名稱 |

## 注意事項
- **首次執行**會自動下載 VoxCPM2 模型（約 4.7GB），快取在 D:\.cache\huggingface
- **CPU 模式**較慢（10 字約需 45 分鐘），建議在有 NVIDIA GPU（8GB+ VRAM）的機器上使用
- 輸出音檔預設為 16kHz 單聲道 WAV 格式
- 若需自訂對話內容，可在呼叫後編輯 dialogue.py 或直接傳入文字

## 輸出
WAV 音檔，路徑由 `--output` 指定（預設在目前專案的 output/ 目錄）。
