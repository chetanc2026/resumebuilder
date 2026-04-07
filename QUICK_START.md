# ⚡ QuickApply AI - 15-Minute Quick Start

## 📋 What You're Getting

A complete, production-ready Streamlit app that:
- Extracts job details from LinkedIn screenshots using Claude Vision
- Tailors resumes to job requirements
- Calculates ATS compatibility scores
- Generates professional email drafts
- Creates LinkedIn outreach messages
- Exports formatted PDF resumes

**Everything is included. Just add your API key and deploy!**

---

## 🚀 Deployment in 5 Steps

### Step 1: Get Anthropic API Key (2 minutes)
1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign up with email or Google
3. Click "API Keys" → "Create Key"
4. Copy the key (starts with `sk-ant-`)
5. **Save it somewhere safe!**

### Step 2: Create GitHub Repo (2 minutes)
1. Go to [github.com/new](https://github.com/new)
2. Name it: `quickapply-ai`
3. Select "Public"
4. Click "Create repository"

### Step 3: Add Files to GitHub (3 minutes)

**Method A: Web Upload (Easiest)**
1. In your GitHub repo, click "Add file" → "Upload files"
2. Select all files provided:
   - streamlit_app.py
   - requirements.txt
   - .gitignore
   - README.md
3. Click "Commit changes"

**Method B: Create Folder Structure**
1. Click "Add file" → "Create new file"
2. Type: `utils/__init__.py` (empty file)
3. Repeat for each file in `utils/`:
   - utils/image_processor.py
   - utils/resume_processor.py
   - utils/ai_generator.py
   - utils/pdf_generator.py

### Step 4: Deploy to Streamlit Cloud (5 minutes)

1. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
2. Click "Sign in with GitHub"
3. Click "New app"
4. Select:
   - Repository: `your-username/quickapply-ai`
   - Branch: `main`
   - File: `streamlit_app.py`
5. Click "Advanced settings" → "Secrets"
6. Add this:
   ```
   ANTHROPIC_API_KEY = "sk-ant-YOUR_KEY_HERE"
   ```
7. Click "Deploy"
8. Wait 2-3 minutes ✨

### Step 5: Test & Share (3 minutes)

Your app is live at: `https://quickapply-ai-YOUR_USERNAME.streamlit.app`

**Test it:**
1. Upload a LinkedIn job post screenshot
2. Upload your resume
3. Click "Generate"
4. See results! 🎉

---

## 📁 File Structure (Copy Exactly!)

```
your-github-repo/
├── streamlit_app.py          ← Main app
├── requirements.txt          ← Dependencies
├── README.md                 ← Documentation
├── .gitignore               ← Git ignore
└── utils/                   ← Create this folder
    ├── __init__.py          ← Empty file
    ├── image_processor.py   ← Extract job details
    ├── resume_processor.py  ← Read resume files
    ├── ai_generator.py      ← Claude API calls
    └── pdf_generator.py     ← Create PDF
```

---

## 🔍 Important Notes

### ✅ DO:
- Keep API key in Streamlit Secrets (not in code)
- Use a **public** GitHub repository
- Commit all files exactly as provided
- Test the app after deployment

### ❌ DON'T:
- Put API key in any file
- Use a private GitHub repository
- Rename files or folders
- Change import statements

---

## 🛠️ Troubleshooting

### "App won't load"
1. Check [Streamlit Cloud Logs](https://share.streamlit.io)
2. Go to "Manage App" → "Logs"
3. Look for red error messages

### "ANTHROPIC_API_KEY not found"
1. Go to Streamlit Cloud dashboard
2. Click your app
3. Click "Settings"
4. Add the key to "Secrets"

### "ModuleNotFoundError"
1. Check all files are in right place
2. Verify `utils/` folder exists
3. Verify `requirements.txt` is in root

### "Failed to extract job details"
1. Ensure screenshot is clear
2. Job posting text should be readable
3. Try higher resolution image

---

## 💰 Cost Estimate

| Service | Cost |
|---------|------|
| Streamlit Cloud | **FREE** |
| GitHub | **FREE** |
| Claude API | ~$0.05-0.10 per app |
| **Total Monthly** | **$1-3** (for 20-60 apps) |

---

## 📱 Using the App

### For Job Seekers:
1. Find job on LinkedIn
2. Take screenshot
3. Upload screenshot + resume
4. Click "Generate"
5. Get:
   - Tailored resume
   - ATS score
   - Email draft
   - LinkedIn message
   - Downloadable PDF

### Expected Results:
- Processing time: 30-60 seconds
- ATS score: 60-95%
- Email: 150-200 words
- LinkedIn message: 50-100 words

---

## 🔐 Security

Your API key:
- Never stored in code
- Never visible in Git history
- Only accessible to you in Streamlit Cloud
- Can be rotated anytime

---

## 📚 What Each File Does

| File | Purpose |
|------|---------|
| `streamlit_app.py` | Main application UI and logic |
| `requirements.txt` | Python package versions |
| `utils/image_processor.py` | Extracts job details from screenshots |
| `utils/resume_processor.py` | Reads PDF/DOCX/TXT resumes |
| `utils/ai_generator.py` | Calls Claude API for all AI features |
| `utils/pdf_generator.py` | Creates formatted resume PDFs |
| `.gitignore` | Prevents committing secrets |
| `README.md` | Project documentation |

---

## ✨ Features Explained

### 📸 Job Extraction
- Reads LinkedIn job post screenshot
- Extracts: title, company, requirements, skills
- Uses Claude Vision API

### ✏️ Resume Tailoring
- Reads your resume
- Matches it to job requirements
- Emphasizes relevant skills
- Maintains original format

### 📊 ATS Scoring
- Calculates compatibility 0-100%
- Shows keywords found/missing
- Suggests improvements
- Helps beat automated screening

### 📧 Email Generation
- Creates professional application email
- References the specific job
- Mentions relevant qualifications
- Ready to copy and send

### 💼 LinkedIn Messages
- Personalized connection request
- Shows interest in role
- Mentions company/job details
- Friendly and professional tone

### 📥 PDF Export
- Downloads formatted resume
- Professional styling
- Maintains structure
- One-click download

---

## 🌐 Accessing Your App

### After Deployment:
- **App URL:** `https://quickapply-ai-YOUR_USERNAME.streamlit.app`
- **Share with:** Copy link to friends
- **No login needed:** Anyone can use it
- **100% free:** For your users

---

## 📞 Getting Help

1. **Error messages?** Check the logs in Streamlit Cloud
2. **API key issues?** Verify in Secrets section
3. **File errors?** Check folder structure matches above
4. **Other issues?** Check [Streamlit Docs](https://docs.streamlit.io)

---

## 🎯 Next Steps

1. ✅ Get API key
2. ✅ Create GitHub repo
3. ✅ Add files
4. ✅ Deploy to Streamlit
5. ✅ Test the app
6. ✅ Share the link!
7. ✅ Celebrate! 🎉

---

## 📋 Deployment Checklist

- [ ] Anthropic API key created
- [ ] GitHub account ready
- [ ] GitHub repo created (public)
- [ ] All files uploaded to GitHub
- [ ] Streamlit Cloud account created
- [ ] App deployed
- [ ] API key added to Secrets
- [ ] App is loading
- [ ] Tested with sample files
- [ ] App URL working
- [ ] Shared with friends

---

## 💡 Tips for Best Results

**For Job Posts:**
- Use clear, high-resolution screenshots
- Ensure text is readable
- Include full job description
- Screenshot should show job title and company

**For Resumes:**
- Use PDF or DOCX format
- Ensure text is readable (not scanned image)
- Include relevant experience and skills
- Update before uploading

**For ATS Scores:**
- Aim for 80%+ score
- Add missing keywords naturally
- Highlight relevant achievements
- Use job-specific terminology

---

## 🚀 You're Ready!

Everything you need is provided. Follow the 5 steps above and your app will be live in 15 minutes!

**Questions?** Check the main README.md file for more details.

**Ready to deploy?** Start with Step 1! 🎯

---

Made with ❤️ for job seekers everywhere
