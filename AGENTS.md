# AGENTS.md - ForestScanner Edge-to-Cloud Project

## 專案概覽

ForestScanner 是一套森林調查系統，包含三個模組：
- **ForestScanner/** — iPhone App (Swift/SwiftUI, ARKit, CoreML)
- **PostProcessing/** — Mac Pro 後處理管線 (Python 3.11+)
- **Tools/** — Docker 工具容器 (監控/自動化)

完整架構見 ARCHITECTURE.md

## 非協商規則

### iPhone App (ForestScanner/)
- 不在 iPhone 上跑重度 AI 推理，只做輕量標記
- LiDAR 只取中心點深度，不存整張深度圖
- 所有時間戳用 Unix timestamp (Double, seconds since epoch)
- sensor_log.json 格式見 ARCHITECTURE.md 第二節 Data Contract
- Swift code 用 SwiftUI，不用 UIKit (ARView 除外)
- 目標裝置: iPhone 13 Pro, iOS 17+
- 不要引入不必要的第三方 dependency

### Python 後處理 (PostProcessing/)
- Python 3.11+，所有函數必須有型別標註
- 用 pathlib 處理路徑，不用 os.path
- 每個模組都要有對應的 tests/
- 圖像處理用 OpenCV，點雲用 Open3D
- YOLO 用 ultralytics 套件
- 不要硬寫絕對路徑，用設定檔或環境變數

### SaaS 整合
- 不要廣泛重寫 gee_volume.py (SaaS 非協商規則)
- 不要公開 restricted Taiwan raster outputs
- 新 API endpoint 格式對齊現有 gis.py 的風格
- Docker-first: 所有新服務必須有 Dockerfile

## 測試命令

```bash
# Python 後處理
cd PostProcessing && pytest tests/ -v

# Docker 服務健康檢查
docker compose -f Tools/docker-compose.tools.yml ps

# SaaS 健康檢查
curl http://localhost:8082/health
```

## 目錄結構

```
EDGEDEVICE/
├── AGENTS.md                    # 本檔案 (AI Agent 行為規範)
├── ARCHITECTURE.md              # 完整架構文件
├── REFERENCE_PROJECTS.md        # 參考專案指南
├── GITHUB_TRENDING_GUIDE.md     # GitHub 工具指南
├── ForestScanner/               # iPhone App (Xcode project)
│   └── (Phase 1 開始建立)
├── PostProcessing/              # Python 後處理管線
│   ├── requirements.txt
│   ├── pipeline/                # 核心處理邏輯
│   │   ├── panorama_split.py    # 360 → 6 分鏡 (py360convert)
│   │   ├── sfm_reconstruct.py   # SfM 重建 (COLMAP wrapper)
│   │   ├── tree_detect.py       # YOLO 樹木偵測
│   │   ├── pointcloud_dbh.py    # 點雲 → DBH 萃取 (Open3D)
│   │   └── export_geojson.py    # 輸出 GeoJSON → SaaS
│   └── tests/
├── Models/                      # ML 模型檔案
│   └── (YOLO .mlpackage, .pt)
├── ScanData/                    # 掃描原始資料 (不進 git)
│   └── (sensor_log.json, video_360.insv)
├── Tools/                       # Docker 工具
│   └── docker-compose.tools.yml
└── .windsurf/
    └── workflows/
```

## 檔案大小限制

- ScanData/ 和 Models/ 裡的大檔案不進 Git
- .gitignore 已設定排除 *.insv, *.ply, *.laz, *.pt, *.mlpackage
