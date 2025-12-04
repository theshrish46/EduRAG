import re


def clean_syllabus_text(txt):
    # Handle None or empty string early
    if not txt or txt is None:
        return "", {}

    if not txt or not isinstance(txt, str):
        return "", {
            "course_info": "",
            "modules": [],
            "course_outcomes": "",
            "co_po_mapping": "",
        }

    original_txt = txt  # keep a backup for fallback

    try:
        # ---------------------------------------------------------------------
        # 1) CLEAN HEADERS (SAFE VERSION — NO OVERMATCHING)
        # ---------------------------------------------------------------------

        # Remove only specific headers, non-greedy, safer
        txt = re.sub(
            r"MASTER OF COMPUTER APPLICATIONS[\w\s]*", "", txt, flags=re.IGNORECASE
        )
        txt = re.sub(r"\(Autonomous Institution[^)]+\)", "", txt, flags=re.IGNORECASE)
        txt = re.sub(
            r"BANGALORE INSTUITE OF TECHNOLOGY.*?(?=Module|Semester|$)",
            "",
            txt,
            flags=re.IGNORECASE,
        )

        # Remove page numbers
        txt = re.sub(r"Page\s*\d+", "", txt, flags=re.IGNORECASE)

        # Normalize whitespace
        txt = re.sub(r"\s+", " ", txt).strip()

        # ---------------------------------------------------------------------
        # 2) EXTRACT COURSE METADATA
        # ---------------------------------------------------------------------

        course_pattern = r"(Semester.*?Credits \d+)"
        course_info = re.search(course_pattern, txt)
        course_info = course_info.group(1).strip() if course_info else ""

        # ---------------------------------------------------------------------
        # 3) EXTRACT MODULES SAFELY
        # ---------------------------------------------------------------------

        module_pattern = r"(Module[\s\-–_:]*(?:\d+|[IVXLCDM]+).*?)(?=(?:Module[\s\-–_:]*(?:\d+|[IVXLCDM]+)|Course outcome|Course Outcome|$))"
        modules = re.findall(module_pattern, txt, flags=re.IGNORECASE)

        clean_modules = []
        for m in modules:
            # Remove pedagogy sections only INSIDE module
            m = re.sub(
                r"Pedagogy\s*:.*?(?=Module-\d|Course outcome|$)",
                "",
                m,
                flags=re.IGNORECASE,
            )
            clean_modules.append(m.strip())

        # Fallback: if OCR failed and no modules detected, return raw text as single module
        if not clean_modules:
            clean_modules = [txt]

        # ---------------------------------------------------------------------
        # 4) EXTRACT COURSE OUTCOMES
        # ---------------------------------------------------------------------

        co_pattern = r"(Course outcome.*?)(?=Mapping|$)"
        co_section = re.search(co_pattern, txt, flags=re.IGNORECASE)
        co_section = co_section.group(1).strip() if co_section else ""

        # ---------------------------------------------------------------------
        # 5) EXTRACT CO-PO MAPPING
        # ---------------------------------------------------------------------

        po_pattern = r"(Mapping of COS and POs.*)"
        po_section = re.search(po_pattern, txt, flags=re.IGNORECASE)
        po_section = po_section.group(1).strip() if po_section else ""

        # ---------------------------------------------------------------------
        # 6) STRUCTURE (UNCHANGED)
        # ---------------------------------------------------------------------
        structured = {
            "course_info": course_info,
            "modules": clean_modules,
            "course_outcomes": co_section,
            "co_po_mapping": po_section,
        }

        # ---------------------------------------------------------------------
        # 7) CLEANED STRING (YOUR FORMAT — UNCHANGED)
        # ---------------------------------------------------------------------
        cleaned_string = "\n".join(
            [
                str(course_info),
                str(clean_modules),  # FIX: previously used wrong variable
                str(co_section),
                str(po_section),
            ]
        )

        return cleaned_string, structured

    except Exception as e:
        # FAILSAFE: return raw text as fallback, avoid pipeline crash
        return original_txt, {
            "course_info": "",
            "modules": [original_txt],
            "course_outcomes": "",
            "co_po_mapping": "",
            "error": str(e),
        }
