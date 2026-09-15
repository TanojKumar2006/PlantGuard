import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Clock, Search, Trash2, Leaf, X, Eye, ExternalLink } from 'lucide-react';
import { getHistory, deleteHistoryItem, clearHistory } from '../utils/api';
import type { HistoryItem } from '../types';
import SeverityBadge from '../components/SeverityBadge';
import ConfidenceBar from '../components/ConfidenceBar';
import { format, parseISO } from 'date-fns';

const API_BASE = '';  // Proxied through vite: /uploads → backend

export default function HistoryPage() {
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchPlant, setSearchPlant] = useState('');
  const [searchDisease, setSearchDisease] = useState('');
  const [deleting, setDeleting] = useState<number | null>(null);

  const load = (plant?: string, disease?: string) => {
    setLoading(true);
    getHistory({ limit: 100, plant: plant || undefined, disease: disease || undefined })
      .then(setHistory)
      .finally(() => setLoading(false));
  };

  useEffect(() => { load(); }, []);

  const handleSearch = () => load(searchPlant, searchDisease);
  const handleClear = () => {
    if (!confirm('Clear all prediction history? This cannot be undone.')) return;
    clearHistory().then(() => load());
  };
  const handleDelete = async (id: number) => {
    setDeleting(id);
    await deleteHistoryItem(id);
    setDeleting(null);
    setHistory(prev => prev.filter(h => h.id !== id));
  };

  return (
    <div className="max-w-5xl mx-auto px-4 py-10">
      <div className="flex items-start justify-between mb-8 gap-4">
        <div>
          <h1 className="text-3xl font-extrabold text-gray-900 dark:text-white mb-1 flex items-center gap-3">
            <Clock className="w-7 h-7 text-brand-500" />
            Diagnosis History
          </h1>
          <p className="text-gray-500 dark:text-gray-400">
            {loading ? 'Loading…' : `${history.length} diagnosis record${history.length !== 1 ? 's' : ''}`}
          </p>
        </div>
        {history.length > 0 && (
          <button onClick={handleClear} className="btn-secondary text-sm text-red-600 dark:text-red-400 shrink-0">
            <Trash2 className="w-4 h-4" />
            Clear All
          </button>
        )}
      </div>

      {/* Search */}
      <div className="card p-4 mb-6 flex flex-col sm:flex-row gap-3">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 pointer-events-none" />
          <input type="text" placeholder="Filter by plant…"
            value={searchPlant}
            onChange={e => setSearchPlant(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleSearch()}
            className="w-full pl-9 pr-3 py-2 rounded-xl border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-sm text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-brand-400"
          />
        </div>
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 pointer-events-none" />
          <input type="text" placeholder="Filter by disease…"
            value={searchDisease}
            onChange={e => setSearchDisease(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleSearch()}
            className="w-full pl-9 pr-3 py-2 rounded-xl border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-sm text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-brand-400"
          />
        </div>
        <button onClick={handleSearch} className="btn-primary shrink-0">Search</button>
        {(searchPlant || searchDisease) && (
          <button onClick={() => { setSearchPlant(''); setSearchDisease(''); load(); }} className="btn-secondary shrink-0">
            <X className="w-4 h-4" />
          </button>
        )}
      </div>

      {loading && (
        <div className="space-y-3">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="h-24 rounded-2xl bg-gray-100 dark:bg-slate-800 animate-pulse" />
          ))}
        </div>
      )}

      {!loading && history.length === 0 && (
        <div className="card p-12 text-center">
          <Leaf className="w-10 h-10 mx-auto mb-3 text-gray-300 dark:text-gray-600" />
          <p className="text-gray-500 dark:text-gray-400 mb-3">No diagnoses found.</p>
          <Link to="/diagnose" className="btn-primary inline-flex">Start Diagnosis</Link>
        </div>
      )}

      {!loading && history.length > 0 && (
        <div className="space-y-3">
          {history.map((h) => (
            <div key={h.id} className="card p-4 flex items-center gap-4 hover:shadow-md transition-shadow group">
              {/* Thumbnail */}
              <div className="w-14 h-14 rounded-xl overflow-hidden shrink-0 border border-gray-200 dark:border-slate-700 bg-gray-100 dark:bg-slate-700">
                {h.image_path ? (
                  <img
                    src={`${API_BASE}${h.image_path}`}
                    alt={h.disease_name}
                    className="w-full h-full object-cover"
                    onError={e => { (e.target as HTMLImageElement).style.display = 'none'; }}
                  />
                ) : (
                  <div className="w-full h-full flex items-center justify-center">
                    <Leaf className="w-6 h-6 text-brand-500" />
                  </div>
                )}
              </div>

              {/* Info */}
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-0.5 flex-wrap">
                  <span className="font-semibold text-gray-900 dark:text-white text-sm">{h.disease_name}</span>
                  <SeverityBadge severity={h.severity} />
                  {h.is_demo && (
                    <span className="tag bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-400 text-xs">Demo</span>
                  )}
                </div>
                <div className="text-xs text-gray-400 mb-2">
                  {h.plant_name} · {h.created_at ? format(parseISO(h.created_at), 'PPp') : ''}
                </div>
                <div className="flex items-center gap-2">
                  <ConfidenceBar confidence={h.confidence} className="w-32" />
                  <span className="text-xs text-gray-500 dark:text-gray-400">
                    {Math.round(h.confidence * 100)}% confidence
                  </span>
                </div>
              </div>

              {/* Model badge */}
              <div className="hidden md:block text-xs text-gray-400 text-right shrink-0 max-w-[120px]">
                <div className="truncate">{h.model_used?.replace('EfficientNetB0 (TensorFlow/Keras) – trained on PlantVillage', 'EfficientNetB0')}</div>
              </div>

              {/* Actions */}
              <div className="flex items-center gap-1 shrink-0">
                {/* View result button */}
                <Link
                  to={`/diagnose`}
                  state={{ historyId: h.id }}
                  className="p-2 rounded-xl hover:bg-brand-50 dark:hover:bg-brand-900/20 text-gray-400 hover:text-brand-500 transition-colors"
                  title="View details"
                >
                  <Eye className="w-4 h-4" />
                </Link>
                {/* Delete */}
                <button
                  onClick={() => handleDelete(h.id)}
                  disabled={deleting === h.id}
                  className="p-2 rounded-xl hover:bg-red-50 dark:hover:bg-red-900/20 text-gray-400 hover:text-red-500 transition-colors"
                  title="Delete"
                >
                  {deleting === h.id ? (
                    <div className="w-4 h-4 border-2 border-gray-300 border-t-red-500 rounded-full animate-spin" />
                  ) : (
                    <Trash2 className="w-4 h-4" />
                  )}
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
