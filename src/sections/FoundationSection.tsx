import { FormField } from '../components/FormField';
import { NumericInput } from '../components/NumericInput';
import { SectionCard } from '../components/SectionCard';
import type {
  ConcreteFootMode,
  FoundationInputs,
  ValidationErrors,
} from '../domain/types';
import { parseNonNegativeNumber } from '../domain/validation';

interface FoundationSectionProps {
  values: FoundationInputs;
  errors: ValidationErrors;
  onChange: <K extends keyof FoundationInputs>(
    key: K,
    value: FoundationInputs[K],
  ) => void;
  onModeChange: (mode: ConcreteFootMode) => void;
  onValidationChange: (
    field: `foundation.${keyof FoundationInputs}`,
    message: string | null,
  ) => void;
}

export function FoundationSection({
  values,
  errors,
  onChange,
  onModeChange,
  onValidationChange,
}: FoundationSectionProps) {
  return (
    <SectionCard
      id="foundation"
      title="Ayak ve Beton"
      description="Betonlanacak ayak ve çukur ölçülerini girin."
    >
      <div className="field-grid">
        <FormField label="Beton ayak hesaplama modu" htmlFor="concrete-mode">
          <select
            id="concrete-mode"
            className="select-input"
            value={values.concreteFootMode}
            onChange={(event) =>
              onModeChange(event.target.value as ConcreteFootMode)
            }
          >
            <option value="count">Adet</option>
            <option value="percent">Yüzde</option>
          </select>
        </FormField>

        {values.concreteFootMode === 'count' ? (
          <FormField
            label="Betonlanacak ayak sayısı"
            htmlFor="concrete-legs-count"
          >
            <NumericInput
              id="concrete-legs-count"
              value={values.concreteLegsCount}
              unit="adet"
              error={errors['foundation.concreteLegsCount']}
              onValueChange={(value) => onChange('concreteLegsCount', value)}
              onValidationChange={(message) =>
                onValidationChange('foundation.concreteLegsCount', message)
              }
              parseValue={parseNonNegativeNumber}
            />
          </FormField>
        ) : (
          <FormField
            label="Betonlanacak ayak oranı"
            htmlFor="concrete-legs-percent"
          >
            <NumericInput
              id="concrete-legs-percent"
              value={values.concreteLegsPercent}
              unit="%"
              error={errors['foundation.concreteLegsPercent']}
              onValueChange={(value) => onChange('concreteLegsPercent', value)}
              onValidationChange={(message) =>
                onValidationChange('foundation.concreteLegsPercent', message)
              }
              parseValue={parseNonNegativeNumber}
            />
          </FormField>
        )}

        <FormField label="Çukur genişliği" htmlFor="pit-width">
          <NumericInput
            id="pit-width"
            value={values.pitWidthM}
            unit="m"
            error={errors['foundation.pitWidthM']}
            onValueChange={(value) => onChange('pitWidthM', value)}
            onValidationChange={(message) =>
              onValidationChange('foundation.pitWidthM', message)
            }
            parseValue={parseNonNegativeNumber}
          />
        </FormField>

        <FormField label="Çukur uzunluğu" htmlFor="pit-length">
          <NumericInput
            id="pit-length"
            value={values.pitLengthM}
            unit="m"
            error={errors['foundation.pitLengthM']}
            onValueChange={(value) => onChange('pitLengthM', value)}
            onValidationChange={(message) =>
              onValidationChange('foundation.pitLengthM', message)
            }
            parseValue={parseNonNegativeNumber}
          />
        </FormField>

        <FormField label="Çukur derinliği" htmlFor="pit-depth">
          <NumericInput
            id="pit-depth"
            value={values.pitDepthM}
            unit="m"
            error={errors['foundation.pitDepthM']}
            onValueChange={(value) => onChange('pitDepthM', value)}
            onValidationChange={(message) =>
              onValidationChange('foundation.pitDepthM', message)
            }
            parseValue={parseNonNegativeNumber}
          />
        </FormField>

        <FormField label="Beton fire oranı" htmlFor="concrete-waste">
          <NumericInput
            id="concrete-waste"
            value={values.concreteWastePercent}
            unit="%"
            error={errors['foundation.concreteWastePercent']}
            onValueChange={(value) => onChange('concreteWastePercent', value)}
            onValidationChange={(message) =>
              onValidationChange('foundation.concreteWastePercent', message)
            }
            parseValue={parseNonNegativeNumber}
          />
        </FormField>
      </div>
    </SectionCard>
  );
}
