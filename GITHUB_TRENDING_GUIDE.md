# 2025-2026 GitHub 熱門專案分類指南

按照你的需求分類，標注與你森林 SaaS 的關聯性、學習優先順序，以及如何利用。

---

## A. AI Agent 和 LLM 工具 (最熱門賽道)

### 2026 新王者

| 專案 | Stars | 說明 | 對你的價值 |
|------|-------|------|-----------|
| **[OpenClaw](https://github.com/nicepkg/openclaw)** | 210k+ | 2026 爆紅王！個人 AI 助手，完全本地運行，接 WhatsApp/Telegram/iMessage，能自己寫新技能 | 可以讓它自動監控你的 SaaS 服務 + 自動回覆客戶訊息 |
| **[Gemini CLI](https://github.com/google-gemini/gemini-cli)** | 新 | Google 官方：終端機裡直接用 Gemini 多模態模型 | 命令列 AI 助手，自動化腳本 + CI/CD |
| **[Claude Code](https://github.com/anthropics/claude-code)** | 新 | Anthropic 的 Agentic Coding 工具，理解整個 codebase | 跟 Windsurf 同類但終端導向，可互補 |
| **[Open WebUI](https://github.com/open-webui/open-webui)** | 124k+ | 自架 ChatGPT 替代，接 Ollama，支援 RAG / 語音 / 視頻 | 團隊內部 AI 平台，不花 API 錢 |
| **[DeepSeek-V3](https://github.com/deepseek-ai/DeepSeek-V3)** | 30k+ | 開源模型匹敵 GPT-4，128K context，免費商用 | Ollama 跑 DeepSeek = 免費的 GPT-4 級別本地 AI |

### 經典款 (持續成長)

| 專案 | Stars | 說明 | 對你的價值 |
|------|-------|------|-----------|
| **[Ollama](https://github.com/ollama/ollama)** | 120k+ | 本地運行 LLM 的標準工具 | 在 Mac Pro 上跑本地 AI，不花 API 錢 |
| **[LangChain](https://github.com/langchain-ai/langchain)** | 105k+ | LLM 應用開發框架 | 建構 AI pipeline 的標準工具 |
| **[Dify](https://github.com/langgenius/dify)** | 90k+ | 開源 LLM App 開發平台 (RAG + Agent)，支援 MCP | SaaS 加 AI 對話功能 |
| **[Langflow](https://github.com/langflow-ai/langflow)** | 熱門 | 拖拉式 AI Agent 設計工具 (LangChain 視覺化) | 不會寫 code 也能設計 AI 流程 |
| **[OpenHands](https://github.com/All-Hands-AI/OpenHands)** | 52k+ | AI 軟體工程師 agent | 跟 Windsurf 互補，處理你不會的模組 |
| **[RAGFlow](https://github.com/infiniflow/ragflow)** | 70k+ | 企業級 RAG 引擎，支援引用追蹤 | 讓 SaaS 客戶上傳林務法規 AI 自動解讀 |

**學習方式**: 先裝 Ollama + Open WebUI，5 分鐘擁有自己的本地 ChatGPT:
```bash
brew install ollama
ollama run deepseek-v3
# 另開一個終端:
docker run -d -p 3000:8080 -e OLLAMA_BASE_URL=http://host.docker.internal:11434 ghcr.io/open-webui/open-webui:main
```

**與你 SaaS 結合**: 未來可在 SylvaNexus 加入 AI 問答 (巡山員問「這區蓄積量異常原因」)。

---

## B. 自動化流程 (Automation)

| 專案 | Stars | 說明 | 對你的價值 |
|------|-------|------|-----------|
| **[n8n](https://github.com/n8n-io/n8n)** | 65k+ | 視覺化工作流自動化，400+ 整合，可自架 | **高度相關**: SaaS 監控自動化 |
| **[Windmill](https://github.com/windmill-labs/windmill)** | 12k+ | 開源 Retool 替代，腳本+工作流 | 後處理管線視覺化排程 |
| **[Activepieces](https://github.com/activepieces/activepieces)** | 12k+ | 開源 Zapier 替代 | 簡單 webhook 串接 |

**學習方式**:
```bash
docker run -it --rm -p 5678:5678 n8nio/n8n
```

**與你 SaaS 結合的具體場景**:
- GEE 衛星資料更新 -> n8n 觸發 -> 自動跑 gee_volume.py -> LINE 通知巡山員
- iPhone 掃描上傳完成 -> n8n 觸發 -> 自動跑後處理管線 -> 結果入庫
- 每週自動生成 NDVI 變化報告 -> Email 給客戶

---

## C. 股票 / 金融分析工具

| 專案 | Stars | 說明 | 學習價值 |
|------|-------|------|---------|
| **[Freqtrade](https://github.com/freqtrade/freqtrade)** | 50k+ | 開源加密貨幣交易機器人 (Python) | 學策略開發 + 回測框架 + ML 整合 |
| **[QuantConnect/Lean](https://github.com/QuantConnect/Lean)** | 19k+ | 專業量化交易引擎 (C#/Python) | 學多市場串接 + 即時數據處理 |
| **[TradingAgents](https://github.com/TauricResearch/TradingAgents)** | 新專案 | 多 Agent AI 交易系統 (LLM驅動) | 學 AI Agent 協作決策模式 |
| **[awesome-quant](https://github.com/wilsonfreitas/awesome-quant)** | 20k+ | 量化金融資源大全 | 索引：找到你需要的特定工具 |

**學習方式**: Freqtrade 裝起來玩回測即可，不需要真的投錢:
```bash
pip install freqtrade
freqtrade create-userdir
freqtrade backtesting --strategy SampleStrategy
```

**跟你本業的隱藏關聯**: Freqtrade 的「時間序列分析 + 自動決策」架構，跟你的「NDVI 時序監測 + 自動預警」邏輯幾乎相同。

---

## H. Harness Engineering (你問的那個)

### 這是什麼？

Harness Engineering 是 2026 年最重要的新概念，由 **OpenAI Codex 團隊**在 2026 年 2 月提出。

**一句話解釋**: AI Agent (模型) 是馬，Harness (駁具) 是韁繩 + 馬鞍 + 轄頭。沒有 Harness，馬想跑哪就跑哪。

```
Agent = Model + Harness

Model 負責推理 (reasoning)
Harness 負責其他所有事情:
  - 工具編排 (Tool Orchestration): Agent 能用什麼工具
  - 護欄 (Guardrails): Agent 不能做什麼
  - 錯誤回復 (Error Recovery): 失敗時怎麼辦
  - 可觀察性 (Observability): 看得到 Agent 在幹嘆
  - 人類介入點 (Human-in-the-Loop): 哪些決策要人確認
```

### 為什麼重要？

OpenAI 的 Codex 團隊用 3 個工程師 + AI Agent，寫出了 **100 萬行 code，零行是人寫的**。平均每人每天合併 3.5 個 PR。秘密不是模型更強，而是 Harness 設計得好。

LangChain 的實驗也證實：**只改 Harness，不改模型**，就把 coding benchmark 從 52.8% 提升到 66.5%。

### 你已經在用的 Harness

你可能沒意識到，但你已經在做 Harness Engineering 了：

| 你用的工具 | 它的 Harness 機制 | 對應檔案 |
|---------|----------------|----------|
| **Windsurf (Cascade)** | `.windsurf/workflows/*.md` | 工作流定義檔 |
| **Claude Code** | `CLAUDE.md` | 專案指令檔 |
| **OpenAI Codex** | `AGENTS.md` | Agent 行為規範 |
| **Cursor** | `.cursor/rules` | 編輯器規則檔 |

### 實踐應用: 你的森林專案怎麼用

**你可以在 EDGEDEVICE/ 建立一個 Harness 讓 Windsurf 更有效率**:

```
EDGEDEVICE/
  .windsurf/
    workflows/
      build-ios.md          # 怎麼 build iPhone App
      run-postprocessing.md  # 怎麼跑後處理管線
      deploy-saas.md         # 怎麼部署到 Docker
  AGENTS.md                  # AI Agent 的行為規範
  ARCHITECTURE.md            # 已有
  REFERENCE_PROJECTS.md      # 已有
```

`AGENTS.md` 範例:
```markdown
# AGENTS.md - ForestScanner Project

## 規則
- 不要在 iPhone 上跑重度 AI 推理
- LiDAR 只取中心點深度，不存整張深度圖
- 所有時間戳用 Unix timestamp (Double)
- sensor_log.json 格式見 ARCHITECTURE.md 第二節
- Swift code 用 SwiftUI，不用 UIKit (A5 UI 模組除外)
- Python 後處理用 3.11+，型別標註必須
- 不要在 gee_volume.py 裡做廣泛重寫 (SaaS 規則)

## 測試命令
- iOS: xcodebuild test -scheme ForestScanner
- Python: pytest PostProcessing/tests/
- SaaS: docker compose up -d && curl localhost:8082/health
```

### 相關專案 / 資源

| 專案 | 說明 |
|------|------|
| **[awesome-harness-engineering](https://github.com/ai-boost/awesome-harness-engineering)** | Harness Engineering 資源大全 |
| **[AutoHarness](https://github.com/aiming-lab/AutoHarness)** | 自動化 Harness 生成框架 |
| **[OpenAI 原始文章](https://openai.com/index/harness-engineering/)** | Codex 團隊的官方說明 |
| **[Anthropic 文章](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)** | Claude 團隊的 Harness 實踐 |

---

## D. 網頁設計 / Landing Page / 集客行銷

| 專案 | Stars | 說明 | 對你的價值 |
|------|-------|------|-----------|
| **[SaaS-Boilerplate](https://github.com/ixartz/SaaS-Boilerplate)** | 8k+ | Next.js + Tailwind + Auth + 多租戶 | **直接相關**: 你的 SylvaNexus 前端可以參考 |
| **[next-saas-starter](https://github.com/Blazity/next-saas-starter)** | 6k+ | Next.js SaaS Landing Page 模板 | hiiforest.com 的行銷頁面可直接用 |
| **[Puck](https://github.com/measuredco/puck)** | 6k+ | Next.js 視覺化頁面編輯器 | 讓客戶自己編輯專案報告頁面 |
| **[Plausible](https://github.com/plausible/analytics)** | 22k+ | 開源隱私友善網站分析 (Google Analytics 替代) | 追蹤 SaaS 訪客行為 |
| **[Umami](https://github.com/umami-software/umami)** | 25k+ | 開源網站分析，極簡 | 輕量版訪客追蹤 |
| **[PostHog](https://github.com/PostHog/posthog)** | 25k+ | 產品分析 + A/B 測試 + Session 回放 | **集客測試**: 追蹤客戶在 SaaS 裡的行為路徑 |
| **[GrowthBook](https://github.com/growthbook/growthbook)** | 7k+ | 開源 A/B 測試 + Feature Flag | 測試不同定價方案 / UI 的效果 |

**學習方式**: 先部署 Plausible 或 Umami 到你的 EC2 上，追蹤 hiiforest.com 流量:
```bash
# Plausible 一鍵部署
docker compose -f docker-compose.yml up -d
```

**集客行銷路徑**:
1. `next-saas-starter` -> 建 hiiforest.com Landing Page
2. `Plausible` -> 追蹤訪客從哪來
3. `PostHog` -> A/B 測試定價頁面
4. `GrowthBook` -> Feature Flag 控制功能開放

---

## E. 開發效率工具

| 專案 | Stars | 說明 | 對你的價值 |
|------|-------|------|-----------|
| **[Puppeteer](https://github.com/puppeteer/puppeteer)** | 90k+ | 瀏覽器自動化 (Google 官方) | 自動化測試你的 SaaS 前端 |
| **[ShellCheck](https://github.com/koalaman/shellcheck)** | 37k+ | Shell 腳本語法檢查 | 確保部署腳本不出錯 |
| **[HTTPie](https://github.com/httpie/cli)** | 35k+ | 人性化 HTTP 客戶端 | 比 curl 好用 100 倍，測試 API |
| **[it-tools](https://github.com/CorentinTh/it-tools)** | 28k+ | IT 工具箱 (base64, hash, JWT 解碼等) | 日常開發小工具集 |
| **[Hoppscotch](https://github.com/hoppscotch/hoppscotch)** | 71k+ | 開源 Postman 替代 | 測試 SaaS API endpoint |
| **[Tabby](https://github.com/Eugeny/tabby)** | 30k+ | 現代化終端機模擬器 | SSH 進 EC2 更方便 |
| **[DevDocs](https://github.com/freeCodeCamp/devdocs)** | 36k+ | 離線 API 文件瀏覽器 | 在森林沒網路時查文件 |
| **[Lapce](https://github.com/lapce/lapce)** | 35k+ | Rust 寫的超快程式碼編輯器 | 輕量替代方案 (但你已有 Windsurf) |

**最推薦先裝**: HTTPie + ShellCheck + Gemini CLI + it-tools
```bash
brew install httpie shellcheck
npx @anthropic-ai/claude-code   # Claude Code (如果你有 API key)
npx @anthropic-ai/gemini-cli    # 或 Gemini CLI
# it-tools 自架
docker run -d -p 8080:80 corentinth/it-tools
```

---

## F. 硬體效能 / 系統優化

| 專案 | Stars | 說明 | 對你的價值 |
|------|-------|------|-----------|
| **[PowerToys](https://github.com/microsoft/PowerToys)** | 28k+ | Windows 系統強化工具集 | 如果你有 Windows 機器 |
| **[Asahi Linux](https://github.com/AsahiLinux)** | 活躍 | Apple Silicon 上跑 Linux | Mac Pro 上跑 GPU 計算 (非 macOS 限制) |
| **[macOS-defaults](https://github.com/yannbertrand/macos-defaults)** | 活躍 | macOS 隱藏設定大全 | 優化 Mac Pro 開發環境 |
| **[iStats](https://github.com/Chris911/iStats)** | 活躍 | Mac 硬體溫度/風扇監控 (CLI) | 監控 YOLO 訓練時的 M1 Pro 溫度 |

**與你相關的效能優化重點**:
- M1 Pro MPS (Metal Performance Shaders) -> YOLO 訓練加速
- macOS 的 GPU 計算不需要「超頻」，Apple Silicon 是固定頻率
- 真正的瓶頸在記憶體頻寬，M1 Pro 16GB 的統一記憶體是硬限制
- 如果需要更強 GPU，考慮 EC2 (你已有 AWS) 而非本地超頻

---

## G. 自架服務 (Self-Hosted，與你 EC2/Docker 直接相關)

| 專案 | Stars | 說明 | 對你的價值 |
|------|-------|------|-----------|
| **[Immich](https://github.com/immich-app/immich)** | 60k+ | 自架 Google Photos 替代 | 管理大量森林現場照片/影片 |
| **[Nextcloud](https://github.com/nextcloud/server)** | 29k+ | 自架雲端硬碟 | 巡山員上傳掃描資料的私有雲 |
| **[Uptime Kuma](https://github.com/louislam/uptime-kuma)** | 65k+ | 服務監控面板 | 監控你的 SaaS Docker 服務狀態 |
| **[Portainer](https://github.com/portainer/portainer)** | 32k+ | Docker 視覺化管理 | EC2 上管理 Docker 容器更方便 |
| **[Coolify](https://github.com/coollabsio/coolify)** | 40k+ | 自架 Heroku/Vercel 替代 | 一鍵部署你的 SaaS 到 EC2 |

**最推薦先裝**: Uptime Kuma + Portainer (5 分鐘搞定)
```bash
# Uptime Kuma - 監控 SaaS 服務是否在線
docker run -d -p 3001:3001 louislam/uptime-kuma

# Portainer - Docker 視覺化管理
docker run -d -p 9000:9000 -v /var/run/docker.sock:/var/run/docker.sock portainer/portainer-ce
```

---

## 三台機器分工策略 (Mac + Windows + EC2)

### 現況

| 機器 | 角色 | 系統 | 特長 |
|------|------|------|------|
| **Mac** (M1 Pro 16GB) | 開發機 + iPhone 開發 | macOS, Docker, Xcode, Windsurf | Apple Silicon GPU (MPS), Xcode |
| **Windows** | SaaS 本地開發 + Docker 鏡像 | Windows + Docker Desktop / WSL2 | 可能有獨顯 GPU (CUDA), 較大記憶體 |
| **EC2 AWS** | 生產環境 + 24/7 服務 | Linux | 彈性擴展, 公網 IP, S3 |

### 每台機器裝什麼

```
╔════════════════════╦════════════════════╦════════════════════╗
║  Mac (M1 Pro)      ║  Windows (Docker)  ║  EC2 (Production)  ║
╠════════════════════╬════════════════════╬════════════════════╣
║ Xcode + Windsurf   ║ Docker Desktop     ║ SaaS Docker Stack  ║
║ Ollama + DeepSeek  ║ SaaS Docker Stack  ║ Uptime Kuma        ║
║ Open WebUI         ║ (dev 鏡像)         ║ Portainer          ║
║ HTTPie + ShellCheck║ Ollama (NVIDIA GPU)║ Plausible/Umami    ║
║ YOLO 訓練 (MPS)    ║ YOLO 訓練 (CUDA)   ║ n8n                ║
║ Python 後處理開發   ║ COLMAP (GPU)       ║ PostHog            ║
║ it-tools           ║ Python 後處理開發   ║ Nginx + SSL        ║
╚════════════════════╩════════════════════╩════════════════════╝
```

### 安裝命令對照表

#### Mac (你現在這台)

```bash
# Tier 1: 5 分鐘
brew install httpie shellcheck
brew install ollama
ollama pull deepseek-v3

# Tier 1: Open WebUI (Ollama 的網頁介面)
docker run -d --name open-webui -p 3000:8080 \
  -e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
  -v open-webui:/app/backend/data \
  ghcr.io/open-webui/open-webui:main

# Tier 1: it-tools
docker run -d --name it-tools -p 8070:80 corentinth/it-tools
```

#### Windows (Docker Desktop + WSL2)

```powershell
# Docker Desktop 裡的 WSL2 終端:
# SaaS 開發鏡像 (跟 EC2 同一份 docker-compose.yml)
cd D:\SylvaNexus_Workspace\SylvaNexus_Platform
docker compose up -d

# Ollama (Windows 原生安裝器下載)
# https://ollama.com/download/windows
# 安裝後:
ollama pull deepseek-v3

# 如果有 NVIDIA GPU:
# YOLO 訓練用 CUDA 會比 Mac MPS 快很多
pip install ultralytics
python -c "from ultralytics import YOLO; m=YOLO('yolov10n.pt'); m.train(data='coco8.yaml', epochs=3, device=0)"
```

#### EC2 (Production)

```bash
# SSH 進入後:
# Tier 1: Uptime Kuma (監控 SaaS)
docker run -d --name uptime-kuma -p 3001:3001 \
  -v uptime-kuma:/app/data \
  --restart unless-stopped \
  louislam/uptime-kuma

# Tier 1: Portainer (Docker 管理)
docker run -d --name portainer -p 9000:9000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  --restart unless-stopped \
  portainer/portainer-ce

# Tier 2: n8n (自動化)
docker run -d --name n8n -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  --restart unless-stopped \
  n8nio/n8n

# Tier 2: Plausible (網站分析)
# 參考: https://github.com/plausible/community-edition
git clone https://github.com/plausible/community-edition plausible
cd plausible && docker compose up -d
```

### 同步策略: 三台機器怎麼保持一致

```
程式碼同步: Git (已有)
  Mac  ← git push/pull →  GitHub  ← git push/pull →  Windows
                               │
                         EC2 自動 pull (n8n 或 webhook)

Docker 鏡像同步: 同一份 docker-compose.yml
  Windows (dev) 跟 EC2 (prod) 用同一份
  差異只在 .env 檔 (DB 密碼、API Key 等)

資料同步: S3
  iPhone 掃描結果 → S3 → 三台都能存取
  後處理結果 → S3 → SaaS API 讀取

大檔案 (點雲/360影片): S3 + aws s3 sync
  不進 Git！太大了
  Mac/Windows 處理完 → aws s3 sync ./output s3://hiiforest-assets/scans/
```

### 各工具該裝在哪

| 工具 | Mac | Windows | EC2 | 原因 |
|------|-----|---------|-----|------|
| **Ollama** | ✅ | ✅ | ❌ | 本地開發用，EC2 沒 GPU 不划算 |
| **Open WebUI** | ✅ | ✅ | ❌ | 接 Ollama，跟著 Ollama 走 |
| **HTTPie** | ✅ | ✅ | ✅ | 三台都要測 API |
| **ShellCheck** | ✅ | ❌ | ✅ | Mac + EC2 用 bash，Windows 用 PowerShell |
| **Uptime Kuma** | ❌ | ❌ | ✅ | 只需要在 prod 監控 |
| **Portainer** | ❌ | ✅ | ✅ | 管理 Docker，Mac 用 Docker Desktop 就夠 |
| **n8n** | ❌ | ❌ | ✅ | 自動化要 24/7 運行 |
| **Plausible** | ❌ | ❌ | ✅ | 網站分析要公網 |
| **PostHog** | ❌ | ❌ | ✅ | A/B 測試要公網 |
| **it-tools** | ✅ | ✅ | ❌ | 本地開發小工具 |
| **YOLO 訓練** | ✅ MPS | ✅ CUDA | ❌ | 用本地 GPU |
| **COLMAP** | ✅ | ✅ | ❌ | SfM 重建用本地 GPU |
| **Xcode** | ✅ | ❌ | ❌ | 只有 Mac 能跑 |
| **Windsurf** | ✅ | ✅ | ❌ | 兩台開發機都裝 |

### docker-compose.yml 的管理方式

```
SaaSDocker/
  docker-compose.yml          # 基礎服務 (postgres, backend, gis, frontend)
  docker-compose.override.yml # 本地開發用 (自動產生, 不進 git)
  docker-compose.ec2.yml      # EC2 生產環境 (你已有)
  docker-compose.tools.yml    # 新增: 監控/分析工具

# 本地開發 (Mac 或 Windows):
docker compose up -d

# EC2 生產:
docker compose -f docker-compose.yml -f docker-compose.ec2.yml up -d

# EC2 監控工具:
docker compose -f docker-compose.tools.yml up -d
```

---

## 學習進度分配建議

你的時間有限，以下是按「對你事業的 ROI」排序：

### Tier 1: 本週就裝 (直接提升開發效率)

| 專案 | 花費時間 | 效果 |
|------|---------|------|
| HTTPie | 5 分鐘 | 測 API 速度提升 10 倍 |
| ShellCheck | 5 分鐘 | 部署腳本不再出錯 |
| Uptime Kuma | 10 分鐘 | 知道 SaaS 有沒有掛 |
| Ollama | 15 分鐘 | 本地跑 AI，理解 LLM |

### Tier 2: 本月學 (與 SaaS 營運直接相關)

| 專案 | 花費時間 | 效果 |
|------|---------|------|
| n8n | 2 小時 | 自動化 GEE 更新 + 通知流程 |
| Plausible/Umami | 1 小時 | 開始追蹤 hiiforest.com 訪客 |
| PostHog | 3 小時 | A/B 測試定價方案 |
| Portainer | 30 分鐘 | EC2 Docker 管理視覺化 |

### Tier 3: 下個月學 (擴展能力)

| 專案 | 花費時間 | 效果 |
|------|---------|------|
| Dify / LangChain | 1 天 | 在 SaaS 裡加 AI 功能 |
| next-saas-starter | 1 天 | 重建 hiiforest.com Landing Page |
| Freqtrade (回測) | 半天 | 學時間序列分析架構 (可應用到 NDVI 監測) |
| GrowthBook | 半天 | Feature Flag 控制新功能上線 |

### Tier 4: 有空再看 (擴展視野)

| 專案 | 說明 |
|------|------|
| Coolify | 如果想簡化 EC2 部署 |
| Immich | 如果需要管理大量現場照片 |
| Nextcloud | 如果需要私有雲檔案管理 |
| Lapce | 如果想試試別的編輯器 |

---

## 隱藏組合技 (對你的 SaaS 最有價值的串接)

```
組合 1: n8n + Ollama + SaaS
  GEE 衛星偵測到 NDVI 異常
    -> n8n 觸發 Ollama 本地 AI 分析原因
    -> 自動生成中文報告
    -> LINE 通知巡山員 + 在 SaaS 上標記警示區域

組合 2: PostHog + GrowthBook + SaaS
  追蹤客戶在 SaaS 裡最常用哪些功能
    -> A/B 測試不同 UI 版本
    -> 用數據決定 Premium 方案該包含什麼功能

組合 3: n8n + iPhone App + 後處理管線
  巡山員上傳掃描資料
    -> n8n 偵測新檔案
    -> 自動觸發 Python 後處理 (Mac Pro)
    -> 完成後自動入庫 SaaS
    -> 通知巡山員「你的掃描結果好了」

組合 4: Plausible + next-saas-starter + hiiforest.com
  漂亮的 Landing Page + 隱私友善的訪客分析
    -> 知道客戶從哪裡來 (Google? 林務局網站? 學術會議?)
    -> 優化行銷策略
```
