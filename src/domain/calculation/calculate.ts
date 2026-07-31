import {
  cableMaterialForTrenchType,
  getMaterial,
} from '../recipes/materialCatalog';
import { getKioskRecipe } from '../recipes/kioskRecipes';
import { getTableRecipe } from '../recipes/tableRecipes';
import type {
  CableTrenchInput,
  CalculationInputs,
  CalculationResult,
  KioskGroupInput,
  MaterialId,
  MaterialResultRow,
  MaterialUnit,
  ProjectInput,
  SummaryValues,
  TrenchRowSummary,
  ValidationErrors,
  WallInput,
  WallRowSummary,
} from '../types';
import {
  calculateConcreteFootCountFromPercent,
  calculateConcreteVolumePerFoot,
  calculateExcavationVolume,
  calculateGrossWallArea,
  calculateKioskMaterialTotal,
  calculateNetBimsCount,
  calculateNetConcreteVolume,
  calculateNetWallArea,
  calculateOrderBimsCount,
  calculateOrderCableLength,
  calculateOrderConcreteVolume,
  calculateOrderSandVolume,
  calculatePanelCount,
  calculateRecipeMaterialTotal,
  calculateRunLength,
  calculateSandVolume,
  calculateTableCount,
  calculateTotalFootCount,
  isFiniteNumber,
  isNonNegativeInteger,
} from './formulas';

export const MSG = {
  plantPowerPositive: 'Santral gücü 0’dan büyük olmalıdır.',
  panelPowerPositive: 'Panel gücü 0’dan büyük olmalıdır.',
  panelsPerTablePositive: 'Masa başına panel sayısı 0’dan büyük olmalıdır.',
  feetPerTablePositive: 'Masa başına ayak sayısı 0’dan büyük olmalıdır.',
  concretePercentRange: 'Betonlanacak ayak oranı 0–100 arasında olmalıdır.',
  concreteExceedsTotal:
    'Betonlanacak ayak sayısı toplam ayak sayısını aşamaz.',
  openingExceedsWall:
    'Kapı ve pencere boşluğu brüt duvar alanını aşamaz.',
  bimsFacePositive: 'Bims yüzeyi (genişlik × yükseklik) 0’dan büyük olmalıdır.',
  invalidTableRecipe: 'Geçersiz masa reçetesi seçildi.',
  invalidKioskRecipe: 'Geçersiz köşk reçetesi seçildi.',
  widthPositive: 'Kanal genişliği 0’dan büyük olmalıdır.',
  depthPositive: 'Kanal derinliği 0’dan büyük olmalıdır.',
  sandExceedsDepth: 'Alt + üst kum yüksekliği kanal derinliğini aşamaz.',
  percentRange: 'Oran 0–100 arasında olmalıdır.',
  nonNegativeInteger: 'Değer negatif olmayan bir tam sayı olmalıdır.',
} as const;

interface MaterialContribution {
  materialId: MaterialId;
  calculatedQuantity: number;
  orderQuantity: number;
  wasteRatePercent: number | null;
  note: string;
}

const MATERIAL_ORDER: MaterialId[] = [
  'PANEL',
  'TABLE',
  'FOUNDATION_FOOT',
  'STEEL_POST',
  'PURLIN',
  'DIAGONAL_BRACE',
  'MID_CLAMP',
  'END_CLAMP',
  'BOLT',
  'CONCRETE',
  'EXCAVATION',
  'SAND',
  'DC_CABLE',
  'AC_CABLE',
  'MV_CABLE',
  'COMMUNICATION_CABLE',
  'GROUNDING_CABLE',
  'OTHER_CABLE',
  'WARNING_TAPE',
  'CABLE_PROTECTION_PLATE',
  'CONDUIT',
  'OG_COPPER_LUG',
  'AG_COPPER_LUG',
  'GROUNDING_LUG',
  'CABLE_GLAND',
  'BIMS_BLOCK',
];

function emptySummary(): SummaryValues {
  return {
    panel: null,
    table: null,
    totalLegs: null,
    concrete: null,
    sand: null,
    bims: null,
  };
}

