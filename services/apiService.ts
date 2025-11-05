import { Ingredient, Extraction, Assay, FunctionalTest, Attachment, IngredientForm, ExtractionStage, FiltrationType, AssayType, ApplicationType } from '../types';

// --- SEED DATA ---

// Helper map to link extraction lots to unique ingredient IDs
const batchIdToIngredientId: { [key: string]: string } = {
  'HPI-2024-01': 'ing_1',
  'HPI-2024-02': 'ing_2',
  'HPI-2024-03': 'ing_3',
  'HPC-2024-01': 'ing_4',
  'HPC-2024-02': 'ing_5',
  'HF-2024-01': 'ing_6',
  'HF-2024-02': 'ing_7',
};

let ingredients: Ingredient[] = [
  {
    id: 'ing_1',
    name: 'Hemp Protein Isolate',
    supplier: 'PlantPro Solutions',
    batch_id: 'HPI-2024-01',
    form: IngredientForm.POWDER,
    protein_pct: 90.5,
    moisture_pct: null,
    ash_pct: null,
    ph: 7.2,
    color_visual_notes: '',
    storage_condition: '',
    received_date: '2024-01-05T00:00:00.000Z',
    comments: '',
    attachments: [],
  },
  {
    id: 'ing_2',
    name: 'Hemp Protein Isolate',
    supplier: 'NutriHemp Corp',
    batch_id: 'HPI-2024-02',
    form: IngredientForm.POWDER,
    protein_pct: 88.2,
    moisture_pct: null,
    ash_pct: null,
    ph: 7.4,
    color_visual_notes: '',
    storage_condition: '',
    received_date: '2024-01-08T00:00:00.000Z',
    comments: '',
    attachments: [],
  },
  {
    id: 'ing_3',
    name: 'Hemp Protein Isolate',
    supplier: 'Bunge',
    batch_id: 'HPI-2024-03',
    form: IngredientForm.POWDER,
    protein_pct: 89.1,
    moisture_pct: null,
    ash_pct: null,
    ph: 6.9,
    color_visual_notes: '',
    storage_condition: '',
    received_date: '2024-01-12T00:00:00.000Z',
    comments: '',
    attachments: [],
  },
  {
    id: 'ing_4',
    name: 'Hemp Protein Concentrate',
    supplier: 'Ingredion',
    batch_id: 'HPC-2024-01',
    form: IngredientForm.POWDER,
    protein_pct: 78.5,
    moisture_pct: null,
    ash_pct: null,
    ph: 6.8,
    color_visual_notes: '',
    storage_condition: '',
    received_date: '2024-01-15T00:00:00.000Z',
    comments: '',
    attachments: [],
  },
  {
    id: 'ing_5',
    name: 'Hemp Protein Concentrate',
    supplier: 'Cosucra',
    batch_id: 'HPC-2024-02',
    form: IngredientForm.SLURRY,
    protein_pct: 72.3,
    moisture_pct: null,
    ash_pct: null,
    ph: 6.5,
    color_visual_notes: '',
    storage_condition: '',
    received_date: '2024-01-18T00:00:00.000Z',
    comments: '',
    attachments: [],
  },
  {
    id: 'ing_6',
    name: 'Hemp Flour',
    supplier: 'PlantPro Solutions',
    batch_id: 'HF-2024-01',
    form: IngredientForm.POWDER,
    protein_pct: 52.1,
    moisture_pct: null,
    ash_pct: null,
    ph: 6.2,
    color_visual_notes: '',
    storage_condition: '',
    received_date: '2024-01-22T00:00:00.000Z',
    comments: '',
    attachments: [],
  },
  {
    id: 'ing_7',
    name: 'Hemp Flour',
    supplier: 'NutriHemp Corp',
    batch_id: 'HF-2024-02',
    form: IngredientForm.POWDER,
    protein_pct: 48.9,
    moisture_pct: null,
    ash_pct: null,
    ph: 6.1,
    color_visual_notes: '',
    storage_condition: '',
    received_date: '2024-01-24T00:00:00.000Z',
    comments: '',
    attachments: [],
  },
];

