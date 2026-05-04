# ForestScanner — 產品架構與開發流程總覽

## 系統全景：SylvaNexus Edge-to-Cloud Pipeline

```
┌─────────────────────────────────────────────────────────────────────┐
│                        現場 (FIELD)                                  │
│                                                                     │
│   ┌──────────────┐         ┌──────────────┐                        │
│   │  iPhone 13   │ USB/BLE │  360 Camera  │                        │
│   │  Pro App     │◄───────►│  (Insta360/  │                        │
│   │              │  sync   │   Ricoh)     │                        │
│   │  - ARKit     │         │              │                        │
│   │  - LiDAR     │         │  8K → SD卡   │                        │
│   │  - IMU       │         └──────────────┘                        │
│   │  - CoreML    │                                                  │
│   │  - GPS       │                                                  │
│   └──────┬───────┘                                                  │
│          │ sensor_log.json                                          │
│          │ ai_metadata.json                                         │
│          │ thumbnail_frames/                                        │
└──────────┼──────────────────────────────────────────────────────────┘
           │
           ▼  上傳 (Wi-Fi / 回家)
┌──────────┴──────────────────────────────────────────────────────────┐
│                     Mac Pro 本地 / EC2 雲端                          │
│                                                                     │
│   ┌────────────────────────────────────────────────────────────┐   │
│   │  後處理管線 (Python)                                        │   │
│   │                                                            │   │
│   │  1. sync_align.py — 對齊 sensor_log + SD卡 360影片時間戳    │   │
│   │  2. frame_extract.py — 從 8K 影片抽取 Keyframes            │   │
│   │  3. dewarping.py — 全景 → 6 × 72° 透視分鏡 (OpenCV)        │   │
│   │  4. yolo_detect.py — YOLOv10 跑 6 分鏡 → 樹幹/樹種辨識     │   │
│   │  5. scale_recovery.py — LiDAR 錨點 × 視覺距離 → 真實尺度    │   │
│   │  6. sfm_pipeline.py — COLMAP / ODM → 3D 點雲 + Mesh        │   │
│   │  7. tree_measure.py — 從點雲/Mesh 萃取 DBH / 樹高           │   │
│   │  8. export_to_saas.py — 打包 GeoJSON → 上傳 SylvaNexus API  │   │
│   └────────────────────────────────────────────────────────────┘   │
└──────────┬──────────────────────────────────────────────────────────┘
           │
           ▼  REST API (JSON / GeoJSON)
┌──────────┴──────────────────────────────────────────────────────────┐
│              SylvaNexus SaaS Platform (Docker)                      │
│                                                                     │
│   ┌──────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────┐ │
│   │ frontend │  │  backend     │  │ gis-service   │  │ postgres │ │
│   │ :8082    │  │  :8002       │  │ :8080        │  │ +PostGIS │ │
│   │          │  │  auth/JWT    │  │              │  │  :5433   │ │
│   │ SylvaApp │  │  Cognito     │  │ gee_volume   │  │          │ │
│   │ .js      │  │  payment     │  │ gis.py       │  │ 蓄積量    │ │
│   │          │  │  upload API  │  │ lidar_proc   │  │ 林相      │ │
│   │ Leaflet  │  │  S3 bridge   │  │ sfm_ingest◄──NEW│ 掃描結果  │ │
│   │ 地圖+3D  │  │              │  │ field_scan◄──NEW│          │ │
│   └──────────┘  └──────────────┘  └──────────────┘  └──────────┘ │
│                                                                     │
│   現有功能: GEE 衛星 / NDVI / 蓄積量 / 水文 / 林相 / 路網            │
│   新增功能: 地面掃描資料匯入 / 點雲瀏覽 / 現場照片 / DBH 校驗        │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 一、產品模組拆解

### Module A — iPhone 採集 App (Swift / Xcode)

| 子模組 | 技術 | 輸出 | 優先順序 |
|--------|------|------|---------|
| **A1. ARKit 感測器紀錄器** | ARKit + CoreMotion | `sensor_log.json` (IMU 位姿 + LiDAR 中心深度 + 時間戳) | P0 — 第1週 |
| **A2. 外部 360 相機控制** | AVCaptureDevice (UVC) / Insta360 SDK | 錄影啟動同步 + 低畫質預覽流 | P1 — 第2週 |
| **A3. Metal 六角分鏡 Shader** | Metal GPU | 6 × 72° 透視切片 (預覽用) | P2 — 第3週 |
| **A4. CoreML 即時標記 (輕量)** | Vision + YOLOv10n | `ai_metadata.json` (哪秒/哪分鏡/什麼樹) | P2 — 第3週 |
| **A5. 導覽 UI** | SwiftUI | S行走法軌跡圖 + 雷射測距顯示 + 速度警示 + 閉環提示 | P1 — 第2週 |
| **A6. 資料匯出** | FileManager + ZIP | 打包 sensor_log + ai_metadata + 縮圖 → AirDrop/iCloud | P1 — 第2週 |

### Module B — 後處理管線 (Python / Mac Pro)

| 子模組 | 技術 | 輸入 | 輸出 | 優先順序 |
|--------|------|------|------|---------|
| **B1. 時間戳對齊** | NumPy interpolation | sensor_log.json + 360 影片 metadata | aligned_frames.csv | P0 |
| **B2. 影格提取** | FFmpeg / OpenCV | 8K .insv/.mp4 | Keyframes (JPEG) | P0 |
| **B3. 全景分鏡** | OpenCV (py360convert) | Equirectangular → 6 × Perspective | 透視圖 (PNG) | P1 |
| **B4. YOLO 全量辨識** | ultralytics YOLOv10-L | 6 分鏡圖 | detections.json (bbox + class + conf) | P1 |
| **B5. 尺度還原** | LiDAR depth anchor | sensor_log LiDAR 距離 + 視覺距離 | scale_factor | P1 |
| **B6. SfM / 3D 重建** | COLMAP / WebODM | Keyframes + 位姿 | 點雲 (.ply) / Mesh (.obj) | P2 |
| **B7. 單木萃取** | Open3D / DBSCAN | 點雲 + YOLO bbox | tree_inventory.csv (DBH, 樹高, 座標, 樹種) | P2 |
| **B8. SaaS 匯出** | requests / boto3 | tree_inventory + GeoJSON | POST → SylvaNexus API | P2 |

### Module C — SaaS 平台擴充 (SylvaNexus Docker)

| 子模組 | 技術 | 改動位置 | 優先順序 |
|--------|------|---------|---------|
| **C1. field_scan 匯入 API** | FastAPI endpoint | `gis-service/app/api/endpoints/field_scan.py` (新檔) | P2 |
| **C2. 掃描結果入庫** | PostGIS | `field_scans` + `trees` 表 | P2 |
| **C3. 前端 - 單木圖層** | Leaflet / SylvaApp.js | 地圖上顯示每棵樹的 DBH/樹種 pin | P3 |
| **C4. 前端 - 點雲瀏覽** | Potree / Three.js | 3D 點雲線上檢視 | P3 |
| **C5. GEE × 地面校驗** | Python | 比對 GEE 蓄積量 vs 地面掃描 DBH → 校正係數 | P3 |

---

## 二、資料格式規範 (Data Contract)

### sensor_log.json — iPhone 輸出

```json
{
  "device": "iPhone13Pro",
  "session_id": "scan_20260504_001",
  "start_time_unix": 1746297600.000,
  "sync_offset_sec": 0.032,
  "frames": [
    {
      "t": 0.000,
      "pose": [
        [1,0,0,0],
        [0,1,0,0],
        [0,0,1,0],
        [0,0,0,1]
      ],
      "accel": [0.01, -9.78, 0.03],
      "gyro": [0.001, -0.002, 0.000],
      "gps": { "lat": 24.2345, "lon": 120.8765, "accuracy": 8.5 },
      "lidar_center_m": 3.42
    }
  ]
}
```

### ai_metadata.json — iPhone 即時標記

```json
{
  "session_id": "scan_20260504_001",
  "detections": [
    {
      "t": 12.500,
      "panel_id": 2,
      "class": "trunk",
      "confidence": 0.87,
      "bbox_norm": [0.3, 0.2, 0.15, 0.6]
    }
  ]
}
```

### tree_inventory.csv — 後處理輸出 → SaaS 匯入

```csv
tree_id,lat,lon,species,dbh_cm,height_m,confidence,scan_session,timestamp
T001,24.2345,120.8765,Camphor,35.2,18.5,0.92,scan_20260504_001,2026-05-04T10:30:00
T002,24.2347,120.8763,Cypress,42.1,22.3,0.88,scan_20260504_001,2026-05-04T10:30:05
```

### SaaS API — field_scan 匯入端點 (新增)

```
POST /api/v1/{project_id}/field-scans
Content-Type: multipart/form-data

