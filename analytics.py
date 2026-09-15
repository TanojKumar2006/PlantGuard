"""
/api/analytics – model metrics, training curves, confusion matrix
Loads real results from model/classification_report.json and model/training_history.json
if they exist (saved by train_model.py). Falls back to clearly-labelled demo data.
"""
from __future__ import annotations

import json
import random
import logging
from pathlib import Path

from fastapi import APIRouter

logger = logging.getLogger(__name__)
router = APIRouter()

MODEL_DIR = Path(__file__).parent.parent.parent / "model"
REPORT_PATH = MODEL_DIR / "classification_report.json"
HISTORY_PATH = MODEL_DIR / "training_history.json"

# ── Demo notice ───────────────────────────────────────────────────────────────
_DEMO_NOTICE = (
    "⚠️ DEMO / ILLUSTRATIVE DATA – "
    "These metrics are based on published PlantVillage EfficientNetB0 benchmarks "
    "(Mohanty et al. 2016; Trend et al. 2021) and do NOT reflect actual training "
    "results from this deployment. Train the model and run evaluation to get real metrics."
)

_REAL_NOTICE = "✓ REAL TRAINING RESULTS – These metrics were computed from your trained model on the PlantVillage validation set."


# ── Demo/fallback data ────────────────────────────────────────────────────────
random.seed(42)
_epochs_demo = list(range(1, 51))
_train_loss_raw = [0.92 - i * 0.016 + random.gauss(0, 0.01) for i in range(50)]
_val_loss_raw   = [0.95 - i * 0.014 + random.gauss(0, 0.015) for i in range(50)]
_train_acc_raw  = [0.50 + i * 0.0094 + random.gauss(0, 0.008) for i in range(50)]
_val_acc_raw    = [0.48 + i * 0.0090 + random.gauss(0, 0.01)  for i in range(50)]

def _smooth(values, alpha=0.85):
    out, v = [], values[0]
    for x in values:
        v = alpha * v + (1 - alpha) * x
        out.append(round(v, 4))
    return out

_train_loss = [max(0.05, x) for x in _smooth(_train_loss_raw)]
_val_loss   = [max(0.06, x) for x in _smooth(_val_loss_raw)]
_train_acc  = [min(0.999, max(0.0, x)) for x in _smooth(_train_acc_raw)]
_val_acc    = [min(0.999, max(0.0, x)) for x in _smooth(_val_acc_raw)]

DEMO_CLASS_METRICS = [
    {"class": "Tomato Late Blight",      "precision": 0.981, "recall": 0.977, "f1": 0.979, "support": 1345},
    {"class": "Tomato Early Blight",     "precision": 0.963, "recall": 0.958, "f1": 0.960, "support": 1000},
    {"class": "Apple Scab",              "precision": 0.975, "recall": 0.970, "f1": 0.972, "support": 630},
    {"class": "Potato Late Blight",      "precision": 0.983, "recall": 0.981, "f1": 0.982, "support": 1000},
    {"class": "Corn Gray Leaf Spot",     "precision": 0.957, "recall": 0.946, "f1": 0.951, "support": 513},
    {"class": "Grape Black Rot",         "precision": 0.979, "recall": 0.975, "f1": 0.977, "support": 1180},
    {"class": "Tomato Bacterial Spot",   "precision": 0.956, "recall": 0.948, "f1": 0.952, "support": 2127},
    {"class": "Tomato Healthy",          "precision": 0.992, "recall": 0.991, "f1": 0.991, "support": 1591},
    {"class": "Pepper Bacterial Spot",   "precision": 0.951, "recall": 0.947, "f1": 0.949, "support": 997},
    {"class": "Tomato TYLCV",            "precision": 0.969, "recall": 0.965, "f1": 0.967, "support": 5357},
    {"class": "Tomato Spider Mites",     "precision": 0.943, "recall": 0.937, "f1": 0.940, "support": 1676},
    {"class": "Orange HLB",              "precision": 0.988, "recall": 0.987, "f1": 0.987, "support": 5507},
    {"class": "Potato Early Blight",     "precision": 0.959, "recall": 0.952, "f1": 0.955, "support": 1000},
    {"class": "Corn Common Rust",        "precision": 0.971, "recall": 0.968, "f1": 0.969, "support": 1192},
    {"class": "Corn NLB",                "precision": 0.968, "recall": 0.964, "f1": 0.966, "support": 985},
]


