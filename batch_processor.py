"""
Batch Processing Module
Process multiple nutrition labels simultaneously
"""

import streamlit as st
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
from datetime import datetime
import json


def process_batch(files, product_type, extract_func, validate_func, checklist_config):
    """
    Process multiple files in batch

    Args:
        files: List of uploaded files
        product_type: Product type for RACC validation
        extract_func: Function to extract data from files
        validate_func: Function to validate compliance
        checklist_config: Checklist configuration

    Returns:
        list: Results for each file
    """
    results = []

    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()

    total_files = len(files)

    # Process files (sequentially to avoid API rate limits)
    for idx, file in enumerate(files):
        status_text.text(f"Processing {idx + 1}/{total_files}: {file.name}")

        try:
            # Extract data
            extracted_data = extract_func(file, product_type)

            # Run compliance checks
            compliance_results = validate_func(extracted_data, checklist_config)

            # Store result
            results.append({
                "filename": file.name,
                "status": "SUCCESS",
                "extracted_data": extracted_data,
                "compliance_results": compliance_results,
                "score": compliance_results.get("overallScore", 0),
                "passed": compliance_results.get("passed", 0),
                "failed": compliance_results.get("failed", 0),
                "warnings": compliance_results.get("warnings", 0)
            })

        except Exception as e:
            # Handle errors
            results.append({
                "filename": file.name,
                "status": "FAILED",
                "error": str(e),
                "score": 0,
                "passed": 0,
                "failed": 0,
                "warnings": 0
            })

        # Update progress
        progress_bar.progress((idx + 1) / total_files)

    status_text.text(f"✅ Completed processing {total_files} files")

    return results


def process_batch_comparison(spec_files, pkg_files, product_type, extract_func, compare_func, tolerance_settings=None):
    """
    Process batch comparison of spec sheets vs packaging labels

    Args:
        spec_files: List of spec sheet files
        pkg_files: List of packaging files (same order as spec_files)
        product_type: Product type
        extract_func: Extraction function
        compare_func: Comparison function
        tolerance_settings: Tolerance configuration

    Returns:
        list: Comparison results for each pair
    """
    if len(spec_files) != len(pkg_files):
        st.error("Number of spec files must match number of packaging files")
        return []

    results = []
    progress_bar = st.progress(0)
    status_text = st.empty()

    total_pairs = len(spec_files)

    for idx, (spec_file, pkg_file) in enumerate(zip(spec_files, pkg_files)):
        status_text.text(f"Comparing {idx + 1}/{total_pairs}: {spec_file.name} vs {pkg_file.name}")

        try:
            # Extract from both files
            spec_data = extract_func(spec_file, product_type)
            pkg_data = extract_func(pkg_file, product_type)

            # Compare
            comparison = compare_func(spec_data, pkg_data, tolerance_settings)

            # Store result
            results.append({
                "spec_filename": spec_file.name,
                "pkg_filename": pkg_file.name,
                "status": "SUCCESS",
                "match_score": comparison.get("matchScore", 0),
                "overall_match": comparison.get("overallMatch", False),
                "critical_mismatches": len(comparison.get("criticalMismatches", [])),
                "minor_differences": len(comparison.get("minorDifferences", [])),
                "comparison_results": comparison
            })

        except Exception as e:
            results.append({
                "spec_filename": spec_file.name,
                "pkg_filename": pkg_file.name,
                "status": "FAILED",
                "error": str(e),
                "match_score": 0,
                "overall_match": False
            })

        progress_bar.progress((idx + 1) / total_pairs)

    status_text.text(f"✅ Completed {total_pairs} comparisons")

    return results


def create_batch_summary_dataframe(batch_results):
    """
    Create summary DataFrame from batch results

    Args:
        batch_results: List of batch processing results

    Returns:
        pandas.DataFrame: Summary table
    """
    summary_data = []

    for result in batch_results:
        summary_data.append({
            "Filename": result.get("filename", "N/A"),
            "Status": result.get("status", "UNKNOWN"),
            "Score": f"{result.get('score', 0)}%",
            "Passed": result.get("passed", 0),
            "Failed": result.get("failed", 0),
            "Warnings": result.get("warnings", 0),
            "Error": result.get("error", "")
        })

    return pd.DataFrame(summary_data)