Body:
  - tree_inventory.csv
  - scan_metadata.json
  - pointcloud.ply (optional, upload to S3)

Response:
  { "status": "ok", "trees_imported": 127, "scan_id": "FS-20260504-001" }
```

---

## 三、銜接檢查清單 (Integration Checklist)

### iPhone App → 後處理管線

| # | 銜接點 | 驗證方法 | 狀態 |
|---|--------|---------|------|
| 1 | `sensor_log.json` 時間戳格式 (`CACurrentMediaTime`) 能被 Python `json.load` 正確解析 | 寫 unit test | ⬜ |
| 2 | LiDAR 中心深度值 (sceneDepth) 在 5m 內誤差 < 5cm | 實測: 對著牆壁量 + 捲尺比對 | ⬜ |
| 3 | IMU 採樣率 ≥ 30Hz，且每筆都有對應的 ARFrame timestamp | 錄製 1 分鐘後用 Python 繪圖檢查連續性 | ⬜ |
| 4 | 360 相機的錄影啟動時間 (sync_offset_sec) 能正確記錄 | 手動拍手 (聲波 + 視覺) 驗證偏移量 | ⬜ |
| 5 | ai_metadata.json 的 panel_id (0-5) 對應正確的方位角 | 在已知場景測試: 正前方樹 → panel_id=0 | ⬜ |

### 後處理管線 → SaaS 平台

| # | 銜接點 | 驗證方法 | 狀態 |
|---|--------|---------|------|
| 6 | tree_inventory.csv 座標系 = WGS84 (EPSG:4326) | 匯入後在 Leaflet 上顯示位置正確 | ⬜ |
| 7 | DBH 單位 = cm，與 GEE `gee_volume.py` 的 `dbh_cm` 欄位一致 | 比對 Schumacher 模型 vs 實測值 | ⬜ |
| 8 | `field_scan.py` API 可被 frontend SylvaApp.js 正確呼叫 | curl 測試 + 前端 Console 檢查 | ⬜ |
| 9 | 點雲 (.ply) 上傳至 S3 的路徑 = `s3://hiiforest-assets/{project_id}/scans/{scan_id}/` | 從前端能載入並顯示 | ⬜ |
| 10 | 掃描結果能與 GEE 蓄積量 grid 在同一地圖上疊加 | 打開 baxianshan 專案，兩層同時顯示 | ⬜ |

