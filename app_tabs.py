"""
Additional App Tabs for New Features
Batch Processing, Excel Import, Manual Editor, Claims Validation
"""

import streamlit as st
from excel_importer import import_from_excel, export_to_excel
from batch_processor import process_batch, process_batch_comparison, render_batch_results
from manual_editor import render_manual_editor, show_extraction_confidence
from claims_validator import validate_all_claims


def render_batch_processing_tab(product_type, extract_func, validate_func, checklist_config):
    """Render batch processing tab"""
    st.header("📦 Batch Processing")
    st.markdown("Upload and analyze multiple labels at once for efficient quality control.")

    st.divider()

    # Choose mode
    mode = st.radio(
        "Processing Mode",
        options=["Compliance Checks", "Spec vs Packaging Comparison"],
        horizontal=True,
        help="Choose whether to run compliance checks or comparisons"
    )

    st.divider()

    if mode == "Compliance Checks":
        st.subheader("📤 Upload Multiple Labels")

        uploaded_files = st.file_uploader(
            "Choose nutrition label files (PDF, PNG, JPG)",
            type=["pdf", "png", "jpg", "jpeg"],
            accept_multiple_files=True,
            key="batch_upload",
            help="Select multiple files to process in batch"
        )

        if uploaded_files:
            st.info(f"📁 {len(uploaded_files)} file(s) selected")

            # Show file list
            with st.expander("📋 Selected Files", expanded=False):
                for idx, file in enumerate(uploaded_files, 1):
                    st.text(f"{idx}. {file.name} ({file.size / 1024:.1f} KB)")

            if st.button("🚀 Process All Files", type="primary", use_container_width=True):
                with st.spinner("Processing batch..."):
                    results = process_batch(
                        uploaded_files,
                        product_type,
                        extract_func,
                        validate_func,
                        checklist_config
                    )

                    st.session_state.batch_results = results
                    st.session_state.batch_mode = "compliance"
                    st.rerun()

        # Display results if available
        if "batch_results" in st.session_state and st.session_state.get("batch_mode") == "compliance":
            st.divider()
            render_batch_results(st.session_state.batch_results, comparison_mode=False)

    else:  # Comparison mode
        st.subheader("📤 Upload Spec Sheets and Packaging Labels")

        col1, col2 = st.columns(2)

        with col1:
            spec_files = st.file_uploader(
                "Spec Sheets",
                type=["pdf", "png", "jpg", "jpeg"],
                accept_multiple_files=True,
                key="batch_spec_upload",
                help="Upload spec sheet files"
            )

        with col2:
            pkg_files = st.file_uploader(
                "Packaging Labels",
                type=["pdf", "png", "jpg", "jpeg"],
                accept_multiple_files=True,
                key="batch_pkg_upload",
                help="Upload packaging files (same order as spec sheets)"
            )

        if spec_files and pkg_files:
            if len(spec_files) != len(pkg_files):
                st.error(f"❌ Number of spec files ({len(spec_files)}) must match packaging files ({len(pkg_files)})")
            else:
                st.success(f"✅ {len(spec_files)} pairs ready for comparison")

                # Show pairs
                with st.expander("📋 File Pairs", expanded=False):
                    for idx, (spec, pkg) in enumerate(zip(spec_files, pkg_files), 1):
                        st.text(f"{idx}. {spec.name} ↔ {pkg.name}")

                if st.button("🔍 Compare All Pairs", type="primary", use_container_width=True):
                    from comparator import compare_nutrition_data

                    with st.spinner("Comparing pairs..."):
                        results = process_batch_comparison(
                            spec_files,
                            pkg_files,
                            product_type,
                            extract_func,
                            compare_nutrition_data
                        )

                        st.session_state.batch_results = results
                        st.session_state.batch_mode = "comparison"
                        st.rerun()

        # Display results if available
        if "batch_results" in st.session_state and st.session_state.get("batch_mode") == "comparison":
            st.divider()
            render_batch_results(st.session_state.batch_results, comparison_mode=True)


