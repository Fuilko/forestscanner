---
description: How to run the PostProcessing pipeline on scan data
---

# Run Post-Processing Pipeline

## Prerequisites
- Python 3.11+ with venv activated
- PostProcessing/requirements.txt installed

## Steps

1. Activate the virtual environment
// turbo
```bash
source PostProcessing/.venv/bin/activate
```

2. Run the full pipeline on a scan folder
```bash
python -m pipeline.panorama_split --input ScanData/<scan_id>/video_360.insv --output ScanData/<scan_id>/frames/
python -m pipeline.tree_detect --input ScanData/<scan_id>/frames/ --output ScanData/<scan_id>/detections/
python -m pipeline.sfm_reconstruct --input ScanData/<scan_id>/ --output ScanData/<scan_id>/pointcloud/
python -m pipeline.pointcloud_dbh --input ScanData/<scan_id>/pointcloud/ --output ScanData/<scan_id>/dbh.csv
python -m pipeline.export_geojson --input ScanData/<scan_id>/ --output ScanData/<scan_id>/trees.geojson
```

3. Run tests
// turbo
```bash
cd PostProcessing && pytest tests/ -v
```
