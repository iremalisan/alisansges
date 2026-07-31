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
  /** Reserved for a later step — not applied globally in PR-002. */
  generalWastePercent: number | null;
}

/** @deprecated Prefer ProjectInput — kept as alias for existing imports. */
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

export interface CableTrenchInputs {
  trenchLengthM: number | null;
  trenchWidthM: number | null;
  sandHeightM: number | null;
  sandWastePercent: number | null;
}

export interface KioskInputs {
  selectedKioskRecipeId: string | null;
  kioskCount: number | null;
  ogCopperLugsPerKiosk: number | null;
  agCopperLugsPerKiosk: number | null;
  groundingLugsPerKiosk: number | null;
  cableGlandsPerKiosk: number | null;
  bimsBlocksPerKiosk: number | null;
}

export interface BimsInputs {
  wallLengthM: number | null;
  wallHeightM: number | null;
  openingAreaM2: number | null;
  bimsWidthM: number | null;
  bimsHeightM: number | null;
  bimsWastePercent: number | null;
}

export interface CalculationInputs {
  panelTable: PanelTableInputs;
  foundation: FoundationInputs;
  cableTrench: CableTrenchInputs;
  kiosk: KioskInputs;
  bims: BimsInputs;
}

export type ValidationFieldKey =
  | keyof ProjectInput
  | `panelTable.${keyof PanelTableInputs}`
  | `foundation.${keyof FoundationInputs}`
  | `cableTrench.${keyof CableTrenchInputs}`
  | `kiosk.${keyof KioskInputs}`
  | `bims.${keyof BimsInputs}`;

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

export interface CalculationResult {
  summary: SummaryValues;
  materialRows: MaterialResultRow[];
  validationErrors: ValidationErrors;
}

export interface AppState {
  project: ProjectInput;
  calculations: CalculationInputs;
  validationErrors: ValidationErrors;
  materialRows: MaterialResultRow[];
  summary: SummaryValues;
}

export type AppSectionId =
  | 'project'
  | 'panel-table'
  | 'foundation'
  | 'cable-trench'
  | 'kiosk'
  | 'bims'
  | 'materials';
