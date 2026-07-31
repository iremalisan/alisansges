import { MaterialResultTable } from '../components/MaterialResultTable';
import { ResultSummaryCard } from '../components/ResultSummaryCard';
import { SectionCard } from '../components/SectionCard';
import type { MaterialResultRow, SummaryValues } from '../domain/types';

interface MaterialsSectionProps {
  summary: SummaryValues;
  rows: MaterialResultRow[];
}

export function MaterialsSection({ summary, rows }: MaterialsSectionProps) {
  return (
    <SectionCard
      id="materials"
      title="Malzeme Listesi"
      description="Canlı özet kartlar ve birleştirilmiş malzeme sonuçları."
    >
      <div className="summary-grid" aria-label="Özet sonuçlar">
        <ResultSummaryCard
          label="Panel"
          value={summary.panel}
          unit="adet"
          decimals={0}
        />
        <ResultSummaryCard
          label="Masa"
          value={summary.table}
          unit="adet"
          decimals={0}
        />
        <ResultSummaryCard
          label="Toplam Ayak"
          value={summary.totalLegs}
          unit="adet"
          decimals={0}
        />
        <ResultSummaryCard
          label="Beton"
          value={summary.concrete}
          unit="m³"
          decimals={3}
        />
        <ResultSummaryCard
          label="Kum"
          value={summary.sand}
          unit="m³"
          decimals={3}
        />
        <ResultSummaryCard
          label="Bims"
          value={summary.bims}
          unit="adet"
          decimals={0}
        />
      </div>

      <MaterialResultTable rows={rows} />
    </SectionCard>
  );
}
