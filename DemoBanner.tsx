import { AlertTriangle } from 'lucide-react';

interface DemoBannerProps {
  className?: string;
}

export default function DemoBanner({ className = '' }: DemoBannerProps) {
  return (
    <div className={`flex items-start gap-3 rounded-xl border border-amber-200 dark:border-amber-800 bg-amber-50 dark:bg-amber-900/20 p-4 text-sm text-amber-800 dark:text-amber-300 ${className}`}>
      <AlertTriangle className="w-4 h-4 mt-0.5 shrink-0" />
      <p>
        <strong>Demo Mode</strong> – The real EfficientNetB0 model weights are not loaded.
        This prediction is <strong>simulated for demonstration purposes</strong> and does not reflect actual analysis of the uploaded image.
        To enable real AI inference, train the model and place the weights at <code className="px-1 py-0.5 rounded bg-amber-100 dark:bg-amber-900">backend/model/plantguard_efficientnetb0.h5</code>.
      </p>
    </div>
  );
}
