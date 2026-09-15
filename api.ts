import axios from 'axios';
import type {
  AnalysisResult,
  HistoryItem,
  HistoryRecord,
  HistoryStats,
  ModelMetrics,
  TrainingHistory,
  ClassMetrics,
  ConfusionMatrix,
  PlantEntry,
  ModelInfo,
} from '../types';

const api = axios.create({
  baseURL: '/api',
  timeout: 90000, // 90s for model inference on first load
});

// ── Analyze ───────────────────────────────────────────────────────────────────
export const analyzeImage = async (file: File): Promise<AnalysisResult> => {
  const form = new FormData();
  form.append('file', file);
  const res = await api.post<AnalysisResult>('/analyze/', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return res.data;
};

// ── History ───────────────────────────────────────────────────────────────────
export const getHistory = async (params?: {
  skip?: number;
  limit?: number;
  plant?: string;
  disease?: string;
}): Promise<HistoryItem[]> => {
  const res = await api.get<HistoryItem[]>('/history/', { params });
  return res.data;
};

export const getHistoryStats = async (): Promise<HistoryStats> => {
  const res = await api.get<HistoryStats>('/history/count');
  return res.data;
};

export const getHistoryRecord = async (id: number): Promise<HistoryRecord> => {
  const res = await api.get<HistoryRecord>(`/history/${id}`);
  return res.data;
};

export const deleteHistoryItem = async (id: number): Promise<void> => {
  await api.delete(`/history/${id}`);
};

export const clearHistory = async (): Promise<void> => {
  await api.delete('/history/');
};

// ── Analytics ─────────────────────────────────────────────────────────────────
export const getModelMetrics = async (): Promise<ModelMetrics> => {
  const res = await api.get<ModelMetrics>('/analytics/metrics');
  return res.data;
};

export const getTrainingHistory = async (): Promise<TrainingHistory> => {
  const res = await api.get<TrainingHistory>('/analytics/training-history');
  return res.data;
};

export const getClassMetrics = async (): Promise<ClassMetrics> => {
  const res = await api.get<ClassMetrics>('/analytics/class-metrics');
  return res.data;
};

export const getConfusionMatrix = async (): Promise<ConfusionMatrix> => {
  const res = await api.get<ConfusionMatrix>('/analytics/confusion-matrix');
  return res.data;
};

export const getModelInfo = async (): Promise<ModelInfo> => {
  const res = await api.get<ModelInfo>('/analytics/model-info');
  return res.data;
};

// ── Library ───────────────────────────────────────────────────────────────────
export const getPlantLibrary = async (q?: string): Promise<PlantEntry[]> => {
  const res = await api.get<PlantEntry[]>('/library/', { params: q ? { q } : {} });
  return res.data;
};

export const getDiseaseDetail = async (classLabel: string) => {
  const res = await api.get(`/library/disease/${encodeURIComponent(classLabel)}`);
  return res.data;
};

// ── Treatment ─────────────────────────────────────────────────────────────────
export const getTreatmentGuide = async (classLabel: string) => {
  const res = await api.get(`/treatment/${encodeURIComponent(classLabel)}`);
  return res.data;
};

export const getTreatmentList = async () => {
  const res = await api.get('/treatment/');
  return res.data;
};

export default api;
