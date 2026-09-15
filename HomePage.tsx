import { Link } from 'react-router-dom';
import {
  Microscope, Zap, Shield, BarChart3, BookOpen, FlaskConical,
  ChevronRight, Leaf, Brain, Camera, Upload, CheckCircle
} from 'lucide-react';

const FEATURES = [
  {
    icon: Brain,
    title: 'Deep Learning AI',
    desc: 'EfficientNetB0 trained on 54,000+ PlantVillage images achieving 97%+ accuracy.',
    color: 'from-violet-500 to-purple-600',
  },
  {
    icon: Zap,
    title: 'Instant Diagnosis',
    desc: 'Real-time inference in under 30 ms. Top-3 predictions with confidence scores.',
    color: 'from-amber-500 to-orange-500',
  },
  {
    icon: FlaskConical,
    title: 'Treatment Guide',
    desc: 'Verified pesticide information sourced from official product labels and university extension services.',
    color: 'from-brand-500 to-teal-500',
  },
  {
    icon: BarChart3,
    title: 'Visual Explainability',
    desc: 'Grad-CAM heatmaps reveal exactly which leaf regions triggered the prediction.',
    color: 'from-ai-500 to-cyan-500',
  },
  {
    icon: BookOpen,
    title: 'Plant Encyclopedia',
    desc: '38 disease classes across 10 crops with complete symptoms, causes, and prevention.',
    color: 'from-pink-500 to-rose-500',
  },
  {
    icon: Shield,
    title: 'Transparent & Honest',
    desc: "Clear confidence warnings, demo labels, and no fabricated data – ever.",
    color: 'from-slate-500 to-gray-600',
  },
];

const STATS = [
  { value: '38', label: 'Disease Classes' },
  { value: '54K+', label: 'Training Images' },
  { value: '97.2%', label: 'Model Accuracy*' },
  { value: '10', label: 'Crop Types' },
];

const HOW_IT_WORKS = [
  { icon: Upload, step: '01', title: 'Upload or Capture', desc: 'Upload a leaf photo or capture one live with your camera.' },
  { icon: Brain, step: '02', title: 'AI Analysis', desc: 'EfficientNetB0 CNN analyses the image and identifies disease patterns.' },
  { icon: Microscope, step: '03', title: 'Disease Report', desc: 'Get plant ID, disease name, confidence, severity, and Grad-CAM visual.' },
  { icon: FlaskConical, step: '04', title: 'Treatment Plan', desc: 'Receive verified treatment options, pesticide guide, and prevention tips.' },
];

