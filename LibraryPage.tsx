import { useEffect, useState } from 'react';
import { BookOpen, Search, ChevronRight, Leaf, X } from 'lucide-react';
import { getPlantLibrary, getDiseaseDetail } from '../utils/api';
import type { PlantEntry, DiseaseEntry } from '../types';
import TypeBadge from '../components/TypeBadge';

export default function LibraryPage() {
  const [library, setLibrary] = useState<PlantEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [query, setQuery] = useState('');
  const [selected, setSelected] = useState<PlantEntry | null>(null);
  const [selectedDisease, setSelectedDisease] = useState<DiseaseEntry | null>(null);

  const load = (q?: string) => {
    setLoading(true);
    getPlantLibrary(q).then(setLibrary).finally(() => setLoading(false));
  };

  useEffect(() => { load(); }, []);

  const handleSearch = () => load(query || undefined);

  return (
    <div className="max-w-6xl mx-auto px-4 py-10">
      <div className="mb-8">
        <h1 className="text-3xl font-extrabold text-gray-900 dark:text-white mb-1 flex items-center gap-3">
          <BookOpen className="w-7 h-7 text-brand-500" />
          Plant Library
        </h1>
        <p className="text-gray-500 dark:text-gray-400">Encyclopedia of 10 crops and 38 disease/healthy classes</p>
      </div>

      {/* Search */}
      <div className="flex gap-3 mb-6 max-w-xl">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
          <input
            type="text"
            placeholder="Search plants or diseases..."
            value={query}
            onChange={e => setQuery(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleSearch()}
            className="w-full pl-9 pr-3 py-2.5 rounded-xl border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-sm text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-brand-400"
          />
        </div>
        <button onClick={handleSearch} className="btn-primary">Search</button>
        {query && (
          <button onClick={() => { setQuery(''); load(); }} className="btn-secondary">
            <X className="w-4 h-4" />
          </button>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Plant list */}
        <div className="lg:col-span-1">
          {loading && (
            <div className="space-y-2">
              {[...Array(5)].map((_, i) => (
                <div key={i} className="h-14 rounded-xl bg-gray-100 dark:bg-slate-800 animate-pulse" />
              ))}
            </div>
          )}
          {!loading && library.map((plant) => (
            <button
              key={plant.name}
              onClick={() => { setSelected(plant); setSelectedDisease(null); }}
              className={`w-full flex items-center gap-3 p-3.5 rounded-xl mb-2 text-left transition-all ${
                selected?.name === plant.name
                  ? 'bg-brand-50 dark:bg-brand-900/20 border border-brand-200 dark:border-brand-700'
                  : 'hover:bg-gray-50 dark:hover:bg-slate-800 border border-transparent'
              }`}
            >
              <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-brand-100 to-green-100 dark:from-brand-900/30 dark:to-green-900/30 flex items-center justify-center shrink-0">
                <Leaf className="w-5 h-5 text-brand-500" />
              </div>
              <div className="flex-1 min-w-0">
                <div className="font-semibold text-sm text-gray-900 dark:text-white truncate">{plant.name}</div>
                <div className="text-xs text-gray-400">{plant.diseases.length} disease class{plant.diseases.length !== 1 ? 'es' : ''}</div>
              </div>
              <ChevronRight className="w-4 h-4 text-gray-300 dark:text-gray-600 shrink-0" />
            </button>
          ))}
        </div>

        {/* Disease list or Disease detail */}
        <div className="lg:col-span-2">
          {!selected && (
            <div className="card p-12 flex flex-col items-center justify-center text-center gap-3 h-64 border-dashed">
              <BookOpen className="w-10 h-10 text-gray-300 dark:text-gray-600" />
              <p className="text-gray-400">Select a plant to see its diseases</p>
            </div>
          )}

          {selected && !selectedDisease && (
            <div className="card p-5">
              <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-1">{selected.name}</h2>
              <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">
                {selected.diseases.length} disease class{selected.diseases.length !== 1 ? 'es' : ''} · {selected.healthy_class ? 'Healthy class available' : ''}
              </p>
              <div className="space-y-2">
                {selected.diseases.map((d) => (
                  <button
                    key={d.class_label}
                    onClick={() => setSelectedDisease(d)}
                    className="w-full flex items-center gap-3 p-3 rounded-xl hover:bg-gray-50 dark:hover:bg-slate-700 border border-gray-100 dark:border-slate-700 text-left transition-colors"
                  >
                    <div className="flex-1">
                      <div className="font-medium text-sm text-gray-900 dark:text-white">{d.common_name}</div>
                      <div className="text-xs text-gray-400 mt-0.5 line-clamp-1">{d.summary}</div>
                    </div>
                    <TypeBadge type={d.type} />
                    <ChevronRight className="w-4 h-4 text-gray-300 dark:text-gray-600 shrink-0" />
                  </button>
                ))}
              </div>
            </div>
          )}

          {selected && selectedDisease && (
            <DiseaseDetailCard
              disease={selectedDisease}
              onBack={() => setSelectedDisease(null)}
            />
          )}
        </div>
      </div>
    </div>
  );
}

function DiseaseDetailCard({ disease, onBack }: { disease: DiseaseEntry; onBack: () => void }) {
  const [detail, setDetail] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getDiseaseDetail(disease.class_label).then(setDetail).finally(() => setLoading(false));
  }, [disease.class_label]);

  return (
    <div className="card p-5">
      <button onClick={onBack} className="flex items-center gap-1 text-sm text-brand-600 dark:text-brand-400 hover:underline mb-4">
        ← Back to {disease.class_label.split('___')[0]?.replace(/_/g, ' ')}
      </button>
      {loading && <div className="space-y-2">{[...Array(4)].map((_, i) => <div key={i} className="h-6 rounded-lg bg-gray-100 dark:bg-slate-700 animate-pulse" />)}</div>}
      {detail && (
        <div className="text-sm space-y-4">
          <div className="flex items-start gap-3">
            <div>
              <h2 className="text-xl font-bold text-gray-900 dark:text-white">{detail.disease_info?.common_name}</h2>
              <p className="text-gray-400 italic">{detail.disease_info?.scientific_name}</p>
            </div>
            <TypeBadge type={detail.disease_info?.type ?? ''} />
          </div>
          <p className="text-gray-500 dark:text-gray-400 leading-relaxed">{detail.disease_info?.summary}</p>

          {detail.disease_info?.symptoms?.length > 0 && (
            <div>
              <h4 className="font-semibold text-gray-900 dark:text-white mb-2">Symptoms</h4>
              <ul className="list-disc list-inside space-y-1 text-gray-500 dark:text-gray-400">
                {detail.disease_info.symptoms.map((s: string, i: number) => <li key={i}>{s}</li>)}
              </ul>
            </div>
          )}
          {detail.disease_info?.cause && detail.disease_info.cause !== 'N/A' && (
            <div>
              <h4 className="font-semibold text-gray-900 dark:text-white mb-1">Cause</h4>
              <p className="text-gray-500 dark:text-gray-400">{detail.disease_info.cause}</p>
            </div>
          )}
          {detail.disease_info?.prevention?.length > 0 && (
            <div>
              <h4 className="font-semibold text-gray-900 dark:text-white mb-2">Prevention</h4>
              <ul className="list-disc list-inside space-y-1 text-gray-500 dark:text-gray-400">
                {detail.disease_info.prevention.map((p: string, i: number) => <li key={i}>{p}</li>)}
              </ul>
            </div>
          )}
          {detail.disease_info?.references?.length > 0 && (
            <p className="text-xs text-gray-400 border-t border-gray-100 dark:border-slate-700 pt-3">
              Sources: {detail.disease_info.references.join(' · ')}
            </p>
          )}
        </div>
      )}
    </div>
  );
}
