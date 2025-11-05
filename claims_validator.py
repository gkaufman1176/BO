"""
Claims Validation Module
Validate nutrition and health claims against FDA regulations
Based on 21 CFR 101.54 (Nutrient content claims) and 21 CFR 101.62
"""


def validate_all_claims(extracted_data, detect_from_label=True):
    """
    Validate all possible nutrition claims

    Args:
        extracted_data: Extracted nutrition data
        detect_from_label: Whether to auto-detect claims from product name

    Returns:
        dict: Claim validation results
    """
    results = {
        "validClaims": [],
        "invalidClaims": [],
        "suggestedClaims": [],
        "summary": {
            "totalChecked": 0,
            "valid": 0,
            "invalid": 0
        }
    }

    # Get nutrition values
    nutrients = extracted_data.get("nutrients", {})
    calories = extracted_data.get("calories", {}).get("perServing", 0)
    serving_size = extracted_data.get("servingInfo", {}).get("servingSize", {}).get("value", 50)

    # Define all claims to check
    claims_to_check = [
        # Fat claims
        ("Fat Free", validate_fat_free_claim, nutrients),
        ("Low Fat", validate_low_fat_claim, nutrients),
        ("Reduced Fat", validate_reduced_fat_claim, nutrients),

        # Saturated Fat claims
        ("Low Saturated Fat", validate_low_saturated_fat_claim, nutrients),
        ("Saturated Fat Free", validate_saturated_fat_free_claim, nutrients),

        # Cholesterol claims
        ("Cholesterol Free", validate_cholesterol_free_claim, nutrients),
        ("Low Cholesterol", validate_low_cholesterol_claim, nutrients),

        # Sodium claims
        ("Sodium Free", validate_sodium_free_claim, nutrients),
        ("Very Low Sodium", validate_very_low_sodium_claim, nutrients),
        ("Low Sodium", validate_low_sodium_claim, nutrients),
        ("Reduced Sodium", validate_reduced_sodium_claim, nutrients),

        # Calorie claims
        ("Calorie Free", validate_calorie_free_claim, calories),
        ("Low Calorie", validate_low_calorie_claim, calories),
        ("Reduced Calorie", validate_reduced_calorie_claim, calories),

        # Sugar claims
        ("Sugar Free", validate_sugar_free_claim, nutrients),
        ("No Added Sugars", validate_no_added_sugars_claim, nutrients),

        # Fiber claims
        ("Good Source of Fiber", validate_good_source_fiber_claim, nutrients),
        ("High Fiber", validate_high_fiber_claim, nutrients),

        # Protein claims
        ("Good Source of Protein", validate_good_source_protein_claim, nutrients, serving_size),
        ("High Protein", validate_high_protein_claim, nutrients, serving_size),

        # General nutrient claims
        ("Light/Lite", validate_light_claim, calories, nutrients),
    ]

    for claim_name, validator_func, *args in claims_to_check:
        result = validator_func(*args)

        results["totalChecked"] += 1

        if result["valid"]:
            results["validClaims"].append({
                "claim": claim_name,
                "status": "VALID",
                "requirement": result.get("requirement", ""),
                "actualValue": result.get("actualValue", ""),
                "cfr_reference": result.get("cfr_reference", "")
            })
            results["valid"] += 1
        else:
            # Check if close to qualifying
            if result.get("closeToQualifying"):
                results["suggestedClaims"].append({
                    "claim": claim_name,
                    "status": "CLOSE",
                    "message": result.get("message", ""),
                    "suggestion": result.get("suggestion", "")
                })
            else:
                results["invalidClaims"].append({
                    "claim": claim_name,
                    "status": "INVALID",
                    "reason": result.get("reason", ""),
                    "requirement": result.get("requirement", ""),
                    "actualValue": result.get("actualValue", "")
                })
                results["invalid"] += 1

    results["summary"]["totalChecked"] = len(claims_to_check)
    results["summary"]["valid"] = len(results["validClaims"])
    results["summary"]["invalid"] = len(results["invalidClaims"])

    return results


# =============================================================================
# FAT CLAIMS (21 CFR 101.62(b))
# =============================================================================

def validate_fat_free_claim(nutrients):
    """Fat Free: <0.5g total fat per serving"""
    total_fat = nutrients.get("totalFat", {}).get("value", 999)

    return {
        "valid": total_fat < 0.5,
        "requirement": "<0.5g total fat per serving",
        "actualValue": f"{total_fat}g",
        "cfr_reference": "21 CFR 101.62(b)(2)",
        "reason": f"Total fat is {total_fat}g (must be <0.5g)" if total_fat >= 0.5 else ""
    }


