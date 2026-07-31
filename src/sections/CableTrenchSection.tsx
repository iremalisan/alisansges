import { FormField } from '../components/FormField';
import { NumericInput } from '../components/NumericInput';
import { SectionCard } from '../components/SectionCard';
import { formatSummaryNumber } from '../components/ResultSummaryCard';
import type {
  CableTrenchInput,
  TrenchRowSummary,
  TrenchType,
  ValidationErrors,
  ValidationFieldKey,
} from '../domain/types';
import { TRENCH_TYPES } from '../domain/types';
import { parseNonNegativeNumber } from '../domain/validation';

interface CableTrenchSectionProps {
  trenches: CableTrenchInput[];
  summaries: Record<string, TrenchRowSummary>;
  errors: ValidationErrors;
  onAdd: () => void;
  onUpdate: <K extends keyof CableTrenchInput>(
    id: string,
    key: K,
    value: CableTrenchInput[K],
  ) => void;
  onRemove: (id: string) => void;
  onDuplicate: (id: string) => void;
  onValidationChange: (field: ValidationFieldKey, message: string | null) => void;
}

export function CableTrenchSection({
  trenches,
  summaries,
  errors,
  onAdd,
  onUpdate,
  onRemove,
  onDuplicate,
  onValidationChange,
}: CableTrenchSectionProps) {
  return (
    <SectionCard
      id="cable-trench"
      title="Kablo Kanalı ve Kum"
      description="Birden fazla kanal satırı ekleyebilir; kazı, kum ve kablo sonuçları toplanır."
    >
      <div className="entry-toolbar">
        <button type="button" className="btn btn--secondary" onClick={onAdd}>
          Kanal Ekle
        </button>
      </div>

      {trenches.length === 0 ? (
        <p className="entry-empty">Henüz kanal yok. “Kanal Ekle” ile başlayın.</p>
      ) : (
        <div className="entry-list">
          {trenches.map((trench) => {
            const summary = summaries[trench.id];
            return (
              <article key={trench.id} className="entry-card">
                <div className="entry-card__header">
                  <FormField
                    label="Kanal adı"
                    htmlFor={`trench-name-${trench.id}`}
                  >
                    <input
                      id={`trench-name-${trench.id}`}
                      className="text-input"
                      value={trench.name}
                      onChange={(event) =>
                        onUpdate(trench.id, 'name', event.target.value)
                      }
                    />
                  </FormField>
                  <div className="entry-card__actions">
                    <button
                      type="button"
                      className="btn btn--ghost"
                      onClick={() => onDuplicate(trench.id)}
                    >
                      Kopyala
                    </button>
                    <button
                      type="button"
                      className="btn btn--ghost"
                      onClick={() => onRemove(trench.id)}
                    >
                      Sil
                    </button>
                  </div>
                </div>

                <div className="field-grid field-grid--dense">
                  <FormField label="Tip" htmlFor={`trench-type-${trench.id}`}>
                    <select
                      id={`trench-type-${trench.id}`}
                      className="select-input"
                      value={trench.type}
                      onChange={(event) =>
                        onUpdate(
                          trench.id,
                          'type',
                          event.target.value as TrenchType,
                        )
                      }
                    >
                      {TRENCH_TYPES.map((type) => (
                        <option key={type} value={type}>
                          {type}
                        </option>
                      ))}
                    </select>
                  </FormField>

                  {(
                    [
                      ['lengthM', 'Uzunluk', 'm'],
                      ['widthM', 'Genişlik', 'm'],
                      ['depthM', 'Derinlik', 'm'],
                      ['lowerSandHeightM', 'Alt kum yüksekliği', 'm'],
                      ['upperSandHeightM', 'Üst kum yüksekliği', 'm'],
                      ['sandWastePercent', 'Kum fire oranı', '%'],
                      ['cableLengthM', 'Kablo uzunluğu', 'm'],
                      ['cableWastePercent', 'Kablo fire oranı', '%'],
                      ['warningTapeRuns', 'Uyarı bandı hat sayısı', 'adet'],
                      [
                        'protectionPlateRuns',
                        'Koruma plakası hat sayısı',
                        'adet',
                      ],
                      ['conduitRuns', 'Boru / korruge hat sayısı', 'adet'],
                    ] as const
                  ).map(([key, label, unit]) => (
                    <FormField
                      key={key}
                      label={label}
                      htmlFor={`trench-${key}-${trench.id}`}
                    >
                      <NumericInput
                        id={`trench-${key}-${trench.id}`}
                        value={trench[key]}
                        unit={unit}
                        error={errors[`trench.${trench.id}.${key}`]}
                        onValueChange={(value) =>
                          onUpdate(trench.id, key, value)
                        }
                        onValidationChange={(message) =>
                          onValidationChange(
                            `trench.${trench.id}.${key}`,
                            message,
                          )
                        }
                        parseValue={parseNonNegativeNumber}
                      />
                    </FormField>
                  ))}
                </div>

                <div className="entry-summary" aria-label={`${trench.name} özet`}>
                  <span>
                    Kazı:{' '}
                    <strong>
                      {formatSummaryNumber(summary?.excavationM3 ?? null, 3)} m³
                    </strong>
                  </span>
                  <span>
                    Kum:{' '}
                    <strong>
                      {formatSummaryNumber(summary?.sandOrderM3 ?? null, 3)} m³
                    </strong>
                  </span>
                  <span>
                    Kablo:{' '}
                    <strong>
                      {formatSummaryNumber(summary?.cableOrderM ?? null, 3)} m
                    </strong>
                  </span>
                </div>
              </article>
            );
          })}
        </div>
      )}
    </SectionCard>
  );
}
