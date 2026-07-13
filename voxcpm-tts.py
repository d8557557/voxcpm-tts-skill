#!/usr/bin/env python3
"""VoxCPM2 TTS wrapper — 跨專案調用語音克隆技能。"""

from __future__ import annotations

import argparse
import io
import json
import os
import subprocess
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")
import sys
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent
CONFIG_FILE = SKILL_DIR / "config.json"


def default_project_dir() -> Path:
    """從 config.json 讀取專案路徑，或回傳預設值。"""
    if CONFIG_FILE.exists():
        cfg = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        return Path(cfg["project_dir"])
    # Fallback: 掃描常見位置
    candidates = [
        Path.home() / "voxcpm2-voice-cloner",
        Path("D:/deskop/OLL測試區/Agent 學習/語音合成"),
    ]
    for p in candidates:
        if (p / "clone.py").exists():
            return p
    print("錯誤：找不到 VoxCPM2 專案目錄。請執行以下指令設定：", file=sys.stderr)
    print(f'  echo \'{{"project_dir": "你的路徑"}}\' > {CONFIG_FILE}', file=sys.stderr)
    sys.exit(1)


def resolve_voices(project_dir: Path) -> list[str]:
    voices_dir = project_dir / "voices"
    if not voices_dir.exists():
        return []
    return sorted(d.name for d in voices_dir.iterdir() if d.is_dir())


def list_voices(project_dir: Path) -> None:
    voices = resolve_voices(project_dir)
    if not voices:
        print("目前沒有任何已錄製的聲音。")
        print("請先錄音：python voxcpm-tts.py record --voice <名稱>")
        return
    print("已錄製的聲音：")
    for v in voices:
        wav = project_dir / "voices" / v / "ref_voice.wav"
        size = wav.stat().st_size if wav.exists() else 0
        print(f"  {v}  ({size/1024:.0f} KB)")


def run_clone(text: str, voice: str, output: str, project_dir: Path, device: str, control: str = "") -> Path:
    """執行 clone.py 並回傳輸出檔案路徑。"""
    out_path = Path(output)
    if not out_path.is_absolute():
        out_path = Path.cwd() / output

    venv_python = project_dir / ".venv" / "Scripts" / "python.exe"
    clone_script = project_dir / "clone.py"
    cmd = [
        str(venv_python),
        str(clone_script),
        text,
        "--voice", voice,
        "--output", str(out_path),
    ]
    if control:
        cmd.extend(["--control", control])
    if device:
        cmd.extend(["--device", device])

    env = os.environ.copy()
    env["HF_HOME"] = env.get("HF_HOME", r"C:\.cache\huggingface")

    print(f"執行：{' '.join(cmd)}")
    result = subprocess.run(cmd, env=env, cwd=project_dir)
    if result.returncode != 0:
        sys.exit(result.returncode)

    if out_path.exists():
        print(f"✅ 語音已生成：{out_path}")
        return out_path
    return out_path


def run_dialogue(voice1: str, voice2: str, output: str, project_dir: Path, device: str) -> Path:
    """執行 dialogue.py 並回傳輸出檔案路徑。"""
    out_path = Path(output)
    if not out_path.is_absolute():
        out_path = Path.cwd() / output

    venv_python = project_dir / ".venv" / "Scripts" / "python.exe"
    dialogue_script = project_dir / "dialogue.py"
    cmd = [
        str(venv_python),
        str(dialogue_script),
        "--voice1", voice1,
        "--voice2", voice2,
        "--output", str(out_path),
    ]
    if device:
        cmd.extend(["--device", device])

    env = os.environ.copy()
    env["HF_HOME"] = env.get("HF_HOME", r"C:\.cache\huggingface")

    print(f"執行：{' '.join(cmd)}")
    result = subprocess.run(cmd, env=env, cwd=project_dir)
    if result.returncode != 0:
        sys.exit(result.returncode)

    if out_path.exists():
        print(f"✅ 對話已生成：{out_path}")
        return out_path
    return out_path


