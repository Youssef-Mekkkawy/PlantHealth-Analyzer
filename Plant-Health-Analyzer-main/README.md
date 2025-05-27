# 🌱 Plant Disease Detection System

> *An AI-powered system for detecting plant diseases using Convolutional Neural Networks*

---

## 📦 Deployment & Distribution

### Converting to Executable (.exe)

The CLI interface can be packaged as a standalone executable using PyInstaller, making it easy to distribute without requiring Python installation.

#### 🔧 Installation

```bash
pip install pyinstaller
```

#### 🏗️ Building the Executable

**Basic Build:**
```bash
pyinstaller --onefile cli.py
```

**Advanced Build with Optimizations:**
```bash
pyinstaller --onefile \
    --name plant_disease_detector \
    --icon=icon.ico \
    --add-data "analyzer;analyzer" \
    --hidden-import=tensorflow \
    --hidden-import=PIL \
    --console \
    cli.py
```

#### ⚙️ PyInstaller Configuration

Create a `build_config.spec` file for reproducible builds:

```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['cli.py'],
    pathex=[],
    binaries=[],
    datas=[('analyzer', 'analyzer')],
    hiddenimports=['tensorflow', 'PIL', 'numpy'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='plant_disease_detector',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
```

**Build with spec file:**
```bash
pyinstaller build_config.spec
```

#### 📁 Distribution Structure

After building, your distribution will look like:

```
project_root/
├── dist/
│   └── plant_disease_detector.exe  # Standalone executable
├── build/                          # Build artifacts (can be deleted)
├── cli.py                         # Original source
├── analyzer/                      # Data directory (copy with exe)
│   ├── dataset/
│   └── outputs/
└── plant_disease_detector.spec    # Build configuration
```

#### 🚀 Using the Executable

**Windows:**
```cmd
# Navigate to the dist folder
cd dist

# Run the executable
plant_disease_detector.exe path\to\image.jpg
```

**Command Line:**
```bash
# From anywhere (if added to PATH)
plant_disease_detector.exe C:\path\to\plant_image.jpg

# Example output:
# bacterial_leaf_blight:87.43%
```

#### 📋 Distribution Checklist

When distributing your application:

- [ ] ✅ Include the `analyzer/` folder with the executable
- [ ] ✅ Ensure the trained model (`.keras` file) is in `analyzer/outputs/plant_health/checkpoints/`
- [ ] ✅ Test the executable on a clean system without Python
- [ ] ✅ Provide sample images for testing
- [ ] ✅ Include usage instructions

#### ⚡ Optimization Tips

**Reduce File Size:**
```bash
# Exclude unnecessary modules
pyinstaller --onefile \
    --exclude-module matplotlib \
    --exclude-module tkinter \
    cli.py
```

**Faster Startup:**
```bash
# Use --onedir for faster startup (larger distribution)
pyinstaller --onedir cli.py
```

#### 🎯 Deployment Scenarios

**1. Single User Installation:**
- Distribute `dist/plant_disease_detector.exe` + `analyzer/` folder
- User can run directly from any location

**2. System-wide Installation:**
```batch
@echo off
REM install.bat
copy plant_disease_detector.exe C:\Program Files\PlantDetector\
xcopy /E /I analyzer C:\Program Files\PlantDetector\analyzer
echo Installation complete!
```

**3. Portable Application:**
- Package everything in a single ZIP file
- No installation required, runs from any folder

#### 🔒 Code Signing (Optional)

For professional distribution:

