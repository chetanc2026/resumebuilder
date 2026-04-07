import google.generativeai as genai
import os
import re

def configure_genai():
    """Initializes the Gemini API with your key"""
    # NOTE: You must add 'GEMINI_API_KEY' to your environment variables or Streamlit secrets
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)

def generate_tailored_resume(job_details, resume_content):
    """Tailor resume to job requirements using Gemini"""
    configure_genai()
    model = genai.GenerativeModel('gemini-1.5-flash-latest') # Use 'gemini-1.5-pro' for higher quality
    
    prompt = f"""You are an expert professional resume writer. Your task is to tailor the provided resume to perfectly match the job requirements while maintaining the original structure and formatting.

IMPORTANT INSTRUCTIONS:
- Keep all original sections (Experience, Education, Skills, etc.)
- Use keywords from the job description naturally in the resume
- Highlight relevant achievements and experiences
- Maintain professional tone and formatting
- Do NOT change the overall structure or add new sections

JOB REQUIREMENTS:
{job_details}

ORIGINAL RESUME:
{resume_content}

Please provide the COMPLETE tailored resume as the output."""

    response = model.generate_content(prompt)
    return response.text

def generate_ats_score(resume_text, job_details):
    """Calculate ATS compatibility score using Gemini"""
    configure_genai()
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
    prompt = f"""Analyze the resume against job requirements and provide an ATS (Applicant Tracking System) compatibility score.

IMPORTANT: Provide the response EXACTLY in this format:

SCORE: [number between 0-100]
KEYWORDS_FOUND: [comma-separated list of keywords]
KEYWORDS_MISSING: [comma-separated list of keywords]
SUGGESTIONS: [Bullet points]

JOB REQUIREMENTS:
{job_details}

RESUME:
{resume_text}"""

    response = model.generate_content(prompt)
    response_text = response.text
    
    result = {"score": 0, "keywords_found": [], "keywords_missing": [], "suggestions": ""}
    
    try:
        lines = response_text.split("\n")
        for i, line in enumerate(lines):
            if line.startswith("SCORE:"):
                score_match = re.findall(r'\d+', line)
                result["score"] = int(score_match[0]) if score_match else 75
            elif line.startswith("KEYWORDS_FOUND:"):
                keywords = line.split(":", 1)[1].strip()
                result["keywords_found"] = [k.strip() for k in keywords.split(",") if k.strip()]
            elif line.startswith("KEYWORDS_MISSING:"):
                keywords = line.split(":", 1)[1].strip()
                result["keywords_missing"] = [k.strip() for k in keywords.split(",") if k.strip()]
            elif line.startswith("SUGGESTIONS:"):
                result["suggestions"] = "\n".join(lines[i+1:]).strip()
                break
    except Exception as e:
        result["score"] = 70
        result["suggestions"] = response_text
    
    return result

def generate_email_draft(job_details, resume_content):
    """Generate professional email draft using Gemini"""
    configure_genai()
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
    prompt = f"""Write a professional job application email based on this job posting. 
    150-200 words, starting with a Subject line.
    
    JOB DETAILS: {job_details}
    CANDIDATE SUMMARY: {resume_content[:500]}"""

    response = model.generate_content(prompt)
    return response.text

def generate_linkedin_message(job_details, resume_content):
    """Generate LinkedIn message using Gemini"""
    configure_genai()
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
    prompt = f"""Write a short (under 100 words) LinkedIn connection message for this role.
    JOB DETAILS: {job_details}
    CANDIDATE INFO: {resume_content[:400]}"""

    response = model.generate_content(prompt)
    return response.text
