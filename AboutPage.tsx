import { Info, Github, Leaf, Brain, Database, Code2, BookOpen, FlaskConical } from 'lucide-react';

const TECH = [
  { label: 'AI Model', value: 'EfficientNetB0 (TensorFlow/Keras)', icon: Brain },
  { label: 'Dataset', value: 'PlantVillage (38 classes, ~54K images)', icon: Database },
  { label: 'Backend', value: 'Python · FastAPI · SQLite (SQLAlchemy)', icon: Code2 },
  { label: 'Frontend', value: 'React 18 · TypeScript · Tailwind CSS', icon: Code2 },
  { label: 'Explainability', value: 'Grad-CAM (Selvaraju et al., 2017)', icon: Brain },
  { label: 'Disease KB', value: '38 classes with symptoms, causes, treatment', icon: BookOpen },
  { label: 'Treatment DB', value: 'University extension & official label sources', icon: FlaskConical },
];

const TEAM_NOTE = "This project is a Neural Networks & Deep Learning course mini-project demonstrating end-to-end AI application development.";

export default function AboutPage() {
  return (
    <div className="max-w-4xl mx-auto px-4 py-10">
      {/* Hero */}
      <div className="text-center mb-12">
        <div className="inline-flex items-center justify-center w-20 h-20 rounded-3xl bg-gradient-to-br from-brand-500 to-ai-500 shadow-glow-green mb-5">
          <Leaf className="w-10 h-10 text-white" />
        </div>
        <h1 className="text-4xl font-extrabold text-gray-900 dark:text-white mb-2">
          PlantGuard <span className="text-gradient">AI</span>
        </h1>
        <p className="text-lg text-gray-500 dark:text-gray-400 max-w-2xl mx-auto">
          AI-Based Plant Disease Detection & Treatment Assistant
        </p>
        <div className="flex items-center justify-center gap-2 mt-3">
          <span className="tag bg-brand-100 text-brand-700 dark:bg-brand-900/40 dark:text-brand-400">Neural Networks & Deep Learning</span>
          <span className="tag bg-ai-100 text-ai-700 dark:bg-ai-900/40 dark:text-ai-400">EfficientNetB0</span>
          <span className="tag bg-purple-100 text-purple-700 dark:bg-purple-900/40 dark:text-purple-400">Grad-CAM</span>
        </div>
      </div>

      {/* Description */}
      <div className="card p-6 mb-6">
        <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-3 flex items-center gap-2">
          <Info className="w-5 h-5 text-brand-500" />
          About This Project
        </h2>
        <div className="text-gray-600 dark:text-gray-300 space-y-3 leading-relaxed">
          <p>
            PlantGuard AI is a full-stack application for plant disease detection using
            Convolutional Neural Networks and Transfer Learning. It uses a fine-tuned
            <strong> EfficientNetB0</strong> model trained on the{' '}
            <strong>PlantVillage dataset</strong> (38 disease/healthy classes across 10 crops)
            to identify diseases from leaf images in real-time.
          </p>
          <p>
            Beyond classification, the system provides:
            <strong> Grad-CAM visualisations</strong> showing which leaf regions influenced
            the prediction, a comprehensive <strong>disease knowledge base</strong> with
            symptoms, causes, and management options, and a{' '}
            <strong>verified treatment guide</strong> sourced from university extension
            services and official product labels.
          </p>
          <p className="text-sm text-amber-700 dark:text-amber-400 bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-lg px-3 py-2">
            ⚠️ <strong>Academic Disclaimer:</strong> {TEAM_NOTE} Analytics metrics shown are
            illustrative benchmarks based on published PlantVillage results. Real model
            weights must be trained separately.
          </p>
        </div>
      </div>

      {/* Tech stack */}
      <div className="card p-6 mb-6">
        <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Technology Stack</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {TECH.map(({ label, value, icon: Icon }) => (
            <div key={label} className="flex items-start gap-3 p-3 rounded-xl bg-gray-50 dark:bg-slate-800/50">
              <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-brand-100 to-ai-100 dark:from-brand-900/30 dark:to-ai-900/30 flex items-center justify-center shrink-0">
                <Icon className="w-4 h-4 text-brand-600 dark:text-brand-400" />
              </div>
              <div>
                <div className="text-xs font-semibold text-gray-400 uppercase tracking-wide">{label}</div>
                <div className="text-sm text-gray-700 dark:text-gray-200 mt-0.5">{value}</div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Model architecture */}
      <div className="card p-6 mb-6">
        <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Model Architecture</h2>
        <div className="text-sm text-gray-600 dark:text-gray-300 space-y-2 leading-relaxed">
          <p><strong>Base model:</strong> EfficientNetB0 pretrained on ImageNet (5.3M parameters)</p>
          <p><strong>Fine-tuning:</strong> Global Average Pooling → Dense(256, ReLU) → Dropout(0.3) → Dense(38, Softmax)</p>
          <p><strong>Input:</strong> 224×224 RGB images, EfficientNet preprocessing</p>
          <p><strong>Training:</strong> Adam optimiser, learning rate 1e-4, batch size 32, 50 epochs with early stopping</p>
          <p><strong>Data augmentation:</strong> Random horizontal flip, rotation (±20°), zoom (±10%), brightness adjustment</p>
          <p><strong>Explainability:</strong> Gradient-weighted Class Activation Mapping (Grad-CAM) using the last convolutional layer</p>
          <p><strong>Demo mode:</strong> When trained weights are not present, the system runs in demo mode with synthetic predictions clearly labelled.</p>
        </div>
      </div>

      {/* Dataset & ethics */}
      <div className="card p-6 mb-6">
        <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Dataset & Ethics</h2>
        <div className="text-sm text-gray-600 dark:text-gray-300 space-y-2 leading-relaxed">
          <p>
            <strong>PlantVillage Dataset:</strong> Publicly available dataset of 54,306 images
            across 38 plant disease/healthy classes. Originally published by Hughes & Salathé (2015).
            Used under Creative Commons Attribution 4.0 licence.
          </p>
          <p>
            <strong>Treatment information:</strong> Pesticide guidance is sourced from published
            product labels, university cooperative extension services (Cornell, UF IFAS, Penn State, UC IPM,
            Purdue), and international organisations (FAO, CIP, INRAE). We do not fabricate dosages,
            prices, or safety claims.
          </p>
          <p>
            <strong>Limitations:</strong> The model was trained on laboratory images. Real-world performance
            may vary with image quality, lighting, and crop varieties not present in the training set.
            Always consult a qualified agronomist for professional diagnosis and treatment advice.
          </p>
        </div>
      </div>

      {/* References */}
      <div className="card p-6">
        <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Key References</h2>
        <ul className="text-sm text-gray-600 dark:text-gray-300 space-y-2">
          {[
            'Hughes, D.P., & Salathé, M. (2015). An open access repository of images on plant health to enable the development of mobile disease diagnostics. arXiv:1511.08060',
            'Tan, M., & Le, Q.V. (2019). EfficientNet: Rethinking model scaling for convolutional neural networks. ICML 2019.',
            'Selvaraju, R.R., et al. (2017). Grad-CAM: Visual explanations from deep networks via gradient-based localization. ICCV 2017.',
            'Mohanty, S.P., et al. (2016). Using deep learning for image-based plant disease detection. Frontiers in Plant Science.',
          ].map((ref, i) => (
            <li key={i} className="flex items-start gap-2">
              <span className="text-brand-500 font-bold shrink-0 mt-0.5">[{i + 1}]</span>
              <span>{ref}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
