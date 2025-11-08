# EXPERIMENTAL PROTOCOLS FOR ACTION LAB
## Scalable Aqueous Protein Extraction Methods - Months 1-3

---

## PROTOCOL 1: SALT EXTRACTION + ULTRAFILTRATION (SE-UF)

### Materials:
- Defatted protein meal (hemp, sunflower, chickpea, pumpkin seed)
- Potassium chloride (KCl), food-grade
- Sodium hydroxide (NaOH) 1M for pH adjustment
- Hydrochloric acid (HCl) 1M for pH adjustment
- Ultrafiltration system with 10 kDa MWCO membrane (tangential flow)
- Centrifuge (4000 rpm minimum)
- pH meter
- Magnetic stirrer with temperature control

### Procedure:

**Step 1: Defatting (if needed)**
1. Grind seeds/meals to <0.5 mm particle size
2. Mix with hexane (1:3 w/v) at room temperature, stir 2h
3. Filter and air-dry to remove hexane
4. *Alternative aqueous defatting:* Use enzyme-assisted oil extraction (not covered here)

**Step 2: Salting-In Extraction**
1. Mix defatted meal with distilled water (1:10 w/v)
2. Add KCl to final concentration 0.4 M
3. Adjust pH to 7.2 with 1M NaOH
4. Stir at room temperature (20-25°C) for 1.5h
5. Centrifuge at 4000 rpm, 20 min to remove insoluble fiber
6. Collect supernatant (protein extract)

**Step 3: Ultrafiltration Concentration**
1. Load supernatant into UF system (10 kDa MWCO)
2. Operate at transmembrane pressure 2-3 bar
3. Concentrate 5-fold (retentate volume = 1/5 of initial)
4. Measure protein content in retentate and permeate

**Step 4: Diafiltration (Salt Removal)**
1. Add 3 volumes of distilled water to retentate
2. Concentrate back to original retentate volume
3. Repeat 2-3 times until permeate conductivity <2 mS/cm
4. Final protein concentrate: pH 6.8-7.2, low salt

**Step 5: Drying (optional)**
1. Freeze-dry retentate or spray-dry at inlet 160-180°C
2. Grind dried protein isolate to powder
3. Store at -20°C in sealed containers

### Measurements:
- **Protein yield (%)** = (Protein in isolate / Protein in starting meal) × 100
- **Protein purity (%)** = (Protein content in isolate / Total solids) × 100 (Kjeldahl N × 6.25)
- **Solubility at pH 7.0 (%)** = (Soluble protein / Total protein) × 100 after centrifugation
- **Residual salt:** Conductivity measurement

### Expected Results:
- Protein yield: 85-92%
- Protein purity: 88-95%
- Solubility at pH 7.0: 60-75%

### Scale-Up Notes:
- For 10 kg batch: 1 kg meal → 10 L water → UF system (100-200 L/h capacity)
- Estimated time: 4-6 hours total
- Water usage: ~50 L/kg protein (including diafiltration)

---

## PROTOCOL 2: ENZYMATIC PRE-TREATMENT + SE-UF

### Additional Materials (beyond Protocol 1):
- Cellulase (food-grade, e.g., Celluclast 1.5L from Novozymes)
- Phytase (food-grade, e.g., Natuphos from BASF)
- Water bath or jacketed reactor (50°C)

### Procedure:

**Step 1: Enzymatic Pre-Treatment**
1. Mix defatted meal with distilled water (1:10 w/v)
2. Adjust pH to 5.5 with 1M HCl
3. Heat to 50°C
4. Add cellulase (1% w/w of meal) and phytase (0.5% w/w of meal)
5. Incubate at 50°C with gentle stirring for 1.5h
6. Heat to 85°C for 10 min to inactivate enzymes
7. Cool to room temperature

**Step 2-5: Follow Protocol 1 (SE-UF)**
- Proceed with KCl extraction, UF, diafiltration, drying

### Measurements (additional):
- **Fiber reduction (%)** = (Fiber in meal - Fiber in isolate) / Fiber in meal × 100
- **Phytic acid reduction (%)** = Measured by HPLC or colorimetric assay
- **Yield improvement vs. SE-UF alone**

### Expected Results:
- Protein yield: 92-97% (10-15% improvement over SE-UF alone for high-fiber proteins)
- Fiber content in isolate: <3% (vs. 5-8% without enzymes)
- Phytic acid reduction: 60-80%

