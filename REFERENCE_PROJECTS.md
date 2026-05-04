# 參考專案與學習資源指南

按照你的開發管線，每個階段需要學什麼、用什麼、從哪裡開始。

---

## 階段 A — iPhone 數據採集 (Swift / ARKit)

### A1. ARKit + LiDAR 數據紀錄

| 專案 | 語言 | 說明 | 你要學的 |
|------|------|------|---------|
| **[StrayScanner](https://github.com/strayrobots/scanner)** | Swift | ✅ 你已下載。紀錄 RGB + Depth + IMU + Odometry | `DatasetEncoder.swift` 的同步寫入邏輯、`OdometryEncoder` 的 4x4 矩陣轉 quaternion |
| **[ARKit-Scanner](https://github.com/xiongyiheng/ARKit-Scanner)** | Swift | RGB-D 掃描，存 color + depth + IMU 到本地，上傳 PC 處理 | ARFrame 的 sceneDepth 取用方式、資料上傳流程 |
| **[SwiftUI-LiDAR](https://github.com/cedanmisquith/SwiftUI-LiDAR)** | SwiftUI | LiDAR 掃描 → 3D Mesh → 匯出 .OBJ | SwiftUI 整合 ARKit 的 UI 架構、Mesh 匯出 |
| **[ExampleOfiOSLiDAR](https://github.com/TokyoYoshida/ExampleOfiOSLiDAR)** | Swift | 日本開發者做的 LiDAR 範例集 (深度圖、碰撞偵測、物件匯出) | Depth Map 的讀取與視覺化、Raycast 測距 |

**建議起點**: 你已有 StrayScanner，先讀懂它的 `DatasetEncoder.swift`，然後精簡成只存 sensor_log.json。

### A2. CoreML + YOLO 物件偵測

| 專案 | 語言 | 說明 | 你要學的 |
|------|------|------|---------|
| **[ultralytics/yolo-ios-app](https://github.com/ultralytics/yolo-ios-app)** | Swift | Ultralytics 官方 iOS App，支援 YOLOv8/v10/v11 | ⭐ 最重要：CoreML 模型載入、Vision framework 推理、即時 bounding box 繪製 |
| **[ObjectDetection-CoreML](https://github.com/tucan9389/ObjectDetection-CoreML)** | Swift | 支援多種 YOLO 模型，結構清晰 | CoreML 模型切換機制、效能優化 |
| **[CoreML-Models](https://github.com/john-rocky/CoreML-Models)** | - | 已轉換好的 CoreML 模型庫 (含 YOLOv10, v11) | 直接下載 .mlpackage 測試，不用自己轉換 |

**建議起點**: 下載 `ultralytics/yolo-ios-app`，直接在 iPhone 上跑看看通用物件辨識的效果。

### A3. iOS 外接相機 (UVC / 360)

| 專案/資源 | 說明 | 你要學的 |
|-----------|------|---------|
| **[Apple AVCaptureDevice docs](https://developer.apple.com/documentation/avfoundation/avcapturedevice)** | iOS 17+ 支援 UVC 外接相機 | `AVCaptureDevice.DiscoverySession` 搜尋外接設備 |
| **[Insta360 SDK for iOS](https://github.com/Insta360Develop/CameraSDK-iOS)** | Insta360 官方 SDK | 如果用 Insta360：控制錄影、預覽流、同步時間 |
| **[Ricoh Theta SDK](https://github.com/ricohapi/theta-client)** | Ricoh Theta 多平台 SDK | 如果用 Ricoh：OSC 協議、Wi-Fi 控制 |

**建議**: 先確定你要用哪一台 360 鏡頭，再決定 SDK。如果暫時沒有，Phase 1-2 可以先用 iPhone 自身相機開發。

---

## 階段 B — 後處理管線 (Python / Mac Pro)

### B1. 360 影像處理 (全景 → 分鏡)

| 專案 | 語言 | 說明 | 你要學的 |
|------|------|------|---------|
| **[py360convert](https://github.com/sunset1995/py360convert)** | Python | ⭐ 全景轉換聖經。Equirectangular ↔ CubeMap ↔ Perspective | `e2p()` 函數：equirect → perspective 投影的數學原理 |
| **[equilib](https://github.com/haruishi43/equilib)** | Python/PyTorch | GPU 加速版全景轉換，支援 batch 處理 | 如果需要高速處理大量影格 |

**學習重點**: `py360convert` 的 `e2p(equirect_img, fov_deg, u_deg, v_deg, out_hw)` 就是你的六角分鏡核心。

```python
# 最小範例：從全景圖切出 72° 視角的透視圖
import py360convert
import cv2

equirect = cv2.imread("360_frame.jpg")
# 切出朝向 60° 方向、72° FOV 的透視圖
perspective = py360convert.e2p(equirect, fov_deg=72, u_deg=60, v_deg=0, out_hw=(640, 640))
```

### B2. SfM / 3D 重建

| 專案 | 語言 | 說明 | 你要學的 |
|------|------|------|---------|
| **[COLMAP](https://github.com/colmap/colmap)** | C++ | ⭐ 學術界標準 SfM/MVS 引擎 | 影像對齊 → 稀疏點雲 → 稠密重建 的完整流程 |
| **[OpenDroneMap (ODM)](https://github.com/OpenDroneMap/ODM)** | Python | ⭐ 你已經用在空拍機數據上。可用於地面影像 | `--camera-lens spherical` 參數處理全景輸入 |
| **[hloc](https://github.com/cvg/Hierarchical-Localization)** | Python | 超強特徵匹配 (SuperPoint + SuperGlue) | 森林這種重複紋理場景的特徵匹配優化 |
| **[GLOMAP](https://github.com/colmap/glomap)** | C++ | COLMAP 團隊的新全局 SfM，速度更快 | 大量影格的快速處理 |

**你已經有 ODM 經驗**，地面影像也可以用 ODM 跑。COLMAP 的優勢是可以匯入 iPhone IMU 位姿作為初始值，加速收斂。

### COLMAP 匯入 iPhone 位姿的格式

```
# images.txt 格式 (COLMAP)
# IMAGE_ID, QW, QX, QY, QZ, TX, TY, TZ, CAMERA_ID, NAME
1 0.95 0.02 0.31 0.01 1.20 0.50 -3.40 1 frame_000001.jpg
2 0.94 0.03 0.32 0.01 1.25 0.52 -3.35 1 frame_000002.jpg

# cameras.txt 格式
# CAMERA_ID, MODEL, WIDTH, HEIGHT, PARAMS[]
1 PINHOLE 1920 1440 fx fy cx cy
```

你的 `sensor_log.json` 中的 quaternion + position 可以直接轉成這個格式。

### B3. 點雲處理 & DBH 萃取

| 專案 | 語言 | 說明 | 你要學的 |
|------|------|------|---------|
| **[Open3D](https://github.com/isl-org/Open3D)** | Python/C++ | ⭐ 點雲處理必備庫 | DBSCAN 聚類、圓柱擬合、法線估算 |
| **[TreeTool](https://github.com/ElsevierSoftwareX/SOFTX-D-21-00028)** | Python | ⭐ 學術論文配套：從點雲偵測樹木 + 萃取 DBH | 完整的 tree detection → DBH pipeline |
| **[forest_3d_app](https://github.com/lloydwindrim/forest_3d_app)** | Python | 森林點雲 → 樹木偵測 → DBH | 地面移除 + 樹幹分割 + DBH 計算 |
| **[cloud2trees](https://github.com/georgewoolsey/cloud2trees)** | R/Python | 從點雲萃取 tree list, CHM, DTM, DBH | 完整的 forest inventory 輸出 |
| **[FSCT](https://github.com/Sean-Regan/FSCT)** | Python | Forest Structural Complexity Tool，全自動 | 自動偵測樹幹 + DBH + 位置 |

**建議起點**: 先裝 Open3D，用你既有的空拍點雲練手。然後下載 TreeTool 跑它的範例數據。

```python
# Open3D 最小範例：載入點雲 → DBSCAN 聚類
import open3d as o3d
import numpy as np

pcd = o3d.io.read_point_cloud("forest_scan.ply")
# 移除地面 (RANSAC 平面擬合)
plane_model, inliers = pcd.segment_plane(distance_threshold=0.1, ransac_n=3, num_iterations=1000)
trees_pcd = pcd.select_by_index(inliers, invert=True)
# DBSCAN 聚類 → 每棵樹一個 cluster
labels = np.array(trees_pcd.cluster_dbscan(eps=0.3, min_points=50))
```

### B4. YOLO 訓練 & 樹木辨識

| 專案 | 語言 | 說明 | 你要學的 |
|------|------|------|---------|
| **[ultralytics](https://github.com/ultralytics/ultralytics)** | Python | ⭐ YOLOv8/v10/v11 訓練框架 | `model.train(device='mps')` 用 M1 Pro 訓練 |
| **[DeepForest](https://github.com/weecology/deepforest)** | Python | 森林特化的樹冠偵測模型 (預訓練好的) | 直接 `model.predict_image()` 看效果 |
| **[Roboflow Universe](https://universe.roboflow.com/)** | 線上 | 搜尋 "tree trunk", "tree bark" 資料集 | 下載標註好的訓練資料 |

```python
# 最小範例：用 M1 Pro 訓練 YOLO
from ultralytics import YOLO
model = YOLO('yolov10n.pt')
model.train(data='forest.yaml', epochs=100, imgsz=640, device='mps')
model.export(format='coreml', nms=True)  # → .mlpackage 丟進 Xcode
```

---

## 階段 C — SaaS 整合 (Python / FastAPI)

你的 SaaS 已有完整架構，新增的 API 可以直接參考現有的 `gee_volume.py`。

| 現有資產 | 路徑 | 可複用的 |
|---------|------|---------|
| `gee_volume.py` | `services/gis-service/app/api/endpoints/` | Schumacher 模型、species 匹配、GeoDataFrame 處理 |
| `gis.py` / `gis_new.py` | 同上 | GeoJSON endpoint 的標準格式、project config 讀取 |
| `pointcloud_pipeline.py` | `services/gis-service/app/services/` | 點雲處理的既有框架 |
| `lidar_processor.py` | 同上 | LiDAR 數據入庫邏輯 |

---

## 建議學習順序 (最小可行路徑)

```
Week 1: 讀 StrayScanner 原始碼
        ├── 理解 ARKit session + depth + IMU 的資料流
        └── 在 iPhone 上跑一次，看產出的 CSV/PNG 長什麼樣

Week 2: 下載 ultralytics/yolo-ios-app
        ├── 在 iPhone 上跑通用 YOLO，對著樹拍看看辨識什麼
        └── 理解 CoreML + Vision framework 的推理流程

Week 3: 安裝 py360convert + Open3D
        ├── 用一張 360 全景圖測試 e2p() 切分鏡
        └── 用你既有的空拍點雲跑 Open3D DBSCAN

Week 4: 下載 TreeTool
        ├── 跑它的範例數據，理解 tree detection → DBH 的流程
        └── 嘗試用你自己的空拍點雲跑看看

Week 5: 安裝 COLMAP
        ├── 用手機拍一組照片 (不用 360)，跑一次 SfM
        └── 理解 images.txt / cameras.txt 格式
        └── 嘗試匯入 StrayScanner 的 odometry.csv 作為初始位姿

(此時你已經理解每個環節怎麼運作，可以開始整合)
```

---

## 關鍵演算法速查

| 演算法 | 用在哪裡 | 庫 | 一句話解釋 |
|--------|---------|-----|---------|
| **DBSCAN** | 點雲中分割每棵樹 | Open3D / sklearn | 密度聚類：靠近的點歸同一群 |
| **RANSAC** | 從點雲找地面平面 | Open3D | 隨機取樣擬合：找到最多點符合的平面 |
| **圓柱擬合** | 從樹幹切面計算 DBH | Open3D / scipy | 在 1.3m 高度切一圈點，擬合最佳圓 |
| **Quaternion** | IMU 姿態表示 | simd (Swift) / scipy | 四元數：避免萬向鎖的旋轉表示法 |
| **Gnomonic 投影** | 全景 → 透視 | py360convert | 球面 → 平面的數學映射 |
| **Bundle Adjustment** | SfM 全局優化 | COLMAP | 同時優化所有相機位姿和 3D 點 |
| **NMS** | YOLO 去重複框 | ultralytics | 非極大值抑制：重疊的框只留最好的 |
| **Schumacher** | H→DBH→Volume | 你的 gee_volume.py | 森林學經驗公式：樹高推胸徑推材積 |

---

## 你目前已有但還沒連起來的資產

| 資產 | 位置 | 狀態 |
|------|------|------|
| StrayScanner 原始碼 | `/Users/fuiko/Documents/scanner/` | ✅ 已下載 |
| SylvaNexus SaaS 平台 | `SaaSDocker/` | ✅ Docker 運行中 |
| 空拍機 300+ 公頃正射影像 / DSM | 你的專案資料 | ✅ 已有 |
| GEE 蓄積量管線 | `gee_volume.py` | ✅ 已完成 |
| Schumacher SPECIES_MODELS | `gee_volume.py` 內 | ✅ 6 樹種參數 |
| M1 Pro GPU | Mac Pro | ✅ 可用 `device='mps'` 訓練 |
| Windsurf + Opus | 開發工具 | ✅ $200/mo |

**缺的只是把這些串起來的「膠水代碼」**— 而這正是 Windsurf 最擅長的。