### SaaS 平台內部

| # | 銜接點 | 驗證方法 | 狀態 |
|---|--------|---------|------|
| 11 | `field_scans` 表在 PostgreSQL + PostGIS 中建立 | `docker exec` 進 postgres 檢查 | ⬜ |
| 12 | auth-service JWT 可驗證 App 上傳的 token | 從 iPhone 模擬上傳 + 檢查 401/200 | ⬜ |
| 13 | 前端 project config JSON 新增 `field_scan` layer 定義 | 檢查 baxianshan.json | ⬜ |

---

## 四、開發時程與里程碑

### Phase 1 — 基礎採集 (Week 1-2)

```
目標: iPhone 能穩定紀錄 IMU + LiDAR 測距 + 時間戳
```

- [ ] 在 EDGEDEVICE/ 建立 Xcode 專案 `ForestScanner`
- [ ] 參考 StrayScanner 實作 `ForestDataLogger.swift`
  - ARKit session → 每幀抓取 camera.transform + sceneDepth center
  - CoreMotion → accelerometer + gyroscope (100Hz)
  - 統一輸出 sensor_log.json
- [ ] 實作基本 SwiftUI 錄製介面 (開始/停止/時間顯示)
- [ ] 在 iPhone 13 Pro 上實機測試:
  - 錄製 5 分鐘，確認 JSON 完整無毀損
  - 比對 LiDAR 深度 vs 捲尺 (室內先測)

