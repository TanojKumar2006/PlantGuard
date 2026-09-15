import { useState, useCallback, useRef } from 'react';
import { useDropzone } from 'react-dropzone';
import Webcam from 'react-webcam';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Upload, Camera, X, AlertTriangle, CheckCircle, Loader2,
  FlaskConical, Leaf, Microscope, Info, ChevronDown, ChevronUp,
  ShieldAlert, Activity, RefreshCw, ZoomIn, Eye, BookOpen,
  Thermometer, Bug, AlertCircle, ShoppingBag, Image as ImageIcon,
  Brain, Sparkles, TriangleAlert,
} from 'lucide-react';
import { analyzeImage } from '../utils/api';
import type { AnalysisResult } from '../types';
import SeverityBadge from '../components/SeverityBadge';
import TypeBadge from '../components/TypeBadge';
import ConfidenceBar from '../components/ConfidenceBar';

type Tab = 'upload' | 'camera';
type GradcamView = 'overlay' | 'heatmap' | 'original';

function Section({ title, icon: Icon, iconColor, children, defaultOpen = true }: {
  title: string;
  icon: React.ElementType;
  iconColor: string;
  children: React.ReactNode;
  defaultOpen?: boolean;
}) {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <div className="card overflow-hidden">
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex items-center justify-between p-4 hover:bg-gray-50 dark:hover:bg-slate-700/50 transition-colors"
      >
        <div className="flex items-center gap-2">
          <Icon className={`w-4 h-4 ${iconColor}`} />
          <span className="font-semibold text-gray-900 dark:text-white text-sm">{title}</span>
        </div>
        {open ? <ChevronUp className="w-4 h-4 text-gray-400" /> : <ChevronDown className="w-4 h-4 text-gray-400" />}
      </button>
      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="overflow-hidden"
          >
            <div className="px-4 pb-5 border-t border-gray-100 dark:border-slate-700 pt-4">
              {children}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

function BulletList({ items, icon: Icon = CheckCircle, iconClass = 'text-brand-500' }: {
  items: string[];
  icon?: React.ElementType;
  iconClass?: string;
}) {
  return (
    <ul className="space-y-2">
      {items.map((item, i) => (
        <li key={i} className="flex items-start gap-2">
          <Icon className={`w-3.5 h-3.5 ${iconClass} mt-0.5 shrink-0`} />
          <span className="text-sm text-gray-600 dark:text-gray-300">{item}</span>
        </li>
      ))}
    </ul>
  );
}

function InfoGrid({ items }: { items: [string, string][] }) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
      {items.filter(([, v]) => v && v !== 'N/A').map(([k, v]) => (
        <div key={k} className="bg-gray-50 dark:bg-slate-800/60 rounded-xl p-3">
          <div className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-1">{k}</div>
          <div className="text-sm text-gray-700 dark:text-gray-200 leading-snug">{v}</div>
        </div>
      ))}
    </div>
  );
}

