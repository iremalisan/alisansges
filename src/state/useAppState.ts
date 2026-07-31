import { useCallback, useState } from 'react';
import { applyCalculation, createInitialAppState } from '../domain/defaults';
import {
  applyKioskRecipeToGroup,
  createEmptyKioskGroup,
  createEmptyTrench,
  createEmptyWall,
  duplicateKioskGroupEntry,
  duplicateTrenchEntry,
  duplicateWallEntry,
} from '../domain/entries';
import {
  sampleCalculationInputs,
  sampleProjectInputs,
} from '../domain/sampleProject';
import type {
  AppState,
  CableTrenchInput,
  ConcreteFootMode,
  FoundationInputs,
  KioskGroupInput,
  PanelTableInputs,
  ProjectInput,
  ValidationFieldKey,
  WallInput,
} from '../domain/types';
import { clearErrorsForPrefix, setFieldError } from '../domain/validation';
import { getTableRecipe } from '../domain/recipes/tableRecipes';

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
            panelsPerTable:
              recipe?.panelsPerTable ??
              prev.calculations.panelTable.panelsPerTable,
            legsPerTable:
              recipe?.feetPerTable ?? prev.calculations.panelTable.legsPerTable,
          },
        },
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

  const addTrench = useCallback(() => {
    setState(
      commit((prev) => ({
        ...prev,
        calculations: {
          ...prev.calculations,
          trenches: [...prev.calculations.trenches, createEmptyTrench()],
        },
      })),
    );
  }, []);

  const updateTrench = useCallback(
    <K extends keyof CableTrenchInput>(
      id: string,
      key: K,
      value: CableTrenchInput[K],
    ) => {
      setState(
        commit((prev) => ({
          ...prev,
          calculations: {
            ...prev.calculations,
            trenches: prev.calculations.trenches.map((trench) =>
              trench.id === id ? { ...trench, [key]: value } : trench,
            ),
          },
        })),
      );
    },
    [],
  );

  const removeTrench = useCallback((id: string) => {
    setState(
      commit((prev) => ({
        ...prev,
        validationErrors: clearErrorsForPrefix(
          prev.validationErrors,
          `trench.${id}.`,
        ),
        calculations: {
          ...prev.calculations,
          trenches: prev.calculations.trenches.filter(
            (trench) => trench.id !== id,
          ),
        },
      })),
    );
  }, []);

  const duplicateTrench = useCallback((id: string) => {
    setState(
      commit((prev) => {
        const source = prev.calculations.trenches.find((t) => t.id === id);
        if (!source) {
          return prev;
        }

        return {
          ...prev,
          calculations: {
            ...prev.calculations,
            trenches: [
              ...prev.calculations.trenches,
              duplicateTrenchEntry(source),
            ],
          },
        };
      }),
    );
  }, []);

  const addKioskGroup = useCallback(() => {
    setState(
      commit((prev) => ({
        ...prev,
        calculations: {
          ...prev.calculations,
          kioskGroups: [
            ...prev.calculations.kioskGroups,
            createEmptyKioskGroup(),
          ],
        },
      })),
    );
  }, []);

  const updateKioskGroup = useCallback(
    <K extends keyof KioskGroupInput>(
      id: string,
      key: K,
      value: KioskGroupInput[K],
    ) => {
      setState(
        commit((prev) => ({
          ...prev,
          calculations: {
            ...prev.calculations,
            kioskGroups: prev.calculations.kioskGroups.map((group) =>
              group.id === id ? { ...group, [key]: value } : group,
            ),
          },
        })),
      );
    },
    [],
  );

  const selectKioskGroupRecipe = useCallback((id: string, recipeId: string) => {
    setState(
      commit((prev) => ({
        ...prev,
        calculations: {
          ...prev.calculations,
          kioskGroups: prev.calculations.kioskGroups.map((group) =>
            group.id === id ? applyKioskRecipeToGroup(group, recipeId) : group,
          ),
        },
      })),
    );
  }, []);

  const removeKioskGroup = useCallback((id: string) => {
    setState(
      commit((prev) => ({
        ...prev,
        validationErrors: clearErrorsForPrefix(
          prev.validationErrors,
          `kioskGroup.${id}.`,
        ),
        calculations: {
          ...prev.calculations,
          kioskGroups: prev.calculations.kioskGroups.filter(
            (group) => group.id !== id,
          ),
        },
      })),
    );
  }, []);

  const duplicateKioskGroup = useCallback((id: string) => {
    setState(
      commit((prev) => {
        const source = prev.calculations.kioskGroups.find((g) => g.id === id);
        if (!source) {
          return prev;
        }

        return {
          ...prev,
          calculations: {
            ...prev.calculations,
            kioskGroups: [
              ...prev.calculations.kioskGroups,
              duplicateKioskGroupEntry(source),
            ],
          },
        };
      }),
    );
  }, []);

  const addWall = useCallback(() => {
    setState(
      commit((prev) => ({
        ...prev,
        calculations: {
          ...prev.calculations,
          walls: [...prev.calculations.walls, createEmptyWall()],
        },
      })),
    );
  }, []);

  const updateWall = useCallback(
    <K extends keyof WallInput>(id: string, key: K, value: WallInput[K]) => {
      setState(
        commit((prev) => ({
          ...prev,
          calculations: {
            ...prev.calculations,
            walls: prev.calculations.walls.map((wall) =>
              wall.id === id ? { ...wall, [key]: value } : wall,
            ),
          },
        })),
      );
    },
    [],
  );

  const removeWall = useCallback((id: string) => {
    setState(
      commit((prev) => ({
        ...prev,
        validationErrors: clearErrorsForPrefix(
          prev.validationErrors,
          `wall.${id}.`,
        ),
        calculations: {
          ...prev.calculations,
          walls: prev.calculations.walls.filter((wall) => wall.id !== id),
        },
      })),
    );
  }, []);

  const duplicateWall = useCallback((id: string) => {
    setState(
      commit((prev) => {
        const source = prev.calculations.walls.find((w) => w.id === id);
        if (!source) {
          return prev;
        }

        return {
          ...prev,
          calculations: {
            ...prev.calculations,
            walls: [...prev.calculations.walls, duplicateWallEntry(source)],
          },
        };
      }),
    );
  }, []);

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
        trenchSummaries: {},
        wallSummaries: {},
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
    addTrench,
    updateTrench,
    removeTrench,
    duplicateTrench,
    addKioskGroup,
    updateKioskGroup,
    selectKioskGroupRecipe,
    removeKioskGroup,
    duplicateKioskGroup,
    addWall,
    updateWall,
    removeWall,
    duplicateWall,
    setValidationError,
    loadSampleProject,
    resetForm,
  };
}
