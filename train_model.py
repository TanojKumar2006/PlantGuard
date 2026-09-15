"""
PlantGuard AI – EfficientNetB0 Training Script
================================================
Usage:
    python train_model.py --data_dir ./data/PlantVillage --epochs 50 --batch 32

Dataset: PlantVillage (38-class version)
Download:
    Kaggle:   https://www.kaggle.com/datasets/emmarex/plantdisease
    Mendeley: https://data.mendeley.com/datasets/tywbtsjrjv/1

After training, the model weights are saved to:
    backend/model/plantguard_efficientnetb0.h5

Additionally saves:
    backend/model/class_names.json           – class index → label mapping
    backend/model/classification_report.json – per-class precision/recall/F1
    backend/model/training_history.json      – epoch-by-epoch accuracy/loss
    backend/model/confusion_matrix.json      – 5×5 confusion matrix for top classes
    backend/model/training_curves.png        – accuracy/loss plot

Requirements (in addition to requirements.txt):
    tensorflow matplotlib scikit-learn tqdm

Install:
    pip install tensorflow matplotlib scikit-learn tqdm
"""
import argparse
import os
import sys
import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")  # headless-safe backend
import matplotlib.pyplot as plt

# ── Args ─────────────────────────────────────────────────────────────────────
parser = argparse.ArgumentParser(description="Train PlantGuard EfficientNetB0 model")
parser.add_argument("--data_dir", type=str, default="./data/PlantVillage",
                    help="Path to PlantVillage dataset (sub-folders = class names)")
parser.add_argument("--epochs", type=int, default=50)
parser.add_argument("--batch", type=int, default=32)
parser.add_argument("--img_size", type=int, default=224)
parser.add_argument("--lr", type=float, default=1e-4)
parser.add_argument("--output_dir", type=str, default="./model")
parser.add_argument("--fine_tune_from", type=int, default=100,
                    help="Layer index from which to unfreeze for fine-tuning (second phase)")
parser.add_argument("--val_split", type=float, default=0.2,
                    help="Fraction of data to use for validation")
args = parser.parse_args()

DATA_DIR = Path(args.data_dir)
OUTPUT_DIR = Path(args.output_dir)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

if not DATA_DIR.exists():
    print(f"ERROR: Data directory not found: {DATA_DIR}")
    print("Please download PlantVillage from Kaggle and extract it so each class is a sub-folder.")
    print("  kaggle datasets download -d emmarex/plantdisease")
    sys.exit(1)

# ── Imports ──────────────────────────────────────────────────────────────────
import tensorflow as tf
from tensorflow.keras import layers, models, callbacks
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.applications.efficientnet import preprocess_input
from sklearn.metrics import classification_report, confusion_matrix

print(f"TensorFlow version: {tf.__version__}")
print(f"GPUs available: {tf.config.list_physical_devices('GPU')}")

