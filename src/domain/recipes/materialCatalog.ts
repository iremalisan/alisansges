import type { MaterialDefinition, MaterialId } from '../types';

export const MATERIAL_CATALOG: Record<MaterialId, MaterialDefinition> = {
  PANEL: {
    id: 'PANEL',
    name: 'Panel',
    category: 'PV',
    unit: 'adet',
  },
  TABLE: {
    id: 'TABLE',
    name: 'Masa',
    category: 'Konstrüksiyon',
    unit: 'adet',
  },
  FOUNDATION_FOOT: {
    id: 'FOUNDATION_FOOT',
    name: 'Toplam Ayak',
    category: 'Konstrüksiyon',
    unit: 'adet',
  },
  STEEL_POST: {
    id: 'STEEL_POST',
    name: 'Çelik Dikme',
    category: 'Mekanik',
    unit: 'adet',
  },
  PURLIN: {
    id: 'PURLIN',
    name: 'Purlin',
    category: 'Mekanik',
    unit: 'adet',
  },
  DIAGONAL_BRACE: {
    id: 'DIAGONAL_BRACE',
    name: 'Çapraz Destek',
    category: 'Mekanik',
    unit: 'adet',
  },
  MID_CLAMP: {
    id: 'MID_CLAMP',
    name: 'Orta Kelepçe',
    category: 'Mekanik',
    unit: 'adet',
  },
  END_CLAMP: {
    id: 'END_CLAMP',
    name: 'Uç Kelepçe',
    category: 'Mekanik',
    unit: 'adet',
  },
  BOLT: {
    id: 'BOLT',
    name: 'Cıvata',
    category: 'Mekanik',
    unit: 'adet',
  },
  CONCRETE: {
    id: 'CONCRETE',
    name: 'Beton',
    category: 'İnşaat',
    unit: 'm³',
  },
  SAND: {
    id: 'SAND',
    name: 'Kum',
    category: 'İnşaat',
    unit: 'm³',
  },
  OG_COPPER_LUG: {
    id: 'OG_COPPER_LUG',
    name: 'OG Bakır Pabuç',
    category: 'Elektrik',
    unit: 'adet',
  },
  AG_COPPER_LUG: {
    id: 'AG_COPPER_LUG',
    name: 'AG Bakır Pabuç',
    category: 'Elektrik',
    unit: 'adet',
  },
  GROUNDING_LUG: {
    id: 'GROUNDING_LUG',
    name: 'Topraklama Pabucu',
    category: 'Elektrik',
    unit: 'adet',
  },
  CABLE_GLAND: {
    id: 'CABLE_GLAND',
    name: 'Kablo Rakorı',
    category: 'Elektrik',
    unit: 'adet',
  },
  BIMS_BLOCK: {
    id: 'BIMS_BLOCK',
    name: 'Bims',
    category: 'İnşaat',
    unit: 'adet',
  },
};

export function getMaterial(id: MaterialId): MaterialDefinition {
  return MATERIAL_CATALOG[id];
}
