"""
Excel Import Module
Import nutrition data from Excel spec sheets
"""

import pandas as pd
import re
from io import BytesIO


def import_from_excel(uploaded_file):
    """
    Import nutrition data from Excel file

    Supports various common spec sheet formats:
    - Standard nutrition facts table format
    - FDA submission format
    - Custom internal formats

    Args:
        uploaded_file: Streamlit uploaded Excel file

    Returns:
        dict: Structured nutrition data in standard format
    """
    try:
        # Read Excel file
        df = pd.read_excel(uploaded_file, sheet_name=0, header=None)

        # Try to detect format and parse
        data = auto_detect_format(df)

        if not data:
            # Fallback: Try standard format
            data = parse_standard_format(df)

        return data

    except Exception as e:
        return {
            "error": "Failed to import Excel file",
            "details": str(e),
            "_metadata": {
                "source": "excel_import",
                "confidence": "low"
            }
        }


def auto_detect_format(df):
    """
    Auto-detect Excel format and route to appropriate parser

    Args:
        df: Pandas DataFrame

    Returns:
        dict: Parsed data or None if format not recognized
    """
    # Convert DataFrame to string for pattern matching
    df_str = df.astype(str).values.flatten()

    # Look for key patterns
    has_nutrition_facts = any('nutrition facts' in str(cell).lower() for cell in df_str)
    has_serving_size = any('serving size' in str(cell).lower() for cell in df_str)
    has_calories = any('calories' in str(cell).lower() for cell in df_str)

    if has_nutrition_facts and has_serving_size and has_calories:
        # Standard nutrition facts format
        return parse_standard_format(df)
    elif has_serving_size and has_calories:
        # Simplified format
        return parse_simplified_format(df)
    else:
        # Try key-value pair format
        return parse_key_value_format(df)


def parse_standard_format(df):
    """
    Parse standard nutrition facts table format

    Expected format:
    | Nutrition Facts     |        |
    | Serving Size        | 55g    |
    | Calories            | 120    |
    | Total Fat           | 5g     | 6%  |
    ...

    Args:
        df: Pandas DataFrame

    Returns:
        dict: Structured nutrition data
    """
    data = {
        "productName": None,
        "formatType": "single-column",
        "servingInfo": {},
        "calories": {},
        "nutrients": {},
        "ingredients": {},
        "allergens": {},
        "_metadata": {
            "source": "excel_import",
            "format": "standard",
            "confidence": "medium"
        }
    }

    # Helper function to find cell value
    def find_value(df, search_terms, column_offset=1):
        """Find value next to a label"""
        for idx, row in df.iterrows():
            for col in df.columns:
                cell = str(row[col]).lower()
                for term in search_terms:
                    if term in cell:
                        # Get value from next column
                        if col + column_offset < len(df.columns):
                            value = row[col + column_offset]
                            return value if pd.notna(value) else None
        return None

    # Extract product name
    data["productName"] = find_value(df, ["product name", "product:", "item name"])

    # Extract serving size
    serving_size_str = find_value(df, ["serving size", "serving per container"])
    if serving_size_str:
        serving_data = parse_serving_size(str(serving_size_str))
        data["servingInfo"]["servingSize"] = serving_data

    # Extract servings per container
    servings = find_value(df, ["servings per container", "servings:", "number of servings"])
    if servings:
        data["servingInfo"]["servingsPerContainer"] = parse_number(str(servings))

    # Extract calories
    calories = find_value(df, ["calories", "energy"])
    if calories:
        data["calories"]["perServing"] = parse_number(str(calories))

    # Extract nutrients
    nutrient_mapping = {
        "total fat": "totalFat",
        "fat": "totalFat",
        "saturated fat": "saturatedFat",
        "trans fat": "transFat",
        "cholesterol": "cholesterol",
        "sodium": "sodium",
        "total carbohydrate": "totalCarbohydrate",
        "carbohydrate": "totalCarbohydrate",
        "dietary fiber": "dietaryFiber",
        "fiber": "dietaryFiber",
        "total sugars": "totalSugars",
        "sugars": "totalSugars",
        "added sugars": "addedSugars",
        "protein": "protein",
        "vitamin d": "vitaminD",
        "calcium": "calcium",
        "iron": "iron",
        "potassium": "potassium"
    }

    for search_term, nutrient_key in nutrient_mapping.items():
        # Find nutrient value
        for idx, row in df.iterrows():
            for col in df.columns:
                cell = str(row[col]).lower().strip()

                # Exact match or close match
                if cell == search_term or search_term in cell:
                    # Get value from next column
                    value_col = col + 1
                    dv_col = col + 2

                    if value_col < len(df.columns):
                        value_str = str(row[value_col])
                        value, unit = parse_nutrient_value(value_str)

                        # Get %DV if available
                        daily_value = None
                        if dv_col < len(df.columns):
                            dv_str = str(row[dv_col])
                            daily_value = parse_percentage(dv_str)

                        data["nutrients"][nutrient_key] = {
                            "value": value,
                            "unit": unit,
                            "dailyValue": daily_value
                        }
                    break

    # Extract ingredients
    ingredients = find_value(df, ["ingredients:", "ingredients", "ingredient list"])
    if ingredients:
        data["ingredients"]["text"] = str(ingredients)
        data["ingredients"]["list"] = parse_ingredient_list(str(ingredients))

    # Extract allergens
    allergens = find_value(df, ["contains:", "allergens:", "allergen information"])
    if allergens:
        data["allergens"]["containsStatement"] = str(allergens)
        data["allergens"]["allergenList"] = parse_allergen_list(str(allergens))

    return data


