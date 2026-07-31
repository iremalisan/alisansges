import { createEntityId, createFixedId } from './ids';
import {
  getKioskRecipe,
  kioskRecipeToInputValues,
} from './recipes/kioskRecipes';
import type {
  CableTrenchInput,
  KioskGroupInput,
  TrenchType,
  WallInput,
} from './types';

export function createEmptyTrench(
  overrides: Partial<CableTrenchInput> = {},
): CableTrenchInput {
  return {
    id: overrides.id ?? createEntityId('trench'),
    name: overrides.name ?? 'Yeni Kanal',
    type: overrides.type ?? 'DC',
    lengthM: overrides.lengthM ?? null,
    widthM: overrides.widthM ?? null,
    depthM: overrides.depthM ?? null,
    lowerSandHeightM: overrides.lowerSandHeightM ?? null,
    upperSandHeightM: overrides.upperSandHeightM ?? null,
    sandWastePercent: overrides.sandWastePercent ?? null,
    cableLengthM: overrides.cableLengthM ?? null,
    cableWastePercent: overrides.cableWastePercent ?? null,
    warningTapeRuns: overrides.warningTapeRuns ?? null,
    protectionPlateRuns: overrides.protectionPlateRuns ?? null,
    conduitRuns: overrides.conduitRuns ?? null,
  };
}

export function createEmptyKioskGroup(
  overrides: Partial<KioskGroupInput> = {},
): KioskGroupInput {
  return {
    id: overrides.id ?? createEntityId('kiosk'),
    name: overrides.name ?? 'Yeni Köşk Grubu',
    recipeId: overrides.recipeId ?? null,
    count: overrides.count ?? null,
    ogCopperLugPerKiosk: overrides.ogCopperLugPerKiosk ?? null,
    agCopperLugPerKiosk: overrides.agCopperLugPerKiosk ?? null,
    groundingLugPerKiosk: overrides.groundingLugPerKiosk ?? null,
    cableGlandPerKiosk: overrides.cableGlandPerKiosk ?? null,
    bimsBlockPerKiosk: overrides.bimsBlockPerKiosk ?? null,
  };
}

export function createEmptyWall(
  overrides: Partial<WallInput> = {},
): WallInput {
  return {
    id: overrides.id ?? createEntityId('wall'),
    name: overrides.name ?? 'Yeni Duvar',
    lengthM: overrides.lengthM ?? null,
    heightM: overrides.heightM ?? null,
    openingAreaM2: overrides.openingAreaM2 ?? null,
    bimsWidthM: overrides.bimsWidthM ?? null,
    bimsHeightM: overrides.bimsHeightM ?? null,
    bimsWastePercent: overrides.bimsWastePercent ?? null,
  };
}

export function duplicateTrenchEntry(source: CableTrenchInput): CableTrenchInput {
  return {
    ...source,
    id: createEntityId('trench'),
    name: `${source.name} (Kopya)`,
  };
}

export function duplicateKioskGroupEntry(
  source: KioskGroupInput,
): KioskGroupInput {
  return {
    ...source,
    id: createEntityId('kiosk'),
    name: `${source.name} (Kopya)`,
  };
}

export function duplicateWallEntry(source: WallInput): WallInput {
  return {
    ...source,
    id: createEntityId('wall'),
    name: `${source.name} (Kopya)`,
  };
}

export function applyKioskRecipeToGroup(
  group: KioskGroupInput,
  recipeId: string,
): KioskGroupInput {
  const recipe = getKioskRecipe(recipeId);
  if (!recipe) {
    return { ...group, recipeId };
  }

  const values = kioskRecipeToInputValues(recipe);

  return {
    ...group,
    recipeId,
    ogCopperLugPerKiosk: values.ogCopperLugsPerKiosk,
    agCopperLugPerKiosk: values.agCopperLugsPerKiosk,
    groundingLugPerKiosk: values.groundingLugsPerKiosk,
    cableGlandPerKiosk: values.cableGlandsPerKiosk,
    bimsBlockPerKiosk: values.bimsBlocksPerKiosk,
  };
}

export function createFixedTrench(
  slug: string,
  data: Omit<CableTrenchInput, 'id'> & { type: TrenchType },
): CableTrenchInput {
  return {
    ...data,
    id: createFixedId('trench', slug),
  };
}

export function createFixedKioskGroup(
  slug: string,
  data: Omit<KioskGroupInput, 'id'>,
): KioskGroupInput {
  return {
    ...data,
    id: createFixedId('kiosk', slug),
  };
}

export function createFixedWall(
  slug: string,
  data: Omit<WallInput, 'id'>,
): WallInput {
  return {
    ...data,
    id: createFixedId('wall', slug),
  };
}