def render_excel_import_tab(product_type):
    """Render Excel import tab"""
    st.header("📊 Excel Import")
    st.markdown("Import nutrition data from Excel spec sheets instead of images.")

    st.divider()

    # Instructions
    with st.expander("ℹ️ How to Use Excel Import", expanded=False):
        st.markdown("""
        ### Supported Formats

        The tool can automatically detect and import from:

        1. **Standard Nutrition Facts Table**
           - Column 1: Nutrient names
           - Column 2: Values
           - Column 3: % Daily Value (optional)

        2. **FDA Submission Format**
           - Common format used for regulatory submissions

        3. **Custom Internal Formats**
           - Auto-detection will attempt to parse

        ### Tips for Best Results

        - Use the first sheet in your workbook
        - Include clear labels (e.g., "Serving Size", "Total Fat")
        - Ensure values have units (g, mg, etc.)
        - Keep formatting simple (avoid merged cells)
        """)

    # File upload
    st.subheader("📤 Upload Excel File")

    excel_file = st.file_uploader(
        "Choose Excel file (.xlsx, .xls)",
        type=["xlsx", "xls"],
        key="excel_upload",
        help="Upload your nutrition spec sheet in Excel format"
    )

    if excel_file:
        st.info(f"📄 File: {excel_file.name} ({excel_file.size / 1024:.1f} KB)")

        if st.button("📥 Import Data", type="primary", use_container_width=True):
            with st.spinner("Importing from Excel..."):
                imported_data = import_from_excel(excel_file)

                if "error" in imported_data:
                    st.error(f"❌ Import failed: {imported_data.get('details')}")
                else:
                    st.success("✅ Data imported successfully!")
                    st.session_state.excel_imported_data = imported_data
                    st.rerun()

    # Display imported data
    if "excel_imported_data" in st.session_state:
        st.divider()
        st.subheader("✏️ Review Imported Data")

        imported_data = st.session_state.excel_imported_data

        # Show imported data in editor
        show_extraction_confidence(imported_data)

        st.divider()

        # Manual editing option
        if st.checkbox("Enable Manual Editing", value=False):
            edited_data = render_manual_editor(imported_data, key_prefix="excel_editor")
            st.session_state.excel_imported_data = edited_data

        # Run compliance checks
        st.divider()

        if st.button("✅ Run Compliance Checks", type="primary", use_container_width=True):
            from validators import run_compliance_checks
            import json

            with open("checklist_config.json", "r") as f:
                checklist_config = json.load(f)

            with st.spinner("Running compliance checks..."):
                compliance_results = run_compliance_checks(
                    st.session_state.excel_imported_data,
                    checklist_config
                )

                st.session_state.excel_compliance_results = compliance_results
                st.rerun()

        # Show results
        if "excel_compliance_results" in st.session_state:
            st.divider()

            from app import display_results
            display_results(
                st.session_state.excel_imported_data,
                st.session_state.excel_compliance_results
            )


def render_manual_editor_tab(product_type, extract_func):
    """Render manual correction interface tab"""
    st.header("✏️ Manual Data Editor")
    st.markdown("Review and correct AI-extracted nutrition data before validation.")

    st.divider()

    # Upload or use existing data
    data_source = st.radio(
        "Data Source",
        options=["Upload New File", "Use Previously Extracted Data"],
        horizontal=True
    )

    if data_source == "Upload New File":
        uploaded_file = st.file_uploader(
            "Upload nutrition label",
            type=["pdf", "png", "jpg", "jpeg"],
            key="editor_upload"
        )

        if uploaded_file:
            if st.button("📥 Extract Data", type="primary"):
                with st.spinner("Extracting data with GPT-4 Vision..."):
                    extracted_data = extract_func(uploaded_file, product_type)
                    st.session_state.editor_data = extracted_data
                    st.rerun()

    else:
        # Use existing data from session
        if "extracted_data" in st.session_state:
            st.session_state.editor_data = st.session_state.extracted_data
            st.info("✅ Using previously extracted data")
        else:
            st.warning("⚠️ No previously extracted data found. Please upload a file first.")

    # Show editor if data available
    if "editor_data" in st.session_state:
        st.divider()

        # Show confidence
        show_extraction_confidence(st.session_state.editor_data)

        st.divider()

        # Render editor
        edited_data = render_manual_editor(
            st.session_state.editor_data,
            key_prefix="main_editor"
        )

        # Update session state
        if f"main_editor_edited_data" in st.session_state:
            st.session_state.editor_data = st.session_state.main_editor_edited_data

        st.divider()

        # Run validation with edited data
        if st.button("✅ Validate with Edited Data", type="primary", use_container_width=True):
            from validators import run_compliance_checks
            import json

            with open("checklist_config.json", "r") as f:
                checklist_config = json.load(f)

            with st.spinner("Running compliance checks..."):
                compliance_results = run_compliance_checks(edited_data, checklist_config)
                st.session_state.editor_compliance_results = compliance_results
                st.rerun()

        # Show results
        if "editor_compliance_results" in st.session_state:
            st.divider()

            from app import display_results
            display_results(edited_data, st.session_state.editor_compliance_results)


