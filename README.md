# 🏥 FDA Nutrition Label Compliance Checker

**Automated compliance validation for plant-based meat & dairy product labels**

Internal tool to check nutrition labels against FDA regulations (21 CFR 101.9, 101.4, FALCPA).

---

## ✨ Features

- 📤 **Upload** PDF or image files of nutrition labels
- 🤖 **AI-Powered Extraction** using GPT-4 Vision for accurate OCR
- ✅ **Automated Compliance Checks** against FDA requirements
- 📊 **Detailed Reports** with pass/fail status for each requirement
- 📥 **PDF Export** of compliance results
- 🔍 **60+ Validation Rules** covering:
  - Nutrition Facts format (single/dual column)
  - RACC serving size compliance
  - Rounding rules validation
  - Nutrient order and formatting
  - % Daily Value calculations
  - Allergen declarations (Top 9)
  - Ingredient list requirements
  - Required label elements

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key (for GPT-4 Vision)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd BO
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key:
   # OPENAI_API_KEY=sk-your-key-here
   ```

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If not, navigate to the URL shown in your terminal

---

## 📖 How to Use

### Step 1: Select Product Type
In the sidebar, choose your product type (e.g., "plant-based-deli-slices") for accurate RACC validation.

### Step 2: Upload Label
- Drag and drop or click to upload
- Supported formats: PDF, PNG, JPG, JPEG
- Max file size: 10MB

### Step 3: Analyze
Click the "🚀 Analyze Label" button to:
1. Extract data using GPT-4 Vision
2. Run 60+ compliance checks
3. Generate detailed results

### Step 4: Review Results
- View overall compliance score
- Check detailed pass/fail status for each requirement
- Review extracted nutrition data
- See CFR references for each check

### Step 5: Export Report
Download a professional PDF report with all compliance results.

---

## 📋 What Gets Checked

### 1. **Nutrition Facts Format** (21 CFR 101.9(d))
- Single vs. dual-column format
- Dual-column requirements based on servings
- Column labeling

### 2. **Serving Size** (21 CFR 101.9(b))
- RACC compliance (Reference Amount Customarily Consumed)
- Metric units (g or mL)
- Household measures
- Servings per container declaration

### 3. **Calories**
- Proper formatting (bold, larger font)
- Per-serving values
- Per-container values (if dual-column)

### 4. **Nutrient Order & Units**
- FDA-required nutrient order
- Correct units (g, mg, mcg)
- Bold/indentation formatting

### 5. **% Daily Values** (21 CFR 101.9(d)(9))
- All mandatory %DV declarations
- 2016 FDA reference values
- Trans fat (no %DV) validation
- Added sugars %DV requirement

### 6. **Rounding Rules** (21 CFR 101.9(c))
- **Total Fat/Saturated Fat**: Nearest 0.5g if <5g, nearest 1g if ≥5g
- **Trans Fat**: Must be 0g or 0.5g only
- **Sodium**: Nearest 5mg if <140mg, nearest 10mg if ≥140mg
- **Sugars**: Nearest 1g
- **Protein**: Nearest whole gram
- **Vitamins/Minerals**: %DV to whole numbers

### 7. **Footnote**
- Required FDA footnote text
- Proper formatting

### 8. **Ingredient List** (21 CFR 101.4)
- "Ingredients:" label in bold
- Descending order by weight
- Sub-ingredients in parentheses
- Common/usual names

### 9. **Allergen Declaration** (FALCPA)
- "Contains:" statement
- Top 9 allergens coverage
- Prominent placement

### 10. **Other Required Elements**
- Net weight declaration
- Manufacturer name & address
- Storage/handling instructions
- Product identity

---

## 🏗️ Project Structure

```
BO/
├── app.py                      # Main Streamlit application
├── extractor.py                # GPT-4 Vision data extraction
├── validators.py               # Compliance validation functions
├── report_generator.py         # PDF report generation
├── checklist_config.json       # Compliance rules configuration
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

---

## 🔧 Configuration

### Product Types & RACC Values

The app includes RACC (Reference Amount Customarily Consumed) values for common plant-based products:

| Product Type | RACC |
|--------------|------|
| Deli Slices | 55g |
| Burgers | 110g |
| Sausages | 55g |
| Ground Meat | 84g |
| Milk | 240mL |
| Cheese | 30g |
| Yogurt | 170g |

Edit `checklist_config.json` to add more product types or modify RACC values.

### Customizing Checks