function roundQuantity(value: number, unit: MaterialUnit): number {
  if (unit === 'adet') {
    return Math.ceil(value - Number.EPSILON);
  }

  return Math.round(value * 1000) / 1000;
}

function roundPercent(value: number): number {
  return Math.round(value * 100) / 100;
}

function pushContribution(
  list: MaterialContribution[],
  contribution: MaterialContribution,
): void {
  if (
    !isFiniteNumber(contribution.calculatedQuantity) ||
    !isFiniteNumber(contribution.orderQuantity)
  ) {
    return;
  }

  list.push(contribution);
}

function summarizeNotes(notes: string[]): string {
  if (notes.length <= 4) {
    return notes.join(' + ');
  }

  return `${notes.length} kaynaktan toplandı`;
}

function aggregateContributions(
  contributions: MaterialContribution[],
): MaterialResultRow[] {
  const grouped = new Map<
    MaterialId,
    {
      calculatedQuantity: number;
      orderQuantity: number;
      wasteRates: number[];
      notes: string[];
    }
  >();

  for (const item of contributions) {
    const existing = grouped.get(item.materialId);
    if (!existing) {
      grouped.set(item.materialId, {
        calculatedQuantity: item.calculatedQuantity,
        orderQuantity: item.orderQuantity,
        wasteRates:
          item.wasteRatePercent === null ? [] : [item.wasteRatePercent],
        notes: [item.note],
      });
      continue;
    }

    existing.calculatedQuantity += item.calculatedQuantity;
    existing.orderQuantity += item.orderQuantity;
    if (item.wasteRatePercent !== null) {
      existing.wasteRates.push(item.wasteRatePercent);
    }
    existing.notes.push(item.note);
  }

  const rows: MaterialResultRow[] = [];

  for (const materialId of MATERIAL_ORDER) {
    const group = grouped.get(materialId);
    if (!group) {
      continue;
    }

    const definition = getMaterial(materialId);
    const uniqueWaste = [...new Set(group.wasteRates)];

    rows.push({
      id: materialId,
      category: definition.category,
      material: definition.name,
      calculatedQuantity: roundQuantity(
        group.calculatedQuantity,
        definition.unit,
      ),
      unit: definition.unit,
      wasteRatePercent:
        uniqueWaste.length === 1 ? roundPercent(uniqueWaste[0]) : null,
      orderQuantity: roundQuantity(group.orderQuantity, definition.unit),
      calculationNote: summarizeNotes(group.notes),
    });
  }

  return rows;
}

function validatePercent(
  value: number | null,
  errors: ValidationErrors,
  key: keyof ValidationErrors & string,
): boolean {
  if (value === null) {
    return true;
  }

  if (value < 0 || value > 100) {
    errors[key] = MSG.percentRange;
    return false;
  }

  return true;
}