def create_comparison_summary_dataframe(comparison_results):
    """
    Create summary DataFrame from comparison results

    Args:
        comparison_results: List of comparison results

    Returns:
        pandas.DataFrame: Summary table
    """
    summary_data = []

    for result in comparison_results:
        summary_data.append({
            "Spec File": result.get("spec_filename", "N/A"),
            "Package File": result.get("pkg_filename", "N/A"),
            "Status": result.get("status", "UNKNOWN"),
            "Match Score": f"{result.get('match_score', 0)}%",
            "Overall Match": "✅ PASS" if result.get("overall_match") else "❌ FAIL",
            "Critical Issues": result.get("critical_mismatches", 0),
            "Minor Issues": result.get("minor_differences", 0),
            "Error": result.get("error", "")
        })

    return pd.DataFrame(summary_data)


def export_batch_results_to_excel(batch_results, comparison_mode=False):
    """
    Export batch results to Excel file

    Args:
        batch_results: List of results
        comparison_mode: Whether this is comparison results

    Returns:
        bytes: Excel file bytes
    """
    from io import BytesIO
    import xlsxwriter

    output = BytesIO()

    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        workbook = writer.book

        # Define formats
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#D3D3D3',
            'border': 1
        })

        pass_format = workbook.add_format({
            'bg_color': '#90EE90',
            'border': 1
        })

        fail_format = workbook.add_format({
            'bg_color': '#FFB6C1',
            'border': 1
        })

        # Summary sheet
        if comparison_mode:
            summary_df = create_comparison_summary_dataframe(batch_results)
        else:
            summary_df = create_batch_summary_dataframe(batch_results)

        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        # Format summary sheet
        worksheet = writer.sheets['Summary']
        worksheet.set_column('A:A', 30)  # Filename column width
        worksheet.set_column('B:H', 15)  # Other columns

        # Detailed results for each file
        for idx, result in enumerate(batch_results, 1):
            if result.get("status") != "SUCCESS":
                continue

            sheet_name = f"File_{idx}"[:31]  # Excel sheet name limit

            if comparison_mode:
                # Comparison detailed results
                comp_results = result.get("comparison_results", {})
                create_comparison_detail_sheet(writer, sheet_name, comp_results)
            else:
                # Compliance detailed results
                compliance = result.get("compliance_results", {})
                create_compliance_detail_sheet(writer, sheet_name, compliance)

    excel_bytes = output.getvalue()
    output.close()

    return excel_bytes


def create_compliance_detail_sheet(writer, sheet_name, compliance_results):
    """Create detailed compliance results sheet"""
    checks = compliance_results.get("checks", [])

    detail_data = []
    for check in checks:
        detail_data.append({
            "Category": check.get("category", ""),
            "Requirement": check.get("requirement", ""),
            "Status": check.get("status", ""),
            "Details": check.get("details", ""),
            "Severity": check.get("severity", ""),
            "CFR Reference": check.get("cfr_reference", "")
        })

    df = pd.DataFrame(detail_data)
    df.to_excel(writer, sheet_name=sheet_name, index=False)

    # Format
    worksheet = writer.sheets[sheet_name]
    worksheet.set_column('A:A', 25)  # Category
    worksheet.set_column('B:B', 50)  # Requirement
    worksheet.set_column('C:C', 10)  # Status
    worksheet.set_column('D:D', 50)  # Details
    worksheet.set_column('E:E', 15)  # Severity
    worksheet.set_column('F:F', 20)  # CFR Reference


def create_comparison_detail_sheet(writer, sheet_name, comparison_results):
    """Create detailed comparison results sheet"""
    all_diffs = []

    # Critical mismatches
    for diff in comparison_results.get("criticalMismatches", []):
        all_diffs.append({
            "Severity": "CRITICAL",
            "Field": diff.get("field", ""),
            "Spec": diff.get("spec", ""),
            "Packaging": diff.get("packaging", ""),
            "Difference": diff.get("difference", ""),
            "Message": diff.get("message", "")
        })

    # Minor differences
    for diff in comparison_results.get("minorDifferences", []):
        all_diffs.append({
            "Severity": "MINOR",
            "Field": diff.get("field", ""),
            "Spec": diff.get("spec", ""),
            "Packaging": diff.get("packaging", ""),
            "Difference": diff.get("difference", ""),
            "Message": diff.get("message", "")
        })

    df = pd.DataFrame(all_diffs)
    df.to_excel(writer, sheet_name=sheet_name, index=False)

    # Format
    worksheet = writer.sheets[sheet_name]
    worksheet.set_column('A:A', 12)  # Severity
    worksheet.set_column('B:B', 25)  # Field
    worksheet.set_column('C:D', 20)  # Spec/Packaging
    worksheet.set_column('E:E', 15)  # Difference
    worksheet.set_column('F:F', 50)  # Message


