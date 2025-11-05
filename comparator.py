"""
Spec Sheet vs Packaging Label Comparator
Compare nutrition data between spec sheet and actual packaging
"""

from difflib import SequenceMatcher
import re


def compare_nutrition_data(spec_data, packaging_data, tolerance_settings=None):
    """
    Compare nutrition data from spec sheet vs packaging label

    Args:
        spec_data: Extracted data from spec sheet (source of truth)
        packaging_data: Extracted data from packaging label
        tolerance_settings: Dict of acceptable variance percentages

    Returns:
        dict: Comparison results with discrepancies
    """
    if tolerance_settings is None:
        tolerance_settings = get_default_tolerances()

    results = {
        "overallMatch": True,
        "matchScore": 0,  # Percentage of fields that match
        "criticalMismatches": [],
        "minorDifferences": [],
        "exactMatches": [],
        "summary": {
            "totalChecks": 0,
            "exactMatches": 0,
            "withinTolerance": 0,
            "outOfTolerance": 0
        }
    }

    # Compare serving information
    serving_comparison = compare_serving_info(
        spec_data.get("servingInfo", {}),
        packaging_data.get("servingInfo", {}),
        tolerance_settings
    )
    results["servingInfo"] = serving_comparison

    # Compare calories
    calories_comparison = compare_calories(
        spec_data.get("calories", {}),
        packaging_data.get("calories", {}),
        tolerance_settings
    )
    results["calories"] = calories_comparison

    # Compare nutrients
    nutrients_comparison = compare_nutrients(
        spec_data.get("nutrients", {}),
        packaging_data.get("nutrients", {}),
        tolerance_settings
    )
    results["nutrients"] = nutrients_comparison

    # Compare ingredients
    ingredients_comparison = compare_ingredients(
        spec_data.get("ingredients", {}),
        packaging_data.get("ingredients", {})
    )
    results["ingredients"] = ingredients_comparison

    # Compare allergens
    allergens_comparison = compare_allergens(
        spec_data.get("allergens", {}),
        packaging_data.get("allergens", {})
    )
    results["allergens"] = allergens_comparison

    # Aggregate results
    aggregate_comparison_results(results)

    return results


def get_default_tolerances():
    """
    Get default tolerance settings for nutrient comparisons

    Returns:
        dict: Tolerance percentages and absolute values
    """
    return {
        "servingSize": {
            "percentage": 2.0,  # ±2% allowed
            "absolute": 1.0     # or ±1g
        },
        "calories": {
            "percentage": 5.0,  # ±5% allowed
            "absolute": 5       # or ±5 calories
        },
        "nutrients": {
            # Most nutrients: ±5% or rounding variance
            "default": {
                "percentage": 5.0,
                "absolute": None  # Use FDA rounding rules
            },
            # Specific nutrient overrides
            "sodium": {
                "percentage": 5.0,
                "absolute": 10  # ±10mg (FDA rounding unit)
            },
            "totalFat": {
                "percentage": 5.0,
                "absolute": 0.5  # ±0.5g (FDA rounding unit)
            }
        },
        "ingredients": {
            "allowTypos": False,  # Require exact match
            "fuzzyThreshold": 95  # 95%+ similarity for warnings
        }
    }


