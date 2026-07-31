import type { ValidationErrors, ValidationFieldKey } from './types';

export const NEGATIVE_VALUE_MESSAGE = 'Negatif değer girilemez.';
export const INVALID_NUMBER_MESSAGE = 'Geçerli bir sayı girin.';

export function parseNonNegativeNumber(
  raw: string,
): { value: number | null; error: string | null } {
  const trimmed = raw.trim();

  if (trimmed === '') {
    return { value: null, error: null };
  }

  const normalized = trimmed.replace(',', '.');
  const parsed = Number(normalized);

  if (!Number.isFinite(parsed)) {
    return { value: null, error: INVALID_NUMBER_MESSAGE };
  }

  if (parsed < 0) {
    return { value: null, error: NEGATIVE_VALUE_MESSAGE };
  }

  return { value: parsed, error: null };
}

export function setFieldError(
  errors: ValidationErrors,
  field: ValidationFieldKey,
  message: string | null,
): ValidationErrors {
  const next = { ...errors };

  if (message) {
    next[field] = message;
  } else {
    delete next[field];
  }

  return next;
}