### Phase 2 — 360 對接 + 導覽 UI (Week 3-4)

```
目標: iPhone 控制 360 鏡頭 + S行走法導覽 + 同步時間戳
```

- [ ] 測試 iPhone 13 Pro 透過 Lightning 讀取 UVC 360 鏡頭
- [ ] 實作同步時間戳機制 (sync_offset_sec)
- [ ] SwiftUI 導覽介面:
  - 即時軌跡小地圖 (ARKit worldTransform)
  - 雷射測距準心 + 數值顯示
  - 速度過快警示
  - 回到起點閉環提示
- [ ] 資料匯出: ZIP 打包 → Files app / AirDrop

### Phase 3 — 後處理管線 MVP (Week 5-7)

```
目標: 從 360 影片 + sensor_log → 產出 tree_inventory.csv
```

- [ ] Python 環境建立 (ultralytics, opencv, colmap, open3d)
- [ ] sync_align.py — 時間戳對齊
- [ ] frame_extract.py — FFmpeg 抽幀
- [ ] dewarping.py — 全景 → 6 分鏡 (用 py360convert)
- [ ] yolo_detect.py — 用通用 YOLOv10 模型先跑
- [ ] scale_recovery.py — LiDAR 錨點定標
- [ ] 初步手動測試: 在身邊森林走一圈 → 產出結果

### Phase 4 — SaaS 對接 (Week 8-9)

```
目標: 掃描結果能匯入 SylvaNexus 並在地圖上顯示
```

- [ ] 新增 `field_scan.py` API endpoint (gis-service)
- [ ] PostgreSQL schema: field_scans + trees 表
- [ ] export_to_saas.py — 自動上傳腳本
- [ ] SylvaApp.js — 新增「地面掃描」圖層
- [ ] 驗證: baxianshan 專案同時顯示 GEE 蓄積量 + 地面 DBH

### Phase 5 — AI 模型訓練 + 精度提升 (Week 10-12)

```
目標: 森林特製 YOLO 模型 + SfM 3D 重建
```

- [ ] 在 Roboflow 收集 + 標註台灣樹種數據
- [ ] M1 Pro 上用 ultralytics 訓練 YOLOv10n (device='mps')
- [ ] 匯出 .mlpackage → Xcode 整合
- [ ] COLMAP / ODM 3D 重建測試
- [ ] GEE 蓄積量 vs 地面量測交叉校驗 → 調整 Schumacher 參數

---

## 五、已有 SaaS 資產 × iPhone App 的銜接點

### gis-service 已有端點 (可直接利用)

| 端點 | 用途 | 與 App 的關係 |
|------|------|--------------|
| `GET /api/v1/projects` | 列出所有專案 | App 選擇要上傳到哪個專案 |
| `GET /api/v1/{project_id}/config` | 取得專案設定 | App 取得掃描區域邊界 + 座標系 |
| `POST /api/v1/gis/analyze/terrain` | 地形分析 | 後處理時自動取得掃描區域的坡度資料 |
| `GET /api/v1/baxianshan/hydrology/*` | 水文分析 | 在 App UI 上疊加危險區域警示 |
| `GET /api/v1/{project_id}/gee-volume/*` | GEE 蓄積量 | 與地面掃描 DBH 交叉比對 |

