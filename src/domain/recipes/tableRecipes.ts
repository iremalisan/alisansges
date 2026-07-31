import type { TableRecipe } from '../types';

/**
 * Starter table recipes for local estimation.
 * These are editable sample values — not certified engineering standards.
 */
export const TABLE_RECIPES: TableRecipe[] = [
  {
    id: '2p-x-14',
    name: '2P x 14',
    panelsPerTable: 28,
    feetPerTable: 6,
    items: [
      { materialId: 'STEEL_POST', quantityPerTable: 6 },
      { materialId: 'PURLIN', quantityPerTable: 8 },
      { materialId: 'DIAGONAL_BRACE', quantityPerTable: 8 },
      { materialId: 'MID_CLAMP', quantityPerTable: 52 },
      { materialId: 'END_CLAMP', quantityPerTable: 4 },
      { materialId: 'BOLT', quantityPerTable: 180 },
    ],
  },
  {
    id: '2p-x-28',
    name: '2P x 28',
    panelsPerTable: 56,
    feetPerTable: 8,
    items: [
      { materialId: 'STEEL_POST', quantityPerTable: 8 },
      { materialId: 'PURLIN', quantityPerTable: 16 },
      { materialId: 'DIAGONAL_BRACE', quantityPerTable: 12 },
      { materialId: 'MID_CLAMP', quantityPerTable: 108 },
      { materialId: 'END_CLAMP', quantityPerTable: 4 },
      { materialId: 'BOLT', quantityPerTable: 320 },
    ],
  },
];

export const DEFAULT_TABLE_RECIPE_ID = TABLE_RECIPES[0].id;

export function getTableRecipe(id: string | null): TableRecipe | null {
  if (!id) {
    return null;
  }

  return TABLE_RECIPES.find((recipe) => recipe.id === id) ?? null;
}
