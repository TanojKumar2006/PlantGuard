import { useEffect, useState } from 'react';
import { FlaskConical, Search, ChevronRight, X, AlertTriangle } from 'lucide-react';
import { getTreatmentList, getTreatmentGuide } from '../utils/api';

export default function TreatmentPage() {
  const [list, setList] = useState<string[]>([]);
  const [search, setSearch] = useState('');
  const [selected, setSelected] = useState<string | null>(null);
  const [detail, setDetail] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    getTreatmentList().then((d) => setList(d.entries ?? []));
  }, []);

  const filtered = list.filter((l) =>
    !search || l.toLowerCase().replace(/_/g, ' ').includes(search.toLowerCase())
  );

  const handleSelect = async (label: string) => {
    setSelected(label);
    setLoading(true);
    setDetail(null);
    try {
      const d = await getTreatmentGuide(label);
      setDetail(d);
    } catch { /* ignore */ }
    setLoading(false);
  };

  const labelToDisplay = (l: string) => {
    const [plant, disease] = l.split('___');
    return `${plant?.replace(/_/g,' ')} — ${disease?.replace(/_/g,' ')}`;
  };

  return (
    <div className="max-w-6xl mx-auto px-4 py-10">
      <div className="mb-8">
        <h1 className="text-3xl font-extrabold text-gray-900 dark:text-white mb-1 flex items-center gap-3">
          <FlaskConical className="w-7 h-7 text-ai-500" />
          Treatment Guide
        </h1>
        <p className="text-gray-500 dark:text-gray-400">Verified pesticide & management information by disease</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Disease selector */}
        <div className="lg:col-span-1">
          <div className="relative mb-3">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search disease..."
              value={search}
              onChange={e => setSearch(e.target.value)}
              className="w-full pl-9 pr-3 py-2.5 rounded-xl border border-gray-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-sm text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-brand-400"
            />
          </div>
          <div className="space-y-1 max-h-[60vh] overflow-y-auto">
            {filtered.map((label) => (
              <button
                key={label}
                onClick={() => handleSelect(label)}
                className={`w-full text-left px-3 py-2.5 rounded-xl text-sm transition-colors ${
                  selected === label
                    ? 'bg-brand-50 dark:bg-brand-900/20 border border-brand-200 dark:border-brand-700 text-brand-700 dark:text-brand-400'
                    : 'hover:bg-gray-50 dark:hover:bg-slate-800 text-gray-700 dark:text-gray-300'
                }`}
              >
                {labelToDisplay(label)}
              </button>
            ))}
          </div>
        </div>

        {/* Detail */}
        <div className="lg:col-span-2">
          {!selected && (
            <div className="card p-12 flex flex-col items-center justify-center text-center gap-3 h-64 border-dashed">
              <FlaskConical className="w-10 h-10 text-gray-300 dark:text-gray-600" />
              <p className="text-gray-400">Select a disease to view treatment options</p>
            </div>
          )}
          {loading && (
            <div className="space-y-3">
              {[...Array(3)].map((_, i) => <div key={i} className="h-16 rounded-xl bg-gray-100 dark:bg-slate-800 animate-pulse" />)}
            </div>
          )}
          {detail && !loading && (
            <div className="space-y-4">
              <div className="card p-5">
                <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-0.5">{detail.disease_name}</h2>
                <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">{detail.plant_name}</p>
                <div className="text-xs text-amber-700 dark:text-amber-400 bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-lg px-3 py-2">
                  <AlertTriangle className="inline w-3.5 h-3.5 mr-1" />
                  {detail.disclaimer}
                </div>
              </div>

              {detail.prevention?.length > 0 && (
                <div className="card p-5">
                  <h3 className="font-bold text-gray-900 dark:text-white mb-3">Prevention & Cultural Practices</h3>
                  <ul className="text-sm text-gray-500 dark:text-gray-400 space-y-1 list-disc list-inside">
                    {detail.prevention.map((p: string, i: number) => <li key={i}>{p}</li>)}
                  </ul>
                  {detail.cultural_biological?.length > 0 && (
                    <div className="mt-3">
                      <h4 className="font-semibold text-sm text-gray-700 dark:text-gray-200 mb-2">Biological / Cultural Controls</h4>
                      <ul className="text-sm text-gray-500 dark:text-gray-400 space-y-1 list-disc list-inside">
                        {detail.cultural_biological.map((c: string, i: number) => <li key={i}>{c}</li>)}
                      </ul>
                    </div>
                  )}
                </div>
              )}

              {detail.treatments?.map((t: any, i: number) => (
                <div key={i} className="card p-5">
                  <div className="flex items-start justify-between gap-2 mb-3">
                    <div>
                      <h3 className="font-bold text-gray-900 dark:text-white">{t.active_ingredient}</h3>
                      <p className="text-xs text-gray-400 italic mt-0.5">{t.product_example}</p>
                    </div>
                    <span className="tag bg-ai-100 text-ai-700 dark:bg-ai-900/40 dark:text-ai-400 shrink-0">Option {i + 1}</span>
                  </div>
                  <div className="grid grid-cols-2 gap-3 mb-3">
                    {[
                      ['Use For', t.use_for],
                      ['Rate', t.rate],
                      ['Preparation', t.preparation],
                      ['When to Apply', t.when_to_apply],
                      ['Frequency', t.frequency],
                      ['Pre-harvest Interval', t.phi],
                    ].map(([k, v]) => (
                      <div key={k} className="bg-gray-50 dark:bg-slate-800/50 rounded-lg p-3">
                        <div className="text-xs text-gray-400 mb-1">{k}</div>
                        <div className="text-sm text-gray-700 dark:text-gray-200">{v}</div>
                      </div>
                    ))}
                  </div>
                  {t.safety?.length > 0 && (
                    <div className="rounded-xl bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 p-3">
                      <div className="text-xs font-semibold text-red-700 dark:text-red-400 mb-1">⚠ Safety Precautions</div>
                      <ul className="text-xs text-red-600 dark:text-red-300 space-y-0.5">
                        {t.safety.map((s: string, si: number) => <li key={si}>• {s}</li>)}
                      </ul>
                    </div>
                  )}
                  <div className="text-xs text-gray-400 mt-3 border-t border-gray-100 dark:border-slate-700 pt-2">
                    Source: {t.source}
                  </div>
                </div>
              ))}

              {detail.products?.length > 0 && (
                <div className="card p-5">
                  <h3 className="font-bold text-gray-900 dark:text-white mb-3">Available Products</h3>
                  <p className="text-xs text-gray-400 mb-3">Product listing is informational only. Verify availability and registration in your region before purchase.</p>
                  {detail.products.map((p: any, i: number) => (
                    <div key={i} className="border border-gray-100 dark:border-slate-700 rounded-xl p-3 mb-2">
                      <div className="font-medium text-gray-900 dark:text-white text-sm">{p.product_name}</div>
                      <div className="text-xs text-gray-400 mt-0.5">{p.active_ingredient} · {p.manufacturer}</div>
                      <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">{p.availability}</div>
                      <div className="text-xs text-brand-600 dark:text-brand-400 mt-1">{p.buy_link_note}</div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