### gis-service 需新增端點

| 端點 | 方法 | 功能 |
|------|------|------|
| `POST /api/v1/{project_id}/field-scans` | POST | 匯入 tree_inventory + 掃描 metadata |
| `GET /api/v1/{project_id}/field-scans` | GET | 列出該專案所有掃描記錄 |
| `GET /api/v1/{project_id}/field-scans/{scan_id}/trees` | GET | 取得某次掃描的所有樹木資料 (GeoJSON) |
| `GET /api/v1/{project_id}/field-scans/{scan_id}/pointcloud` | GET | 取得點雲 S3 URL |
| `POST /api/v1/{project_id}/calibration/field-vs-gee` | POST | GEE 蓄積量 vs 地面掃描 校驗分析 |

### backend 需確認

| 項目 | 狀態 | 說明 |
|------|------|------|
| JWT auth | ⬜ README 顯示「認證服務」尚未完成 | App 上傳需要認證 token |
| S3 upload | ✅ docker-compose 已有 AWS_S3_BUCKET | 點雲上傳可直接用 |
| 用量追蹤 | ⬜ 訂閱制尚未實作 | 掃描次數/儲存空間需計費 |

---

## 六、檔案目錄規劃

```
EDGEDEVICE/
├── ARCHITECTURE.md              ← 本文件
├── ForestScanner/               ← Xcode 專案 (iPhone App)
│   ├── ForestScanner.xcodeproj
│   ├── ForestScanner/
│   │   ├── App/
│   │   │   ├── ForestScannerApp.swift
│   │   │   └── ContentView.swift
│   │   ├── Core/
│   │   │   ├── ForestDataLogger.swift     ← A1: 感測器紀錄器
│   │   │   ├── LiDARRangeFinder.swift     ← LiDAR 中心點測距
│   │   │   ├── CameraSync.swift           ← A2: 360 同步控制
│   │   │   └── DataExporter.swift         ← A6: ZIP 匯出
│   │   ├── Metal/
│   │   │   ├── PanoramaSlicer.metal       ← A3: 六角分鏡 Shader
│   │   │   └── ShaderTypes.h
│   │   ├── AI/
│   │   │   ├── TreeDetector.swift         ← A4: CoreML YOLO 包裝
│   │   │   └── Models/                    ← .mlpackage 放這裡
│   │   ├── UI/
│   │   │   ├── ScanView.swift             ← A5: 主掃描畫面
│   │   │   ├── TrajectoryMapView.swift    ← 軌跡小地圖
│   │   │   └── LaserOverlayView.swift     ← 雷射準心
│   │   └── Resources/
│   │       └── Info.plist
│   └── ForestScannerTests/
│
├── PostProcessing/              ← Python 後處理管線
│   ├── requirements.txt
│   ├── config.yaml
│   ├── sync_align.py            ← B1
│   ├── frame_extract.py         ← B2
│   ├── dewarping.py             ← B3
│   ├── yolo_detect.py           ← B4
│   ├── scale_recovery.py        ← B5
│   ├── sfm_pipeline.py          ← B6
│   ├── tree_measure.py          ← B7
│   ├── export_to_saas.py        ← B8
│   └── tests/
│
├── Training/                    ← YOLO 模型訓練
│   ├── download_data.py         ← Roboflow 資料下載
│   ├── train_yolo.py            ← M1 Pro MPS 訓練
│   ├── export_coreml.py         ← 匯出 .mlpackage
│   └── datasets/
│       └── forest/
│
└── docs/
    ├── DATA_CONTRACT.md         ← JSON/CSV 格式規範
    └── INTEGRATION_TEST.md      ← 銜接測試腳本
```

---

## 七、並行開發策略

以下事項可以**同時進行**，不互相依賴:

