"""
Manual Correction Interface
Allow users to review and correct extracted nutrition data
"""

import streamlit as st
import json


def render_manual_editor(extracted_data, key_prefix="editor"):
    """
    Render manual editing interface for extracted data

    Args:
        extracted_data: Extracted nutrition data to edit
        key_prefix: Prefix for streamlit widget keys

    Returns:
        dict: Edited data
    """
    st.subheader("✏️ Review & Correct Extracted Data")

    st.info("💡 **Tip**: Review the AI-extracted values below and make corrections if needed. Changes will be used for validation.")

    edited_data = extracted_data.copy()

    # Product Name
    st.markdown("### 📦 Product Information")
    col1, col2 = st.columns(2)

    with col1:
        edited_data["productName"] = st.text_input(
            "Product Name",
            value=extracted_data.get("productName", ""),
            key=f"{key_prefix}_product_name"
        )

    with col2:
        edited_data["formatType"] = st.selectbox(
            "Format Type",
            options=["single-column", "dual-column"],
            index=0 if extracted_data.get("formatType") == "single-column" else 1,
            key=f"{key_prefix}_format_type"
        )

    st.divider()

    # Serving Information
    st.markdown("### 🍽️ Serving Information")

    serving_info = extracted_data.get("servingInfo", {})
    serving_size = serving_info.get("servingSize", {})

    col1, col2, col3 = st.columns(3)

    with col1:
        serving_value = st.number_input(
            "Serving Size Value",
            min_value=0.0,
            value=float(serving_size.get("value", 0)) if serving_size.get("value") else 0.0,
            step=0.5,
            key=f"{key_prefix}_serving_value"
        )

    with col2:
        serving_unit = st.selectbox(
            "Unit",
            options=["g", "mL", "oz"],
            index=["g", "mL", "oz"].index(serving_size.get("unit", "g")) if serving_size.get("unit") in ["g", "mL", "oz"] else 0,
            key=f"{key_prefix}_serving_unit"
        )

    with col3:
        household_measure = st.text_input(
            "Household Measure",
            value=serving_size.get("householdMeasure", ""),
            placeholder="e.g., about 5 slices",
            key=f"{key_prefix}_household"
        )

    servings_per_container = st.text_input(
        "Servings per Container",
        value=str(serving_info.get("servingsPerContainer", "")),
        placeholder="e.g., about 2.5",
        key=f"{key_prefix}_servings"
    )

    # Update edited data
    edited_data["servingInfo"] = {
        "servingSize": {
            "value": serving_value,
            "unit": serving_unit,
            "householdMeasure": household_measure
        },
        "servingsPerContainer": servings_per_container
    }

    st.divider()

    # Calories
    st.markdown("### 🔥 Calories")

    calories_data = extracted_data.get("calories", {})

    col1, col2 = st.columns(2)

    with col1:
        calories_per_serving = st.number_input(
            "Calories per Serving",
            min_value=0,
            value=int(calories_data.get("perServing", 0)) if calories_data.get("perServing") else 0,
            step=5,
            key=f"{key_prefix}_calories"
        )

    with col2:
        if edited_data["formatType"] == "dual-column":
            calories_per_container = st.number_input(
                "Calories per Container",
                min_value=0,
                value=int(calories_data.get("perContainer", 0)) if calories_data.get("perContainer") else 0,
                step=5,
                key=f"{key_prefix}_calories_container"
            )
        else:
            calories_per_container = None

    edited_data["calories"] = {
        "perServing": calories_per_serving,
        "perContainer": calories_per_container
    }

    st.divider()

    # Nutrients
    st.markdown("### 📊 Nutrients")

    nutrients_data = extracted_data.get("nutrients", {})
    edited_nutrients = {}

    nutrient_definitions = [
        ("totalFat", "Total Fat", "g"),
        ("saturatedFat", "Saturated Fat", "g"),
        ("transFat", "Trans Fat", "g"),
        ("cholesterol", "Cholesterol", "mg"),
        ("sodium", "Sodium", "mg"),
        ("totalCarbohydrate", "Total Carbohydrate", "g"),
        ("dietaryFiber", "Dietary Fiber", "g"),
        ("totalSugars", "Total Sugars", "g"),
        ("addedSugars", "Added Sugars", "g"),
        ("protein", "Protein", "g"),
        ("vitaminD", "Vitamin D", "mcg"),
        ("calcium", "Calcium", "mg"),
        ("iron", "Iron", "mg"),
        ("potassium", "Potassium", "mg")
    ]

    # Create table-like layout
    for key, name, unit in nutrient_definitions:
        nutrient = nutrients_data.get(key, {})

        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            st.markdown(f"**{name}**")

        with col2:
            value = st.number_input(
                f"Value ({unit})",
                min_value=0.0,
                value=float(nutrient.get("value", 0)) if nutrient.get("value") is not None else 0.0,
                step=0.5 if unit == "g" else 1.0 if unit == "mg" else 0.1,
                key=f"{key_prefix}_nutrient_{key}",
                label_visibility="collapsed"
            )

        with col3:
            # %DV (not for trans fat)
            if key != "transFat":
                dv = st.number_input(
                    "% DV",
                    min_value=0,
                    value=int(nutrient.get("dailyValue", 0)) if nutrient.get("dailyValue") is not None else 0,
                    step=1,
                    key=f"{key_prefix}_dv_{key}",
                    label_visibility="collapsed"
                )
            else:
                dv = None

        edited_nutrients[key] = {
            "value": value,
            "unit": unit,
            "dailyValue": dv
        }

    edited_data["nutrients"] = edited_nutrients

    st.divider()

    # Ingredients
    st.markdown("### 🌾 Ingredients")

    ingredients_data = extracted_data.get("ingredients", {})

    ingredients_text = st.text_area(
        "Ingredient List",
        value=ingredients_data.get("text", ""),
        height=100,
        placeholder="Enter ingredients separated by commas",
        key=f"{key_prefix}_ingredients"
    )

    edited_data["ingredients"] = {
        "text": ingredients_text,
        "list": [ing.strip() for ing in ingredients_text.split(",")] if ingredients_text else [],
        "hasBoldLabel": ingredients_data.get("hasBoldLabel", False)
    }

    st.divider()

    # Allergens
    st.markdown("### ⚠️ Allergens")

    allergens_data = extracted_data.get("allergens", {})

    col1, col2 = st.columns(2)

    with col1:
        contains_statement = st.text_input(
            "Contains Statement",
            value=allergens_data.get("containsStatement", ""),
            placeholder="e.g., Contains: Soy",
            key=f"{key_prefix}_allergens"
        )

    with col2:
        allergen_list = st.multiselect(
            "Allergens (select all that apply)",
            options=["Milk", "Eggs", "Fish", "Shellfish", "Tree nuts", "Peanuts", "Wheat", "Soybeans", "Sesame"],
            default=allergens_data.get("allergenList", []),
            key=f"{key_prefix}_allergen_list"
        )

    edited_data["allergens"] = {
        "containsStatement": contains_statement,
        "allergenList": allergen_list
    }

    st.divider()

    # Action buttons
    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        if st.button("💾 Save Changes", type="primary", use_container_width=True, key=f"{key_prefix}_save"):
            st.session_state[f"{key_prefix}_edited_data"] = edited_data
            st.success("✅ Changes saved!")

    with col2:
        if st.button("🔄 Reset to Original", use_container_width=True, key=f"{key_prefix}_reset"):
            st.rerun()

    with col3:
        # Export edited data
        json_data = json.dumps(edited_data, indent=2)
        st.download_button(
            "📥 Download as JSON",
            data=json_data,
            file_name="edited_nutrition_data.json",
            mime="application/json",
            use_container_width=True,
            key=f"{key_prefix}_download"
        )

    return edited_data