let extractions: Extraction[] = [
    { id: 'EXT-240101', ingredient_id: batchIdToIngredientId['HPI-2024-01'], stage: ExtractionStage.STAGE2, stage_label: 'Stage 2 – Cold Salt Extract', method: 'Salt', ph: 6.8, salt_conc: 2.5, temp_c: 20, time_min: 30, solids_pct: 10.0, yield_pct: 84.5, centrifuge: '4000x15', filtration_type: FiltrationType.UF, supernatant_color: 'Pale yellow, clear', texture_observation: 'Fine, dispersed precipitate', operator: 'J.D.', date: '2024-01-10T00:00:00.000Z', notes: 'Mild conditions control', attachments: [] },
    { id: 'EXT-240102', ingredient_id: batchIdToIngredientId['HPI-2024-01'], stage: ExtractionStage.STAGE2, stage_label: 'Stage 2 – Cold Salt Extract', method: 'Salt', ph: 4.5, salt_conc: 5.0, temp_c: 45, time_min: 90, solids_pct: 12.5, yield_pct: 75.8, centrifuge: '5000x10', filtration_type: FiltrationType.UF, supernatant_color: 'Yellow, slightly turbid', texture_observation: 'Heavy precipitate', operator: 'M.S.', date: '2024-01-11T00:00:00.000Z', notes: 'Harsh conditions trial', attachments: [] },
    { id: 'EXT-240103', ingredient_id: batchIdToIngredientId['HPI-2024-02'], stage: ExtractionStage.STAGE2, stage_label: 'Stage 2 – Cold Salt Extract', method: 'Salt', ph: 5.0, salt_conc: 4.0, temp_c: 40, time_min: 80, solids_pct: 10.0, yield_pct: 78.5, centrifuge: '4500x10', filtration_type: FiltrationType.MICRO, supernatant_color: 'Light brown, slightly turbid', texture_observation: 'Slightly gelatinous curd', operator: 'K.L.', date: '2024-01-12T00:00:00.000Z', notes: '', attachments: [] },
    { id: 'EXT-240104', ingredient_id: batchIdToIngredientId['HPI-2024-03'], stage: ExtractionStage.STAGE2, stage_label: 'Stage 2 – Cold Salt Extract', method: 'Salt', ph: 5.5, salt_conc: 3.0, temp_c: 30, time_min: 30, solids_pct: 15.0, yield_pct: 81.5, centrifuge: '5000x15', filtration_type: FiltrationType.UF, supernatant_color: 'Yellow, clear', texture_observation: 'Fine precipitate', operator: 'J.D.', date: '2024-01-14T00:00:00.000Z', notes: '', attachments: [] },
    { id: 'EXT-240105', ingredient_id: batchIdToIngredientId['HPC-2024-01'], stage: ExtractionStage.STAGE2, stage_label: 'Stage 2 – Cold Salt Extract', method: 'Salt', ph: 6.5, salt_conc: 2.0, temp_c: 25, time_min: 45, solids_pct: 11.0, yield_pct: 72.1, centrifuge: '5000x15', filtration_type: FiltrationType.NONE, supernatant_color: 'Opaque, greenish tint', texture_observation: 'Heavy precipitate', operator: 'M.S.', date: '2024-01-16T00:00:00.000Z', notes: 'Filtration comparison', attachments: [] },
    { id: 'EXT-240106', ingredient_id: batchIdToIngredientId['HPC-2024-01'], stage: ExtractionStage.STAGE2, stage_label: 'Stage 2 – Cold Salt Extract', method: 'Salt', ph: 6.5, salt_conc: 2.0, temp_c: 25, time_min: 45, solids_pct: 11.0, yield_pct: 75.3, centrifuge: '4000x15', filtration_type: FiltrationType.MICRO, supernatant_color: 'Light brown, clear', texture_observation: 'Compact pellet', operator: 'K.L.', date: '2024-01-17T00:00:00.000Z', notes: 'Filtration comparison', attachments: [] },
    { id: 'EXT-240107', ingredient_id: batchIdToIngredientId['HPC-2024-01'], stage: ExtractionStage.STAGE2, stage_label: 'Stage 2 – Cold Salt Extract', method: 'Salt', ph: 6.5, salt_conc: 2.0, temp_c: 25, time_min: 45, solids_pct: 11.0, yield_pct: 76.5, centrifuge: '4000x15', filtration_type: FiltrationType.UF, supernatant_color: 'Pale yellow, very clear', texture_observation: 'Fine precipitate', operator: 'J.D.', date: '2024-01-18T00:00:00.000Z', notes: 'Filtration comparison', attachments: [] },
    { id: 'EXT-240108', ingredient_id: batchIdToIngredientId['HPC-2024-02'], stage: ExtractionStage.STAGE2, stage_label: 'Stage 2 – Cold Salt Extract', method: 'Salt', ph: 7.0, salt_conc: 1.5, temp_c: 10, time_min: 75, solids_pct: 9.5, yield_pct: 69.5, centrifuge: '4500x10', filtration_type: FiltrationType.UF, supernatant_color: 'Greenish-yellow, turbid', texture_observation: 'Gelatinous pellet', operator: 'M.S.', date: '2024-01-20T00:00:00.000Z', notes: '', attachments: [] },
    { id: 'EXT-240109', ingredient_id: batchIdToIngredientId['HPC-2024-02'], stage: ExtractionStage.STAGE2, stage_label: 'Stage 2 – Cold Salt Extract', method: 'Salt', ph: 6.2, salt_conc: 3.5, temp_c: 35, time_min: 50, solids_pct: 12.0, yield_pct: 71.2, centrifuge: '5000x10', filtration_type: FiltrationType.MICRO, supernatant_color: 'Light brown, slightly turbid', texture_observation: 'Dispersed solids', operator: 'K.L.', date: '2024-01-21T00:00:00.000Z', notes: '', attachments: [] },
    { id: 'EXT-240110', ingredient_id: batchIdToIngredientId['HPI-2024-01'], stage: ExtractionStage.STAGE2, stage_label: 'Stage 2 – Cold Salt Extract', method: 'Salt', ph: 4.5, salt_conc: 5.0, temp_c: 40, time_min: 75, solids_pct: 10.5, yield_pct: 28.5, centrifuge: '5000x15', filtration_type: FiltrationType.NONE, supernatant_color: 'Brown, opaque', texture_observation: 'Gritty texture', operator: 'J.D.', date: '2024-01-22T00:00:00.000Z', notes: 'Extraction at pI, low solubility observed.', attachments: [] },
    { id: 'EXT-240111', ingredient_id: batchIdToIngredientId['HPC-2024-02'], stage: ExtractionStage.STAGE2, stage_label: 'Stage 2 – Cold Salt Extract', method: 'Salt', ph: 6.5, salt_conc: 2.5, temp_c: 20, time_min: 60, solids_pct: 10.0, yield_pct: 70.5, centrifuge: '4000x15', filtration_type: FiltrationType.UF, supernatant_color: 'Pale yellow, clear', texture_observation: 'Compact pellet', operator: 'M.S.', date: '2024-01-23T00:00:00.000Z', notes: '', attachments: [] },
    { id: 'EXT-240112', ingredient_id: batchIdToIngredientId['HF-2024-01'], stage: ExtractionStage.STAGE2, stage_label: 'Stage 2 – Cold Salt Extract', method: 'Salt', ph: 6.0, salt_conc: 3.0, temp_c: 25, time_min: 40, solids_pct: 13.0, yield_pct: 58.1, centrifuge: '4500x10', filtration_type: FiltrationType.MICRO, supernatant_color: 'Dark brown, very turbid', texture_observation: 'Fibrous precipitate', operator: 'K.L.', date: '2024-01-25T00:00:00.000Z', notes: '', attachments: [] },
    { id: 'EXT-240113', ingredient_id: batchIdToIngredientId['HF-2024-01'], stage: ExtractionStage.STAGE2, stage_label: 'Stage 2 – Cold Salt Extract', method: 'Salt', ph: 6.5, salt_conc: 2.0, temp_c: 30, time_min: 50, solids_pct: 13.5, yield_pct: 59.5, centrifuge: '5000x10', filtration_type: FiltrationType.MICRO, supernatant_color: 'Brown, turbid', texture_observation: 'Fine dispersed solids', operator: 'J.D.', date: '2024-01-26T00:00:00.000Z', notes: '', attachments: [] },
    { id: 'EXT-240114', ingredient_id: batchIdToIngredientId['HF-2024-02'], stage: ExtractionStage.STAGE2, stage_label: 'Stage 2 – Cold Salt Extract', method: 'Salt', ph: 5.8, salt_conc: 4.0, temp_c: 35, time_min: 60, solids_pct: 14.0, yield_pct: 55.4, centrifuge: '5000x15', filtration_type: FiltrationType.NONE, supernatant_color: 'Greenish-brown, opaque', texture_observation: 'Compact, gritty pellet', operator: 'M.S.', date: '2024-01-28T00:00:00.000Z', notes: 'Slight foaming during agitation', attachments: [] },
    { id: 'EXT-240115', ingredient_id: batchIdToIngredientId['HPI-2024-02'], stage: ExtractionStage.STAGE2, stage_label: 'Stage 2 – Cold Salt Extract', method: 'Salt', ph: 6.8, salt_conc: 1.8, temp_c: 18, time_min: 45, solids_pct: 11.5, yield_pct: 82.0, centrifuge: '4000x15', filtration_type: FiltrationType.UF, supernatant_color: 'Pale yellow, clear', texture_observation: 'Fine precipitate', operator: 'K.L.', date: '2024-01-29T00:00:00.000Z', notes: 'Process ran smoothly', attachments: [] },
];

