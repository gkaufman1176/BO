export type Attachment = {
  name: string;
  mime: string;
  size: number;
  url: string;
  gcs_path: string;
};

export enum IngredientForm {
  POWDER = 'powder',
  SLURRY = 'slurry',
  ISOLATE = 'isolate',
  CONCENTRATE = 'concentrate',
  LIQUID = 'liquid',
}

export interface Ingredient {
  id: string;
  name: string;
  supplier: string;
  batch_id: string;
  form: IngredientForm;
  protein_pct: number | null;
  moisture_pct: number | null;
  ash_pct: number | null;
  ph: number | null;
  color_visual_notes: string;
  storage_condition: string;
  received_date: string;
  comments: string;
  attachments: Attachment[];
}

export enum ExtractionStage {
  STAGE1 = 'stage1',
  STAGE2 = 'stage2',
  STAGE3 = 'stage3',
  STAGE4 = 'stage4',
}

export enum FiltrationType {
    MICRO = 'Micro',
    UF = 'UF',
    NONE = 'None',
    EMPTY = '',
}

export interface Extraction {
  id: string;
  ingredient_id: string;
  stage: ExtractionStage;
  stage_label: string;
  method: 'Salt';
  ph: number | null;
  salt_conc: number | null;
  temp_c: number | null;
  time_min: number | null;
  solids_pct: number | null;
  yield_pct: number | null;
  centrifuge: string;
  filtration_type: FiltrationType;
  supernatant_color: string;
  texture_observation: string;
  operator: string;
  date: string;
  notes: string;
  attachments: Attachment[];
}

export enum AssayType {
    SOLUBILITY = 'Solubility',
    DSC = 'DSC',
    DLS = 'DLS',
    TURBISCAN = 'Turbiscan',
    TEXTURE = 'Texture',
    PH_STABILITY = 'pH Stability',
}

export interface Assay {
  id: string;
  extraction_id: string;
  assay_type: AssayType;
  parameter: string;
  value: number | null;
  unit: string;
  instrument: string;
  date: string;
  analyst: string;
  replicate_num: number | null;
  notes: string;
  attachments: Attachment[];
}

export enum ApplicationType {
    CHEESE_MELT = 'Cheese Melt',
    GELATION = 'Gelation',
    EMULSION = 'Emulsion',
    FOAM = 'Foam',
    BINDING = 'Binding',
    OTHER = 'Other',
}

export interface FunctionalTest {
  id: string;
  extraction_id: string;
  application_type: ApplicationType;
  condition: string;
  performance_metric: string;
  score_or_value: string;
  evaluator: string;
  date: string;
  comments: string;
  attachments: Attachment[];
}
