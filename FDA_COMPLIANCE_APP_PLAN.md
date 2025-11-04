# FDA Nutrition Label Compliance Checker App - Development Plan

## 📋 Project Overview

**Goal**: Build an application that automatically validates nutrition labels and spec sheets against FDA compliance requirements (21 CFR 101.9, 101.4, FALCPA) for plant-based meat and dairy products.

**Core Functionality**:
1. Upload spec sheets or packaging label images
2. Extract text and structured data using OCR
3. Check compliance against your comprehensive checklist
4. Reference relevant CFR regulations
5. Generate detailed compliance reports

---

## 🏗️ System Architecture

### **Option A: Full-Stack Web Application (Recommended)**
```
┌─────────────────┐
│   Frontend      │  React/Next.js + TypeScript
│   (User Upload) │  - File upload UI
└────────┬────────┘  - Results dashboard
         │           - PDF report generation
         ▼
┌─────────────────┐
│   Backend API   │  Python/FastAPI or Node.js/Express
│   (Processing)  │  - Document processing
└────────┬────────┘  - Compliance engine
         │           - CFR integration
         ▼
┌─────────────────┐
│   AI/ML Layer   │  - OCR (Tesseract, Google Vision, AWS Textract)
│   (Extraction)  │  - GPT-4/Claude for structured extraction
└────────┬────────┘  - NLP for regulation matching
         │
         ▼
┌─────────────────┐
│   Database      │  PostgreSQL or MongoDB
│   (Storage)     │  - Checklist templates
└─────────────────┘  - CFR regulations
                     - Audit history
```

### **Option B: Streamlit Prototype (Faster MVP)**
```
┌─────────────────┐
│  Streamlit App  │  Single Python app
│  (All-in-One)   │  - Upload interface
└────────┬────────┘  - Processing logic
         │           - Results display
         ▼
┌─────────────────┐
│   AI Services   │  OpenAI API / Claude API
│   (External)    │  Google Vision API
└─────────────────┘
```

---

## 🎯 Phase 1: Foundation & Core Features

### 1.1 Technology Stack Selection

**Backend Options**:
- **Python + FastAPI** ✅ (Recommended for ML/AI integration)
  - Libraries: Pytesseract, pdf2image, Pillow, OpenAI SDK
  - Better for document processing

- **Node.js + Express**
  - Better for real-time processing
  - Libraries: Tesseract.js, Sharp, Multer

**Frontend**:
- **React + TypeScript** (robust, scalable)
- **Next.js** (includes backend API routes)
- **Streamlit** (rapid prototyping, Python-only)

**OCR/Document Processing**:
1. **Tesseract OCR** (free, open-source)
2. **Google Cloud Vision API** (paid, high accuracy)
3. **AWS Textract** (paid, structured data extraction)
4. **Azure Computer Vision** (paid)

**AI/LLM Integration**:
- **OpenAI GPT-4 Vision** - Can analyze images directly
- **Claude 3.5 Sonnet** - Excellent at structured extraction
- **Google Gemini** - Multimodal capabilities

### 1.2 Data Structure Design

```json
{
  "upload": {
    "id": "uuid",
    "filename": "nutrition_label.pdf",
    "uploadedAt": "2025-11-04T10:00:00Z",
    "productType": "plant-based-meat"
  },
  "extractedData": {
    "servingSize": {
      "value": 55,
      "unit": "g",
      "householdMeasure": "about 5 slices"
    },
    "servingsPerContainer": 2.5,
    "calories": 120,
    "nutrients": {
      "totalFat": {"value": 5, "unit": "g", "dailyValue": 6},
      "saturatedFat": {"value": 0.5, "unit": "g", "dailyValue": 3},
      "transFat": {"value": 0, "unit": "g"},
      "cholesterol": {"value": 0, "unit": "mg", "dailyValue": 0},
      // ... more nutrients
    },
    "ingredients": ["Water", "Pea Protein", "..."],
    "allergens": ["Soy"]
  },
  "complianceResults": {
    "overallScore": 85,
    "passed": 42,
    "failed": 8,
    "warnings": 5,
    "checks": [
      {
        "category": "Nutrition Facts Format Type",
        "requirement": "Does the label use the correct layout format?",
        "status": "PASS",
        "confidence": 0.95,
        "details": "Single-column format detected"
      },
      // ... all checklist items
    ]
  }
}
```

---

## 🔍 Phase 2: Document Processing Pipeline

