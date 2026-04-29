# 漫畫/遊戲即時翻譯工具 v1.0

第一個正式發布版。Windows 桌面工具，OCR 截圖 + AI 翻譯 + Anki 單字卡匯出。

## 下載

| 檔案 | 大小 | 說明 |
|---|---|---|
| [`翻譯工具_v1.0.zip`](https://github.com/brokenblack/manga-TCNtranslator/releases/download/v1.0/翻譯工具_v1.0.zip) | 398 MB | Windows 內建解壓即可使用 |
| [`翻譯工具_v1.0.7z`](https://github.com/brokenblack/manga-TCNtranslator/releases/download/v1.0/翻譯工具_v1.0.7z) | 279 MB | 需安裝 [7-Zip](https://www.7-zip.org/) |

> 兩個檔案內容完全相同，依你習慣的解壓工具擇一下載。
> 也可以在頁面底部「Assets」區塊直接下載。

## 快速開始

1. 下載 ZIP 並解壓到任意資料夾（建議桌面或 `C:\Tools`）
2. 進入解壓後的 `翻譯工具/` 資料夾
3. 雙擊 `翻譯工具.exe`
4. 點右上角「⚙️ 翻譯設定」→「翻譯 API」分頁
5. 填入 [API Key] → 儲存

詳細使用方式請見資料夾內的 `使用說明.txt`。

## 功能

- **OCR 截圖翻譯** — Ctrl + Alt + Q 框選遊戲畫面，自動辨識日／韓文並翻譯
- **Textractor 整合** — 監聽剪貼簿，與 VN 工具搭配
- **多 API + 自動 fallback** — 支援 Groq / Gemini / Claude / OpenRouter / Ollama，按優先級自動切換（網路斷線可 fallback 到本地 Ollama）
- **Anki 匯出** — 句子卡 + 挖空卡（Cloze），可選 Forvo 真人音訊
- **翻譯歷史** — 側欄記錄全部翻譯，支援批量加入 Anki
- **可自訂熱鍵** — 截圖快捷鍵 / Textractor 監聽快捷鍵都可改

## 安全性

已通過 [VirusTotal 掃描](https://www.virustotal.com/gui/file/a102d76e8c8f02fb15756a8f36d8b8cc6c0cdffb9ecb650fdf43a80bf3ca1ae3)：**1/67 安全廠商標記**（僅越南 Bkav Pro 的 ML 模型誤報，主流大廠 BitDefender / Acronis / Avira / CrowdStrike / ClamAV 等全部 clean）。

⚠️ **Windows Defender 可能誤報**：這是 PyInstaller 未簽章 exe 的常態。處理方式：
1. 開啟「Windows 安全性」
2. 「病毒與威脅防護」→「保護歷程記錄」
3. 找到本程式 →「動作」→「允許」

或將整個資料夾加入「排除項目」。

## 系統需求

- Windows 10 / 11 (64 位元)
- 記憶體：建議 4 GB 以上
- 硬碟：解壓後約 1.5 GB（含 OCR 模型約 2.5 GB）
- 網路：使用線上 AI 翻譯時需要

## 檔案完整性驗證 (SHA256)

```
ZIP : b546557d63730800d7a2cc24064a6d6099d64e973be01418f7520ba654b77a58
7z  : 80458ecd3ecf86cb97e21f6a5c08a2811b0970372b2123e1df9b672350f24a69
EXE : a102d76e8c8f02fb15756a8f36d8b8cc6c0cdffb9ecb650fdf43a80bf3ca1ae3
```

下載後可在 PowerShell 用 `Get-FileHash 翻譯工具_v1.0.zip` 驗證。

## 已知限制

- 部分以「以系統管理員身分執行」的遊戲，全域熱鍵需要本程式也用同樣權限執行才能攔截
- 首次使用 OCR 會自動下載模型（約 400 MB / 引擎），請確保有網路連線
- 系統匣 / 開機自動啟動為選用功能，可在「設定 → 一般」開關

## 問題回報

[GitHub Issues](https://github.com/brokenblack/manga-TCNtranslator/issues)

授權：MIT
