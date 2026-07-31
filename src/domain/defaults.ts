import type { AppState, CalculationInputs, ProjectInputs } from './types';

export const emptyProjectInputs = (): ProjectInputs => ({
  projectName: '',
  plantPowerMWp: null,
  panelPowerWp: null,
  generalWastePercent: null,
});

export const emptyCalculationInputs = (): CalculationInputs => ({
  panelTable: {
    panelsPerTable: null,
    legsPerTable: null,
  },
  foundation: {
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
    kioskCount: null,
    ogCopperLugsPerKiosk: null,
    agCopperLugsPerKiosk: null,
    groundingLugsPerKiosk: null,
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

export const createInitialAppState = (): AppState => ({
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
