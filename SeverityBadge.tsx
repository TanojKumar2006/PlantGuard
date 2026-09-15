import clsx from 'clsx';

interface SeverityBadgeProps {
  severity: string;
}

export default function SeverityBadge({ severity }: SeverityBadgeProps) {
  const s = severity?.toLowerCase() ?? 'unknown';
  const classes: Record<string, string> = {
    none:      'severity-none',
    mild:      'severity-mild',
    moderate:  'severity-moderate',
    severe:    'severity-severe',
    uncertain: 'tag bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300',
  };
  return (
    <span className={clsx('tag', classes[s] ?? classes.uncertain)}>
      {severity}
    </span>
  );
}
