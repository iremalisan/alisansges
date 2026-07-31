/** Domain models for GES Metraj Pro. */

export type MaterialId =
  | 'PANEL'
  | 'TABLE'
  | 'FOUNDATION_FOOT'
  | 'STEEL_POST'
  | 'PURLIN'
  | 'DIAGONAL_BRACE'
  | 'MID_CLAMP'
  | 'END_CLAMP'
  | 'BOLT'
  | 'CONCRETE'
  | 'SAND'
  | 'EXCAVATION'
  | 'DC_CABLE'
  | 'AC_CABLE'
  | 'MV_CABLE'
  | 'COMMUNICATION_CABLE'
  | 'GROUNDING_CABLE'
  | 'OTHER_CABLE'
  | 'WARNING_TAPE'
  | 'CABLE_PROTECTION_PLATE'
  | 'CONDUIT'
  | 'OG_COPPER_LUG'
  | 'AG_COPPER_LUG'
  | 'GROUNDING_LUG'
  | 'CABLE_GLAND'
  | 'BIMS_BLOCK';

export type MaterialUnit = 'adet' | 'm' | 'm²' | 'm³';

export interface MaterialDefinition {
  id: MaterialId;
  name: string;
  category: string;
  unit: MaterialUnit;
}

export interface ProjectInput {
  projectName: string;
  plantPowerMWp: number | null;
  panelPowerWp: number | null;
  /** Reserved — not applied globally yet. */
  generalWastePercent: number | null;
}

export type ProjectInputs = ProjectInput;

export interface TableRecipeItem {
  materialId: MaterialId;
  quantityPerTable: number;
}

export interface TableRecipe {
  id: string;
  name: string;
  panelsPerTable: number;
  feetPerTable: number;
  items: TableRecipeItem[];
}

export interface KioskRecipeItem {
  materialId: MaterialId;
  quantityPerKiosk: number;
}

export interface KioskRecipe {
  id: string;
  name: string;
  items: KioskRecipeItem[];
}

export interface PanelTableInputs {
  selectedTableRecipeId: string | null;
  panelsPerTable: number | null;
  legsPerTable: number | null;
}

export type ConcreteFootMode = 'count' | 'percent';

export interface FoundationInputs {
  concreteFootMode: ConcreteFootMode;
  concreteLegsCount: number | null;
  concreteLegsPercent: number | null;
  pitWidthM: number | null;
  pitLengthM: number | null;
  pitDepthM: number | null;
  concreteWastePercent: number | null;
}

export type TrenchType =
  | 'DC'
  | 'AC'
  | 'OG'
  | 'Haberleşme'
  | 'Topraklama'
  | 'Diğer';

export interface CableTrenchInput {
  id: string;
  name: string;
  type: TrenchType;
  lengthM: number | null;
  widthM: number | null;
  depthM: number | null;
  lowerSandHeightM: number | null;
  upperSandHeightM: number | null;
  sandWastePercent: number | null;
  cableLengthM: number | null;
  cableWastePercent: number | null;
  warningTapeRuns: number | null;
  protectionPlateRuns: number | null;
  conduitRuns: number | null;
}

export interface KioskGroupInput {
  id: string;
  name: string;
  recipeId: string | null;
  count: number | null;
  ogCopperLugPerKiosk: number | null;
  agCopperLugPerKiosk: number | null;
  groundingLugPerKiosk: number | null;
  cableGlandPerKiosk: number | null;
  bimsBlockPerKiosk: number | null;
}

export interface WallInput {
  id: string;
  name: string;
  lengthM: number | null;
  heightM: number | null;
  openingAreaM2: number | null;
  bimsWidthM: number | null;
  bimsHeightM: number | null;
  bimsWastePercent: number | null;
}

export interface CalculationInputs {
  panelTable: PanelTableInputs;
  foundation: FoundationInputs;
  trenches: CableTrenchInput[];
  kioskGroups: KioskGroupInput[];
  walls: WallInput[];
}

export type ValidationFieldKey =
  | keyof ProjectInput
  | `panelTable.${keyof PanelTableInputs}`
  | `foundation.${keyof FoundationInputs}`
  | `trench.${string}.${keyof CableTrenchInput}`
  | `kioskGroup.${string}.${keyof KioskGroupInput}`
  | `wall.${string}.${keyof WallInput}`;

export interface ValidationError {
  field: ValidationFieldKey;
  message: string;
}

export type ValidationErrors = Partial<Record<ValidationFieldKey, string>>;

export interface MaterialResultRow {
  id: MaterialId | string;
  category: string;
  material: string;
  calculatedQuantity: number | null;
  unit: MaterialUnit | string;
  wasteRatePercent: number | null;
  orderQuantity: number | null;
  calculationNote: string;
}

export interface SummaryValues {
  panel: number | null;
  table: number | null;
  totalLegs: number | null;
  concrete: number | null;
  sand: number | null;
  bims: number | null;
}

export interface TrenchRowSummary {
  excavationM3: number | null;
  sandOrderM3: number | null;
  cableOrderM: number | null;
}

export interface WallRowSummary {
  grossAreaM2: number | null;
  netAreaM2: number | null;
  orderBimsCount: number | null;
}

export interface CalculationResult {
  summary: SummaryValues;
  materialRows: MaterialResultRow[];
  validationErrors: ValidationErrors;
  trenchSummaries: Record<string, TrenchRowSummary>;
  wallSummaries: Record<string, WallRowSummary>;
}

export interface AppState {
  project: ProjectInput;
  calculations: CalculationInputs;
  validationErrors: ValidationErrors;
  materialRows: MaterialResultRow[];
  summary: SummaryValues;
  trenchSummaries: Record<string, TrenchRowSummary>;
  wallSummaries: Record<string, WallRowSummary>;
}

export type AppSectionId =
  | 'project'
  | 'panel-table'
  | 'foundation'
  | 'cable-trench'
  | 'kiosk'
  | 'bims'
  | 'materials';

export const TRENCH_TYPES: TrenchType[] = [
  'DC',
  'AC',
  'OG',
  'Haberleşme',
  'Topraklama',
  'Diğer',
];
