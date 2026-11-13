# pyright: reportMissingImports=false
# type: ignore
"""
Blood Test Report Parser & Biomarker Intelligence Engine (Module 4B)
--------------------------------------------------------------------
Extracts digital text from uploaded clinical laboratory reports (PDF or images),
identifies key routine biomarkers using fuzzy alias matching and regex pattern
extraction, compares values against clinical reference boundaries, flags out-of-range
indicators, and generates educational diagnostic explanations.
"""

import os
import re

try:
    import pymupdf  # type: ignore
except Exception:
    try:
        import fitz as pymupdf  # type: ignore
    except Exception:
        pymupdf = None

from app.models.blood_report_data import BIOMARKER_DATABASE

class BloodReportParser:
    """Clinical parser for laboratory test reports."""

    @staticmethod
    def extract_text_from_file(file_path):
        """
        Extracts raw textual content from uploaded file.
        Supports PDF files via PyMuPDF.
        """
        if not os.path.exists(file_path):
            return ""

        ext = os.path.splitext(file_path)[1].lower()
        extracted_text = ""

        if ext == ".pdf":
            if pymupdf is not None:
                try:
                    doc = pymupdf.open(file_path)
                    for page in doc:
                        page_text = page.get_text("text")
                        if page_text:
                            extracted_text += page_text + "\n"
                    doc.close()
                except Exception as e:
                    print(f"Notice: PyMuPDF failed to read PDF: {e}")
            else:
                print("Notice: PyMuPDF is not installed or available.")
        else:
            # For image files or plain text files
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    extracted_text = f.read()
            except Exception:
                extracted_text = ""

        return extracted_text.strip()

    @classmethod
    def parse_file(cls, file_path):
        """Extracts text and parses biomarkers directly from a PDF or image file path."""
        raw_text = cls.extract_text_from_file(file_path)
        return cls.parse_report_text(raw_text)

    @classmethod
    def parse_report_text(cls, raw_text):
        """
        Scans extracted raw text for recognized biomarkers, values, and reference ranges.
        Returns structured analysis report.
        """
        if not raw_text or len(raw_text.strip()) < 10:
            return cls._generate_fallback_or_empty_result(
                "No readable text could be extracted from the document. Please ensure the uploaded file is a clear digital laboratory report."
            )

        extracted_biomarkers = []
        lines = [line.strip() for line in raw_text.splitlines() if line.strip()]

        # Iterate over known biomarkers in clinical knowledge base
        for bio_key, bio_info in BIOMARKER_DATABASE.items():
            matched = cls._find_biomarker_in_lines(bio_key, bio_info, lines, raw_text)
            if matched:
                extracted_biomarkers.append(matched)

        if not extracted_biomarkers:
            # Fallback for structured testing or unstructured documents
            return cls._generate_fallback_or_empty_result(
                "No standard routine hematology or biochemistry biomarkers were detected in the uploaded file.",
                raw_text=raw_text
            )

        return cls._synthesize_report_summary(extracted_biomarkers, raw_text)

    @classmethod
    def _find_biomarker_in_lines(cls, bio_key, bio_info, lines, full_text):
        """
        Searches lines for biomarker aliases and nearby numeric values.
        """
        aliases = bio_info["aliases"]

        for line in lines:
            line_lower = line.lower()
            for alias in aliases:
                # Use word boundary or substring match
                pattern = r"(?i)\b" + re.escape(alias) + r"\b"
                if re.search(pattern, line_lower):
                    # Found alias on this line, search for numeric value
                    val = cls._extract_numeric_from_line(line, alias)
                    if val is not None:
                        return cls._evaluate_biomarker_value(bio_key, bio_info, val, line)

        # If not found per line, attempt multi-line regex across the full text
        for alias in aliases:
            rgx = re.compile(
                r"(?i)\b" + re.escape(alias) + r"[\s:=-]+([0-9]+[.,]?[0-9]*)",
                re.MULTILINE
            )
            m = rgx.search(full_text)
            if m:
                try:
                    num_str = m.group(1).replace(",", "")
                    val = float(num_str)
                    return cls._evaluate_biomarker_value(bio_key, bio_info, val, m.group(0))
                except ValueError:
                    pass

        return None

    @classmethod
    def _extract_numeric_from_line(cls, line, alias_matched):
        """
        Extracts the primary measured number from a line containing a biomarker name.
        Slices the line to only search for numbers AFTER the matched alias name.
        Avoids reading digits from the test name itself (e.g. HbA1c) or dates.
        """
        lower_line = line.lower()
        alias_pos = lower_line.find(alias_matched.lower())
        
        if alias_pos != -1:
            search_text = line[alias_pos + len(alias_matched):]
        else:
            search_text = line

        # Look for numbers with optional decimal point (or comma)
        numbers = re.findall(r"([0-9]+(?:\.[0-9]+)?)", search_text.replace(",", ""))
        if not numbers:
            return None

        # Filter out common 4-digit years (e.g. 2024, 2025, 2026)
        valid_nums = []
        for n_str in numbers:
            try:
                flt = float(n_str)
                if flt in (2024.0, 2025.0, 2026.0, 2027.0):
                    continue
                valid_nums.append(flt)
            except ValueError:
                continue

        if valid_nums:
            return valid_nums[0]

        return None

    @classmethod
    def _evaluate_biomarker_value(cls, bio_key, bio_info, value, source_line):
        """
        Evaluates a measured biomarker value against reference ranges.
        """
        ref_min = bio_info["ref_min"]
        ref_max = bio_info["ref_max"]
        crit_low = bio_info.get("critical_low", -float("inf"))
        crit_high = bio_info.get("critical_high", float("inf"))
        unit = bio_info["default_unit"]

        if value <= crit_low:
            status = "CRITICAL_LOW"
            badge_class = "bg-danger text-white"
            interpretation = bio_info["interpretations"].get("CRITICAL_LOW", bio_info["interpretations"]["LOW"])
        elif value >= crit_high:
            status = "CRITICAL_HIGH"
            badge_class = "bg-danger text-white"
            interpretation = bio_info["interpretations"].get("CRITICAL_HIGH", bio_info["interpretations"]["HIGH"])
        elif value < ref_min:
            status = "LOW"
            badge_class = "bg-warning text-dark"
            interpretation = bio_info["interpretations"]["LOW"]
        elif value > ref_max:
            status = "HIGH"
            badge_class = "bg-danger text-white"
            interpretation = bio_info["interpretations"]["HIGH"]
        else:
            status = "NORMAL"
            badge_class = "bg-success text-white"
            interpretation = bio_info["interpretations"]["NORMAL"]

        return {
            "key": bio_key,
            "name": bio_info["display_name"],
            "category": bio_info["category"],
            "measured_value": value,
            "unit": unit,
            "ref_range": f"{ref_min} - {ref_max} {unit}",
            "ref_min": ref_min,
            "ref_max": ref_max,
            "status": status,
            "badge_class": badge_class,
            "interpretation": interpretation,
            "source_snippet": source_line[:80]
        }

    @classmethod
    def _synthesize_report_summary(cls, biomarkers, raw_text):
        """
        Synthesizes summary statistics and high-level clinical guidance.
        """
        total = len(biomarkers)
        normal_list = [b for b in biomarkers if b["status"] == "NORMAL"]
        high_list = [b for b in biomarkers if b["status"] in ("HIGH", "CRITICAL_HIGH")]
        low_list = [b for b in biomarkers if b["status"] in ("LOW", "CRITICAL_LOW")]
        critical_list = [b for b in biomarkers if "CRITICAL" in b["status"]]

        normal_count = len(normal_list)
        abnormal_count = len(high_list) + len(low_list)
        critical_count = len(critical_list)

        if critical_count > 0:
            overall_status = "CRITICAL CLINICAL OUTLIERS DETECTED"
            overall_badge = "bg-danger text-white"
            summary_statement = (
                f"Critical physiological outliers detected ({critical_count} critical parameters: "
                f"{', '.join([b['name'] for b in critical_list])}). "
                "These values represent significant deviations from homeostatic norms. "
                "Immediate consultation with a physician or emergency hospital evaluation is strongly recommended."
            )
            urgency = "HIGH / URGENT MEDICAL ATTENTION"
        elif abnormal_count > 0:
            overall_status = "OUT-OF-RANGE PARAMETERS IDENTIFIED"
            overall_badge = "bg-warning text-dark"
            summary_statement = (
                f"Evaluation completed for {total} biomarkers. Identified {abnormal_count} out-of-range parameters "
                f"({len(high_list)} elevated, {len(low_list)} decreased), while {normal_count} parameters are in normal physiological range. "
                "Discuss these findings with your prescribing clinician or primary care doctor for diagnostic correlation."
            )
            urgency = "MODERATE / OUTPATIENT CLINICAL FOLLOW-UP"
        else:
            overall_status = "ALL EVALUATED BIOMARKERS WITHIN NORMAL RANGE"
            overall_badge = "bg-success text-white"
            summary_statement = (
                f"All {total} extracted biomarkers fall comfortably within standard laboratory reference ranges. "
                "Continue routine preventative health screening, balanced nutrition, and healthy physical activity."
            )
            urgency = "ROUTINE / OPTIMAL BASELINE"

        recommendations = []
        if any("glucose" in b["key"] or "hba1c" in b["key"] for b in high_list):
            recommendations.append("Glycemic markers are elevated. Consider an oral glucose tolerance test (OGTT) or endocrinology review, and monitor carbohydrate intake.")
        if any(b["key"] == "hemoglobin" for b in low_list):
            recommendations.append("Low hemoglobin suggests anemia. Serum ferritin, iron profile, vitamin B12, and peripheral blood smear review are recommended to evaluate etiology.")
        if any(b["key"] == "creatinine" for b in high_list):
            recommendations.append("Elevated serum creatinine indicates potential renal strain. Ensure adequate hydration, review nephrotoxic medications with your doctor, and recheck renal function.")
        if any("cholesterol" in b["key"] or "triglycerides" in b["key"] for b in high_list):
            recommendations.append("Lipid panel abnormalities indicate cardiovascular risk. Heart-healthy Mediterranean-style diet, aerobic exercise, and clinical ASCVD scoring are advised.")
        if not recommendations:
            recommendations.append("Maintain routine annual check-ups, stay hydrated, and continue balanced dietary habits.")

        return {
            "status": "success",
            "total_extracted": total,
            "normal_count": normal_count,
            "abnormal_count": abnormal_count,
            "critical_count": critical_count,
            "overall_status": overall_status,
            "overall_badge": overall_badge,
            "urgency": urgency,
            "summary_statement": summary_statement,
            "recommendations": recommendations,
            "biomarkers": biomarkers,
            "raw_text_preview": raw_text[:500] if raw_text else "",
            "disclaimer": (
                "Automated laboratory document analysis is designed for patient education and informational reference only. "
                "Biomarker reference ranges vary between individual testing laboratories, instruments, patient age, and sex. "
                "This report does not provide a definitive medical diagnosis and must be interpreted by a qualified healthcare professional."
            )
        }

    @classmethod
    def _generate_fallback_or_empty_result(cls, error_msg, raw_text=""):
        """Generates graceful fallback response when no biomarkers are detected."""
        return {
            "status": "warning",
            "total_extracted": 0,
            "normal_count": 0,
            "abnormal_count": 0,
            "critical_count": 0,
            "overall_status": "UNSTRUCTURED OR UNRECOGNIZED LABORATORY DOCUMENT",
            "overall_badge": "bg-secondary text-white",
            "urgency": "INDETERMINATE",
            "summary_statement": error_msg,
            "recommendations": [
                "Ensure your uploaded report contains clear text identifying standard biomarkers (e.g., Hemoglobin, Fasting Glucose, WBC, Platelets, Creatinine).",
                "For scanned paper copies, upload a clean, high-contrast digital PDF or document scan."
            ],
            "biomarkers": [],
            "raw_text_preview": raw_text[:500] if raw_text else "",
            "disclaimer": (
                "BioHealth AI laboratory report parser extracts values for routine standard parameters. "
                "Always present official printed laboratory reports directly to your physician for clinical decisions."
            )
        }
