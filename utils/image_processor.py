import google.generativeai as genai
from PIL import Image
import os

def extract_text_from_image(uploaded_file):
    """Extract job details from LinkedIn screenshot using Gemini 1.5 Flash-latest"""
    try:
        # Configure Gemini - ensure GEMINI_API_KEY is in your environment/secrets
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")
        
        genai.configure(api_key=api_key)
        
        # Load the image directly using PIL
        img = Image.open(uploaded_file)
        
        # Use gemini-1.5-flash for fast, cost-effective vision processing
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        prompt = """Analyze this LinkedIn job posting screenshot and extract the following information:

1. **Job Title** - The exact position title
2. **Company Name** - Name of the hiring company
3. **Key Requirements** - Main skills and qualifications listed
4. **Responsibilities** - Primary job duties and responsibilities
5. **Required Skills** - Technical and soft skills needed
6. **Experience Level** - Entry-level, mid-level, senior, or specific years required
7. **Location** - Job location (remote, on-site, hybrid)
8. **Any Special Requirements** - Certifications, degrees, or unique requirements

Format the response clearly with headers for each section. Be comprehensive but concise."""

        # Generate content using the image and prompt
        response = model.generate_content([prompt, img])
        
        return response.text
    
    except Exception as e:
        raise Exception(f"Failed to extract job details from image: {str(e)}")


def validate_image(uploaded_file):
    """Validate uploaded image"""
    try:
        img = Image.open(uploaded_file)
        # Reset file pointer to ensure other functions can read it from the start
        uploaded_file.seek(0)
        return True
    except Exception:
        return False