### 2.1 Image/PDF Upload & Preprocessing

```python
# Pseudo-code workflow
def process_upload(file):
    # Step 1: Convert PDF to images (if needed)
    if file.type == "pdf":
        images = convert_pdf_to_images(file)
    else:
        images = [file]

    # Step 2: Preprocess images
    for img in images:
        img = resize_image(img, max_width=2000)
        img = enhance_contrast(img)
        img = deskew(img)  # Fix rotation

    return images
```

### 2.2 OCR Text Extraction

**Method 1: Traditional OCR**
```python
import pytesseract
from PIL import Image

def extract_text_ocr(image):
    text = pytesseract.image_to_string(image)
    return text
```

**Method 2: Vision API + LLM (Recommended)**
```python
import openai

def extract_structured_data(image_path):
    response = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": """Extract nutrition facts from this label.
                    Return JSON with: servingSize, calories, nutrients, ingredients, allergens.
                    Follow FDA formatting rules."""
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                }
            ]
        }],
        response_format={"type": "json_object"}
    )
    return response.choices[0].message.content
```

### 2.3 Data Validation & Normalization

```python
def validate_extracted_data(data):
    errors = []

    # Check required fields
    if not data.get("servingSize"):
        errors.append("Missing serving size")

    # Validate nutrient values
    if data.get("transFat", 0) > 0 and data.get("transFat") not in [0, 0.5]:
        errors.append("Trans fat must be 0 or 0.5g")

    # Check rounding rules
    total_fat = data.get("totalFat", {}).get("value", 0)
    if total_fat < 5 and (total_fat % 0.5 != 0):
        errors.append("Total fat <5g must be rounded to nearest 0.5g")

    return errors
```

---

## ✅ Phase 3: Compliance Checking Engine

### 3.1 Checklist Implementation

**Convert your markdown checklist to structured data:**

```python
COMPLIANCE_CHECKLIST = {
    "nutrition_facts_format": {
        "category": "Nutrition Facts Format Type",
        "checks": [
            {
                "id": "format_type",
                "requirement": "Does the label use the correct layout format?",
                "validator": "check_format_type",
                "severity": "critical",
                "cfr_reference": "21 CFR 101.9(d)"
            },
            {
                "id": "dual_column_required",
                "requirement": "Dual-column required if container is 100-200% RACC",
                "validator": "check_dual_column_requirement",
                "severity": "critical",
                "cfr_reference": "21 CFR 101.9(d)(11)"
            }
        ]
    },
    "serving_size": {
        "category": "Serving Size & Servings per Container",
        "checks": [
            {
                "id": "racc_compliance",
                "requirement": "Serving size uses RACC (e.g., ~55g for deli slices)",
                "validator": "check_racc_compliance",
                "severity": "critical",
                "cfr_reference": "21 CFR 101.9(b)(1)"
            }
        ]
    }
    # ... more categories
}
```

### 3.2 Validator Functions

```python
def check_format_type(extracted_data):
    """Check if nutrition facts format is correct"""
    servings_per_container = extracted_data.get("servingsPerContainer", 0)
    has_dual_column = extracted_data.get("formatType") == "dual-column"

    # Logic for dual-column requirement
    requires_dual = 1.5 <= servings_per_container <= 4

    if requires_dual and not has_dual_column:
        return {
            "status": "FAIL",
            "message": "Dual-column format required for 1.5-4 servings per container",
            "actual": f"{servings_per_container} servings, single-column",
            "expected": "Dual-column format"
        }

    return {"status": "PASS"}

def check_racc_compliance(extracted_data):
    """Check serving size against RACC tables"""
    RACC_TABLE = {
        "plant-based-deli-slices": 55,  # grams
        "plant-based-burgers": 110,
        "plant-based-sausages": 55,
        "plant-based-milk": 240  # mL
    }

    product_type = extracted_data.get("productType")
    serving_size = extracted_data.get("servingSize", {}).get("value")

    racc = RACC_TABLE.get(product_type)
    if not racc:
        return {"status": "WARNING", "message": "RACC not found for product type"}

    # Allow 10% variance
    if abs(serving_size - racc) > racc * 0.1:
        return {
            "status": "FAIL",
            "message": f"Serving size {serving_size}g differs from RACC {racc}g",
            "cfr_reference": "21 CFR 101.9(b)"
        }

    return {"status": "PASS"}
```

### 3.3 Rounding Rules Engine