def parse_simplified_format(df):
    """Parse simplified two-column format (Label | Value)"""
    data = {
        "servingInfo": {},
        "calories": {},
        "nutrients": {},
        "ingredients": {},
        "allergens": {},
        "_metadata": {
            "source": "excel_import",
            "format": "simplified",
            "confidence": "medium"
        }
    }

    # Assume first column is labels, second is values
    for idx, row in df.iterrows():
        if len(row) >= 2:
            label = str(row[0]).lower().strip()
            value = row[1]

            if pd.isna(value):
                continue

            # Match label to field
            if 'serving size' in label:
                data["servingInfo"]["servingSize"] = parse_serving_size(str(value))
            elif 'servings' in label and 'container' in label:
                data["servingInfo"]["servingsPerContainer"] = parse_number(str(value))
            elif 'calorie' in label:
                data["calories"]["perServing"] = parse_number(str(value))
            # Add more mappings as needed

    return data


def parse_key_value_format(df):
    """Parse generic key-value pair format"""
    # Similar to simplified but more flexible
    return parse_simplified_format(df)


# Helper Functions

def parse_serving_size(text):
    """
    Parse serving size from text

    Examples:
        "55g" -> {"value": 55, "unit": "g"}
        "240mL (1 cup)" -> {"value": 240, "unit": "mL", "householdMeasure": "1 cup"}
        "5 slices (55g)" -> {"value": 55, "unit": "g", "householdMeasure": "5 slices"}

    Args:
        text: Serving size text

    Returns:
        dict: Parsed serving size
    """
    result = {
        "value": None,
        "unit": None,
        "householdMeasure": None
    }

    # Extract number and unit
    # Match patterns like "55g", "240mL", "55 g", "240 mL"
    match = re.search(r'(\d+\.?\d*)\s*(g|ml|mg|mcg|oz|cup|tbsp|tsp)', text.lower())
    if match:
        result["value"] = float(match.group(1))
        result["unit"] = match.group(2)

    # Extract household measure from parentheses
    household_match = re.search(r'\(([^)]+)\)', text)
    if household_match:
        household = household_match.group(1)
        # If it doesn't contain a number with unit, it's likely the household measure
        if not re.search(r'\d+\s*(g|ml|mg)', household.lower()):
            result["householdMeasure"] = household
        else:
            # If no household measure found yet, check if there's text before parentheses
            before_paren = text.split('(')[0].strip()
            if before_paren and not re.search(r'^\d+\.?\d*\s*(g|ml)', before_paren.lower()):
                result["householdMeasure"] = before_paren

    return result


def parse_nutrient_value(text):
    """
    Parse nutrient value and unit from text

    Args:
        text: Nutrient value text (e.g., "5g", "450mg", "0.5")

    Returns:
        tuple: (value, unit)
    """
    text = str(text).strip()

    # Match number followed by optional unit
    match = re.search(r'(\d+\.?\d*)\s*(g|mg|mcg)?', text.lower())
    if match:
        value = float(match.group(1))
        unit = match.group(2) if match.group(2) else "g"
        return value, unit

    return None, None


def parse_percentage(text):
    """
    Parse percentage value from text

    Args:
        text: Percentage text (e.g., "6%", "6", "6.0%")

    Returns:
        int: Percentage value or None
    """
    text = str(text).strip()

    # Remove % sign and convert to int
    match = re.search(r'(\d+\.?\d*)\s*%?', text)
    if match:
        return int(float(match.group(1)))

    return None


def parse_number(text):
    """
    Parse numeric value from text

    Args:
        text: Numeric text

    Returns:
        float or str: Numeric value or original text
    """
    text = str(text).strip()

    # Try to extract number
    match = re.search(r'(\d+\.?\d*)', text)
    if match:
        num = float(match.group(1))
        # Return int if whole number
        return int(num) if num.is_integer() else num

    # If contains "about", return as-is
    if 'about' in text.lower():
        return text

    return text


