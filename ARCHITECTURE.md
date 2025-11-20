# Architecture Documentation

Clean architecture with modular design and separation of concerns.

## Architecture Principles

1. **Separation of Concerns**: Each module has a single responsibility
2. **Modularity**: Components are independent and reusable
3. **Clean Architecture**: Clear dependency flow (config → io → processing → generation → quantization)
4. **Testability**: Pure functions and isolated components

## Module Structure

### 1. Configuration (`src/config/`)

**Purpose**: Centralized configuration management

**Files**:
- `constants.py`: Contains all configuration constants

**Key Constants**:
- `TILE_SIZE_CM`: Default ceramic tile size (2.0cm)
- `SUPPORTED_IMAGE_FORMATS`: Set of supported image file extensions

**Usage**:
```python
from src.config import TILE_SIZE_CM, SUPPORTED_IMAGE_FORMATS
```

### 2. Input/Output (`src/io/`)

**Purpose**: File and image input/output operations

#### `image_loader.py`
- **Responsibility**: Image file discovery and loading
- **Functions**:
  - `get_image_files(directory)`: Scans directory for supported image files
  - `load_image(image_path)`: Loads a PIL Image object from file

#### `file_handler.py`
- **Responsibility**: Saving matrix data to files
- **Functions**:
  - `save_matrix_to_file(matrix, output_path)`: Saves matrix as human-readable text
  - `save_matrix_to_json(matrix, output_path)`: Saves matrix as JSON

**Design Decision**: Separated image loading from file saving to allow independent testing and potential future formats.

### 3. Image Processing (`src/processing/`)

**Purpose**: Core image manipulation operations

#### `image_processor.py`
- **Responsibility**: Image transformations (resizing, format conversion)
- **Class**: `ImageProcessor`
- **Methods**:
  - `resize_image(image, target_rows, target_cols)`: Resizes image to specific dimensions
  - `convert_to_rgb(image)`: Ensures image is in RGB mode
  - `image_to_array(image, rows, cols)`: Converts image to numpy array

**Design Decision**: Uses LANCZOS resampling for high-quality image resizing, ensuring better color representation in the final matrix.

### 4. Matrix Generation (`src/generation/`)

**Purpose**: Matrix creation and dimension calculations

#### `matrix_generator.py`
- **Responsibility**: Matrix generation and aspect ratio preservation
- **Class**: `MatrixGenerator`
- **Methods**:
  - `calculate_matrix_dimensions(width_cm, height_cm)`: Converts cm dimensions to matrix size
  - `calculate_dimensions_preserving_aspect_ratio(image, max_width_cm, max_height_cm)`: Adjusts dimensions to maintain aspect ratio
  - `generate_matrix(image, width_cm, height_cm, preserve_aspect_ratio=True)`: Main matrix generation method
  - `get_matrix_info(matrix)`: Extracts information about the generated matrix

**Key Algorithm**: Aspect ratio preservation with closest match
- Calculates original image aspect ratio
- Evaluates two options:
  1. Fit to requested width (calculate height from aspect ratio)
  2. Fit to requested height (calculate width from aspect ratio)
- Calculates total difference for each option: |width_diff| + |height_diff|
- Chooses the option with the smallest total difference
- This ensures the output is as close as possible to requested dimensions

**Design Decision**: Aspect ratio preservation prevents image distortion, which is critical for accurate tile representation.

### 5. Visualization (`src/visualization/`)

**Purpose**: Generating visual previews

#### `image_recreator.py`
- **Responsibility**: Creating preview images from RGB matrices
- **Functions**:
  - `recreate_image_from_matrix(matrix, output_path, scale_factor=10)`: Converts matrix back to image

**Design Decision**: Uses NEAREST resampling for upscaling to maintain the pixelated tile effect. Default 10x scale makes small matrices visible.

### 6. Main Entry Point (`main.py`)

**Purpose**: Command-line interface and orchestration

**Responsibilities**:
- Parsing command-line arguments
- Orchestrating the processing pipeline
- User interaction (dimension input)
- Error handling and user feedback

