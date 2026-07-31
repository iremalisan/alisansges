import { describe, expect, it, beforeEach } from 'vitest';
import { calculateMaterials, MSG } from './calculate';
import {
  calculateExcavationVolume,
  calculateOrderCableLength,
  calculatePanelCount,
  calculateRunLength,
  calculateSandVolume,
  calculateTableCount,
  calculateTotalFootCount,
} from './formulas';
import {
  sampleCalculationInputs,
  sampleProjectInputs,
} from '../sampleProject';
import { emptyCalculationInputs, emptyProjectInputs } from '../defaults';
import {
  applyKioskRecipeToGroup,
  createEmptyTrench,
  createFixedKioskGroup,
  createFixedTrench,
  createFixedWall,
} from '../entries';
import { resetIdSequence } from '../ids';
import type { CalculationInputs } from '../types';
import { cableMaterialForTrenchType } from '../recipes/materialCatalog';

beforeEach(() => {
  resetIdSequence(0);
});

describe('formulas (PR-002 retained)', () => {
  it('calculates 90 MWp / 700 Wp as 128572 panels', () => {
    expect(calculatePanelCount(90, 700)).toBe(128572);
  });

  it('rounds table count up and calculates total feet', () => {
    expect(calculateTableCount(128572, 56)).toBe(2296);
    expect(calculateTotalFootCount(2296, 8)).toBe(18368);
  });
});

describe('trench formulas', () => {
  it('calculates excavation and dual sand layers', () => {
    expect(calculateExcavationVolume(4500, 0.6, 0.8)).toBe(2160);
    expect(calculateSandVolume(4500, 0.6, 0.1)).toBe(270);
  });

  it('applies cable waste and run multipliers', () => {
    expect(calculateOrderCableLength(2750, 3)).toBeCloseTo(2832.5, 6);
    expect(calculateRunLength(2500, 1)).toBe(2500);
  });

  it('maps trench types to cable material IDs', () => {
    expect(cableMaterialForTrenchType('DC')).toBe('DC_CABLE');
    expect(cableMaterialForTrenchType('OG')).toBe('MV_CABLE');
    expect(cableMaterialForTrenchType('Haberleşme')).toBe(
      'COMMUNICATION_CABLE',
    );
  });
});

