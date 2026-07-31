import type { CalculationInputs, ProjectInputs } from './types';

/** Sample input values only — no calculated material results. */
export const SAMPLE_PROJECT_NAME = '90 MWp Örnek Proje';

export const sampleProjectInputs = (): ProjectInputs => ({
  projectName: SAMPLE_PROJECT_NAME,
  plantPowerMWp: 90,
  panelPowerWp: 580,
  generalWastePercent: 2,
});

export const sampleCalculationInputs = (): CalculationInputs => ({
  panelTable: {
    panelsPerTable: 28,
    legsPerTable: 4,
  },
  foundation: {
    concreteLegsCount: null,
    concreteLegsPercent: 100,
    pitWidthM: 0.4,
    pitLengthM: 0.4,
    pitDepthM: 0.8,
    concreteWastePercent: 5,
  },
  cableTrench: {
    trenchLengthM: 12000,
    trenchWidthM: 0.4,
    sandHeightM: 0.15,
    sandWastePercent: 5,
  },
  kiosk: {
    kioskCount: 18,
    ogCopperLugsPerKiosk: 6,
    agCopperLugsPerKiosk: 12,
    groundingLugsPerKiosk: 4,
  },
  bims: {
    wallLengthM: 120,
    wallHeightM: 2.5,
    openingAreaM2: 18,
    bimsWidthM: 0.2,
    bimsHeightM: 0.2,
    bimsWastePercent: 5,
  },
});
