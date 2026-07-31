import { describe, expect, it } from 'vitest';
import { calculateMaterials, MSG } from './calculate';
import {
  calculateConcreteFootCountFromPercent,
  calculateConcreteVolumePerFoot,
  calculateNetBimsCount,
  calculateNetWallArea,
  calculateOrderBimsCount,
  calculateOrderConcreteVolume,
  calculateOrderSandVolume,
  calculatePanelCount,
  calculateRecipeMaterialTotal,
  calculateSandVolume,
  calculateTableCount,
  calculateTotalFootCount,
  calculateKioskMaterialTotal,
} from './formulas';
import {
  sampleCalculationInputs,
  sampleProjectInputs,
} from '../sampleProject';
import { emptyCalculationInputs, emptyProjectInputs } from '../defaults';
import type { CalculationInputs, ProjectInput } from '../types';

describe('formulas', () => {
  it('calculates 90 MWp / 700 Wp as 128572 panels', () => {
    expect(calculatePanelCount(90, 700)).toBe(128572);
  });

  it('rounds table count up', () => {
    expect(calculateTableCount(128572, 56)).toBe(2296);
  });

  it('calculates total feet', () => {
    expect(calculateTotalFootCount(2296, 8)).toBe(18368);
  });

  it('supports percentage concrete foot mode', () => {
    expect(calculateConcreteFootCountFromPercent(18368, 10)).toBe(1837);
  });

  it('calculates concrete volume and waste', () => {
    const perFoot = calculateConcreteVolumePerFoot(0.45, 0.45, 1.2);
    expect(perFoot).toBeCloseTo(0.243, 6);
    const net = 1837 * perFoot;
    const order = calculateOrderConcreteVolume(net, 5);
    expect(order).toBeCloseTo(net * 1.05, 6);
  });

  it('calculates sand volume and waste', () => {
    const sand = calculateSandVolume(8500, 0.6, 0.2);
    expect(sand).toBe(1020);
    expect(calculateOrderSandVolume(sand, 5)).toBeCloseTo(1071, 6);
  });

  it('validates wall area and bims counts', () => {
    expect(calculateNetWallArea(80, 3, 20)).toBe(220);
    expect(calculateNetWallArea(10, 2, 30)).toBeLessThan(0);
    expect(calculateNetBimsCount(220, 0.4, 0.2)).toBe(2750);
    expect(calculateOrderBimsCount(2750, 5)).toBe(2888);
  });

  it('multiplies recipe and kiosk quantities', () => {
    expect(calculateRecipeMaterialTotal(10, 8)).toBe(80);
    expect(calculateKioskMaterialTotal(10, 24)).toBe(240);
  });
});