```
時間軸 ──────────────────────────────────────────────►

Week 1-2:
  [你] iPhone App A1 (sensor_log)        ← 最優先
  [你] iPhone App A5 (基本 UI)
  [同時] Python 環境 setup (requirements.txt)
  [同時] 去森林拍 360 影片素材 (未來測試用)

Week 3-4:
  [你] iPhone App A2 (360 控制)
  [同時] B1+B2 用假資料先測通 sync_align + frame_extract
  [同時] 在 Roboflow 搜集/標註樹木數據

Week 5-7:
  [你] B3-B7 後處理管線整合
  [同時] YOLO 模型訓練 (Training/)
  [同時] iPhone App A3+A4 (Metal Shader + CoreML)

Week 8-9:
  [你] C1-C3 SaaS 對接 (field_scan API)
  [同時] 實地掃描測試 + 精度校驗

Week 10-12:
  [你] C4-C5 (點雲瀏覽 + GEE 校驗)
  [同時] 森林特製模型部署到 App
  [同時] TestFlight 外部測試
```

---

## 八、三層數據架構：地面 → 空拍機 → 衛星

```
精度高                                             覆蓋大
 │                                                  │
 │  ┌───────────────────────────────────────┐  │
 │  │ Tier 1: 地面掃描 (iPhone + 360)        │  │
 │  │ ✔ DBH, 樹幹位置, 樹種, 森林結構       │  │
 │  │ ✔ 低成本, 快速, 巡山員可執行          │  │
 │  │ ✘ 樹高, 冠層                           │  │
 │  └───────────────────────────────────────┘  │
 │          │ 校正 DBH                           │
 │          ▼                                      │
 │  ┌───────────────────────────────────────┐  │
 │  │ Tier 2: 空拍機 SfM (+ PPK/GCP)          │  │
 │  │ ✔ 樹高 (CHM), 冠層結構, DSM             │  │
 │  │ ✔ 高精度地理座標 (PPK cm級)          │  │
 │  │ ✔ 與地面 DBH 交叉比對                  │  │
 │  │ ✘ 樹下結構, 成本較高                │  │
 │  └───────────────────────────────────────┘  │
 │          │ 校正樹高 & Schumacher             │
 │          ▼                                      │
 │  ┌───────────────────────────────────────┐  │
 ▼  │ Tier 3: 衛星 (GEE / Sentinel)           │  ▼
    │ ✔ 大面積 NDVI, 時序變化, 風險篩查     │
    │ ✔ 粗略蓄積量估算 (現有 gee_volume.py) │
    │ ✘ 單木級別精度                       │
    └───────────────────────────────────────┘
```

### 各層职責與精度定位

| | Tier 1: 地面 (iPhone+360) | Tier 2: 空拍機 SfM | Tier 3: 衛星 GEE |
|---|---|---|---|
| **核心產出** | DBH, 樹種, 樹幹座標 | 樹高 CHM, DSM, 正射影像 | NDVI, 粗略蓄積量, 時序變化 |
| **精度** | DBH ±1.5cm (迭代後) | 樹高 ±0.5m (PPK+GCP) | 樹高 ±2-5m (粗略) |
| **覆蓋** | 1-5 公頃/次 | 10-50 公頃/次 | 無限 |
| **成本** | 極低 (已有硬體) | 中 (無人機 + RTK base) | 極低 (GEE 免費) |
| **執行者** | 巡山員 | 無人機操作員 | 自動化腳本 |
| **頻率** | 每次巡山 | 季/年 | 月 (Sentinel 5天一回) |
| **SaaS 對接** | field_scan API (新增) | drone_scan API (未來) | gee_volume (已有) |

### 三層交叉校正邏輯

```
地面 DBH 實測 (±1.5cm)
  │
  ├─→ 校正 Tier 3: gee_volume.py SPECIES_MODELS 的 H→DBH 參數 (a, b)
  │   → 衛星蓄積量估算更準
  │
  └─→ 比對 Tier 2: 空拍 SfM 的樹高
      → 驗證 Schumacher H→DBH 公式是否合理
      → 反推樹種特定參數

空拍機樹高 CHM (±0.5m, PPK+GCP)
  │
  ├─→ 校正 Tier 3: GEE 衛星樹高的系統性偏差
  │
  └─→ 結合地面 DBH → 單木材積 (V_tree) 計算
      → 積算成林分蓄積量
```

