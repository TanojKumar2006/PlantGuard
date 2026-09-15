"""
PlantGuard AI – Model Service
EfficientNetB0 Transfer Learning with TensorFlow/Keras
Real Grad-CAM (Selvaraju et al., 2017) – original + heatmap + overlay
Demo Mode when model weights not available (clearly labelled)
"""
from __future__ import annotations

import os
import json
import random
import io
import base64
import logging
from pathlib import Path
from typing import Optional

import numpy as np
from PIL import Image

logger = logging.getLogger(__name__)

# ── Constants ────────────────────────────────────────────────────────────────
IMG_SIZE = (224, 224)
MODEL_PATH = Path(__file__).parent.parent.parent / "model" / "plantguard_efficientnetb0.h5"
CLASS_NAMES_PATH = Path(__file__).parent.parent.parent / "model" / "class_names.json"
DEMO_MODE = not MODEL_PATH.exists()

if DEMO_MODE:
    logger.warning(
        "⚠️  MODEL NOT FOUND – PlantGuard is running in DEMO MODE with simulated predictions. "
        "Train the model with: python train_model.py --data_dir ./data/PlantVillage"
    )

# ── Load model (lazy) ────────────────────────────────────────────────────────
_model = None
_gradcam_model = None


def _load_model():
    global _model, _gradcam_model
    if _model is not None:
        return
    try:
        import tensorflow as tf
        _model = tf.keras.models.load_model(str(MODEL_PATH), compile=False)

        # Find last convolutional layer for Grad-CAM
        last_conv_layer = None
        for layer in reversed(_model.layers):
            # EfficientNetB0's last conv is in the sub-model; search recursively
            if hasattr(layer, 'layers'):
                for sub in reversed(layer.layers):
                    if 'conv' in sub.name.lower() or 'swish' in sub.name.lower():
                        last_conv_layer = sub.name
                        break
                if last_conv_layer:
                    break
            if 'conv' in layer.name.lower():
                last_conv_layer = layer.name
                break

        if last_conv_layer:
            try:
                _gradcam_model = tf.keras.Model(
                    inputs=_model.inputs,
                    outputs=[_model.get_layer(last_conv_layer).output, _model.output],
                )
                logger.info(f"Grad-CAM model built using layer: {last_conv_layer}")
            except Exception as eg:
                logger.warning(f"Could not build Grad-CAM model: {eg}")

        logger.info(f"✓ Model loaded from {MODEL_PATH} — {_model.count_params():,} params")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        raise


# ── Load class names ─────────────────────────────────────────────────────────
def _get_class_labels():
    """Load class labels from saved JSON or fall back to built-in list."""
    if CLASS_NAMES_PATH.exists():
        with open(CLASS_NAMES_PATH) as f:
            return json.load(f)
    from app.services.disease_kb import CLASS_LABELS
    return CLASS_LABELS


# ── Image preprocessing (EfficientNetB0 standard) ────────────────────────────
def preprocess_image(img: Image.Image) -> np.ndarray:
    """
    Preprocess image for EfficientNetB0:
    - Convert to RGB
    - Resize to 224×224
    - Apply EfficientNet preprocessing (rescale to [-1, 1])
    """
    img_rgb = img.convert("RGB").resize(IMG_SIZE, Image.BILINEAR)
    arr = np.array(img_rgb, dtype=np.float32)
    # EfficientNetB0 uses [-1, 1] normalisation via preprocess_input
    try:
        from tensorflow.keras.applications.efficientnet import preprocess_input
        arr = preprocess_input(arr)
    except ImportError:
        # Fallback: manual rescaling equivalent to preprocess_input
        arr = (arr / 127.5) - 1.0
    return np.expand_dims(arr, axis=0)


# ── Grad-CAM (Selvaraju et al., 2017) ────────────────────────────────────────
def _compute_gradcam_heatmap(img_array: np.ndarray, class_idx: int) -> Optional[np.ndarray]:
    """
    Compute real Grad-CAM heatmap.
    Returns uint8 array (0-255) at 224×224 or None if unavailable.
    """
    try:
        import tensorflow as tf
        with tf.GradientTape() as tape:
            conv_out, preds = _gradcam_model(img_array, training=False)
            tape.watch(conv_out)
            loss = preds[:, class_idx]
        grads = tape.gradient(loss, conv_out)
        if grads is None:
            return None
        # Pool gradients over spatial dimensions
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        cam = conv_out.numpy()[0]
        pooled = pooled_grads.numpy()
        # Weighted sum of feature maps
        for i in range(cam.shape[-1]):
            cam[:, :, i] *= pooled[i]
        heatmap = np.mean(cam, axis=-1)
        heatmap = np.maximum(heatmap, 0)
        if heatmap.max() > 0:
            heatmap /= heatmap.max()
        # Resize to input size
        hm_img = Image.fromarray((heatmap * 255).astype(np.uint8)).resize(IMG_SIZE, Image.BILINEAR)
        return np.array(hm_img)
    except Exception as e:
        logger.warning(f"Grad-CAM computation failed: {e}")
        return None