def validate_low_fat_claim(nutrients):
    """Low Fat: ≤3g total fat per serving"""
    total_fat = nutrients.get("totalFat", {}).get("value", 999)

    return {
        "valid": total_fat <= 3,
        "requirement": "≤3g total fat per serving",
        "actualValue": f"{total_fat}g",
        "cfr_reference": "21 CFR 101.62(b)(2)",
        "reason": f"Total fat is {total_fat}g (must be ≤3g)" if total_fat > 3 else "",
        "closeToQualifying": 3 < total_fat <= 4,
        "suggestion": f"Reduce total fat by {total_fat - 3:.1f}g to qualify" if 3 < total_fat <= 4 else ""
    }


def validate_reduced_fat_claim(nutrients):
    """Reduced Fat: At least 25% less fat than reference food"""
    # Note: This requires reference food data, which we don't have
    # Return as manual check required
    return {
        "valid": False,
        "requirement": "At least 25% less fat than reference food",
        "actualValue": "Manual verification required",
        "cfr_reference": "21 CFR 101.62(b)(3)",
        "reason": "Requires comparison with reference food - manual verification needed"
    }


# =============================================================================
# SATURATED FAT CLAIMS (21 CFR 101.62(c))
# =============================================================================

def validate_saturated_fat_free_claim(nutrients):
    """Saturated Fat Free: <0.5g saturated fat AND <0.5g trans fat"""
    sat_fat = nutrients.get("saturatedFat", {}).get("value", 999)
    trans_fat = nutrients.get("transFat", {}).get("value", 999)

    valid = sat_fat < 0.5 and trans_fat < 0.5

    return {
        "valid": valid,
        "requirement": "<0.5g saturated fat AND <0.5g trans fat per serving",
        "actualValue": f"Sat: {sat_fat}g, Trans: {trans_fat}g",
        "cfr_reference": "21 CFR 101.62(c)(2)",
        "reason": f"Saturated fat: {sat_fat}g, Trans fat: {trans_fat}g (both must be <0.5g)" if not valid else ""
    }


def validate_low_saturated_fat_claim(nutrients):
    """Low Saturated Fat: ≤1g saturated fat AND ≤15% calories from saturated fat"""
    sat_fat = nutrients.get("saturatedFat", {}).get("value", 999)
    # Simplified check (would need calorie calculation for exact validation)

    return {
        "valid": sat_fat <= 1,
        "requirement": "≤1g saturated fat per serving (and ≤15% of calories)",
        "actualValue": f"{sat_fat}g",
        "cfr_reference": "21 CFR 101.62(c)(2)",
        "reason": f"Saturated fat is {sat_fat}g (must be ≤1g)" if sat_fat > 1 else "",
        "closeToQualifying": 1 < sat_fat <= 1.5,
        "suggestion": f"Reduce saturated fat by {sat_fat - 1:.1f}g to qualify" if 1 < sat_fat <= 1.5 else ""
    }


# =============================================================================
# CHOLESTEROL CLAIMS (21 CFR 101.62(d))
# =============================================================================

def validate_cholesterol_free_claim(nutrients):
    """Cholesterol Free: <2mg cholesterol AND ≤2g saturated fat"""
    cholesterol = nutrients.get("cholesterol", {}).get("value", 999)
    sat_fat = nutrients.get("saturatedFat", {}).get("value", 999)

    valid = cholesterol < 2 and sat_fat <= 2

    return {
        "valid": valid,
        "requirement": "<2mg cholesterol AND ≤2g saturated fat per serving",
        "actualValue": f"Cholesterol: {cholesterol}mg, Sat Fat: {sat_fat}g",
        "cfr_reference": "21 CFR 101.62(d)(2)",
        "reason": f"Cholesterol: {cholesterol}mg (must be <2mg), Sat fat: {sat_fat}g (must be ≤2g)" if not valid else ""
    }


def validate_low_cholesterol_claim(nutrients):
    """Low Cholesterol: ≤20mg cholesterol AND ≤2g saturated fat"""
    cholesterol = nutrients.get("cholesterol", {}).get("value", 999)
    sat_fat = nutrients.get("saturatedFat", {}).get("value", 999)

    valid = cholesterol <= 20 and sat_fat <= 2

    return {
        "valid": valid,
        "requirement": "≤20mg cholesterol AND ≤2g saturated fat per serving",
        "actualValue": f"Cholesterol: {cholesterol}mg, Sat Fat: {sat_fat}g",
        "cfr_reference": "21 CFR 101.62(d)(2)",
        "reason": f"Cholesterol: {cholesterol}mg, Sat fat: {sat_fat}g" if not valid else ""
    }