### Economics:
- Enzyme cost: $0.30-$0.50/kg meal (cellulase $15-25/kg, phytase $30-50/kg)
- Added time: 2h (enzymatic incubation + inactivation)

---

## PROTOCOL 3: REVERSIBLE SALT PRECIPITATION (AMMONIUM SULFATE)

### Materials:
- Defatted protein meal
- Ammonium sulfate ((NH₄)₂SO₄), food-grade
- Dialysis tubing (10-12 kDa MWCO) or UF system
- Centrifuge
- Magnetic stirrer

### Procedure:

**Step 1: Protein Extraction**
1. Mix defatted meal with distilled water (1:10 w/v)
2. Adjust pH to 7.5 with 1M NaOH
3. Stir at room temperature for 1.5h
4. Centrifuge at 4000 rpm, 20 min
5. Collect supernatant

**Step 2: Salting-Out Precipitation**
1. Calculate amount of (NH₄)₂SO₄ needed for 60% saturation (~390 g/L)
2. Add (NH₄)₂SO₄ slowly to supernatant with stirring (over 30 min)
3. Stir additional 30 min after complete addition
4. Centrifuge at 4000 rpm, 30 min
5. Collect protein pellet, discard supernatant (save for recycling)

**Step 3: Resolubilization**
1. Dissolve pellet in minimum volume of distilled water (pH 7.0)
2. Protein solution will be high in residual (NH₄)₂SO₄

**Step 4: Desalting (Option A - Dialysis)**
1. Transfer protein solution to dialysis tubing
2. Dialyze against distilled water (1:50 v/v) at 4°C
3. Change water 3-4 times over 24h
4. Final protein solution: low salt, pH ~6.5-7.0

**Step 4: Desalting (Option B - Diafiltration)**
1. Load protein solution into UF system (10 kDa MWCO)
2. Diafilter with 5-10 volumes of distilled water
3. Faster than dialysis (2-3h vs. 24h)

**Step 5: Drying**
- Freeze-dry or spray-dry as in Protocol 1

### Measurements:
- Protein yield, purity, solubility (same as Protocol 1)
- Residual (NH₄)₂SO₄: Can be measured by ion chromatography

### Expected Results:
- Protein yield: 75-85%
- Protein purity: 85-92%
- Solubility at pH 7.0: 55-70% (depends on desalting efficiency)

### Economics:
- (NH₄)₂SO₄ cost: $0.05-$0.10/kg protein (cheap, recyclable)
- Dialysis: Labor-intensive, slow
- Diafiltration: Faster, preferred for scale-up

### (NH₄)₂SO₄ Recycling:
- Supernatant from Step 2 contains ~60% saturated (NH₄)₂SO₄
- Can be concentrated and reused (multiple cycles)
- Reduces consumable cost to <$0.05/kg protein

---

## PROTOCOL 4: FUNCTIONAL TESTING - CHEESE APPLICATION

### Materials:
- Protein isolates from Protocols 1-3
- Coconut oil (refined)
- Waxy maize starch
- Kappa-carrageenan
- Salt, citric acid, nutritional yeast (optional for flavor)
- Texture analyzer with compression probe
- Differential scanning calorimeter (DSC)
- Pizza oven or conventional oven

### Cheese Analog Formulation (100g total):
- Protein isolate: 8.0 g
- Coconut oil: 20.0 g
- Waxy maize starch: 4.0 g
- Kappa-carrageenan: 1.5 g
- Water: 63.5 g
- Salt: 2.0 g
- Citric acid: 0.5 g (pH ~5.5-5.8)
- Nutritional yeast: 0.5 g (optional)

### Procedure:

**Step 1: Prepare Cheese Analog**
1. Blend protein isolate with cold water (stir to disperse)
2. Heat to 60°C, add coconut oil (melted), starch, carrageenan
3. Blend at high speed for 2 min
4. Add salt, citric acid, nutritional yeast
5. Heat to 85°C with continuous stirring (10 min)
6. Pour into molds (50 g portions)
7. Refrigerate at 4°C for 2h to set

**Step 2: Gel Strength Measurement**
1. Use texture analyzer with cylindrical probe (12.7 mm diameter)
2. Compression test: 50% strain at 1 mm/s
3. Record maximum force (N)
4. Convert to stress (kPa) = Force / Area
5. Repeat 5 times per sample

**Step 3: Thermal Stability (DSC)**
1. Weigh 10-15 mg cheese analog into DSC pan
2. Heat from 20°C to 120°C at 5°C/min
3. Record melting temperature (Tm) and enthalpy (ΔH)