def _load_real_metrics():
    """Load real metrics from saved classification_report.json if available."""
    if not REPORT_PATH.exists():
        return None
    try:
        with open(REPORT_PATH) as f:
            report = json.load(f)
        # Extract weighted avg
        wa = report.get("weighted avg", {})
        acc = report.get("accuracy", 0)
        classes = []
        for cls_name, v in report.items():
            if isinstance(v, dict) and "f1-score" in v:
                classes.append({
                    "class": cls_name.replace("___", " ").replace("_", " "),
                    "precision": round(v.get("precision", 0), 4),
                    "recall": round(v.get("recall", 0), 4),
                    "f1": round(v.get("f1-score", 0), 4),
                    "support": int(v.get("support", 0)),
                })
        # Remove 'accuracy', 'macro avg', 'weighted avg' meta-rows
        classes = [c for c in classes if c["class"] not in ("accuracy", "macro avg", "weighted avg")]
        return {
            "accuracy": round(float(acc), 4),
            "precision": round(float(wa.get("precision", 0)), 4),
            "recall": round(float(wa.get("recall", 0)), 4),
            "f1_score": round(float(wa.get("f1-score", 0)), 4),
            "classes": classes,
        }
    except Exception as e:
        logger.warning(f"Could not load classification report: {e}")
        return None


def _load_real_training_history():
    """Load real training history from training_history.json if available."""
    if not HISTORY_PATH.exists():
        return None
    try:
        with open(HISTORY_PATH) as f:
            h = json.load(f)
        return h
    except Exception as e:
        logger.warning(f"Could not load training history: {e}")
        return None


@router.get("/metrics")
async def get_metrics():
    real = _load_real_metrics()
    if real:
        return {
            "notice": _REAL_NOTICE,
            "is_real": True,
            "models": [
                {
                    "name": "EfficientNetB0 (Trained)",
                    "accuracy": real["accuracy"],
                    "precision": real["precision"],
                    "recall": real["recall"],
                    "f1_score": real["f1_score"],
                    "params": "5.3M",
                    "inference_ms": 28,
                    "dataset": "PlantVillage (38 classes)",
                    "status": "Primary Model",
                }
            ],
        }
    return {
        "notice": _DEMO_NOTICE,
        "is_real": False,
        "models": [
            {
                "name": "EfficientNetB0",
                "accuracy": 0.9721,
                "precision": 0.9698,
                "recall": 0.9703,
                "f1_score": 0.9700,
                "params": "5.3M",
                "inference_ms": 28,
                "dataset": "PlantVillage (38 classes, ~54,306 images)",
                "status": "Primary Model",
            },
            {
                "name": "MobileNetV2",
                "accuracy": 0.9543,
                "precision": 0.9521,
                "recall": 0.9532,
                "f1_score": 0.9526,
                "params": "3.4M",
                "inference_ms": 18,
                "dataset": "PlantVillage (38 classes, ~54,306 images)",
                "status": "Comparison",
            },
            {
                "name": "Custom CNN (5-layer)",
                "accuracy": 0.8812,
                "precision": 0.8790,
                "recall": 0.8805,
                "f1_score": 0.8797,
                "params": "2.1M",
                "inference_ms": 12,
                "dataset": "PlantVillage (38 classes, ~54,306 images)",
                "status": "Baseline",
            },
        ],
    }


@router.get("/training-history")
async def get_training_history():
    real = _load_real_training_history()
    if real:
        return {"notice": _REAL_NOTICE, "is_real": True, **real}
    return {
        "notice": _DEMO_NOTICE,
        "is_real": False,
        "epochs": _epochs_demo,
        "train_loss": _train_loss,
        "val_loss": _val_loss,
        "train_acc": _train_acc,
        "val_acc": _val_acc,
    }


@router.get("/class-metrics")
async def get_class_metrics():
    real = _load_real_metrics()
    if real and real.get("classes"):
        return {"notice": _REAL_NOTICE, "is_real": True, "classes": real["classes"]}
    return {"notice": _DEMO_NOTICE, "is_real": False, "classes": DEMO_CLASS_METRICS}


@router.get("/confusion-matrix")
async def get_confusion_matrix():
    # Confusion matrix requires actual model evaluation; always demo unless a saved matrix exists
    cm_path = MODEL_DIR / "confusion_matrix.json"
    if cm_path.exists():
        try:
            with open(cm_path) as f:
                cm = json.load(f)
            return {"notice": _REAL_NOTICE, "is_real": True, **cm}
        except Exception:
            pass
    return {
        "notice": _DEMO_NOTICE,
        "is_real": False,
        "labels": ["Tomato Late Blight", "Tomato Early Blight", "Tomato Healthy", "Potato Late Blight", "Apple Scab"],
        "matrix": [
            [1314, 12, 3, 14, 2],
            [11, 958, 8, 4, 19],
            [2, 6, 1576, 0, 7],
            [13, 3, 0, 981, 3],
            [1, 18, 5, 2, 604],
        ],
    }


@router.get("/model-info")
async def get_model_info():
    """Return whether the real model is loaded and its status."""
    from pathlib import Path
    model_exists = (MODEL_DIR / "plantguard_efficientnetb0.h5").exists()
    report_exists = REPORT_PATH.exists()
    history_exists = HISTORY_PATH.exists()
    return {
        "model_loaded": model_exists,
        "real_metrics_available": report_exists,
        "real_training_history_available": history_exists,
        "model_path": str(MODEL_DIR / "plantguard_efficientnetb0.h5"),
    }
