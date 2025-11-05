"""
FDA Nutrition Label Compliance Checker
Streamlit App for Internal Use
"""

import streamlit as st
import json
from pathlib import Path
from dotenv import load_dotenv
import os

# Import our modules
from extractor import extract_nutrition_data
from validators import run_compliance_checks
from report_generator import generate_pdf_report
from app_comparison import render_comparison_tab

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="FDA Nutrition Label Compliance Checker",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load checklist config
@st.cache_data
def load_checklist_config():
    with open("checklist_config.json", "r") as f:
        return json.load(f)

def main():
    st.title("✅ FDA Nutrition Label Compliance Checker")
    st.markdown("**For Plant-Based Meat & Dairy Products** | 21 CFR 101.9, 101.4, FALCPA")

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")

        # Product type selection
        product_type = st.selectbox(
            "Product Type",
            [
                "plant-based-deli-slices",
                "plant-based-burgers",
                "plant-based-sausages",
                "plant-based-ground",
                "plant-based-milk",
                "plant-based-cheese",
                "plant-based-yogurt",
                "other"
            ],
            help="Select the type of product for RACC validation"
        )

        st.divider()

        # API key check
        if os.getenv("OPENAI_API_KEY"):
            st.success("✅ OpenAI API Key Loaded")
        else:
            st.error("❌ OpenAI API Key Missing")
            st.info("Add your API key to `.env` file:\n```\nOPENAI_API_KEY=sk-...\n```")

        st.divider()

        st.markdown("""
        ### About
        This tool validates nutrition labels against FDA requirements.

        **Upload**:
        - PDF, PNG, JPG formats
        - Max 10MB per file

        **Checks**:
        - Format compliance
        - RACC validation
        - Rounding rules
        - Allergen declarations
        - CFR references
        """)

    # Main content
    tab1, tab2, tab3, tab4 = st.tabs(["📤 Upload & Analyze", "📊 Spec vs Package", "📋 Checklist Reference", "ℹ️ Help"])

    with tab1:
        st.header("Upload Nutrition Label or Spec Sheet")

        # File uploader
        uploaded_file = st.file_uploader(
            "Choose a file (PDF, PNG, JPG)",
            type=["pdf", "png", "jpg", "jpeg"],
            help="Upload a nutrition facts label image or spec sheet PDF"
        )

        if uploaded_file:
            # Display uploaded file
            col1, col2 = st.columns([1, 1])

            with col1:
                st.subheader("📄 Uploaded File")
                st.info(f"**Filename**: {uploaded_file.name}")
                st.info(f"**Size**: {uploaded_file.size / 1024:.1f} KB")

                # Display image preview
                if uploaded_file.type.startswith("image"):
                    st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

            with col2:
                st.subheader("🔍 Analysis")

                # Analyze button
                if st.button("🚀 Analyze Label", type="primary", use_container_width=True):
                    with st.spinner("Extracting data with GPT-4 Vision..."):
                        # Extract nutrition data
                        extracted_data = extract_nutrition_data(uploaded_file, product_type)

                        # Store in session state
                        st.session_state.extracted_data = extracted_data
                        st.session_state.product_type = product_type

                    with st.spinner("Running compliance checks..."):
                        # Run compliance checks
                        checklist = load_checklist_config()
                        compliance_results = run_compliance_checks(extracted_data, checklist)

                        # Store in session state
                        st.session_state.compliance_results = compliance_results

                    st.success("✅ Analysis Complete!")
                    st.rerun()

        # Display results if available
        if "compliance_results" in st.session_state and "extracted_data" in st.session_state:
            st.divider()
            display_results(
                st.session_state.extracted_data,
                st.session_state.compliance_results
            )

    with tab2:
        # Spec vs Package Comparison
        render_comparison_tab(product_type)

    with tab3:
        st.header("📋 FDA Compliance Checklist Reference")
        display_checklist_reference(load_checklist_config())

    with tab4:
        st.header("ℹ️ Help & Instructions")
        display_help()

