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

/** Clear calculation-owned keys before merging fresh calculation errors. */
export const CALCULATION_ERROR_KEYS: ValidationFieldKey[] = [
  'plantPowerMWp',
  'panelPowerWp',
  'panelTable.selectedTableRecipeId',
  'panelTable.panelsPerTable',
  'panelTable.legsPerTable',
  'foundation.concreteLegsCount',
  'foundation.concreteLegsPercent',
  'kiosk.selectedKioskRecipeId',
  'bims.openingAreaM2',
  'bims.bimsWidthM',
  'bims.bimsHeightM',
];

export function mergeValidationErrors(
  previousErrors: ValidationErrors,
  calculationErrors: ValidationErrors,
): ValidationErrors {
  const merged: ValidationErrors = {};

  for (const [key, message] of Object.entries(previousErrors) as Array<
    [ValidationFieldKey, string]
  >) {
    const isParseError =
      message === NEGATIVE_VALUE_MESSAGE ||
      message === INVALID_NUMBER_MESSAGE;

    if (!CALCULATION_ERROR_KEYS.includes(key) || isParseError) {
      merged[key] = message;
    }
  }

  return { ...merged, ...calculationErrors };
}
