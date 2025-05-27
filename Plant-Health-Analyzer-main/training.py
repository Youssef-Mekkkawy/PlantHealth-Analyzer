import os
# Turn off oneDNN/MKL conv primitives
# os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
import tensorflow as tf
# tf.config.threading.set_intra_op_parallelism_threads(1)
# tf.config.threading.set_inter_op_parallelism_threads(1)
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt

# 1. Parameters
IMAGE_SIZE = 256
BATCH_SIZE = 32
EPOCHS     = 15
DATA_DIR   = "dataset"

# 2. Community-style naming
SAVE_DIR   = "outputs/plant_health/checkpoints"
MODEL_BASE = "mixedplants_cnn_v1_20250525"
FINAL_MODEL_NAME = MODEL_BASE + ".keras"

os.makedirs(SAVE_DIR, exist_ok=True)

# 3. Load datasets
raw_train_ds = keras.utils.image_dataset_from_directory(
    DATA_DIR,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(IMAGE_SIZE, IMAGE_SIZE),
    batch_size=BATCH_SIZE
)
raw_val_ds = keras.utils.image_dataset_from_directory(
    DATA_DIR,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(IMAGE_SIZE, IMAGE_SIZE),
    batch_size=BATCH_SIZE
)

class_names = raw_train_ds.class_names
print("Detected classes:", class_names)

# 4. Performance tuning
AUTOTUNE = tf.data.AUTOTUNE
train_ds  = raw_train_ds.cache().prefetch(AUTOTUNE)
val_ds    = raw_val_ds.cache().prefetch(AUTOTUNE)

# 5. Build model
model = keras.Sequential([
    layers.Rescaling(1./255, input_shape=(IMAGE_SIZE, IMAGE_SIZE, 3)),
    layers.Conv2D(32, 3, activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(64, 3, activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(128, 3, activation='relu'),
    layers.MaxPooling2D(),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(len(class_names), activation='softmax'),
])

model.summary()

# 6. Compile
model.compile(
    optimizer='adam',
    loss=keras.losses.SparseCategoricalCrossentropy(),
    metrics=['accuracy']
)

# 7. Checkpoint callback: **only save weights** when val_accuracy improves
checkpoint_cb = keras.callbacks.ModelCheckpoint(
    filepath=os.path.join(
        SAVE_DIR,
        MODEL_BASE + "_epoch{epoch:02d}_valacc{val_accuracy:.2f}.weights.h5",
    ),
    monitor="val_accuracy",
    save_best_only=True,
    save_weights_only=True,
    mode="max",
    verbose=1
)

# 8. Train
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=EPOCHS,
    callbacks=[checkpoint_cb],
    verbose=1
)

# 9. After training, **save the full model** once in Keras V3 format
final_path = os.path.join(SAVE_DIR, FINAL_MODEL_NAME)
model.save(final_path)
print(f"Final model saved to: {final_path}")

# 10. Plot training curves
acc      = history.history['accuracy']
val_acc  = history.history['val_accuracy']
loss     = history.history['loss']
val_loss = history.history['val_loss']
epochs   = range(1, EPOCHS + 1)

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(epochs, acc,     label='Train Acc')
plt.plot(epochs, val_acc, label='Val Acc')
plt.legend(loc='lower right')
plt.title('Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs, loss,     label='Train Loss')
plt.plot(epochs, val_loss, label='Val Loss')
plt.legend(loc='upper right')
plt.title('Loss')

plt.tight_layout()
plt.show()
