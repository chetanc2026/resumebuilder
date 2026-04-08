from fpdf import FPDF
import re
import textwrap


def _sanitize_pdf_text(text):
    """Convert common Unicode punctuation to PDF core-font-safe text."""
    replacements = {
        "\u2013": "-",   # en dash
        "\u2014": "-",   # em dash
        "\u2018": "'",   # left single quote
        "\u2019": "'",   # right single quote
        "\u201c": '"',   # left double quote
        "\u201d": '"',   # right double quote
        "\u2026": "...", # ellipsis
        "\u00a0": " ",   # non-breaking space
        "\u2022": "-",   # bullet
        "\u25cf": "-",   # black circle
        "\u25aa": "-",   # small square
    }

    for src, dst in replacements.items():
        text = text.replace(src, dst)

    # Remove common markdown wrappers to avoid noisy PDF output.
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"__(.*?)__", r"\1", text)
    text = text.replace("`", "")

    # Keep only characters supported by core fonts.
    return text.encode("latin-1", errors="ignore").decode("latin-1")


def _clean_label(text):
    text = _sanitize_pdf_text(text or "").strip()
    text = re.sub(r"^[\s*#_+|:;,.\-]+", "", text)
    text = re.sub(r"[\s*#_+|:;,.\-]+$", "", text)
    return re.sub(r"\s+", " ", text).strip()


def _normalize_line(line):
    line = _sanitize_pdf_text(line or "")
    line = line.replace("\t", " ")
    line = re.sub(r"\s+", " ", line)
    return line.strip()


def _is_section_header(line):
    normalized = _clean_label(line)
    if not normalized:
        return False

    known_sections = {
        "summary",
        "professional summary",
        "objective",
        "skills",
        "technical skills",
        "core competencies",
        "experience",
        "professional experience",
        "work experience",
        "internship experience",
        "education",
        "projects",
        "certifications",
        "achievements",
        "awards",
        "activities",
        "volunteering",
        "leadership",
        "languages",
        "references",
    }

    lower = normalized.lower()
    if lower in known_sections:
        return True

    return (
        normalized.isupper()
        and len(normalized) < 50
        and len(normalized.split()) <= 4
    )


def _detect_candidate_profile(resume_text):
    lowered = resume_text.lower()

    fresher_markers = (
        "fresher",
        "recent graduate",
        "new graduate",
        "student",
        "intern",
        "entry level",
        "entry-level",
    )
    if any(marker in lowered for marker in fresher_markers):
        return "fresher"

    year_mentions = [int(match) for match in re.findall(r"(\d{1,2})\+?\s+years?", lowered)]
    if year_mentions and max(year_mentions) >= 2:
        return "experienced"

    date_ranges = re.findall(r"(19\d{2}|20\d{2})\s*[-–—]\s*(present|current|19\d{2}|20\d{2})", lowered)
    if len(date_ranges) >= 1:
        return "experienced"

    if any(keyword in lowered for keyword in ("professional experience", "work experience", "employment history")):
        return "experienced"

    return "fresher"


def _layout_for_profile(profile):
    if profile == "fresher":
        return {
            "margin": 9,
            "title_size": 16,
            "section_size": 11.5,
            "body_size": 9.25,
            "body_height": 3.8,
            "bullet_indent": 13,
            "name_spacing": 1.0,
            "section_spacing": 1.25,
            "paragraph_spacing": 1.0,
            "bottom_margin": 10,
        }

    return {
        "margin": 12,
        "title_size": 16,
        "section_size": 11.5,
        "body_size": 9.75,
        "body_height": 4.05,
        "bullet_indent": 14,
        "name_spacing": 1.2,
        "section_spacing": 1.5,
        "paragraph_spacing": 1.2,
        "bottom_margin": 12,
    }


def _apply_font(pdf, family="Times", style="", size=10):
    pdf.set_font(family, style, size)


def _extract_header_block(lines):
    header_lines = []
    body_start_index = 0

    for index, line in enumerate(lines):
        if _is_section_header(line):
            body_start_index = index
            break

        normalized = _normalize_line(line)
        if normalized:
            header_lines.append(normalized)
            body_start_index = index + 1

    return header_lines, body_start_index


def _render_header(pdf, header_lines, layout, candidate_name=""):
    heading_color = (11, 31, 58)
    body_color = (0, 0, 0)

    name_line = _clean_label(candidate_name) if candidate_name else ""
    header_lines = [_normalize_line(line) for line in header_lines if _normalize_line(line)]

    if not name_line and header_lines:
        name_line = _clean_label(header_lines[0])
        header_lines = header_lines[1:]

    if name_line:
        name_line = re.sub(r"[^A-Za-z0-9 .'-]", "", name_line)
        name_line = name_line.upper()
        _apply_font(pdf, "Times", "B", layout["title_size"])
        pdf.set_text_color(*body_color)
        pdf.cell(0, 7, name_line, align="C", ln=True)

    if header_lines:
        pdf.set_text_color(*body_color)
        _apply_font(pdf, "Times", "", layout["body_size"] - 0.25)
        contact_line = " | ".join(line.strip(" |") for line in header_lines if line.strip())
        contact_line = re.sub(r"\s*\|\s*", " | ", contact_line)
        if contact_line:
            pdf.cell(0, layout["body_height"] + 0.1, contact_line, align="C", ln=True)

    if name_line or header_lines:
        pdf.ln(layout["name_spacing"])
        pdf.set_draw_color(*heading_color)
        pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
        pdf.ln(layout["section_spacing"])
        pdf.set_draw_color(0, 0, 0)