**Processing Flow**:
1. Check input directory and find images
2. Load image
3. Get dimensions (CLI args or user input)
4. Initialize MatrixGenerator
5. Generate matrix (with aspect ratio preservation)
6. Save outputs (TXT, JSON, PNG)
7. Display results

## Data Flow

```
Input Image (input/)
    ↓
[image_loader.py] Load Image
    ↓
[main.py] Get Dimensions (user/CLI)
    ↓
[matrix_generator.py] Calculate Dimensions (preserve aspect ratio)
    ↓
[image_processor.py] Resize & Convert Image
    ↓
[matrix_generator.py] Generate RGB Matrix
    ↓
[file_handler.py] Save Matrix (TXT, JSON)
[image_recreator.py] Generate Preview (PNG)
    ↓
Output Files (output/)
```

## Aspect Ratio Preservation Algorithm

The core algorithm ensures images are not distorted while choosing dimensions closest to the request:

1. **Calculate Original Aspect Ratio**:
   ```python
   aspect_ratio = original_width / original_height
   ```

2. **Calculate Option 1 (Fit to Requested Width)**:
   ```python
   option1_width = requested_width
   option1_height = requested_width / aspect_ratio
   option1_total_diff = |option1_width - requested_width| + |option1_height - requested_height|
   ```

3. **Calculate Option 2 (Fit to Requested Height)**:
   ```python
   option2_width = requested_height * aspect_ratio
   option2_height = requested_height
   option2_total_diff = |option2_width - requested_width| + |option2_height - requested_height|
   ```

4. **Choose Closest Match**:
   - Compare total differences of both options
   - Select the option with the smallest total difference
   - This ensures the output dimensions are as close as possible to what was requested
   - Display differences to the user for transparency

## File Naming Convention

Output files follow this pattern:
- **Preview**: `{image_name}-{timestamp}.png`
- **Matrix Text**: `{image_name}-{timestamp}_matrix.txt`
- **Matrix JSON**: `{image_name}-{timestamp}_matrix.json`

Timestamp format: `YYYYMMDD_HHMMSS` (e.g., `20250115_143052`)

**Design Decision**: Includes image name for easy identification and timestamp to prevent overwrites.

## Matrix Data Structure

The RGB matrix is a NumPy array with shape `(rows, cols, 3)`:
- **First dimension**: Number of rows (vertical tiles)
- **Second dimension**: Number of columns (horizontal tiles)
- **Third dimension**: RGB values [R, G, B] each from 0-255

Example:
```python
matrix[row][col] = [255, 128, 64]  # Red=255, Green=128, Blue=64
```

## Extension Points

The architecture allows for easy extensions:

1. **New File Formats**: Add handlers in `io/file_handler.py`
2. **Different Tile Sizes**: Modify `config/constants.py` or make it configurable
3. **Additional Output Formats**: Extend `matrix_generator.py` or add new generators
4. **Image Filters**: Add preprocessing in `processing/image_processor.py`
5. **Batch Processing**: Extend `main.py` to process multiple images

## Dependencies

- **Pillow (PIL)**: Image loading, resizing, and format conversion
- **NumPy**: Matrix operations and array handling

## Testing Strategy

Each module can be tested independently:
- `io/`: Test file operations with mock files
- `processing/`: Test transformations with sample images
- `generation/`: Test dimension calculations with known inputs
- `visualization/`: Test preview generation with sample matrices

## Performance Considerations

1. **Image Resizing**: Uses LANCZOS resampling (high quality, slightly slower)
2. **Matrix Generation**: Direct numpy array conversion (fast)
3. **File I/O**: Sequential operations, could be parallelized for batch processing
4. **Memory**: Large images are resized before conversion to reduce memory usage

## Future Enhancements

Potential improvements to the architecture:
1. **Batch Processing**: Process multiple images in one run
2. **Color Quantization**: Reduce color palette for ceramic tile availability
3. **Configuration File**: External configuration for tile sizes and formats
4. **Progress Bars**: For large image processing
5. **Image Selection**: Allow user to choose which image to process
6. **Custom Tile Sizes**: Support non-square tiles (rectangular)

