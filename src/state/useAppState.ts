import { useCallback, useState } from 'react';
import { applyCalculation, createInitialAppState } from '../domain/defaults';
import { getKioskRecipe, kioskRecipeToInputValues } from '../domain/recipes/kioskRecipes';
import { getTableRecipe } from '../domain/recipes/tableRecipes';
import {
  sampleCalculationInputs,
  sampleProjectInputs,
} from '../domain/sampleProject';
import type {
  AppState,
  BimsInputs,
  CableTrenchInputs,
  ConcreteFootMode,
  FoundationInputs,
  KioskInputs,
  PanelTableInputs,
  ProjectInput,
  ValidationFieldKey,
} from '../domain/types';
import { setFieldError } from '../domain/validation';

function commit(updater: (prev: AppState) => AppState) {
  return (prev: AppState) => applyCalculation(updater(prev));
}

export function useAppState() {
  const [state, setState] = useState<AppState>(createInitialAppState);

  const updateProject = useCallback(
    <K extends keyof ProjectInput>(key: K, value: ProjectInput[K]) => {
      setState(
        commit((prev) => ({
          ...prev,
          project: { ...prev.project, [key]: value },
        })),
      );
    },
    [],
  );

  const updatePanelTable = useCallback(
    <K extends keyof PanelTableInputs>(key: K, value: PanelTableInputs[K]) => {
      setState(
        commit((prev) => ({
          ...prev,
          calculations: {
            ...prev.calculations,
            panelTable: { ...prev.calculations.panelTable, [key]: value },
          },
        })),
      );
    },
    [],
  );

  const selectTableRecipe = useCallback((recipeId: string) => {
    const recipe = getTableRecipe(recipeId);
    setState(
      commit((prev) => ({
        ...prev,
        calculations: {
          ...prev.calculations,
          panelTable: {
            ...prev.calculations.panelTable,
            selectedTableRecipeId: recipeId,
            panelsPerTable: recipe?.panelsPerTable ?? prev.calculations.panelTable.panelsPerTable,
            legsPerTable: recipe?.feetPerTable ?? prev.calculations.panelTable.legsPerTable,
          },
        },
        validationErrors: setFieldError(
          prev.validationErrors,
          'panelTable.selectedTableRecipeId',
          recipe ? null : 'Geçersiz masa reçetesi seçildi.',
        ),
      })),
    );
  }, []);

  const updateFoundation = useCallback(
    <K extends keyof FoundationInputs>(key: K, value: FoundationInputs[K]) => {
      setState(
        commit((prev) => ({
          ...prev,
          calculations: {
            ...prev.calculations,
            foundation: { ...prev.calculations.foundation, [key]: value },
          },
        })),
      );
    },
    [],
  );

  const setConcreteFootMode = useCallback((mode: ConcreteFootMode) => {
    setState(
      commit((prev) => ({
        ...prev,
        calculations: {
          ...prev.calculations,
          foundation: {
            ...prev.calculations.foundation,
            concreteFootMode: mode,
          },
        },
      })),
    );
  }, []);

  const updateCableTrench = useCallback(
    <K extends keyof CableTrenchInputs>(key: K, value: CableTrenchInputs[K]) => {
      setState(
        commit((prev) => ({
          ...prev,
          calculations: {
            ...prev.calculations,
            cableTrench: { ...prev.calculations.cableTrench, [key]: value },
          },
        })),
      );
    },
    [],
  );

  const updateKiosk = useCallback(
    <K extends keyof KioskInputs>(key: K, value: KioskInputs[K]) => {
      setState(
        commit((prev) => ({
          ...prev,
          calculations: {
            ...prev.calculations,
            kiosk: { ...prev.calculations.kiosk, [key]: value },
          },
        })),
      );
    },
    [],
  );

  const selectKioskRecipe = useCallback((recipeId: string) => {
    const recipe = getKioskRecipe(recipeId);
    const values = recipe ? kioskRecipeToInputValues(recipe) : null;

    setState(
      commit((prev) => ({
        ...prev,
        calculations: {
          ...prev.calculations,
          kiosk: {
            ...prev.calculations.kiosk,
            selectedKioskRecipeId: recipeId,
            ...(values ?? {}),
          },
        },
        validationErrors: setFieldError(
          prev.validationErrors,
          'kiosk.selectedKioskRecipeId',
          recipe ? null : 'Geçersiz köşk reçetesi seçildi.',
        ),
      })),
    );
  }, []);

  const updateBims = useCallback(
    <K extends keyof BimsInputs>(key: K, value: BimsInputs[K]) => {
      setState(
        commit((prev) => ({
          ...prev,
          calculations: {
            ...prev.calculations,
            bims: { ...prev.calculations.bims, [key]: value },
          },
        })),
      );
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
    setState(
      applyCalculation({
        project: sampleProjectInputs(),
        calculations: sampleCalculationInputs(),
        validationErrors: {},
        materialRows: [],
        summary: {
          panel: null,
          table: null,
          totalLegs: null,
          concrete: null,
          sand: null,
          bims: null,
        },
      }),
    );
  }, []);

  const resetForm = useCallback(() => {
    setState(createInitialAppState());
  }, []);

  return {
    state,
    updateProject,
    updatePanelTable,
    selectTableRecipe,
    updateFoundation,
    setConcreteFootMode,
    updateCableTrench,
    updateKiosk,
    selectKioskRecipe,
    updateBims,
    setValidationError,
    loadSampleProject,
    resetForm,
  };
}