function processTrench(
  trench: CableTrenchInput,
  contributions: MaterialContribution[],
  errors: ValidationErrors,
): TrenchRowSummary {
  const summary: TrenchRowSummary = {
    excavationM3: null,
    sandOrderM3: null,
    cableOrderM: null,
  };

  const length = trench.lengthM;
  const width = trench.widthM;
  const depth = trench.depthM;

  if (length !== null && length > 0) {
    if (width !== null && width <= 0) {
      errors[`trench.${trench.id}.widthM`] = MSG.widthPositive;
    }
    if (depth !== null && depth <= 0) {
      errors[`trench.${trench.id}.depthM`] = MSG.depthPositive;
    }
  }

  const sandOk =
    validatePercent(
      trench.sandWastePercent,
      errors,
      `trench.${trench.id}.sandWastePercent`,
    ) &&
    validatePercent(
      trench.cableWastePercent,
      errors,
      `trench.${trench.id}.cableWastePercent`,
    );

  if (
    trench.lowerSandHeightM !== null &&
    trench.upperSandHeightM !== null &&
    depth !== null &&
    trench.lowerSandHeightM + trench.upperSandHeightM > depth
  ) {
    errors[`trench.${trench.id}.lowerSandHeightM`] = MSG.sandExceedsDepth;
    errors[`trench.${trench.id}.upperSandHeightM`] = MSG.sandExceedsDepth;
  }

  for (const runField of [
    'warningTapeRuns',
    'protectionPlateRuns',
    'conduitRuns',
  ] as const) {
    const value = trench[runField];
    if (value !== null && !isNonNegativeInteger(value)) {
      errors[`trench.${trench.id}.${runField}`] = MSG.nonNegativeInteger;
    }
  }

  const trenchInvalid =
    Boolean(errors[`trench.${trench.id}.widthM`]) ||
    Boolean(errors[`trench.${trench.id}.depthM`]) ||
    Boolean(errors[`trench.${trench.id}.lowerSandHeightM`]) ||
    Boolean(errors[`trench.${trench.id}.sandWastePercent`]) ||
    Boolean(errors[`trench.${trench.id}.cableWastePercent`]);

  if (
    !trenchInvalid &&
    length !== null &&
    width !== null &&
    depth !== null &&
    width > 0 &&
    depth > 0
  ) {
    const excavation = calculateExcavationVolume(length, width, depth);
    if (isFiniteNumber(excavation)) {
      summary.excavationM3 = roundQuantity(excavation, 'm³');
      pushContribution(contributions, {
        materialId: 'EXCAVATION',
        calculatedQuantity: excavation,
        orderQuantity: excavation,
        wasteRatePercent: null,
        note: `${trench.name}: ${length}×${width}×${depth} m³`,
      });
    }
  }

  const sandHeightsInvalid = Boolean(
    errors[`trench.${trench.id}.lowerSandHeightM`],
  );

  if (
    !trenchInvalid &&
    !sandHeightsInvalid &&
    sandOk &&
    length !== null &&
    width !== null &&
    width > 0 &&
    trench.lowerSandHeightM !== null &&
    trench.upperSandHeightM !== null &&
    trench.sandWastePercent !== null
  ) {
    const lower = calculateSandVolume(
      length,
      width,
      trench.lowerSandHeightM,
    );
    const upper = calculateSandVolume(
      length,
      width,
      trench.upperSandHeightM,
    );
    const net = lower + upper;
    const order = calculateOrderSandVolume(net, trench.sandWastePercent);

    if (isFiniteNumber(net) && isFiniteNumber(order)) {
      summary.sandOrderM3 = roundQuantity(order, 'm³');
      pushContribution(contributions, {
        materialId: 'SAND',
        calculatedQuantity: net,
        orderQuantity: order,
        wasteRatePercent: trench.sandWastePercent,
        note: `${trench.name}: alt + üst kum, %${trench.sandWastePercent} fire`,
      });
    }
  }

  if (
    !trenchInvalid &&
    trench.cableLengthM !== null &&
    trench.cableLengthM > 0 &&
    trench.cableWastePercent !== null &&
    sandOk
  ) {
    const orderCable = calculateOrderCableLength(
      trench.cableLengthM,
      trench.cableWastePercent,
    );
    if (isFiniteNumber(orderCable)) {
      summary.cableOrderM = roundQuantity(orderCable, 'm');
      pushContribution(contributions, {
        materialId: cableMaterialForTrenchType(trench.type),
        calculatedQuantity: trench.cableLengthM,
        orderQuantity: orderCable,
        wasteRatePercent: trench.cableWastePercent,
        note: `${trench.name}: ${trench.cableLengthM} m, %${trench.cableWastePercent} fire`,
      });
    }
  }

  if (
    !trenchInvalid &&
    length !== null &&
    trench.warningTapeRuns !== null &&
    trench.warningTapeRuns > 0 &&
    isNonNegativeInteger(trench.warningTapeRuns)
  ) {
    const total = calculateRunLength(length, trench.warningTapeRuns);
    pushContribution(contributions, {
      materialId: 'WARNING_TAPE',
      calculatedQuantity: total,
      orderQuantity: total,
      wasteRatePercent: null,
      note: `${trench.name}: ${length} m × ${trench.warningTapeRuns} hat`,
    });
  }

  if (
    !trenchInvalid &&
    length !== null &&
    trench.protectionPlateRuns !== null &&
    trench.protectionPlateRuns > 0 &&
    isNonNegativeInteger(trench.protectionPlateRuns)
  ) {
    const total = calculateRunLength(length, trench.protectionPlateRuns);
    pushContribution(contributions, {
      materialId: 'CABLE_PROTECTION_PLATE',
      calculatedQuantity: total,
      orderQuantity: total,
      wasteRatePercent: null,
      note: `${trench.name}: ${length} m × ${trench.protectionPlateRuns} hat`,
    });
  }

  if (
    !trenchInvalid &&
    length !== null &&
    trench.conduitRuns !== null &&
    trench.conduitRuns > 0 &&
    isNonNegativeInteger(trench.conduitRuns)
  ) {
    const total = calculateRunLength(length, trench.conduitRuns);
    pushContribution(contributions, {
      materialId: 'CONDUIT',
      calculatedQuantity: total,
      orderQuantity: total,
      wasteRatePercent: null,
      note: `${trench.name}: ${length} m × ${trench.conduitRuns} hat`,
    });
  }

  return summary;
}

