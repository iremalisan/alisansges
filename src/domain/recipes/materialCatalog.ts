import type { MaterialDefinition, MaterialId, TrenchType } from '../types';

export const MATERIAL_CATALOG: Record<MaterialId, MaterialDefinition> = {
  PANEL: { id: 'PANEL', name: 'Panel', category: 'PV', unit: 'adet' },
  TABLE: { id: 'TABLE', name: 'Masa', category: 'Konstrüksiyon', unit: 'adet' },
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
  PURLIN: { id: 'PURLIN', name: 'Purlin', category: 'Mekanik', unit: 'adet' },
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
  BOLT: { id: 'BOLT', name: 'Cıvata', category: 'Mekanik', unit: 'adet' },
  CONCRETE: {
    id: 'CONCRETE',
    name: 'Beton',
    category: 'İnşaat',
    unit: 'm³',
  },
  SAND: { id: 'SAND', name: 'Kum', category: 'İnşaat', unit: 'm³' },
  EXCAVATION: {
    id: 'EXCAVATION',
    name: 'Kazı',
    category: 'İnşaat',
    unit: 'm³',
  },
  DC_CABLE: {
    id: 'DC_CABLE',
    name: 'DC Kablo',
    category: 'Kablo',
    unit: 'm',
  },
  AC_CABLE: {
    id: 'AC_CABLE',
    name: 'AC Kablo',
    category: 'Kablo',
    unit: 'm',
  },
  MV_CABLE: {
    id: 'MV_CABLE',
    name: 'OG Kablo',
    category: 'Kablo',
    unit: 'm',
  },
  COMMUNICATION_CABLE: {
    id: 'COMMUNICATION_CABLE',
    name: 'Haberleşme Kablosu',
    category: 'Kablo',
    unit: 'm',
  },
  GROUNDING_CABLE: {
    id: 'GROUNDING_CABLE',
    name: 'Topraklama Kablosu',
    category: 'Kablo',
    unit: 'm',
  },
  OTHER_CABLE: {
    id: 'OTHER_CABLE',
    name: 'Diğer Kablo',
    category: 'Kablo',
    unit: 'm',
  },
  WARNING_TAPE: {
    id: 'WARNING_TAPE',
    name: 'Uyarı Bandı',
    category: 'Kablo',
    unit: 'm',
  },
  CABLE_PROTECTION_PLATE: {
    id: 'CABLE_PROTECTION_PLATE',
    name: 'Kablo Koruma Plakası',
    category: 'Kablo',
    unit: 'm',
  },
  CONDUIT: {
    id: 'CONDUIT',
    name: 'Korruge / Boru',
    category: 'Kablo',
    unit: 'm',
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

export function cableMaterialForTrenchType(type: TrenchType): MaterialId {
  switch (type) {
    case 'DC':
      return 'DC_CABLE';
    case 'AC':
      return 'AC_CABLE';
    case 'OG':
      return 'MV_CABLE';
    case 'Haberleşme':
      return 'COMMUNICATION_CABLE';
    case 'Topraklama':
      return 'GROUNDING_CABLE';
    case 'Diğer':
      return 'OTHER_CABLE';
  }
}
