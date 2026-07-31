import { FormField } from '../components/FormField';
import { NumericInput } from '../components/NumericInput';
import { SectionCard } from '../components/SectionCard';
import { ValidationMessage } from '../components/ValidationMessage';
import { KIOSK_RECIPES } from '../domain/recipes/kioskRecipes';
import type {
  KioskGroupInput,
  ValidationErrors,
  ValidationFieldKey,
} from '../domain/types';
import { parseNonNegativeNumber } from '../domain/validation';

interface KioskSectionProps {
  groups: KioskGroupInput[];
  errors: ValidationErrors;
  onAdd: () => void;
  onUpdate: <K extends keyof KioskGroupInput>(
    id: string,
    key: K,
    value: KioskGroupInput[K],
  ) => void;
  onSelectRecipe: (id: string, recipeId: string) => void;
  onRemove: (id: string) => void;
  onDuplicate: (id: string) => void;
  onValidationChange: (field: ValidationFieldKey, message: string | null) => void;
}

export function KioskSection({
  groups,
  errors,
  onAdd,
  onUpdate,
  onSelectRecipe,
  onRemove,
  onDuplicate,
  onValidationChange,
}: KioskSectionProps) {
  return (
    <SectionCard
      id="kiosk"
      title="Beton Köşk ve Bakır Pabuç"
      description="Birden fazla köşk grubu tanımlayın; aynı malzemeler tek satırda birleşir."
    >
      <p className="recipe-warning" role="note">
        Hazır reçeteler örnek başlangıç değerleridir. Gerçek proje standartlarınıza
        göre kontrol ediniz.
      </p>

      <div className="entry-toolbar">
        <button type="button" className="btn btn--secondary" onClick={onAdd}>
          Köşk Grubu Ekle
        </button>
      </div>

      {groups.length === 0 ? (
        <p className="entry-empty">
          Henüz köşk grubu yok. “Köşk Grubu Ekle” ile başlayın.
        </p>
      ) : (
        <div className="entry-list">
          {groups.map((group) => (
            <article key={group.id} className="entry-card">
              <div className="entry-card__header">
                <FormField
                  label="Grup adı"
                  htmlFor={`kiosk-name-${group.id}`}
                >
                  <input
                    id={`kiosk-name-${group.id}`}
                    className="text-input"
                    value={group.name}
                    onChange={(event) =>
                      onUpdate(group.id, 'name', event.target.value)
                    }
                  />
                </FormField>
                <div className="entry-card__actions">
                  <button
                    type="button"
                    className="btn btn--ghost"
                    onClick={() => onDuplicate(group.id)}
                  >
                    Kopyala
                  </button>
                  <button
                    type="button"
                    className="btn btn--ghost"
                    onClick={() => onRemove(group.id)}
                  >
                    Sil
                  </button>
                </div>
              </div>

              <div className="field-grid field-grid--dense">
                <FormField
                  label="Köşk reçetesi"
                  htmlFor={`kiosk-recipe-${group.id}`}
                >
                  <select
                    id={`kiosk-recipe-${group.id}`}
                    className="select-input"
                    value={group.recipeId ?? ''}
                    onChange={(event) => {
                      if (event.target.value) {
                        onSelectRecipe(group.id, event.target.value);
                      } else {
                        onUpdate(group.id, 'recipeId', null);
                      }
                    }}
                  >
                    <option value="">Reçete seçin</option>
                    {KIOSK_RECIPES.map((recipe) => (
                      <option key={recipe.id} value={recipe.id}>
                        {recipe.name}
                      </option>
                    ))}
                  </select>
                  <ValidationMessage
                    message={errors[`kioskGroup.${group.id}.recipeId`]}
                  />
                </FormField>

                <FormField
                  label="Köşk adedi"
                  htmlFor={`kiosk-count-${group.id}`}
                >
                  <NumericInput
                    id={`kiosk-count-${group.id}`}
                    value={group.count}
                    unit="adet"
                    error={errors[`kioskGroup.${group.id}.count`]}
                    onValueChange={(value) =>
                      onUpdate(group.id, 'count', value)
                    }
                    onValidationChange={(message) =>
                      onValidationChange(
                        `kioskGroup.${group.id}.count`,
                        message,
                      )
                    }
                    parseValue={parseNonNegativeNumber}
                  />
                </FormField>

                {(
                  [
                    ['ogCopperLugPerKiosk', 'OG bakır pabuç / köşk'],
                    ['agCopperLugPerKiosk', 'AG bakır pabuç / köşk'],
                    ['groundingLugPerKiosk', 'Topraklama pabucu / köşk'],
                    ['cableGlandPerKiosk', 'Kablo rakoru / köşk'],
                    ['bimsBlockPerKiosk', 'Bims / köşk'],
                  ] as const
                ).map(([key, label]) => (
                  <FormField
                    key={key}
                    label={label}
                    htmlFor={`kiosk-${key}-${group.id}`}
                  >
                    <NumericInput
                      id={`kiosk-${key}-${group.id}`}
                      value={group[key]}
                      unit="adet"
                      error={errors[`kioskGroup.${group.id}.${key}`]}
                      onValueChange={(value) =>
                        onUpdate(group.id, key, value)
                      }
                      onValidationChange={(message) =>
                        onValidationChange(
                          `kioskGroup.${group.id}.${key}`,
                          message,
                        )
                      }
                      parseValue={parseNonNegativeNumber}
                    />
                  </FormField>
                ))}
              </div>
            </article>
          ))}
        </div>
      )}
    </SectionCard>
  );
}
