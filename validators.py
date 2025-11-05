"""
FDA Compliance Validators
Functions to check nutrition label compliance against FDA regulations
"""

def run_compliance_checks(extracted_data, checklist_config):
    """
    Run all compliance checks from the checklist config

    Args:
        extracted_data: Dictionary of extracted nutrition data
        checklist_config: Checklist configuration from JSON

    Returns:
        dict: Compliance results with status for each check
    """
    results = {
        "overallScore": 0,
        "passed": 0,
        "failed": 0,
        "warnings": 0,
        "manual": 0,
        "checks": []
    }

    # Get validator functions
    validators = get_validators()

    # Iterate through each category
    for category in checklist_config["categories"]:
        category_name = category["name"]
        cfr_ref = category.get("cfr_reference", "N/A")

        # Check each requirement in the category
        for check in category["checks"]:
            validator_name = check.get("validator")
            requirement = check["requirement"]
            severity = check.get("severity", "medium")

            # Get the validator function
            validator_func = validators.get(validator_name)

            if validator_func:
                # Run the validator
                try:
                    result = validator_func(extracted_data, check, category)

                    # Build check result
                    check_result = {
                        "category": category_name,
                        "requirement": requirement,
                        "status": result.get("status", "MANUAL"),
                        "details": result.get("details", ""),
                        "severity": severity,
                        "cfr_reference": cfr_ref
                    }

                    results["checks"].append(check_result)

                    # Update counters
                    status = check_result["status"]
                    if status == "PASS":
                        results["passed"] += 1
                    elif status == "FAIL":
                        results["failed"] += 1
                    elif status == "WARNING":
                        results["warnings"] += 1
                    else:
                        results["manual"] += 1

                except Exception as e:
                    # Handle validator errors
                    results["checks"].append({
                        "category": category_name,
                        "requirement": requirement,
                        "status": "MANUAL",
                        "details": f"Validator error: {str(e)}",
                        "severity": severity,
                        "cfr_reference": cfr_ref
                    })
                    results["manual"] += 1
            else:
                # Validator not implemented
                results["checks"].append({
                    "category": category_name,
                    "requirement": requirement,
                    "status": "MANUAL",
                    "details": "Automated check not available - requires manual review",
                    "severity": severity,
                    "cfr_reference": cfr_ref
                })
                results["manual"] += 1

    # Calculate overall score
    total = results["passed"] + results["failed"] + results["warnings"]
    if total > 0:
        results["overallScore"] = int((results["passed"] / total) * 100)

    return results


def get_validators():
    """
    Return dictionary of validator functions

    Returns:
        dict: Mapping of validator names to functions
    """
    return {
        # Format Type Validators
        "check_format_layout": check_format_layout,
        "check_dual_column_requirement": check_dual_column_requirement,
        "check_dual_column_values": check_dual_column_values,
        "check_column_labels": check_column_labels,

        # Serving Size Validators
        "check_racc_compliance": check_racc_compliance,
        "check_metric_units": check_metric_units,
        "check_servings_declared": check_servings_declared,
        "check_household_measure": check_household_measure,
        "check_serving_format": check_serving_format,

        # Calories Validators
        "check_calories_formatting": check_calories_formatting,
        "check_calories_value": check_calories_value,
        "check_calories_dual_column": check_calories_dual_column,

        # Nutrient Validators
        "check_nutrient_order": check_nutrient_order,
        "check_nutrient_formatting": check_nutrient_formatting,
        "check_nutrient_units": check_nutrient_units,

        # Daily Value Validators
        "check_dv_declared": check_dv_declared,
        "check_dv_reference": check_dv_reference,
        "check_trans_fat_no_dv": check_trans_fat_no_dv,
        "check_added_sugars_dv": check_added_sugars_dv,
        "check_zero_nutrients_dv": check_zero_nutrients_dv,

        # Footnote Validators
        "check_footnote_present": check_footnote_present,
        "check_footnote_formatting": check_footnote_formatting,

        # Ingredient Validators
        "check_ingredients_label": check_ingredients_label,
        "check_descending_order": check_descending_order,
        "check_sub_ingredients": check_sub_ingredients,
        "check_common_names": check_common_names,

        # Allergen Validators
        "check_contains_statement": check_contains_statement,
        "check_top_9_coverage": check_top_9_coverage,
        "check_allergen_prominence": check_allergen_prominence,

        # Rounding Validators
        "check_fat_rounding": check_fat_rounding,
        "check_trans_fat_rounding": check_trans_fat_rounding,
        "check_sodium_rounding": check_sodium_rounding,
        "check_sugar_rounding": check_sugar_rounding,
        "check_protein_rounding": check_protein_rounding,
        "check_vitamin_mineral_rounding": check_vitamin_mineral_rounding,

        # Other Elements Validators
        "check_net_weight": check_net_weight,
        "check_manufacturer_info": check_manufacturer_info,
        "check_safe_handling": check_safe_handling,
        "check_product_identity": check_product_identity,
    }