let assays: Assay[] = [
    { id: 'asy_1', extraction_id: 'EXT-240101', assay_type: AssayType.SOLUBILITY, parameter: 'Protein Solubility Index (PSI)', value: 94.2, unit: '%', instrument: '', date: '2024-01-11T00:00:00.000Z', analyst: 'A. Smith', replicate_num: 1, notes: '', attachments: [] },
    { id: 'asy_2', extraction_id: 'EXT-240102', assay_type: AssayType.SOLUBILITY, parameter: 'Protein Solubility Index (PSI)', value: 72.5, unit: '%', instrument: '', date: '2024-01-12T00:00:00.000Z', analyst: 'J. Doe', replicate_num: 1, notes: '', attachments: [] },
    { id: 'asy_3', extraction_id: 'EXT-240103', assay_type: AssayType.DSC, parameter: 'Onset Temp', value: 67.8, unit: '°C', instrument: '', date: '2024-01-13T00:00:00.000Z', analyst: 'A. Smith', replicate_num: 1, notes: '', attachments: [] },
    { id: 'asy_4', extraction_id: 'EXT-240104', assay_type: AssayType.TURBISCAN, parameter: 'TSI', value: 0.8, unit: 'TSI', instrument: '', date: '2024-01-15T00:00:00.000Z', analyst: 'J. Doe', replicate_num: 1, notes: '', attachments: [] },
    { id: 'asy_5', extraction_id: 'EXT-240105', assay_type: AssayType.DSC, parameter: 'Onset Temp', value: 66.5, unit: '°C', instrument: '', date: '2024-01-17T00:00:00.000Z', analyst: 'A. Smith', replicate_num: 1, notes: '', attachments: [] },
    { id: 'asy_6', extraction_id: 'EXT-240106', assay_type: AssayType.DLS, parameter: 'Particle Size (Z-Ave)', value: 350, unit: 'nm', instrument: '', date: '2024-01-18T00:00:00.000Z', analyst: 'J. Doe', replicate_num: 1, notes: '', attachments: [] },
    { id: 'asy_7', extraction_id: 'EXT-240107', assay_type: AssayType.DLS, parameter: 'Particle Size (Z-Ave)', value: 185, unit: 'nm', instrument: '', date: '2024-01-19T00:00:00.000Z', analyst: 'A. Smith', replicate_num: 1, notes: '', attachments: [] },
    { id: 'asy_8', extraction_id: 'EXT-240108', assay_type: AssayType.TURBISCAN, parameter: 'TSI', value: 3.5, unit: 'TSI', instrument: '', date: '2024-01-21T00:00:00.000Z', analyst: 'J. Doe', replicate_num: 1, notes: '', attachments: [] },
    { id: 'asy_9', extraction_id: 'EXT-240109', assay_type: AssayType.SOLUBILITY, parameter: 'Protein Solubility Index (PSI)', value: 80.1, unit: '%', instrument: '', date: '2024-01-22T00:00:00.000Z', analyst: 'A. Smith', replicate_num: 1, notes: '', attachments: [] },
    { id: 'asy_10', extraction_id: 'EXT-240110', assay_type: AssayType.DSC, parameter: 'Onset Temp', value: 68.2, unit: '°C', instrument: '', date: '2024-01-23T00:00:00.000Z', analyst: 'J. Doe', replicate_num: 1, notes: '', attachments: [] },
    { id: 'asy_11', extraction_id: 'EXT-240111', assay_type: AssayType.DLS, parameter: 'Particle Size (Z-Ave)', value: 255, unit: 'nm', instrument: '', date: '2024-01-24T00:00:00.000Z', analyst: 'A. Smith', replicate_num: 1, notes: '', attachments: [] },
    { id: 'asy_12', extraction_id: 'EXT-240112', assay_type: AssayType.SOLUBILITY, parameter: 'Protein Solubility Index (PSI)', value: 78.5, unit: '%', instrument: '', date: '2024-01-26T00:00:00.000Z', analyst: 'J. Doe', replicate_num: 1, notes: '', attachments: [] },
    { id: 'asy_13', extraction_id: 'EXT-240113', assay_type: AssayType.DSC, parameter: 'Onset Temp', value: 72.1, unit: '°C', instrument: '', date: '2024-01-27T00:00:00.000Z', analyst: 'A. Smith', replicate_num: 1, notes: '', attachments: [] },
    { id: 'asy_14', extraction_id: 'EXT-240114', assay_type: AssayType.TURBISCAN, parameter: 'TSI', value: 4.8, unit: 'TSI', instrument: '', date: '2024-01-29T00:00:00.000Z', analyst: 'J. Doe', replicate_num: 1, notes: '', attachments: [] },
    { id: 'asy_15', extraction_id: 'EXT-240115', assay_type: AssayType.DSC, parameter: 'Onset Temp', value: 79.5, unit: '°C', instrument: '', date: '2024-01-30T00:00:00.000Z', analyst: 'A. Smith', replicate_num: 1, notes: '', attachments: [] },
];

