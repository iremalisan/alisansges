import { getMaterial } from '../recipes/materialCatalog';
import { getKioskRecipe } from '../recipes/kioskRecipes';
import { getTableRecipe } from '../recipes/tableRecipes';
import type {
  CalculationInputs,
  CalculationResult,
  MaterialId,
  MaterialResultRow,
  MaterialUnit,
  ProjectInput,
  SummaryValues,
  ValidationErrors,
} from '../types';
import {
  calculateConcreteFootCountFromPercent,
  calculateConcreteVolumePerFoot,
  calculateKioskMaterialTotal,
  calculateNetBimsCount,
  calculateNetConcreteVolume,
  calculateNetWallArea,
  calculateOrderBimsCount,
  calculateOrderConcreteVolume,
  calculateOrderSandVolume,
  calculatePanelCount,
  calculateRecipeMaterialTotal,
  calculateSandVolume,
  calculateTableCount,
  calculateTotalFootCount,
  isFiniteNumber,
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
  'SAND',
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
      calculationNote: group.notes.join(' + '),
    });
  }

  return rows;
}

export function calculateMaterials(
  project: ProjectInput,
  calculations: CalculationInputs,
): CalculationResult {
  const errors: ValidationErrors = {};
  const contributions: MaterialContribution[] = [];
  const summary = emptySummary();

  const { panelTable, foundation, cableTrench, kiosk, bims } = calculations;

  if (
    panelTable.selectedTableRecipeId &&
    !getTableRecipe(panelTable.selectedTableRecipeId)
  ) {
    errors['panelTable.selectedTableRecipeId'] = MSG.invalidTableRecipe;
  }

  if (
    kiosk.selectedKioskRecipeId &&
    !getKioskRecipe(kiosk.selectedKioskRecipeId)
  ) {
    errors['kiosk.selectedKioskRecipeId'] = MSG.invalidKioskRecipe;
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

  if (
    cableTrench.trenchLengthM !== null &&
    cableTrench.trenchWidthM !== null &&
    cableTrench.sandHeightM !== null &&
    cableTrench.sandWastePercent !== null
  ) {
    const sandVolume = calculateSandVolume(
      cableTrench.trenchLengthM,
      cableTrench.trenchWidthM,
      cableTrench.sandHeightM,
    );
    const orderSand = calculateOrderSandVolume(
      sandVolume,
      cableTrench.sandWastePercent,
    );

    if (isFiniteNumber(sandVolume) && isFiniteNumber(orderSand)) {
      summary.sand = roundQuantity(orderSand, 'm³');
      pushContribution(contributions, {
        materialId: 'SAND',
        calculatedQuantity: sandVolume,
        orderQuantity: orderSand,
        wasteRatePercent: cableTrench.sandWastePercent,
        note: `${cableTrench.trenchLengthM} × ${cableTrench.trenchWidthM} × ${cableTrench.sandHeightM} m³, fire %${cableTrench.sandWastePercent}`,
      });
    }
  }

  if (kiosk.kioskCount !== null && kiosk.kioskCount >= 0) {
    const kioskPairs: Array<{
      materialId: MaterialId;
      perKiosk: number | null;
      label: string;
    }> = [
      {
        materialId: 'OG_COPPER_LUG',
        perKiosk: kiosk.ogCopperLugsPerKiosk,
        label: 'OG bakır pabuç',
      },
      {
        materialId: 'AG_COPPER_LUG',
        perKiosk: kiosk.agCopperLugsPerKiosk,
        label: 'AG bakır pabuç',
      },
      {
        materialId: 'GROUNDING_LUG',
        perKiosk: kiosk.groundingLugsPerKiosk,
        label: 'topraklama pabucu',
      },
      {
        materialId: 'CABLE_GLAND',
        perKiosk: kiosk.cableGlandsPerKiosk,
        label: 'kablo rakoru',
      },
      {
        materialId: 'BIMS_BLOCK',
        perKiosk: kiosk.bimsBlocksPerKiosk,
        label: 'bims (köşk)',
      },
    ];

    for (const pair of kioskPairs) {
      if (pair.perKiosk === null) {
        continue;
      }

      const total = calculateKioskMaterialTotal(
        kiosk.kioskCount,
        pair.perKiosk,
      );
      pushContribution(contributions, {
        materialId: pair.materialId,
        calculatedQuantity: total,
        orderQuantity: total,
        wasteRatePercent: null,
        note: `${kiosk.kioskCount} köşk × ${pair.perKiosk} ${pair.label}/köşk`,
      });
    }
  }

  if (
    bims.wallLengthM !== null &&
    bims.wallHeightM !== null &&
    bims.openingAreaM2 !== null
  ) {
    const netWallArea = calculateNetWallArea(
      bims.wallLengthM,
      bims.wallHeightM,
      bims.openingAreaM2,
    );

    if (netWallArea < 0) {
      errors['bims.openingAreaM2'] = MSG.openingExceedsWall;
    } else if (
      bims.bimsWidthM !== null &&
      bims.bimsHeightM !== null &&
      bims.bimsWastePercent !== null
    ) {
      const faceArea = bims.bimsWidthM * bims.bimsHeightM;
      if (faceArea <= 0) {
        errors['bims.bimsWidthM'] = MSG.bimsFacePositive;
        errors['bims.bimsHeightM'] = MSG.bimsFacePositive;
      } else {
        const netBims = calculateNetBimsCount(
          netWallArea,
          bims.bimsWidthM,
          bims.bimsHeightM,
        );
        const orderBims = calculateOrderBimsCount(
          netBims,
          bims.bimsWastePercent,
        );

        pushContribution(contributions, {
          materialId: 'BIMS_BLOCK',
          calculatedQuantity: netBims,
          orderQuantity: orderBims,
          wasteRatePercent: bims.bimsWastePercent,
          note: `ceil((${bims.wallLengthM}×${bims.wallHeightM} − ${bims.openingAreaM2}) / (${bims.bimsWidthM}×${bims.bimsHeightM})), fire %${bims.bimsWastePercent}`,
        });
      }
    }
  }

  const materialRows = aggregateContributions(contributions);
  const bimsRow = materialRows.find((row) => row.id === 'BIMS_BLOCK');
  summary.bims = bimsRow?.orderQuantity ?? null;

  return {
    summary,
    materialRows,
    validationErrors: errors,
  };
}
