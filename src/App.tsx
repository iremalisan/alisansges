import { useState } from 'react';
import { AppHeader } from './components/AppHeader';
import { SidebarNav } from './components/SidebarNav';
import type { AppSectionId } from './domain/types';
import { BimsSection } from './sections/BimsSection';
import { CableTrenchSection } from './sections/CableTrenchSection';
import { FoundationSection } from './sections/FoundationSection';
import { KioskSection } from './sections/KioskSection';
import { MaterialsSection } from './sections/MaterialsSection';
import { PanelTableSection } from './sections/PanelTableSection';
import { ProjectSection } from './sections/ProjectSection';
import { useAppState } from './state/useAppState';
import './App.css';

function scrollToSection(sectionId: AppSectionId) {
  const element = document.getElementById(sectionId);
  if (element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
}

export default function App() {
  const {
    state,
    updateProject,
    updatePanelTable,
    updateFoundation,
    updateCableTrench,
    updateKiosk,
    updateBims,
    setValidationError,
    loadSampleProject,
    resetForm,
  } = useAppState();

  const [activeSection, setActiveSection] = useState<AppSectionId>('project');

  const handleNavigate = (sectionId: AppSectionId) => {
    setActiveSection(sectionId);
    scrollToSection(sectionId);
  };

  return (
    <div className="app-shell">
      <AppHeader />

      <div className="app-toolbar">
        <div className="app-toolbar__actions">
          <button
            type="button"
            className="btn btn--primary"
            onClick={loadSampleProject}
          >
            90 MWp Örnek Proje
          </button>
          <button type="button" className="btn btn--secondary" onClick={resetForm}>
            Formu Temizle
          </button>
        </div>
        <p className="app-toolbar__hint">
          Girdi alanlarını doldurun. Sonuçlar hesaplama motoru eklendikten sonra
          üretilecek.
        </p>
      </div>

      <div className="app-layout">
        <aside className="app-layout__sidebar">
          <SidebarNav activeSection={activeSection} onNavigate={handleNavigate} />
        </aside>

        <main className="app-layout__main">
          <ProjectSection
            values={state.project}
            errors={state.validationErrors}
            onChange={updateProject}
            onValidationChange={setValidationError}
          />

          <PanelTableSection
            values={state.calculations.panelTable}
            errors={state.validationErrors}
            onChange={updatePanelTable}
            onValidationChange={setValidationError}
          />

          <FoundationSection
            values={state.calculations.foundation}
            errors={state.validationErrors}
            onChange={updateFoundation}
            onValidationChange={setValidationError}
          />

          <CableTrenchSection
            values={state.calculations.cableTrench}
            errors={state.validationErrors}
            onChange={updateCableTrench}
            onValidationChange={setValidationError}
          />

          <KioskSection
            values={state.calculations.kiosk}
            errors={state.validationErrors}
            onChange={updateKiosk}
            onValidationChange={setValidationError}
          />

          <BimsSection
            values={state.calculations.bims}
            errors={state.validationErrors}
            onChange={updateBims}
            onValidationChange={setValidationError}
          />

          <MaterialsSection
            summary={state.summary}
            rows={state.materialRows}
          />
        </main>
      </div>
    </div>
  );
}