def render_claims_validation_tab(product_type, extract_func):
    """Render claims validation tab"""
    st.header("🏆 Nutrition Claims Validator")
    st.markdown("Verify if your product qualifies for nutrition and health claims under FDA regulations.")

    st.divider()

    # Upload or use existing
    data_source = st.radio(
        "Data Source",
        options=["Upload New Label", "Use Previously Extracted Data"],
        horizontal=True,
        key="claims_data_source"
    )

    if data_source == "Upload New Label":
        uploaded_file = st.file_uploader(
            "Upload nutrition label",
            type=["pdf", "png", "jpg", "jpeg"],
            key="claims_upload"
        )

        if uploaded_file:
            if st.button("📥 Extract & Validate Claims", type="primary"):
                with st.spinner("Extracting data..."):
                    extracted_data = extract_func(uploaded_file, product_type)
                    st.session_state.claims_data = extracted_data

                with st.spinner("Validating claims..."):
                    claims_results = validate_all_claims(extracted_data)
                    st.session_state.claims_results = claims_results
                    st.rerun()

    else:
        if "extracted_data" in st.session_state:
            if st.button("🏆 Validate Claims", type="primary"):
                with st.spinner("Validating claims..."):
                    claims_results = validate_all_claims(st.session_state.extracted_data)
                    st.session_state.claims_results = claims_results
                    st.rerun()
        else:
            st.warning("⚠️ No data available. Please extract data first.")

    # Display results
    if "claims_results" in st.session_state:
        st.divider()
        display_claims_results(st.session_state.claims_results)


def display_claims_results(claims_results):
    """Display claims validation results"""
    st.header("🏆 Claims Validation Results")

    # Summary
    summary = claims_results.get("summary", {})

    col1, col2, col3 = st.columns(3)

    col1.metric("Valid Claims", summary.get("valid", 0), help="Claims your product qualifies for")
    col2.metric("Invalid Claims", summary.get("invalid", 0), help="Claims not met")
    col3.metric("Close to Qualifying", len(claims_results.get("suggestedClaims", [])), help="Almost qualifies")

    st.divider()

    # Valid claims
    valid_claims = claims_results.get("validClaims", [])
    if valid_claims:
        st.success(f"✅ **Your product qualifies for {len(valid_claims)} claim(s):**")

        for claim in valid_claims:
            with st.expander(f"✅ {claim.get('claim')}", expanded=False):
                col_a, col_b = st.columns(2)

                with col_a:
                    st.markdown("**Requirement:**")
                    st.info(claim.get("requirement"))

                with col_b:
                    st.markdown("**Your Product:**")
                    st.success(claim.get("actualValue"))

                st.caption(f"📖 {claim.get('cfr_reference')}")

    # Suggested claims (close to qualifying)
    suggested = claims_results.get("suggestedClaims", [])
    if suggested:
        st.warning(f"💡 **{len(suggested)} claim(s) you're close to qualifying for:**")

        for claim in suggested:
            with st.expander(f"💡 {claim.get('claim')} - Almost There!", expanded=True):
                st.warning(claim.get("message"))

                if claim.get("suggestion"):
                    st.info(f"**Suggestion:** {claim.get('suggestion')}")

    # Invalid claims
    invalid_claims = claims_results.get("invalidClaims", [])
    if invalid_claims:
        with st.expander(f"❌ Claims Not Met ({len(invalid_claims)})", expanded=False):
            for claim in invalid_claims[:10]:  # Show first 10
                st.markdown(f"**{claim.get('claim')}**: {claim.get('reason')}")
                st.caption(f"Requirement: {claim.get('requirement')}")
                st.divider()

    st.divider()

    # Export claims report
    st.subheader("📥 Export Claims Report")

    import json
    from datetime import datetime

    json_data = json.dumps(claims_results, indent=2)

    st.download_button(
        "📄 Download JSON Report",
        data=json_data,
        file_name=f"claims_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json",
        use_container_width=True
    )