# =============================================================================
# SODIUM CLAIMS (21 CFR 101.61)
# =============================================================================

def validate_sodium_free_claim(nutrients):
    """Sodium Free: <5mg sodium per serving"""
    sodium = nutrients.get("sodium", {}).get("value", 9999)

    return {
        "valid": sodium < 5,
        "requirement": "<5mg sodium per serving",
        "actualValue": f"{sodium}mg",
        "cfr_reference": "21 CFR 101.61(b)(4)",
        "reason": f"Sodium is {sodium}mg (must be <5mg)" if sodium >= 5 else ""
    }


def validate_very_low_sodium_claim(nutrients):
    """Very Low Sodium: ≤35mg sodium per serving"""
    sodium = nutrients.get("sodium", {}).get("value", 9999)

    return {
        "valid": sodium <= 35,
        "requirement": "≤35mg sodium per serving",
        "actualValue": f"{sodium}mg",
        "cfr_reference": "21 CFR 101.61(b)(5)",
        "reason": f"Sodium is {sodium}mg (must be ≤35mg)" if sodium > 35 else "",
        "closeToQualifying": 35 < sodium <= 50,
        "suggestion": f"Reduce sodium by {sodium - 35}mg to qualify" if 35 < sodium <= 50 else ""
    }


def validate_low_sodium_claim(nutrients):
    """Low Sodium: ≤140mg sodium per serving"""
    sodium = nutrients.get("sodium", {}).get("value", 9999)

    return {
        "valid": sodium <= 140,
        "requirement": "≤140mg sodium per serving",
        "actualValue": f"{sodium}mg",
        "cfr_reference": "21 CFR 101.61(b)(6)",
        "reason": f"Sodium is {sodium}mg (must be ≤140mg)" if sodium > 140 else "",
        "closeToQualifying": 140 < sodium <= 160,
        "suggestion": f"Reduce sodium by {sodium - 140}mg to qualify" if 140 < sodium <= 160 else ""
    }


def validate_reduced_sodium_claim(nutrients):
    """Reduced Sodium: At least 25% less sodium than reference"""
    # Requires reference food - manual check
    return {
        "valid": False,
        "requirement": "At least 25% less sodium than reference food",
        "actualValue": "Manual verification required",
        "cfr_reference": "21 CFR 101.61(b)(7)",
        "reason": "Requires comparison with reference food"
    }


# =============================================================================
# CALORIE CLAIMS (21 CFR 101.60)
# =============================================================================

def validate_calorie_free_claim(calories):
    """Calorie Free: <5 calories per serving"""
    return {
        "valid": calories < 5,
        "requirement": "<5 calories per serving",
        "actualValue": f"{calories} cal",
        "cfr_reference": "21 CFR 101.60(b)(1)",
        "reason": f"Calories are {calories} (must be <5)" if calories >= 5 else ""
    }


def validate_low_calorie_claim(calories):
    """Low Calorie: ≤40 calories per serving"""
    return {
        "valid": calories <= 40,
        "requirement": "≤40 calories per serving",
        "actualValue": f"{calories} cal",
        "cfr_reference": "21 CFR 101.60(b)(2)",
        "reason": f"Calories are {calories} (must be ≤40)" if calories > 40 else "",
        "closeToQualifying": 40 < calories <= 50,
        "suggestion": f"Reduce calories by {calories - 40} to qualify" if 40 < calories <= 50 else ""
    }


def validate_reduced_calorie_claim(calories):
    """Reduced Calorie: At least 25% fewer calories than reference"""
    # Requires reference food
    return {
        "valid": False,
        "requirement": "At least 25% fewer calories than reference food",
        "actualValue": "Manual verification required",
        "cfr_reference": "21 CFR 101.60(b)(3)",
        "reason": "Requires comparison with reference food"
    }


# =============================================================================
# SUGAR CLAIMS (21 CFR 101.60(c))
# =============================================================================

def validate_sugar_free_claim(nutrients):
    """Sugar Free: <0.5g sugars per serving"""
    sugars = nutrients.get("totalSugars", {}).get("value", 999)

    return {
        "valid": sugars < 0.5,
        "requirement": "<0.5g sugars per serving",
        "actualValue": f"{sugars}g",
        "cfr_reference": "21 CFR 101.60(c)",
        "reason": f"Total sugars are {sugars}g (must be <0.5g)" if sugars >= 0.5 else ""
    }


