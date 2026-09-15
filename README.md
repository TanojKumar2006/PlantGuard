# 🌱 PlantGuard AI — Plant Disease Detection & Treatment Assistant

An end-to-end AI application for plant disease diagnosis using EfficientNetB0 transfer learning, real Grad-CAM visualisation, and verified treatment guidance.

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [System Requirements](#system-requirements)
3. [Quick Start](#quick-start)
4. [Dataset Setup](#dataset-setup)
5. [Training the Model](#training-the-model)
6. [Running the Backend](#running-the-backend)
7. [Running the Frontend](#running-the-frontend)
8. [Testing with Real Images](#testing-with-real-images)
9. [Evaluation Results](#evaluation-results)
10. [Architecture](#architecture)
11. [API Reference](#api-reference)
12. [Remaining Limitations](#remaining-limitations)

---

## 🔬 Project Overview

PlantGuard AI covers:
- **38 disease classes** across 10 crops (PlantVillage dataset)
- **EfficientNetB0** transfer learning with two-phase training
- **Real Grad-CAM** (original + heatmap + overlay)
- **Top-3 predictions** with confidence scores
- **Severity estimation** per detection
- **Complete disease knowledge base** with symptoms, cause, effects, prevention
- **Verified treatment & pesticide guide** from university extension services
- **Demo Mode** when model weights not present (clearly labelled)
- **Dashboard, History, Analytics, Plant Library, Treatment Guide**

---

## 💻 System Requirements

| Component | Minimum | Recommended |
|---|---|---|
| Python | 3.10+ | 3.11+ |
| Node.js | 18+ | 20+ |
| RAM | 8 GB | 16 GB |
| Disk | 10 GB | 20 GB |
| GPU | None (CPU only) | NVIDIA GPU for faster training |

---

## 🚀 Quick Start

### 1. Clone / navigate to the project

```bash
cd plantguard
```

### 2. Backend setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install base dependencies
pip install -r requirements.txt

# Install TensorFlow (required for real AI inference)
pip install tensorflow
# For GPU support:
pip install tensorflow[and-cuda]

# Install training utilities (only needed for train_model.py)
pip install matplotlib scikit-learn
```

### 3. Frontend setup

```bash
cd frontend
npm install
```

---

## 📦 Dataset Setup

### Download PlantVillage

**Option A: Kaggle** (recommended)
```bash
# Install kaggle CLI
pip install kaggle

# Set up API key: https://www.kaggle.com/settings → API → New Token
# Place kaggle.json in ~/.kaggle/

# Download dataset
kaggle datasets download -d emmarex/plantdisease
unzip plantdisease.zip -d ./data/PlantVillage
```

**Option B: Mendeley Data**
- URL: https://data.mendeley.com/datasets/tywbtsjrjv/1
- Download and extract to `backend/data/PlantVillage/`

### Expected directory structure

```
backend/data/PlantVillage/
├── Apple___Apple_scab/          (630 images)
├── Apple___Black_rot/           (621 images)
├── Apple___Cedar_apple_rust/    (275 images)
├── Apple___healthy/             (1645 images)
├── Blueberry___healthy/         (1502 images)
├── Cherry___Powdery_mildew/     (1052 images)
... (38 class folders total)
```

**Dataset location:** `backend/data/PlantVillage/`  
**Total images:** ~54,306  
**Classes:** 38 (26 diseases + 12 healthy across 10 crops)

---

## 🧠 Training the Model

### Command

```bash
cd backend

# Standard training (50 epochs, batch 32, GPU if available)
python train_model.py --data_dir ./data/PlantVillage --epochs 50 --batch 32

# Fast test run (fewer epochs)
python train_model.py --data_dir ./data/PlantVillage --epochs 10 --batch 32

# Custom settings
python train_model.py \
  --data_dir ./data/PlantVillage \
  --epochs 50 \
  --batch 32 \
  --lr 1e-4 \
  --fine_tune_from 100 \
  --img_size 224 \
  --output_dir ./model
```

### Training process

1. **Phase 1** (epochs 1–25): EfficientNetB0 base frozen, only classifier head trained
2. **Phase 2** (epochs 26–50): Fine-tuning from layer 100 onwards with LR/10

### Outputs (saved to `backend/model/`)

| File | Description |
|---|---|
| `plantguard_efficientnetb0.h5` | **Final trained model** |
| `plantguard_efficientnetb0_best.h5` | Best checkpoint (highest val accuracy) |
| `class_names.json` | Class index → label mapping used for inference |
| `classification_report.json` | Per-class precision, recall, F1, support |
| `training_history.json` | Epoch-by-epoch accuracy and loss |
| `confusion_matrix.json` | Top-10 class confusion matrix |
| `training_curves.png` | Accuracy/loss plot |

---

## ⚙️ Running the Backend

```bash
cd backend

# Activate virtual environment first
venv\Scripts\activate   # Windows
source venv/bin/activate # Linux/Mac

# Start FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: http://localhost:8000  
Interactive API docs: http://localhost:8000/docs

**Environment variables (optional, create `backend/.env`):**
```
DATABASE_URL=sqlite+aiosqlite:///./plantguard.db
```

---

## 🖥️ Running the Frontend

```bash
cd frontend

# Development server (with hot reload)
npm run dev

# Production build
npm run build
npm run preview
```

Frontend will be available at: http://localhost:5173

The Vite dev server automatically proxies `/api` and `/uploads` to the backend at port 8000.

---

## 🧪 Testing with Real-World Images

### Via the Web UI

1. Start backend: `uvicorn app.main:app --reload`
2. Start frontend: `npm run dev`
3. Go to http://localhost:5173/diagnose
4. Upload any of:
   - PlantVillage test images (from `backend/data/PlantVillage/`)
   - Real-world photos taken with a phone
   - Online leaf images (save and upload)

### Via the API directly

```bash
# Test with curl
curl -X POST http://localhost:8000/api/analyze/ \
  -F "file=@path/to/leaf.jpg" \
  | python -m json.tool

# Test with Python
python -c "
import requests
with open('leaf.jpg', 'rb') as f:
    r = requests.post('http://localhost:8000/api/analyze/', files={'file': f})
    d = r.json()
    print(f'Plant: {d[\"plant_name\"]}')
    print(f'Disease: {d[\"disease_name\"]}')
    print(f'Confidence: {d[\"confidence\"]*100:.1f}%')
    print(f'Severity: {d[\"severity\"]}')
    print(f'Demo: {d[\"is_demo\"]}')
"
```

### Test cases to verify

| Test | Expected |
|---|---|
| PlantVillage dataset image | High confidence (>85%) |
| Real-world phone photo | Varies; may have lower confidence |
| Healthy leaf | disease_name = "Healthy", severity = "None" |
| Non-leaf image | Low confidence + warning |
| Blurry/dark image | Low confidence warning |
| Invalid file (text file) | 400 error |
| File > 20 MB | 400 error |

---

## 📊 Evaluation Results

After training (`python train_model.py`), actual results are saved to:

| Metric | Published Benchmark\* | Your Results |
|---|---|---|
| Accuracy | ~97.2% | See `model/classification_report.json` |
| Precision | ~96.9% | See `model/classification_report.json` |
| Recall | ~97.0% | See `model/classification_report.json` |
| F1-Score | ~97.0% | See `model/classification_report.json` |

\* Based on Mohanty et al. (2016) and subsequent EfficientNet papers on PlantVillage.

The Analytics page at `/analytics` automatically displays real metrics if `classification_report.json` is present, clearly labelled as real vs illustrative data.

---

## 🏗️ Architecture

```
Real Image
    │
    ▼
Preprocessing (224×224 RGB, EfficientNet [-1,1] normalisation)
    │
    ▼
EfficientNetB0 (ImageNet pretrained, fine-tuned on PlantVillage)
    │
    ▼
GlobalAveragePooling2D → BatchNorm → Dense(256, ReLU) → Dropout(0.3)
    │
    ▼
Dense(38, Softmax)
    │
    ├── Top-3 predictions + confidence scores
    ├── Severity estimate
    ├── Real Grad-CAM (original + heatmap + overlay)
    │
    ▼
FastAPI Response → Disease KB → Treatment DB → SQLite History
    │
    ▼
React Frontend (Results Page)
```

### Tech Stack

| Layer | Technology |
|---|---|
| AI Model | EfficientNetB0, TensorFlow 2.x / Keras |
| Explainability | Grad-CAM (Selvaraju et al., 2017) |
| Dataset | PlantVillage (Hughes & Salathé, 2015) |
| Backend API | Python · FastAPI · SQLite (SQLAlchemy async) |
| Image Processing | Pillow · OpenCV |
| Frontend | React 18 · TypeScript · Tailwind CSS · Vite |
| Charts | Recharts |
| Animations | Framer Motion |

---

## 📡 API Reference

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/analyze/` | Upload image → full diagnosis |
| GET | `/api/history/` | List diagnosis history |
| GET | `/api/history/count` | Stats: total, healthy, diseased, most common |
| GET | `/api/history/{id}` | Single record with full disease info |
| DELETE | `/api/history/{id}` | Delete a record |
| DELETE | `/api/history/` | Clear all history |
| GET | `/api/analytics/metrics` | Model accuracy/F1 (real or demo) |
| GET | `/api/analytics/training-history` | Training curves |
| GET | `/api/analytics/class-metrics` | Per-class precision/recall/F1 |
| GET | `/api/analytics/confusion-matrix` | Confusion matrix |
| GET | `/api/analytics/model-info` | Model load status |
| GET | `/api/library/` | Plant library (38 classes) |
| GET | `/api/library/disease/{label}` | Full disease detail |
| GET | `/api/treatment/` | Treatment guide list |
| GET | `/api/treatment/{label}` | Treatment + products for a disease |
| GET | `/api/health` | Health check |
| GET | `/docs` | Swagger UI |

---

## ⚠️ Remaining Limitations

1. **Domain shift**: The model was trained on controlled laboratory images. Real-world photos (different lighting, angles, background, soil on leaves) may produce lower confidence.

2. **38 classes only**: PlantVillage covers 10 crops. Diseases of other plants (e.g., wheat, rice, banana) are not recognised.

3. **Single-disease assumption**: The model predicts one class per image. Multiple co-occurring diseases on one leaf may confuse the model.

4. **Image quality sensitivity**: Very blurry, dark, or poorly framed photos reduce accuracy significantly.

5. **Treatment information**: Pesticide guidance is for educational purposes only. Registration status, dosages, and pre-harvest intervals vary by country and year. Always consult the current product label and local agricultural authority.

6. **No cure for viral/bacterial diseases**: HLB, TYLCV, ToMV have no chemical cure. Management is preventive.

7. **CPU inference time**: On CPU, first inference may take 15–60 seconds while TensorFlow initialises. Subsequent inferences are faster (2–10 sec).

---

## 📚 References

1. Hughes, D.P., & Salathé, M. (2015). An open access repository of images on plant health to enable the development of mobile disease diagnostics. *arXiv:1511.08060*
2. Tan, M., & Le, Q.V. (2019). EfficientNet: Rethinking model scaling for convolutional neural networks. *ICML 2019*
3. Selvaraju, R.R., et al. (2017). Grad-CAM: Visual explanations from deep networks via gradient-based localization. *ICCV 2017*
4. Mohanty, S.P., et al. (2016). Using deep learning for image-based plant disease detection. *Frontiers in Plant Science*
