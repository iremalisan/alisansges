import { FormField } from '../components/FormField';
import { NumericInput } from '../components/NumericInput';
import { SectionCard } from '../components/SectionCard';
import type { KioskInputs, ValidationErrors } from '../domain/types';
import { parseNonNegativeNumber } from '../domain/validation';

interface KioskSectionProps {
  values: KioskInputs;
  errors: ValidationErrors;
  onChange: <K extends keyof KioskInputs>(key: K, value: KioskInputs[K]) => void;
  onValidationChange: (
    field: `kiosk.${keyof KioskInputs}`,
    message: string | null,
  ) => void;
}

export function KioskSection({
  values,
  errors,
  onChange,
  onValidationChange,
}: KioskSectionProps) {
  return (
    <SectionCard
      id="kiosk"
      title="Beton Köşk ve Bakır Pabuç"
      description="Köşk adedi ve pabuç miktarlarını girin."
    >
      <div className="field-grid">
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
      </div>
    </SectionCard>
  );
}
