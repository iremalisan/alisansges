import { describe, expect, it } from 'vitest';
import {
  INVALID_NUMBER_MESSAGE,
  NEGATIVE_VALUE_MESSAGE,
  parseNonNegativeNumber,
} from './validation';

describe('parseNonNegativeNumber', () => {
  it('accepts empty input as null', () => {
    expect(parseNonNegativeNumber('')).toEqual({ value: null, error: null });
  });

  it('accepts decimal values', () => {
    expect(parseNonNegativeNumber('0.4')).toEqual({ value: 0.4, error: null });
    expect(parseNonNegativeNumber('1,25')).toEqual({ value: 1.25, error: null });
  });

  it('rejects negative values', () => {
    expect(parseNonNegativeNumber('-1')).toEqual({
      value: null,
      error: NEGATIVE_VALUE_MESSAGE,
    });
  });

  it('rejects invalid numbers', () => {
    expect(parseNonNegativeNumber('abc')).toEqual({
      value: null,
      error: INVALID_NUMBER_MESSAGE,
    });
  });
});
