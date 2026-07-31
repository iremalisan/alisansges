import './ResultSummaryCard.css';

interface ResultSummaryCardProps {
  label: string;
  value: number | null;
  unit?: string;
}

function formatValue(value: number | null): string {
  if (value === null || value === undefined) {
    return '—';
  }

  return new Intl.NumberFormat('tr-TR', {
    maximumFractionDigits: 3,
  }).format(value);
}

export function ResultSummaryCard({ label, value, unit }: ResultSummaryCardProps) {
  return (
    <article className="result-summary-card" aria-label={label}>
      <p className="result-summary-card__label">{label}</p>
      <p className="result-summary-card__value">
        <span>{formatValue(value)}</span>
        {unit ? <span className="result-summary-card__unit">{unit}</span> : null}
      </p>
    </article>
  );
}