function processKioskGroup(
  group: KioskGroupInput,
  contributions: MaterialContribution[],
  errors: ValidationErrors,
): void {
  if (group.recipeId && !getKioskRecipe(group.recipeId)) {
    errors[`kioskGroup.${group.id}.recipeId`] = MSG.invalidKioskRecipe;
  }

  if (group.count !== null && !isNonNegativeInteger(group.count)) {
    errors[`kioskGroup.${group.id}.count`] = MSG.nonNegativeInteger;
    return;
  }

  if (group.count === null || group.count < 0) {
    return;
  }

  const pairs: Array<{
    materialId: MaterialId;
    perKiosk: number | null;
    field: keyof KioskGroupInput;
    label: string;
  }> = [
    {
      materialId: 'OG_COPPER_LUG',
      perKiosk: group.ogCopperLugPerKiosk,
      field: 'ogCopperLugPerKiosk',
      label: 'OG bakır pabuç',
    },
    {
      materialId: 'AG_COPPER_LUG',
      perKiosk: group.agCopperLugPerKiosk,
      field: 'agCopperLugPerKiosk',
      label: 'AG bakır pabuç',
    },
    {
      materialId: 'GROUNDING_LUG',
      perKiosk: group.groundingLugPerKiosk,
      field: 'groundingLugPerKiosk',
      label: 'topraklama pabucu',
    },
    {
      materialId: 'CABLE_GLAND',
      perKiosk: group.cableGlandPerKiosk,
      field: 'cableGlandPerKiosk',
      label: 'kablo rakoru',
    },
    {
      materialId: 'BIMS_BLOCK',
      perKiosk: group.bimsBlockPerKiosk,
      field: 'bimsBlockPerKiosk',
      label: 'bims',
    },
  ];

  for (const pair of pairs) {
    if (pair.perKiosk === null) {
      continue;
    }

    if (pair.perKiosk < 0) {
      errors[`kioskGroup.${group.id}.${pair.field}`] =
        'Negatif değer girilemez.';
      continue;
    }

    const total = calculateKioskMaterialTotal(group.count, pair.perKiosk);
    pushContribution(contributions, {
      materialId: pair.materialId,
      calculatedQuantity: total,
      orderQuantity: total,
      wasteRatePercent: null,
      note: `${group.count} × ${group.name}`,
    });
  }
}