```bash
# Sign the executable (requires certificate)
signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com plant_disease_detector.exe
```

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Training Module](#-training-module)
- [CLI Interface](#-cli-interface)
- [Model Architecture](#-model-architecture)
- [Usage Examples](#-usage-examples)
- [Technical Specifications](#-technical-specifications)
- [Deployment & Distribution](#-deployment--distribution)
- [Troubleshooting](#-troubleshooting)

---

## 🔍 Overview

The Plant Disease Detection System is a machine learning application that uses deep learning to identify plant diseases from images. The system consists of two main components:

- **Training Pipeline** (`training.py`) - For training CNN models on plant disease datasets
- **CLI Interface** (`cli.py`) - For real-time disease detection from image files

### ✨ Key Features

- 🎯 **High Accuracy**: CNN-based classification with 256x256 image processing
- 🚀 **Fast Inference**: Optimized model loading and prediction pipeline
- 📁 **Flexible Dataset**: Supports multiple plant disease classes
- 💻 **Command Line Interface**: Easy-to-use CLI for batch processing
- 📊 **Training Visualization**: Built-in plotting for training metrics

---

## 📁 Project Structure

```
project_root/
├── cli.py                     # Command-line interface for predictions
├── training.py                # Model training script
├── analyzer/                  # Main analyzer directory
│   ├── dataset/              # Training data directory
│   │   ├── class_1/          # Disease/healthy class 1
│   │   │   ├── image1.jpg
│   │   │   └── image2.jpg
│   │   ├── class_2/          # Disease/healthy class 2
│   │   └── ...
│   └── outputs/
│       └── plant_health/
│           └── checkpoints/   # Trained models and weights
│               ├── *.keras    # Final trained models
│               └── *.weights.h5  # Training checkpoints
└── README.md
```

### 📂 Directory Descriptions

| Directory | Purpose |
|-----------|---------|
| `cli.py` | Command-line interface for making predictions |
| `training.py` | Model training script |
| `analyzer/` | Main analyzer directory containing all project data |
| `analyzer/dataset/` | Contains training images organized by class |
| `analyzer/outputs/plant_health/checkpoints/` | Stores trained models and training checkpoints |

---

## 🚀 Getting Started

### Prerequisites

```bash
pip install tensorflow pillow numpy matplotlib
```

### 📦 Required Dependencies

- **TensorFlow** `>=2.0` - Deep learning framework
- **Pillow** - Image processing library
- **NumPy** - Numerical computing
- **Matplotlib** - For training visualization

---

## 🧠 Training Module

### `training.py` - Model Training Pipeline

The training module implements a comprehensive CNN training pipeline for plant disease classification.

#### 🔧 Configuration Parameters

```python
IMAGE_SIZE = 256      # Input image dimensions (256x256)
BATCH_SIZE = 32       # Training batch size
EPOCHS = 15           # Number of training epochs
DATA_DIR = "dataset"  # Path to training data
```

#### 🏗️ Model Architecture

The system uses a Sequential CNN model with the following layers:

1. **Input Layer**: 256×256×3 RGB images
2. **Preprocessing**: Rescaling (normalization to 0-1 range)
3. **Convolutional Blocks**:
   - Conv2D (32 filters) + MaxPooling2D
   - Conv2D (64 filters) + MaxPooling2D  
   - Conv2D (128 filters) + MaxPooling2D
4. **Dense Layers**:
   - Flatten layer
   - Dense (128 units, ReLU activation)
   - Output Dense (num_classes, Softmax activation)

#### 🎯 Training Features

- **Data Augmentation**: Automatic train/validation split (80/20)
- **Model Checkpointing**: Saves best weights based on validation accuracy
- **Performance Optimization**: Dataset caching and prefetching
- **Visual Monitoring**: Real-time accuracy and loss plotting

#### 💾 Output Files

| File Type | Naming Convention | Purpose |
|-----------|------------------|---------|
| `.keras` | `mixedplants_cnn_v1_YYYYMMDD.keras` | Final trained model |
| `.weights.h5` | `*_epoch{XX}_valacc{X.XX}.weights.h5` | Training checkpoints |

---

## 💻 CLI Interface

### `cli.py` - Command Line Prediction Tool

The CLI module provides a streamlined interface for making predictions on individual images.

#### 🔍 Key Features

- **Automatic Model Loading**: Loads the trained Keras model
- **Dynamic Class Detection**: Automatically detects classes from dataset structure
- **Image Preprocessing**: Handles image loading, resizing, and normalization
- **Confidence Scoring**: Returns prediction confidence as percentage

#### 🖥️ Usage Syntax

```bash
python cli.py <image_path>
```

#### 📤 Output Format

```
<predicted_class>:<confidence_percentage>%
```

#### ⚙️ Technical Implementation

```python
# Model Configuration
IMG_SIZE = (256, 256)                    # Input image size
MODEL_PATH = "outputs/.../model.keras"  # Trained model path

# Prediction Pipeline
1. Load and validate model
2. Preprocess input image
3. Generate prediction
4. Return formatted result
```

#### 🛡️ Error Handling

- **File Validation**: Checks if image file exists
- **Model Validation**: Verifies model-class compatibility
- **Path Resolution**: Handles both frozen (.exe) and script execution

---

## 🏛️ Model Architecture

### Network Design

```
Input (256×256×3)
       ↓
   Rescaling (1./255)
       ↓
   Conv2D (32, 3×3, ReLU)
       ↓
   MaxPooling2D (2×2)
       ↓
   Conv2D (64, 3×3, ReLU)
       ↓
   MaxPooling2D (2×2)
       ↓
   Conv2D (128, 3×3, ReLU)
       ↓
   MaxPooling2D (2×2)
       ↓
     Flatten
       ↓
   Dense (128, ReLU)
       ↓
   Dense (num_classes, Softmax)
       ↓
    Output Probabilities
```

### 📊 Model Specifications

| Parameter | Value |
|-----------|-------|
| **Input Shape** | (256, 256, 3) |
| **Total Layers** | 9 |
| **Trainable Parameters** | ~2.5M (varies by class count) |
| **Optimizer** | Adam |
| **Loss Function** | Sparse Categorical Crossentropy |
| **Metrics** | Accuracy |

---

## 💡 Usage Examples

### Training a New Model

```bash
# Prepare your dataset in the following structure:
# analyzer/dataset/
#   ├── healthy_plant/
#   ├── disease_1/
#   ├── disease_2/
#   └── ...

# Run training from project root
python training.py
```

### Making Predictions

```bash
# Single image prediction
python cli.py path/to/plant_image.jpg

# Example output:
# bacterial_leaf_blight:87.43%
```

### Batch Processing (Shell Script)

```bash
#!/bin/bash
for img in test_images/*.jpg; do
    echo "Processing: $img"
    python cli.py "$img"
done
```

---

## ⚙️ Technical Specifications

### 🖼️ Image Requirements

- **Format**: JPG, PNG, or other PIL-supported formats
- **Size**: Any size (automatically resized to 256×256)
- **Channels**: RGB (converted automatically if needed)

### 🔧 Environment Configuration

The system includes several optimizations for better performance:

```python
# Disable oneDNN messages for cleaner output
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Suppress TensorFlow logging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.get_logger().setLevel(logging.ERROR)
```

### 🎯 Path Resolution

The CLI automatically handles different execution contexts:

```python
# Supports both script execution and PyInstaller .exe
if getattr(sys, 'frozen', False):
    # Running as .exe
    exe_dir = os.path.dirname(sys.executable)
    PROJECT_ROOT = os.path.abspath(os.path.join(exe_dir, os.pardir))
else:
    # Running as Python script
    script_dir = os.path.dirname(os.path.realpath(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(script_dir, os.pardir))
```

### 💾 Memory Optimization

- **Dataset Caching**: Caches preprocessed data for faster training
- **Prefetching**: Overlaps data loading with model execution
- **Batch Processing**: Efficiently processes multiple images

---

## 🔧 Troubleshooting

### Common Issues and Solutions

#### ❌ "Model not found" Error

```bash
Error: model not found at 'outputs/plant_health/checkpoints/...'
```

**Solution**: Run `training.py` first to generate the model file.

#### ❌ Class Mismatch Error

```bash
Error: model outputs X but found Y classes
```

**Solution**: Ensure the dataset structure matches the trained model's classes.

#### ❌ Image Loading Issues

**Solutions**:
- Verify image file exists and is readable
- Check image format compatibility
- Ensure sufficient disk space

#### ⚠️ Performance Issues

**Optimizations**:
- Use SSD storage for dataset
- Increase `BATCH_SIZE` if you have sufficient GPU memory
- Enable GPU acceleration if available

#### 🔧 Executable Issues

**Problem**: "Cannot find analyzer folder"
```
Error: model not found at 'analyzer/outputs/...'
```

**Solution**: Ensure the `analyzer/` folder is in the same directory as the `.exe` file.

**Problem**: "DLL load failed" on Windows
**Solutions**:
- Install Microsoft Visual C++ Redistributable
- Use `--hidden-import` for missing modules during build
- Test on the target system before distribution

**Problem**: Large executable file size
**Solutions**:
```bash
# Exclude unnecessary modules
pyinstaller --onefile --exclude-module matplotlib cli.py

# Use UPX compression
pyinstaller --onefile --upx-dir /path/to/upx cli.py
```

---

## 📈 Model Performance Tips

### 🎯 Improving Accuracy

1. **Data Quality**: Use high-resolution, well-lit images
2. **Data Balance**: Ensure equal representation of all classes
3. **Data Augmentation**: Add rotation, flipping, and scaling
4. **Training Duration**: Increase epochs for complex datasets

### 🚀 Optimization Strategies

- **Learning Rate Scheduling**: Implement adaptive learning rates
- **Early Stopping**: Prevent overfitting with validation monitoring
- **Transfer Learning**: Use pre-trained models for better starting weights

---

## 📞 Support

For technical support or feature requests:

1. Check the troubleshooting section above
2. Verify all dependencies are correctly installed
3. Ensure dataset structure follows the specified format
4. Review error messages for specific guidance

---

*Built with ❤️ using TensorFlow and Python*