def validate_no_added_sugars_claim(nutrients):
    """No Added Sugars: 0g added sugars"""
    added_sugars = nutrients.get("addedSugars", {}).get("value", 999)

    return {
        "valid": added_sugars == 0,
        "requirement": "0g added sugars per serving",
        "actualValue": f"{added_sugars}g",
        "cfr_reference": "21 CFR 101.60(c)(2)",
        "reason": f"Added sugars are {added_sugars}g (must be 0g)" if added_sugars > 0 else ""
    }


# =============================================================================
# FIBER CLAIMS (21 CFR 101.54(d))
# =============================================================================

def validate_good_source_fiber_claim(nutrients):
    """Good Source of Fiber: 2.5g to 4.9g fiber (10-19% DV)"""
    fiber = nutrients.get("dietaryFiber", {}).get("value", 0)

    valid = 2.5 <= fiber < 5

    return {
        "valid": valid,
        "requirement": "2.5-4.9g fiber per serving (10-19% DV)",
        "actualValue": f"{fiber}g",
        "cfr_reference": "21 CFR 101.54(d)",
        "reason": f"Fiber is {fiber}g (must be 2.5-4.9g)" if not valid else "",
        "closeToQualifying": 2.0 <= fiber < 2.5,
        "suggestion": f"Increase fiber by {2.5 - fiber:.1f}g to qualify" if 2.0 <= fiber < 2.5 else ""
    }


def validate_high_fiber_claim(nutrients):
    """High Fiber: ≥5g fiber per serving (≥20% DV)"""
    fiber = nutrients.get("dietaryFiber", {}).get("value", 0)

    return {
        "valid": fiber >= 5,
        "requirement": "≥5g fiber per serving (≥20% DV)",
        "actualValue": f"{fiber}g",
        "cfr_reference": "21 CFR 101.54(d)",
        "reason": f"Fiber is {fiber}g (must be ≥5g)" if fiber < 5 else "",
        "closeToQualifying": 4.0 <= fiber < 5,
        "suggestion": f"Increase fiber by {5 - fiber:.1f}g to qualify" if 4.0 <= fiber < 5 else ""
    }


# =============================================================================
# PROTEIN CLAIMS (21 CFR 101.54(e))
# =============================================================================

def validate_good_source_protein_claim(nutrients, serving_size):
    """Good Source of Protein: 10% DV (5g) per serving"""
    protein = nutrients.get("protein", {}).get("value", 0)

    # FDA protein DV is 50g, so 10% = 5g
    return {
        "valid": protein >= 5,
        "requirement": "≥5g protein per serving (10% DV)",
        "actualValue": f"{protein}g",
        "cfr_reference": "21 CFR 101.54(e)",
        "reason": f"Protein is {protein}g (must be ≥5g)" if protein < 5 else "",
        "closeToQualifying": 4.0 <= protein < 5,
        "suggestion": f"Increase protein by {5 - protein:.1f}g to qualify" if 4.0 <= protein < 5 else ""
    }


def validate_high_protein_claim(nutrients, serving_size):
    """High Protein: 20% DV (10g) per serving"""
    protein = nutrients.get("protein", {}).get("value", 0)

    # FDA protein DV is 50g, so 20% = 10g
    return {
        "valid": protein >= 10,
        "requirement": "≥10g protein per serving (20% DV)",
        "actualValue": f"{protein}g",
        "cfr_reference": "21 CFR 101.54(e)",
        "reason": f"Protein is {protein}g (must be ≥10g)" if protein < 10 else "",
        "closeToQualifying": 8.0 <= protein < 10,
        "suggestion": f"Increase protein by {10 - protein:.1f}g to qualify" if 8.0 <= protein < 10 else ""
    }


# =============================================================================
# LIGHT/LITE CLAIMS (21 CFR 101.56)
# =============================================================================

def validate_light_claim(calories, nutrients):
    """Light/Lite: 1/3 fewer calories OR 50% less fat than reference"""
    # Requires reference food for proper validation
    # Can check if product is low in both calories and fat as indicator

    total_fat = nutrients.get("totalFat", {}).get("value", 999)
    is_low_cal = calories <= 40
    is_low_fat = total_fat <= 3

    # Simplified check
    return {
        "valid": False,  # Requires reference food
        "requirement": "1/3 fewer calories OR 50% less fat than reference food",
        "actualValue": f"{calories} cal, {total_fat}g fat",
        "cfr_reference": "21 CFR 101.56",
        "reason": "Requires comparison with reference food - manual verification needed",
        "closeToQualifying": is_low_cal and is_low_fat,
        "suggestion": "Product qualifies as low-calorie and low-fat" if is_low_cal and is_low_fat else ""
    }