def run_design(description: str, text: str, output: str, project_dir: Path, device: str) -> Path:
    """Voice Design：用描述創造新聲音，不需參考音檔。"""
    out_path = Path(output)
    if not out_path.is_absolute():
        out_path = Path.cwd() / output

    venv_python = project_dir / ".venv" / "Scripts" / "python.exe"

    # 用內嵌 Python 直接跑 model.generate()，把描述包在 () 裡
    code = f"""
import os, sys, time
os.environ.setdefault("HF_HOME", "D:\\\\.cache\\\\huggingface")
sys.path.insert(0, r"{project_dir}")
import soundfile as sf
from voxcpm import VoxCPM

model = VoxCPM.from_pretrained(
    "openbmb/VoxCPM2",
    load_denoiser=False,
    device="{'cpu' if not device else device}",
    optimize=False,
)
gen_text = "({description}){text}"
print(f"生成中（描述：{description}）...")
t0 = time.time()
wav = model.generate(
    text=gen_text,
    cfg_value=2.0,
    inference_timesteps=10,
)
dur = len(wav) / model.tts_model.sample_rate
print(f"生成完成，耗時 {{time.time()-t0:.1f}}s（語音長度 {{dur:.1f}}s）")
sf.write(r"{out_path}", wav, model.tts_model.sample_rate)
print(f"已存檔：{out_path}")
"""
    env = os.environ.copy()
    env["HF_HOME"] = env.get("HF_HOME", r"C:\.cache\huggingface")
    print(f"Voice Design：用「{description}」的描述來創造聲音")
    result = subprocess.run([str(venv_python), "-c", code], env=env, cwd=project_dir)
    if result.returncode != 0:
        sys.exit(result.returncode)
    if out_path.exists():
        print(f"✅ 語音已生成：{out_path}")
        return out_path
    return out_path


def run_play(file_path: str) -> None:
    """播放 WAV 音檔。"""
    import subprocess
    path = Path(file_path).resolve()
    if not path.exists():
        print(f"錯誤：找不到檔案 {path}")
        sys.exit(1)
    try:
        import winsound
        winsound.PlaySound(str(path), winsound.SND_FILENAME)
        print(f"播放完成：{path}")
    except Exception:
        # Fallback: 用系統預設播放器
        os.startfile(str(path))


def run_record(voice: str, project_dir: Path) -> None:
    """開啟錄音網頁介面。"""
    venv_python = project_dir / ".venv" / "Scripts" / "python.exe"
    webui_script = project_dir / "webui_record.py"
    cmd = [str(venv_python), str(webui_script), "--voice", voice]
    print(f"開啟錄音介面：{' '.join(cmd)}")
    subprocess.run(cmd, env=os.environ.copy(), cwd=project_dir)


def main() -> None:
    project_dir = default_project_dir()

    parser = argparse.ArgumentParser(description="VoxCPM2 TTS 技能 — 語音克隆與生成")
    sub = parser.add_subparsers(dest="action", required=True)

    # list
    sub.add_parser("list", help="列出所有已錄製的聲音")

    # clone
    p_clone = sub.add_parser("clone", help="用指定聲音生成語音")
    p_clone.add_argument("text", help="要生成的文字")
    p_clone.add_argument("--voice", "-v", required=True, help="聲音名稱")
    p_clone.add_argument("--control", "-c", default="", help="情緒/風格控制描述（如：愉快、活潑）")
    p_clone.add_argument("--output", "-o", default="output/cloned_voice.wav", help="輸出檔案路徑")
    p_clone.add_argument("--device", "-d", help="強制指定裝置 (cuda/xpu/cpu)")

    # dialogue
    p_dial = sub.add_parser("dialogue", help="用兩個聲音生成對話")
    p_dial.add_argument("--voice1", required=True, help="聲音 A")
    p_dial.add_argument("--voice2", required=True, help="聲音 B")
    p_dial.add_argument("--output", "-o", default="output/dialogue.wav", help="輸出檔案路徑")
    p_dial.add_argument("--device", "-d", help="強制指定裝置 (cuda/xpu/cpu)")

    # design
    p_design = sub.add_parser("design", help="用描述創造新聲音（不需參考音檔）")
    p_design.add_argument("description", help="聲音描述（如：年輕女性、溫柔甜美）")
    p_design.add_argument("text", help="要說的文字內容")
    p_design.add_argument("--output", "-o", default="output/designed_voice.wav", help="輸出檔案路徑")
    p_design.add_argument("--device", "-d", help="強制指定裝置 (cuda/xpu/cpu)")

    # play
    p_play = sub.add_parser("play", help="播放已生成的音檔")
    p_play.add_argument("file", help="WAV 檔案路徑")

    # record
    p_rec = sub.add_parser("record", help="錄製新聲音（開啟網頁介面）")
    p_rec.add_argument("--voice", "-v", required=True, help="聲音名稱")

    args = parser.parse_args()

    if args.action == "list":
        list_voices(project_dir)
    elif args.action == "clone":
        run_clone(args.text, args.voice, args.output, project_dir, args.device, args.control)
    elif args.action == "dialogue":
        run_dialogue(args.voice1, args.voice2, args.output, project_dir, args.device)
    elif args.action == "design":
        run_design(args.description, args.text, args.output, project_dir, args.device)
    elif args.action == "play":
        run_play(args.file)
    elif args.action == "record":
        run_record(args.voice, project_dir)


if __name__ == "__main__":
    main()