def compare_serving_info(spec_serving, pkg_serving, tolerances):
    """Compare serving size information"""
    comparison = {
        "status": "MATCH",
        "differences": []
    }

    # Compare serving size value
    spec_size = spec_serving.get("servingSize", {}).get("value")
    pkg_size = pkg_serving.get("servingSize", {}).get("value")

    if spec_size and pkg_size:
        diff = abs(spec_size - pkg_size)
        tolerance_pct = tolerances["servingSize"]["percentage"]
        tolerance_abs = tolerances["servingSize"]["absolute"]

        allowed_diff = max(
            spec_size * (tolerance_pct / 100),
            tolerance_abs
        )

        if diff > allowed_diff:
            comparison["status"] = "MISMATCH"
            comparison["differences"].append({
                "field": "Serving Size",
                "spec": f"{spec_size}g",
                "packaging": f"{pkg_size}g",
                "difference": f"{diff:.1f}g",
                "percentDiff": f"{(diff/spec_size)*100:.1f}%",
                "severity": "CRITICAL",
                "message": f"Serving size differs by {diff:.1f}g (>{allowed_diff:.1f}g allowed)"
            })
        elif diff > 0:
            comparison["status"] = "MINOR_DIFF"
            comparison["differences"].append({
                "field": "Serving Size",
                "spec": f"{spec_size}g",
                "packaging": f"{pkg_size}g",
                "difference": f"{diff:.1f}g",
                "percentDiff": f"{(diff/spec_size)*100:.1f}%",
                "severity": "WARNING",
                "message": f"Minor difference: {diff:.1f}g (within tolerance)"
            })

    # Compare servings per container
    spec_servings = spec_serving.get("servingsPerContainer")
    pkg_servings = pkg_serving.get("servingsPerContainer")

    if str(spec_servings) != str(pkg_servings):
        comparison["differences"].append({
            "field": "Servings per Container",
            "spec": str(spec_servings),
            "packaging": str(pkg_servings),
            "severity": "WARNING",
            "message": "Servings per container differs"
        })

    # Compare household measure
    spec_household = spec_serving.get("servingSize", {}).get("householdMeasure", "")
    pkg_household = pkg_serving.get("servingSize", {}).get("householdMeasure", "")

    if spec_household and pkg_household:
        similarity = calculate_string_similarity(spec_household, pkg_household)
        if similarity < 100:
            comparison["differences"].append({
                "field": "Household Measure",
                "spec": spec_household,
                "packaging": pkg_household,
                "similarity": f"{similarity}%",
                "severity": "WARNING" if similarity > 90 else "CRITICAL",
                "message": f"Household measure text differs (similarity: {similarity}%)"
            })

    return comparison


def compare_calories(spec_cal, pkg_cal, tolerances):
    """Compare calorie values"""
    comparison = {
        "status": "MATCH",
        "differences": []
    }

    spec_value = spec_cal.get("perServing")
    pkg_value = pkg_cal.get("perServing")

    if spec_value and pkg_value:
        diff = abs(spec_value - pkg_value)
        tolerance_pct = tolerances["calories"]["percentage"]
        tolerance_abs = tolerances["calories"]["absolute"]

        allowed_diff = max(
            spec_value * (tolerance_pct / 100),
            tolerance_abs
        )

        if diff > allowed_diff:
            comparison["status"] = "MISMATCH"
            comparison["differences"].append({
                "field": "Calories",
                "spec": spec_value,
                "packaging": pkg_value,
                "difference": diff,
                "percentDiff": f"{(diff/spec_value)*100:.1f}%",
                "severity": "CRITICAL",
                "message": f"Calories differ by {diff} (>{allowed_diff} allowed)"
            })
        elif diff > 0:
            comparison["status"] = "MINOR_DIFF"
            comparison["differences"].append({
                "field": "Calories",
                "spec": spec_value,
                "packaging": pkg_value,
                "difference": diff,
                "percentDiff": f"{(diff/spec_value)*100:.1f}%",
                "severity": "WARNING",
                "message": f"Minor difference: {diff} calories (within tolerance)"
            })

    return comparison


