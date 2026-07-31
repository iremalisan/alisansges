import { FormField } from '../components/FormField';
import { NumericInput } from '../components/NumericInput';
import { SectionCard } from '../components/SectionCard';
import { ValidationMessage } from '../components/ValidationMessage';
import { TABLE_RECIPES } from '../domain/recipes/tableRecipes';
import type { PanelTableInputs, ValidationErrors } from '../domain/types';
import { parseNonNegativeNumber } from '../domain/validation';

interface PanelTableSectionProps {
  values: PanelTableInputs;
  errors: ValidationErrors;
  onChange: <K extends keyof PanelTableInputs>(
    key: K,
    value: PanelTableInputs[K],
  ) => void;
  onSelectRecipe: (recipeId: string) => void;
  onValidationChange: (
    field: `panelTable.${keyof PanelTableInputs}`,
    message: string | null,
  ) => void;
}

export function PanelTableSection({
  values,
  errors,
  onChange,
  onSelectRecipe,
  onValidationChange,
}: PanelTableSectionProps) {
  return (
    <SectionCard
      id="panel-table"
      title="Panel ve Masa"
      description="Masa reçetesini seçin; panel ve ayak adetlerini gerekirse düzenleyin."
    >
      <p className="recipe-warning" role="note">
        Hazır reçeteler örnek başlangıç değerleridir. Gerçek proje standartlarınıza
        göre kontrol ediniz.
      </p>

      <div className="field-grid">
        <FormField label="Masa reçetesi" htmlFor="table-recipe">
          <select
            id="table-recipe"
            className="select-input"
            value={values.selectedTableRecipeId ?? ''}
            onChange={(event) => {
              if (event.target.value) {
                onSelectRecipe(event.target.value);
              } else {
                onChange('selectedTableRecipeId', null);
              }
            }}
          >
            <option value="">Reçete seçin</option>
            {TABLE_RECIPES.map((recipe) => (
              <option key={recipe.id} value={recipe.id}>
                {recipe.name}
              </option>
            ))}
          </select>
          <ValidationMessage
            message={errors['panelTable.selectedTableRecipeId']}
          />
        </FormField>

        <FormField label="Masa başına panel sayısı" htmlFor="panels-per-table">
          <NumericInput
            id="panels-per-table"
            value={values.panelsPerTable}
            unit="adet"
            error={errors['panelTable.panelsPerTable']}
            onValueChange={(value) => onChange('panelsPerTable', value)}
            onValidationChange={(message) =>
              onValidationChange('panelTable.panelsPerTable', message)
            }
            parseValue={parseNonNegativeNumber}
          />
        </FormField>

        <FormField label="Masa başına ayak sayısı" htmlFor="legs-per-table">
          <NumericInput
            id="legs-per-table"
            value={values.legsPerTable}
            unit="adet"
            error={errors['panelTable.legsPerTable']}
            onValueChange={(value) => onChange('legsPerTable', value)}
            onValidationChange={(message) =>
              onValidationChange('panelTable.legsPerTable', message)
            }
            parseValue={parseNonNegativeNumber}
          />
        </FormField>
      </div>
    </SectionCard>
  );
}