All compliance checks are defined in `checklist_config.json`. You can:
- Add new categories
- Modify check requirements
- Update CFR references
- Change severity levels

---

## 🧪 API Costs

**OpenAI GPT-4o (Vision)**:
- Approximate cost: $0.03-0.05 per label
- Based on image size and complexity
- High accuracy for text extraction

**Tips to reduce costs**:
- Optimize image resolution (recommended: 1200-2000px width)
- Use clear, high-contrast images
- Crop to show only the nutrition label

---

## ⚠️ Limitations & Disclaimers

### Important Notes

1. **This tool is for INTERNAL USE ONLY**
   - Not a substitute for legal/regulatory review
   - Does not constitute official compliance certification
   - Always verify with qualified regulatory professionals

2. **AI Extraction Limitations**
   - OCR may misread unclear or low-quality images
   - Manual verification recommended for critical checks
   - Confidence varies based on image quality

3. **Manual Checks Required**
   - Visual formatting (bold, italics, font sizes)
   - Exact ingredient order verification
   - Label placement and sizing
   - Color contrast and readability

4. **Regulatory Changes**
   - CFR regulations may be updated
   - Always check current FDA guidelines
   - This tool reflects regulations as of 2024

---

## 🐛 Troubleshooting

### "OpenAI API Key Missing" Error
- Check that `.env` file exists in the project root
- Verify `OPENAI_API_KEY=sk-...` is set correctly
- Restart the Streamlit app after adding the key

### Poor Extraction Results
- Use high-resolution images (300+ DPI)
- Ensure label is clearly visible and well-lit
- Try converting PDF to image first
- Crop to show only the nutrition facts panel

### "Validator Error" Messages
- Some checks may fail if data wasn't extracted
- Review the extracted data in the results
- Manually correct extraction if needed
- Report persistent issues as bugs

### PDF Generation Fails
- Check that all required fields are present
- Ensure reportlab is installed: `pip install reportlab`
- Try reducing the size of extracted data

---

## 🔐 Security & Privacy

- **No data storage**: Uploaded files are processed in memory only
- **API security**: OpenAI API key stored in local `.env` file only
- **No logging**: Nutrition data is not saved or logged
- **Local processing**: All validation runs on your machine

---

## 📚 Resources

### FDA Regulations
- [21 CFR 101.9 - Nutrition Labeling](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-B/part-101/subpart-A/section-101.9)
- [21 CFR 101.4 - Food; Designation of Ingredients](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-B/part-101/subpart-A/section-101.4)
- [FALCPA - Food Allergen Labeling](https://www.fda.gov/food/food-allergensgluten-free-guidance-documents-regulatory-information/food-allergen-labeling-and-consumer-protection-act-2004-falcpa)

### FDA Guidance Documents
- [Nutrition Facts Label Guide](https://www.fda.gov/food/nutrition-facts-label/how-understand-and-use-nutrition-facts-label)
- [RACC Tables](https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfcfr/CFRSearch.cfm?fr=101.12)
- [Daily Values](https://www.fda.gov/food/nutrition-facts-label/daily-value-nutrition-and-supplement-facts-labels)

---

## 🛠️ Development

### Tech Stack
- **Frontend/Backend**: Streamlit
- **OCR/Extraction**: OpenAI GPT-4o Vision API
- **PDF Generation**: ReportLab
- **Image Processing**: Pillow, pdf2image

### Adding New Validators

1. Add check to `checklist_config.json`:
   ```json
   {
     "id": "my_new_check",
     "requirement": "Description of requirement",
     "validator": "check_my_new_rule",
     "severity": "critical"
   }
   ```

2. Implement validator in `validators.py`:
   ```python
   def check_my_new_rule(data, check, category):
       # Your validation logic
       return {
           "status": "PASS" | "FAIL" | "WARNING" | "MANUAL",
           "details": "Explanation of result"
       }
   ```

3. Register in `get_validators()` function

---

## 📝 License

Internal use only. Not for distribution.

---

## 🤝 Support

For questions or issues:
1. Check the troubleshooting section above
2. Review the FDA resources
3. Contact your regulatory compliance team

---

## ✅ Checklist Before First Use

- [ ] Python 3.8+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] OpenAI API key added to `.env` file
- [ ] App runs successfully (`streamlit run app.py`)
- [ ] Test with a sample nutrition label
- [ ] Review and understand limitations
- [ ] Confirm internal use only

---

**Ready to check your labels!** 🚀

Run `streamlit run app.py` and upload your first nutrition label.
