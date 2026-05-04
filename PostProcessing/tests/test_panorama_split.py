"""Tests for panorama_split module."""

import numpy as np
import pytest

from pipeline.panorama_split import (
    AZIMUTHS,
    FOV_DEG,
    split_equirect_to_perspectives,
    process_single_image,
)
from pathlib import Path


class TestSplitEquirectToPerspectives:
    """Test the core splitting function."""

    def _make_equirect(self, h: int = 512, w: int = 1024) -> np.ndarray:
        """Create a synthetic equirectangular image (2:1 aspect ratio)."""
        return np.random.randint(0, 255, (h, w, 3), dtype=np.uint8)

    def test_returns_6_views(self) -> None:
        equirect = self._make_equirect()
        result = split_equirect_to_perspectives(equirect)
        assert len(result) == 6

    def test_output_shape(self) -> None:
        equirect = self._make_equirect()
        result = split_equirect_to_perspectives(equirect, out_hw=(320, 320))
        for view in result:
            assert view.shape == (320, 320, 3)

    def test_custom_fov(self) -> None:
        equirect = self._make_equirect()
        result = split_equirect_to_perspectives(equirect, fov_deg=90.0)
        assert len(result) == 6

    def test_custom_azimuths(self) -> None:
        equirect = self._make_equirect()
        azimuths = [0.0, 90.0, 180.0, 270.0]
        result = split_equirect_to_perspectives(equirect, azimuths=azimuths)
        assert len(result) == 4

    def test_views_are_different(self) -> None:
        """Different azimuths should produce different views."""
        equirect = self._make_equirect(h=1024, w=2048)
        result = split_equirect_to_perspectives(equirect)
        # At least some views should differ
        diffs = [
            np.mean(np.abs(result[i].astype(float) - result[j].astype(float)))
            for i in range(len(result))
            for j in range(i + 1, len(result))
        ]
        assert any(d > 1.0 for d in diffs), "All views are identical"

    def test_default_azimuths_cover_360(self) -> None:
        """6 views × 60° spacing = 360° coverage."""
        assert len(AZIMUTHS) == 6
        assert AZIMUTHS[-1] + 60.0 == 360.0

    def test_fov_overlap(self) -> None:
        """72° FOV with 60° spacing → 12° overlap."""
        overlap = FOV_DEG - 60.0
        assert overlap == 12.0


class TestProcessSingleImage:
    """Test file-based processing."""

    def test_output_files_created(self, tmp_path: Path) -> None:
        """Should create 6 JPG files."""
        # Create a fake equirectangular image
        import cv2
        fake_img = np.random.randint(0, 255, (512, 1024, 3), dtype=np.uint8)
        input_path = tmp_path / "test_equirect.jpg"
        cv2.imwrite(str(input_path), fake_img)

        output_dir = tmp_path / "output"
        paths = process_single_image(input_path, output_dir)

        assert len(paths) == 6
        for p in paths:
            assert p.exists()
            assert p.suffix == ".jpg"

    def test_file_not_found(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError):
            process_single_image(tmp_path / "nonexistent.jpg", tmp_path / "out")
