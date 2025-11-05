"""
Comparison Tab Module for Streamlit App
Spec Sheet vs Packaging Label Comparison
"""

import streamlit as st
from extractor import extract_nutrition_data
from comparator import compare_nutrition_data, get_default_tolerances


def render_comparison_tab(product_type):
    """
    Render the Spec vs Packaging comparison interface

    Args:
        product_type: Selected product type
    """
    st.header("📊 Spec Sheet vs Packaging Comparison")
    st.markdown("Upload both your **spec sheet** (source of truth) and **packaging label** (what was printed) to find discrepancies.")

    st.divider()

    # Dual upload interface
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📄 Spec Sheet (Source of Truth)")
        spec_file = st.file_uploader(
            "Upload Spec Sheet",
            type=["pdf", "png", "jpg", "jpeg"],
            key="spec_upload",
            help="Your approved nutrition spec sheet"
        )

        if spec_file:
            st.image(spec_file) if spec_file.type.startswith("image") else st.info(f"📄 {spec_file.name}")

    with col2:
        st.subheader("📦 Packaging Label (Printed)")
        pkg_file = st.file_uploader(
            "Upload Packaging Label",
            type=["pdf", "png", "jpg", "jpeg"],
            key="pkg_upload",
            help="The actual printed packaging label"
        )

        if pkg_file:
            st.image(pkg_file) if pkg_file.type.startswith("image") else st.info(f"📄 {pkg_file.name}")

    st.divider()

    # Tolerance settings (expandable)
    with st.expander("⚙️ Tolerance Settings", expanded=False):
        st.markdown("**Set acceptable variance ranges for comparisons:**")

        col_a, col_b, col_c = st.columns(3)

        with col_a:
            serving_tolerance = st.slider(
                "Serving Size Tolerance (%)",
                min_value=0.0,
                max_value=10.0,
                value=2.0,
                step=0.5,
                help="Allowed % difference for serving size"
            )

        with col_b:
            calorie_tolerance = st.slider(
                "Calorie Tolerance (%)",
                min_value=0.0,
                max_value=10.0,
                value=5.0,
                step=0.5,
                help="Allowed % difference for calories"
            )

        with col_c:
            nutrient_tolerance = st.slider(
                "Nutrient Tolerance (%)",
                min_value=0.0,
                max_value=10.0,
                value=5.0,
                step=0.5,
                help="Allowed % difference for nutrients"
            )

        # Build custom tolerance settings
        custom_tolerances = get_default_tolerances()
        custom_tolerances["servingSize"]["percentage"] = serving_tolerance
        custom_tolerances["calories"]["percentage"] = calorie_tolerance
        custom_tolerances["nutrients"]["default"]["percentage"] = nutrient_tolerance

    # Analyze button
    if spec_file and pkg_file:
        if st.button("🔍 Compare Spec vs Packaging", type="primary", use_container_width=True):
            with st.spinner("Extracting data from spec sheet..."):
                spec_data = extract_nutrition_data(spec_file, product_type)
                st.session_state.spec_data = spec_data

            with st.spinner("Extracting data from packaging label..."):
                pkg_data = extract_nutrition_data(pkg_file, product_type)
                st.session_state.pkg_data = pkg_data

            with st.spinner("Comparing nutrition data..."):
                comparison_results = compare_nutrition_data(
                    spec_data,
                    pkg_data,
                    custom_tolerances if 'custom_tolerances' in locals() else None
                )
                st.session_state.comparison_results = comparison_results

            st.success("✅ Comparison Complete!")
            st.rerun()

    # Display results if available
    if "comparison_results" in st.session_state:
        st.divider()
        display_comparison_results(
            st.session_state.comparison_results,
            st.session_state.get("spec_data"),
            st.session_state.get("pkg_data")
        )