def compare_nutrients(spec_nutrients, pkg_nutrients, tolerances):
    """Compare all nutrient values"""
    comparison = {
        "status": "MATCH",
        "differences": []
    }

    nutrient_names = {
        "totalFat": "Total Fat",
        "saturatedFat": "Saturated Fat",
        "transFat": "Trans Fat",
        "cholesterol": "Cholesterol",
        "sodium": "Sodium",
        "totalCarbohydrate": "Total Carbohydrate",
        "dietaryFiber": "Dietary Fiber",
        "totalSugars": "Total Sugars",
        "addedSugars": "Added Sugars",
        "protein": "Protein",
        "vitaminD": "Vitamin D",
        "calcium": "Calcium",
        "iron": "Iron",
        "potassium": "Potassium"
    }

    for nutrient_key, nutrient_name in nutrient_names.items():
        spec_nutrient = spec_nutrients.get(nutrient_key, {})
        pkg_nutrient = pkg_nutrients.get(nutrient_key, {})

        spec_value = spec_nutrient.get("value")
        pkg_value = pkg_nutrient.get("value")

        if spec_value is None or pkg_value is None:
            continue

        # Get tolerance for this nutrient
        nutrient_tolerance = tolerances["nutrients"].get(
            nutrient_key,
            tolerances["nutrients"]["default"]
        )

        diff = abs(spec_value - pkg_value)

        # Calculate allowed difference
        tolerance_pct = nutrient_tolerance["percentage"]
        tolerance_abs = nutrient_tolerance.get("absolute")

        if tolerance_abs:
            allowed_diff = max(
                spec_value * (tolerance_pct / 100),
                tolerance_abs
            )
        else:
            allowed_diff = spec_value * (tolerance_pct / 100)

        if diff > allowed_diff:
            comparison["status"] = "MISMATCH"
            unit = spec_nutrient.get("unit", "")

            comparison["differences"].append({
                "field": nutrient_name,
                "spec": f"{spec_value}{unit}",
                "packaging": f"{pkg_value}{unit}",
                "difference": f"{diff}{unit}",
                "percentDiff": f"{(diff/spec_value)*100:.1f}%" if spec_value > 0 else "N/A",
                "severity": "CRITICAL",
                "message": f"{nutrient_name} differs by {diff}{unit}"
            })
        elif diff > 0:
            comparison["status"] = "MINOR_DIFF" if comparison["status"] == "MATCH" else comparison["status"]
            unit = spec_nutrient.get("unit", "")

            comparison["differences"].append({
                "field": nutrient_name,
                "spec": f"{spec_value}{unit}",
                "packaging": f"{pkg_value}{unit}",
                "difference": f"{diff}{unit}",
                "percentDiff": f"{(diff/spec_value)*100:.1f}%" if spec_value > 0 else "N/A",
                "severity": "INFO",
                "message": f"Minor difference (within tolerance)"
            })

        # Compare %DV if present
        spec_dv = spec_nutrient.get("dailyValue")
        pkg_dv = pkg_nutrient.get("dailyValue")

        if spec_dv is not None and pkg_dv is not None and spec_dv != pkg_dv:
            comparison["differences"].append({
                "field": f"{nutrient_name} %DV",
                "spec": f"{spec_dv}%",
                "packaging": f"{pkg_dv}%",
                "severity": "WARNING",
                "message": f"%DV differs: {spec_dv}% vs {pkg_dv}%"
            })

    return comparison


def compare_ingredients(spec_ingredients, pkg_ingredients):
    """Compare ingredient lists"""
    comparison = {
        "status": "MATCH",
        "differences": []
    }

    spec_text = spec_ingredients.get("text", "").strip()
    pkg_text = pkg_ingredients.get("text", "").strip()

    # Normalize for comparison (lowercase, remove extra spaces)
    spec_normalized = normalize_text(spec_text)
    pkg_normalized = normalize_text(pkg_text)

    if spec_normalized != pkg_normalized:
        similarity = calculate_string_similarity(spec_normalized, pkg_normalized)

        if similarity < 95:
            comparison["status"] = "MISMATCH"
            severity = "CRITICAL"
        else:
            comparison["status"] = "MINOR_DIFF"
            severity = "WARNING"

        # Find specific differences
        spec_list = spec_ingredients.get("list", [])
        pkg_list = pkg_ingredients.get("list", [])

        missing_in_pkg = [ing for ing in spec_list if ing not in pkg_list]
        extra_in_pkg = [ing for ing in pkg_list if ing not in spec_list]

        message_parts = []
        if missing_in_pkg:
            message_parts.append(f"Missing: {', '.join(missing_in_pkg[:3])}")
        if extra_in_pkg:
            message_parts.append(f"Extra: {', '.join(extra_in_pkg[:3])}")

        comparison["differences"].append({
            "field": "Ingredient List",
            "spec": spec_text[:200] + "..." if len(spec_text) > 200 else spec_text,
            "packaging": pkg_text[:200] + "..." if len(pkg_text) > 200 else pkg_text,
            "similarity": f"{similarity}%",
            "severity": severity,
            "message": "; ".join(message_parts) if message_parts else f"Text differs (similarity: {similarity}%)",
            "missingInPackaging": missing_in_pkg,
            "extraInPackaging": extra_in_pkg
        })

    return comparison


