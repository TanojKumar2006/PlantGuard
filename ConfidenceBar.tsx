interface ConfidenceBarProps {
  confidence: number; // 0–1
  className?: string;
}

export default function ConfidenceBar({ confidence, className = '' }: ConfidenceBarProps) {
  const pct = Math.round(confidence * 100);
  const color = pct >= 80 ? 'from-brand-400 to-brand-500'
    : pct >= 60 ? 'from-yellow-400 to-orange-400'
    : 'from-red-400 to-red-500';

  return (
    <div className={`flex items-center gap-3 ${className}`}>
      <div className="flex-1 confidence-bar">
        <div
          className={`confidence-fill bg-gradient-to-r ${color}`}
          style={{ width: `${pct}%` }}
        />
      </div>
      <span className="text-sm font-semibold tabular-nums w-12 text-right text-gray-700 dark:text-gray-200">
        {pct}%
      </span>
    </div>
  );
}
