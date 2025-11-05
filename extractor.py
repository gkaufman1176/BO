"""
Nutrition Label Data Extraction using GPT-4 Vision
"""

import base64
import json
import os
from io import BytesIO
from PIL import Image
from openai import OpenAI

def extract_nutrition_data(uploaded_file, product_type):
    """
    Extract structured nutrition data from an uploaded label image using GPT-4 Vision

    Args:
        uploaded_file: Streamlit uploaded file object
        product_type: Type of product (for RACC validation)

    Returns:
        dict: Structured nutrition data
    """
    # Initialize OpenAI client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Convert uploaded file to base64
    image_data = uploaded_file.getvalue()

    # Handle PDF files - convert first page to image
    if uploaded_file.type == "application/pdf":
        from pdf2image import convert_from_bytes
        images = convert_from_bytes(image_data, first_page=1, last_page=1)
        img = images[0]
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        image_data = buffered.getvalue()

    # Encode to base64
    base64_image = base64.b64encode(image_data).decode('utf-8')

    # Create the prompt for GPT-4 Vision
    prompt = """You are an FDA compliance expert analyzing a nutrition label for a plant-based food product.

Extract ALL information from this nutrition label in JSON format. Be extremely precise with numbers and text.

Return a JSON object with this EXACT structure:

{
  "productType": "plant-based-meat or plant-based-dairy",
  "productName": "exact product name from label",
  "formatType": "single-column or dual-column",
  "servingInfo": {
    "servingSize": {
      "value": number (in grams or mL),
      "unit": "g or mL",
      "householdMeasure": "exact text like 'about 5 slices'"
    },
    "servingsPerContainer": number or "about X"
  },
  "calories": {
    "perServing": number,
    "perContainer": number (if dual-column, else null)
  },
  "nutrients": {
    "totalFat": {"value": number, "unit": "g", "dailyValue": number},
    "saturatedFat": {"value": number, "unit": "g", "dailyValue": number},
    "transFat": {"value": number, "unit": "g"},
    "cholesterol": {"value": number, "unit": "mg", "dailyValue": number},
    "sodium": {"value": number, "unit": "mg", "dailyValue": number},
    "totalCarbohydrate": {"value": number, "unit": "g", "dailyValue": number},
    "dietaryFiber": {"value": number, "unit": "g", "dailyValue": number},
    "totalSugars": {"value": number, "unit": "g"},
    "addedSugars": {"value": number, "unit": "g", "dailyValue": number},
    "protein": {"value": number, "unit": "g"},
    "vitaminD": {"value": number, "unit": "mcg", "dailyValue": number},
    "calcium": {"value": number, "unit": "mg", "dailyValue": number},
    "iron": {"value": number, "unit": "mg", "dailyValue": number},
    "potassium": {"value": number, "unit": "mg", "dailyValue": number}
  },
  "nutrientOrder": ["list nutrients in order they appear"],
  "ingredients": {
    "text": "full ingredient list text",
    "list": ["array", "of", "individual", "ingredients"],
    "hasBoldLabel": true/false
  },
  "allergens": {
    "containsStatement": "exact 'Contains:' text if present",
    "allergenList": ["array of allergens mentioned"]
  },
  "footnote": {
    "present": true/false,
    "text": "exact footnote text if present"
  },
  "otherElements": {
    "netWeight": "text like '5 oz (142g)'",
    "manufacturer": "company name and address",
    "storageInstructions": "text if present"
  }
}

IMPORTANT RULES:
- Extract EXACT numbers - do not round or modify
- If a value is missing or unclear, use null
- For "about" values, include the word "about" in the string
- Capture ALL allergens mentioned
- Note if dual-column format (shows both per serving AND per container)
- Extract nutrients in the order they appear on the label
- Include footnote text verbatim if present
- For trans fat, note exact value (usually 0g or 0.5g)

Return ONLY valid JSON, no other text."""

    try:
        # Call GPT-4 Vision API
        response = client.chat.completions.create(
            model="gpt-4o",  # Updated model name
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                                "detail": "high"
                            }
                        }
                    ]
                }
            ],
            max_tokens=2000,
            temperature=0.1  # Low temperature for accuracy
        )

        # Parse the response
        response_text = response.choices[0].message.content

        # Clean up response if it has markdown code blocks
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]

        # Parse JSON
        extracted_data = json.loads(response_text.strip())

        # Add metadata
        extracted_data["_metadata"] = {
            "productType": product_type,
            "extractionModel": "gpt-4o",
            "confidence": "high"  # Could be calculated based on response
        }

        return extracted_data

    except json.JSONDecodeError as e:
        # If JSON parsing fails, return error structure
        return {
            "error": "Failed to parse GPT-4 response",
            "details": str(e),
            "raw_response": response_text[:500],
            "_metadata": {
                "productType": product_type,
                "extractionModel": "gpt-4o",
                "confidence": "low"
            }
        }

    except Exception as e:
        # Handle other errors
        return {
            "error": "Extraction failed",
            "details": str(e),
            "_metadata": {
                "productType": product_type,
                "extractionModel": "gpt-4o",
                "confidence": "low"
            }
        }

def validate_extracted_data(data):
    """
    Basic validation of extracted data structure

    Args:
        data: Extracted nutrition data dict

    Returns:
        list: Validation errors
    """
    errors = []

    if "error" in data:
        errors.append(f"Extraction error: {data.get('details', 'Unknown error')}")
        return errors

    # Check required fields
    required_fields = ["servingInfo", "calories", "nutrients"]
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")

    # Check serving info
    if "servingInfo" in data:
        serving = data["servingInfo"]
        if "servingSize" not in serving or "servingsPerContainer" not in serving:
            errors.append("Incomplete serving information")

    # Check nutrients
    if "nutrients" in data:
        required_nutrients = [
            "totalFat", "saturatedFat", "transFat", "cholesterol",
            "sodium", "totalCarbohydrate", "protein"
        ]
        for nutrient in required_nutrients:
            if nutrient not in data["nutrients"]:
                errors.append(f"Missing required nutrient: {nutrient}")

    return errors
