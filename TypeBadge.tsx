import clsx from 'clsx';

interface TypeBadgeProps {
  type: string;
}

export default function TypeBadge({ type }: TypeBadgeProps) {
  const t = type?.toLowerCase() ?? '';
  const cls = t.includes('fungal') ? 'type-fungal'
    : t.includes('bacterial') ? 'type-bacterial'
    : t.includes('viral') ? 'type-viral'
    : t.includes('pest') ? 'type-pest'
    : t.includes('healthy') ? 'type-healthy'
    : 'tag bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300';
  return <span className={clsx('tag', cls)}>{type}</span>;
}
