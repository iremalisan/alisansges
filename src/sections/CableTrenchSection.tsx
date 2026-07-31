import { FormField } from '../components/FormField';
import { NumericInput } from '../components/NumericInput';
import { SectionCard } from '../components/SectionCard';
import type { CableTrenchInputs, ValidationErrors } from '../domain/types';
import { parseNonNegativeNumber } from '../domain/validation';

interface CableTrenchSectionProps {
  values: CableTrenchInputs;
  errors: ValidationErrors;
  onChange: <K extends keyof CableTrenchInputs>(
    key: K,
    value: CableTrenchInputs[K],
  ) => void;
  onValidationChange: (
    field: `cableTrench.${keyof CableTrenchInputs}`,
    message: string | null,
  ) => void;
}

export function CableTrenchSection({
  values,
  errors,
  onChange,
  onValidationChange,
}: CableTrenchSectionProps) {
  return (
    <SectionCard
      id="cable-trench"
      title="Kablo Kanalı ve Kum"
      description="Kanal ölçüleri ve kum yüksekliğini girin."
    >
      <div className="field-grid">
        <FormField label="Kanal uzunluğu" htmlFor="trench-length">
          <NumericInput
            id="trench-length"
            value={values.trenchLengthM}
            unit="m"
            error={errors['cableTrench.trenchLengthM']}
            onValueChange={(value) => onChange('trenchLengthM', value)}
            onValidationChange={(message) =>
              onValidationChange('cableTrench.trenchLengthM', message)
            }
            parseValue={parseNonNegativeNumber}
          />
        </FormField>

        <FormField label="Kanal genişliği" htmlFor="trench-width">
          <NumericInput
            id="trench-width"
            value={values.trenchWidthM}
            unit="m"
            error={errors['cableTrench.trenchWidthM']}
            onValueChange={(value) => onChange('trenchWidthM', value)}
            onValidationChange={(message) =>
              onValidationChange('cableTrench.trenchWidthM', message)
            }
            parseValue={parseNonNegativeNumber}
          />
        </FormField>

        <FormField label="Kum yüksekliği" htmlFor="sand-height">
          <NumericInput
            id="sand-height"
            value={values.sandHeightM}
            unit="m"
            error={errors['cableTrench.sandHeightM']}
            onValueChange={(value) => onChange('sandHeightM', value)}
            onValidationChange={(message) =>
              onValidationChange('cableTrench.sandHeightM', message)
            }
            parseValue={parseNonNegativeNumber}
          />
        </FormField>

        <FormField label="Kum fire oranı" htmlFor="sand-waste">
          <NumericInput
            id="sand-waste"
            value={values.sandWastePercent}
            unit="%"
            error={errors['cableTrench.sandWastePercent']}
            onValueChange={(value) => onChange('sandWastePercent', value)}
            onValidationChange={(message) =>
              onValidationChange('cableTrench.sandWastePercent', message)
            }
            parseValue={parseNonNegativeNumber}
          />
        </FormField>
      </div>
    </SectionCard>
  );
}
