"""
panorama_split.py — 360 全景圖 → 6 張透視圖 (hexagonal split)

將 equirectangular 全景圖切成 6 張 72° FOV 的透視圖，
每張有 12° 重疊區域，覆蓋完整 360°。

方位角分配:
  View 0: 0°   (正前方)
  View 1: 60°  (右前方)
  View 2: 120° (右後方)
  View 3: 180° (正後方)
  View 4: 240° (左後方)
  View 5: 300° (左前方)

Usage:
  python -m pipeline.panorama_split --input <equirect.jpg> --output <output_dir>
  python -m pipeline.panorama_split --input <folder_of_frames> --output <output_dir>
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

import click
import cv2
import numpy as np
import py360convert

logger = logging.getLogger(__name__)

# 6 方位角 (度), 每隔 60°, FOV 72° → 12° 重疊
AZIMUTHS: list[float] = [0.0, 60.0, 120.0, 180.0, 240.0, 300.0]
FOV_DEG: float = 72.0
OUTPUT_SIZE: tuple[int, int] = (640, 640)  # (H, W)


def split_equirect_to_perspectives(
    equirect: np.ndarray,
    fov_deg: float = FOV_DEG,
    azimuths: list[float] = AZIMUTHS,
    out_hw: tuple[int, int] = OUTPUT_SIZE,
    v_deg: float = 0.0,
) -> list[np.ndarray]:
    """將一張 equirectangular 全景圖切成多張透視圖。

    Args:
        equirect: 全景圖 (H, W, 3), equirectangular 投影
        fov_deg: 每張透視圖的水平 FOV (度)
        azimuths: 各方位角 (度)
        out_hw: 輸出尺寸 (height, width)
        v_deg: 垂直角度 (度), 0 = 水平, 正值向上

    Returns:
        list of perspective images
    """
    perspectives: list[np.ndarray] = []
    for u_deg in azimuths:
        persp = py360convert.e2p(
            equirect,
            fov_deg=(fov_deg, fov_deg),
            u_deg=u_deg,
            v_deg=v_deg,
            out_hw=out_hw,
            mode="bilinear",
        )
        perspectives.append(persp)
    return perspectives


def process_single_image(
    input_path: Path,
    output_dir: Path,
    fov_deg: float = FOV_DEG,
    out_hw: tuple[int, int] = OUTPUT_SIZE,
) -> list[Path]:
    """處理單張全景圖，輸出 6 張透視圖。

    Args:
        input_path: 輸入的 equirectangular 圖片路徑
        output_dir: 輸出目錄
        fov_deg: FOV (度)
        out_hw: 輸出尺寸

    Returns:
        輸出檔案路徑列表
    """
    logger.info("Processing: %s", input_path.name)

    equirect = cv2.imread(str(input_path))
    if equirect is None:
        raise FileNotFoundError(f"Cannot read image: {input_path}")

    perspectives = split_equirect_to_perspectives(
        equirect, fov_deg=fov_deg, out_hw=out_hw
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    stem = input_path.stem
    output_paths: list[Path] = []

    for i, (persp, azimuth) in enumerate(zip(perspectives, AZIMUTHS)):
        filename = f"{stem}_view{i}_{int(azimuth)}deg.jpg"
        out_path = output_dir / filename
        cv2.imwrite(str(out_path), persp, [cv2.IMWRITE_JPEG_QUALITY, 95])
        output_paths.append(out_path)
        logger.info("  Saved: %s (azimuth=%d°)", filename, int(azimuth))

    return output_paths


def process_batch(
    input_dir: Path,
    output_dir: Path,
    fov_deg: float = FOV_DEG,
    out_hw: tuple[int, int] = OUTPUT_SIZE,
    extensions: Optional[set[str]] = None,
) -> dict[str, list[Path]]:
    """批次處理整個資料夾的全景圖。

    Args:
        input_dir: 包含 equirectangular 圖片的資料夾
        output_dir: 輸出目錄
        fov_deg: FOV (度)
        out_hw: 輸出尺寸
        extensions: 要處理的副檔名集合

    Returns:
        {原始檔名: [輸出路徑列表]}
    """
    if extensions is None:
        extensions = {".jpg", ".jpeg", ".png", ".bmp"}

    image_files = sorted(
        p for p in input_dir.iterdir()
        if p.suffix.lower() in extensions
    )

    if not image_files:
        logger.warning("No images found in %s", input_dir)
        return {}

    logger.info("Found %d images to process", len(image_files))
    results: dict[str, list[Path]] = {}

    for img_path in image_files:
        output_paths = process_single_image(
            img_path, output_dir, fov_deg=fov_deg, out_hw=out_hw
        )
        results[img_path.name] = output_paths

    logger.info("Done! Processed %d images → %d perspectives",
                len(results), len(results) * len(AZIMUTHS))
    return results


@click.command()
@click.option("--input", "input_path", required=True, type=click.Path(exists=True),
              help="輸入: 單張全景圖 或 包含全景圖的資料夾")
@click.option("--output", "output_dir", required=True, type=click.Path(),
              help="輸出目錄")
@click.option("--fov", default=FOV_DEG, type=float,
              help=f"FOV 角度 (預設: {FOV_DEG}°)")
@click.option("--size", default=640, type=int,
              help="輸出尺寸 (預設: 640x640)")
@click.option("--verbose", "-v", is_flag=True, help="顯示詳細日誌")
def main(
    input_path: str,
    output_dir: str,
    fov: float,
    size: int,
    verbose: bool,
) -> None:
    """360 全景圖 → 6 張透視圖 (hexagonal split)"""
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(levelname)s | %(message)s",
    )

    inp = Path(input_path)
    out = Path(output_dir)
    hw = (size, size)

    if inp.is_file():
        paths = process_single_image(inp, out, fov_deg=fov, out_hw=hw)
        click.echo(f"✓ Generated {len(paths)} perspective views → {out}")
    elif inp.is_dir():
        results = process_batch(inp, out, fov_deg=fov, out_hw=hw)
        total = sum(len(v) for v in results.values())
        click.echo(f"✓ Processed {len(results)} images → {total} views → {out}")
    else:
        click.echo(f"✗ Input not found: {inp}", err=True)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
