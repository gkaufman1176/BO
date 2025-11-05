import { ingredientApi, extractionApi, assayApi, functionalTestApi } from './services/apiService';
import { Ingredient, Extraction, Assay, FunctionalTest, IngredientForm, ExtractionStage, FiltrationType, AssayType, ApplicationType } from './types';
import type { Column } from './components/WorksheetPage';

export const worksheetConfigs = {
  ingredients: {
    title: "Ingredients",
    dataType: "ingredients",
    api: ingredientApi,
    defaultNewRow: { name: '', supplier: '', batch_id: '', form: IngredientForm.POWDER, protein_pct: null, moisture_pct: null, ash_pct: null, ph: null, color_visual_notes: '', storage_condition: '', received_date: new Date().toISOString(), comments: '', attachments: [] } as Omit<Ingredient, 'id'>,
    columns: [
      { key: 'name', header: 'Ingredient Name' },
      { key: 'supplier', header: 'Supplier' },
      { key: 'batch_id', header: 'Batch/Lot ID' },
      { key: 'form', header: 'Form', type: 'select', options: Object.values(IngredientForm) },
      { key: 'protein_pct', header: 'Protein %', type: 'number' },
      { key: 'moisture_pct', header: 'Moisture %', type: 'number' },
      { key: 'ash_pct', header: 'Ash %', type: 'number' },
      { key: 'ph', header: 'pH', type: 'number' },
      { key: 'color_visual_notes', header: 'Color / Visual' },
      { key: 'storage_condition', header: 'Storage Condition' },
      { key: 'received_date', header: 'Received Date', type: 'date' },
      { key: 'comments', header: 'Notes' },
      { key: 'attachments', header: 'Attachments', type: 'attachments' },
    ] as Column<Ingredient>[]
  },
  extractions: {
    title: "Extraction Trials",
    dataType: "extractions",
    api: extractionApi,
    defaultNewRow: { ingredient_id: '', stage: ExtractionStage.STAGE2, stage_label: 'Stage 2 – Cold Salt Extract', method: 'Salt', ph: null, salt_conc: null, temp_c: null, time_min: null, solids_pct: null, yield_pct: null, centrifuge: '', filtration_type: FiltrationType.EMPTY, supernatant_color: '', texture_observation: '', operator: '', date: new Date().toISOString(), notes: '', attachments: [] } as Omit<Extraction, 'id'>,
    columns: [
      { key: 'ingredient_id', header: 'Ingredient', type: 'link', linkSource: 'ingredients' },
      { key: 'method', header: 'Method', readOnly: true },
      { key: 'ph', header: 'pH', type: 'number' },
      { key: 'salt_conc', header: 'Salt Conc. (%)', type: 'number' },
      { key: 'temp_c', header: 'Temp °C', type: 'number' },
      { key: 'time_min', header: 'Time (min)', type: 'number' },
      { key: 'solids_pct', header: 'Solids %', type: 'number' },
      { key: 'yield_pct', header: 'Yield %', type: 'number' },
      { key: 'centrifuge', header: 'Centrifuge (rpm×min)' },
      { key: 'filtration_type', header: 'Filtration Type', type: 'select', options: Object.values(FiltrationType) },
      { key: 'supernatant_color', header: 'Supernatant Color' },
      { key: 'texture_observation', header: 'Texture Observation' },
      { key: 'operator', header: 'Operator' },
      { key: 'date', header: 'Date', type: 'date' },
      { key: 'notes', header: 'Notes' },
      { key: 'attachments', header: 'Attachments', type: 'attachments' },
    ] as Column<Extraction>[]
  },
  assays: {
    title: "Assay Results",
    dataType: "assays",
    api: assayApi,
    defaultNewRow: { extraction_id: '', assay_type: AssayType.SOLUBILITY, parameter: '', value: null, unit: '', instrument: '', date: new Date().toISOString(), analyst: '', replicate_num: 1, notes: '', attachments: [] } as Omit<Assay, 'id'>,
    columns: [
        { key: 'extraction_id', header: 'Extraction Ref' }, // Would be a link in a real app
        { key: 'assay_type', header: 'Assay Type', type: 'select', options: Object.values(AssayType) },
        { key: 'parameter', header: 'Parameter' },
        { key: 'value', header: 'Value', type: 'number' },
        { key: 'unit', header: 'Unit' },
        { key: 'instrument', header: 'Instrument' },
        { key: 'date', header: 'Date', type: 'date' },
        { key: 'analyst', header: 'Analyst' },
        { key: 'replicate_num', header: 'Replicate #', type: 'number' },
        { key: 'notes', header: 'Notes' },
        { key: 'attachments', header: 'Attachments', type: 'attachments' },
    ] as Column<Assay>[]
  },
  functionalTests: {
    title: "Functional Tests",
    dataType: "functional-tests",
    api: functionalTestApi,
    defaultNewRow: { extraction_id: '', application_type: ApplicationType.OTHER, condition: '', performance_metric: '', score_or_value: '', evaluator: '', date: new Date().toISOString(), comments: '', attachments: [] } as Omit<FunctionalTest, 'id'>,
    columns: [
        { key: 'extraction_id', header: 'Extraction Ref' },
        { key: 'application_type', header: 'Application Type', type: 'select', options: Object.values(ApplicationType) },
        { key: 'condition', header: 'Condition (pH/Temp/Conc.)' },
        { key: 'performance_metric', header: 'Metric' },
        { key: 'score_or_value', header: 'Value' },
        { key: 'evaluator', header: 'Evaluator' },
        { key: 'date', header: 'Date', type: 'date' },
        { key: 'comments', header: 'Comments' },
        { key: 'attachments', header: 'Attachments', type: 'attachments' },
    ] as Column<FunctionalTest>[]
  }
};