export default function DiagnosePage() {
  const [tab, setTab] = useState<Tab>('upload');
  const [preview, setPreview] = useState<string | null>(null);
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [scanning, setScanning] = useState(false);
  const [gradcamView, setGradcamView] = useState<GradcamView>('overlay');
  const webcamRef = useRef<Webcam>(null);

  const onDrop = useCallback((accepted: File[]) => {
    if (!accepted[0]) return;
    setFile(accepted[0]);
    setPreview(URL.createObjectURL(accepted[0]));
    setResult(null);
    setError(null);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'image/jpeg': [], 'image/png': [], 'image/webp': [] },
    maxFiles: 1,
    multiple: false,
  });

  const capturePhoto = () => {
    const src = webcamRef.current?.getScreenshot();
    if (!src) return;
    fetch(src).then(r => r.blob()).then(blob => {
      const f = new File([blob], 'capture.jpg', { type: 'image/jpeg' });
      setFile(f);
      setPreview(src);
      setResult(null);
      setError(null);
      setTab('upload');
    });
  };

  const handleAnalyze = async () => {
    if (!file) return;
    setLoading(true);
    setScanning(true);
    setError(null);
    setResult(null);
    try {
      await new Promise(r => setTimeout(r, 1400));
      setScanning(false);
      const res = await analyzeImage(file);
      setResult(res);
    } catch (e: any) {
      setError(e?.response?.data?.detail ?? e?.message ?? 'Analysis failed. Is the backend running?');
    } finally {
      setLoading(false);
      setScanning(false);
    }
  };

  const handleReset = () => {
    setPreview(null);
    setFile(null);
    setResult(null);
    setError(null);
  };

  const currentGradcam =
    gradcamView === 'overlay' ? result?.gradcam_overlay_b64 :
    gradcamView === 'heatmap' ? result?.gradcam_heatmap_b64 :
    result?.gradcam_original_b64;

  const hasGradcam = !!(result?.gradcam_overlay_b64 || result?.gradcam_heatmap_b64);

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-2 mb-2">
          <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-brand-500 to-ai-500 flex items-center justify-center">
            <Microscope className="w-4 h-4 text-white" />
          </div>
          <h1 className="text-2xl font-extrabold text-gray-900 dark:text-white">
            Plant Disease Diagnosis
          </h1>
        </div>
        <p className="text-gray-500 dark:text-gray-400 text-sm ml-10">
          Upload a clear leaf photo. Our EfficientNetB0 AI will identify diseases, estimate severity, and generate a treatment plan.
        </p>
      </div>

      {/* Main grid */}
      <div className="grid grid-cols-1 xl:grid-cols-5 gap-6">
        {/* ── Left panel: Upload ── */}
        <div className="xl:col-span-2 space-y-4">
          {/* Tab selector */}
          <div className="flex rounded-xl overflow-hidden border border-gray-200 dark:border-slate-700">
            {(['upload', 'camera'] as Tab[]).map((t) => (
              <button key={t} onClick={() => setTab(t)}
                className={`flex-1 flex items-center justify-center gap-2 py-3 text-sm font-semibold transition-colors ${
                  tab === t
                    ? 'bg-gradient-to-r from-brand-500 to-brand-600 text-white shadow-sm'
                    : 'bg-white dark:bg-slate-800 text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-slate-700'
                }`}>
                {t === 'upload' ? <Upload className="w-4 h-4" /> : <Camera className="w-4 h-4" />}
                {t === 'upload' ? 'Upload Image' : 'Live Camera'}
              </button>
            ))}
          </div>

          {/* Drop zone */}
          {tab === 'upload' && !preview && (
            <div {...getRootProps()}
              className={`border-2 border-dashed rounded-2xl p-10 text-center cursor-pointer transition-all duration-200 ${
                isDragActive
                  ? 'border-brand-500 bg-brand-50 dark:bg-brand-900/20 scale-[1.01]'
                  : 'border-gray-300 dark:border-slate-600 hover:border-brand-400 hover:bg-gray-50 dark:hover:bg-slate-800/50'
              }`}>
              <input {...getInputProps()} />
              <div className="flex flex-col items-center gap-4">
                <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-brand-100 to-ai-100 dark:from-brand-900/30 dark:to-ai-900/30 flex items-center justify-center">
                  <Upload className="w-8 h-8 text-brand-500" />
                </div>
                <div>
                  <p className="font-semibold text-gray-700 dark:text-gray-200">
                    {isDragActive ? 'Drop here!' : 'Drag & drop a leaf image'}
                  </p>
                  <p className="text-xs text-gray-400 mt-1">JPEG · PNG · WEBP · max 20 MB</p>
                </div>
                <div className="flex gap-2 flex-wrap justify-center">
                  {['Tomato leaf', 'Corn leaf', 'Potato leaf', 'Apple leaf'].map(t => (
                    <span key={t} className="tag bg-gray-100 dark:bg-slate-700 text-gray-500 dark:text-gray-400 text-xs">{t}</span>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Camera */}
          {tab === 'camera' && !preview && (
            <div className="rounded-2xl overflow-hidden border border-gray-200 dark:border-slate-700">
              <Webcam ref={webcamRef} screenshotFormat="image/jpeg" className="w-full"
                videoConstraints={{ facingMode: 'environment' }} />
              <button onClick={capturePhoto}
                className="w-full py-3 bg-gradient-to-r from-brand-500 to-brand-600 hover:from-brand-600 hover:to-brand-700 text-white font-semibold flex items-center justify-center gap-2 transition-colors">
                <Camera className="w-4 h-4" /> Capture Photo
              </button>
            </div>
          )}

          {/* Preview */}
          {preview && (
            <motion.div initial={{ opacity: 0, scale: 0.97 }} animate={{ opacity: 1, scale: 1 }}
              className="relative rounded-2xl overflow-hidden border border-gray-200 dark:border-slate-700 bg-black aspect-square">
              <img src={preview} alt="Leaf preview" className="w-full h-full object-contain" />
              {/* Scanning overlay */}
              {scanning && (
                <div className="absolute inset-0 bg-black/65 flex flex-col items-center justify-center gap-4">
                  <div className="relative w-full h-full overflow-hidden">
                    <div className="scan-line opacity-80" />
                    {['top-6 left-6 border-t-2 border-l-2', 'top-6 right-6 border-t-2 border-r-2',
                      'bottom-6 left-6 border-b-2 border-l-2', 'bottom-6 right-6 border-b-2 border-r-2'].map(c => (
                      <div key={c} className={`absolute w-8 h-8 border-brand-400 ${c}`} />
                    ))}
                    <div className="absolute inset-0 flex items-center justify-center">
                      <div className="text-center text-white">
                        <div className="w-16 h-16 rounded-full bg-brand-500/20 border-2 border-brand-400 flex items-center justify-center mx-auto mb-3">
                          <Brain className="w-7 h-7 text-brand-400 animate-pulse" />
                        </div>
                        <p className="text-sm font-semibold">Scanning leaf tissue…</p>
                        <p className="text-xs text-gray-300 mt-1">Running EfficientNetB0</p>
                      </div>
                    </div>
                  </div>
                </div>
              )}
              <button onClick={handleReset}
                className="absolute top-3 right-3 p-1.5 rounded-full bg-black/60 text-white hover:bg-black/80 transition-colors">
                <X className="w-4 h-4" />
              </button>
            </motion.div>
          )}

          {/* Analyze button */}
          {preview && !loading && !result && (
            <motion.button onClick={handleAnalyze} whileTap={{ scale: 0.97 }}
              className="w-full btn-primary justify-center py-4 text-base shadow-glow-green">
              <Sparkles className="w-5 h-5" />
              Analyse with AI
            </motion.button>
          )}

          {loading && !scanning && (
            <div className="card p-4 flex items-center gap-3">
              <Loader2 className="w-5 h-5 animate-spin text-brand-500 shrink-0" />
              <div>
                <p className="text-sm font-medium text-gray-700 dark:text-gray-200">Processing image…</p>
                <p className="text-xs text-gray-400">This may take a moment on first run</p>
              </div>
            </div>
          )}

          {error && (
            <motion.div initial={{ opacity: 0, y: -8 }} animate={{ opacity: 1, y: 0 }}
              className="card p-4 flex items-start gap-3 border-red-200 dark:border-red-800 bg-red-50 dark:bg-red-900/20">
              <AlertTriangle className="w-5 h-5 text-red-500 shrink-0 mt-0.5" />
              <div className="text-sm text-red-700 dark:text-red-300">
                <strong>Error:</strong> {error}
              </div>
            </motion.div>
          )}

          {result && (
            <button onClick={handleReset} className="btn-secondary w-full justify-center">
              <RefreshCw className="w-4 h-4" />
              Diagnose another plant
            </button>
          )}

          {/* AI disclaimer */}
          <div className="card p-3 flex items-start gap-2 text-xs text-gray-400 dark:text-gray-500">
            <TriangleAlert className="w-3.5 h-3.5 shrink-0 mt-0.5 text-amber-400" />
            <span>AI diagnosis is for educational purposes. Always consult a qualified agronomist for professional advice.</span>
          </div>
        </div>

        {/* ── Right panel: Results ── */}
        <div className="xl:col-span-3 space-y-4">
          {!result && !loading && (
            <div className="card p-12 flex flex-col items-center justify-center text-center gap-4 min-h-[400px] border-dashed">
              <div className="w-16 h-16 rounded-2xl bg-gray-100 dark:bg-slate-700 flex items-center justify-center">
                <Leaf className="w-8 h-8 text-gray-300 dark:text-gray-600" />
              </div>
              <div>
                <p className="font-medium text-gray-400 dark:text-gray-500">AI Diagnosis Results</p>
                <p className="text-sm text-gray-300 dark:text-gray-600 mt-1">Upload a leaf image to see the full diagnosis</p>
              </div>
            </div>
          )}

          <AnimatePresence>
            {result && (
              <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="space-y-4">

                {/* ── Hero result card ── */}
                <div className="card p-5 border-l-4 border-l-brand-500">
                  <div className="flex items-start gap-4 mb-5">
                    {/* Uploaded image thumbnail */}
                    {result.image_url && (
                      <div className="w-20 h-20 rounded-xl overflow-hidden shrink-0 border border-gray-200 dark:border-slate-700 bg-gray-100">
                        <img src={result.image_url} alt="Analysed leaf" className="w-full h-full object-cover" />
                      </div>
                    )}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <Leaf className="w-3.5 h-3.5 text-brand-500" />
                        <span className="text-xs font-bold text-brand-600 dark:text-brand-400 uppercase tracking-wider">
                          {result.plant_name}
                        </span>
                        {result.is_demo && (
                          <span className="tag bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300">
                            Demo
                          </span>
                        )}
                      </div>
                      <h2 className="text-2xl font-extrabold text-gray-900 dark:text-white leading-tight">
                        {result.disease_name}
                      </h2>
                      <p className="text-sm text-gray-400 italic mt-0.5">{result.disease_info?.scientific_name}</p>
                    </div>
                    <div className="flex flex-col items-end gap-2 shrink-0">
                      <SeverityBadge severity={result.severity} />
                      {result.disease_info?.type && <TypeBadge type={result.disease_info.type} />}
                    </div>
                  </div>

                  {/* Confidence */}
                  <div className="mb-4">
                    <div className="flex items-center justify-between mb-1.5">
                      <span className="text-xs font-bold text-gray-500 uppercase tracking-wide">AI Confidence</span>
                      <span className={`text-base font-extrabold ${
                        result.confidence >= 0.85 ? 'text-green-600' :
                        result.confidence >= 0.70 ? 'text-yellow-600' :
                        result.confidence >= 0.50 ? 'text-orange-600' : 'text-red-500'
                      }`}>
                        {(result.confidence * 100).toFixed(1)}%
                      </span>
                    </div>
                    <ConfidenceBar confidence={result.confidence} />
                  </div>

                  {/* Low confidence warning */}
                  {result.low_confidence_warning && (
                    <div className="flex items-center gap-2 text-xs text-amber-700 dark:text-amber-400 bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-lg p-3 mb-4">
                      <AlertCircle className="w-3.5 h-3.5 shrink-0" />
                      <span>Low confidence prediction. Try a clearer, well-lit photo focused on a single leaf.</span>
                    </div>
                  )}

                  {/* Top-3 predictions */}
                  <div>
                    <h4 className="text-xs font-bold text-gray-400 uppercase tracking-wide mb-3">Top-3 Predictions</h4>
                    <div className="space-y-2.5">
                      {result.top3.map((t, i) => {
                        const pName = t.plant_name || t.label.split('___')[0]?.replace(/_/g, ' ');
                        const dName = t.disease_name || t.label.split('___')[1]?.replace(/_/g, ' ');
                        return (
                          <div key={i} className={`flex items-center gap-3 p-2.5 rounded-xl transition-colors ${
                            i === 0 ? 'bg-brand-50 dark:bg-brand-900/20 border border-brand-200/60 dark:border-brand-800/50' : ''
                          }`}>
                            <span className={`w-6 h-6 rounded-full text-xs font-bold flex items-center justify-center shrink-0 ${
                              i === 0 ? 'bg-brand-500 text-white' : 'bg-gray-100 dark:bg-slate-700 text-gray-500'
                            }`}>{i + 1}</span>
                            <div className="flex-1 min-w-0">
                              <p className="text-xs font-semibold text-gray-700 dark:text-gray-200 truncate">{dName}</p>
                              <p className="text-xs text-gray-400 truncate">{pName}</p>
                            </div>
                            <div className="flex items-center gap-2 shrink-0">
                              <span className="text-xs font-bold text-gray-600 dark:text-gray-300 w-10 text-right">
                                {(t.confidence * 100).toFixed(1)}%
                              </span>
                              <div className="w-20">
                                <ConfidenceBar confidence={t.confidence} />
                              </div>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </div>

                  {/* Model info */}
                  <div className="mt-4 pt-3 border-t border-gray-100 dark:border-slate-700 flex items-center gap-1.5 text-xs text-gray-400">
                    <Microscope className="w-3 h-3" />
                    <span>{result.model_used}</span>
                  </div>
                </div>

                {/* ── Grad-CAM section ── */}
                {hasGradcam && (
                  <Section title="Grad-CAM Visual Explanation" icon={Activity} iconColor="text-ai-500">
                    <div className="space-y-3">
                      {/* View switcher */}
                      <div className="flex items-center gap-2">
                        <span className="text-xs text-gray-400 mr-1">View:</span>
                        {[
                          { key: 'overlay', label: 'Overlay', icon: Eye },
                          { key: 'heatmap', label: 'Heatmap', icon: Activity },
                          { key: 'original', label: 'Original', icon: ImageIcon },
                        ].map(({ key, label, icon: Icon }) => (
                          <button key={key} onClick={() => setGradcamView(key as GradcamView)}
                            className={`flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                              gradcamView === key
                                ? 'bg-ai-500 text-white'
                                : 'bg-gray-100 dark:bg-slate-700 text-gray-600 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-slate-600'
                            }`}>
                            <Icon className="w-3 h-3" />
                            {label}
                          </button>
                        ))}
                        {result.is_demo && (
                          <span className="tag bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300 text-xs ml-auto">
                            Synthetic heatmap (demo)
                          </span>
                        )}
                      </div>

                      {/* Image display */}
                      {currentGradcam && (
                        <div className="rounded-xl overflow-hidden border border-gray-100 dark:border-slate-700">
                          <img src={currentGradcam} alt={`Grad-CAM ${gradcamView}`} className="w-full" />
                        </div>
                      )}

                      <div className="text-xs text-gray-400 dark:text-gray-500 space-y-1 bg-gray-50 dark:bg-slate-800/50 rounded-xl p-3">
                        <p><strong className="text-gray-500 dark:text-gray-400">What is this?</strong> Gradient-weighted Class Activation Mapping (Grad-CAM) shows which regions of the leaf influenced the prediction.</p>
                        <p><strong className="text-red-400">Red/warm areas</strong> = high AI attention. <strong className="text-blue-400">Blue/cool areas</strong> = low attention.</p>
                        <p className="italic">Method: Selvaraju et al. (2017). Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization. ICCV 2017.</p>
                      </div>
                    </div>
                  </Section>
                )}

                {/* ── Disease Information ── */}
                {result.disease_info && result.disease_name !== 'Healthy' && (
                  <Section title="Disease Information" icon={Info} iconColor="text-brand-500">
                    <div className="space-y-4 text-sm">
                      {/* Summary */}
                      <p className="text-gray-600 dark:text-gray-300 leading-relaxed">{result.disease_info.summary}</p>

                      {/* Symptoms */}
                      {result.disease_info.symptoms?.length > 0 && (
                        <div>
                          <h4 className="font-bold text-gray-900 dark:text-white mb-2 flex items-center gap-1.5">
                            <Eye className="w-3.5 h-3.5 text-amber-500" />
                            Symptoms
                          </h4>
                          <BulletList items={result.disease_info.symptoms} iconClass="text-amber-500" />
                        </div>
                      )}

                      {/* Cause */}
                      {result.disease_info.cause && result.disease_info.cause !== 'N/A' && (
                        <div>
                          <h4 className="font-bold text-gray-900 dark:text-white mb-1.5 flex items-center gap-1.5">
                            <Bug className="w-3.5 h-3.5 text-purple-500" />
                            Cause
                          </h4>
                          <p className="text-gray-500 dark:text-gray-400 leading-relaxed">{result.disease_info.cause}</p>
                        </div>
                      )}

                      {/* Effects */}
                      {result.disease_info.effects && result.disease_info.effects !== 'N/A' && (
                        <div>
                          <h4 className="font-bold text-gray-900 dark:text-white mb-1.5 flex items-center gap-1.5">
                            <Thermometer className="w-3.5 h-3.5 text-red-500" />
                            Effects
                          </h4>
                          <p className="text-gray-500 dark:text-gray-400 leading-relaxed">{result.disease_info.effects}</p>
                        </div>
                      )}

                      {/* Severity factors */}
                      {result.disease_info.severity_factors?.length > 0 && (
                        <div>
                          <h4 className="font-bold text-gray-900 dark:text-white mb-2 flex items-center gap-1.5">
                            <AlertTriangle className="w-3.5 h-3.5 text-orange-500" />
                            Risk Factors
                          </h4>
                          <BulletList items={result.disease_info.severity_factors} iconClass="text-orange-500" />
                        </div>
                      )}

                      {/* References */}
                      {result.disease_info.references?.length > 0 && (
                        <p className="text-xs text-gray-400 border-t border-gray-100 dark:border-slate-700 pt-3">
                          Sources: {result.disease_info.references.join(' · ')}
                        </p>
                      )}
                    </div>
                  </Section>
                )}

                {/* ── Immediate Actions ── */}
                {result.disease_info?.immediate_actions?.length > 0 && result.disease_name !== 'Healthy' && (
                  <Section title="Immediate Actions" icon={ShieldAlert} iconColor="text-red-500">
                    <div className="space-y-1">
                      <div className="text-xs text-red-600 dark:text-red-400 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg px-3 py-2 mb-3">
                        Act quickly to prevent spread to healthy plants.
                      </div>
                      <BulletList items={result.disease_info.immediate_actions} iconClass="text-red-500" />
                    </div>
                  </Section>
                )}

                {/* ── Prevention ── */}
                {result.disease_info?.prevention?.length > 0 && (
                  <Section title="Prevention & Cultural Management" icon={BookOpen} iconColor="text-green-500" defaultOpen={false}>
                    <div className="space-y-4">
                      <BulletList items={result.disease_info.prevention} iconClass="text-green-500" />
                      {result.disease_info.cultural_biological?.length > 0 && (
                        <div>
                          <h4 className="font-bold text-gray-900 dark:text-white mb-2 text-sm">Biological / Cultural Controls</h4>
                          <BulletList items={result.disease_info.cultural_biological} iconClass="text-teal-500" />
                        </div>
                      )}
                    </div>
                  </Section>
                )}

                {/* ── Treatment Guide ── */}
                {result.treatments?.length > 0 && (
                  <Section title="Treatment & Pesticide Guide" icon={FlaskConical} iconColor="text-ai-500" defaultOpen={false}>
                    <div className="space-y-5">
                      <div className="text-xs text-amber-700 dark:text-amber-400 bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-xl px-3 py-2">
                        ⚠️ <strong>Regulatory notice:</strong> Always consult the current registered product label in your country/region before applying any pesticide. Dosages, registration status, and pre-harvest intervals vary. Information is for educational purposes only.
                      </div>
                      {result.treatments.map((t, i) => (
                        <div key={i} className="border border-gray-100 dark:border-slate-700 rounded-xl overflow-hidden">
                          <div className="bg-gray-50 dark:bg-slate-800/60 px-4 py-3 flex items-start justify-between gap-2">
                            <div>
                              <span className="tag bg-ai-100 text-ai-700 dark:bg-ai-900/40 dark:text-ai-300 text-xs mb-1">
                                Option {i + 1}
                              </span>
                              <h4 className="font-bold text-gray-900 dark:text-white text-sm">{t.active_ingredient}</h4>
                              <p className="text-xs text-gray-400 italic mt-0.5">{t.product_example}</p>
                            </div>
                          </div>
                          <div className="p-4 space-y-3">
                            <InfoGrid items={[
                              ['Use for', t.use_for],
                              ['Rate', t.rate],
                              ['Preparation', t.preparation],
                              ['When to apply', t.when_to_apply],
                              ['Frequency', t.frequency],
                              ['Pre-harvest interval (PHI)', t.phi],
                            ]} />
                            {t.safety?.length > 0 && (
                              <div className="rounded-xl bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 p-3">
                                <div className="text-xs font-bold text-red-700 dark:text-red-400 mb-2">⚠ Safety Precautions</div>
                                <ul className="text-xs text-red-600 dark:text-red-300 space-y-1">
                                  {t.safety.map((s, si) => <li key={si} className="flex gap-1.5"><span>•</span>{s}</li>)}
                                </ul>
                              </div>
                            )}
                            <p className="text-xs text-gray-400 border-t border-gray-100 dark:border-slate-700 pt-2">
                              Source: {t.source}
                            </p>
                          </div>
                        </div>
                      ))}
                    </div>
                  </Section>
                )}

                {/* ── Products ── */}
                {result.products?.length > 0 && (
                  <Section title="Available Products" icon={ShoppingBag} iconColor="text-purple-500" defaultOpen={false}>
                    <div className="space-y-1">
                      <p className="text-xs text-gray-400 dark:text-gray-500 mb-3">
                        Product listing is informational only. Verify availability and registration in your region. Never fabricated links or price claims.
                      </p>
                      {result.products.map((p, i) => (
                        <div key={i} className="border border-gray-100 dark:border-slate-700 rounded-xl p-4">
                          <div className="flex items-start justify-between gap-2 mb-2">
                            <div>
                              <p className="font-semibold text-gray-900 dark:text-white text-sm">{p.product_name}</p>
                              <p className="text-xs text-gray-400 mt-0.5">{p.active_ingredient} · {p.manufacturer}</p>
                            </div>
                            <span className="tag bg-purple-100 text-purple-700 dark:bg-purple-900/40 dark:text-purple-300 text-xs shrink-0">{p.type}</span>
                          </div>
                          <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">{p.availability}</p>
                          <p className="text-xs text-brand-600 dark:text-brand-400 mt-1">{p.buy_link_note}</p>
                        </div>
                      ))}
                    </div>
                  </Section>
                )}

              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
}
