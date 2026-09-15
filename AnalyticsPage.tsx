import { useEffect, useState } from 'react';
import { BarChart3, AlertTriangle, TrendingUp, CheckCircle2 } from 'lucide-react';
import {
  getModelMetrics, getTrainingHistory, getClassMetrics, getConfusionMatrix, getModelInfo
} from '../utils/api';
import type { ModelMetrics, TrainingHistory, ClassMetrics, ConfusionMatrix, ModelInfo } from '../types';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  BarChart, Bar, ResponsiveContainer, Cell, ReferenceLine
} from 'recharts';
import ConfidenceBar from '../components/ConfidenceBar';

const COLORS = ['#22c55e', '#0ea5e9', '#8b5cf6', '#f59e0b', '#ef4444'];

export default function AnalyticsPage() {
  const [metrics, setMetrics] = useState<ModelMetrics | null>(null);
  const [training, setTraining] = useState<TrainingHistory | null>(null);
  const [classM, setClassM] = useState<ClassMetrics | null>(null);
  const [confusion, setConfusion] = useState<ConfusionMatrix | null>(null);
  const [modelInfo, setModelInfo] = useState<ModelInfo | null>(null);

  useEffect(() => {
    getModelMetrics().then(setMetrics);
    getTrainingHistory().then(setTraining);
    getClassMetrics().then(setClassM);
    getConfusionMatrix().then(setConfusion);
    getModelInfo().then(setModelInfo).catch(() => {});
  }, []);

  const isDark = document.documentElement.classList.contains('dark');
  const gridColor = isDark ? '#334155' : '#e5e7eb';
  const labelColor = isDark ? '#94a3b8' : '#6b7280';

  return (
    <div className="max-w-6xl mx-auto px-4 py-10">
      <div className="mb-8">
        <h1 className="text-3xl font-extrabold text-gray-900 dark:text-white mb-1 flex items-center gap-3">
          <BarChart3 className="w-7 h-7 text-ai-500" />
          Model Analytics
        </h1>
        <p className="text-gray-500 dark:text-gray-400">Training metrics, performance benchmarks, and class-wise analysis</p>
      </div>

      {/* Model status + notice */}
      {metrics?.notice && (
        <div className={`flex items-start gap-3 rounded-xl border p-4 text-sm mb-6 ${
          metrics.is_real
            ? 'border-green-200 dark:border-green-800 bg-green-50 dark:bg-green-900/10 text-green-800 dark:text-green-300'
            : 'border-amber-200 dark:border-amber-800 bg-amber-50 dark:bg-amber-900/20 text-amber-800 dark:text-amber-300'
        }`}>
          {metrics.is_real
            ? <CheckCircle2 className="w-4 h-4 mt-0.5 shrink-0" />
            : <AlertTriangle className="w-4 h-4 mt-0.5 shrink-0" />
          }
          <p>{metrics.notice}</p>
        </div>
      )}

      {/* Model comparison */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5 mb-8">
        {metrics?.models?.map((m, i) => (
          <div key={m.name} className={`card p-5 ${i === 0 ? 'ring-2 ring-brand-400 dark:ring-brand-600' : ''}`}>
            <div className="flex items-center justify-between mb-3">
              <h3 className="font-bold text-gray-900 dark:text-white">{m.name}</h3>
              <span className={`tag ${i === 0 ? 'bg-brand-100 text-brand-700 dark:bg-brand-900/40 dark:text-brand-400' : 'bg-gray-100 text-gray-600 dark:bg-slate-700 dark:text-gray-300'}`}>
                {m.status}
              </span>
            </div>
            <div className="text-3xl font-extrabold text-gradient mb-3">
              {(m.accuracy * 100).toFixed(1)}%
            </div>
            {[
              { label: 'Accuracy', value: m.accuracy },
              { label: 'Precision', value: m.precision },
              { label: 'Recall', value: m.recall },
              { label: 'F1-Score', value: m.f1_score },
            ].map(({ label, value }) => (
              <div key={label} className="mb-2">
                <div className="flex justify-between text-xs text-gray-500 mb-1">
                  <span>{label}</span>
                  <span className="font-medium">{(value * 100).toFixed(1)}%</span>
                </div>
                <ConfidenceBar confidence={value} />
              </div>
            ))}
            <div className="flex gap-4 mt-3 text-xs text-gray-400 border-t border-gray-100 dark:border-slate-700 pt-3">
              <span>Params: {m.params}</span>
              <span>~{m.inference_ms}ms</span>
            </div>
            <div className="text-xs text-gray-400 mt-1">{m.dataset}</div>
          </div>
        ))}
      </div>

      {/* Training curves */}
      {training && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Accuracy */}
          <div className="card p-5">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-bold text-gray-900 dark:text-white flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-brand-500" />
                Training vs Validation Accuracy
              </h3>
              {training.is_real && <span className="tag bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400 text-xs">Real data</span>}
            </div>
            <ResponsiveContainer width="100%" height={240}>
              <LineChart data={training.epochs.map((e, i) => ({
                epoch: e,
                Train: +(training.train_acc[i] * 100).toFixed(2),
                Val: +(training.val_acc[i] * 100).toFixed(2),
              }))}>
                <CartesianGrid stroke={gridColor} strokeDasharray="3 3" />
                <XAxis dataKey="epoch" tick={{ fill: labelColor, fontSize: 11 }} label={{ value: 'Epoch', position: 'insideBottom', offset: -2, fill: labelColor, fontSize: 11 }} />
                <YAxis tick={{ fill: labelColor, fontSize: 11 }} unit="%" domain={[0, 100]} />
                <Tooltip formatter={(v: any) => `${v}%`} contentStyle={{ background: isDark ? '#1e293b' : '#fff', border: `1px solid ${gridColor}`, borderRadius: 8 }} />
                <Legend />
                {training.phase1_end_epoch && (
                  <ReferenceLine x={training.phase1_end_epoch} stroke="#8b5cf6" strokeDasharray="4 4"
                    label={{ value: 'Fine-tune', fill: '#8b5cf6', fontSize: 10 }} />
                )}
                <Line type="monotone" dataKey="Train" stroke="#22c55e" strokeWidth={2} dot={false} />
                <Line type="monotone" dataKey="Val" stroke="#0ea5e9" strokeWidth={2} dot={false} strokeDasharray="5 5" />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Loss */}
          <div className="card p-5">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-bold text-gray-900 dark:text-white flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-red-400" />
                Training vs Validation Loss
              </h3>
              {training.is_real && <span className="tag bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400 text-xs">Real data</span>}
            </div>
            <ResponsiveContainer width="100%" height={240}>
              <LineChart data={training.epochs.map((e, i) => ({
                epoch: e,
                Train: +training.train_loss[i].toFixed(4),
                Val: +training.val_loss[i].toFixed(4),
              }))}>
                <CartesianGrid stroke={gridColor} strokeDasharray="3 3" />
                <XAxis dataKey="epoch" tick={{ fill: labelColor, fontSize: 11 }} />
                <YAxis tick={{ fill: labelColor, fontSize: 11 }} />
                <Tooltip contentStyle={{ background: isDark ? '#1e293b' : '#fff', border: `1px solid ${gridColor}`, borderRadius: 8 }} />
                <Legend />
                {training.phase1_end_epoch && (
                  <ReferenceLine x={training.phase1_end_epoch} stroke="#8b5cf6" strokeDasharray="4 4" />
                )}
                <Line type="monotone" dataKey="Train" stroke="#f59e0b" strokeWidth={2} dot={false} />
                <Line type="monotone" dataKey="Val" stroke="#ef4444" strokeWidth={2} dot={false} strokeDasharray="5 5" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      {/* Class-wise metrics */}
      {classM && (
        <div className="card p-5 mb-8">
          <h3 className="font-bold text-gray-900 dark:text-white mb-4">Class-wise F1-Score</h3>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={classM.classes.map(c => ({ name: c.class, F1: +(c.f1 * 100).toFixed(1) }))} layout="vertical">
              <CartesianGrid stroke={gridColor} strokeDasharray="3 3" horizontal={false} />
              <XAxis type="number" domain={[75, 100]} tick={{ fill: labelColor, fontSize: 10 }} unit="%" />
              <YAxis type="category" dataKey="name" width={160} tick={{ fill: labelColor, fontSize: 10 }} />
              <Tooltip formatter={(v: any) => `${v}%`} contentStyle={{ background: isDark ? '#1e293b' : '#fff', border: `1px solid ${gridColor}`, borderRadius: 8 }} />
              <Bar dataKey="F1" radius={[0, 4, 4, 0]}>
                {classM.classes.map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Confusion matrix */}
      {confusion && (
        <div className="card p-5">
          <h3 className="font-bold text-gray-900 dark:text-white mb-2">Confusion Matrix (Top 5 Classes)</h3>
          <p className="text-xs text-gray-400 mb-4">Rows = Actual, Columns = Predicted</p>
          <div className="overflow-x-auto">
            <table className="text-xs">
              <thead>
                <tr>
                  <th className="text-gray-400 p-2 text-right font-normal">Actual ↓ / Predicted →</th>
                  {confusion.labels.map((l) => (
                    <th key={l} className="p-2 font-semibold text-gray-600 dark:text-gray-300 max-w-[80px] text-center">
                      {l.replace('Tomato ', 'Tom. ').replace('Potato ', 'Pot. ').replace('Apple ', 'App. ')}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {confusion.matrix.map((row, i) => {
                  const total = row.reduce((a, b) => a + b, 0);
                  return (
                    <tr key={i}>
                      <td className="p-2 font-semibold text-gray-600 dark:text-gray-300 text-right pr-4 whitespace-nowrap">
                        {confusion.labels[i].replace('Tomato ', 'Tom. ').replace('Potato ', 'Pot. ')}
                      </td>
                      {row.map((v, j) => {
                        const intensity = total > 0 ? v / total : 0;
                        const isCorrect = i === j;
                        return (
                          <td
                            key={j}
                            className="p-2 text-center font-mono"
                            style={{
                              background: isCorrect
                                ? `rgba(34,197,94,${0.15 + intensity * 0.7})`
                                : intensity > 0.05 ? `rgba(239,68,68,${intensity * 0.5})` : undefined,
                              color: isCorrect ? '#166534' : intensity > 0.05 ? '#b91c1c' : undefined,
                            }}
                          >
                            {v}
                          </td>
                        );
                      })}
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