let functionalTests: FunctionalTest[] = [
    { id: 'ft_1', extraction_id: 'EXT-240101', application_type: ApplicationType.FOAM, condition: '', performance_metric: 'Height Retention', score_or_value: '92% after 30 min', evaluator: 'C.L.', date: '2024-01-12T00:00:00.000Z', comments: '', attachments: [] },
    { id: 'ft_2', extraction_id: 'EXT-240102', application_type: ApplicationType.EMULSION, condition: '', performance_metric: 'Stability Time', score_or_value: 'Phase sep. at 10 min', evaluator: 'R.B.', date: '2024-01-13T00:00:00.000Z', comments: '', attachments: [] },
    { id: 'ft_3', extraction_id: 'EXT-240103', application_type: ApplicationType.GELATION, condition: '', performance_metric: 'Gel Strength', score_or_value: 'Weak gel', evaluator: 'C.L.', date: '2024-01-14T00:00:00.000Z', comments: '', attachments: [] },
    { id: 'ft_4', extraction_id: 'EXT-240104', application_type: ApplicationType.CHEESE_MELT, condition: '', performance_metric: 'Meltability Index', score_or_value: '8/10, good stretch', evaluator: 'R.B.', date: '2024-01-16T00:00:00.000Z', comments: '', attachments: [] },
    { id: 'ft_5', extraction_id: 'EXT-240105', application_type: ApplicationType.EMULSION, condition: '', performance_metric: 'Stability Time', score_or_value: 'Phase sep. at 15 min', evaluator: 'C.L.', date: '2024-01-18T00:00:00.000Z', comments: '', attachments: [] },
    { id: 'ft_6', extraction_id: 'EXT-240106', application_type: ApplicationType.EMULSION, condition: '', performance_metric: 'Stability Time', score_or_value: 'Stable 40 min', evaluator: 'R.B.', date: '2024-01-19T00:00:00.000Z', comments: '', attachments: [] },
    { id: 'ft_7', extraction_id: 'EXT-240107', application_type: ApplicationType.EMULSION, condition: '', performance_metric: 'Stability Time', score_or_value: 'Stable 55 min', evaluator: 'C.L.', date: '2024-01-20T00:00:00.000Z', comments: '', attachments: [] },
    { id: 'ft_8', extraction_id: 'EXT-240108', application_type: ApplicationType.GELATION, condition: '', performance_metric: 'Gel Strength', score_or_value: '380 g', evaluator: 'R.B.', date: '2024-01-22T00:00:00.000Z', comments: '', attachments: [] },
    { id: 'ft_9', extraction_id: 'EXT-240109', application_type: ApplicationType.FOAM, condition: '', performance_metric: 'Height Retention', score_or_value: '75% after 30 min', evaluator: 'C.L.', date: '2024-01-23T00:00:00.000Z', comments: '', attachments: [] },
    { id: 'ft_10', extraction_id: 'EXT-240110', application_type: ApplicationType.EMULSION, condition: '', performance_metric: 'Stability Time', score_or_value: 'Phase sep. at 15 min', evaluator: 'R.B.', date: '2024-01-24T00:00:00.000Z', comments: '', attachments: [] },
    { id: 'ft_11', extraction_id: 'EXT-240111', application_type: ApplicationType.BINDING, condition: '', performance_metric: 'Water Holding Capacity', score_or_value: '3.9 g/g', evaluator: 'C.L.', date: '2024-01-25T00:00:00.000Z', comments: '', attachments: [] },
    { id: 'ft_12', extraction_id: 'EXT-240112', application_type: ApplicationType.GELATION, condition: '', performance_metric: 'Gel Strength', score_or_value: '355 g', evaluator: 'R.B.', date: '2024-01-27T00:00:00.000Z', comments: '', attachments: [] },
    { id: 'ft_13', extraction_id: 'EXT-240113', application_type: ApplicationType.BINDING, condition: '', performance_metric: 'Water Holding Capacity', score_or_value: '3.6 g/g', evaluator: 'C.L.', date: '2024-01-28T00:00:00.000Z', comments: '', attachments: [] },
    { id: 'ft_14', extraction_id: 'EXT-240114', application_type: ApplicationType.FOAM, condition: '', performance_metric: 'Height Retention', score_or_value: '71% after 30 min', evaluator: 'R.B.', date: '2024-01-30T00:00:00.000Z', comments: '', attachments: [] },
    { id: 'ft_15', extraction_id: 'EXT-240115', application_type: ApplicationType.FOAM, condition: '', performance_metric: 'Height Retention', score_or_value: '90% after 30 min', evaluator: 'C.L.', date: '2024-01-31T00:00:00.000Z', comments: '', attachments: [] },
];


