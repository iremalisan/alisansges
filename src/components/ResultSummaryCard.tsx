import './ResultSummaryCard.css';

interface ResultSummaryCardProps {
  label: string;
  value: number | null;
  unit?: string;
  decimals?: number;
}

export function formatSummaryNumber(
  value: number | null,
  decimals = 0,
): string {
  if (value === null || value === undefined || !Number.isFinite(value)) {
    return '—';
  }

  return new Intl.NumberFormat('tr-TR', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  }).format(value);
}

export function ResultSummaryCard({
  label,
  value,
  unit,
  decimals = 0,
}: ResultSummaryCardProps) {
  return (
    <article className="result-summary-card" aria-label={label}>
      <p className="result-summary-card__label">{label}</p>
      <p className="result-summary-card__value">
        <span>{formatSummaryNumber(value, decimals)}</span>
        {unit ? <span className="result-summary-card__unit">{unit}</span> : null}
      </p>
    </article>
  );
}
