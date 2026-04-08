# 🚀 QuickApply AI

An intelligent job application assistant powered by Gemini AI. Tailor your resume, get ATS scores, and generate professional outreach messages—all in seconds.

## ✨ Features

- **AI-powered Resume Tailoring** - Customize your resume to match job requirements in real-time
- **ATS Score Analysis** - Know your compatibility score before applying (0-100%)
- **Professional Email Drafts** - Generate compelling application emails instantly
- **LinkedIn Messages** - Create personalized connection request messages
- **One-Click PDF Export** - Download formatted resumes with a single click
- **Zero Setup Required** - No login, no database, no complex configuration
- **Free to Use** - Powered by Gemini API (minimal cost)

## 🎯 How It Works

1. **Upload Job Posting** - Take a screenshot of the LinkedIn job post
2. **Upload Your Resume** - Submit your resume (PDF, DOCX, or TXT)
3. **Generate Package** - Click generate and let AI do the work
4. **Review Results** - See your tailored resume, ATS score, and draft messages
5. **Download & Send** - Download resume PDF and copy message drafts

```
LinkedIn Job Post Screenshot → Gemini Vision API → Extract Job Details
                                                    ↓
Your Resume → Gemini Text API → Tailor Resume + ATS Score + Email Draft + LinkedIn Message
                                 ↓
                          Download Resume (PDF) + Copy Messages
```

## 🚀 Quick Start

### Option 1: Deploy to Streamlit Cloud (Recommended)

**Prerequisites:**
- GitHub account
- Google AI API key (from [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey))

**Steps:**

1. Fork this repository
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
3. Connect your GitHub account
4. Click "New app" and select this repository
5. Choose `streamlit_app.py` as the entry point
6. Add `GEMINI_API_KEY` in **Settings → Secrets**
7. Deploy! 🎉

Your app will be live at: `https://quickapply-ai-[your-name].streamlit.app`

### Option 2: Run Locally

**Prerequisites:**
- Python 3.8+
- Git

**Installation:**

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/quickapply-ai.git
cd quickapply-ai

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set API key
export GEMINI_API_KEY='your-api-key-here'

# Run app
streamlit run streamlit_app.py
```

Your app will be available at: `http://localhost:8501`

### Option 3: Deploy to Heroku

```bash
# Login to Heroku
heroku login

# Create Heroku app
heroku create your-app-name

# Set API key
heroku config:set GEMINI_API_KEY='your-api-key-here'

# Deploy
git push heroku main
```

## 📋 Project Structure

```
quickapply-ai/
├── streamlit_app.py              # Main Streamlit application
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── .gitignore                    # Git ignore file
└── utils/
    ├── __init__.py
    ├── image_processor.py        # Extract text from job post screenshots
    ├── resume_processor.py       # Process resume files (PDF, DOCX, TXT)
    ├── ai_generator.py          # Gemini API integration for all AI features
    └── pdf_generator.py         # Create formatted resume PDFs
```

## 🔑 Getting Your API Key

1. Visit [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Sign up or log in
3. Navigate to **API Keys**
4. Create a new API key
5. Copy and securely store it

**For Streamlit Cloud:**
- Add to **Settings → Secrets** as `GEMINI_API_KEY`

**For Local Development:**
```bash
export GEMINI_API_KEY='AIza...'
```

**For Heroku:**
```bash
heroku config:set GEMINI_API_KEY='AIza...'
```

## 💻 Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend | Streamlit |
| AI Engine | Gemini 2.0 Flash (Google AI) |
| Vision API | Gemini Vision (Image Analysis) |
| PDF Generation | FPDF2 |
| Document Processing | PyPDF2, python-docx |
| Hosting | Streamlit Cloud / Heroku |

## 📊 Cost Breakdown

| Service | Cost |
|---------|------|
| Streamlit Cloud | **FREE** (3 apps per account) |
| Google AI Gemini API | ~$0.003 per 1K input tokens |
| GitHub | **FREE** (public repos) |
| **Estimated Cost per Job** | **$0.05 - $0.10** |

## 🛠️ Configuration

### Local Development

Create `.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "AIza..."
```

### Streamlit Cloud

1. Go to your app settings
2. Click **Secrets**
3. Add:
```toml
GEMINI_API_KEY = "AIza..."
```

## 🔒 Security Best Practices

✅ **Do:**
- Keep API keys in environment variables
- Use `.gitignore` to prevent committing secrets
- Use Streamlit Secrets for production
- Keep dependencies updated
- Validate user uploads

❌ **Don't:**
- Commit API keys to Git
- Share API keys in public issues/discussions
- Use production keys in development
- Disable input validation

## 📦 Dependencies

All dependencies are listed in `requirements.txt`:

- **streamlit** - Web app framework
- **google-generativeai** - Gemini API client
- **pillow** - Image processing
- **PyPDF2** - PDF reading
- **python-docx** - DOCX file support
- **fpdf2** - PDF generation

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'google.generativeai'"

```bash
pip install -r requirements.txt
```

### "GEMINI_API_KEY not found"

Make sure you've set the environment variable:
```bash
export GEMINI_API_KEY='your-key-here'
# or
heroku config:set GEMINI_API_KEY='your-key-here'
```

### "Failed to extract job details from image"

- Ensure the screenshot is clear and readable
- Job posting should be visible in the image
- Try a higher resolution screenshot
- Ensure text is not blurry

### "PDF generation failed"

- Check that your resume has readable text
- Try a different resume format (PDF → TXT)
- Ensure resume is not corrupted

### "Failed to fetch" error

- Check your internet connection
- Verify API key is valid
- Check Google AI API status at [status.cloud.google.com](https://status.cloud.google.com)

## 📈 Future Enhancements

- [ ] Cover letter generation
- [ ] Interview question preparation
- [ ] Salary negotiation guides
- [ ] Application tracking integration
- [ ] Multiple resume templates
- [ ] Batch job processing
- [ ] Email integration for auto-sending
- [ ] Analytics dashboard
- [ ] Dark mode
- [ ] Multi-language support

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit (`git commit -m 'Add amazing feature'`)
5. Push (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## 📄 License

MIT License - feel free to use this project for personal or commercial purposes.

## ⭐ Support

If you found this helpful, please:
- ⭐ Star this repository
- 📤 Share with others
- 🐛 Report issues
- 💬 Suggest features

## 📧 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/quickapply-ai/issues)
- **Discussions**: [GitHub Discussions](https://github.com/YOUR_USERNAME/quickapply-ai/discussions)
- **Documentation**: See README sections above

## 🙏 Acknowledgments

Built with:
- [Gemini AI](https://ai.google.dev) by Google AI
- [Streamlit](https://streamlit.io) for the web framework
- [FPDF2](https://py-pdf.github.io/fpdf2/) for PDF generation

---

<div align="center">

**Made with ❤️ for job seekers everywhere**

[Streamlit Cloud](https://streamlit.io/cloud) • [Google AI API](https://ai.google.dev) • [GitHub](https://github.com)

</div>