// --- MOCK API ---
const wait = (ms: number) => new Promise(res => setTimeout(res, ms));

const createApi = <T extends { id: string }>(store: () => T[], updateStore: (newData: T[]) => void) => {
  return {
    async getAll(): Promise<T[]> {
      await wait(200);
      return [...store()];
    },
    async create(item: Omit<T, 'id'>): Promise<T> {
      await wait(300);
      const newItem = { ...item, id: `new_${Date.now()}` } as T;
      updateStore([...store(), newItem]);
      return newItem;
    },
    async update(id: string, updates: Partial<T>): Promise<T> {
      await wait(300);
      let updatedItem: T | undefined;
      const newStore = store().map(item => {
        if (item.id === id) {
          updatedItem = { ...item, ...updates };
          return updatedItem;
        }
        return item;
      });
      if (!updatedItem) throw new Error('Item not found');
      updateStore(newStore);
      return updatedItem;
    },
    async delete(id: string): Promise<void> {
      await wait(500);
      updateStore(store().filter(item => item.id !== id));
    },
  };
};

export const ingredientApi = createApi(() => ingredients, (data) => ingredients = data);

export const extractionApi = {
  ...createApi(() => extractions, (data) => extractions = data),
  async getByStage(stage: ExtractionStage): Promise<Extraction[]> {
    await wait(200);
    return extractions.filter(e => e.stage === stage);
  }
};