def _encode_image(img_arr: np.ndarray) -> str:
    """Encode uint8 RGB numpy array as base64 PNG data URI."""
    buf = io.BytesIO()
    Image.fromarray(img_arr.astype(np.uint8)).save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def _build_gradcam_images(original_img: Image.Image, heatmap: np.ndarray) -> dict:
    """
    Build three Grad-CAM image variants:
    - original: resized original leaf (base64)
    - heatmap: coloured heatmap only (base64)
    - overlay: heatmap blended on original (base64)
    """
    import cv2
    img_rgb = np.array(original_img.convert("RGB").resize(IMG_SIZE))
    # Colour heatmap with JET colormap
    hm_colored = cv2.applyColorMap(heatmap.astype(np.uint8), cv2.COLORMAP_JET)
    hm_colored = cv2.cvtColor(hm_colored, cv2.COLOR_BGR2RGB)
    # Overlay blend
    overlay = cv2.addWeighted(img_rgb, 0.55, hm_colored, 0.45, 0)

    return {
        "gradcam_original_b64": _encode_image(img_rgb),
        "gradcam_heatmap_b64": _encode_image(hm_colored),
        "gradcam_overlay_b64": _encode_image(overlay),
    }


# ── Demo Grad-CAM ─────────────────────────────────────────────────────────────
def _demo_gradcam(original_img: Image.Image) -> dict:
    """Generate synthetic Grad-CAM for demo mode (clearly labelled)."""
    import cv2
    w, h = IMG_SIZE
    img_rgb = np.array(original_img.convert("RGB").resize(IMG_SIZE))
    x, y = np.meshgrid(np.linspace(-1, 1, w), np.linspace(-1, 1, h))
    cx = random.uniform(-0.4, 0.4)
    cy = random.uniform(-0.3, 0.3)
    sigma = random.uniform(0.25, 0.55)
    heatmap = np.exp(-((x - cx)**2 + (y - cy)**2) / sigma).astype(np.float32)
    heatmap = (heatmap * 255).astype(np.uint8)
    hm_colored = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    hm_colored = cv2.cvtColor(hm_colored, cv2.COLOR_BGR2RGB)
    overlay = cv2.addWeighted(img_rgb, 0.55, hm_colored, 0.45, 0)
    return {
        "gradcam_original_b64": _encode_image(img_rgb),
        "gradcam_heatmap_b64": _encode_image(hm_colored),
        "gradcam_overlay_b64": _encode_image(overlay),
    }


# ── Demo predictions ──────────────────────────────────────────────────────────
from app.services.disease_kb import CLASS_LABELS, parse_class_label

DEMO_PREDICTIONS = [
    ("Tomato___Late_blight", 0.91, "Severe"),
    ("Potato___Early_blight", 0.87, "Moderate"),
    ("Apple___Apple_scab", 0.83, "Moderate"),
    ("Tomato___Bacterial_spot", 0.79, "Mild"),
    ("Corn_(maize)___Northern_Leaf_Blight", 0.76, "Moderate"),
    ("Grape___Black_rot", 0.88, "Severe"),
    ("Tomato___Septoria_leaf_spot", 0.82, "Mild"),
    ("Tomato___Early_blight", 0.85, "Moderate"),
    ("Orange___Haunglongbing_(Citrus_greening)", 0.78, "Severe"),
    ("Tomato___Spider_mites Two-spotted_spider_mite", 0.81, "Mild"),
    ("Pepper,_bell___Bacterial_spot", 0.74, "Mild"),
    ("Tomato___healthy", 0.96, "None"),
    ("Apple___healthy", 0.94, "None"),
    ("Potato___Late_blight", 0.93, "Severe"),
    ("Corn_(maize)___Common_rust_", 0.80, "Moderate"),
]


