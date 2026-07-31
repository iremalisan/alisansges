import type { AppSectionId } from './types';

export interface NavItem {
  id: AppSectionId;
  label: string;
}

export const NAV_ITEMS: NavItem[] = [
  { id: 'project', label: 'Proje Bilgileri' },
  { id: 'panel-table', label: 'Panel ve Masa' },
  { id: 'foundation', label: 'Ayak ve Beton' },
  { id: 'cable-trench', label: 'Kablo Kanalı ve Kum' },
  { id: 'kiosk', label: 'Beton Köşk ve Bakır Pabuç' },
  { id: 'bims', label: 'Bims Duvar' },
  { id: 'materials', label: 'Malzeme Listesi' },
];
