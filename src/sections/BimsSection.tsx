import { FormField } from '../components/FormField';
import { NumericInput } from '../components/NumericInput';
import { SectionCard } from '../components/SectionCard';
import type { BimsInputs, ValidationErrors } from '../domain/types';
import { parseNonNegativeNumber } from '../domain/validation';

interface BimsSectionProps {
  values: BimsInputs;
  errors: ValidationErrors;
  onChange: <K extends keyof BimsInputs>(key: K, value: BimsInputs[K]) => void;
  onValidationChange: (
    field: `bims.${keyof BimsInputs}`,
    message: string | null,
  ) => void;
}

export function BimsSection({
  values,
  errors,
  onChange,
  onValidationChange,
}: BimsSectionProps) {
  return (
    <SectionCard
      id="bims"
      title="Bims Duvar"
      description="Duvar ölçüleri ve bims boyutlarını girin."
    >
      <div className="field-grid">
        <FormField label="Duvar uzunluğu" htmlFor="wall-length">
          <NumericInput
            id="wall-length"
            value={values.wallLengthM}
            unit="m"
            error={errors['bims.wallLengthM']}
            onValueChange={(value) => onChange('wallLengthM', value)}
            onValidationChange={(message) =>
              onValidationChange('bims.wallLengthM', message)
            }
            parseValue={parseNonNegativeNumber}
          />
        </FormField>

        <FormField label="Duvar yüksekliği" htmlFor="wall-height">
          <NumericInput
            id="wall-height"
            value={values.wallHeightM}
            unit="m"
            error={errors['bims.wallHeightM']}
            onValueChange={(value) => onChange('wallHeightM', value)}
            onValidationChange={(message) =>
              onValidationChange('bims.wallHeightM', message)
            }
            parseValue={parseNonNegativeNumber}
          />
        </FormField>

        <FormField
          label="Kapı ve pencere boşluğu"
          htmlFor="opening-area"
        >
          <NumericInput
            id="opening-area"
            value={values.openingAreaM2}
            unit="m²"
            error={errors['bims.openingAreaM2']}
            onValueChange={(value) => onChange('openingAreaM2', value)}
            onValidationChange={(message) =>
              onValidationChange('bims.openingAreaM2', message)
            }
            parseValue={parseNonNegativeNumber}
          />
        </FormField>

        <FormField label="Bims genişliği" htmlFor="bims-width">
          <NumericInput
            id="bims-width"
            value={values.bimsWidthM}
            unit="m"
            error={errors['bims.bimsWidthM']}
            onValueChange={(value) => onChange('bimsWidthM', value)}
            onValidationChange={(message) =>
              onValidationChange('bims.bimsWidthM', message)
            }
            parseValue={parseNonNegativeNumber}
          />
        </FormField>

        <FormField label="Bims yüksekliği" htmlFor="bims-height">
          <NumericInput
            id="bims-height"
            value={values.bimsHeightM}
            unit="m"
            error={errors['bims.bimsHeightM']}
            onValueChange={(value) => onChange('bimsHeightM', value)}
            onValidationChange={(message) =>
              onValidationChange('bims.bimsHeightM', message)
            }
            parseValue={parseNonNegativeNumber}
          />
        </FormField>

        <FormField label="Bims fire oranı" htmlFor="bims-waste">
          <NumericInput
            id="bims-waste"
            value={values.bimsWastePercent}
            unit="%"
            error={errors['bims.bimsWastePercent']}
            onValueChange={(value) => onChange('bimsWastePercent', value)}
            onValidationChange={(message) =>
              onValidationChange('bims.bimsWastePercent', message)
            }
            parseValue={parseNonNegativeNumber}
          />
        </FormField>
      </div>
    </SectionCard>
  );
}
