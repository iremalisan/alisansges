import { useEffect, useState, type ChangeEvent } from 'react';
import { UnitLabel } from './UnitLabel';
import { ValidationMessage } from './ValidationMessage';
import './NumericInput.css';

interface NumericInputProps {
  id: string;
  value: number | null;
  unit?: string;
  error?: string;
  step?: string;
  disabled?: boolean;
  'aria-label'?: string;
  onValueChange: (value: number | null) => void;
  onValidationChange: (message: string | null) => void;
  parseValue: (raw: string) => { value: number | null; error: string | null };
}

function toDisplay(value: number | null): string {
  return value === null || value === undefined ? '' : String(value);
}

export function NumericInput({
  id,
  value,
  unit,
  error,
  step = 'any',
  disabled = false,
  'aria-label': ariaLabel,
  onValueChange,
  onValidationChange,
  parseValue,
}: NumericInputProps) {
  const [draft, setDraft] = useState(() => toDisplay(value));
  const describedBy = error ? `${id}-error` : undefined;

  useEffect(() => {
    setDraft(toDisplay(value));
  }, [value]);

  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    const raw = event.target.value;

    if (raw.trim() === '') {
      setDraft('');
      onValueChange(null);
      onValidationChange(null);
      return;
    }

    // Allow in-progress decimal typing (e.g. "0." or ",") without clearing.
    if (/^\d+[.,]$/.test(raw.trim())) {
      setDraft(raw);
      onValidationChange(null);
      return;
    }

    const result = parseValue(raw);

    if (result.error) {
      // Do not accept invalid/negative values into the field or state.
      setDraft(toDisplay(value));
      onValidationChange(result.error);
      return;
    }

    setDraft(raw);
    onValueChange(result.value);
    onValidationChange(null);
  };

  return (
    <div className="numeric-input">
      <div className={`numeric-input__control${error ? ' is-invalid' : ''}`}>
        <input
          id={id}
          className="numeric-input__field"
          type="number"
          inputMode="decimal"
          min={0}
          step={step}
          value={draft}
          disabled={disabled}
          aria-label={ariaLabel}
          aria-invalid={Boolean(error)}
          aria-describedby={describedBy}
          onChange={handleChange}
        />
        {unit ? <UnitLabel unit={unit} /> : null}
      </div>
      <ValidationMessage id={`${id}-error`} message={error} />
    </div>
  );
}