# ============================================================================
# VALIDATOR FUNCTIONS
# ============================================================================

# --- Format Type Validators ---

def check_format_layout(data, check, category):
    """Check if label uses correct format (single vs dual column)"""
    format_type = data.get("formatType", "").lower()

    if format_type in ["single-column", "dual-column"]:
        return {
            "status": "PASS",
            "details": f"Format type: {format_type}"
        }
    else:
        return {
            "status": "MANUAL",
            "details": "Could not determine format type - manual review needed"
        }


def check_dual_column_requirement(data, check, category):
    """Check if dual-column is required based on servings per container"""
    serving_info = data.get("servingInfo", {})
    servings = serving_info.get("servingsPerContainer")
    format_type = data.get("formatType", "").lower()

    # Extract numeric value from servings
    if isinstance(servings, str):
        servings = servings.replace("about", "").strip()
        try:
            servings = float(servings)
        except:
            return {
                "status": "MANUAL",
                "details": "Could not parse servings per container value"
            }

    # Dual column typically required for 1.5-4 servings (when package could be eaten at once)
    if servings and 1.5 <= servings <= 4:
        if "dual" in format_type:
            return {
                "status": "PASS",
                "details": f"Dual-column format correctly used ({servings} servings per container)"
            }
        else:
            return {
                "status": "WARNING",
                "details": f"Dual-column may be required ({servings} servings) - verify if package could be consumed at once"
            }
    else:
        return {
            "status": "PASS",
            "details": f"Single-column appropriate ({servings} servings per container)"
        }


def check_dual_column_values(data, check, category):
    """Check if both per-serving and per-container values declared (dual-column only)"""
    format_type = data.get("formatType", "").lower()

    if "dual" not in format_type:
        return {"status": "PASS", "details": "Not applicable (single-column format)"}

    calories = data.get("calories", {})
    if calories.get("perServing") and calories.get("perContainer"):
        return {
            "status": "PASS",
            "details": "Both per-serving and per-container values declared"
        }
    else:
        return {
            "status": "FAIL",
            "details": "Dual-column format requires both per-serving and per-container values"
        }


def check_column_labels(data, check, category):
    """Check if columns are clearly labeled"""
    return {
        "status": "MANUAL",
        "details": "Visual formatting check - verify column labels manually"
    }


# --- Serving Size Validators ---

def check_racc_compliance(data, check, category):
    """Check if serving size matches RACC"""
    racc_table = check.get("racc_table", {})
    product_type = data.get("_metadata", {}).get("productType")

    serving_info = data.get("servingInfo", {})
    serving_size = serving_info.get("servingSize", {}).get("value")

    if not product_type or not serving_size:
        return {
            "status": "MANUAL",
            "details": "Missing product type or serving size data"
        }

    racc = racc_table.get(product_type)
    if not racc:
        return {
            "status": "MANUAL",
            "details": f"RACC not defined for product type: {product_type}"
        }

    # Allow 10% variance
    variance = abs(serving_size - racc)
    allowed_variance = racc * 0.1

    if variance <= allowed_variance:
        return {
            "status": "PASS",
            "details": f"Serving size {serving_size}g matches RACC {racc}g (within 10%)"
        }
    else:
        return {
            "status": "FAIL",
            "details": f"Serving size {serving_size}g differs from RACC {racc}g by {variance}g (>{allowed_variance}g allowed)"
        }