**Step 4: Melt/Stretch Test (Pizza Oven)**
1. Shred cheese analog (coarse grater)
2. Spread 50 g on pizza dough or bread
3. Bake at 220°C for 10 min
4. Visual assessment: melting (yes/no), browning, oil separation
5. Stretch test: Lift with spatula, measure stretch distance (cm)
6. Photo documentation

**Step 5: Water Holding Capacity**
1. Weigh 5 g cheese analog (W1)
2. Centrifuge at 3000 rpm, 10 min
3. Decant and weigh expelled water (W2)
4. WHC (g/g) = (W1 - W2) / Protein weight in sample

### Scoring (vs. Animal Baseline):
- **Gel strength:** Target >60 kPa (casein ~80-100 kPa)
- **Tm:** Target >75°C (casein Tm ~78-82°C)
- **Melt:** Visual score 1-5 (1=no melt, 5=full melt like mozzarella)
- **Stretch:** Target >10 cm (mozzarella ~20-30 cm)
- **WHC:** Target >2.5 g/g

### Comparison:
- Run 3 controls: Commercial pea protein, soy protein, dairy mozzarella
- Rank all samples

---

## PROTOCOL 5: FUNCTIONAL TESTING - EGG APPLICATION

### Foaming Test:

**Materials:**
- Protein isolates (10% solution, pH 7.0)
- Whisk or stand mixer
- Graduated cylinder (250 mL)
- Timer

**Procedure:**
1. Prepare 10% protein solution (10 g protein in 100 mL water, pH 7.0)
2. Measure 50 mL into mixing bowl
3. Whip at high speed (Kitchen Aid speed 8) for 5 min
4. Immediately transfer to graduated cylinder
5. Record total volume (V1)
6. **Foaming Capacity (FC)** = V1 - 50 mL
7. Let stand at room temperature, measure volume at 30 min (V2)
8. **Foam Stability (%)** = (V2 - 50) / (V1 - 50) × 100

**Target:**
- FC >150 mL (egg white ~200-250 mL)
- Foam Stability >40% (egg white ~60-70%)

### Emulsion Test:

**Materials:**
- Protein isolates (2% solution)
- Canola oil
- Homogenizer or high-speed blender
- Graduated cylinder

**Procedure:**
1. Prepare 2% protein solution (2 g in 100 mL water, pH 7.0)
2. Add canola oil dropwise while blending at high speed
3. Continue until phase inversion (emulsion breaks)
4. Record total oil added (mL)
5. **Emulsifying Capacity (EC)** = mL oil / g protein

**Stability Test:**
1. Prepare emulsion with 50% oil (50 mL protein solution + 50 mL oil)
2. Homogenize 2 min at high speed
3. Pour into graduated cylinder (100 mL total)
4. Let stand 24h at room temperature
5. Measure cream layer (top), emulsion layer (middle), serum (bottom)
6. **Emulsion Stability (%)** = (Emulsion layer / Total volume) × 100

**Target:**
- EC >300 mL oil/g protein (egg ~400-500 mL/g)
- Emulsion Stability >60%

### Baking Test (Muffins):

**Control Recipe (with egg):**
- 150 g flour
- 100 g sugar
- 2 eggs (100 g)
- 50 g butter
- 100 mL milk
- 5 g baking powder

**Egg Replacement:**
- Replace 100 g egg with 100 g protein solution
- Protein solution: 15 g protein isolate + 85 g water (to mimic egg protein content ~13-15%)

**Procedure:**
1. Mix dry ingredients (flour, sugar, baking powder)
2. Mix wet ingredients (protein solution or egg, melted butter, milk)
3. Combine wet and dry, mix until just combined
4. Pour into muffin cups (50 g each)
5. Bake at 180°C for 20 min
6. Cool 10 min

**Evaluation:**
- Height (cm) - measure center of muffin
- Volume (mL) - rapeseed displacement method
- Texture - crumb structure (visual score 1-5)
- Moisture - hand-feel (dry vs. moist)
- Taste - sensory panel (if available)

**Target:**
- Height >80% of egg control
- Volume >80% of egg control
- Texture score >3/5

---

## PROTOCOL 6: FUNCTIONAL TESTING - BEVERAGE APPLICATION

### Solubility Test:

**Procedure:**
1. Prepare protein solutions at different pH values:
   - pH 3.5 (citric acid buffer)
   - pH 7.0 (phosphate buffer)
   - pH 9.0 (borate buffer)
