/** Pure numeric formulas for GES Metraj Pro. */

export function calculatePanelCount(
  plantPowerMWp: number,
  panelPowerWp: number,
): number {
  return Math.ceil((plantPowerMWp * 1_000_000) / panelPowerWp);
}

export function calculateTableCount(
  panelCount: number,
  panelsPerTable: number,
): number {
  return Math.ceil(panelCount / panelsPerTable);
}

export function calculateTotalFootCount(
  tableCount: number,
  feetPerTable: number,
): number {
  return tableCount * feetPerTable;
}

export function calculateConcreteFootCountFromPercent(
  totalFootCount: number,
  concreteFootPercentage: number,
): number {
  return Math.ceil((totalFootCount * concreteFootPercentage) / 100);
}

export function calculateConcreteVolumePerFoot(
  pitWidthM: number,
  pitLengthM: number,
  pitDepthM: number,
): number {
  return pitWidthM * pitLengthM * pitDepthM;
}

export function calculateNetConcreteVolume(
  concreteFootCount: number,
  concreteVolumePerFoot: number,
): number {
  return concreteFootCount * concreteVolumePerFoot;
}

export function calculateOrderConcreteVolume(
  netConcreteVolume: number,
  concreteWastePercent: number,
): number {
  return netConcreteVolume * (1 + concreteWastePercent / 100);
}

export function calculateSandVolume(
  trenchLengthM: number,
  trenchWidthM: number,
  sandHeightM: number,
): number {
  return trenchLengthM * trenchWidthM * sandHeightM;
}

export function calculateOrderSandVolume(
  sandVolume: number,
  sandWastePercent: number,
): number {
  return sandVolume * (1 + sandWastePercent / 100);
}

export function calculateExcavationVolume(
  lengthM: number,
  widthM: number,
  depthM: number,
): number {
  return lengthM * widthM * depthM;
}

export function calculateOrderCableLength(
  cableLengthM: number,
  cableWastePercent: number,
): number {
  return cableLengthM * (1 + cableWastePercent / 100);
}

export function calculateRunLength(
  lengthM: number,
  runs: number,
): number {
  return lengthM * runs;
}

export function calculateKioskMaterialTotal(
  kioskCount: number,
  perKioskQuantity: number,
): number {
  return kioskCount * perKioskQuantity;
}

export function calculateGrossWallArea(
  wallLengthM: number,
  wallHeightM: number,
): number {
  return wallLengthM * wallHeightM;
}

export function calculateNetWallArea(
  wallLengthM: number,
  wallHeightM: number,
  openingAreaM2: number,
): number {
  return wallLengthM * wallHeightM - openingAreaM2;
}

export function calculateNetBimsCount(
  netWallArea: number,
  bimsWidthM: number,
  bimsHeightM: number,
): number {
  return Math.ceil(netWallArea / (bimsWidthM * bimsHeightM));
}

export function calculateOrderBimsCount(
  netBimsCount: number,
  bimsWastePercent: number,
): number {
  return Math.ceil(netBimsCount * (1 + bimsWastePercent / 100));
}

export function calculateRecipeMaterialTotal(
  tableCount: number,
  quantityPerTable: number,
): number {
  return tableCount * quantityPerTable;
}

export function isFiniteNumber(value: number): boolean {
  return Number.isFinite(value);
}

export function isNonNegativeInteger(value: number): boolean {
  return Number.isInteger(value) && value >= 0;
}
