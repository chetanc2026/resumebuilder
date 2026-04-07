import pypdf
import io
# Move this import to the top to ensure dependencies are checked at startup
try:
    from docx import Document
except ImportError:
    Document = None

def extract_resume_text(uploaded_file):
    """Extract text from resume (PDF, DOCX, or TXT)"""
    # Important: Reset file pointer in case it was read elsewhere
    uploaded_file.seek(0)
    file_type = uploaded_file.type
    
    try:
        if file_type == "application/pdf":
            return extract_from_pdf(uploaded_file)
        elif file_type == "text/plain":
            return uploaded_file.read().decode("utf-8")
        elif "wordprocessingml" in file_type or file_type == "application/msword":
            return extract_from_docx(uploaded_file)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
    except Exception as e:
        raise Exception(f"Failed to extract resume text: {str(e)}")

def extract_from_pdf(pdf_file):
    """Extract text from PDF using pypdf"""
    try:
        pdf_reader = pypdf.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        
        if not text.strip():
            raise ValueError("No text found in PDF. Please ensure the PDF is not a scanned image.")
        return text
    except Exception as e:
        raise Exception(f"Failed to extract text from PDF: {str(e)}")

def extract_from_docx(docx_file):
    """Extract text from DOCX"""
    if Document is None:
        raise Exception("python-docx is not installed. Please check your requirements.txt.")
    try:
        doc = Document(docx_file)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except Exception as e:
        raise Exception(f"Failed to extract text from DOCX: {str(e)}")