function processWall(
  wall: WallInput,
  contributions: MaterialContribution[],
  errors: ValidationErrors,
): WallRowSummary {
  const summary: WallRowSummary = {
    grossAreaM2: null,
    netAreaM2: null,
    orderBimsCount: null,
  };

  validatePercent(
    wall.bimsWastePercent,
    errors,
    `wall.${wall.id}.bimsWastePercent`,
  );

  if (
    wall.lengthM === null ||
    wall.heightM === null ||
    wall.openingAreaM2 === null
  ) {
    return summary;
  }

  const gross = calculateGrossWallArea(wall.lengthM, wall.heightM);
  const net = calculateNetWallArea(
    wall.lengthM,
    wall.heightM,
    wall.openingAreaM2,
  );

  summary.grossAreaM2 = roundQuantity(gross, 'm²');
  summary.netAreaM2 = roundQuantity(net, 'm²');

  if (net < 0) {
    errors[`wall.${wall.id}.openingAreaM2`] = MSG.openingExceedsWall;
    return summary;
  }

  if (
    wall.bimsWidthM === null ||
    wall.bimsHeightM === null ||
    wall.bimsWastePercent === null ||
    errors[`wall.${wall.id}.bimsWastePercent`]
  ) {
    return summary;
  }

  const face = wall.bimsWidthM * wall.bimsHeightM;
  if (face <= 0) {
    errors[`wall.${wall.id}.bimsWidthM`] = MSG.bimsFacePositive;
    errors[`wall.${wall.id}.bimsHeightM`] = MSG.bimsFacePositive;
    return summary;
  }

  const netBims = calculateNetBimsCount(
    net,
    wall.bimsWidthM,
    wall.bimsHeightM,
  );
  const orderBims = calculateOrderBimsCount(netBims, wall.bimsWastePercent);
  summary.orderBimsCount = orderBims;

  pushContribution(contributions, {
    materialId: 'BIMS_BLOCK',
    calculatedQuantity: netBims,
    orderQuantity: orderBims,
    wasteRatePercent: wall.bimsWastePercent,
    note: `${wall.name}`,
  });

  return summary;
}