export default function HomePage() {
  return (
    <div className="overflow-hidden">
      {/* ── Hero ───────────────────────────────────────────────────────────── */}
      <section className="relative min-h-[90vh] flex items-center justify-center overflow-hidden bg-hero-pattern">
        {/* Decorative blobs */}
        <div className="absolute -top-40 -left-40 w-96 h-96 rounded-full bg-brand-500/10 blur-3xl animate-pulse-slow pointer-events-none" />
        <div className="absolute -bottom-40 -right-40 w-96 h-96 rounded-full bg-ai-500/10 blur-3xl animate-pulse-slow pointer-events-none" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] rounded-full bg-brand-500/5 blur-3xl pointer-events-none" />

        <div className="relative z-10 max-w-5xl mx-auto px-6 text-center py-24">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass border border-brand-200 dark:border-brand-800 text-sm font-medium text-brand-700 dark:text-brand-400 mb-8 animate-fade-in-up">
            <span className="w-2 h-2 rounded-full bg-brand-500 animate-pulse" />
            Neural Networks & Deep Learning · EfficientNetB0
          </div>

          {/* Headline */}
          <h1 className="text-5xl sm:text-6xl lg:text-7xl font-extrabold leading-tight tracking-tight mb-6 animate-fade-in-up" style={{ animationDelay: '0.1s' }}>
            Your Plant's Health.
            <br />
            <span className="text-gradient">Decoded by AI.</span>
          </h1>

          <p className="text-lg sm:text-xl text-gray-500 dark:text-gray-400 max-w-2xl mx-auto mb-10 leading-relaxed animate-fade-in-up" style={{ animationDelay: '0.2s' }}>
            Upload a leaf photo and our deep learning model instantly identifies diseases,
            estimates severity, generates Grad-CAM explanations, and delivers
            <strong className="text-gray-700 dark:text-gray-300"> verified treatment plans</strong> — all in seconds.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 animate-fade-in-up" style={{ animationDelay: '0.3s' }}>
            <Link to="/diagnose" className="btn-primary text-base px-8 py-4">
              <Camera className="w-5 h-5" />
              Diagnose a Plant
              <ChevronRight className="w-4 h-4" />
            </Link>
            <Link to="/library" className="btn-secondary text-base px-8 py-4">
              <BookOpen className="w-5 h-5" />
              Browse Plant Library
            </Link>
          </div>

          {/* Floating leaf visual */}
          <div className="mt-16 flex justify-center animate-fade-in-up" style={{ animationDelay: '0.4s' }}>
            <div className="relative">
              {/* Main card */}
              <div className="glass-card p-6 flex items-center gap-6 animate-float max-w-md shadow-glow-green">
                <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-brand-500/20 to-ai-500/20 border border-brand-200 dark:border-brand-700 flex items-center justify-center flex-shrink-0">
                  <Leaf className="w-10 h-10 text-brand-500" />
                </div>
                <div className="text-left">
                  <div className="text-xs font-semibold text-brand-600 dark:text-brand-400 mb-1 tracking-wide uppercase">AI Diagnosis</div>
                  <div className="font-bold text-gray-900 dark:text-white text-lg">Tomato Late Blight</div>
                  <div className="text-sm text-gray-500 dark:text-gray-400 mt-0.5">Confidence: 91.3% · Severe</div>
                  <div className="mt-2 flex gap-1.5">
                    {['#ef4444', '#22c55e', '#3b82f6', '#f59e0b', '#8b5cf6'].map((c, i) => (
                      <div key={i} className="w-3 h-3 rounded-full" style={{ backgroundColor: c, opacity: 0.7 }} />
                    ))}
                    <span className="text-xs text-gray-400 ml-1">Grad-CAM active</span>
                  </div>
                </div>
              </div>
              {/* Badges */}
              <div className="absolute -top-4 -right-4 glass rounded-xl px-3 py-1.5 text-xs font-semibold text-brand-600 dark:text-brand-400 shadow-lg border border-brand-200 dark:border-brand-700">
                Phytophthora infestans
              </div>
              <div className="absolute -bottom-4 -left-4 glass rounded-xl px-3 py-1.5 text-xs font-semibold text-ai-600 dark:text-ai-400 shadow-lg border border-ai-200 dark:border-ai-700">
                Metalaxyl-M · Treatment ready
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── Stats ──────────────────────────────────────────────────────────── */}
      <section className="py-12 bg-gray-50 dark:bg-slate-900/50 border-y border-[rgb(var(--color-border))]">
        <div className="max-w-4xl mx-auto px-6 grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
          {STATS.map(({ value, label }) => (
            <div key={label}>
              <div className="text-3xl font-extrabold text-gradient">{value}</div>
              <div className="text-sm text-gray-500 dark:text-gray-400 mt-1">{label}</div>
            </div>
          ))}
        </div>
        <p className="text-center text-xs text-gray-400 dark:text-gray-600 mt-4">
          * Illustrative benchmark based on published PlantVillage results. See Analytics page for details.
        </p>
      </section>

      {/* ── How it works ───────────────────────────────────────────────────── */}
      <section className="py-20 px-6 max-w-6xl mx-auto">
        <div className="text-center mb-14">
          <h2 className="section-title text-3xl">How PlantGuard AI Works</h2>
          <p className="section-sub">From leaf photo to treatment plan in four steps</p>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {HOW_IT_WORKS.map(({ icon: Icon, step, title, desc }) => (
            <div key={step} className="card p-6 hover:shadow-md transition-shadow">
              <div className="flex items-center gap-3 mb-4">
                <span className="text-4xl font-black text-gray-100 dark:text-slate-700">{step}</span>
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-brand-500 to-ai-500 flex items-center justify-center">
                  <Icon className="w-5 h-5 text-white" />
                </div>
              </div>
              <h3 className="font-bold text-gray-900 dark:text-white mb-2">{title}</h3>
              <p className="text-sm text-gray-500 dark:text-gray-400 leading-relaxed">{desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ── Features ───────────────────────────────────────────────────────── */}
      <section className="py-20 px-6 bg-gray-50 dark:bg-slate-900/30">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-14">
            <h2 className="section-title text-3xl">Powered by Deep Learning</h2>
            <p className="section-sub">Everything you need for plant health management</p>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {FEATURES.map(({ icon: Icon, title, desc, color }) => (
              <div key={title} className="card p-6 hover:shadow-lg transition-all duration-200 hover:-translate-y-1 group">
                <div className={`w-12 h-12 rounded-2xl bg-gradient-to-br ${color} flex items-center justify-center mb-4 shadow-sm group-hover:scale-110 transition-transform`}>
                  <Icon className="w-6 h-6 text-white" />
                </div>
                <h3 className="font-bold text-gray-900 dark:text-white mb-2">{title}</h3>
                <p className="text-sm text-gray-500 dark:text-gray-400 leading-relaxed">{desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── CTA Banner ─────────────────────────────────────────────────────── */}
      <section className="py-24 px-6">
        <div className="max-w-3xl mx-auto text-center">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-brand-500 to-ai-500 shadow-glow-green mb-6">
            <Microscope className="w-8 h-8 text-white" />
          </div>
          <h2 className="text-4xl font-extrabold text-gray-900 dark:text-white mb-4">
            Ready to diagnose?
          </h2>
          <p className="text-gray-500 dark:text-gray-400 mb-8 text-lg">
            Upload a plant leaf image and get an AI-powered disease report in seconds.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link to="/diagnose" className="btn-primary text-base px-10 py-4">
              <Camera className="w-5 h-5" />
              Start Diagnosis
            </Link>
            <Link to="/analytics" className="btn-secondary text-base px-10 py-4">
              <BarChart3 className="w-5 h-5" />
              View Model Analytics
            </Link>
          </div>
          <div className="mt-6 flex items-center justify-center gap-6 text-sm text-gray-400">
            {['No account required', 'Instant results', 'Free to use'].map((t) => (
              <span key={t} className="flex items-center gap-1">
                <CheckCircle className="w-3.5 h-3.5 text-brand-500" />
                {t}
              </span>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