def display_results(extracted_data, compliance_results):
    """Display compliance check results"""
    st.header("📊 Compliance Results")

    # Overall score
    total_checks = len(compliance_results["checks"])
    passed = sum(1 for c in compliance_results["checks"] if c["status"] == "PASS")
    failed = sum(1 for c in compliance_results["checks"] if c["status"] == "FAIL")
    warnings = sum(1 for c in compliance_results["checks"] if c["status"] == "WARNING")

    score = int((passed / total_checks) * 100) if total_checks > 0 else 0

    # Score metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Overall Score", f"{score}%", help="Percentage of checks passed")
    col2.metric("✅ Passed", passed, help="Checks that passed")
    col3.metric("❌ Failed", failed, help="Critical failures", delta_color="inverse")
    col4.metric("⚠️ Warnings", warnings, help="Non-critical issues")

    # Export button
    if st.button("📥 Download PDF Report", use_container_width=True):
        pdf_bytes = generate_pdf_report(extracted_data, compliance_results)
        st.download_button(
            "⬇️ Download Report",
            data=pdf_bytes,
            file_name="compliance_report.pdf",
            mime="application/pdf"
        )

    st.divider()

    # Detailed results by category
    st.subheader("📝 Detailed Compliance Checks")

    # Group by category
    categories = {}
    for check in compliance_results["checks"]:
        cat = check["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(check)

    # Display each category
    for category_name, checks in categories.items():
        with st.expander(f"**{category_name}** ({len([c for c in checks if c['status'] == 'PASS'])}/{len(checks)} passed)", expanded=True):
            for check in checks:
                status_icon = {
                    "PASS": "✅",
                    "FAIL": "❌",
                    "WARNING": "⚠️",
                    "MANUAL": "👁️"
                }.get(check["status"], "❓")

                status_color = {
                    "PASS": "green",
                    "FAIL": "red",
                    "WARNING": "orange",
                    "MANUAL": "blue"
                }.get(check["status"], "gray")

                st.markdown(f"{status_icon} **{check['requirement']}**")

                if check.get("details"):
                    st.info(check["details"])

                if check.get("cfr_reference"):
                    st.caption(f"📖 CFR Reference: {check['cfr_reference']}")

                st.divider()

    st.divider()

    # Extracted data
    st.subheader("📋 Extracted Nutrition Data")

    col1, col2 = st.columns(2)

    with col1:
        st.json(extracted_data.get("servingInfo", {}))

    with col2:
        st.json(extracted_data.get("nutrients", {}))

def display_checklist_reference(checklist):
    """Display the full checklist as reference"""
    for category in checklist["categories"]:
        with st.expander(f"**{category['name']}** - {category.get('cfr_reference', 'N/A')}", expanded=False):
            st.markdown(f"**CFR Reference**: {category.get('cfr_reference', 'Not specified')}")
            st.divider()

            for check in category["checks"]:
                st.markdown(f"✓ {check['requirement']}")
                if check.get("severity"):
                    st.caption(f"Severity: {check['severity']}")

def display_help():
    """Display help information"""
    st.markdown("""
    ## How to Use

    1. **Select Product Type** in the sidebar
    2. **Upload** your nutrition label (PDF or image)
    3. **Click Analyze** to run compliance checks
    4. **Review Results** and download PDF report

    ## What Gets Checked

    - ✅ Nutrition Facts format (single/dual column)
    - ✅ Serving size RACC compliance
    - ✅ Calorie declaration
    - ✅ Nutrient order and formatting
    - ✅ % Daily Value calculations
    - ✅ Rounding rules (FDA requirements)
    - ✅ Ingredient list format
    - ✅ Allergen declarations (Top 9)
    - ✅ Required label elements

    ## Compliance Levels

    - **PASS** ✅ - Meets FDA requirements
    - **FAIL** ❌ - Does not meet requirements (critical)
    - **WARNING** ⚠️ - Potential issue (review recommended)
    - **MANUAL** 👁️ - Requires human verification

    ## CFR References

    - **21 CFR 101.9** - Nutrition labeling
    - **21 CFR 101.4** - Ingredient labeling
    - **FALCPA** - Food allergen labeling

    ## Need Help?

    - Check that your `.env` file has a valid OpenAI API key
    - Ensure uploaded images are clear and readable
    - For best results, use high-resolution images (300+ DPI)

    ## Limitations

    ⚠️ **This tool is for internal guidance only. It does not constitute legal or regulatory advice.**

    - AI-based extraction may have errors
    - Always verify results manually
    - Consult with regulatory experts for final approval
    """)

if __name__ == "__main__":
    main()