```python
def validate_rounding_rules(extracted_data):
    """Validate all nutrient rounding per FDA rules"""
    results = []

    # Total Fat rounding
    total_fat = extracted_data["nutrients"]["totalFat"]["value"]
    if total_fat < 5:
        if total_fat % 0.5 != 0:
            results.append({
                "nutrient": "Total Fat",
                "status": "FAIL",
                "rule": "Round to nearest 0.5g if <5g",
                "actual": total_fat
            })
    elif total_fat >= 5:
        if total_fat % 1 != 0:
            results.append({
                "nutrient": "Total Fat",
                "status": "FAIL",
                "rule": "Round to nearest 1g if ≥5g",
                "actual": total_fat
            })

    # Trans Fat must be 0 or 0.5
    trans_fat = extracted_data["nutrients"]["transFat"]["value"]
    if trans_fat not in [0, 0.5]:
        results.append({
            "nutrient": "Trans Fat",
            "status": "FAIL",
            "rule": "Must be 0g or 0.5g only",
            "actual": trans_fat
        })

    # ... more rounding rules

    return results
```

---

## 📖 Phase 4: CFR Regulation Integration

### 4.1 CFR Data Structure

```python
CFR_REGULATIONS = {
    "21_CFR_101.9": {
        "title": "Nutrition labeling of food",
        "sections": {
            "(b)(1)": {
                "text": "Serving size declaration based on RACC...",
                "relevant_for": ["serving_size"],
                "penalty_level": "critical"
            },
            "(d)(11)": {
                "text": "Dual-column presentation...",
                "relevant_for": ["format_type"],
                "penalty_level": "critical"
            }
        }
    },
    "21_CFR_101.4": {
        "title": "Food; designation of ingredients",
        "sections": {
            "(a)": {
                "text": "Ingredients listed in descending order of predominance...",
                "relevant_for": ["ingredient_list"]
            }
        }
    }
}
```

### 4.2 Regulation Lookup & Linking

```python
def get_relevant_cfr(check_id):
    """Retrieve CFR text for specific check"""
    for reg_key, regulation in CFR_REGULATIONS.items():
        for section_key, section in regulation["sections"].items():
            if check_id in section["relevant_for"]:
                return {
                    "regulation": reg_key,
                    "section": section_key,
                    "text": section["text"],
                    "full_reference": f"{reg_key}{section_key}"
                }
    return None
```

### 4.3 Scraping CFR Regulations (Optional)

```python
# Use eCFR API or web scraping
import requests

def fetch_cfr_text(title, section):
    """Fetch live CFR text from eCFR API"""
    url = f"https://www.ecfr.gov/api/versioner/v1/full/{title}/{section}.json"
    response = requests.get(url)
    if response.ok:
        data = response.json()
        return data["content"]
    return None
```

---

## 🎨 Phase 5: User Interface Design

### 5.1 App Flow

```
1. Landing Page
   ├─ Product Type Selection
   │  ├─ Plant-Based Meat
   │  ├─ Plant-Based Dairy
   │  └─ Other (Generic)
   │
2. Upload Page
   ├─ Drag & Drop Zone
   ├─ File Type: PDF, JPG, PNG
   └─ Multiple File Support
   │
3. Processing Screen
   ├─ Progress Bar
   ├─ OCR Extraction Status
   └─ Compliance Check Status
   │
4. Results Dashboard
   ├─ Overall Compliance Score (%)
   ├─ Pass/Fail Summary
   ├─ Detailed Checklist Results
   │  ├─ Category Grouping
   │  ├─ Individual Check Status
   │  └─ CFR References
   ├─ Extracted Data Review
   │  ├─ Nutrition Facts Table
   │  └─ Edit/Correct Data
   └─ Export Options
      ├─ PDF Report
      └─ JSON/CSV Export
```

### 5.2 Wireframe Components

**Upload Component**:
```jsx
<UploadZone>
  <ProductTypeSelector />
  <FileDropzone
    acceptedTypes={['image/jpeg', 'image/png', 'application/pdf']}
    maxSize={10MB}
  />
  <FilePreview />
  <AnalyzeButton />
</UploadZone>
```

**Results Component**:
```jsx
<ResultsDashboard>
  <ComplianceScore score={85} />

  <ChecklistResults>
    {categories.map(category => (
      <CategoryCard>
        <CategoryHeader />
        <CheckList>
          {checks.map(check => (
            <CheckItem
              status={check.status}  // PASS, FAIL, WARNING
              requirement={check.requirement}
              cfrReference={check.cfr}
              details={check.details}
            />
          ))}
        </CheckList>
      </CategoryCard>
    ))}
  </ChecklistResults>

  <ExtractedDataPanel />
  <ExportButtons />
</ResultsDashboard>
```

