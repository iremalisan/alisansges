import { calculateMaterials } from './calculation/calculate';
import type { AppState, CalculationInputs, ProjectInput } from './types';
import { mergeValidationErrors } from './validation';

export const emptyProjectInputs = (): ProjectInput => ({
  projectName: '',
  plantPowerMWp: null,
  panelPowerWp: null,
  generalWastePercent: null,
});

export const emptyCalculationInputs = (): CalculationInputs => ({
  panelTable: {
    selectedTableRecipeId: null,
    panelsPerTable: null,
    legsPerTable: null,
  },
  foundation: {
    concreteFootMode: 'percent',
    concreteLegsCount: null,
    concreteLegsPercent: null,
    pitWidthM: null,
    pitLengthM: null,
    pitDepthM: null,
    concreteWastePercent: null,
  },
  cableTrench: {
    trenchLengthM: null,
    trenchWidthM: null,
    sandHeightM: null,
    sandWastePercent: null,
  },
  kiosk: {
    selectedKioskRecipeId: null,
    kioskCount: null,
    ogCopperLugsPerKiosk: null,
    agCopperLugsPerKiosk: null,
    groundingLugsPerKiosk: null,
    cableGlandsPerKiosk: null,
    bimsBlocksPerKiosk: null,
  },
  bims: {
    wallLengthM: null,
    wallHeightM: null,
    openingAreaM2: null,
    bimsWidthM: null,
    bimsHeightM: null,
    bimsWastePercent: null,
  },
});

export function applyCalculation(state: AppState): AppState {
  const result = calculateMaterials(state.project, state.calculations);

  return {
    ...state,
    summary: result.summary,
    materialRows: result.materialRows,
    validationErrors: mergeValidationErrors(
      state.validationErrors,
      result.validationErrors,
    ),
  };
}

export const createInitialAppState = (): AppState =>
  applyCalculation({
    project: emptyProjectInputs(),
    calculations: emptyCalculationInputs(),
    validationErrors: {},
    materialRows: [],
    summary: {
      panel: null,
      table: null,
      totalLegs: null,
      concrete: null,
      sand: null,
      bims: null,
    },
  });