def display_comparison_results(results, spec_data, pkg_data):
    """Display comparison results"""

    st.header("📊 Comparison Results")

    # Overall score
    match_score = results.get("matchScore", 0)
    overall_match = results.get("overallMatch", False)

    col1, col2, col3, col4 = st.columns(4)

    # Score color
    if match_score >= 95:
        score_color = "green"
        status_emoji = "✅"
    elif match_score >= 85:
        score_color = "orange"
        status_emoji = "⚠️"
    else:
        score_color = "red"
        status_emoji = "❌"

    col1.metric(
        "Match Score",
        f"{match_score}%",
        help="Percentage of exact and within-tolerance matches"
    )

    col2.metric(
        "Status",
        "PASS" if overall_match else "FAIL",
        help="Overall pass/fail status",
        delta="✅ Approved" if overall_match else "❌ Review Required",
        delta_color="normal" if overall_match else "inverse"
    )

    summary = results.get("summary", {})
    col3.metric(
        "Exact Matches",
        summary.get("exactMatches", 0),
        help="Sections with perfect matches"
    )

    col4.metric(
        "Critical Issues",
        summary.get("outOfTolerance", 0),
        help="Values outside tolerance",
        delta_color="inverse"
    )

    st.divider()

    # Critical mismatches (if any)
    critical = results.get("criticalMismatches", [])
    if critical:
        st.error(f"❌ **{len(critical)} Critical Mismatch(es) Found**")

        for i, mismatch in enumerate(critical, 1):
            with st.expander(f"🔴 Critical: {mismatch.get('field', 'Unknown')}", expanded=True):
                col_spec, col_pkg, col_diff = st.columns(3)

                with col_spec:
                    st.markdown("**Spec Sheet:**")
                    st.code(str(mismatch.get("spec", "N/A")))

                with col_pkg:
                    st.markdown("**Packaging:**")
                    st.code(str(mismatch.get("packaging", "N/A")))

                with col_diff:
                    st.markdown("**Difference:**")
                    if "difference" in mismatch:
                        st.code(str(mismatch.get("difference")))
                    if "percentDiff" in mismatch:
                        st.metric("% Difference", mismatch.get("percentDiff"))

                st.warning(f"⚠️ {mismatch.get('message', 'Values do not match')}")

    # Minor differences
    minor = results.get("minorDifferences", [])
    if minor:
        with st.expander(f"⚠️ {len(minor)} Minor Difference(s) (Within Tolerance)", expanded=False):
            for diff in minor:
                col_a, col_b, col_c = st.columns([2, 2, 3])

                with col_a:
                    st.markdown(f"**{diff.get('field')}**")

                with col_b:
                    st.text(f"Spec: {diff.get('spec')}")
                    st.text(f"Pkg: {diff.get('packaging')}")

                with col_c:
                    st.info(diff.get('message', ''))

                st.divider()

    # Exact matches
    exact = results.get("exactMatches", [])
    if exact:
        st.success(f"✅ **{len(exact)} Section(s) Match Perfectly**: {', '.join(exact)}")

    st.divider()

    # Detailed comparison tables
    st.subheader("📋 Detailed Comparison")

    # Serving Info
    with st.expander("🍽️ Serving Information", expanded=True):
        display_serving_comparison(results.get("servingInfo", {}), spec_data, pkg_data)

    # Calories
    with st.expander("🔥 Calories", expanded=True):
        display_calories_comparison(results.get("calories", {}), spec_data, pkg_data)

    # Nutrients
    with st.expander("📊 Nutrients", expanded=True):
        display_nutrients_comparison(results.get("nutrients", {}), spec_data, pkg_data)

    # Ingredients
    with st.expander("🌾 Ingredients", expanded=True):
        display_ingredients_comparison(results.get("ingredients", {}), spec_data, pkg_data)

    # Allergens
    with st.expander("⚠️ Allergens", expanded=True):
        display_allergens_comparison(results.get("allergens", {}), spec_data, pkg_data)

    # Export options
    st.divider()
    st.subheader("📥 Export Comparison Report")

    col_x, col_y = st.columns(2)

    with col_x:
        if st.button("📄 Download PDF Report", use_container_width=True):
            # TODO: Implement comparison PDF report
            st.info("Comparison PDF export coming soon!")

    with col_y:
        if st.button("📊 Download Excel Report", use_container_width=True):
            # TODO: Implement Excel export
            st.info("Excel export coming soon!")


def display_serving_comparison(comparison, spec_data, pkg_data):
    """Display serving information comparison"""
    status = comparison.get("status", "MATCH")
    differences = comparison.get("differences", [])

    spec_serving = spec_data.get("servingInfo", {})
    pkg_serving = pkg_data.get("servingInfo", {})

    # Create comparison table
    data = {
        "Field": [],
        "Spec Sheet": [],
        "Packaging": [],
        "Status": []
    }

    # Serving size
    spec_size = spec_serving.get("servingSize", {})
    pkg_size = pkg_serving.get("servingSize", {})

    data["Field"].append("Serving Size")
    data["Spec Sheet"].append(f"{spec_size.get('value', 'N/A')}{spec_size.get('unit', '')}")
    data["Packaging"].append(f"{pkg_size.get('value', 'N/A')}{pkg_size.get('unit', '')}")

    size_match = spec_size.get('value') == pkg_size.get('value')
    data["Status"].append("✅ Match" if size_match else "❌ Differ")

    # Servings per container
    data["Field"].append("Servings per Container")
    data["Spec Sheet"].append(str(spec_serving.get("servingsPerContainer", "N/A")))
    data["Packaging"].append(str(pkg_serving.get("servingsPerContainer", "N/A")))

    servings_match = str(spec_serving.get("servingsPerContainer")) == str(pkg_serving.get("servingsPerContainer"))
    data["Status"].append("✅ Match" if servings_match else "⚠️ Differ")

    # Household measure
    data["Field"].append("Household Measure")
    data["Spec Sheet"].append(spec_size.get("householdMeasure", "N/A"))
    data["Packaging"].append(pkg_size.get("householdMeasure", "N/A"))

    household_match = spec_size.get("householdMeasure") == pkg_size.get("householdMeasure")
    data["Status"].append("✅ Match" if household_match else "⚠️ Differ")

    st.table(data)

    # Show differences
    if differences:
        for diff in differences:
            severity = diff.get("severity", "WARNING")
            if severity == "CRITICAL":
                st.error(f"❌ {diff.get('message')}")
            else:
                st.warning(f"⚠️ {diff.get('message')}")


