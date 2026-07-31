import { FormField } from '../components/FormField';
import { NumericInput } from '../components/NumericInput';
import { SectionCard } from '../components/SectionCard';
import { ValidationMessage } from '../components/ValidationMessage';
import type { ProjectInputs, ValidationErrors } from '../domain/types';
import { parseNonNegativeNumber } from '../domain/validation';

interface ProjectSectionProps {
  values: ProjectInputs;
  errors: ValidationErrors;
  onChange: <K extends keyof ProjectInputs>(key: K, value: ProjectInputs[K]) => void;
  onValidationChange: (field: keyof ProjectInputs, message: string | null) => void;
}

export function ProjectSection({
  values,
  errors,
  onChange,
  onValidationChange,
}: ProjectSectionProps) {
  return (
    <SectionCard
      id="project"
      title="Proje Bilgileri"
      description="Santral ve panel temel bilgilerini girin."
    >
      <div className="field-grid">
        <FormField label="Proje adı" htmlFor="project-name">
          <input
            id="project-name"
            className="text-input"
            type="text"
            value={values.projectName}
            onChange={(event) => onChange('projectName', event.target.value)}
            autoComplete="off"
          />
        </FormField>

        <FormField label="Santral gücü" htmlFor="plant-power">
          <NumericInput
            id="plant-power"
            value={values.plantPowerMWp}
            unit="MWp"
            error={errors.plantPowerMWp}
            onValueChange={(value) => onChange('plantPowerMWp', value)}
            onValidationChange={(message) =>
              onValidationChange('plantPowerMWp', message)
            }
            parseValue={parseNonNegativeNumber}
          />
        </FormField>

        <FormField label="Panel gücü" htmlFor="panel-power">
          <NumericInput
            id="panel-power"
            value={values.panelPowerWp}
            unit="Wp"
            error={errors.panelPowerWp}
            onValueChange={(value) => onChange('panelPowerWp', value)}
            onValidationChange={(message) =>
              onValidationChange('panelPowerWp', message)
            }
            parseValue={parseNonNegativeNumber}
          />
        </FormField>

        <FormField label="Genel fire oranı" htmlFor="general-waste">
          <NumericInput
            id="general-waste"
            value={values.generalWastePercent}
            unit="%"
            error={errors.generalWastePercent}
            onValueChange={(value) => onChange('generalWastePercent', value)}
            onValidationChange={(message) =>
              onValidationChange('generalWastePercent', message)
            }
            parseValue={parseNonNegativeNumber}
          />
        </FormField>
      </div>
      <ValidationMessage message={errors.projectName} />
    </SectionCard>
  );
}