describe('calculateMaterials multi-entry', () => {
  it('keeps the 90 MWp panel result', () => {
    const result = calculateMaterials(
      sampleProjectInputs(),
      sampleCalculationInputs(),
    );
    expect(result.summary.panel).toBe(128572);
    expect(result.summary.table).toBe(2296);
    expect(result.summary.totalLegs).toBe(18368);
  });

  it('aggregates sand and excavation across trenches', () => {
    const result = calculateMaterials(
      sampleProjectInputs(),
      sampleCalculationInputs(),
    );

    expect(result.summary.sand).toBeCloseTo(1260, 3);
    const excavation = result.materialRows.find((r) => r.id === 'EXCAVATION');
    expect(excavation?.orderQuantity).toBeCloseTo(4720, 3);
  });

  it('maps cables with waste and skips zero runs', () => {
    const result = calculateMaterials(
      sampleProjectInputs(),
      sampleCalculationInputs(),
    );

    const dc = result.materialRows.find((r) => r.id === 'DC_CABLE');
    const mv = result.materialRows.find((r) => r.id === 'MV_CABLE');
    const conduit = result.materialRows.find((r) => r.id === 'CONDUIT');
    const tape = result.materialRows.find((r) => r.id === 'WARNING_TAPE');

    expect(dc?.orderQuantity).toBeCloseTo(9888, 3);
    expect(mv?.orderQuantity).toBeCloseTo(2832.5, 3);
    expect(conduit?.orderQuantity).toBe(4000);
    expect(tape?.orderQuantity).toBe(8500);
  });

  it('aggregates multiple kiosk groups and walls into one BIMS row', () => {
    const result = calculateMaterials(
      sampleProjectInputs(),
      sampleCalculationInputs(),
    );

    const bims = result.materialRows.filter((r) => r.id === 'BIMS_BLOCK');
    expect(bims).toHaveLength(1);
    // 10*600 + 2*900 + 2888 + 1182 = 11870
    expect(bims[0].orderQuantity).toBe(11870);
    expect(result.summary.bims).toBe(11870);
  });

  it('aggregates OG copper lugs across kiosk groups', () => {
    const result = calculateMaterials(
      sampleProjectInputs(),
      sampleCalculationInputs(),
    );
    const og = result.materialRows.find((r) => r.id === 'OG_COPPER_LUG');
    expect(og?.orderQuantity).toBe(10 * 24 + 2 * 36);
  });

  it('uses edited kiosk values instead of recipe defaults', () => {
    const base = sampleCalculationInputs();
    const calculations: CalculationInputs = {
      ...base,
      kioskGroups: base.kioskGroups.map((group, index) =>
        index === 0
          ? { ...group, ogCopperLugPerKiosk: 5, count: 2 }
          : group,
      ),
    };

    const result = calculateMaterials(sampleProjectInputs(), calculations);
    const og = result.materialRows.find((r) => r.id === 'OG_COPPER_LUG');
    expect(og?.orderQuantity).toBe(2 * 5 + 2 * 36);
  });

  it('isolates validation errors between trench rows', () => {
    const calculations: CalculationInputs = {
      ...emptyCalculationInputs(),
      trenches: [
        createFixedTrench('ok', {
          name: 'OK',
          type: 'DC',
          lengthM: 10,
          widthM: 0.5,
          depthM: 0.5,
          lowerSandHeightM: 0.1,
          upperSandHeightM: 0.1,
          sandWastePercent: 5,
          cableLengthM: 0,
          cableWastePercent: 0,
          warningTapeRuns: 0,
          protectionPlateRuns: 0,
          conduitRuns: 0,
        }),
        createFixedTrench('bad', {
          name: 'BAD',
          type: 'AC',
          lengthM: 10,
          widthM: 0,
          depthM: 0.5,
          lowerSandHeightM: 0.1,
          upperSandHeightM: 0.1,
          sandWastePercent: 5,
          cableLengthM: null,
          cableWastePercent: null,
          warningTapeRuns: 0,
          protectionPlateRuns: 0,
          conduitRuns: 0,
        }),
      ],
    };

    const result = calculateMaterials(emptyProjectInputs(), calculations);
    expect(result.validationErrors['trench.trench-bad.widthM']).toBe(
      MSG.widthPositive,
    );
    expect(result.trenchSummaries['trench-ok'].excavationM3).toBeCloseTo(2.5, 3);
    expect(result.trenchSummaries['trench-bad'].excavationM3).toBeNull();
  });

  it('rejects sand heights exceeding trench depth', () => {
    const calculations: CalculationInputs = {
      ...emptyCalculationInputs(),
      trenches: [
        createFixedTrench('deep', {
          name: 'Deep',
          type: 'DC',
          lengthM: 10,
          widthM: 1,
          depthM: 0.2,
          lowerSandHeightM: 0.15,
          upperSandHeightM: 0.15,
          sandWastePercent: 5,
          cableLengthM: null,
          cableWastePercent: null,
          warningTapeRuns: 0,
          protectionPlateRuns: 0,
          conduitRuns: 0,
        }),
      ],
    };

    const result = calculateMaterials(emptyProjectInputs(), calculations);
    expect(result.validationErrors['trench.trench-deep.lowerSandHeightM']).toBe(
      MSG.sandExceedsDepth,
    );
  });

  it('rejects wall openings larger than gross area without breaking other walls', () => {
    const calculations: CalculationInputs = {
      ...emptyCalculationInputs(),
      walls: [
        createFixedWall('good', {
          name: 'Good',
          lengthM: 10,
          heightM: 2,
          openingAreaM2: 1,
          bimsWidthM: 0.4,
          bimsHeightM: 0.2,
          bimsWastePercent: 5,
        }),
        createFixedWall('bad', {
          name: 'Bad',
          lengthM: 10,
          heightM: 2,
          openingAreaM2: 50,
          bimsWidthM: 0.4,
          bimsHeightM: 0.2,
          bimsWastePercent: 5,
        }),
      ],
    };

    const result = calculateMaterials(emptyProjectInputs(), calculations);
    expect(result.validationErrors['wall.wall-bad.openingAreaM2']).toBe(
      MSG.openingExceedsWall,
    );
    expect(result.wallSummaries['wall-good'].orderBimsCount).not.toBeNull();
  });

  it('does not emit NaN or Infinity for partial multi-entry inputs', () => {
    const calculations: CalculationInputs = {
      ...emptyCalculationInputs(),
      trenches: [createEmptyTrench({ name: 'Partial', lengthM: 5 })],
      kioskGroups: [
        createFixedKioskGroup('partial', {
          name: 'Partial',
          recipeId: null,
          count: 1,
          ogCopperLugPerKiosk: null,
          agCopperLugPerKiosk: null,
          groundingLugPerKiosk: null,
          cableGlandPerKiosk: null,
          bimsBlockPerKiosk: null,
        }),
      ],
      walls: [
        createFixedWall('partial', {
          name: 'Partial',
          lengthM: 4,
          heightM: null,
          openingAreaM2: null,
          bimsWidthM: null,
          bimsHeightM: null,
          bimsWastePercent: null,
        }),
      ],
    };

    const result = calculateMaterials(
      { ...emptyProjectInputs(), plantPowerMWp: 1 },
      calculations,
    );

    for (const row of result.materialRows) {
      if (row.calculatedQuantity !== null) {
        expect(Number.isFinite(row.calculatedQuantity)).toBe(true);
      }
      if (row.orderQuantity !== null) {
        expect(Number.isFinite(row.orderQuantity)).toBe(true);
      }
    }
  });

  it('supports independent recipe population for kiosk groups', () => {
    const group = applyKioskRecipeToGroup(
      createFixedKioskGroup('r', {
        name: 'R',
        recipeId: null,
        count: 1,
        ogCopperLugPerKiosk: null,
        agCopperLugPerKiosk: null,
        groundingLugPerKiosk: null,
        cableGlandPerKiosk: null,
        bimsBlockPerKiosk: null,
      }),
      'standard-concrete-kiosk',
    );

    expect(group.ogCopperLugPerKiosk).toBe(24);
    expect(group.bimsBlockPerKiosk).toBe(600);
  });
});
