import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Microscope, Clock, BarChart3, Leaf, TrendingUp, Activity, CheckCircle2, AlertCircle } from 'lucide-react';
import { getHistory, getHistoryStats, getModelInfo } from '../utils/api';
import type { HistoryItem, HistoryStats, ModelInfo } from '../types';
import SeverityBadge from '../components/SeverityBadge';
import ConfidenceBar from '../components/ConfidenceBar';
import { format, parseISO } from 'date-fns';

export default function DashboardPage() {
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [stats, setStats] = useState<HistoryStats | null>(null);
  const [modelInfo, setModelInfo] = useState<ModelInfo | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      getHistory({ limit: 6 }),
      getHistoryStats(),
      getModelInfo().catch(() => null),
    ]).then(([h, s, m]) => {
      setHistory(h);
      setStats(s);
      setModelInfo(m);
    }).finally(() => setLoading(false));
  }, []);

  const avgConf = history.length > 0
    ? history.reduce((sum, h) => sum + h.confidence, 0) / history.length
    : 0;

  return (
    <div className="max-w-6xl mx-auto px-4 py-10">
      <div className="mb-8">
        <h1 className="text-3xl font-extrabold text-gray-900 dark:text-white mb-1">Dashboard</h1>
        <p className="text-gray-500 dark:text-gray-400">Overview of scan history and model status</p>
      </div>

      {/* Model status banner */}
      {modelInfo && (
        <div className={`card p-4 mb-6 flex items-center gap-3 border-l-4 ${
          modelInfo.model_loaded
            ? 'border-l-green-500 bg-green-50 dark:bg-green-900/10'
            : 'border-l-amber-500 bg-amber-50 dark:bg-amber-900/10'
        }`}>
          {modelInfo.model_loaded
            ? <CheckCircle2 className="w-5 h-5 text-green-500 shrink-0" />
            : <AlertCircle className="w-5 h-5 text-amber-500 shrink-0" />
          }
          <div className="flex-1">
            <p className={`text-sm font-semibold ${modelInfo.model_loaded ? 'text-green-700 dark:text-green-400' : 'text-amber-700 dark:text-amber-400'}`}>
              {modelInfo.model_loaded ? '✓ Real EfficientNetB0 Model Loaded' : '⚠️ Running in Demo Mode'}
            </p>
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">
              {modelInfo.model_loaded
                ? `Real metrics ${modelInfo.real_metrics_available ? 'available' : 'not yet generated (run evaluation)'}`
                : `Model not found at ${modelInfo.model_path}. Train with: python train_model.py --data_dir ./data/PlantVillage`
              }
            </p>
          </div>
          {!modelInfo.model_loaded && (
            <Link to="/about" className="btn-secondary text-xs shrink-0">Setup Guide</Link>
          )}
        </div>
      )}

      {/* Stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {[
          {
            label: 'Total Scans', value: loading ? '—' : (stats?.count ?? 0),
            icon: Microscope, color: 'text-brand-500', bg: 'bg-brand-50 dark:bg-brand-900/20'
          },
          {
            label: 'Diseases Found', value: loading ? '—' : (stats?.diseased ?? 0),
            icon: Activity, color: 'text-red-500', bg: 'bg-red-50 dark:bg-red-900/20'
          },
          {
            label: 'Healthy Plants', value: loading ? '—' : (stats?.healthy ?? 0),
            icon: Leaf, color: 'text-green-500', bg: 'bg-green-50 dark:bg-green-900/20'
          },
          {
            label: 'Avg Confidence', value: loading ? '—' : `${Math.round(avgConf * 100)}%`,
            icon: TrendingUp, color: 'text-ai-500', bg: 'bg-ai-50 dark:bg-ai-900/20'
          },
        ].map(({ label, value, icon: Icon, color, bg }) => (
          <div key={label} className="card p-5 flex items-center gap-4">
            <div className={`w-11 h-11 rounded-xl ${bg} flex items-center justify-center shrink-0`}>
              <Icon className={`w-5 h-5 ${color}`} />
            </div>
            <div>
              <div className="text-xl font-bold text-gray-900 dark:text-white">{value}</div>
              <div className="text-xs text-gray-500 dark:text-gray-400">{label}</div>
            </div>
          </div>
        ))}
      </div>

      {/* Most detected disease */}
      {stats?.most_common_disease && (
        <div className="card p-4 mb-6 flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-red-50 dark:bg-red-900/20 flex items-center justify-center shrink-0">
            <Activity className="w-5 h-5 text-red-500" />
          </div>
          <div>
            <p className="text-xs text-gray-400 uppercase tracking-wide font-semibold">Most Detected Disease</p>
            <p className="font-bold text-gray-900 dark:text-white">{stats.most_common_disease}</p>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent scans */}
        <div className="card p-5">
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-bold text-gray-900 dark:text-white flex items-center gap-2">
              <Clock className="w-4 h-4 text-gray-400" />
              Recent Diagnoses
            </h2>
            <Link to="/history" className="text-xs text-brand-600 dark:text-brand-400 hover:underline">
              View all →
            </Link>
          </div>

          {loading && (
            <div className="space-y-3">
              {[...Array(4)].map((_, i) => (
                <div key={i} className="h-12 rounded-xl bg-gray-100 dark:bg-slate-700 animate-pulse" />
              ))}
            </div>
          )}

          {!loading && history.length === 0 && (
            <div className="text-center py-8 text-gray-400">
              <Microscope className="w-8 h-8 mx-auto mb-2 opacity-40" />
              <p className="text-sm">No diagnoses yet.</p>
              <Link to="/diagnose" className="btn-primary mt-3 text-sm inline-flex">Start Diagnosis</Link>
            </div>
          )}

          {!loading && history.map((h) => (
            <div key={h.id} className="flex items-center gap-3 py-2.5 border-b border-gray-100 dark:border-slate-700 last:border-0">
              <div className="w-8 h-8 rounded-lg bg-brand-50 dark:bg-brand-900/20 flex items-center justify-center shrink-0">
                <Leaf className="w-4 h-4 text-brand-500" />
              </div>
              <div className="flex-1 min-w-0">
                <div className="text-sm font-medium text-gray-900 dark:text-white truncate">{h.disease_name}</div>
                <div className="text-xs text-gray-400">{h.plant_name} · {format(parseISO(h.created_at), 'MMM d, HH:mm')}</div>
              </div>
              <div className="flex items-center gap-2 shrink-0">
                <SeverityBadge severity={h.severity} />
                {h.is_demo && (
                  <span className="tag bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-400 text-xs">Demo</span>
                )}
              </div>
            </div>
          ))}
        </div>

        {/* Model performance + quick actions */}
        <div className="space-y-4">
          {/* Confidence breakdown */}
          {!loading && history.length > 0 && (
            <div className="card p-5">
              <div className="flex items-center justify-between mb-4">
                <h2 className="font-bold text-gray-900 dark:text-white flex items-center gap-2">
                  <BarChart3 className="w-4 h-4 text-gray-400" />
                  Recent Confidence Scores
                </h2>
                <Link to="/analytics" className="text-xs text-brand-600 dark:text-brand-400 hover:underline">
                  Analytics →
                </Link>
              </div>
              <div className="space-y-2">
                {history.slice(0, 5).map((h) => (
                  <div key={h.id} className="flex items-center gap-3">
                    <span className="text-xs text-gray-500 dark:text-gray-400 w-28 truncate shrink-0">{h.disease_name}</span>
                    <ConfidenceBar confidence={h.confidence} className="flex-1" />
                    <span className="text-xs font-bold text-gray-600 dark:text-gray-300 w-10 text-right shrink-0">
                      {Math.round(h.confidence * 100)}%
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Quick actions */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            {[
              { to: '/diagnose', label: 'New Diagnosis', icon: Microscope, desc: 'Analyse a leaf image', color: 'from-brand-500 to-brand-600' },
              { to: '/library', label: 'Plant Library', icon: Leaf, desc: '38 disease classes', color: 'from-ai-500 to-cyan-500' },
              { to: '/treatment', label: 'Treatment Guide', icon: Activity, desc: 'Pesticide & management', color: 'from-purple-500 to-violet-600' },
            ].map(({ to, label, icon: Icon, desc, color }) => (
              <Link key={to} to={to}
                className="card p-4 flex items-center gap-3 hover:shadow-md hover:-translate-y-0.5 transition-all duration-200">
                <div className={`w-10 h-10 rounded-xl bg-gradient-to-br ${color} flex items-center justify-center shrink-0 shadow-sm`}>
                  <Icon className="w-5 h-5 text-white" />
                </div>
                <div>
                  <div className="font-semibold text-gray-900 dark:text-white text-sm">{label}</div>
                  <div className="text-xs text-gray-400">{desc}</div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
