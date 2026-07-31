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
      description="Özet kartlar ve malzeme tablosu. Hesaplama motoru sonraki adımda eklenecek."
    >
      <p className="engine-notice" role="status">
        Hesaplama motoru sonraki adımda eklenecek.
      </p>

      <div className="summary-grid" aria-label="Özet sonuçlar">
        <ResultSummaryCard label="Panel" value={summary.panel} unit="adet" />
        <ResultSummaryCard label="Masa" value={summary.table} unit="adet" />
        <ResultSummaryCard
          label="Toplam Ayak"
          value={summary.totalLegs}
          unit="adet"
        />
        <ResultSummaryCard label="Beton" value={summary.concrete} unit="m³" />
        <ResultSummaryCard label="Kum" value={summary.sand} unit="m³" />
        <ResultSummaryCard label="Bims" value={summary.bims} unit="adet" />
      </div>

      <MaterialResultTable rows={rows} />
    </SectionCard>
  );
}
