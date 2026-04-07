# QuickApply AI - Streamlit Deployment Guide

## Step-by-Step Deployment Process

### 1. Create a GitHub Repository

**Option A: Using GitHub Web Interface**
1. Go to [github.com/new](https://github.com/new)
2. Repository name: `quickapply-ai`
3. Description: "AI-powered job application assistant - Tailor resumes, generate emails & LinkedIn messages"
4. Set to **Public** (required for free Streamlit deployment)
5. Initialize with README
6. Click "Create repository"

**Option B: Using Git CLI**
```bash
git init quickapply-ai
cd quickapply-ai
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/quickapply-ai.git
git branch -M main
git push -u origin main
```

---

### 2. Project Structure

Create this folder structure in your repo:

```
quickapply-ai/
├── streamlit_app.py          # Main Streamlit app
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore file
├── README.md                # Project documentation
├── utils/
│   ├── __init__.py
│   ├── image_processor.py   # Extract text from images
│   ├── resume_processor.py  # Process resume text
│   ├── ai_generator.py      # AI text generation
│   └── pdf_generator.py     # PDF creation
└── assets/
    └── sample_resume.pdf    # Example resume
```

---

### 3. Core Files to Create

#### **requirements.txt**
```txt
streamlit==1.28.1
pillow==10.0.0
pypdf==3.17.1
python-docx==0.8.11
fpdf2==2.7.0
anthropic==0.7.1
opencv-python==4.8.1.78
pytesseract==0.3.10
pdf2image==1.16.3
```

#### **streamlit_app.py** (Main Application)
```python
import streamlit as st
import os
from pathlib import Path
from utils.image_processor import extract_text_from_image
from utils.resume_processor import extract_resume_text
from utils.ai_generator import generate_ats_score, generate_email_draft, generate_linkedin_message
from utils.pdf_generator import create_resume_pdf

st.set_page_config(
    page_title="QuickApply AI",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    .header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .card {
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        background: #f9f9f9;
        margin-bottom: 1rem;
    }
    .score-badge {
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
        padding: 1rem;
        border-radius: 8px;
        color: white;
    }
    .high-score { background: #22c55e; }
    .medium-score { background: #f59e0b; }
    .low-score { background: #ef4444; }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="header">
        <h1>🚀 QuickApply AI</h1>
        <p>Tailor your resume & craft perfect application messages in seconds</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar for instructions
with st.sidebar:
    st.header("📖 How It Works")
    st.markdown("""
    1. **Upload LinkedIn Job Post** - Screenshot of the job vacancy
    2. **Upload Your Resume** - PDF or text format
    3. **Generate Results** - Get tailored resume + ATS score + draft messages
    4. **Download & Send** - Download resume PDF and copy message drafts
    """)
    
    st.divider()
    st.markdown("""
    **Features:**
    - ✨ AI-powered resume tailoring
    - 📊 ATS compatibility scoring
    - 📧 Professional email drafts
    - 💼 LinkedIn message templates
    - 📄 One-click PDF download
    """)

# Main workflow
st.header("Step 1: Upload Job Posting & Resume")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Job Posting")
    job_image = st.file_uploader(
        "Upload LinkedIn job post screenshot",
        type=["png", "jpg", "jpeg"],
        key="job_upload"
    )

with col2:
    st.subheader("Your Resume")
    resume_file = st.file_uploader(
        "Upload your resume (PDF or text)",
        type=["pdf", "txt", "docx"],
        key="resume_upload"
    )

# Process button
if st.button("🔥 Generate Application Package", type="primary", use_container_width=True):
    
    if job_image is None or resume_file is None:
        st.error("❌ Please upload both a job posting and resume")
        st.stop()
    
    with st.spinner("⏳ Processing your application..."):
        
        # Step 1: Extract job details from image
        st.info("📸 Analyzing job posting...")
        job_details = extract_text_from_image(job_image)
        st.session_state.job_details = job_details
        
        # Step 2: Extract resume content
        st.info("📄 Reading your resume...")
        resume_content = extract_resume_text(resume_file)
        st.session_state.resume_content = resume_content
        
        # Step 3: Tailor resume (using AI)
        st.info("✨ Tailoring resume to job requirements...")
        tailored_resume = generate_tailored_resume(job_details, resume_content)
        st.session_state.tailored_resume = tailored_resume
        
        # Step 4: Calculate ATS score
        st.info("📊 Calculating ATS compatibility score...")
        ats_result = generate_ats_score(tailored_resume, job_details)
        st.session_state.ats_result = ats_result
        
        # Step 5: Generate email draft
        st.info("📧 Drafting professional email...")
        email_draft = generate_email_draft(job_details, ats_result)
        st.session_state.email_draft = email_draft
        
        # Step 6: Generate LinkedIn message
        st.info("💼 Creating LinkedIn message...")
        linkedin_msg = generate_linkedin_message(job_details, ats_result)
        st.session_state.linkedin_msg = linkedin_msg
        
        # Step 7: Create PDF
        st.info("📥 Generating resume PDF...")
        pdf_bytes = create_resume_pdf(tailored_resume)
        st.session_state.pdf_bytes = pdf_bytes
        
        st.success("✅ Application package ready!")

# Display Results
if "ats_result" in st.session_state:
    st.header("Step 2: Your Application Package")
    
    # ATS Score Display
    col1, col2, col3 = st.columns(3)
    
    with col1:
        score = st.session_state.ats_result.get("score", 0)
        score_class = "high-score" if score >= 80 else "medium-score" if score >= 60 else "low-score"
        st.markdown(f"""
            <div class="score-badge {score_class}">
                ATS Score<br>{score}%
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.metric("Keywords Found", st.session_state.ats_result.get("keywords_found", 0))
    
    with col3:
        st.metric("Keywords Missing", st.session_state.ats_result.get("keywords_missing", 0))
    
    st.divider()
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📄 Tailored Resume",
        "📊 ATS Analysis",
        "📧 Email Draft",
        "💼 LinkedIn Message",
        "📥 Download"
    ])
    
    with tab1:
        st.markdown("### Your Tailored Resume")
        st.markdown(st.session_state.tailored_resume)
    
    with tab2:
        st.markdown("### ATS Compatibility Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Keywords Present:**")
            st.write(", ".join(st.session_state.ats_result.get("keywords_present", [])))
        
        with col2:
            st.markdown("**Keywords Missing:**")
            st.write(", ".join(st.session_state.ats_result.get("keywords_missing", [])))
        
        st.markdown("**Improvement Suggestions:**")
        st.write(st.session_state.ats_result.get("suggestions", ""))
    
    with tab3:
        st.markdown("### Email Draft")
        email_text = st.session_state.email_draft
        st.text_area("Copy this email:", value=email_text, height=200, disabled=True)
        st.button("📋 Copy Email", key="copy_email")
    
    with tab4:
        st.markdown("### LinkedIn Message")
        linkedin_text = st.session_state.linkedin_msg
        st.text_area("Copy this message:", value=linkedin_text, height=150, disabled=True)
        st.button("📋 Copy Message", key="copy_linkedin")
    
    with tab5:
        st.markdown("### Download Resume")
        col1, col2 = st.columns(2)
        
        with col1:
            st.download_button(
                label="📥 Download Resume (PDF)",
                data=st.session_state.pdf_bytes,
                file_name="tailored_resume.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        
        with col2:
            if st.button("🔄 Regenerate", use_container_width=True):
                st.session_state.clear()
                st.rerun()

# Footer
st.divider()
st.markdown("""
    <div style="text-align: center; color: #999; margin-top: 2rem;">
        <p>Built with ❤️ using Streamlit | Made for job seekers by job seekers</p>
    </div>
""", unsafe_allow_html=True)
```

#### **utils/image_processor.py**
```python
import anthropic
import base64
from PIL import Image
import io

def extract_text_from_image(uploaded_file):
    """Extract job details from LinkedIn screenshot using Claude's vision API"""
    
    # Read image
    image_data = uploaded_file.read()
    base64_image = base64.standard_b64encode(image_data).decode("utf-8")
    
    # Determine image type
    image_type = "image/png" if uploaded_file.type == "image/png" else "image/jpeg"
    
    # Call Claude API with vision
    client = anthropic.Anthropic()
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": image_type,
                            "data": base64_image,
                        },
                    },
                    {
                        "type": "text",
                        "text": """Extract the following information from this LinkedIn job posting:
                        
1. Job Title
2. Company Name
3. Key Requirements (list the main skills/qualifications)
4. Responsibilities (brief summary)
5. Required Skills (technical and soft skills)
6. Experience Level (entry-level, mid-level, senior)
7. Any other important details

Format as structured text."""
                    }
                ],
            }
        ],
    )
    
    return message.content[0].text


def validate_image(uploaded_file):
    """Validate uploaded image"""
    try:
        img = Image.open(uploaded_file)
        img.verify()
        return True
    except:
        return False
```

#### **utils/resume_processor.py**
```python
import PyPDF2
import docx

def extract_resume_text(uploaded_file):
    """Extract text from resume (PDF, DOCX, or TXT)"""
    
    file_type = uploaded_file.type
    
    if file_type == "application/pdf":
        return extract_from_pdf(uploaded_file)
    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return extract_from_docx(uploaded_file)
    elif file_type == "text/plain":
        return uploaded_file.read().decode("utf-8")
    else:
        raise ValueError(f"Unsupported file type: {file_type}")

def extract_from_pdf(pdf_file):
    """Extract text from PDF"""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_from_docx(docx_file):
    """Extract text from DOCX"""
    doc = docx.Document(docx_file)
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return text
```

#### **utils/ai_generator.py**
```python
import anthropic
import os

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def generate_tailored_resume(job_details, resume_content):
    """Tailor resume to job requirements using Claude"""
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=2000,
        messages=[
            {
                "role": "user",
                "content": f"""You are an expert resume writer. Your task is to tailor the following resume to match the job requirements while maintaining the original format and structure.

JOB DETAILS:
{job_details}

ORIGINAL RESUME:
{resume_content}

Please create a tailored version that:
1. Emphasizes relevant skills and experience
2. Uses keywords from the job description
3. Maintains professional formatting
4. Keeps the same structure as original
5. Highlights achievements relevant to this role

Return only the tailored resume text, no explanations."""
            }
        ],
    )
    
    return message.content[0].text

def generate_ats_score(resume_text, job_details):
    """Calculate ATS compatibility score"""
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1500,
        messages=[
            {
                "role": "user",
                "content": f"""Analyze the following resume against the job requirements and provide an ATS (Applicant Tracking System) compatibility score.

JOB REQUIREMENTS:
{job_details}

RESUME:
{resume_text}

Please provide:
1. Overall ATS score (0-100)
2. List of keywords from job description that are present in resume
3. List of important keywords missing from resume
4. Specific suggestions to improve ATS score

Format as:
SCORE: [number]
KEYWORDS FOUND: [comma-separated list]
KEYWORDS MISSING: [comma-separated list]
SUGGESTIONS: [bullet points]"""
            }
        ],
    )
    
    response_text = message.content[0].text
    
    # Parse response
    lines = response_text.split("\n")
    result = {
        "score": 0,
        "keywords_found": [],
        "keywords_missing": [],
        "suggestions": ""
    }
    
    for line in lines:
        if line.startswith("SCORE:"):
            try:
                result["score"] = int(line.split(":")[1].strip())
            except:
                result["score"] = 75
        elif line.startswith("KEYWORDS FOUND:"):
            keywords = line.split(":", 1)[1].strip()
            result["keywords_found"] = [k.strip() for k in keywords.split(",")]
        elif line.startswith("KEYWORDS MISSING:"):
            keywords = line.split(":", 1)[1].strip()
            result["keywords_missing"] = [k.strip() for k in keywords.split(",")]
        elif line.startswith("SUGGESTIONS:"):
            result["suggestions"] = "\n".join(lines[lines.index(line)+1:])
    
    return result

def generate_email_draft(job_details, ats_result):
    """Generate professional email draft"""
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=800,
        messages=[
            {
                "role": "user",
                "content": f"""Write a professional job application email based on this job posting and ATS analysis.

JOB DETAILS:
{job_details}

Make the email:
1. Professional and concise (under 200 words)
2. Personalized to the specific role
3. Include a call to action
4. Reference relevant qualifications
5. End with a professional closing

Return only the email content, starting with "Subject:" line."""
            }
        ],
    )
    
    return message.content[0].text

def generate_linkedin_message(job_details, ats_result):
    """Generate LinkedIn message"""
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=500,
        messages=[
            {
                "role": "user",
                "content": f"""Write a short, engaging LinkedIn message to reach out about this job opportunity.

JOB DETAILS:
{job_details}

The message should be:
1. Friendly and professional
2. Under 100 words
3. Show genuine interest in the role
4. Mention specific aspects of the company/role
5. Include a soft call to action

Return only the message text."""
            }
        ],
    )
    
    return message.content[0].text
```

#### **utils/pdf_generator.py**
```python
from fpdf import FPDF
import io

def create_resume_pdf(resume_text):
    """Create a formatted PDF from resume text"""
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    
    # Add resume text with basic formatting
    lines = resume_text.split("\n")
    
    for line in lines:
        if line.strip():
            # Bold for section headers (all caps)
            if line.isupper() and len(line) < 50:
                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 6, line.strip(), ln=True)
                pdf.set_font("Arial", size=11)
            else:
                pdf.set_font("Arial", size=10)
                pdf.multi_cell(0, 5, line.strip())
        else:
            pdf.ln(2)
    
    # Return PDF as bytes
    return pdf.output(dest="S").encode("latin-1")
```

#### **.gitignore**
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv

# Streamlit
.streamlit/
*.streamlit.app

# API Keys
.env
secrets.toml

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Files
*.pdf
*.xlsx
uploads/
```

#### **README.md**
```markdown
# QuickApply AI

An intelligent job application assistant powered by Claude AI. Tailor your resume, get ATS scores, and generate professional outreach messages—all in seconds.

## Features

✨ **Smart Resume Tailoring** - AI-powered customization based on job requirements  
📊 **ATS Score Analysis** - Know your compatibility before applying  
📧 **Email Drafts** - Professional application emails generated automatically  
💼 **LinkedIn Messages** - Personalized connection requests ready to send  
📥 **One-Click PDF Export** - Download formatted resume instantly  
🚀 **Zero Setup** - No login, no complex configuration

## How to Use

1. Upload a screenshot of the LinkedIn job posting
2. Upload your resume (PDF, DOCX, or TXT)
3. Click "Generate Application Package"
4. Review and download your customized materials
5. Copy & send emails and messages

## Tech Stack

- **Frontend**: Streamlit
- **AI Engine**: Claude 3.5 Sonnet (Anthropic)
- **PDF Generation**: FPDF2
- **File Processing**: PyPDF2, python-docx

## Installation

### Local Setup

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/quickapply-ai.git
cd quickapply-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set API key
export ANTHROPIC_API_KEY='your-api-key-here'

# Run app
streamlit run streamlit_app.py
```

### Streamlit Cloud Deployment

1. Push code to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Click "New app"
4. Select your repository and `streamlit_app.py`
5. Add `ANTHROPIC_API_KEY` in Secrets
6. Deploy!

## Configuration

Create `.streamlit/secrets.toml` for local development:

```toml
ANTHROPIC_API_KEY = "sk-ant-..."
```

For Streamlit Cloud, add secrets in Settings → Secrets.

## API Keys

Get your Anthropic API key:
1. Visit [console.anthropic.com](https://console.anthropic.com)
2. Create account
3. Generate API key
4. Add to environment variables

## File Structure

```
quickapply-ai/
├── streamlit_app.py
├── requirements.txt
├── README.md
├── .gitignore
└── utils/
    ├── image_processor.py
    ├── resume_processor.py
    ├── ai_generator.py
    └── pdf_generator.py
```

## Troubleshooting

**"ModuleNotFoundError"**
```bash
pip install -r requirements.txt
```

**"API Key not found"**
Check that `ANTHROPIC_API_KEY` is set in environment or Streamlit secrets.

**"Failed to process image"**
Ensure image is clear and contains readable job posting text.

## Contributing

Contributions welcome! Please:
1. Fork repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

MIT License - see LICENSE file for details

## Support

- 📧 Email: support@quickapply.ai
- 🐛 Issues: [GitHub Issues](https://github.com/YOUR_USERNAME/quickapply-ai/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/YOUR_USERNAME/quickapply-ai/discussions)

---

**Made for job seekers by job seekers** ❤️
```

---

### 4. Deployment Steps

#### **Deploy to Streamlit Cloud (Recommended - FREE)**

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial streamlit app"
   git push origin main
   ```

2. **Go to Streamlit Cloud**
   - Visit https://streamlit.io/cloud
   - Sign in with GitHub
   - Click "New app"
   - Select repository, branch, and `streamlit_app.py`

3. **Add Secrets**
   - In app settings, go to "Secrets"
   - Add: `ANTHROPIC_API_KEY = "sk-ant-..."`

4. **Deploy** - Your app goes live instantly!

#### **Deploy to Heroku (Alternative)**

```bash
# Install Heroku CLI
# heroku login

# Create Procfile
echo "web: streamlit run streamlit_app.py --logger.level=error" > Procfile

# Create runtime.txt
echo "python-3.11.0" > runtime.txt

# Deploy
heroku create your-app-name
heroku config:set ANTHROPIC_API_KEY="sk-ant-..."
git push heroku main
```

---

### 5. Security Best Practices

✅ Never commit API keys  
✅ Use `.gitignore` for `.env` and `secrets.toml`  
✅ Use Streamlit Secrets for production  
✅ Keep dependencies updated  
✅ Validate user uploads  

---

### 6. Cost Estimate

| Service | Cost |
|---------|------|
| Streamlit Cloud | **FREE** (up to 3 apps) |
| Anthropic Claude API | ~$0.003/1K input tokens |
| GitHub | FREE (public repo) |
| **Total** | **~$0.10 per app use** |

---

## Quick Commands Reference

```bash
# Local development
streamlit run streamlit_app.py

# Install dependencies
pip install -r requirements.txt

# Update requirements
pip freeze > requirements.txt

# Git workflow
git add .
git commit -m "Feature description"
git push origin main
```

---

## Next Steps

1. ✅ Create GitHub repo
2. ✅ Add files above
3. ✅ Get Anthropic API key
4. ✅ Deploy to Streamlit Cloud
5. ✅ Share with friends!

Happy deploying! 🚀