def display_calories_comparison(comparison, spec_data, pkg_data):
    """Display calories comparison"""
    spec_cal = spec_data.get("calories", {})
    pkg_cal = pkg_data.get("calories", {})

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Spec Sheet**")
        st.metric("Calories", spec_cal.get("perServing", "N/A"))

    with col2:
        st.markdown("**Packaging**")
        st.metric("Calories", pkg_cal.get("perServing", "N/A"))

    with col3:
        st.markdown("**Status**")
        if spec_cal.get("perServing") == pkg_cal.get("perServing"):
            st.success("✅ Match")
        else:
            diff = abs(spec_cal.get("perServing", 0) - pkg_cal.get("perServing", 0))
            st.error(f"❌ Differ by {diff}")

    # Show differences
    differences = comparison.get("differences", [])
    if differences:
        for diff in differences:
            if diff.get("severity") == "CRITICAL":
                st.error(f"❌ {diff.get('message')}")
            else:
                st.warning(f"⚠️ {diff.get('message')}")


def display_nutrients_comparison(comparison, spec_data, pkg_data):
    """Display nutrients comparison table"""
    spec_nutrients = spec_data.get("nutrients", {})
    pkg_nutrients = pkg_data.get("nutrients", {})

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

    # Build comparison table
    table_data = []

    for key, name in nutrient_names.items():
        spec_nut = spec_nutrients.get(key, {})
        pkg_nut = pkg_nutrients.get(key, {})

        spec_val = spec_nut.get("value")
        pkg_val = pkg_nut.get("value")

        if spec_val is None and pkg_val is None:
            continue

        unit = spec_nut.get("unit", "")

        # Status
        if spec_val == pkg_val:
            status = "✅"
        elif spec_val is None or pkg_val is None:
            status = "❓"
        else:
            status = "❌"

        table_data.append({
            "Nutrient": name,
            "Spec": f"{spec_val}{unit}" if spec_val is not None else "N/A",
            "Package": f"{pkg_val}{unit}" if pkg_val is not None else "N/A",
            "Status": status
        })

    if table_data:
        st.table(table_data)
    else:
        st.info("No nutrient data extracted")

    # Show differences
    differences = comparison.get("differences", [])
    if differences:
        st.markdown("**Issues Found:**")
        for diff in differences:
            if diff.get("severity") == "CRITICAL":
                st.error(f"❌ {diff.get('field')}: {diff.get('message')}")
            elif diff.get("severity") == "INFO":
                st.info(f"ℹ️ {diff.get('field')}: {diff.get('message')}")


def display_ingredients_comparison(comparison, spec_data, pkg_data):
    """Display ingredients comparison"""
    spec_ing = spec_data.get("ingredients", {})
    pkg_ing = pkg_data.get("ingredients", {})

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Spec Sheet Ingredients:**")
        st.text_area("", spec_ing.get("text", "Not extracted"), height=150, key="spec_ing_display", disabled=True)

    with col2:
        st.markdown("**Packaging Ingredients:**")
        st.text_area("", pkg_ing.get("text", "Not extracted"), height=150, key="pkg_ing_display", disabled=True)

    # Show differences
    differences = comparison.get("differences", [])
    if differences:
        for diff in differences:
            similarity = diff.get("similarity", "N/A")
            st.metric("Text Similarity", similarity)

            if diff.get("missingInPackaging"):
                st.error(f"❌ Missing in packaging: {', '.join(diff['missingInPackaging'])}")

            if diff.get("extraInPackaging"):
                st.warning(f"⚠️ Extra in packaging: {', '.join(diff['extraInPackaging'])}")

            st.info(diff.get("message"))
    else:
        st.success("✅ Ingredient lists match")


def display_allergens_comparison(comparison, spec_data, pkg_data):
    """Display allergens comparison"""
    spec_all = spec_data.get("allergens", {})
    pkg_all = pkg_data.get("allergens", {})

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Spec Sheet Allergens:**")
        spec_list = spec_all.get("allergenList", [])
        if spec_list:
            for allergen in spec_list:
                st.markdown(f"- {allergen}")
        else:
            st.info("No allergens declared")

    with col2:
        st.markdown("**Packaging Allergens:**")
        pkg_list = pkg_all.get("allergenList", [])
        if pkg_list:
            for allergen in pkg_list:
                st.markdown(f"- {allergen}")
        else:
            st.info("No allergens declared")

    # Show differences
    differences = comparison.get("differences", [])
    if differences:
        for diff in differences:
            if "missingAllergens" in diff:
                st.error(f"❌ Critical: Missing allergens in packaging: {', '.join(diff['missingAllergens'])}")

            if "extraAllergens" in diff:
                st.warning(f"⚠️ Extra allergens in packaging: {', '.join(diff['extraAllergens'])}")
    else:
        st.success("✅ Allergen lists match")
