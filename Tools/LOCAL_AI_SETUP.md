# Local AI 環境設定

> 適用於 Mac M1 Pro 16GB | 最後更新：2026-05-04

---

## Ollama

### 安裝

```bash
brew install ollama
brew services start ollama
```

### 已下載的模型

| 模型 | 大小 | 用途 |
|------|------|------|
| `qwen2.5-coder:1.5b` | 986 MB | 自動補全 (極快, ~1GB RAM) |
| `llama3.2:3b` | 2.0 GB | 對話 + 編輯 (~2GB RAM) |
| `qwen2.5-coder:7b` | 4.7 GB | 重度任務 (~5GB RAM, 慎用) |

```bash
ollama pull qwen2.5-coder:1.5b
ollama pull llama3.2:3b
ollama pull qwen2.5-coder:7b
```

### 記憶體優化 (16GB 機器必要)

plist 位置：`~/Library/LaunchAgents/homebrew.mxcl.ollama.plist`

```xml
<key>EnvironmentVariables</key>
<dict>
    <key>OLLAMA_FLASH_ATTENTION</key>
    <string>1</string>
    <key>OLLAMA_KV_CACHE_TYPE</key>
    <string>q8_0</string>
    <key>OLLAMA_KEEP_ALIVE</key>
    <string>2m</string>
    <key>OLLAMA_MAX_LOADED_MODELS</key>
    <string>1</string>
</dict>
```

| 參數 | 值 | 說明 |
|------|---|------|
| `OLLAMA_FLASH_ATTENTION` | 1 | M1 Pro 加速推理 |
| `OLLAMA_KV_CACHE_TYPE` | q8_0 | KV Cache 量化省記憶體 |
| `OLLAMA_KEEP_ALIVE` | 2m | 閒置 2 分鐘卸載模型 |
| `OLLAMA_MAX_LOADED_MODELS` | 1 | 同時只載入 1 個模型 |

修改後重啟：

```bash
brew services stop ollama
brew services start ollama
```

### API

```
http://localhost:11434
```

快速測試：

```bash
curl http://localhost:11434/api/tags
ollama run qwen2.5-coder:1.5b "print hello world in python"
```

---

## Continue.dev (VS Code)

### 安裝

VS Code → `⌘+Shift+X` → 搜尋 `Continue` → Install

### 設定檔

位置：`~/.continue/config.yaml`

```yaml
name: ForestScanner Dev Config
version: 0.0.1
schema: v1

models:
  # 日常對話 + 編輯 (~2GB RAM)
  - name: Llama 3.2 3B
    provider: ollama
    model: llama3.2:3b
    apiBase: http://localhost:11434
    roles: [chat, edit, apply]

  # 自動補全 (~1GB RAM)
  - name: Qwen Coder 1.5B (autocomplete)
    provider: ollama
    model: qwen2.5-coder:1.5b
    apiBase: http://localhost:11434
    roles: [autocomplete]

  # 重度任務 (~5GB RAM, 手動切換)
  - name: Qwen Coder 7B (heavy)
    provider: ollama
    model: qwen2.5-coder:7b
    apiBase: http://localhost:11434
    roles: [chat, edit]

  # (可選) 雲端模型
  # - name: Gemini Flash
  #   provider: google-genai
  #   model: gemini-2.5-flash
  #   apiKey: YOUR_GEMINI_API_KEY
  #   roles: [chat, edit]

context:
  - provider: file
  - provider: code
  - provider: terminal
  - provider: folder
```

### 快捷鍵

| 快捷鍵 | 功能 |
|--------|------|
| `⌘+L` | 開啟 AI 對話 |
| `⌘+I` | 在程式碼裡叫 AI 編輯 |
| `Tab` | 接受自動補全 |
| `⌘+Shift+L` | 把選取的程式碼加到對話 |

---

## Open WebUI

```bash
# 已在 docker-compose.tools.yml 中定義
docker compose -f Tools/docker-compose.tools.yml up -d
```

- URL: http://localhost:3000
- 自動接 Ollama (localhost:11434)
- 用途：一般問答、文件分析

---

## 記憶體預算 (M1 Pro 16GB)

```
日常開發 (Xcode + Windsurf + Docker + 1.5B 補全):
├── macOS + IDE:     ~5 GB
├── Docker (容器):    ~1.7 GB
├── Ollama 1.5B:     ~1 GB
└── 剩餘:            ~8 GB ✅

需要 AI 對話 (切到 3B):
├── macOS + IDE:     ~5 GB
├── Docker:          ~1.7 GB
├── Ollama 3B:       ~2 GB
└── 剩餘:            ~7 GB ✅

跑 7B 重度任務 (建議先停 Docker):
├── macOS + IDE:     ~5 GB
├── Ollama 7B:       ~5 GB
└── 剩餘:            ~6 GB ⚠️ 剛好
```

釋放記憶體跑 7B：

```bash
docker stop open-webui it-tools
# 用完再啟動
docker start open-webui it-tools
```

---

## Windows 設定 (之後)

Windows 那台 (4080 + 64GB) 可以跑更大的模型：

```bash
# 安裝 Ollama (Windows)
winget install Ollama.Ollama

# 拉大模型
ollama pull deepseek-r1:32b
ollama pull qwen2.5-coder:32b
ollama pull llama3.1:70b
```

Windows 不需要記憶體限制，64GB 夠跑 70B。

---

## 開發策略

| 工具 | 角色 | 費用 |
|------|------|------|
| **Windsurf (Cascade)** | 主力：架構、重構、複雜邏輯 | $200/mo |
| **Continue.dev + Ollama** | 輔助：補全、快速問答 | 免費 |
| **Open WebUI** | 一般對話、文件分析 | 免費 |
| **Xcode 26 Intelligence** | iOS 開發專用 (接 Ollama) | 免費 |

> 主力開發用 Windsurf，SLM 訓練等需要時再導入。
