import {
  applyKioskRecipeToGroup,
  createFixedKioskGroup,
  createFixedTrench,
  createFixedWall,
} from './entries';
import { getTableRecipe } from './recipes/tableRecipes';
import type { CalculationInputs, ProjectInput } from './types';

export const SAMPLE_PROJECT_NAME = '90 MWp Örnek GES';
export const SAMPLE_TABLE_RECIPE_ID = '2p-x-28';
export const SAMPLE_KIOSK_RECIPE_ID = 'standard-concrete-kiosk';
export const SAMPLE_LARGE_KIOSK_RECIPE_ID = 'large-concrete-kiosk';

export const sampleProjectInputs = (): ProjectInput => ({
  projectName: SAMPLE_PROJECT_NAME,
  plantPowerMWp: 90,
  panelPowerWp: 700,
  generalWastePercent: null,
});

export const sampleCalculationInputs = (): CalculationInputs => {
  const tableRecipe = getTableRecipe(SAMPLE_TABLE_RECIPE_ID);

  const mainKiosk = applyKioskRecipeToGroup(
    createFixedKioskGroup('ana', {
      name: 'Ana Köşkler',
      recipeId: SAMPLE_KIOSK_RECIPE_ID,
      count: 10,
      ogCopperLugPerKiosk: null,
      agCopperLugPerKiosk: null,
      groundingLugPerKiosk: null,
      cableGlandPerKiosk: null,
      bimsBlockPerKiosk: null,
    }),
    SAMPLE_KIOSK_RECIPE_ID,
  );

  const auxKiosk = applyKioskRecipeToGroup(
    createFixedKioskGroup('yardimci', {
      name: 'Yardımcı Köşkler',
      recipeId: SAMPLE_LARGE_KIOSK_RECIPE_ID,
      count: 2,
      ogCopperLugPerKiosk: null,
      agCopperLugPerKiosk: null,
      groundingLugPerKiosk: null,
      cableGlandPerKiosk: null,
      bimsBlockPerKiosk: null,
    }),
    SAMPLE_LARGE_KIOSK_RECIPE_ID,
  );

  return {
    panelTable: {
      selectedTableRecipeId: SAMPLE_TABLE_RECIPE_ID,
      panelsPerTable: tableRecipe?.panelsPerTable ?? 56,
      legsPerTable: tableRecipe?.feetPerTable ?? 8,
    },
    foundation: {
      concreteFootMode: 'percent',
      concreteLegsCount: null,
      concreteLegsPercent: 10,
      pitWidthM: 0.45,
      pitLengthM: 0.45,
      pitDepthM: 1.2,
      concreteWastePercent: 5,
    },
    trenches: [
      createFixedTrench('dc-ana', {
        name: 'DC Ana Kanal',
        type: 'DC',
        lengthM: 4500,
        widthM: 0.6,
        depthM: 0.8,
        lowerSandHeightM: 0.1,
        upperSandHeightM: 0.1,
        sandWastePercent: 5,
        cableLengthM: 9600,
        cableWastePercent: 3,
        warningTapeRuns: 1,
        protectionPlateRuns: 1,
        conduitRuns: 0,
      }),
      createFixedTrench('og-ana', {
        name: 'OG Ana Kanal',
        type: 'OG',
        lengthM: 2500,
        widthM: 0.8,
        depthM: 1.1,
        lowerSandHeightM: 0.1,
        upperSandHeightM: 0.2,
        sandWastePercent: 5,
        cableLengthM: 2750,
        cableWastePercent: 3,
        warningTapeRuns: 1,
        protectionPlateRuns: 1,
        conduitRuns: 1,
      }),
      createFixedTrench('haberlesme', {
        name: 'Haberleşme Kanalı',
        type: 'Haberleşme',
        lengthM: 1500,
        widthM: 0.4,
        depthM: 0.6,
        lowerSandHeightM: 0.05,
        upperSandHeightM: 0.05,
        sandWastePercent: 5,
        cableLengthM: 1650,
        cableWastePercent: 3,
        warningTapeRuns: 1,
        protectionPlateRuns: 0,
        conduitRuns: 1,
      }),
    ],
    kioskGroups: [mainKiosk, auxKiosk],
    walls: [
      createFixedWall('ana-kosk', {
        name: 'Ana Köşk Duvarı',
        lengthM: 80,
        heightM: 3,
        openingAreaM2: 20,
        bimsWidthM: 0.4,
        bimsHeightM: 0.2,
        bimsWastePercent: 5,
      }),
      createFixedWall('depo', {
        name: 'Depo Duvarı',
        lengthM: 35,
        heightM: 2.8,
        openingAreaM2: 8,
        bimsWidthM: 0.4,
        bimsHeightM: 0.2,
        bimsWastePercent: 5,
      }),
    ],
  };
};