export function calculateMaterials(
  project: ProjectInput,
  calculations: CalculationInputs,
): CalculationResult {
  const errors: ValidationErrors = {};
  const contributions: MaterialContribution[] = [];
  const summary = emptySummary();
  const trenchSummaries: Record<string, TrenchRowSummary> = {};
  const wallSummaries: Record<string, WallRowSummary> = {};

  const { panelTable, foundation, trenches, kioskGroups, walls } =
    calculations;

  if (
    panelTable.selectedTableRecipeId &&
    !getTableRecipe(panelTable.selectedTableRecipeId)
  ) {
    errors['panelTable.selectedTableRecipeId'] = MSG.invalidTableRecipe;
  }

  let panelCount: number | null = null;
  let tableCount: number | null = null;
  let totalFootCount: number | null = null;

  if (project.plantPowerMWp !== null && project.plantPowerMWp <= 0) {
    errors.plantPowerMWp = MSG.plantPowerPositive;
  }

  if (project.panelPowerWp !== null && project.panelPowerWp <= 0) {
    errors.panelPowerWp = MSG.panelPowerPositive;
  }

  if (
    project.plantPowerMWp !== null &&
    project.panelPowerWp !== null &&
    project.plantPowerMWp > 0 &&
    project.panelPowerWp > 0
  ) {
    panelCount = calculatePanelCount(
      project.plantPowerMWp,
      project.panelPowerWp,
    );
    summary.panel = panelCount;
    pushContribution(contributions, {
      materialId: 'PANEL',
      calculatedQuantity: panelCount,
      orderQuantity: panelCount,
      wasteRatePercent: null,
      note: `ceil(${project.plantPowerMWp} MWp × 1.000.000 / ${project.panelPowerWp} Wp)`,
    });
  }

  if (panelTable.panelsPerTable !== null && panelTable.panelsPerTable <= 0) {
    errors['panelTable.panelsPerTable'] = MSG.panelsPerTablePositive;
  }

  if (panelTable.legsPerTable !== null && panelTable.legsPerTable <= 0) {
    errors['panelTable.legsPerTable'] = MSG.feetPerTablePositive;
  }

  if (
    panelCount !== null &&
    panelTable.panelsPerTable !== null &&
    panelTable.panelsPerTable > 0
  ) {
    tableCount = calculateTableCount(panelCount, panelTable.panelsPerTable);
    summary.table = tableCount;
    pushContribution(contributions, {
      materialId: 'TABLE',
      calculatedQuantity: tableCount,
      orderQuantity: tableCount,
      wasteRatePercent: null,
      note: `ceil(${panelCount} panel / ${panelTable.panelsPerTable} panel/masa)`,
    });
  }

  if (
    tableCount !== null &&
    panelTable.legsPerTable !== null &&
    panelTable.legsPerTable > 0
  ) {
    totalFootCount = calculateTotalFootCount(
      tableCount,
      panelTable.legsPerTable,
    );
    summary.totalLegs = totalFootCount;
    pushContribution(contributions, {
      materialId: 'FOUNDATION_FOOT',
      calculatedQuantity: totalFootCount,
      orderQuantity: totalFootCount,
      wasteRatePercent: null,
      note: `${tableCount} masa × ${panelTable.legsPerTable} ayak/masa`,
    });
  }

  const tableRecipe = getTableRecipe(panelTable.selectedTableRecipeId);
  if (tableCount !== null && tableRecipe) {
    for (const item of tableRecipe.items) {
      const total = calculateRecipeMaterialTotal(
        tableCount,
        item.quantityPerTable,
      );
      const material = getMaterial(item.materialId);
      pushContribution(contributions, {
        materialId: item.materialId,
        calculatedQuantity: total,
        orderQuantity: total,
        wasteRatePercent: null,
        note: `${tableCount} masa × ${item.quantityPerTable} ${material.name}/masa (${tableRecipe.name})`,
      });
    }
  }

  let concreteFootCount: number | null = null;

  if (
    foundation.concreteLegsPercent !== null &&
    (foundation.concreteLegsPercent < 0 ||
      foundation.concreteLegsPercent > 100)
  ) {
    errors['foundation.concreteLegsPercent'] = MSG.concretePercentRange;
  }

  if (foundation.concreteFootMode === 'count') {
    if (foundation.concreteLegsCount !== null) {
      if (
        totalFootCount !== null &&
        foundation.concreteLegsCount > totalFootCount
      ) {
        errors['foundation.concreteLegsCount'] = MSG.concreteExceedsTotal;
      } else {
        concreteFootCount = foundation.concreteLegsCount;
      }
    }
  } else if (
    totalFootCount !== null &&
    foundation.concreteLegsPercent !== null &&
    foundation.concreteLegsPercent >= 0 &&
    foundation.concreteLegsPercent <= 100
  ) {
    concreteFootCount = calculateConcreteFootCountFromPercent(
      totalFootCount,
      foundation.concreteLegsPercent,
    );
  }

  if (
    concreteFootCount !== null &&
    foundation.pitWidthM !== null &&
    foundation.pitLengthM !== null &&
    foundation.pitDepthM !== null &&
    foundation.concreteWastePercent !== null
  ) {
    const volumePerFoot = calculateConcreteVolumePerFoot(
      foundation.pitWidthM,
      foundation.pitLengthM,
      foundation.pitDepthM,
    );
    const netVolume = calculateNetConcreteVolume(
      concreteFootCount,
      volumePerFoot,
    );
    const orderVolume = calculateOrderConcreteVolume(
      netVolume,
      foundation.concreteWastePercent,
    );

    if (isFiniteNumber(netVolume) && isFiniteNumber(orderVolume)) {
      summary.concrete = roundQuantity(orderVolume, 'm³');
      pushContribution(contributions, {
        materialId: 'CONCRETE',
        calculatedQuantity: netVolume,
        orderQuantity: orderVolume,
        wasteRatePercent: foundation.concreteWastePercent,
        note: `${concreteFootCount} ayak × (${foundation.pitWidthM} × ${foundation.pitLengthM} × ${foundation.pitDepthM}) m³, fire %${foundation.concreteWastePercent}`,
      });
    }
  }

  for (const trench of trenches) {
    trenchSummaries[trench.id] = processTrench(
      trench,
      contributions,
      errors,
    );
  }

  for (const group of kioskGroups) {
    processKioskGroup(group, contributions, errors);
  }

  for (const wall of walls) {
    wallSummaries[wall.id] = processWall(wall, contributions, errors);
  }

  const materialRows = aggregateContributions(contributions);
  const sandRow = materialRows.find((row) => row.id === 'SAND');
  const bimsRow = materialRows.find((row) => row.id === 'BIMS_BLOCK');
  summary.sand = sandRow?.orderQuantity ?? null;
  summary.bims = bimsRow?.orderQuantity ?? null;

  return {
    summary,
    materialRows,
    validationErrors: errors,
    trenchSummaries,
    wallSummaries,
  };
}