IMG_SIZE = (args.img_size, args.img_size)
PHASE1_EPOCHS = max(10, args.epochs // 2)
PHASE2_EPOCHS = args.epochs

# ── Data loading ─────────────────────────────────────────────────────────────
print("\nLoading dataset...")

train_ds = tf.keras.utils.image_dataset_from_directory(
    DATA_DIR,
    validation_split=args.val_split,
    subset="training",
    seed=42,
    image_size=IMG_SIZE,
    batch_size=args.batch,
    label_mode="int",
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    DATA_DIR,
    validation_split=args.val_split,
    subset="validation",
    seed=42,
    image_size=IMG_SIZE,
    batch_size=args.batch,
    label_mode="int",
)

class_names = train_ds.class_names
NUM_CLASSES = len(class_names)
print(f"Classes found: {NUM_CLASSES}")
print("Classes:", class_names[:5], "...")

# Save class index → label mapping for inference
class_names_path = OUTPUT_DIR / "class_names.json"
with open(class_names_path, "w") as f:
    json.dump(class_names, f, indent=2)
print(f"Class names saved to: {class_names_path}")

# ── Preprocessing & augmentation ─────────────────────────────────────────────
augment = tf.keras.Sequential([
    layers.RandomFlip("horizontal_and_vertical"),
    layers.RandomRotation(0.2),
    layers.RandomZoom(0.15),
    layers.RandomBrightness(0.15),
    layers.RandomContrast(0.1),
], name="augmentation")

AUTOTUNE = tf.data.AUTOTUNE


def preprocess(img, label):
    img = tf.cast(img, tf.float32)
    img = preprocess_input(img)  # EfficientNet: rescale to [-1, 1]
    return img, label


train_ds = (
    train_ds
    .map(lambda x, y: (augment(x, training=True), y), num_parallel_calls=AUTOTUNE)
    .map(preprocess, num_parallel_calls=AUTOTUNE)
    .prefetch(AUTOTUNE)
)

val_ds = (
    val_ds
    .map(preprocess, num_parallel_calls=AUTOTUNE)
    .prefetch(AUTOTUNE)
)

# ── Model definition ──────────────────────────────────────────────────────────
print("\nBuilding EfficientNetB0 model...")

base = EfficientNetB0(weights="imagenet", include_top=False, input_shape=(*IMG_SIZE, 3))
base.trainable = False  # Phase 1: freeze base

inputs = layers.Input(shape=(*IMG_SIZE, 3), name="input_layer")
x = base(inputs, training=False)
x = layers.GlobalAveragePooling2D(name="global_avg_pool")(x)
x = layers.BatchNormalization()(x)
x = layers.Dense(256, activation="relu", name="dense_256")(x)
x = layers.Dropout(0.3, name="dropout_0.3")(x)
outputs = layers.Dense(NUM_CLASSES, activation="softmax", name="predictions")(x)

model = models.Model(inputs, outputs, name="PlantGuard_EfficientNetB0")
model.summary()

print(f"\nTotal parameters: {model.count_params():,}")
print(f"Trainable parameters (Phase 1): {sum(p.numpy().size for p in model.trainable_weights):,}")

# ── Callbacks ─────────────────────────────────────────────────────────────────
best_model_path = str(OUTPUT_DIR / "plantguard_efficientnetb0_best.h5")
cbs = [
    callbacks.ModelCheckpoint(
        best_model_path,
        monitor="val_accuracy",
        save_best_only=True,
        verbose=1,
    ),
    callbacks.EarlyStopping(
        monitor="val_accuracy",
        patience=8,
        restore_best_weights=True,
        verbose=1,
    ),
    callbacks.ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.5,
        patience=4,
        min_lr=1e-7,
        verbose=1,
    ),
    callbacks.TensorBoard(log_dir=str(OUTPUT_DIR / "logs")),
]

# ── Phase 1: Train classifier head (base frozen) ──────────────────────────────
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=args.lr),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)

print(f"\n── Phase 1: Training classifier head (base frozen) – {PHASE1_EPOCHS} epochs ──")
h1 = model.fit(train_ds, validation_data=val_ds, epochs=PHASE1_EPOCHS, callbacks=cbs)

# ── Phase 2: Fine-tune upper layers ───────────────────────────────────────────
print(f"\n── Phase 2: Fine-tuning from layer {args.fine_tune_from} onwards ──")
base.trainable = True
for layer in base.layers[:args.fine_tune_from]:
    layer.trainable = False

trainable_count = sum(p.numpy().size for p in model.trainable_weights)
print(f"Trainable parameters (Phase 2): {trainable_count:,}")

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=args.lr / 10),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)

h2 = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=PHASE2_EPOCHS,
    initial_epoch=len(h1.history["accuracy"]),
    callbacks=cbs,
)

# ── Save final model ──────────────────────────────────────────────────────────
final_path = str(OUTPUT_DIR / "plantguard_efficientnetb0.h5")
model.save(final_path)
print(f"\n✓ Model saved to: {final_path}")

# ── Evaluation ────────────────────────────────────────────────────────────────
print("\nEvaluating on validation set...")
val_loss, val_acc = model.evaluate(val_ds, verbose=1)
print(f"Validation accuracy: {val_acc:.4f}")
print(f"Validation loss:     {val_loss:.4f}")

# Per-class classification report
print("\nComputing classification report...")
y_true, y_pred = [], []
for imgs, labels in val_ds:
    preds = model.predict(imgs, verbose=0)
    y_true.extend(labels.numpy().tolist())
    y_pred.extend(np.argmax(preds, axis=1).tolist())

report_dict = classification_report(
    y_true, y_pred,
    target_names=class_names,
    output_dict=True,
    zero_division=0,
)
report_path = OUTPUT_DIR / "classification_report.json"
with open(report_path, "w") as f:
    json.dump(report_dict, f, indent=2)