---

## 🚀 Implementation Roadmap

### **Sprint 1: MVP Foundation (Week 1-2)**
- [ ] Set up project structure (backend + frontend)
- [ ] Implement file upload endpoint
- [ ] Basic OCR integration (Tesseract or GPT-4 Vision)
- [ ] Simple text extraction display
- [ ] Convert checklist to JSON structure

### **Sprint 2: Compliance Engine (Week 3-4)**
- [ ] Implement core validator functions
- [ ] Build rounding rules checker
- [ ] Create RACC compliance checker
- [ ] Format type validator
- [ ] Nutrient order validator

### **Sprint 3: Advanced Features (Week 5-6)**
- [ ] CFR regulation database integration
- [ ] Improve OCR accuracy (try multiple methods)
- [ ] Add confidence scoring
- [ ] Implement data correction UI
- [ ] Build detailed reporting

### **Sprint 4: Polish & Deploy (Week 7-8)**
- [ ] PDF report generation
- [ ] Export functionality (JSON, CSV)
- [ ] Error handling & validation
- [ ] User authentication (optional)
- [ ] Deploy to cloud (AWS, GCP, Vercel)

---

## 🛠️ Tech Stack Recommendation

### **Recommended: Full-Stack Modern Approach**

**Backend**:
- Python 3.11+ with FastAPI
- Libraries:
  - `pytesseract` or `openai` (GPT-4 Vision)
  - `pdf2image`, `Pillow` (image processing)
  - `pydantic` (data validation)
  - `sqlalchemy` + PostgreSQL (database)

**Frontend**:
- React 18+ with TypeScript
- Next.js 14 (App Router)
- TailwindCSS (styling)
- shadcn/ui (components)
- React Dropzone (file upload)
- Recharts (data visualization)

**AI/ML**:
- OpenAI GPT-4 Vision API
- OR Claude 3.5 Sonnet API (Anthropic)
- Fallback: Google Cloud Vision API

**Deployment**:
- Backend: Railway, Render, or AWS Lambda
- Frontend: Vercel or Netlify
- Database: Supabase or AWS RDS

### **Alternative: Rapid Prototype**

**Single-Stack Python**:
- Streamlit (all-in-one UI + backend)
- OpenAI API (GPT-4 Vision)
- SQLite (local database)
- Deploy: Streamlit Cloud

---

## 💰 Cost Estimates

### Development Time:
- MVP (basic functionality): 3-4 weeks
- Production-ready: 6-8 weeks
- With team: 4-6 weeks

### API Costs (per 1000 uploads):
- **OCR**:
  - Tesseract: Free
  - GPT-4 Vision: ~$50-100
  - Google Vision: ~$15

- **AI Processing**:
  - GPT-4: ~$0.03 per upload
  - Claude 3.5: ~$0.015 per upload

### Hosting:
- $20-50/month (small scale)
- $100-500/month (production)

---

## 🔐 Security & Privacy Considerations

1. **Data Handling**:
   - Don't store uploaded images permanently (GDPR/privacy)
   - Encrypt sensitive data at rest
   - Use temporary signed URLs for file access

2. **API Security**:
   - Rate limiting on upload endpoints
   - File size limits (max 10MB)
   - Virus scanning for uploads
   - API key management for AI services

3. **Compliance**:
   - Add disclaimer: "For informational purposes only"
   - Not a substitute for legal/regulatory review
   - Version control for CFR regulations

---

## 📊 Success Metrics

- **Accuracy**: >90% OCR text extraction
- **Compliance Detection**: >95% precision on checklist items
- **Processing Time**: <30 seconds per upload
- **User Satisfaction**: 4.5+ star rating

---

## 🎯 Next Steps

1. **Choose your approach**:
   - Quick prototype → Streamlit + GPT-4 Vision
   - Production app → FastAPI + React + Next.js

2. **Set up development environment**:
   - Create GitHub repo
   - Set up API keys (OpenAI/Anthropic/Google)
   - Initialize project structure

3. **Start with Phase 1**:
   - Build basic upload → OCR → display pipeline
   - Test with sample nutrition labels
   - Iterate on accuracy

**Would you like me to start implementing any specific part of this plan?**
