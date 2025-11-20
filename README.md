# Mosaic Pixel Matrixator

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

> Convert images into ceramic tile color matrices with paint mixing instructions.

A Python tool that transforms images into ceramic tile mosaics by generating RGB color matrices with primary color mix percentages. Perfect for artists and craftspeople who want to create pixel art mosaics from images.

## 🚀 Features

- **📸 Image Processing**: Supports common formats (JPG, PNG, BMP, GIF, TIFF, WEBP)
- **📐 Aspect Ratio Preservation**: Automatically maintains image proportions
- **🎨 High-Quality Quantization**: Median cut algorithm for optimized color reduction
- **🎨 Industry-Standard Colors**: CMYK (paint/printing) and Hex codes for color matching
- **📦 Paint Inventory**: Lists all required paint colors with usage counts
- **📊 Multiple Outputs**: TXT, JSON matrices + PNG preview + paint inventory
- **⚙️ Configurable**: Custom tile size and color palette options

## 📋 Requirements

- Python 3.8 or higher
- Pillow >= 10.0.0
- NumPy >= 1.24.0

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/fabricioguidine/mosaic-pixel-matrixator.git
cd mosaic-pixel-matrixator

# Install dependencies
pip install -r requirements.txt
```

## 🎯 Quick Start

1. **Place your image** in the `input/` folder

2. **Run the script**:
   ```bash
   python main.py --width 200 --height 150
   ```

3. **Get results** in the `output/` folder:
   - `{name}-{timestamp}.png` - Visual preview
   - `{name}-{timestamp}_matrix.txt` - Human-readable matrix
   - `{name}-{timestamp}_matrix.json` - JSON format
   - `{name}-{timestamp}_paints.json` - Paint color inventory

## 📖 Usage Examples

### Interactive Mode

```bash
python main.py
# Enter dimensions when prompted
```

### Command-Line Options

```bash
# Basic usage
python main.py --width 200 --height 150

# Custom tile size
python main.py --width 200 --height 150 --tile-size 2.5

# Custom color palette
python main.py --width 200 --height 150 --num-colors 128

# Disable quantization (use original colors)
python main.py --width 200 --height 150 --no-quantize
```

### Options Reference

| Option | Description | Default |
|--------|-------------|---------|
| `--width` | Maximum width in centimeters | Prompted |
| `--height` | Maximum height in centimeters | Prompted |
| `--tile-size` | Tile size in centimeters | 2.2cm |
| `--num-colors` | Number of colors in palette | 64 |
| `--no-quantize` | Disable color quantization | False |

## 🖼️ Example Results

### Original Input Image

![Input Image](https://github.com/fabricioguidine/mosaic-pixel-matrixator/blob/main/examples/images/input-example.png?raw=true)

**Artwork Attribution:**
- **Artist**: Nanzita (Nanzita Ladeira Salgado Alvim Gomes, 1919-2007)
- **Title**: São Francisco de Assis com seus companheiros
- **Technique**: Técnica mista sobre tela (Mixed media on canvas)
- **Year**: 1986
- **Location**: Cataguases, MG, Brazil

### Processed Output

![Output Example](examples/images/output-example.png)

**Example Processing Results:**
- **Dimensions**: 68 rows × 43 columns (2,924 tiles total)
- **Output Size**: 95.79cm × 150.00cm (aspect ratio preserved)
- **Color Quantization**: Median cut algorithm (32 unique colors)
- **Paint Colors**: All colors tracked with usage counts
- **Mix Information**: Each tile shows R%, G%, B% percentages

## 🔧 How It Works

1. **Image Loading**: Loads image from `input/` folder
2. **Aspect Ratio Calculation**: Calculates and preserves aspect ratio
3. **Dimension Calculation**: Chooses closest match to requested dimensions
4. **Matrix Size Calculation**: Calculates tiles needed (dimensions ÷ tile size)
5. **Image Resizing**: Resizes to matrix dimensions
6. **Color Quantization**: Uses median cut algorithm to create optimized palette
7. **Primary Color Mix**: Calculates Red, Green, Blue mix percentages
8. **Paint Inventory**: Tracks all unique colors with usage counts
9. **File Output**: Saves matrix in TXT and JSON formats
10. **Preview Generation**: Creates visual preview image

### Key Rules

- **Aspect Ratio**: Always preserved (no distortion)
- **Closest Match**: Dimensions use closest match algorithm
- **Industry Standards**: Each color shows CMYK (for paint mixing) and Hex (for reference)
- **Tile Size**: Default 2.2cm, customizable via `--tile-size`
- **Color Quantization**: Default 64 colors using median cut

## 📄 Output Formats

### Text Matrix (`{name}-{timestamp}_matrix.txt`)

```
# RGB Color Matrix
# Matrix dimensions: 68 rows x 43 columns
# Format: R,G,B[C:cyan%,M:magenta%,Y:yellow%,K:black%] #HEX
# CMYK percentages for paint mixing (industry standard)

