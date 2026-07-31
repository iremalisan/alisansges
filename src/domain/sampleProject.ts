import { getKioskRecipe, kioskRecipeToInputValues } from './recipes/kioskRecipes';
import { getTableRecipe } from './recipes/tableRecipes';
import type { CalculationInputs, ProjectInput } from './types';

export const SAMPLE_PROJECT_NAME = '90 MWp Örnek GES';
export const SAMPLE_TABLE_RECIPE_ID = '2p-x-28';
export const SAMPLE_KIOSK_RECIPE_ID = 'standard-concrete-kiosk';

export const sampleProjectInputs = (): ProjectInput => ({
  projectName: SAMPLE_PROJECT_NAME,
  plantPowerMWp: 90,
  panelPowerWp: 700,
  generalWastePercent: null,
});

export const sampleCalculationInputs = (): CalculationInputs => {
  const tableRecipe = getTableRecipe(SAMPLE_TABLE_RECIPE_ID);
  const kioskRecipe = getKioskRecipe(SAMPLE_KIOSK_RECIPE_ID);
  const kioskValues = kioskRecipe
    ? kioskRecipeToInputValues(kioskRecipe)
    : {
        ogCopperLugsPerKiosk: null,
        agCopperLugsPerKiosk: null,
        groundingLugsPerKiosk: null,
        cableGlandsPerKiosk: null,
        bimsBlocksPerKiosk: null,
      };

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
    cableTrench: {
      trenchLengthM: 8500,
      trenchWidthM: 0.6,
      sandHeightM: 0.2,
      sandWastePercent: 5,
    },
    kiosk: {
      selectedKioskRecipeId: SAMPLE_KIOSK_RECIPE_ID,
      kioskCount: 10,
      ...kioskValues,
    },
    bims: {
      wallLengthM: 80,
      wallHeightM: 3,
      openingAreaM2: 20,
      bimsWidthM: 0.4,
      bimsHeightM: 0.2,
      bimsWastePercent: 5,
    },
  };
};
