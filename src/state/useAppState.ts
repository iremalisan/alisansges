import { useCallback, useState } from 'react';
import { createInitialAppState } from '../domain/defaults';
import {
  sampleCalculationInputs,
  sampleProjectInputs,
} from '../domain/sampleProject';
import type {
  AppState,
  BimsInputs,
  CableTrenchInputs,
  FoundationInputs,
  KioskInputs,
  PanelTableInputs,
  ProjectInputs,
  ValidationFieldKey,
} from '../domain/types';
import { setFieldError } from '../domain/validation';

export function useAppState() {
  const [state, setState] = useState<AppState>(createInitialAppState);

  const updateProject = useCallback(
    <K extends keyof ProjectInputs>(key: K, value: ProjectInputs[K]) => {
      setState((prev) => ({
        ...prev,
        project: { ...prev.project, [key]: value },
      }));
    },
    [],
  );

  const updatePanelTable = useCallback(
    <K extends keyof PanelTableInputs>(key: K, value: PanelTableInputs[K]) => {
      setState((prev) => ({
        ...prev,
        calculations: {
          ...prev.calculations,
          panelTable: { ...prev.calculations.panelTable, [key]: value },
        },
      }));
    },
    [],
  );

  const updateFoundation = useCallback(
    <K extends keyof FoundationInputs>(key: K, value: FoundationInputs[K]) => {
      setState((prev) => ({
        ...prev,
        calculations: {
          ...prev.calculations,
          foundation: { ...prev.calculations.foundation, [key]: value },
        },
      }));
    },
    [],
  );

  const updateCableTrench = useCallback(
    <K extends keyof CableTrenchInputs>(key: K, value: CableTrenchInputs[K]) => {
      setState((prev) => ({
        ...prev,
        calculations: {
          ...prev.calculations,
          cableTrench: { ...prev.calculations.cableTrench, [key]: value },
        },
      }));
    },
    [],
  );

  const updateKiosk = useCallback(
    <K extends keyof KioskInputs>(key: K, value: KioskInputs[K]) => {
      setState((prev) => ({
        ...prev,
        calculations: {
          ...prev.calculations,
          kiosk: { ...prev.calculations.kiosk, [key]: value },
        },
      }));
    },
    [],
  );

  const updateBims = useCallback(
    <K extends keyof BimsInputs>(key: K, value: BimsInputs[K]) => {
      setState((prev) => ({
        ...prev,
        calculations: {
          ...prev.calculations,
          bims: { ...prev.calculations.bims, [key]: value },
        },
      }));
    },
    [],
  );

  const setValidationError = useCallback(
    (field: ValidationFieldKey, message: string | null) => {
      setState((prev) => ({
        ...prev,
        validationErrors: setFieldError(prev.validationErrors, field, message),
      }));
    },
    [],
  );

  const loadSampleProject = useCallback(() => {
    setState((prev) => ({
      ...prev,
      project: sampleProjectInputs(),
      calculations: sampleCalculationInputs(),
      validationErrors: {},
      // Results stay empty until the calculation engine is added.
      materialRows: [],
      summary: {
        panel: null,
        table: null,
        totalLegs: null,
        concrete: null,
        sand: null,
        bims: null,
      },
    }));
  }, []);

  const resetForm = useCallback(() => {
    setState(createInitialAppState());
  }, []);

  return {
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
  };
}