# Row 1
109,73,77[C:0.0%,M:32.9%,Y:29.4%,K:57.3%] #6D494D 111,76,80[C:0.0%,M:31.5%,Y:27.9%,K:56.5%] #6F4C50 ...
```

### JSON Matrix (`{name}-{timestamp}_matrix.json`)

```json
{
  "dimensions": {
    "rows": 68,
    "columns": 43
  },
  "matrix": [
    [
      {
        "rgb": [109, 73, 77],
        "hex": "#6D494D",
        "cmyk": {
          "c": 0.0,
          "m": 32.9,
          "y": 29.4,
          "k": 57.3
        },
        "hsl": {
          "h": 353.3,
          "s": 19.8,
          "l": 35.7
        }
      }
    ]
  ]
}
```

### Paint Colors (`{name}-{timestamp}_paints.json`)

```json
{
  "total_unique_colors": 32,
  "total_tiles": 2924,
  "required_paints": [
    {
      "rgb": [255, 255, 255],
      "hex": "#FFFFFF",
      "cmyk": {
        "c": 0.0,
        "m": 0.0,
        "y": 0.0,
        "k": 0.0
      },
      "hsl": {
        "h": 0.0,
        "s": 0.0,
        "l": 100.0
      },
      "count": 450
    }
  ]
}
```

**Color System Explanation:**
- **RGB**: Digital color values (0-255) - standard for screens/displays
- **Hex**: Hexadecimal color code (e.g., `#FFFFFF` for white) - universal color reference
- **CMYK**: Cyan, Magenta, Yellow, Black percentages (0-100%) - **industry standard for paint/printing**
  - Use CMYK values to mix paint colors or purchase from paint suppliers
  - Each percentage tells you how much of each primary paint color to mix
- **HSL**: Hue, Saturation, Lightness - intuitive color description

**For Paint Purchasing:**
Use the **CMYK values** or **Hex codes** when ordering from paint suppliers. Most paint stores can match colors using these industry-standard codes.

## 🏗️ Project Structure

```
mosaic-pixel-matrixator/
├── input/           # Input images folder
├── output/          # Generated matrices and previews
├── examples/        # Example images for documentation
├── tests/           # Unit tests
├── src/
│   ├── config/      # Configuration constants
│   ├── io/          # File I/O operations
│   ├── processing/  # Image processing
│   ├── generation/  # Matrix generation
│   ├── quantization/ # Color quantization & paint management
│   └── visualization/ # Preview generation
├── main.py          # CLI entry point
└── requirements.txt # Dependencies
```

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_color_quantizer.py

# Run with coverage
pytest --cov=src tests/
```

## 📚 Architecture

Clean modular architecture with separation of concerns:
- **`config/`**: Constants (tile size, supported formats)
- **`io/`**: File operations (load images, save matrices)
- **`processing/`**: Image transformations (resize, convert)
- **`generation/`**: Matrix creation (dimensions, aspect ratio)
- **`quantization/`**: Color reduction & paint inventory
- **`visualization/`**: Preview image generation

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed documentation.

## 🐛 Troubleshooting

### No image files found
- Ensure your image is in the `input/` folder
- Check that the file format is supported

### Dimensions seem incorrect
- The tool preserves aspect ratio, so actual dimensions may differ
- Check the output message for actual dimensions used

### Import errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check that you're using Python 3.8 or higher

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Original artwork by Nanzita (1919-2007)
- Median cut quantization algorithm for high-quality color reduction

---

Made with ❤️ for artists and crafters