def check_metric_units(data, check, category):
    """Check if serving size includes metric units"""
    serving_info = data.get("servingInfo", {})
    unit = serving_info.get("servingSize", {}).get("unit", "").lower()

    if unit in ["g", "ml"]:
        return {
            "status": "PASS",
            "details": f"Metric unit declared: {unit}"
        }
    else:
        return {
            "status": "FAIL",
            "details": f"Missing or invalid metric unit (found: {unit})"
        }


def check_servings_declared(data, check, category):
    """Check if servings per container is declared"""
    serving_info = data.get("servingInfo", {})
    servings = serving_info.get("servingsPerContainer")

    if servings:
        return {
            "status": "PASS",
            "details": f"Servings per container: {servings}"
        }
    else:
        return {
            "status": "FAIL",
            "details": "Servings per container not declared"
        }


def check_household_measure(data, check, category):
    """Check if household measure is present"""
    serving_info = data.get("servingInfo", {})
    household = serving_info.get("servingSize", {}).get("householdMeasure")

    if household:
        return {
            "status": "PASS",
            "details": f"Household measure: {household}"
        }
    else:
        return {
            "status": "WARNING",
            "details": "Household measure not found - should be present (e.g., 'about 5 slices')"
        }


def check_serving_format(data, check, category):
    """Check serving size format"""
    return {
        "status": "MANUAL",
        "details": "Visual formatting check - verify format manually"
    }


# --- Calories Validators ---

def check_calories_formatting(data, check, category):
    """Check if calories is bold and larger"""
    return {
        "status": "MANUAL",
        "details": "Visual formatting check - verify 'Calories' is bold and larger font"
    }


def check_calories_value(data, check, category):
    """Check if calorie value is present"""
    calories = data.get("calories", {}).get("perServing")

    if calories and isinstance(calories, (int, float)):
        return {
            "status": "PASS",
            "details": f"Calories per serving: {calories}"
        }
    else:
        return {
            "status": "FAIL",
            "details": "Calories per serving not found or invalid"
        }


def check_calories_dual_column(data, check, category):
    """Check per-container calories in dual-column"""
    format_type = data.get("formatType", "").lower()

    if "dual" not in format_type:
        return {"status": "PASS", "details": "Not applicable (single-column)"}

    per_container = data.get("calories", {}).get("perContainer")
    if per_container:
        return {
            "status": "PASS",
            "details": f"Per-container calories: {per_container}"
        }
    else:
        return {
            "status": "FAIL",
            "details": "Per-container calories missing in dual-column format"
        }


# --- Nutrient Validators ---

def check_nutrient_order(data, check, category):
    """Check if nutrients appear in correct order"""
    required_order = category.get("required_order", [])
    actual_order = data.get("nutrientOrder", [])

    if not actual_order:
        return {
            "status": "MANUAL",
            "details": "Nutrient order not extracted - manual review needed"
        }

    # Check if nutrients appear in correct order
    mismatches = []
    for i, expected in enumerate(required_order):
        if i < len(actual_order):
            if expected.lower() not in actual_order[i].lower():
                mismatches.append(f"Position {i+1}: expected '{expected}', found '{actual_order[i]}'")

    if not mismatches:
        return {
            "status": "PASS",
            "details": "Nutrients in correct FDA-required order"
        }
    else:
        return {
            "status": "FAIL",
            "details": "Nutrient order violations: " + "; ".join(mismatches[:3])
        }


def check_nutrient_formatting(data, check, category):
    """Check nutrient formatting (bold, indentation)"""
    return {
        "status": "MANUAL",
        "details": "Visual formatting check - verify bold for main nutrients, indented for sub-nutrients"
    }


