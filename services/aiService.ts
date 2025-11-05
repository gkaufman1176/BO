import { GoogleGenAI, Type } from "@google/genai";
import { ingredientApi } from './apiService';

// This schema defines all possible fields across all data types to guide the AI.
const allFieldsSchema = {
    type: Type.OBJECT,
    properties: {
        // Ingredient fields
        name: { type: Type.STRING, description: "Name of the ingredient" },
        supplier: { type: Type.STRING },
        batch_id: { type: Type.STRING, description: "Batch or Lot ID for the ingredient" },
        form: { type: Type.STRING, enum: ['powder', 'slurry', 'isolate', 'concentrate', 'liquid'] },
        protein_pct: { type: Type.NUMBER },
        moisture_pct: { type: Type.NUMBER },
        ash_pct: { type: Type.NUMBER },
        ph: { type: Type.NUMBER },
        color_visual_notes: { type: Type.STRING },
        storage_condition: { type: Type.STRING },
        received_date: { type: Type.STRING, description: "Date in ISO 8601 format" },
        comments: { type: Type.STRING },

        // Extraction fields
        ingredient_id: { type: Type.STRING, description: "The batch_id of the ingredient being used, NOT the internal system ID." },
        method: { type: Type.STRING },
        salt_conc: { type: Type.NUMBER, description: "Salt concentration in percent" },
        temp_c: { type: Type.NUMBER, description: "Temperature in Celsius" },
        time_min: { type: Type.NUMBER, description: "Time in minutes" },
        solids_pct: { type: Type.NUMBER },
        yield_pct: { type: Type.NUMBER },
        centrifuge: { type: Type.STRING, description: "Centrifuge settings, e.g., '4000x15'" },
        filtration_type: { type: Type.STRING, enum: ['Micro', 'UF', 'None', ''] },
        supernatant_color: { type: Type.STRING },
        texture_observation: { type: Type.STRING },
        operator: { type: Type.STRING },
        date: { type: Type.STRING, description: "Date in ISO 8601 format" },
        notes: { type: Type.STRING },

        // Assay fields
        extraction_id: { type: Type.STRING, description: "The ID of the extraction lot, e.g. 'EXT-240101'" },
        assay_type: { type: Type.STRING, enum: ['Solubility', 'DSC', 'DLS', 'Turbiscan', 'Texture', 'pH Stability'] },
        parameter: { type: Type.STRING },
        value: { type: Type.NUMBER },
        unit: { type: Type.STRING },
        instrument: { type: Type.STRING },
        analyst: { type: Type.STRING },
        replicate_num: { type: Type.INTEGER },

        // Functional Test fields
        application_type: { type: Type.STRING, enum: ['Cheese Melt', 'Gelation', 'Emulsion', 'Foam', 'Binding', 'Other'] },
        condition: { type: Type.STRING },
        performance_metric: { type: Type.STRING },
        score_or_value: { type: Type.STRING },
        evaluator: { type: Type.STRING },
    },
};


export const aiService = {
  async parseTextToData(text: string): Promise<{ dataType: string; data: any }> {
    const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });

    const response = await ai.models.generateContent({
        model: "gemini-2.5-flash",
        contents: `Analyze the following text and convert it into a structured data entry for a lab notebook. The text is: "${text}"`,
        config: {
            responseMimeType: "application/json",
            responseSchema: {
                type: Type.OBJECT,
                properties: {
                    dataType: {
                        type: Type.STRING,
                        description: "The type of data being entered. Must be one of: 'ingredients', 'extractions', 'assays', or 'functional_tests'.",
                        enum: ['ingredients', 'extractions', 'assays', 'functional_tests']
                    },
                    data: allFieldsSchema,
                },
                required: ['dataType', 'data'],
            }
        },
    });

    try {
        const jsonString = response.text.trim();
        const parsed = JSON.parse(jsonString);

        // A common issue is the model nesting the data object inside another data object.
        if (parsed.data && parsed.data.data) {
            parsed.data = parsed.data.data;
        }

        // Gemini might return the ingredient's batch_id for `ingredient_id`.
        // We need to look up the internal ID for linking.
        if (parsed.dataType === 'extractions' && parsed.data.ingredient_id) {
            const allIngredients = await ingredientApi.getAll();
            const ingredient = allIngredients.find(i => i.batch_id === parsed.data.ingredient_id);
            if (ingredient) {
                // Replace the human-readable batch_id with the internal system ID.
                parsed.data.ingredient_id = ingredient.id;
            } else {
                console.warn(`Ingredient with batch_id '${parsed.data.ingredient_id}' not found.`);
                parsed.data.ingredient_id = '';
            }
        }

        return parsed;

    } catch (e) {
      console.error("Failed to parse AI response:", e);
      throw new Error("Could not understand the provided text.");
    }
  },
};
