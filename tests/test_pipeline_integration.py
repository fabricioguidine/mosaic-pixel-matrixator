"""Integration tests for the mosaic pipeline using fixture PNGs.

Covers:
- Tile count correctness on known-size images.
- Color quantization with a known 4-color palette.
- Edge cases: 1x1 image, all-white image, all-black image.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest
from PIL import Image

from src.generation.matrix_generator import MatrixGenerator
from src.processing.image_processor import ImageProcessor
from src.quantization.color_quantizer import ColorQuantizer

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def quadrants_image() -> Image.Image:
    return Image.open(FIXTURES / "sample_quadrants.png").convert("RGB")


@pytest.fixture
def one_by_one_image() -> Image.Image:
    return Image.open(FIXTURES / "sample_1x1.png").convert("RGB")


@pytest.fixture
def white_image() -> Image.Image:
    return Image.open(FIXTURES / "sample_white.png").convert("RGB")


@pytest.fixture
def black_image() -> Image.Image:
    return Image.open(FIXTURES / "sample_black.png").convert("RGB")


@pytest.fixture
def gradient_image() -> Image.Image:
    return Image.open(FIXTURES / "sample_gradient.png").convert("RGB")


class TestTileCount:
    """Validate tile-count summaries from the matrix generator."""

    def test_matrix_dimensions_match_expected_tile_count(self, gradient_image: Image.Image) -> None:
        # With tile_size_cm=2.0 and output 20x20 cm we expect 10x10 tiles = 100.
        gen = MatrixGenerator(tile_size_cm=2.0)
        matrix, (rows, cols), _, _ = gen.generate_matrix(
            gradient_image, output_width_cm=20.0, output_height_cm=20.0,
            preserve_aspect_ratio=False, quantize_colors=False,
        )
        assert rows == 10
        assert cols == 10
        info = gen.get_matrix_info(matrix)
        assert info["total_tiles"] == 100
        assert matrix.shape == (10, 10, 3)

    def test_tile_count_rectangle(self, gradient_image: Image.Image) -> None:
        gen = MatrixGenerator(tile_size_cm=2.0)
        _, (rows, cols), _, _ = gen.generate_matrix(
            gradient_image, output_width_cm=30.0, output_height_cm=10.0,
            preserve_aspect_ratio=False, quantize_colors=False,
        )
        assert (rows, cols) == (5, 15)
        assert rows * cols == 75

    def test_calculate_matrix_dimensions_floor(self) -> None:
        gen = MatrixGenerator(tile_size_cm=2.2)
        # 4.5 / 2.2 = 2.04 -> floor 2
        rows, cols = gen.calculate_matrix_dimensions(4.5, 4.5)
        assert rows == 2
        assert cols == 2


class TestColorQuantizationKnownPalette:
    """Quantize a 4-color image and assert the palette captures those colors."""

    def test_known_palette_recovered(self, quadrants_image: Image.Image) -> None:
        arr = np.array(quadrants_image)
        quantizer = ColorQuantizer(num_colors=4)
        quantized = quantizer.quantize_matrix(arr)

        assert quantized.shape == arr.shape
        assert quantized.dtype == np.uint8

        palette = quantizer.get_palette()
        assert palette.shape == (4, 3)

        # Each of the four canonical colors must have a near-match in the palette.
        targets = np.array(
            [[255, 0, 0], [0, 255, 0], [0, 0, 255], [255, 255, 255]], dtype=np.int32
        )
        palette_int = palette.astype(np.int32)
        for target in targets:
            distances = np.linalg.norm(palette_int - target, axis=1)
            assert distances.min() < 30, f"palette missing color near {target.tolist()}"

    def test_quantized_pixels_belong_to_palette(self, quadrants_image: Image.Image) -> None:
        arr = np.array(quadrants_image)
        quantizer = ColorQuantizer(num_colors=4)
        quantized = quantizer.quantize_matrix(arr)
        palette = {tuple(c) for c in quantizer.get_palette().tolist()}
        unique = {tuple(c) for c in quantized.reshape(-1, 3).tolist()}
        assert unique.issubset(palette)


class TestEdgeCases:
    """Edge cases: 1x1, all-white, all-black inputs."""

    def test_one_by_one_image_pipeline(self, one_by_one_image: Image.Image) -> None:
        gen = MatrixGenerator(tile_size_cm=2.0)
        matrix, (rows, cols), _, _ = gen.generate_matrix(
            one_by_one_image, output_width_cm=4.0, output_height_cm=4.0,
            preserve_aspect_ratio=False, quantize_colors=False,
        )
        assert (rows, cols) == (2, 2)
        # Source pixel is (255,0,0); resized constant.
        assert np.array_equal(matrix[0, 0], np.array([255, 0, 0], dtype=np.uint8))

    def test_all_white_image_quantizes_to_white(self, white_image: Image.Image) -> None:
        arr = np.array(white_image)
        quantizer = ColorQuantizer(num_colors=4)
        out = quantizer.quantize_matrix(arr)
        # Every output pixel should equal (255,255,255) or be padded black.
        # Active palette entry must include white.
        palette = quantizer.get_palette()
        assert any(tuple(c) == (255, 255, 255) for c in palette.tolist())
        whites = (out == np.array([255, 255, 255], dtype=np.uint8)).all(axis=-1)
        assert whites.all(), "all-white image should remain white after quantization"

    def test_all_black_image_quantizes_to_black(self, black_image: Image.Image) -> None:
        arr = np.array(black_image)
        quantizer = ColorQuantizer(num_colors=4)
        out = quantizer.quantize_matrix(arr)
        blacks = (out == np.array([0, 0, 0], dtype=np.uint8)).all(axis=-1)
        assert blacks.all(), "all-black image should remain black after quantization"

    def test_image_processor_rgb_conversion_idempotent(self) -> None:
        proc = ImageProcessor()
        rgb = Image.new("RGB", (5, 5), color=(10, 20, 30))
        assert proc.convert_to_rgb(rgb) is rgb

    def test_image_processor_converts_non_rgb(self) -> None:
        proc = ImageProcessor()
        gray = Image.new("L", (4, 4), color=128)
        converted = proc.convert_to_rgb(gray)
        assert converted.mode == "RGB"

    def test_image_to_array_shape(self, gradient_image: Image.Image) -> None:
        proc = ImageProcessor()
        arr = proc.image_to_array(gradient_image, rows=6, cols=8)
        assert arr.shape == (6, 8, 3)
        assert arr.dtype == np.uint8


class TestAspectRatioPreservation:
    """Pipeline level checks for aspect-ratio behavior."""

    def test_aspect_ratio_preserved_choice(self, gradient_image: Image.Image) -> None:
        gen = MatrixGenerator(tile_size_cm=2.0)
        _, _, (w, h), (wdiff, hdiff) = gen.generate_matrix(
            gradient_image, output_width_cm=20.0, output_height_cm=30.0,
            preserve_aspect_ratio=True, quantize_colors=False,
        )
        # Source is square -> chosen output should keep aspect 1:1.
        assert w == pytest.approx(h, rel=1e-6)
        # Difference must be non-negative.
        assert wdiff >= 0
        assert hdiff >= 0
