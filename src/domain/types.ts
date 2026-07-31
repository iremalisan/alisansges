/** Domain models for GES Metraj Pro (PR-001 placeholders). */

export interface ProjectInputs {
  projectName: string;
  plantPowerMWp: number | null;
  panelPowerWp: number | null;
  generalWastePercent: number | null;
}

export interface PanelTableInputs {
  panelsPerTable: number | null;
  legsPerTable: number | null;
}

export interface FoundationInputs {
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
  kioskCount: number | null;
  ogCopperLugsPerKiosk: number | null;
  agCopperLugsPerKiosk: number | null;
  groundingLugsPerKiosk: number | null;
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
  | keyof ProjectInputs
  | `panelTable.${keyof PanelTableInputs}`
  | `foundation.${keyof FoundationInputs}`
  | `cableTrench.${keyof CableTrenchInputs}`
  | `kiosk.${keyof KioskInputs}`
  | `bims.${keyof BimsInputs}`;

export type ValidationErrors = Partial<Record<ValidationFieldKey, string>>;

export interface MaterialResultRow {
  id: string;
  category: string;
  material: string;
  calculatedQuantity: number | null;
  unit: string;
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

export interface AppState {
  project: ProjectInputs;
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
