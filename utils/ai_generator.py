import google.generativeai as genai
import json
import os
import re
from functools import lru_cache

DEFAULT_GEMINI_MODELS = (
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
    "gemini-2.5-flash",
    "gemini-2.5-pro",
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

    # If model listing is unavailable, use the first configured/default candidate.
    return genai.GenerativeModel(candidates[0])


def _candidate_model_names():
    configured_model = _normalize_model_name(os.environ.get("GEMINI_MODEL", ""))
    candidates = []
    if configured_model:
        candidates.append(configured_model)
    candidates.extend(model for model in DEFAULT_GEMINI_MODELS if model not in candidates)

    available_models = _list_generate_content_models()
    if available_models:
        preferred = [m for m in candidates if m in available_models]
        if preferred:
            return preferred

        flash_models = [m for m in available_models if "flash" in m]
        return flash_models or available_models

    return candidates


def _generate_with_fallback(prompt):
    configure_genai()
    errors = []
    for model_name in _candidate_model_names():
        try:
            model = genai.GenerativeModel(model_name)
            return model.generate_content(prompt)
        except Exception as exc:
            message = str(exc)
            errors.append(f"{model_name}: {message}")
            quota_hit = "429" in message or "quota" in message.lower() or "rate" in message.lower()
            if quota_hit:
                continue
            # Non-quota error on selected model: still try one more model, then continue fallback behavior.
            continue

    raise RuntimeError("All Gemini model attempts failed. " + " | ".join(errors[-3:]))


def _extract_json_block(text):
    text = text.strip()
    if text.startswith("{") and text.endswith("}"):
        return text
    match = re.search(r"\{[\s\S]*\}", text)
    return match.group(0) if match else text


def get_active_model_name():
    """Returns the currently selected Gemini model name for diagnostics."""
    model = get_generative_model()
    model_name = getattr(model, "model_name", "") or getattr(model, "_model_name", "")
    return _normalize_model_name(model_name) or "unknown"

def generate_tailored_resume(job_details, resume_content):
    response = _generate_with_fallback(
        f"""You are a professional resume writer. Rewrite the resume into a clean, ATS-friendly, American-style resume.

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
    )

    return response.text

def generate_application_package(job_details, resume_content):
    response = _generate_with_fallback(
        f"""Generate an ATS-focused job application package from the resume and job details.

Return ONLY valid JSON with this exact schema:
{{
  "tailored_resume": "string",
  "ats_result": {{
    "score": 0,
    "keywords_found": ["string"],
    "keywords_missing": ["string"],
    "suggestions": "string"
  }},
  "email_draft": "string",
  "linkedin_msg": "string"
}}

Rules:
- Keep tailored_resume one-page, ATS-friendly, single-column, concise, US format.
- Use section order: NAME, contact line, PROFESSIONAL SUMMARY, EDUCATION, EXPERIENCE, PROJECTS, SKILLS, ACHIEVEMENTS & LEADERSHIP.
- No markdown wrappers or explanations.
- ats_result.score must be an integer 0-100.
- Keep email_draft around 140-180 words.
- Keep linkedin_msg around 60-90 words.

JOB DETAILS:
{job_details}

SOURCE RESUME:
{resume_content}
"""
    )

    raw = _extract_json_block(response.text)
    parsed = json.loads(raw)

    ats_result = parsed.get("ats_result", {}) if isinstance(parsed, dict) else {}
    score = ats_result.get("score", 70)
    try:
        score = int(score)
    except Exception:
        score = 70

    return {
        "tailored_resume": parsed.get("tailored_resume", ""),
        "ats_result": {
            "score": max(0, min(100, score)),
            "keywords_found": ats_result.get("keywords_found", []) or [],
            "keywords_missing": ats_result.get("keywords_missing", []) or [],
            "suggestions": ats_result.get("suggestions", ""),
        },
        "email_draft": parsed.get("email_draft", ""),
        "linkedin_msg": parsed.get("linkedin_msg", ""),
    }

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
    response = _generate_with_fallback(
        f"Write a professional 200-word application email with a Subject line.\nJob: {job_details}\nResume: {resume_content[:500]}"
    )
    return response.text

def generate_linkedin_message(job_details, resume_content):
    response = _generate_with_fallback(
        f"Write a 100-word LinkedIn DM for this role.\nJob: {job_details}\nResume: {resume_content[:400]}"
    )
    return response.text