print(f"✓ Classification report saved to: {report_path}")
print("\n" + classification_report(y_true, y_pred, target_names=class_names, zero_division=0))

# Confusion matrix (top 10 classes by support for readability)
from collections import Counter
top10_idx = [i for i, _ in Counter(y_true).most_common(10)]
top10_names = [class_names[i] for i in top10_idx]
y_true_filtered = [y for y in y_true if y in top10_idx]
y_pred_filtered = [y_pred[i] for i, y in enumerate(y_true) if y in top10_idx]

cm = confusion_matrix(y_true_filtered, y_pred_filtered, labels=top10_idx)
cm_dict = {
    "labels": top10_names,
    "matrix": cm.tolist(),
}
cm_path = OUTPUT_DIR / "confusion_matrix.json"
with open(cm_path, "w") as f:
    json.dump(cm_dict, f, indent=2)
print(f"✓ Confusion matrix saved to: {cm_path}")

# ── Save training history JSON (for analytics dashboard) ─────────────────────
all_acc      = h1.history["accuracy"]      + h2.history.get("accuracy", [])
all_val_acc  = h1.history["val_accuracy"]  + h2.history.get("val_accuracy", [])
all_loss     = h1.history["loss"]          + h2.history.get("loss", [])
all_val_loss = h1.history["val_loss"]      + h2.history.get("val_loss", [])

history_dict = {
    "epochs": list(range(1, len(all_acc) + 1)),
    "train_acc":  [round(float(v), 4) for v in all_acc],
    "val_acc":    [round(float(v), 4) for v in all_val_acc],
    "train_loss": [round(float(v), 4) for v in all_loss],
    "val_loss":   [round(float(v), 4) for v in all_val_loss],
    "phase1_end_epoch": len(h1.history["accuracy"]),
}
history_path = OUTPUT_DIR / "training_history.json"
with open(history_path, "w") as f:
    json.dump(history_dict, f, indent=2)
print(f"✓ Training history saved to: {history_path}")

# ── Plot training history ─────────────────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
phase1_end = len(h1.history["accuracy"])

ax1.plot(history_dict["epochs"], history_dict["train_acc"],  label="Train Accuracy",      color="#22c55e", linewidth=2)
ax1.plot(history_dict["epochs"], history_dict["val_acc"],    label="Val Accuracy",         color="#0ea5e9", linewidth=2, linestyle="--")
ax1.axvline(phase1_end, linestyle=":", color="gray", alpha=0.7, label=f"Fine-tune start (ep {phase1_end})")
ax1.set_title("Training vs Validation Accuracy", fontsize=13, fontweight="bold")
ax1.set_xlabel("Epoch")
ax1.set_ylabel("Accuracy")
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.set_ylim(0, 1)

ax2.plot(history_dict["epochs"], history_dict["train_loss"], label="Train Loss",   color="#f59e0b", linewidth=2)
ax2.plot(history_dict["epochs"], history_dict["val_loss"],   label="Val Loss",     color="#ef4444", linewidth=2, linestyle="--")
ax2.axvline(phase1_end, linestyle=":", color="gray", alpha=0.7)
ax2.set_title("Training vs Validation Loss", fontsize=13, fontweight="bold")
ax2.set_xlabel("Epoch")
ax2.set_ylabel("Loss")
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.suptitle(
    f"PlantGuard EfficientNetB0 – PlantVillage {NUM_CLASSES} classes\n"
    f"Final Val Accuracy: {val_acc:.4f}",
    fontsize=14
)
plt.tight_layout()
curves_path = str(OUTPUT_DIR / "training_curves.png")
plt.savefig(curves_path, dpi=150, bbox_inches="tight")
plt.close()
print(f"✓ Training curves saved to: {curves_path}")

# ── Final summary ─────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("TRAINING COMPLETE")
print("=" * 60)
print(f"Final validation accuracy : {val_acc:.4f} ({val_acc*100:.1f}%)")
print(f"Final model path          : {final_path}")
print(f"Classification report     : {report_path}")
print(f"Training history (JSON)   : {history_path}")
print(f"Confusion matrix (JSON)   : {cm_path}")
print(f"Training curves (PNG)     : {curves_path}")
print()
print("To start the backend with your trained model:")
print("  cd backend && uvicorn app.main:app --reload")
print("=" * 60)