export const assayApi = createApi(() => assays, (data) => assays = data);
export const functionalTestApi = createApi(() => functionalTests, (data) => functionalTests = data);

export const uploadApi = {
  async uploadFile(file: File, parentType: string, parentId: string): Promise<Attachment> {
    await wait(1000); // Simulate upload time
    console.log(`Uploading ${file.name} for ${parentType}:${parentId}`);
    const attachment: Attachment = {
      name: file.name,
      mime: file.type,
      size: file.size,
      url: URL.createObjectURL(file),
      gcs_path: `gs://lab-data-uploads/${Date.now()}-${file.name}`,
    };
    return attachment;
  },
};

export const dashboardApi = {
  async getOverview() {
    await wait(400);
    const totalIngredients = ingredients.length;
    const totalExtractions = extractions.length;
    const yields = extractions.map(e => e.yield_pct).filter((y): y is number => y !== null);
    const avgYield = yields.length > 0 ? (yields.reduce((a, b) => a + b, 0) / yields.length).toFixed(1) : 'N/A';
    const recentExtractions = [...extractions]
      .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
      .slice(0, 5);

    return {
      totalIngredients,
      totalExtractions,
      avgYield,
      recentExtractions,
    };
  }
}

// Generic create function
export const apiService = {
  async createRecord(dataType: string, data: any): Promise<any> {
    switch (dataType) {
      case 'ingredients':
        return ingredientApi.create(data);
      case 'extractions':
        return extractionApi.create(data);
      case 'assays':
        return assayApi.create(data);
      case 'functional_tests':
        return functionalTestApi.create(data);
      default:
        throw new Error(`Unknown data type: ${dataType}`);
    }
  }
};
