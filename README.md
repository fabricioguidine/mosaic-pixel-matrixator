<div align="center">

<img src=".github/assets/banner.svg" alt="mosaic-pixel-matrixator" width="100%" />

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE) [![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/) [![CI](https://github.com/fabricioguidine/mosaic-pixel-matrixator/actions/workflows/ci.yml/badge.svg)](https://github.com/fabricioguidine/mosaic-pixel-matrixator/actions/workflows/ci.yml) [![codecov](https://codecov.io/gh/fabricioguidine/mosaic-pixel-matrixator/branch/main/graph/badge.svg)](https://codecov.io/gh/fabricioguidine/mosaic-pixel-matrixator) [![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

</div>

> Transforms images into ceramic tile mosaics using color quantization and CMYK paint mixing instructions.

A Python tool that converts a source image into a grid of ceramic tiles. It resizes the image to a tile matrix (while preserving aspect ratio), reduces the palette with a median cut quantizer, and emits both a visual preview and machine-readable matrices that tell you exactly which colors to paint each tile and how to mix them from the CMYK + white base set.

## Table of Contents

- [Features](#features)
- [How it works](#how-it-works)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Output](#output)
- [Examples](#examples)
- [Project structure](#project-structure)
- [Testing](#testing)
- [License](#license)

## Features

- Reads the first image found in `input/` (JPG, JPEG, PNG, BMP, GIF, TIFF, WEBP).
- Preserves aspect ratio by choosing the output dimensions closest to the requested width/height.
- Splits the canvas into a tile matrix based on a configurable tile size (default 2.2 cm).
- Reduces the palette with a median cut quantizer (default 32 colors), or keeps original colors with `--no-quantize`.
- Computes CMYK, Hex and HSL values for every color plus per-tile mixing instructions from the 5 base paints (Cyan, Magenta, Yellow, Black, White).
- Tracks a paint inventory: unique colors, per-color tile counts and percentages.
- Writes four outputs per run: a PNG preview, a human-readable TXT matrix, a JSON matrix, and a paint-inventory JSON.

## How it works

```mermaid
flowchart TD
    A[Image in input/] --> B[Load first image]
    B --> C[Preserve aspect ratio<br/>closest to requested W x H]
    C --> D[Compute matrix dims<br/>dimension / tile size]
    D --> E[Resize image to rows x cols]
    E --> F{Quantize colors?}
    F -- yes --> G[Median cut quantization<br/>num-colors palette]
    F -- no --> H[Keep original colors]
    G --> I[Color matrix RGB]
    H --> I
    I --> J[Per-tile CMYK mixing<br/>from C/M/Y/K + White base]
    J --> K[Paint inventory<br/>counts and percentages]
    K --> L[Outputs: PNG preview,<br/>TXT + JSON matrix, paints.json]
```

Pipeline detail:

1. Loads the first image found in the `input/` directory.
2. Calculates output dimensions that preserve the image's aspect ratio, picking the option closest to the requested width and height.
3. Derives the matrix size in tiles (`dimension / tile size`).
4. Resizes the image to that tile grid.
5. Quantizes the palette with median cut (unless `--no-quantize` is set).
6. Converts each tile color to CMYK and computes mixing percentages from the base paints (Cyan, Magenta, Yellow, Black, White).
7. Builds a paint inventory of unique colors with tile counts and percentages.
8. Writes the preview PNG and the TXT / JSON matrices plus the paints inventory to `output/`.

## Requirements

- Python 3.10 or higher
- Pillow >= 10.0.0
- NumPy >= 1.24.0

## Installation

```powershell
git clone https://github.com/fabricioguidine/mosaic-pixel-matrixator.git
cd mosaic-pixel-matrixator
pip install -r requirements.txt
```

For development (tests, linting, type-checking):

```powershell
pip install -e ".[dev]"
```

## Usage

Place an image in the `input/` folder, then run `main.py`. If `--width` and `--height` are omitted, the tool prompts for them interactively.

```powershell
# Interactive: prompts for width, height and tile size
python main.py

# Provide dimensions directly (centimeters)
python main.py --width 200 --height 150

# Custom tile size
python main.py --width 200 --height 150 --tile-size 2.5

# Larger palette
python main.py --width 200 --height 150 --num-colors 128

# Skip quantization (use original colors)
python main.py --width 200 --height 150 --no-quantize
```

| Option | Description | Default |
|--------|-------------|---------|
| `--width` | Output width in centimeters | Prompted |
| `--height` | Output height in centimeters | Prompted |
| `--tile-size` | Tile size in centimeters | `2.2` |
| `--num-colors` | Colors in the quantized palette | `32` |
| `--no-quantize` | Disable quantization, keep original colors | `False` |

Only the first image in `input/` is processed per run. Supported formats: JPG, JPEG, PNG, BMP, GIF, TIFF, WEBP.

## Output

Each run writes four files to `output/`, named `{image}-{timestamp}`:

- `{image}-{timestamp}.png` — visual preview of the mosaic (tiles scaled up 10x).
- `{image}-{timestamp}_matrix.txt` — human-readable matrix with base colors to purchase, a tiles-to-paint summary, and per-tile mixing instructions.
- `{image}-{timestamp}_matrix.json` — the same matrix as JSON, including `dimensions`, `total_tiles`, `total_unique_colors`, a `tiles_to_paint` summary, and the full `matrix` with RGB/Hex/CMYK/HSL per tile.
- `{image}-{timestamp}_paints.json` — paint inventory: unique color count, total tiles, and `required_paints` with RGB/Hex/CMYK/HSL and usage counts.

Every color carries four representations:

- **RGB** — digital values (0-255).
- **Hex** — universal color reference (e.g. `#FFFFFF`).
- **CMYK** — percentages used for paint mixing.
- **HSL** — hue/saturation/lightness for intuitive description.

The console also prints a per-color table (Hex, RGB, CMYK, tile count, percentage) and the set of base colors to purchase.

Sample TXT header:

```
# RGB Color Matrix with Paint Mixing Instructions
# Matrix dimensions: 68 rows x 43 columns
# Total tiles: 2924
# Format: R,G,B[CMYK] #HEX {mix_instruction}

# BASE COLORS TO PURCHASE:
# - CYAN: RGB[0, 255, 255] #00FFFF CMYK(100.0%,0.0%,0.0%,0.0%)
# - MAGENTA: RGB[255, 0, 255] #FF00FF CMYK(0.0%,100.0%,0.0%,0.0%)
# - YELLOW: RGB[255, 255, 0] #FFFF00 CMYK(0.0%,0.0%,100.0%,0.0%)
# - BLACK: RGB[0, 0, 0] #000000 CMYK(0.0%,0.0%,0.0%,100.0%)
# - WHITE: RGB[255, 255, 255] #FFFFFF CMYK(0.0%,0.0%,0.0%,0.0%)
```

## Examples

### Input

![Input example](https://github.com/fabricioguidine/mosaic-pixel-matrixator/blob/main/examples/images/input-example.png?raw=true)

Artwork: *São Francisco de Assis com seus companheiros* (1986), mixed media on canvas, by Nanzita (Nanzita Ladeira Salgado Alvim Gomes, 1919-2007), Cataguases, MG, Brazil.

### Output

![Output example](examples/images/output-example.png)

This sample run produced:

- 68 rows x 43 columns (2,924 tiles)
- 95.79 cm x 150.00 cm output (aspect ratio preserved)
- 32 unique colors via median cut quantization
- 5 base colors to purchase (Cyan, Magenta, Yellow, Black, White)

## Project structure

```
mosaic-pixel-matrixator/
├── main.py              # CLI entry point
├── input/               # Source images (first one is processed)
├── output/              # Generated previews and matrices
├── examples/images/     # Sample input/output for docs
├── src/
│   ├── config/          # Constants (tile size, supported formats)
│   ├── io/              # Image loading, matrix file output
│   ├── processing/      # Image resize/convert
│   ├── generation/      # Matrix dimensions and generation
│   ├── quantization/    # Median cut, CMYK/HSL, paint inventory
│   └── visualization/   # Preview image recreation
├── tests/               # Pytest suite + fixtures
├── pyproject.toml
└── requirements.txt
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for module-level detail.

## Testing

```powershell
# Run the suite with coverage (configured in pyproject.toml)
pytest

# A single test file
python -m pytest tests/test_color_quantizer.py
```

## License

Licensed under the [MIT License](LICENSE).