def parse_ingredient_list(text):
    """
    Parse ingredient list into array

    Args:
        text: Ingredient list text

    Returns:
        list: Array of ingredients
    """
    # Split by comma
    ingredients = [ing.strip() for ing in text.split(',')]

    # Clean up
    ingredients = [ing for ing in ingredients if ing and ing.lower() != 'nan']

    return ingredients


def parse_allergen_list(text):
    """
    Parse allergen list from text

    Args:
        text: Allergen text

    Returns:
        list: Array of allergens
    """
    # Remove "Contains:" prefix if present
    text = re.sub(r'contains:?\s*', '', text, flags=re.IGNORECASE)

    # Split by comma or "and"
    allergens = re.split(r',|\sand\s', text)

    # Clean up
    allergens = [a.strip().title() for a in allergens if a.strip() and a.strip().lower() != 'nan']

    return allergens


def export_to_excel(data, comparison_results=None):
    """
    Export nutrition data and/or comparison results to Excel

    Args:
        data: Extracted nutrition data
        comparison_results: Optional comparison results

    Returns:
        bytes: Excel file as bytes
    """
    output = BytesIO()

    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # Sheet 1: Nutrition Data
        nutrition_df = create_nutrition_dataframe(data)
        nutrition_df.to_excel(writer, sheet_name='Nutrition Facts', index=False)

        # Sheet 2: Comparison (if provided)
        if comparison_results:
            comparison_df = create_comparison_dataframe(comparison_results)
            comparison_df.to_excel(writer, sheet_name='Comparison Results', index=False)

        # Sheet 3: Ingredients
        if 'ingredients' in data:
            ing_df = pd.DataFrame({
                'Ingredient': data['ingredients'].get('list', [])
            })
            ing_df.to_excel(writer, sheet_name='Ingredients', index=False)

    excel_bytes = output.getvalue()
    output.close()

    return excel_bytes


def create_nutrition_dataframe(data):
    """Create DataFrame from nutrition data"""
    rows = []

    # Serving info
    if 'servingInfo' in data:
        serving = data['servingInfo']
        if 'servingSize' in serving:
            ss = serving['servingSize']
            rows.append({
                'Category': 'Serving Information',
                'Nutrient': 'Serving Size',
                'Value': f"{ss.get('value', '')}{ss.get('unit', '')}",
                'Unit': ss.get('unit', ''),
                '% Daily Value': ''
            })

        if 'servingsPerContainer' in serving:
            rows.append({
                'Category': 'Serving Information',
                'Nutrient': 'Servings per Container',
                'Value': serving['servingsPerContainer'],
                'Unit': '',
                '% Daily Value': ''
            })

    # Calories
    if 'calories' in data:
        rows.append({
            'Category': 'Calories',
            'Nutrient': 'Calories',
            'Value': data['calories'].get('perServing', ''),
            'Unit': '',
            '% Daily Value': ''
        })

    # Nutrients
    if 'nutrients' in data:
        nutrient_names = {
            'totalFat': 'Total Fat',
            'saturatedFat': 'Saturated Fat',
            'transFat': 'Trans Fat',
            'cholesterol': 'Cholesterol',
            'sodium': 'Sodium',
            'totalCarbohydrate': 'Total Carbohydrate',
            'dietaryFiber': 'Dietary Fiber',
            'totalSugars': 'Total Sugars',
            'addedSugars': 'Added Sugars',
            'protein': 'Protein',
            'vitaminD': 'Vitamin D',
            'calcium': 'Calcium',
            'iron': 'Iron',
            'potassium': 'Potassium'
        }

        for key, name in nutrient_names.items():
            if key in data['nutrients']:
                nut = data['nutrients'][key]
                rows.append({
                    'Category': 'Nutrients',
                    'Nutrient': name,
                    'Value': nut.get('value', ''),
                    'Unit': nut.get('unit', ''),
                    '% Daily Value': f"{nut.get('dailyValue', '')}%" if nut.get('dailyValue') is not None else ''
                })

    return pd.DataFrame(rows)


def create_comparison_dataframe(comparison_results):
    """Create DataFrame from comparison results"""
    rows = []

    # Add all differences
    for diff in comparison_results.get('criticalMismatches', []):
        rows.append({
            'Severity': 'CRITICAL',
            'Field': diff.get('field', ''),
            'Spec': diff.get('spec', ''),
            'Packaging': diff.get('packaging', ''),
            'Difference': diff.get('difference', ''),
            'Message': diff.get('message', '')
        })

    for diff in comparison_results.get('minorDifferences', []):
        rows.append({
            'Severity': 'MINOR',
            'Field': diff.get('field', ''),
            'Spec': diff.get('spec', ''),
            'Packaging': diff.get('packaging', ''),
            'Difference': diff.get('difference', ''),
            'Message': diff.get('message', '')
        })

    return pd.DataFrame(rows)
