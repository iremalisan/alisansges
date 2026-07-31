import { FormField } from '../components/FormField';
import { NumericInput } from '../components/NumericInput';
import { SectionCard } from '../components/SectionCard';
import { formatSummaryNumber } from '../components/ResultSummaryCard';
import type {
  ValidationErrors,
  ValidationFieldKey,
  WallInput,
  WallRowSummary,
} from '../domain/types';
import { parseNonNegativeNumber } from '../domain/validation';

interface BimsSectionProps {
  walls: WallInput[];
  summaries: Record<string, WallRowSummary>;
  errors: ValidationErrors;
  onAdd: () => void;
  onUpdate: <K extends keyof WallInput>(
    id: string,
    key: K,
    value: WallInput[K],
  ) => void;
  onRemove: (id: string) => void;
  onDuplicate: (id: string) => void;
  onValidationChange: (field: ValidationFieldKey, message: string | null) => void;
}

export function BimsSection({
  walls,
  summaries,
  errors,
  onAdd,
  onUpdate,
  onRemove,
  onDuplicate,
  onValidationChange,
}: BimsSectionProps) {
  return (
    <SectionCard
      id="bims"
      title="Bims Duvar"
      description="Birden fazla yapı/duvar satırı ekleyin; bims sonuçları köşk reçetesiyle birleşir."
    >
      <div className="entry-toolbar">
        <button type="button" className="btn btn--secondary" onClick={onAdd}>
          Yapı/Duvar Ekle
        </button>
      </div>

      {walls.length === 0 ? (
        <p className="entry-empty">
          Henüz duvar yok. “Yapı/Duvar Ekle” ile başlayın.
        </p>
      ) : (
        <div className="entry-list">
          {walls.map((wall) => {
            const summary = summaries[wall.id];
            return (
              <article key={wall.id} className="entry-card">
                <div className="entry-card__header">
                  <FormField label="Yapı / duvar adı" htmlFor={`wall-name-${wall.id}`}>
                    <input
                      id={`wall-name-${wall.id}`}
                      className="text-input"
                      value={wall.name}
                      onChange={(event) =>
                        onUpdate(wall.id, 'name', event.target.value)
                      }
                    />
                  </FormField>
                  <div className="entry-card__actions">
                    <button
                      type="button"
                      className="btn btn--ghost"
                      onClick={() => onDuplicate(wall.id)}
                    >
                      Kopyala
                    </button>
                    <button
                      type="button"
                      className="btn btn--ghost"
                      onClick={() => onRemove(wall.id)}
                    >
                      Sil
                    </button>
                  </div>
                </div>

                <div className="field-grid field-grid--dense">
                  {(
                    [
                      ['lengthM', 'Duvar uzunluğu', 'm'],
                      ['heightM', 'Duvar yüksekliği', 'm'],
                      ['openingAreaM2', 'Kapı ve pencere boşluğu', 'm²'],
                      ['bimsWidthM', 'Bims genişliği', 'm'],
                      ['bimsHeightM', 'Bims yüksekliği', 'm'],
                      ['bimsWastePercent', 'Bims fire oranı', '%'],
                    ] as const
                  ).map(([key, label, unit]) => (
                    <FormField
                      key={key}
                      label={label}
                      htmlFor={`wall-${key}-${wall.id}`}
                    >
                      <NumericInput
                        id={`wall-${key}-${wall.id}`}
                        value={wall[key]}
                        unit={unit}
                        error={errors[`wall.${wall.id}.${key}`]}
                        onValueChange={(value) =>
                          onUpdate(wall.id, key, value)
                        }
                        onValidationChange={(message) =>
                          onValidationChange(
                            `wall.${wall.id}.${key}`,
                            message,
                          )
                        }
                        parseValue={parseNonNegativeNumber}
                      />
                    </FormField>
                  ))}
                </div>

                <div className="entry-summary" aria-label={`${wall.name} özet`}>
                  <span>
                    Brüt alan:{' '}
                    <strong>
                      {formatSummaryNumber(summary?.grossAreaM2 ?? null, 3)} m²
                    </strong>
                  </span>
                  <span>
                    Net alan:{' '}
                    <strong>
                      {formatSummaryNumber(summary?.netAreaM2 ?? null, 3)} m²
                    </strong>
                  </span>
                  <span>
                    Sipariş bims:{' '}
                    <strong>
                      {formatSummaryNumber(summary?.orderBimsCount ?? null, 0)}{' '}
                      adet
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
