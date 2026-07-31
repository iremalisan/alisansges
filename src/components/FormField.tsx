import type { ReactNode } from 'react';
import './FormField.css';

interface FormFieldProps {
  label: string;
  htmlFor: string;
  required?: boolean;
  children: ReactNode;
  hint?: string;
}

export function FormField({
  label,
  htmlFor,
  required = false,
  children,
  hint,
}: FormFieldProps) {
  return (
    <div className="form-field">
      <label className="form-field__label" htmlFor={htmlFor}>
        <span>{label}</span>
        {required ? (
          <span className="form-field__required" aria-hidden="true">
            *
          </span>
        ) : null}
      </label>
      {children}
      {hint ? <p className="form-field__hint">{hint}</p> : null}
    </div>
  );
}
