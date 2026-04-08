import streamlit as st
import os
from pathlib import Path
import base64
import io
from utils.image_processor import extract_text_from_image
from utils.resume_processor import extract_resume_text
from utils.ai_generator import (
    generate_tailored_resume, 
    generate_ats_score, 
    generate_email_draft, 
    generate_linkedin_message,
    get_active_model_name,
)
from utils.pdf_generator import create_resume_pdf

# Page configuration
st.set_page_config(
    page_title="QuickApply AI",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
    <style>
    * {
        margin: 0;
        padding: 0;
    }
    
    .main {
        padding: 2rem;
    }
    
    .header {
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .header h1 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        font-weight: 800;
    }
    
    .header p {
        font-size: 1.1rem;
        opacity: 0.95;
        font-weight: 500;
    }
    
    .upload-section {
        background: #f8f9ff;
        padding: 2rem;
        border-radius: 12px;
        border: 2px solid #e0e0ff;
        margin-bottom: 2rem;
    }
    
    .score-badge {
        font-size: 3rem;
        font-weight: 900;
        text-align: center;
        padding: 2rem;
        border-radius: 12px;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .high-score { 
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
    }
    
    .medium-score { 
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    }
    
    .low-score { 
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .tab-content {
        padding: 2rem 0;
    }
    
    .footer {
        text-align: center;
        color: #999;
        margin-top: 3rem;
        padding: 2rem 0;
        border-top: 1px solid #e0e0e0;
    }
    
    .button-primary {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = 1
if "results" not in st.session_state:
    st.session_state.results = {}

# Header
st.markdown("""
    <div class="header">
        <h1>🚀 QuickApply AI</h1>
        <p>Tailor your resume & craft perfect application messages in seconds</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 📖 How It Works")
    try:
        st.caption(f"Active Gemini model: {get_active_model_name()}")
    except Exception:
        st.caption("Active Gemini model: unavailable")

    st.markdown("""
    **Step 1:** Upload LinkedIn job post screenshot
    
    **Step 2:** Upload your resume
    
    **Step 3:** Click generate to get:
    - ✨ Tailored resume
    - 📊 ATS score
    - 📧 Email draft
    - 💼 LinkedIn message
    - 📄 PDF download
    """)
    
    st.divider()
    
    st.markdown("## ⚡ Features")
    st.markdown("""
    - AI-powered resume tailoring
    - Real-time ATS scoring
    - Professional email templates
    - LinkedIn message generator
    - One-click PDF export
    - No login required
    - Free to use
    """)
    
    st.divider()
    
    st.info("💡 **Tip:** Best results with clear job post screenshots and complete resumes.")

# Main content
st.markdown("## Step 1️⃣ Upload Your Documents")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📸 Job Posting")
    st.markdown("Upload a screenshot of the LinkedIn job posting")
    job_image = st.file_uploader(
        "Upload job posting screenshot",
        type=["png", "jpg", "jpeg"],
        key="job_upload",
        label_visibility="collapsed"
    )

with col2:
    st.markdown("### 📄 Your Resume")
    st.markdown("Upload your resume (PDF, DOCX, or TXT)")
    resume_file = st.file_uploader(
        "Upload your resume",
        type=["pdf", "txt", "docx"],
        key="resume_upload",
        label_visibility="collapsed"
    )

st.divider()

# Generate button
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    generate_button = st.button(
        "🔥 Generate Application Package",
        type="primary",
        use_container_width=True,
        key="generate_btn"
    )

if generate_button:
    if job_image is None or resume_file is None:
        st.error("❌ Please upload both a job posting and resume to continue")
        st.stop()
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Step 1: Extract job details
        status_text.info("📸 Step 1/6: Analyzing job posting...")
        progress_bar.progress(15)
        job_details = extract_text_from_image(job_image)
        st.session_state.results["job_details"] = job_details
        
        # Step 2: Extract resume
        status_text.info("📄 Step 2/6: Reading your resume...")
        progress_bar.progress(30)
        resume_content = extract_resume_text(resume_file)
        st.session_state.results["resume_content"] = resume_content
        
        # Step 3: Tailor resume
        status_text.info("✨ Step 3/6: Tailoring resume to job requirements...")
        progress_bar.progress(45)
        tailored_resume = generate_tailored_resume(job_details, resume_content)
        st.session_state.results["tailored_resume"] = tailored_resume
        
        # Step 4: Calculate ATS score
        status_text.info("📊 Step 4/6: Calculating ATS compatibility score...")
        progress_bar.progress(60)
        ats_result = generate_ats_score(tailored_resume, job_details)
        st.session_state.results["ats_result"] = ats_result
        
        # Step 5: Generate email draft
        status_text.info("📧 Step 5/6: Creating professional email...")
        progress_bar.progress(75)
        email_draft = generate_email_draft(job_details, resume_content)
        st.session_state.results["email_draft"] = email_draft
        
        # Step 6: Generate LinkedIn message
        status_text.info("💼 Step 6/6: Writing LinkedIn message...")
        progress_bar.progress(85)
        linkedin_msg = generate_linkedin_message(job_details, resume_content)
        st.session_state.results["linkedin_msg"] = linkedin_msg
        
        # Step 7: Create PDF
        status_text.info("📥 Creating downloadable PDF...")
        progress_bar.progress(95)
        pdf_bytes = create_resume_pdf(tailored_resume)
        st.session_state.results["pdf_bytes"] = pdf_bytes
        
        progress_bar.progress(100)
        status_text.success("✅ Application package ready!")
        st.session_state.step = 2
        
        # Show results section
        st.rerun()
        
    except Exception as e:
        status_text.error(f"❌ Error: {str(e)}")
        st.error(f"Failed to generate package. Please check your inputs and try again.")

# Display Results
if st.session_state.step == 2 and "ats_result" in st.session_state.results:
    st.markdown("---")
    st.markdown("## Step 2️⃣ Your Application Package")
    
    results = st.session_state.results
    
    # ATS Score Display
    col1, col2, col3 = st.columns(3)
    
    with col1:
        score = results["ats_result"].get("score", 0)
        score_class = "high-score" if score >= 80 else "medium-score" if score >= 60 else "low-score"
        
        if score >= 80:
            status = "Excellent! 🎯"
        elif score >= 60:
            status = "Good! 👍"
        else:
            status = "Needs work 💪"
        
        st.markdown(f"""
            <div class="score-badge {score_class}">
                {score}%
            </div>
            <div style="text-align: center; margin-top: 0.5rem; color: #666;">
                <strong>ATS Score</strong><br>{status}
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        keywords_found = len(results["ats_result"].get("keywords_found", []))
        st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 2rem; font-weight: bold; color: #667eea;">{keywords_found}</div>
                <div style="color: #666; margin-top: 0.5rem;">Keywords Found</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        keywords_missing = len(results["ats_result"].get("keywords_missing", []))
        st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 2rem; font-weight: bold; color: #f59e0b;">{keywords_missing}</div>
                <div style="color: #666; margin-top: 0.5rem;">Keywords Missing</div>
            </div>
        """, unsafe_allow_html=True)
    
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
        st.markdown("This resume has been customized to match the job requirements:")
        
        # Display resume in a formatted way
        resume_container = st.container()
        with resume_container:
            st.text_area(
                "Tailored Resume",
                value=results["tailored_resume"],
                height=400,
                disabled=True,
                label_visibility="collapsed"
            )
        
        col1, col2 = st.columns(2)
        with col1:
            st.button("📋 Copy Resume", key="copy_resume_text")
        with col2:
            st.info("Download as PDF in the 'Download' tab for better formatting")
    
    with tab2:
        st.markdown("### ATS Compatibility Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### ✅ Keywords Found")
            keywords_found = results["ats_result"].get("keywords_found", [])
            if keywords_found:
                for kw in keywords_found[:15]:  # Show top 15
                    st.markdown(f"- `{kw}`")
                if len(keywords_found) > 15:
                    st.caption(f"...and {len(keywords_found)-15} more")
        
        with col2:
            st.markdown("#### ⚠️ Keywords Missing")
            keywords_missing = results["ats_result"].get("keywords_missing", [])
            if keywords_missing:
                for kw in keywords_missing[:15]:  # Show top 15
                    st.markdown(f"- `{kw}`")
                if len(keywords_missing) > 15:
                    st.caption(f"...and {len(keywords_missing)-15} more")
        
        st.markdown("#### 💡 Improvement Suggestions")
        suggestions = results["ats_result"].get("suggestions", "No suggestions available")
        st.markdown(suggestions)
    
    with tab3:
        st.markdown("### Email Draft")
        st.markdown("**Copy this email and send to the recruiter:**")
        
        email_text = results["email_draft"]
        st.text_area(
            "Email Draft",
            value=email_text,
            height=300,
            disabled=True,
            label_visibility="collapsed"
        )
        
        # Copy to clipboard button
        col1, col2 = st.columns(2)
        with col1:
            st.button("📋 Copy Email to Clipboard", key="copy_email")
        with col2:
            st.markdown("✅ Paste into your email client")
    
    with tab4:
        st.markdown("### LinkedIn Message")
        st.markdown("**Copy this message and send to the recruiter:**")
        
        linkedin_text = results["linkedin_msg"]
        st.text_area(
            "LinkedIn Message",
            value=linkedin_text,
            height=200,
            disabled=True,
            label_visibility="collapsed"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            st.button("📋 Copy LinkedIn Message", key="copy_linkedin")
        with col2:
            st.markdown("✅ Paste into LinkedIn DM")
    
    with tab5:
        st.markdown("### Download Your Resume")
        st.markdown("Download the tailored resume as a professionally formatted PDF:")
        
        if "pdf_bytes" in results:
            st.download_button(
                label="📥 Download Resume (PDF)",
                data=results["pdf_bytes"],
                file_name="tailored_resume.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        else:
            st.warning("PDF generation in progress...")
        
        st.divider()
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Regenerate Results", use_container_width=True):
                st.session_state.step = 1
                st.session_state.results = {}
                st.rerun()
        
        with col2:
            if st.button("🆕 Start Over", use_container_width=True):
                st.session_state.step = 1
                st.session_state.results = {}
                st.rerun()

# Footer
st.divider()
st.markdown("""
    <div class="footer">
        <p>💚 <strong>QuickApply AI</strong> - Powered by Gemini AI</p>
        <p style="font-size: 0.9rem; margin-top: 0.5rem;">Made for job seekers by job seekers</p>
    </div>
""", unsafe_allow_html=True)
