// Core application types

export interface Top3Item {
  label: string;
  confidence: number;
  plant_name?: string;
  disease_name?: string;
}

export interface AnalysisResult {
  id: number;
  is_demo: boolean;
  plant_name: string;
  disease_name: string;
  class_label: string;
  confidence: number;
  severity: 'None' | 'Mild' | 'Moderate' | 'Severe' | 'Uncertain';
  low_confidence_warning: boolean;
  top3: Top3Item[];
  // Grad-CAM: three variants
  gradcam_original_b64: string;
  gradcam_heatmap_b64: string;
  gradcam_overlay_b64: string;
  model_used: string;
  disease_info: DiseaseInfo;
  treatments: Treatment[];
  products: Product[];
  image_url: string;
}

export interface DiseaseInfo {
  common_name: string;
  scientific_name: string;
  type: string;
  summary: string;
  symptoms: string[];
  cause: string;
  effects: string;
  severity_factors: string[];
  prevention: string[];
  immediate_actions: string[];
  cultural_biological: string[];
  references: string[];
}

export interface Treatment {
  active_ingredient: string;
  product_example: string;
  use_for: string;
  rate: string;
  preparation: string;
  when_to_apply: string;
  frequency: string;
  phi: string;
  safety: string[];
  source: string;
}

export interface Product {
  product_name: string;
  active_ingredient: string;
  manufacturer: string;
  type: string;
  availability: string;
  buy_link_note: string;
}

export interface HistoryItem {
  id: number;
  created_at: string;
  image_path: string;
  plant_name: string;
  disease_name: string;
  class_label: string;
  confidence: number;
  severity: string;
  top3: Top3Item[];
  is_demo: boolean;
  model_used: string;
}

export interface HistoryRecord extends HistoryItem {
  disease_info?: DiseaseInfo;
  treatments?: Treatment[];
  products?: Product[];
}

export interface ModelMetrics {
  notice: string;
  is_real?: boolean;
  models: ModelEntry[];
}

export interface ModelEntry {
  name: string;
  accuracy: number;
  precision: number;
  recall: number;
  f1_score: number;
  params: string;
  inference_ms: number;
  dataset: string;
  status: string;
}

export interface TrainingHistory {
  notice: string;
  is_real?: boolean;
  epochs: number[];
  train_loss: number[];
  val_loss: number[];
  train_acc: number[];
  val_acc: number[];
  phase1_end_epoch?: number;
}

export interface ClassMetrics {
  notice: string;
  is_real?: boolean;
  classes: ClassEntry[];
}

export interface ClassEntry {
  class: string;
  precision: number;
  recall: number;
  f1: number;
  support: number;
}

export interface ConfusionMatrix {
  notice: string;
  is_real?: boolean;
  labels: string[];
  matrix: number[][];
}

export interface PlantEntry {
  name: string;
  diseases: DiseaseEntry[];
  healthy_class: string | null;
}

export interface DiseaseEntry {
  class_label: string;
  disease_name: string;
  common_name: string;
  type: string;
  summary: string;
}

export interface HistoryStats {
  count: number;
  healthy: number;
  diseased: number;
  most_common_disease: string | null;
}

export interface ModelInfo {
  model_loaded: boolean;
  real_metrics_available: boolean;
  real_training_history_available: boolean;
  model_path: string;
}
