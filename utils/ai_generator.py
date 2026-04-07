import google.generativeai as genai
import os
import re

def configure_genai():
    """Initializes the Gemini API"""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not set in Secrets.")
    genai.configure(api_key=api_key)

def generate_tailored_resume(job_details, resume_content):
    configure_genai()
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""You are an expert resume writer. Tailor this resume to match the job requirements perfectly while keeping the original structure.
    JOB REQUIREMENTS:
    {job_details}
    ORIGINAL RESUME:
    {resume_content}
    Provide the COMPLETE tailored resume."""

    response = model.generate_content(prompt)
    return response.text

def generate_ats_score(resume_text, job_details):
    configure_genai()
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""Analyze this resume against job requirements for ATS compatibility.
    FORMAT:
    SCORE: [0-100]
    KEYWORDS_FOUND: [list]
    KEYWORDS_MISSING: [list]
    SUGGESTIONS: [bullets]
    
    JOB: {job_details}
    RESUME: {resume_text}"""

    response = model.generate_content(prompt)
    response_text = response.text
    
    result = {"score": 0, "keywords_found": [], "keywords_missing": [], "suggestions": ""}
    try:
        lines = response_text.split("\n")
        for i, line in enumerate(lines):
            if line.startswith("SCORE:"):
                nums = re.findall(r'\d+', line)
                result["score"] = int(nums[0]) if nums else 70
            elif line.startswith("KEYWORDS_FOUND:"):
                result["keywords_found"] = [k.strip() for k in line.split(":", 1)[1].split(",")]
            elif line.startswith("KEYWORDS_MISSING:"):
                result["keywords_missing"] = [k.strip() for k in line.split(":", 1)[1].split(",")]
            elif line.startswith("SUGGESTIONS:"):
                result["suggestions"] = "\n".join(lines[i+1:]).strip()
                break
    except:
        result["suggestions"] = response_text
    return result

def generate_email_draft(job_details, resume_content):
    configure_genai()
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"Write a professional 200-word application email with a Subject line.\nJob: {job_details}\nResume: {resume_content[:500]}"
    return model.generate_content(prompt).text

def generate_linkedin_message(job_details, resume_content):
    configure_genai()
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"Write a 100-word LinkedIn DM for this role.\nJob: {job_details}\nResume: {resume_content[:400]}"
    return model.generate_content(prompt).text
