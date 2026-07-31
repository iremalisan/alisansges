import type { KioskRecipe } from '../types';

/**
 * Starter kiosk recipes for local estimation.
 * These are editable sample values — not certified engineering standards.
 */
export const KIOSK_RECIPES: KioskRecipe[] = [
  {
    id: 'standard-concrete-kiosk',
    name: 'Standart Beton Köşk',
    items: [
      { materialId: 'OG_COPPER_LUG', quantityPerKiosk: 24 },
      { materialId: 'AG_COPPER_LUG', quantityPerKiosk: 18 },
      { materialId: 'GROUNDING_LUG', quantityPerKiosk: 12 },
      { materialId: 'CABLE_GLAND', quantityPerKiosk: 20 },
      { materialId: 'BIMS_BLOCK', quantityPerKiosk: 600 },
    ],
  },
  {
    id: 'large-concrete-kiosk',
    name: 'Büyük Beton Köşk',
    items: [
      { materialId: 'OG_COPPER_LUG', quantityPerKiosk: 36 },
      { materialId: 'AG_COPPER_LUG', quantityPerKiosk: 30 },
      { materialId: 'GROUNDING_LUG', quantityPerKiosk: 18 },
      { materialId: 'CABLE_GLAND', quantityPerKiosk: 32 },
      { materialId: 'BIMS_BLOCK', quantityPerKiosk: 900 },
    ],
  },
];

export const DEFAULT_KIOSK_RECIPE_ID = KIOSK_RECIPES[0].id;

export function getKioskRecipe(id: string | null): KioskRecipe | null {
  if (!id) {
    return null;
  }

  return KIOSK_RECIPES.find((recipe) => recipe.id === id) ?? null;
}

export function kioskRecipeToInputValues(recipe: KioskRecipe): {
  ogCopperLugsPerKiosk: number;
  agCopperLugsPerKiosk: number;
  groundingLugsPerKiosk: number;
  cableGlandsPerKiosk: number;
  bimsBlocksPerKiosk: number;
} {
  const quantity = (materialId: string): number =>
    recipe.items.find((item) => item.materialId === materialId)?.quantityPerKiosk ??
    0;

  return {
    ogCopperLugsPerKiosk: quantity('OG_COPPER_LUG'),
    agCopperLugsPerKiosk: quantity('AG_COPPER_LUG'),
    groundingLugsPerKiosk: quantity('GROUNDING_LUG'),
    cableGlandsPerKiosk: quantity('CABLE_GLAND'),
    bimsBlocksPerKiosk: quantity('BIMS_BLOCK'),
  };
}