### 地面掃描能做到的

| 量測項目 | 精度目標 | 方法 | 可行性 |
|---------|---------|------|--------|
| **DBH (胸徑)** | ±1.5cm | LiDAR 測距 + 多角度 RGB 像素寬度 | ✅ 核心目標 |
| **樹幹位置** | ±10cm | ARKit SLAM 座標 + GPS 粗定位 | ✅ |
| **樹種辨識** | Top-3 準確 | YOLO + 樹皮/葉片特徵 | ✅ 需迭代訓練 |
| **地面偵測** | ±5cm | iPhone LiDAR (5m內) + ARKit 平面偵測 | ✅ |
| **1.3m 胸高標記** | ±3cm | LiDAR 地面點 + IMU 高度偏移計算 | ✅ |
| **森林結構概況** | 定性 | 密度/分佈/樹種組成 | ✅ |

### 地面掃描做不到 → 交給誰

| 量測項目 | 為什麼 RGB 不行 | 交給誰 |
|---------|-----------|----------|
| **樹高** | 密林從地面拍不到樹頂，RGB 無穿透力 | **Tier 2: 空拍機 SfM** (PPK + GCP 校正) |
| **冠層結構** | 需要正上方俯視 | **Tier 2: 空拍機** |
| **大面積 NDVI / 時序** | 範圍太小 | **Tier 3: GEE 衛星** |
| **粗略蓄積量篩查** | 不是它的职責 | **Tier 3: GEE** (已有 gee_volume.py) |

### DBH 量測邏輯

```
1. 人員握桿走到樹旁 (距離 2-3m)
2. iPhone LiDAR 偵測地面 → ground_z
3. 1.3m 胸高切面 = ground_z + 1.3
4. 在這個高度上，多角度 360 影像提供樹幹的像素寬度
5. LiDAR 測距提供真實距離 D
6. DBH = 2 × D × tan(像素寬度 / 焦距 × 0.5) × (1/π) 校正為直徑
7. 多角度取平均 → 最終 DBH
```

### 精度迭代策略

精度不是一次到位的。每次掃描都是訓練數據：

```
v0.1 (開發測試)     →  誤差 ±5cm    ← 通用 YOLO + 初始參數
v0.5 (100次掃描)    →  誤差 ±3cm    ← 巡山員捲尺回饋校正演算法
v1.0 (多用戶多樹種)  →  誤差 ±1.5cm  ← 標案交付等級

校正迴路 (三層互校):
  地面 DBH 實測
    → 回饋到 SaaS → 修正 gee_volume.py SPECIES_MODELS (a, b 參數)
    → 比對空拍機樹高 → 驗證 Schumacher H→DBH 公式
    → 衛星估算蓄積量更準
  空拍機樹高 (PPK+GCP)
    → 校正 GEE 衛星樹高的系統性偏差
    → 結合地面 DBH → 得到單木材積 V_tree
```

### 空拍機整合說明 (Tier 2 — 已有數據)

**你已有 300+ 公頃的空拍 SfM / DSM / 正射影像**，Tier 2 不需要從零開始。

- **已有資產**: 正射影像 (.tif) + DSM (.tif) + SfM 點雲，涵蓋 300+ 公頃
- **需要補充**: PPK 後處理校正 + GCP 地面控制點 (視精度需求而定)
- **SaaS 對接**: 未來新增 `drone_scan API`，格式與現有 `gis.py` 的 DEM/DSM 處理流程一致
- **交叉比對**: 同一林區的地面 DBH + 空拍樹高 + GEE 估算，三組數據在 SaaS 中統一顯示
- **當務之急**: 先做好 Tier 1 (地面掃描)，產出 DBH 後即可與既有空拍 DSM 交叉比對

