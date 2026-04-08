import google.generativeai as genai
import os
import re
from functools import lru_cache

DEFAULT_GEMINI_MODELS = (
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
)


def _normalize_model_name(model_name):
    return (model_name or "").replace("models/", "").strip()

def configure_genai():
    """Initializes the Gemini API"""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not set in Secrets.")
    genai.configure(api_key=api_key)


@lru_cache(maxsize=1)
def _list_generate_content_models():
    """Returns model names that support generateContent for this API key."""
    configure_genai()
    try:
        models = genai.list_models()
    except Exception:
        return []

    available = []
    for model in models:
        methods = getattr(model, "supported_generation_methods", []) or []
        if "generateContent" in methods:
            normalized = _normalize_model_name(getattr(model, "name", ""))
            if normalized:
                available.append(normalized)
    return available


def get_generative_model():
    """Selects a supported Gemini model with safe fallbacks for deployment."""
    configure_genai()

    configured_model = _normalize_model_name(os.environ.get("GEMINI_MODEL", ""))
    candidates = []
    if configured_model:
        candidates.append(configured_model)
    candidates.extend(model for model in DEFAULT_GEMINI_MODELS if model not in candidates)

    available_models = _list_generate_content_models()
    if available_models:
        for model_name in candidates:
            if model_name in available_models:
                return genai.GenerativeModel(model_name)

        flash_models = [m for m in available_models if "flash" in m]
        return genai.GenerativeModel((flash_models or available_models)[0])

    # If model listing is unavailable, probe candidates and pick the first that works.
    for model_name in candidates:
        try:
            model = genai.GenerativeModel(model_name)
            model.generate_content("Reply with OK.")
            return model
        except Exception:
            continue

    raise RuntimeError(
        "No supported Gemini model found. Set GEMINI_MODEL to a valid model from your account."
    )


def get_active_model_name():
    """Returns the currently selected Gemini model name for diagnostics."""
    model = get_generative_model()
    model_name = getattr(model, "model_name", "") or getattr(model, "_model_name", "")
    return _normalize_model_name(model_name) or "unknown"

def generate_tailored_resume(job_details, resume_content):
    model = get_generative_model()

    prompt = f"""You are a professional resume writer. Rewrite the resume into a clean, ATS-friendly, American-style resume.

Hard rules:
- Output plain text only. No markdown, no bullets with symbols other than standard bullet lines, no tables, no icons, no explanations.
- Keep it to one page by being concise and removing low-value content.
- Use the exact section structure below and nothing else:
    NAME
    Phone | Email | LinkedIn | Location
    PROFESSIONAL SUMMARY
    EDUCATION
    EXPERIENCE
    PROJECTS
    SKILLS
    ACHIEVEMENTS & LEADERSHIP
- Use concise language, strong action verbs, and measurable impact where possible.
- Keep bullets to one line whenever possible. Maximum 3 bullets per role or project.
- Omit weak, repetitive, or low-priority details if space is limited.
- No first-person pronouns. Keep tense consistent.
- Align dates to the right using the pattern: Company | Role | Dates or Institution | Degree | Dates.
- Do not include sentences like "willing to relocate".
- Keep the summary to 2-3 lines maximum.
- Education should include institution, location, degree, and dates.
- Skills must be grouped by category on separate lines, for example: Sales: ... | Analytics: ... | Tools: ...

JOB REQUIREMENTS:
{job_details}

SOURCE RESUME:
{resume_content}

Return only the final resume text in the structure above."""

    response = model.generate_content(prompt)
    return response.text

def generate_ats_score(resume_text, job_details):
    model = get_generative_model()
    
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
    model = get_generative_model()
    prompt = f"Write a professional 200-word application email with a Subject line.\nJob: {job_details}\nResume: {resume_content[:500]}"
    return model.generate_content(prompt).text

def generate_linkedin_message(job_details, resume_content):
    model = get_generative_model()
    prompt = f"Write a 100-word LinkedIn DM for this role.\nJob: {job_details}\nResume: {resume_content[:400]}"
    return model.generate_content(prompt).text