def show_extraction_confidence(extracted_data):
    """
    Show confidence indicators for extracted data

    Args:
        extracted_data: Extracted nutrition data
    """
    st.markdown("### 🎯 Extraction Confidence")

    # Simple heuristic for confidence
    confidence_scores = {
        "Product Name": 1.0 if extracted_data.get("productName") else 0.0,
        "Serving Size": 1.0 if extracted_data.get("servingInfo", {}).get("servingSize", {}).get("value") else 0.0,
        "Calories": 1.0 if extracted_data.get("calories", {}).get("perServing") else 0.0,
        "Nutrients": len(extracted_data.get("nutrients", {})) / 14.0,  # 14 required nutrients
        "Ingredients": 1.0 if extracted_data.get("ingredients", {}).get("text") else 0.0,
    }

    col1, col2, col3, col4, col5 = st.columns(5)

    cols = [col1, col2, col3, col4, col5]

    for idx, (field, score) in enumerate(confidence_scores.items()):
        with cols[idx]:
            color = "🟢" if score >= 0.8 else "🟡" if score >= 0.5 else "🔴"
            st.metric(
                field,
                f"{color} {int(score * 100)}%",
                help=f"Confidence: {score:.0%}"
            )

    # Overall confidence
    overall = sum(confidence_scores.values()) / len(confidence_scores)

    if overall < 0.7:
        st.warning("⚠️ **Low extraction confidence** - Please review and correct the data below")
    elif overall < 0.9:
        st.info("ℹ️ **Medium extraction confidence** - Some fields may need review")
    else:
        st.success("✅ **High extraction confidence** - Data looks good, but always verify")


def compare_with_original(original_data, edited_data):
    """
    Show differences between original and edited data

    Args:
        original_data: Original extracted data
        edited_data: Manually edited data
    """
    st.markdown("### 🔍 Changes Made")

    changes = []

    # Compare serving info
    if original_data.get("servingInfo") != edited_data.get("servingInfo"):
        changes.append("Serving Information")

    # Compare calories
    if original_data.get("calories") != edited_data.get("calories"):
        changes.append("Calories")

    # Compare nutrients
    orig_nutrients = original_data.get("nutrients", {})
    edit_nutrients = edited_data.get("nutrients", {})

    for key in set(list(orig_nutrients.keys()) + list(edit_nutrients.keys())):
        if orig_nutrients.get(key) != edit_nutrients.get(key):
            changes.append(f"Nutrient: {key}")

    # Compare ingredients
    if original_data.get("ingredients") != edited_data.get("ingredients"):
        changes.append("Ingredients")

    # Compare allergens
    if original_data.get("allergens") != edited_data.get("allergens"):
        changes.append("Allergens")

    if changes:
        st.warning(f"⚠️ **{len(changes)} field(s) modified**: {', '.join(changes[:5])}")
    else:
        st.info("ℹ️ No changes made")