def check_nutrient_units(data, check, category):
    """Check if nutrients use correct units"""
    nutrients = data.get("nutrients", {})
    errors = []

    unit_requirements = {
        "totalFat": "g",
        "saturatedFat": "g",
        "transFat": "g",
        "cholesterol": "mg",
        "sodium": "mg",
        "totalCarbohydrate": "g",
        "dietaryFiber": "g",
        "totalSugars": "g",
        "addedSugars": "g",
        "protein": "g",
        "vitaminD": "mcg",
        "calcium": "mg",
        "iron": "mg",
        "potassium": "mg"
    }

    for nutrient, expected_unit in unit_requirements.items():
        if nutrient in nutrients:
            actual_unit = nutrients[nutrient].get("unit", "").lower()
            if actual_unit != expected_unit.lower():
                errors.append(f"{nutrient}: expected {expected_unit}, found {actual_unit}")

    if not errors:
        return {
            "status": "PASS",
            "details": "All nutrient units correct"
        }
    else:
        return {
            "status": "FAIL",
            "details": "Unit errors: " + "; ".join(errors[:3])
        }


# --- Daily Value Validators ---

def check_dv_declared(data, check, category):
    """Check if %DV is declared for required nutrients"""
    nutrients = data.get("nutrients", {})

    required_dv = [
        "totalFat", "saturatedFat", "cholesterol", "sodium",
        "totalCarbohydrate", "dietaryFiber", "addedSugars",
        "vitaminD", "calcium", "iron", "potassium"
    ]

    missing_dv = []
    for nutrient in required_dv:
        if nutrient in nutrients:
            if "dailyValue" not in nutrients[nutrient] or nutrients[nutrient]["dailyValue"] is None:
                missing_dv.append(nutrient)

    if not missing_dv:
        return {
            "status": "PASS",
            "details": "All required %DV values declared"
        }
    else:
        return {
            "status": "FAIL",
            "details": f"Missing %DV for: {', '.join(missing_dv[:5])}"
        }


def check_dv_reference(data, check, category):
    """Check if %DV uses 2016 FDA reference values"""
    return {
        "status": "MANUAL",
        "details": "Verify %DV calculations use 2016 FDA reference values manually"
    }


def check_trans_fat_no_dv(data, check, category):
    """Check that trans fat has no %DV"""
    nutrients = data.get("nutrients", {})
    trans_fat = nutrients.get("transFat", {})

    if "dailyValue" in trans_fat and trans_fat["dailyValue"] is not None:
        return {
            "status": "FAIL",
            "details": "Trans fat should NOT have a %DV value"
        }
    else:
        return {
            "status": "PASS",
            "details": "Trans fat correctly has no %DV"
        }


def check_added_sugars_dv(data, check, category):
    """Check that added sugars has %DV"""
    nutrients = data.get("nutrients", {})
    added_sugars = nutrients.get("addedSugars", {})

    if "dailyValue" in added_sugars and added_sugars["dailyValue"] is not None:
        return {
            "status": "PASS",
            "details": f"Added sugars %DV: {added_sugars['dailyValue']}%"
        }
    else:
        return {
            "status": "FAIL",
            "details": "Added sugars must have %DV declared"
        }


def check_zero_nutrients_dv(data, check, category):
    """Check that 0g nutrients still show 0% DV if required"""
    return {
        "status": "MANUAL",
        "details": "Verify 0g nutrients show 0% DV where required"
    }


# --- Footnote Validators ---

def check_footnote_present(data, check, category):
    """Check if required footnote is present"""
    footnote = data.get("footnote", {})
    expected_text = check.get("expected_text", "")

    if footnote.get("present"):
        footnote_text = footnote.get("text", "").lower()
        # Check for key phrases
        if "daily value" in footnote_text and "2,000 calories" in footnote_text:
            return {
                "status": "PASS",
                "details": "Required footnote present"
            }
        else:
            return {
                "status": "WARNING",
                "details": "Footnote present but may not match exact required text"
            }
    else:
        return {
            "status": "FAIL",
            "details": "Required footnote missing"
        }


