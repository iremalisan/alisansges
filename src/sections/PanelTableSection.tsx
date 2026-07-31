import { FormField } from '../components/FormField';
import { NumericInput } from '../components/NumericInput';
import { SectionCard } from '../components/SectionCard';
import type { PanelTableInputs, ValidationErrors } from '../domain/types';
import { parseNonNegativeNumber } from '../domain/validation';

interface PanelTableSectionProps {
  values: PanelTableInputs;
  errors: ValidationErrors;
  onChange: <K extends keyof PanelTableInputs>(
    key: K,
    value: PanelTableInputs[K],
  ) => void;
  onValidationChange: (
    field: `panelTable.${keyof PanelTableInputs}`,
    message: string | null,
  ) => void;
}

export function PanelTableSection({
  values,
  errors,
  onChange,
  onValidationChange,
}: PanelTableSectionProps) {
  return (
    <SectionCard
      id="panel-table"
      title="Panel ve Masa"
      description="Masa başına panel ve ayak adetlerini tanımlayın."
    >
      <div className="field-grid">
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
