import { FormField } from '../components/FormField';
import { NumericInput } from '../components/NumericInput';
import { SectionCard } from '../components/SectionCard';
import { ValidationMessage } from '../components/ValidationMessage';
import { KIOSK_RECIPES } from '../domain/recipes/kioskRecipes';
import type { KioskInputs, ValidationErrors } from '../domain/types';
import { parseNonNegativeNumber } from '../domain/validation';

interface KioskSectionProps {
  values: KioskInputs;
  errors: ValidationErrors;
  onChange: <K extends keyof KioskInputs>(key: K, value: KioskInputs[K]) => void;
  onSelectRecipe: (recipeId: string) => void;
  onValidationChange: (
    field: `kiosk.${keyof KioskInputs}`,
    message: string | null,
  ) => void;
}

export function KioskSection({
  values,
  errors,
  onChange,
  onSelectRecipe,
  onValidationChange,
}: KioskSectionProps) {
  return (
    <SectionCard
      id="kiosk"
      title="Beton Köşk ve Bakır Pabuç"
      description="Köşk reçetesini seçin; köşk adedi ve birim miktarları düzenlenebilir."
    >
      <p className="recipe-warning" role="note">
        Hazır reçeteler örnek başlangıç değerleridir. Gerçek proje standartlarınıza
        göre kontrol ediniz.
      </p>

      <div className="field-grid">
        <FormField label="Köşk reçetesi" htmlFor="kiosk-recipe">
          <select
            id="kiosk-recipe"
            className="select-input"
            value={values.selectedKioskRecipeId ?? ''}
            onChange={(event) => {
              if (event.target.value) {
                onSelectRecipe(event.target.value);
              } else {
                onChange('selectedKioskRecipeId', null);
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
          <ValidationMessage message={errors['kiosk.selectedKioskRecipeId']} />
        </FormField>

        <FormField label="Beton köşk adedi" htmlFor="kiosk-count">
          <NumericInput
            id="kiosk-count"
            value={values.kioskCount}
            unit="adet"
            error={errors['kiosk.kioskCount']}
            onValueChange={(value) => onChange('kioskCount', value)}
            onValidationChange={(message) =>
              onValidationChange('kiosk.kioskCount', message)
            }
            parseValue={parseNonNegativeNumber}
          />
        </FormField>

        <FormField
          label="Köşk başına OG bakır pabuç"
          htmlFor="og-copper-lugs"
        >
          <NumericInput
            id="og-copper-lugs"
            value={values.ogCopperLugsPerKiosk}
            unit="adet"
            error={errors['kiosk.ogCopperLugsPerKiosk']}
            onValueChange={(value) => onChange('ogCopperLugsPerKiosk', value)}
            onValidationChange={(message) =>
              onValidationChange('kiosk.ogCopperLugsPerKiosk', message)
            }
            parseValue={parseNonNegativeNumber}
          />
        </FormField>

        <FormField
          label="Köşk başına AG bakır pabuç"
          htmlFor="ag-copper-lugs"
        >
          <NumericInput
            id="ag-copper-lugs"
            value={values.agCopperLugsPerKiosk}
            unit="adet"
            error={errors['kiosk.agCopperLugsPerKiosk']}
            onValueChange={(value) => onChange('agCopperLugsPerKiosk', value)}
            onValidationChange={(message) =>
              onValidationChange('kiosk.agCopperLugsPerKiosk', message)
            }
            parseValue={parseNonNegativeNumber}
          />
        </FormField>

        <FormField
          label="Köşk başına topraklama pabucu"
          htmlFor="grounding-lugs"
        >
          <NumericInput
            id="grounding-lugs"
            value={values.groundingLugsPerKiosk}
            unit="adet"
            error={errors['kiosk.groundingLugsPerKiosk']}
            onValueChange={(value) => onChange('groundingLugsPerKiosk', value)}
            onValidationChange={(message) =>
              onValidationChange('kiosk.groundingLugsPerKiosk', message)
            }
            parseValue={parseNonNegativeNumber}
          />
        </FormField>

        <FormField label="Köşk başına kablo rakoru" htmlFor="cable-glands">
          <NumericInput
            id="cable-glands"
            value={values.cableGlandsPerKiosk}
            unit="adet"
            error={errors['kiosk.cableGlandsPerKiosk']}
            onValueChange={(value) => onChange('cableGlandsPerKiosk', value)}
            onValidationChange={(message) =>
              onValidationChange('kiosk.cableGlandsPerKiosk', message)
            }
            parseValue={parseNonNegativeNumber}
          />
        </FormField>

        <FormField label="Köşk başına bims" htmlFor="kiosk-bims">
          <NumericInput
            id="kiosk-bims"
            value={values.bimsBlocksPerKiosk}
            unit="adet"
            error={errors['kiosk.bimsBlocksPerKiosk']}
            onValueChange={(value) => onChange('bimsBlocksPerKiosk', value)}
            onValidationChange={(message) =>
              onValidationChange('kiosk.bimsBlocksPerKiosk', message)
            }
            parseValue={parseNonNegativeNumber}
          />
        </FormField>
      </div>
    </SectionCard>
  );
}