def _render_section_header(pdf, title, layout):
    heading_color = (11, 31, 58)
    title = _clean_label(title)
    pdf.ln(layout["section_spacing"])
    pdf.set_text_color(*heading_color)
    _apply_font(pdf, "Times", "B", layout["section_size"])
    pdf.cell(0, 5.8, title.strip().upper(), ln=True)
    pdf.set_draw_color(*heading_color)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
    pdf.ln(0.8)
    pdf.set_text_color(0, 0, 0)
    _apply_font(pdf, "Times", "", layout["body_size"])


def _render_split_role_line(pdf, text, layout):
    parts = [part.strip() for part in text.split("|") if part.strip()]
    if len(parts) < 2:
        return False

    # Typical American resume style: keep company/role on left and date/location on right.
    left = " | ".join(parts[:-1])
    right = parts[-1]

    if not re.search(r"\b(19\d{2}|20\d{2}|present|current|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\b", right.lower()):
        return False

    _apply_font(pdf, "Times", "B", layout["body_size"])
    pdf.cell(0, layout["body_height"], left, ln=False)
    _apply_font(pdf, "Times", "I", layout["body_size"])
    right_w = pdf.get_string_width(right)
    pdf.set_x(pdf.w - pdf.r_margin - right_w)
    pdf.cell(right_w, layout["body_height"], right, ln=True, align="R")
    _apply_font(pdf, "Times", "", layout["body_size"])
    return True


def _render_bullet(pdf, line, layout):
    bullet_text = _normalize_line(line.lstrip("•-* ").strip())
    bullet_text = textwrap.fill(bullet_text, width=84 if layout["body_size"] >= 9.5 else 80)
    wrapped_lines = bullet_text.split("\n")

    for index, wrapped_line in enumerate(wrapped_lines):
        pdf.set_x(pdf.l_margin + layout["bullet_indent"])
        prefix = "- " if index == 0 else "  "
        pdf.multi_cell(0, layout["body_height"], f"{prefix}{wrapped_line}")


def _render_resume(pdf, resume_text, candidate_name=""):
    cleaned_text = _sanitize_pdf_text(resume_text)
    profile = _detect_candidate_profile(cleaned_text)
    layout = _layout_for_profile(profile)
    lower_priority_sections = {
        "skills",
        "technical skills",
        "core competencies",
        "projects",
        "education",
        "certifications",
        "languages",
        "references",
        "awards",
        "achievements",
        "activities",
        "volunteering",
    }

    pdf.set_auto_page_break(auto=True, margin=layout["bottom_margin"])
    pdf.set_margins(left=layout["margin"], top=layout["margin"], right=layout["margin"])
    pdf.add_page()
    pdf.set_text_color(0, 0, 0)

    lines = cleaned_text.split("\n")
    header_lines, body_start_index = _extract_header_block(lines)
    _render_header(pdf, header_lines, layout, candidate_name=candidate_name)

    _apply_font(pdf, "Times", "", layout["body_size"])
    seen_experience = False

    for line in lines[body_start_index:]:
        line_stripped = _normalize_line(line)

        if not line_stripped:
            pdf.ln(layout["paragraph_spacing"])
            continue

        pdf.set_x(pdf.l_margin)

        if _is_section_header(line_stripped):
            normalized_section = _clean_label(line_stripped).lower()
            if profile == "experienced" and seen_experience and normalized_section in lower_priority_sections and pdf.page_no() == 1:
                pdf.add_page()
                pdf.set_text_color(0, 0, 0)
                _apply_font(pdf, "Times", "", layout["body_size"])

            if normalized_section in {"experience", "professional experience", "work experience", "internship experience"}:
                seen_experience = True

            _render_section_header(pdf, line_stripped, layout)
            continue

        if line_stripped.startswith(("-", "•", "*")):
            _apply_font(pdf, "Times", "", layout["body_size"])
            _render_bullet(pdf, line_stripped, layout)
            continue

        if "|" in line_stripped and not line_stripped.startswith(("-", "•", "*")) and len(line_stripped) <= 170:
            if _render_split_role_line(pdf, line_stripped, layout):
                continue

        date_like = re.search(r"\b(19\d{2}|20\d{2})\b", line_stripped) or re.search(r"\b(present|current)\b", line_stripped.lower())
        if date_like and len(line_stripped) < 120:
            _apply_font(pdf, "Times", "B", layout["body_size"])
            pdf.multi_cell(0, layout["body_height"] + 0.4, line_stripped)
            _apply_font(pdf, "Times", "", layout["body_size"])
            continue

        _apply_font(pdf, "Times", "", layout["body_size"])
        pdf.multi_cell(0, layout["body_height"], line_stripped)

    return profile, layout

def create_resume_pdf(resume_text):
    """Create a professionally formatted PDF from resume text"""
    
    try:
        pdf = FPDF(format="A4", unit="mm")
        _render_resume(pdf, resume_text)

        raw_output = pdf.output(dest="S")
        return raw_output.encode("latin-1") if isinstance(raw_output, str) else bytes(raw_output)
    
    except Exception as e:
        raise Exception(f"Failed to generate PDF: {str(e)}")


def create_styled_resume_pdf(resume_text, candidate_name=""):
    """Create a more styled resume PDF with better formatting"""
    
    try:
        pdf = FPDF(format='A4', unit='mm')
        _render_resume(pdf, resume_text, candidate_name=candidate_name)
        
        raw_output = pdf.output(dest="S")
        return raw_output.encode("latin-1") if isinstance(raw_output, str) else bytes(raw_output)
    
    except Exception as e:
        # Fallback to simple version
        return create_resume_pdf(resume_text)