def _generate_demo_top3(primary_label: str, primary_conf: float) -> list[dict]:
    candidates = [l for l in CLASS_LABELS if l != primary_label]
    random.shuffle(candidates)
    p2 = parse_class_label(candidates[0])
    p3 = parse_class_label(candidates[1])
    second_conf = round(primary_conf * random.uniform(0.35, 0.60), 4)
    third_conf = round(primary_conf * random.uniform(0.05, 0.28), 4)
    top3 = [
        {"label": primary_label, "confidence": round(primary_conf, 4),
         "plant_name": parse_class_label(primary_label)[0], "disease_name": parse_class_label(primary_label)[1]},
        {"label": candidates[0], "confidence": second_conf,
         "plant_name": p2[0], "disease_name": p2[1]},
        {"label": candidates[1], "confidence": third_conf,
         "plant_name": p3[0], "disease_name": p3[1]},
    ]
    total = sum(t["confidence"] for t in top3)
    if total > 1.0:
        factor = 1.0 / total
        for t in top3:
            t["confidence"] = round(t["confidence"] * factor, 4)
    return top3


def _estimate_severity(confidence: float, label: str) -> str:
    _, disease = parse_class_label(label)
    if disease.lower() == "healthy":
        return "None"
    if confidence >= 0.90:
        return "Severe"
    elif confidence >= 0.70:
        return "Moderate"
    elif confidence >= 0.50:
        return "Mild"
    else:
        return "Uncertain"


# ── Main inference function ───────────────────────────────────────────────────
def run_inference(img: Image.Image, use_demo: bool = False) -> dict:
    """
    Run inference on a PIL image.

    Returns dict with:
        is_demo, plant_name, disease_name, class_label, confidence, severity,
        low_confidence_warning, top3, model_used,
        gradcam_original_b64, gradcam_heatmap_b64, gradcam_overlay_b64
    """
    if DEMO_MODE or use_demo:
        img_bytes = img.convert("RGB").tobytes()
        idx = hash(img_bytes[:200]) % len(DEMO_PREDICTIONS)
        label, conf, severity = DEMO_PREDICTIONS[idx]
        plant, disease = parse_class_label(label)
        top3 = _generate_demo_top3(label, conf)
        gradcam = _demo_gradcam(img)
        return {
            "is_demo": True,
            "plant_name": plant,
            "disease_name": disease,
            "class_label": label,
            "confidence": conf,
            "severity": severity,
            "low_confidence_warning": conf < 0.60,
            "top3": top3,
            "model_used": "⚠️ Demo Mode – EfficientNetB0 architecture, model weights not trained yet",
            **gradcam,
        }

    # ── Real model inference ──────────────────────────────────────────────────
    _load_model()
    class_labels = _get_class_labels()

    arr = preprocess_image(img)

    import tensorflow as tf
    preds = _model.predict(arr, verbose=0)[0]

    top_idx = int(np.argmax(preds))
    confidence = float(preds[top_idx])

    # Guard against index mismatch between saved model and CLASS_LABELS
    if top_idx >= len(class_labels):
        logger.error(f"Model output index {top_idx} exceeds class list length {len(class_labels)}")
        raise ValueError("Class index mismatch – retrain model or regenerate class_names.json")

    label = class_labels[top_idx]
    plant, disease = parse_class_label(label)

    # Top-3 with plant/disease names
    top3_idx = np.argsort(preds)[::-1][:3]
    top3 = []
    for i in top3_idx:
        if i < len(class_labels):
            l = class_labels[i]
            p, d = parse_class_label(l)
            top3.append({"label": l, "confidence": float(preds[i]), "plant_name": p, "disease_name": d})

    severity = _estimate_severity(confidence, label)

    # Real Grad-CAM
    gradcam_images = {"gradcam_original_b64": "", "gradcam_heatmap_b64": "", "gradcam_overlay_b64": ""}
    if _gradcam_model is not None:
        heatmap = _compute_gradcam_heatmap(arr, top_idx)
        if heatmap is not None:
            gradcam_images = _build_gradcam_images(img, heatmap)

    return {
        "is_demo": False,
        "plant_name": plant,
        "disease_name": disease,
        "class_label": label,
        "confidence": confidence,
        "severity": severity,
        "low_confidence_warning": confidence < 0.60,
        "top3": top3,
        "model_used": "EfficientNetB0 (TensorFlow/Keras) – trained on PlantVillage",
        **gradcam_images,
    }