def render_batch_results(batch_results, comparison_mode=False):
    """
    Render batch results in Streamlit UI

    Args:
        batch_results: List of results
        comparison_mode: Whether this is comparison results
    """
    st.header("📊 Batch Processing Results")

    # Summary metrics
    total = len(batch_results)
    successful = sum(1 for r in batch_results if r.get("status") == "SUCCESS")
    failed = total - successful

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Files", total)
    col2.metric("Successful", successful, delta=f"{(successful/total)*100:.0f}%" if total > 0 else "0%")
    col3.metric("Failed", failed, delta=f"-{(failed/total)*100:.0f}%" if total > 0 and failed > 0 else "0%", delta_color="inverse")

    if comparison_mode:
        passed = sum(1 for r in batch_results if r.get("overall_match"))
        col4.metric("Passed Comparison", passed, delta=f"{(passed/successful)*100:.0f}%" if successful > 0 else "0%")
    else:
        avg_score = sum(r.get("score", 0) for r in batch_results) / total if total > 0 else 0
        col4.metric("Average Score", f"{avg_score:.0f}%")

    st.divider()

    # Summary table
    st.subheader("📋 Summary Table")

    if comparison_mode:
        summary_df = create_comparison_summary_dataframe(batch_results)
    else:
        summary_df = create_batch_summary_dataframe(batch_results)

    st.dataframe(summary_df, use_container_width=True)

    st.divider()

    # Export options
    st.subheader("📥 Export Results")

    col_a, col_b = st.columns(2)

    with col_a:
        # Excel export
        excel_bytes = export_batch_results_to_excel(batch_results, comparison_mode)

        st.download_button(
            "📊 Download Excel Report",
            data=excel_bytes,
            file_name=f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    with col_b:
        # JSON export
        json_data = json.dumps(batch_results, indent=2)

        st.download_button(
            "📄 Download JSON Data",
            data=json_data,
            file_name=f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )

    st.divider()

    # Detailed results
    st.subheader("📝 Detailed Results")

    for idx, result in enumerate(batch_results, 1):
        filename = result.get("filename") or f"{result.get('spec_filename')} vs {result.get('pkg_filename')}"

        if result.get("status") == "FAILED":
            with st.expander(f"❌ {idx}. {filename} - FAILED", expanded=False):
                st.error(f"Error: {result.get('error', 'Unknown error')}")
        else:
            score = result.get("score") or result.get("match_score", 0)
            status_emoji = "✅" if score >= 90 else "⚠️" if score >= 70 else "❌"

            with st.expander(f"{status_emoji} {idx}. {filename} - Score: {score}%", expanded=False):
                if comparison_mode:
                    # Show comparison details
                    comp_results = result.get("comparison_results", {})
                    st.metric("Match Score", f"{comp_results.get('matchScore', 0)}%")

                    critical = comp_results.get("criticalMismatches", [])
                    if critical:
                        st.error(f"❌ {len(critical)} Critical Mismatch(es)")
                        for diff in critical[:3]:  # Show first 3
                            st.text(f"• {diff.get('field')}: {diff.get('message')}")

                    minor = comp_results.get("minorDifferences", [])
                    if minor:
                        st.warning(f"⚠️ {len(minor)} Minor Difference(s)")
                else:
                    # Show compliance details
                    compliance = result.get("compliance_results", {})

                    col_x, col_y, col_z = st.columns(3)
                    col_x.metric("Passed", compliance.get("passed", 0))
                    col_y.metric("Failed", compliance.get("failed", 0))
                    col_z.metric("Warnings", compliance.get("warnings", 0))

                    # Show failed checks
                    failed_checks = [c for c in compliance.get("checks", []) if c.get("status") == "FAIL"]
                    if failed_checks:
                        st.error(f"❌ {len(failed_checks)} Failed Check(s)")
                        for check in failed_checks[:3]:  # Show first 3
                            st.text(f"• {check.get('requirement')}")