2. Add protein isolate to buffer (5% w/v)
3. Stir 30 min at room temperature
4. Centrifuge 4000 rpm, 20 min
5. Measure protein in supernatant (Bradford or Lowry assay)
6. **Solubility (%)** = (Protein in supernatant / Total protein) × 100

**Target:**
- pH 7.0: >60% (whey ~95%, soy ~70-80%)
- pH 3.5: >40% (challenging for plant proteins)

### Turbidity Test:

**Procedure:**
1. Prepare 3% protein solution at pH 7.0
2. Stir 30 min, let stand 10 min
3. Measure turbidity with turbidimeter (NTU units)
4. Or measure absorbance at 600 nm (higher = more turbid)

**Target:**
- Clear beverage: <0.5 NTU
- Opaque beverage (protein shake): <2.0 NTU acceptable

### Stability Test (7-day):

**Procedure:**
1. Prepare 3% protein beverage at pH 7.0 (or pH 3.5 for acidic test)
2. Add stabilizers if testing formulation (e.g., 0.2% carrageenan)
3. Pour into clear bottles (100 mL)
4. Store at 4°C
5. Visual inspection daily for 7 days:
   - Sedimentation (yes/no)
   - Phase separation (yes/no)
   - Color change (yes/no)
6. On day 7, measure turbidity again

**Target:**
- No visible sedimentation
- Turbidity change <20% from day 0

### Particle Size Analysis:

**Procedure:**
1. Prepare 1% protein solution (dilute for measurement)
2. Measure by dynamic light scattering (DLS)
3. Record Z-average diameter (nm) and polydispersity index (PDI)

**Target:**
- Particle size <500 nm (smaller = better stability)
- PDI <0.3 (narrow distribution)

---

## PROTOCOL 7: ECONOMIC ANALYSIS (PILOT SCALE 10 KG PROTEIN)

### Data Collection Template:

**Input:**
- Starting material: ____ kg defatted meal
- Protein content in meal: _____%

**Water Usage:**
| Step | Volume (L) |
|------|------------|
| Extraction | |
| UF/DF rinse | |
| Diafiltration | |
| Equipment cleaning | |
| **TOTAL** | |

**Water usage (L/kg protein)** = Total L / 10 kg

**Energy Consumption:**
| Equipment | Power (kW) | Time (h) | Energy (kWh) |
|-----------|-----------|----------|--------------|
| Stirrer/mixer | | | |
| Centrifuge | | | |
| UF pump | | | |
| Heating (enzymatic) | | | |
| Freeze-dryer | | | |
| **TOTAL** | | | |

**Energy (kWh/kg protein)** = Total kWh / 10 kg

**Consumables Cost:**
| Item | Amount | Unit Cost ($/unit) | Total Cost ($) |
|------|--------|-------------------|----------------|
| KCl or (NH₄)₂SO₄ | | | |
| Enzymes (if used) | | | |
| Acid/base | | | |
| Membrane replacement (amortized) | | | |
| **TOTAL** | | | |

**Consumables ($/kg protein)** = Total $ / 10 kg

**Labor:**
- Total labor hours: ____
- Labor rate: $____ /h
- **Labor cost ($/kg protein)** = (Hours × Rate) / 10 kg

**Equipment Depreciation:**
- Capital cost of equipment: $____
- Useful life: ____ years
- Annual batches: ____
- Kg protein per batch: 10 kg
- **Depreciation ($/kg protein)** = (Capital / Life / Annual batches) / 10 kg

**TOTAL COGS ($/kg protein):**
= Consumables + Labor + Energy (at $0.12/kWh) + Depreciation

**Target: <$2.00/kg protein**

### Yield Calculation:
- Starting protein (kg) = Meal kg × Protein %
- Final protein (kg) = should be ~10 kg
- **Yield (%)** = (Final / Starting) × 100

**Target: >85% yield**

---

## MONTH 1-3 SCHEDULE SUMMARY

### Month 1:
- Week 1-2: Run Protocols 1-3 on hemp, sunflower, chickpea, pumpkin (SE-UF, Enzymatic+SE-UF, Ammonium sulfate)
- Week 3-4: Measure yields, purity, solubility; rank methods

### Month 2:
- Week 5-6: Protocol 4 (cheese testing) on top 3 proteins from Month 1
- Week 7-8: Protocols 5-6 (egg and beverage testing)

### Month 3:
- Week 9-10: Protocol 7 (economic analysis) at 10 kg scale
- Week 11-12: Data analysis, final report, patent drafting

---

**END OF EXPERIMENTAL PROTOCOLS**
