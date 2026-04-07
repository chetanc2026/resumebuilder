import google.generativeai as genai
from PIL import Image
import os

def extract_text_from_image(uploaded_file):
    """Extract job details from LinkedIn screenshot using Gemini 1.5 Flash"""
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")
        
        # Initialize the SDK
        genai.configure(api_key=api_key)
        
        # Load the image
        img = Image.open(uploaded_file)
        
        # Use the stable model name
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = """Analyze this LinkedIn job posting screenshot and extract the following information:
        1. Job Title
        2. Company Name
        3. Key Requirements
        4. Responsibilities
        5. Required Skills
        6. Experience Level
        7. Location
        8. Special Requirements
        Format with clear headers. Be comprehensive but concise."""

        # Generate content
        response = model.generate_content([prompt, img])
        return response.text
    
    except Exception as e:
        raise Exception(f"Failed to extract job details from image: {str(e)}")

def validate_image(uploaded_file):
    """Validate uploaded image"""
    try:
        img = Image.open(uploaded_file)
        uploaded_file.seek(0)
        return True
    except Exception:
        return False
