from fpdf import FPDF
import io
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

    # Keep only characters supported by core fonts.
    return text.encode("latin-1", errors="ignore").decode("latin-1")

def create_resume_pdf(resume_text):
    """Create a professionally formatted PDF from resume text"""
    
    try:
        pdf = FPDF()
        pdf.add_page()
        
        # Set margins
        pdf.set_margins(left=10, top=10, right=10)
        
        # Process resume text
        lines = _sanitize_pdf_text(resume_text).split("\n")
        
        # Track for section headers
        in_section = False
        
        for line in lines:
            line_stripped = line.strip()
            
            if not line_stripped:
                pdf.ln(3)  # Small spacing for blank lines
                continue

            # Keep cursor at left margin before writing any new content line.
            pdf.set_x(pdf.l_margin)
            
            # Check if line is a section header (all caps, relatively short)
            is_header = (
                line_stripped.isupper() and 
                len(line_stripped) < 50 and 
                len(line_stripped.split()) <= 3
            )
            
            if is_header:
                # Section header formatting
                if pdf.get_y() > 10:  # Add spacing before section if not at top
                    pdf.ln(3)
                pdf.set_font("Arial", "B", 13)
                pdf.set_text_color(80, 100, 200)  # Blue color for headers
                pdf.cell(0, 7, line_stripped, ln=True)
                pdf.set_text_color(0, 0, 0)  # Reset to black
                pdf.ln(2)
                in_section = True
            
            elif line.startswith("•") or line.startswith("-"):
                # Bullet point
                pdf.set_font("Arial", "", 10)
                # Extract bullet content and wrap
                bullet_text = line.lstrip("•- ").strip()
                pdf.set_x(15)  # Indent bullet
                
                # Handle multi-line bullets
                wrapped_text = textwrap.fill(bullet_text, width=70)
                wrapped_lines = wrapped_text.split("\n")
                for idx, wrapped_line in enumerate(wrapped_lines):
                    pdf.set_x(15)
                    prefix = "- " if idx == 0 else "  "
                    pdf.multi_cell(0, 5, f"{prefix}{wrapped_line}")
            
            elif any(char.isdigit() for char in line_stripped[:10]):
                # Likely a date or numbered entry
                pdf.set_font("Arial", "B", 10)
                pdf.multi_cell(0, 5, line_stripped)
            
            else:
                # Regular text
                pdf.set_font("Arial", "", 10)
                pdf.multi_cell(0, 5, line_stripped, align='L')
            
            # Check page break
            if pdf.get_y() > 270:
                pdf.add_page()
                pdf.set_margins(left=10, top=10, right=10)
        
        # Convert to bytes across fpdf2 versions.
        raw_output = pdf.output(dest="S")
        pdf_bytes = raw_output.encode("latin-1") if isinstance(raw_output, str) else bytes(raw_output)
        return pdf_bytes
    
    except Exception as e:
        raise Exception(f"Failed to generate PDF: {str(e)}")


def create_styled_resume_pdf(resume_text, candidate_name=""):
    """Create a more styled resume PDF with better formatting"""
    
    try:
        pdf = FPDF(format='A4', unit='mm')
        pdf.add_page()
        
        # Set standard margins
        pdf.set_margins(left=12, top=12, right=12)
        page_width = pdf.w - 24
        
        # Add name if provided
        if candidate_name:
            candidate_name = _sanitize_pdf_text(candidate_name)
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 8, candidate_name, ln=True, align="C")
            pdf.ln(2)
        
        # Process resume
        lines = _sanitize_pdf_text(resume_text).split("\n")
        
        for line in lines:
            line_stripped = line.strip()
            
            if not line_stripped:
                pdf.ln(2)
                continue

            # Keep cursor at left margin before writing any new content line.
            pdf.set_x(pdf.l_margin)
            
            # Section headers
            if (line_stripped.isupper() and 
                len(line_stripped) < 50 and 
                len(line_stripped.split()) <= 4):
                
                if pdf.get_y() > 20:
                    pdf.ln(2)
                
                # Colored section header
                pdf.set_font("Arial", "B", 12)
                pdf.set_text_color(40, 80, 150)
                pdf.cell(0, 6, line_stripped, border_b=1, ln=True)
                pdf.set_text_color(0, 0, 0)
                pdf.ln(1)
            
            else:
                # Regular content
                pdf.set_font("Arial", "", 9.5)
                
                # Wrap text if needed
                if len(line_stripped) > 80:
                    pdf.multi_cell(0, 4, line_stripped)
                else:
                    pdf.cell(0, 4, line_stripped, ln=True)
            
            # Auto page break
            if pdf.will_page_break(4):
                pdf.add_page()
        
        raw_output = pdf.output(dest="S")
        return raw_output.encode("latin-1") if isinstance(raw_output, str) else bytes(raw_output)
    
    except Exception as e:
        # Fallback to simple version
        return create_resume_pdf(resume_text)
