"""End-to-end tests that drive the real CLI (main.py) as a subprocess.

These are hermetic and OS-agnostic:
- A tiny input image is created with Pillow inside ``tmp_path``.
- ``main.py`` is invoked with ``sys.executable`` so the active interpreter and
  venv are used on every platform.
- The CLI is run with ``cwd=tmp_path`` because it reads from ``input/`` and
  writes to ``output/`` relative to the working directory; no global state or
  hardcoded paths are touched.
- Outputs are asserted to exist with the expected image/JSON properties.

A square input image is used so aspect-ratio preservation resolves to clean,
predictable tile dimensions on every platform.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from PIL import Image

REPO_ROOT = Path(__file__).resolve().parent.parent
MAIN = REPO_ROOT / "main.py"
SIZE = 8  # square -> aspect ratio 1:1


def _make_input_image(input_dir: Path, name: str = "tiny.png") -> Path:
    """Create a small square multi-color PNG so quantization has real work."""
    input_dir.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", (SIZE, SIZE))
    px = img.load()
    for x in range(SIZE):
        for y in range(SIZE):
            px[x, y] = ((x * 32) % 256, (y * 40) % 256, ((x + y) * 16) % 256)
    path = input_dir / name
    img.save(path)
    return path


def _run_cli(cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
    """Run the CLI with the active interpreter, capturing decoded text output."""
    return subprocess.run(
        [sys.executable, str(MAIN), *args],
        cwd=str(cwd),
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=120,
        check=False,
    )


def test_cli_end_to_end_produces_all_outputs(tmp_path: Path) -> None:
    _make_input_image(tmp_path / "input")

    # Square input + tile-size 2.0: width 20cm -> 10 cols, height 16cm -> 8 rows.
    result = _run_cli(tmp_path, "--width", "20", "--height", "16", "--tile-size", "2.0")

    assert result.returncode == 0, f"stderr:\n{result.stderr}\nstdout:\n{result.stdout}"
    assert "Processing completed successfully!" in result.stdout

    output_dir = tmp_path / "output"
    assert output_dir.is_dir()

    pngs = list(output_dir.glob("*.png"))
    matrix_txts = list(output_dir.glob("*_matrix.txt"))
    matrix_jsons = list(output_dir.glob("*_matrix.json"))
    paints_jsons = list(output_dir.glob("*_paints.json"))

    assert len(pngs) == 1, f"expected one preview png, got {pngs}"
    assert len(matrix_txts) == 1
    assert len(matrix_jsons) == 1
    assert len(paints_jsons) == 1

    # Preview is a valid RGB PNG upscaled by the default scale factor (10).
    # Matrix is (rows=8, cols=10); PIL size is (width=cols*10, height=rows*10).
    with Image.open(pngs[0]) as preview:
        assert preview.mode == "RGB"
        assert preview.size == (10 * 10, 8 * 10)

    data = json.loads(matrix_jsons[0].read_text(encoding="utf-8"))
    assert data["dimensions"] == {"rows": 8, "columns": 10}
    assert data["total_tiles"] == 80
    assert len(data["matrix"]) == 8
    assert len(data["matrix"][0]) == 10
    assert {"rgb", "hex", "cmyk", "hsl"} <= set(data["matrix"][0][0])


def test_cli_no_quantize_option(tmp_path: Path) -> None:
    _make_input_image(tmp_path / "input")

    # Square input, 12x12cm at tile-size 2.0 -> 6x6 = 36 tiles.
    result = _run_cli(
        tmp_path, "--width", "12", "--height", "12", "--tile-size", "2.0", "--no-quantize"
    )

    assert result.returncode == 0, result.stderr
    paints = list((tmp_path / "output").glob("*_paints.json"))
    assert len(paints) == 1
    payload = json.loads(paints[0].read_text(encoding="utf-8"))
    assert payload["total_tiles"] == 36
    assert payload["total_unique_colors"] >= 1


def test_cli_output_files_are_utf8(tmp_path: Path) -> None:
    """Generated text artifacts must be valid UTF-8 on every platform."""
    _make_input_image(tmp_path / "input")

    result = _run_cli(tmp_path, "--width", "10", "--height", "10", "--tile-size", "2.0")
    assert result.returncode == 0, result.stderr

    text_files = list((tmp_path / "output").glob("*_matrix.txt"))
    assert text_files
    for text_file in text_files:
        # Raises UnicodeDecodeError if a non-UTF-8 codec was used to write.
        content = text_file.read_text(encoding="utf-8")
        assert "RGB Color Matrix" in content


def test_cli_empty_input_dir_reports_no_images(tmp_path: Path) -> None:
    (tmp_path / "input").mkdir()
    result = _run_cli(tmp_path, "--width", "10", "--height", "10")
    assert result.returncode == 0
    assert "No image files found" in result.stdout


def test_cli_rejects_nonpositive_tile_size(tmp_path: Path) -> None:
    _make_input_image(tmp_path / "input")
    result = _run_cli(tmp_path, "--width", "10", "--height", "10", "--tile-size", "0")
    assert result.returncode == 1
    assert "Tile size must be a positive number" in result.stdout
