import sys
import os
from pathlib import Path
import numpy as np
import tensorflow as tf
from PIL import Image
from io import BytesIO

# ─── CONFIGURE LOGGING & ENVIRONMENT ─────────────────────────────────────
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.get_logger().setLevel('ERROR')

# ─── DETERMINE PROJECT ROOT ───────────────────────────────────────────────
# Use current file or executable path, then climb up until finding the 'analyzer' directory
start_path = Path(sys.executable if getattr(sys, 'frozen', False) else __file__).resolve().parent
PROJECT_ROOT = None
for parent in [start_path] + list(start_path.parents):
    if (parent / 'analyzer').is_dir():
        PROJECT_ROOT = parent
        break
if PROJECT_ROOT is None:
    # fallback to cwd
    PROJECT_ROOT = Path.cwd()

# ─── PATHS ────────────────────────────────────────────────────────────────
ANALYZER_DIR = PROJECT_ROOT / 'analyzer'
DATA_DIR     = ANALYZER_DIR / 'dataset'
MODEL_PATH   = ANALYZER_DIR / 'outputs' / 'plant_health' / 'checkpoints' / 'mixedplants_cnn_v1_20250525.keras'
IMG_SIZE     = (256, 256)

# ─── DEBUG OUTPUT ─────────────────────────────────────────────────────────
print(f"PROJECT_ROOT: {PROJECT_ROOT}")
print(f"ANALYZER_DIR: {ANALYZER_DIR}")
print(f"DATA_DIR:     {DATA_DIR}")
print(f"MODEL_PATH:   {MODEL_PATH}")

# ─── VALIDATE MODEL ────────────────────────────────────────────────────────
if not MODEL_PATH.exists():
    sys.stderr.write(f"Error: model not found at {MODEL_PATH}\n")
    sys.exit(1)
model = tf.keras.models.load_model(str(MODEL_PATH))

# ─── LOAD CLASSES ─────────────────────────────────────────────────────────
def load_classes(data_dir: Path):
    if data_dir.exists():
        subdirs = [p.name for p in data_dir.iterdir() if p.is_dir()]
        if subdirs:
            return sorted(subdirs)
    sys.stderr.write(f"Warning: '{data_dir}' is missing or empty; using default classes.\n")
    return [
        'Pepper__bell___Bacterial_spot', 'Pepper__bell___healthy',
        'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy',
        'Tomato_Bacterial_spot', 'Tomato_Early_blight', 'Tomato_Late_blight',
        'Tomato_Leaf_Mold', 'Tomato_Septoria_leaf_spot',
        'Tomato_Spider_mites_Two_spotted_spider_mite', 'Tomato__Target_Spot',
        'Tomato__Tomato_YellowLeaf__Curl_Virus', 'Tomato__Tomato_mosaic_virus',
        'Tomato_healthy'
    ]
classes = load_classes(DATA_DIR)
if model.output_shape[-1] != len(classes):
    sys.stderr.write(
        f"Error: model outputs {model.output_shape[-1]}, but found {len(classes)} classes\n"
    )
    sys.exit(1)

# ─── IMAGE HANDLING ───────────────────────────────────────────────────────
def read_image_file(path: Path) -> np.ndarray:
    data = path.read_bytes()
    img = Image.open(BytesIO(data)).convert("RGB")
    img = img.resize(IMG_SIZE)
    return np.array(img)

# ─── MAIN ENTRYPOINT ─────────────────────────────────────────────────────
def main():
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: cli.py <image_path>\n")
        sys.exit(1)

    image_path = Path(sys.argv[1])
    if not image_path.is_file():
        sys.stderr.write(f"Error: file not found: {image_path}\n")
        sys.exit(1)

    img_arr = read_image_file(image_path)
    batch   = np.expand_dims(img_arr, 0)
    preds   = model.predict(batch)[0]

    idx        = int(np.argmax(preds))
    label      = classes[idx]
    confidence = float(preds[idx]) * 100
    sys.stdout.write(f"{label}:{confidence:.2f}%\n")

if __name__ == "__main__":
    main()