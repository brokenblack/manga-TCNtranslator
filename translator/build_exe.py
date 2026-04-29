"""
build_exe.py
打包遊戲翻譯工具為 Windows EXE（完整打包策略）

策略：
  - 打包核心程式 + 所有 OCR 依賴（torch CPU / transformers / manga-ocr / easyocr）
  - 完全離線，無需額外安裝
  - 預估 EXE 約 1.5–2 GB（torch CPU + 排除 paddle/scipy/matplotlib 後）
  - 打包時間約 20–40 分鐘

依賴前置條件（必須先在 .venv 安裝）：
  uv pip install pyinstaller pillow numpy keyboard pystray opencc-python-reimplemented \
                 anthropic google-generativeai groq \
                 manga-ocr easyocr pykakasi transformers
  uv pip install torch --index-url https://download.pytorch.org/whl/cpu
"""

import subprocess
import sys
import shutil
from pathlib import Path

# Windows cp950 console 不支援 emoji；強制 stdout/stderr 走 UTF-8
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

HERE = Path(__file__).parent


def run(cmd: list, **kw):
    print("▶", " ".join(str(c) for c in cmd))
    result = subprocess.run(cmd, **kw)
    if result.returncode != 0:
        print(f"\n❌ 指令失敗（code {result.returncode}）")
        sys.exit(1)
    return result


def ensure_pyinstaller():
    try:
        import PyInstaller
        print(f"✅ PyInstaller {PyInstaller.__version__}")
    except ImportError:
        print("安裝 PyInstaller...")
        run([sys.executable, "-m", "pip", "install", "pyinstaller"])


def build():
    ensure_pyinstaller()

    for d in ["build", "dist"]:
        p = HERE / d
        if p.exists():
            shutil.rmtree(p)
            print(f"🗑  清除 {d}/")

    icon_args = []
    if (HERE / "icon.ico").exists():
        icon_args = ["--icon", str(HERE / "icon.ico")]

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onedir",
        "--windowed",
        "--name", "翻譯工具",

        # ── 必要 hidden imports ──
        "--hidden-import", "tkinter",
        "--hidden-import", "tkinter.ttk",
        "--hidden-import", "PIL",
        "--hidden-import", "PIL.Image",
        "--hidden-import", "PIL.ImageGrab",
        "--hidden-import", "PIL._tkinter_finder",
        "--hidden-import", "numpy",

        # ── 翻譯 API SDK ──
        "--hidden-import", "anthropic",
        "--hidden-import", "google.generativeai",
        "--hidden-import", "groq",

        # ── 全域熱鍵 / 系統匣 / 簡轉繁 ──
        "--hidden-import", "keyboard",
        "--hidden-import", "pystray",
        "--hidden-import", "pystray._win32",
        "--hidden-import", "opencc",

        # ── OCR / 模型依賴 ──
        # transformers 與 tokenizers 用 lazy module loading，必須 --collect-all
        # 才能抓到 AutoTokenizer 的所有子類別與 tokenizer 設定檔。
        "--hidden-import", "torch",
        "--hidden-import", "torch.nn",
        "--hidden-import", "torch.utils",
        "--hidden-import", "torch.utils.data",

        # ── 收集模組所有檔案（程式碼 + 資料 + 隱式 import）──
        "--collect-all", "manga_ocr",
        "--collect-all", "easyocr",
        "--collect-all", "transformers",
        "--collect-all", "tokenizers",
        "--collect-all", "opencc",
        "--collect-data", "pykakasi",
        "--collect-data", "unidic_lite",

        # ── 排除沒用到的大型模組（瘦身）──
        # 註：scipy 不可排除（easyocr 內部用 scipy.spatial / scipy.ndimage）
        "--exclude-module", "paddleocr",
        "--exclude-module", "paddlepaddle",
        "--exclude-module", "matplotlib",
        "--exclude-module", "pandas",
        "--exclude-module", "notebook",
        "--exclude-module", "IPython",
        "--exclude-module", "jupyter",
        "--exclude-module", "tensorflow",
        "--exclude-module", "tensorboard",

        *icon_args,
        str(HERE / "translator.py"),
    ]

    print("\n⏳ 開始打包（約 30–60 分鐘，請勿中斷）...\n")
    run(cmd, cwd=str(HERE))

    exe = HERE / "dist" / "翻譯工具.exe"
    if not exe.exists():
        exe = HERE / "dist" / "翻譯工具" / "翻譯工具.exe"
    if exe.exists():
        # 把 source 端的「使用說明.txt」一起 copy 到 dist 下
        readme_src = HERE / "使用說明.txt"
        if readme_src.exists():
            shutil.copy2(readme_src, exe.parent / "使用說明.txt")
            print(f"📄 已複製 使用說明.txt 到 dist")

        size_mb = exe.stat().st_size / 1024 / 1024
        print(f"\n✅ 打包完成！")
        print(f"   位置：{exe}")
        print(f"   大小：{size_mb:.1f} MB")
        print(f"\n📌 首次執行：")
        print(f"   OCR 模型會在首次使用時下載到 %APPDATA%\\manga_ocr 或 %HOME%\\.easyocr")
        print(f"   （不在 EXE 同層目錄，所以 EXE 本身仍可攜帶）")
    else:
        print("\n❌ 找不到輸出 EXE，請查看上方錯誤訊息")


if __name__ == "__main__":
    build()