def check_footnote_formatting(data, check, category):
    """Check footnote formatting"""
    return {
        "status": "MANUAL",
        "details": "Visual formatting check - verify footnote is italicized or smaller font"
    }


# --- Ingredient Validators ---

def check_ingredients_label(data, check, category):
    """Check if ingredients list starts with 'Ingredients:' in bold"""
    ingredients = data.get("ingredients", {})

    if ingredients.get("hasBoldLabel"):
        return {
            "status": "PASS",
            "details": "Ingredients label present and bold"
        }
    else:
        return {
            "status": "MANUAL",
            "details": "Could not verify 'Ingredients:' label formatting - check manually"
        }


def check_descending_order(data, check, category):
    """Check if ingredients are in descending order"""
    return {
        "status": "MANUAL",
        "details": "Ingredient order requires manual verification of weight/predominance"
    }


def check_sub_ingredients(data, check, category):
    """Check if sub-ingredients are in parentheses"""
    ingredients = data.get("ingredients", {})
    text = ingredients.get("text", "")

    if "(" in text and ")" in text:
        return {
            "status": "PASS",
            "details": "Sub-ingredients appear to use parentheses"
        }
    else:
        return {
            "status": "MANUAL",
            "details": "Verify sub-ingredient formatting manually"
        }


def check_common_names(data, check, category):
    """Check if ingredients use common names"""
    return {
        "status": "MANUAL",
        "details": "Ingredient naming requires manual expert review"
    }


# --- Allergen Validators ---

def check_contains_statement(data, check, category):
    """Check for 'Contains:' allergen statement"""
    allergens = data.get("allergens", {})
    contains = allergens.get("containsStatement")

    if contains and "contains" in contains.lower():
        return {
            "status": "PASS",
            "details": f"Contains statement: {contains}"
        }
    else:
        return {
            "status": "WARNING",
            "details": "'Contains:' statement not found - verify if allergens are present"
        }


def check_top_9_coverage(data, check, category):
    """Check if all Top 9 allergens are covered"""
    top_9 = category.get("top_9_allergens", [])
    allergens = data.get("allergens", {})
    declared = allergens.get("allergenList", [])

    return {
        "status": "MANUAL",
        "details": f"Found allergens: {', '.join(declared) if declared else 'None'} - verify all present allergens from Top 9 are declared"
    }


def check_allergen_prominence(data, check, category):
    """Check allergen statement prominence"""
    return {
        "status": "MANUAL",
        "details": "Visual check - verify allergen statement is prominent and easily readable"
    }


# --- Rounding Validators ---

def check_fat_rounding(data, check, category):
    """Check total fat and saturated fat rounding"""
    nutrients = data.get("nutrients", {})
    errors = []

    for fat_type in ["totalFat", "saturatedFat"]:
        if fat_type in nutrients:
            value = nutrients[fat_type].get("value", 0)

            if value < 5:
                # Should be rounded to nearest 0.5g
                if value % 0.5 != 0:
                    errors.append(f"{fat_type} {value}g should be rounded to nearest 0.5g")
            else:
                # Should be rounded to nearest 1g
                if value % 1 != 0:
                    errors.append(f"{fat_type} {value}g should be rounded to nearest 1g")

    if not errors:
        return {
            "status": "PASS",
            "details": "Fat values follow FDA rounding rules"
        }
    else:
        return {
            "status": "FAIL",
            "details": "; ".join(errors)
        }


def check_trans_fat_rounding(data, check, category):
    """Check trans fat is 0g or 0.5g only"""
    nutrients = data.get("nutrients", {})
    trans_fat = nutrients.get("transFat", {}).get("value", 0)

    if trans_fat in [0, 0.5]:
        return {
            "status": "PASS",
            "details": f"Trans fat correctly declared as {trans_fat}g"
        }
    else:
        return {
            "status": "FAIL",
            "details": f"Trans fat must be 0g or 0.5g, found {trans_fat}g"
        }