**GEE / 衛星的定位**：低成本快速篩查 + 時序監測，不追求單木精度。
實際標案需要單木級別數據時，由 Tier 1 (地面) + Tier 2 (空拍) 提供。

---

## 九、剛體架 (Rigid Mount) 設計

### 機構示意

```
        ┌──────────┐
        │360 Camera│  ← 頂部: 全景無遮擋
        └────┬─────┘
             │ offset_L (已知, 例如 30cm)
        ┌────┴─────┐
        │ iPhone   │  ← 中段: LiDAR 朝前, 主鏡頭朝外
        │ 13 Pro   │
        └────┬─────┘
             │ 伸縮桿 (碳纖維/鋁合金)
             │ 握把高度 ~1.0-1.2m
        ─────┴───── 地面
```

### 校正參數 (App 內一次性設定)

```swift
struct RigCalibration: Codable {
    let iPhoneTo360OffsetCm: Float    // iPhone 與 360 的垂直距離
    let iPhoneToGroundCm: Float        // iPhone 到桿底距離
    let rigType: String                // "carbon_pole_v1"
}
```

### 為什麼剛體固定是必要的

- **Sensor Fusion 前提**: iPhone IMU 追蹤的是 iPhone 的位姿，360 鏡頭的位姿 = iPhone 位姿 + 固定偏移量 × 旋轉矩陣
- **如果沒固定**: 360 鏡頭相對 iPhone 的位置每秒都在變，時間戳對齊後座標對不上，3D 重建直接崩潰
- **偏移量只需量一次**: 出發前用捲尺量好 offset_L，App 裡設定完就不動了

### 連續掃描工作流

```
巡山員操作:
  1. 組裝剛體桿 + 開啟 App + 開啟 360 鏡頭
  2. App 自動同步時間戳 (sync_offset)
  3. 按下「開始掃描」
  4. 以 0.5-1.0 m/s 步行速度走 S 行走法
     - iPhone 持續 SLAM (ARKit 60fps 位姿追蹤)
     - 360 鏡頭持續錄影 (30fps 8K → SD卡)
     - LiDAR 持續掃描近距離深度 (每幀取中心點)
     - IMU 持續紀錄加速度+角速度 (100Hz)
  5. 回到起點 → App 提示「閉環完成」
  6. 按下「結束」
  7. 整段時間無需按快門，全自動連續採集

數據產出:
  iPhone: sensor_log.json (~50MB/10min)
  SD卡:   video_360.insv   (~20GB/10min at 8K)
```

---

## 十、關鍵風險與對策

| 風險 | 影響 | 對策 |
|------|------|------|
| iPhone 13 Pro Lightning 頻寬不足以串流 8K | 預覽畫面卡頓 | 360 鏡頭獨立錄製到 SD，iPhone 只接收 1080p 預覽 |
| 森林 GPS 精度差 (>10m) | 單木座標飄移 | 以 ARKit Visual Odometry 為主座標，GPS 只做粗定位 |
| iPhone 在森林過熱降頻 | 錄製中斷 | 不在手機端跑重度 AI，只做輕量標記 |
| 360 鏡頭 SDK 不支援 iOS 17 UVC | 無法即時預覽 | fallback: 360 獨立錄影，回家再合併 (仍可行) |
| Schumacher 模型參數與實測偏差大 | 蓄積量計算不準 | 用地面 DBH 校正 gee_volume.py 的 SPECIES_MODELS |
| DBH 初期精度不足 (±5cm) | 標案驗收不過 | 設計「巡山員捲尺回饋」迴路，每次掃描抽驗 3-5 棵，持續迭代 |
| 密林地面偵測失敗 | 1.3m 胸高算錯 | iPhone LiDAR 近距掃地面 + ARKit 平面偵測雙保險 |
| 剛體桿鬆動 | 360↔iPhone 偏移量漂移 | 使用螺絲固定夾具 (非彈簧夾)，掃描前後各拍校正板驗證 |
| auth-service 尚未完成 | App 無法安全上傳 | Phase 4 前先用 API key header 驗證，後補 JWT |