def compare_allergens(spec_allergens, pkg_allergens):
    """Compare allergen declarations"""
    comparison = {
        "status": "MATCH",
        "differences": []
    }

    spec_list = set(spec_allergens.get("allergenList", []))
    pkg_list = set(pkg_allergens.get("allergenList", []))

    # Normalize (lowercase for comparison)
    spec_list = {a.lower() for a in spec_list}
    pkg_list = {a.lower() for a in pkg_list}

    missing_in_pkg = spec_list - pkg_list
    extra_in_pkg = pkg_list - spec_list

    if missing_in_pkg or extra_in_pkg:
        comparison["status"] = "MISMATCH"

        if missing_in_pkg:
            comparison["differences"].append({
                "field": "Allergens - Missing in Packaging",
                "spec": ", ".join(sorted(spec_list)),
                "packaging": ", ".join(sorted(pkg_list)),
                "severity": "CRITICAL",
                "message": f"Missing allergens in packaging: {', '.join(sorted(missing_in_pkg))}",
                "missingAllergens": list(missing_in_pkg)
            })

        if extra_in_pkg:
            comparison["differences"].append({
                "field": "Allergens - Extra in Packaging",
                "spec": ", ".join(sorted(spec_list)),
                "packaging": ", ".join(sorted(pkg_list)),
                "severity": "WARNING",
                "message": f"Extra allergens in packaging: {', '.join(sorted(extra_in_pkg))}",
                "extraAllergens": list(extra_in_pkg)
            })

    # Compare Contains statement text
    spec_contains = spec_allergens.get("containsStatement", "")
    pkg_contains = pkg_allergens.get("containsStatement", "")

    if spec_contains and pkg_contains:
        similarity = calculate_string_similarity(
            normalize_text(spec_contains),
            normalize_text(pkg_contains)
        )

        if similarity < 100:
            comparison["differences"].append({
                "field": "Contains Statement",
                "spec": spec_contains,
                "packaging": pkg_contains,
                "similarity": f"{similarity}%",
                "severity": "WARNING" if similarity > 95 else "CRITICAL",
                "message": f"Contains statement text differs (similarity: {similarity}%)"
            })

    return comparison


def aggregate_comparison_results(results):
    """
    Aggregate all comparison results into summary statistics

    Args:
        results: Results dict (modified in place)
    """
    total_checks = 0
    exact_matches = 0
    within_tolerance = 0
    out_of_tolerance = 0

    critical_mismatches = []
    minor_differences = []
    exact_match_fields = []

    # Process each comparison section
    for section_key in ["servingInfo", "calories", "nutrients", "ingredients", "allergens"]:
        section = results.get(section_key, {})
        status = section.get("status", "MATCH")
        differences = section.get("differences", [])

        if status == "MATCH" and not differences:
            exact_match_fields.append(section_key)
            exact_matches += 1
        elif status == "MINOR_DIFF":
            for diff in differences:
                if diff.get("severity") in ["WARNING", "INFO"]:
                    minor_differences.append(diff)
                    within_tolerance += 1
                else:
                    critical_mismatches.append(diff)
                    out_of_tolerance += 1
        elif status == "MISMATCH":
            for diff in differences:
                if diff.get("severity") == "CRITICAL":
                    critical_mismatches.append(diff)
                    out_of_tolerance += 1
                else:
                    minor_differences.append(diff)
                    within_tolerance += 1

        total_checks += 1

    # Update summary
    results["summary"]["totalChecks"] = total_checks
    results["summary"]["exactMatches"] = exact_matches
    results["summary"]["withinTolerance"] = within_tolerance
    results["summary"]["outOfTolerance"] = out_of_tolerance

    # Set overall match status
    if out_of_tolerance > 0:
        results["overallMatch"] = False
        results["matchScore"] = int(((exact_matches + within_tolerance) / total_checks) * 100) if total_checks > 0 else 0
    else:
        results["overallMatch"] = True
        results["matchScore"] = 100

    # Store aggregated lists
    results["criticalMismatches"] = critical_mismatches
    results["minorDifferences"] = minor_differences
    results["exactMatches"] = exact_match_fields


# Helper Functions

def calculate_string_similarity(str1, str2):
    """
    Calculate similarity between two strings (0-100%)

    Args:
        str1: First string
        str2: Second string

    Returns:
        int: Similarity percentage (0-100)
    """
    if not str1 or not str2:
        return 0 if str1 != str2 else 100

    return int(SequenceMatcher(None, str1, str2).ratio() * 100)


def normalize_text(text):
    """
    Normalize text for comparison (lowercase, remove extra whitespace)

    Args:
        text: Input text

    Returns:
        str: Normalized text
    """
    if not text:
        return ""

    # Lowercase
    text = text.lower()

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)

    # Strip
    text = text.strip()

    return text