describe('calculateMaterials', () => {
  it('returns exact panel count for the 90 MWp example project', () => {
    const result = calculateMaterials(
      sampleProjectInputs(),
      sampleCalculationInputs(),
    );

    expect(result.summary.panel).toBe(128572);
    expect(result.summary.table).toBe(2296);
    expect(result.summary.totalLegs).toBe(18368);
    expect(result.summary.sand).toBeCloseTo(1071, 3);
    expect(result.materialRows.some((row) => row.id === 'PANEL')).toBe(true);
  });

  it('supports manual concrete foot mode', () => {
    const project = sampleProjectInputs();
    const calculations: CalculationInputs = {
      ...sampleCalculationInputs(),
      foundation: {
        ...sampleCalculationInputs().foundation,
        concreteFootMode: 'count',
        concreteLegsCount: 100,
        concreteLegsPercent: null,
      },
    };

    const result = calculateMaterials(project, calculations);
    expect(result.validationErrors['foundation.concreteLegsCount']).toBeUndefined();
    expect(result.summary.concrete).not.toBeNull();
  });

  it('rejects concrete count exceeding total feet', () => {
    const calculations: CalculationInputs = {
      ...sampleCalculationInputs(),
      foundation: {
        ...sampleCalculationInputs().foundation,
        concreteFootMode: 'count',
        concreteLegsCount: 999999,
      },
    };

    const result = calculateMaterials(sampleProjectInputs(), calculations);
    expect(result.validationErrors['foundation.concreteLegsCount']).toBe(
      MSG.concreteExceedsTotal,
    );
    expect(result.summary.concrete).toBeNull();
  });

  it('rejects wall openings larger than gross wall area', () => {
    const calculations: CalculationInputs = {
      ...sampleCalculationInputs(),
      bims: {
        ...sampleCalculationInputs().bims,
        openingAreaM2: 9999,
      },
    };

    const result = calculateMaterials(sampleProjectInputs(), calculations);
    expect(result.validationErrors['bims.openingAreaM2']).toBe(
      MSG.openingExceedsWall,
    );
  });

  it('aggregates duplicate BIMS_BLOCK from kiosk and wall', () => {
    const result = calculateMaterials(
      sampleProjectInputs(),
      sampleCalculationInputs(),
    );

    const bimsRows = result.materialRows.filter((row) => row.id === 'BIMS_BLOCK');
    expect(bimsRows).toHaveLength(1);
    expect(bimsRows[0].orderQuantity).toBe(6000 + 2888);
    expect(bimsRows[0].calculationNote).toContain('köşk');
    expect(bimsRows[0].calculationNote).toContain('ceil');
  });

  it('multiplies table recipe materials by table count', () => {
    const result = calculateMaterials(
      sampleProjectInputs(),
      sampleCalculationInputs(),
    );

    const posts = result.materialRows.find((row) => row.id === 'STEEL_POST');
    expect(posts?.orderQuantity).toBe(2296 * 8);
  });

  it('multiplies kiosk recipe materials by kiosk count', () => {
    const result = calculateMaterials(
      sampleProjectInputs(),
      sampleCalculationInputs(),
    );

    const og = result.materialRows.find((row) => row.id === 'OG_COPPER_LUG');
    expect(og?.orderQuantity).toBe(10 * 24);
  });

  it('does not emit NaN or Infinity for partial inputs', () => {
    const project: ProjectInput = {
      ...emptyProjectInputs(),
      plantPowerMWp: 10,
    };
    const calculations = emptyCalculationInputs();
    const result = calculateMaterials(project, calculations);

    for (const row of result.materialRows) {
      if (row.calculatedQuantity !== null) {
        expect(Number.isFinite(row.calculatedQuantity)).toBe(true);
      }
      if (row.orderQuantity !== null) {
        expect(Number.isFinite(row.orderQuantity)).toBe(true);
      }
    }

    for (const value of Object.values(result.summary)) {
      if (value !== null) {
        expect(Number.isFinite(value)).toBe(true);
      }
    }
  });

  it('rejects invalid recipe selection', () => {
    const calculations: CalculationInputs = {
      ...emptyCalculationInputs(),
      panelTable: {
        selectedTableRecipeId: 'missing-recipe',
        panelsPerTable: 10,
        legsPerTable: 4,
      },
      kiosk: {
        ...emptyCalculationInputs().kiosk,
        selectedKioskRecipeId: 'missing-kiosk',
      },
    };

    const result = calculateMaterials(emptyProjectInputs(), calculations);
    expect(result.validationErrors['panelTable.selectedTableRecipeId']).toBe(
      MSG.invalidTableRecipe,
    );
    expect(result.validationErrors['kiosk.selectedKioskRecipeId']).toBe(
      MSG.invalidKioskRecipe,
    );
  });

  it('rejects zero panel/plant power and zero face dimensions', () => {
    const result = calculateMaterials(
      { ...sampleProjectInputs(), plantPowerMWp: 0, panelPowerWp: 0 },
      {
        ...sampleCalculationInputs(),
        bims: {
          ...sampleCalculationInputs().bims,
          bimsWidthM: 0,
          bimsHeightM: 0,
        },
      },
    );

    expect(result.validationErrors.plantPowerMWp).toBe(MSG.plantPowerPositive);
    expect(result.validationErrors.panelPowerWp).toBe(MSG.panelPowerPositive);
    expect(result.validationErrors['bims.bimsWidthM']).toBe(MSG.bimsFacePositive);
  });
});