def check_sodium_rounding(data, check, category):
    """Check sodium rounding rules"""
    nutrients = data.get("nutrients", {})
    sodium = nutrients.get("sodium", {}).get("value", 0)

    if sodium < 140:
        if sodium % 5 != 0:
            return {
                "status": "FAIL",
                "details": f"Sodium <140mg should be rounded to nearest 5mg, found {sodium}mg"
            }
    else:
        if sodium % 10 != 0:
            return {
                "status": "FAIL",
                "details": f"Sodium ≥140mg should be rounded to nearest 10mg, found {sodium}mg"
            }

    return {
        "status": "PASS",
        "details": f"Sodium {sodium}mg follows rounding rules"
    }


def check_sugar_rounding(data, check, category):
    """Check sugar rounding (nearest 1g)"""
    nutrients = data.get("nutrients", {})
    errors = []

    for sugar_type in ["totalSugars", "addedSugars"]:
        if sugar_type in nutrients:
            value = nutrients[sugar_type].get("value", 0)
            if value % 1 != 0:
                errors.append(f"{sugar_type} {value}g should be rounded to nearest 1g")

    if not errors:
        return {
            "status": "PASS",
            "details": "Sugar values follow rounding rules"
        }
    else:
        return {
            "status": "FAIL",
            "details": "; ".join(errors)
        }


def check_protein_rounding(data, check, category):
    """Check protein rounding"""
    nutrients = data.get("nutrients", {})
    protein = nutrients.get("protein", {}).get("value", 0)

    if protein >= 1 and protein % 1 != 0:
        return {
            "status": "FAIL",
            "details": f"Protein ≥1g should be rounded to whole grams, found {protein}g"
        }

    return {
        "status": "PASS",
        "details": f"Protein {protein}g follows rounding rules"
    }


def check_vitamin_mineral_rounding(data, check, category):
    """Check vitamin/mineral %DV rounding"""
    nutrients = data.get("nutrients", {})
    errors = []

    for nutrient in ["vitaminD", "calcium", "iron", "potassium"]:
        if nutrient in nutrients:
            dv = nutrients[nutrient].get("dailyValue")
            if dv is not None and dv % 1 != 0:
                errors.append(f"{nutrient} %DV should be whole number, found {dv}%")

    if not errors:
        return {
            "status": "PASS",
            "details": "Vitamin/mineral %DV values are whole numbers"
        }
    else:
        return {
            "status": "FAIL",
            "details": "; ".join(errors)
        }


# --- Other Elements Validators ---

def check_net_weight(data, check, category):
    """Check net weight declaration"""
    other = data.get("otherElements", {})
    net_weight = other.get("netWeight")

    if net_weight:
        return {
            "status": "PASS",
            "details": f"Net weight: {net_weight}"
        }
    else:
        return {
            "status": "WARNING",
            "details": "Net weight not extracted - verify manually"
        }


def check_manufacturer_info(data, check, category):
    """Check manufacturer information"""
    other = data.get("otherElements", {})
    manufacturer = other.get("manufacturer")

    if manufacturer:
        return {
            "status": "PASS",
            "details": f"Manufacturer: {manufacturer[:100]}"
        }
    else:
        return {
            "status": "WARNING",
            "details": "Manufacturer info not extracted - verify manually"
        }


def check_safe_handling(data, check, category):
    """Check safe handling instructions"""
    other = data.get("otherElements", {})
    storage = other.get("storageInstructions")

    if storage:
        return {
            "status": "PASS",
            "details": f"Storage instructions: {storage[:100]}"
        }
    else:
        return {
            "status": "MANUAL",
            "details": "Storage/handling instructions not extracted - verify manually"
        }


def check_product_identity(data, check, category):
    """Check product identity/name"""
    product_name = data.get("productName")

    if product_name:
        return {
            "status": "PASS",
            "details": f"Product name: {product_name}"
        }
    else:
        return {
            "status": "WARNING",
            "details": "Product name not extracted - verify clear product identity on label"
        }
