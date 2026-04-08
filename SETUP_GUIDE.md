# 📚 Complete Setup & Deployment Guide

## 🎯 Overview

This guide will walk you through creating a GitHub repository and deploying QuickApply AI to Streamlit Cloud in 15 minutes.

---

## Step 1: Get Your API Key ⚙️

### Prerequisites
- Google AI account (free)

### Get API Key

1. Go to [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
2. Sign up or log in
3. Click **API Keys** in the left sidebar
4. Click **Create Key**
5. Copy your key (save it somewhere safe!)
6. ✅ You'll need this in Step 4

**API Key Format:** Should start with `AIza`

---

## Step 2: Create GitHub Repository 🐙

### Option A: Using GitHub Web Interface (Easiest)

1. Go to [github.com/new](https://github.com/new)
2. Fill in details:
   - **Repository name:** `quickapply-ai`
   - **Description:** "AI-powered job application assistant"
   - **Visibility:** Public (required for free Streamlit deployment)
3. Check "Add a README file"
4. Click **Create repository**

### Option B: Using Git CLI

```bash
# Initialize local repository
mkdir quickapply-ai
cd quickapply-ai
git init

# Create initial commit
echo "# QuickApply AI" > README.md
git add README.md
git commit -m "Initial commit"

# Add remote and push
git remote add origin https://github.com/YOUR_USERNAME/quickapply-ai.git
git branch -M main
git push -u origin main
```

✅ You now have a GitHub repository

---

## Step 3: Add Project Files 📁

### Option A: Upload via GitHub Web Interface

1. Go to your repository on GitHub
2. Click **Add file → Upload files**
3. Drag and drop these files:
   ```
   - streamlit_app.py
   - requirements.txt
   - README.md
   - .gitignore
   ```
4. Click **Commit changes**

### Option B: Using Git CLI

```bash
# Copy all files to your local repo folder
# Then:

cd quickapply-ai

# Add all files
git add .

# Commit
git commit -m "Add QuickApply AI application files"

# Push to GitHub
git push origin main
```

### Directory Structure

Ensure your GitHub repo looks like this:

```
quickapply-ai/
├── streamlit_app.py              ⭐ Main app file
├── requirements.txt              ⭐ Python dependencies
├── README.md                     ⭐ Project documentation
├── .gitignore                    ⭐ Git ignore file
└── utils/                        📁 Create this folder
    ├── __init__.py               (empty file)
    ├── image_processor.py
    ├── resume_processor.py
    ├── ai_generator.py
    └── pdf_generator.py
```

**How to create utils folder:**

1. In GitHub, click **Add file → Create new file**
2. Type: `utils/__init__.py`
3. Leave empty, click **Commit**
4. Repeat for each utility file

Or using Git:
```bash
mkdir utils
touch utils/__init__.py
# Copy Python files to utils/
git add utils/
git commit -m "Add utility modules"
git push
```

✅ All files are now in your GitHub repo

---

## Step 4: Deploy to Streamlit Cloud 🚀

### Prerequisites
- GitHub account (created above)
- Google AI API key (from Step 1)

### Deployment Steps

1. **Go to Streamlit Cloud**
   - Visit [streamlit.io/cloud](https://streamlit.io/cloud)
   - Click **Sign in with GitHub**
   - Authorize Streamlit

2. **Create New App**
   - Click **New app**
   - Select your GitHub repo: `YOUR_USERNAME/quickapply-ai`
   - Branch: `main`
   - Main file path: `streamlit_app.py`

3. **Add Secrets**
   - Click **Advanced settings**
   - Scroll to **Secrets**
   - Paste your API key:
   ```
   GEMINI_API_KEY = "AIzaxxx..."
   ```

4. **Deploy**
   - Click **Deploy**
   - Wait 2-3 minutes for deployment
   - Your app will be live! 🎉

### Your Live App URL

Once deployed, your app will be available at:
```
https://quickapply-ai-[your-username].streamlit.app
```

✅ Your app is now live and accessible to everyone!

---

## Step 5: Test Your App ✅

### Test Checklist

- [ ] App loads without errors
- [ ] Can upload job posting screenshot
- [ ] Can upload resume file (PDF/DOCX/TXT)
- [ ] Generate button works
- [ ] ATS score displays correctly
- [ ] Can view all tabs (Resume, ATS, Email, LinkedIn)
- [ ] Download PDF button works
- [ ] Copy buttons work

### Troubleshooting

If app won't load:

1. **Check Streamlit Cloud logs**
   - Click **Manage app**
   - View **Logs** tab
   - Look for error messages

2. **Verify API Key**
   - Go to **Settings → Secrets**
   - Check API key is correct
   - No quotes needed!

3. **Check Dependencies**
   - Verify `requirements.txt` is in root
   - All package names are correct

---

## Step 6: Share & Use! 📢

### Share Your App

1. **Get your app link:** `https://quickapply-ai-[username].streamlit.app`
2. **Share with friends:**
   - LinkedIn
   - Email
   - GitHub Issues
   - Social media

### Features to Highlight

- 📸 Upload LinkedIn job post
- 📄 Upload your resume
- ✨ AI tailors resume automatically
- 📊 Get ATS score instantly
- 📧 Generate email draft
- 💼 Generate LinkedIn message
- 📥 Download resume PDF
- ⚡ Works instantly, no waiting

---

## 🔧 Maintenance & Updates

### Making Updates

1. **Make changes locally** (or directly on GitHub)
   ```bash
   # Local changes
   git commit -am "Update feature X"
   git push origin main
   ```

2. **Streamlit auto-deploys**
   - Changes appear within 1-2 minutes
   - Check deployment status in app dashboard

3. **View deployment logs**
   - Click **Manage app** in Streamlit Cloud
   - Check **Logs** tab

### Update Dependencies

If you add new packages:

```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update dependencies"
git push
```

---

## 💰 Cost & Limits

### Free Tier (Streamlit Cloud)

✅ **What's Included:**
- 3 public apps per account
- Unlimited traffic
- Auto-scaling
- Custom domain support
- 1 GB workspace per app

⚠️ **Limits:**
- Apps sleep after 7 days of inactivity
- Memory: 1 GB
- CPU: 1 CPU

### Gemini API Costs

📊 **Pricing:**
- Input: $3 per 1M tokens
- Output: $15 per 1M tokens
- **Per app usage: ~$0.05-0.10**

**Example:**
- 1 resume tailoring = ~3,000 tokens
- Cost = ~$0.01

### Free Tier Estimate
- Can run ~100 apps/month for free
- Or pay ~$5-10/month for unlimited usage

---

## 🔒 Security Checklist

Before sharing publicly:

- [ ] API key is NOT in any file (use Secrets)
- [ ] `.gitignore` excludes sensitive files
- [ ] Repository is public (required for Streamlit)
- [ ] No credentials in commit history
- [ ] API key rotation is enabled (Google AI)

---

## 📱 Advanced Customization

### Change App Name/Appearance

Edit `.streamlit/config.toml` (create if needed):

```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[browser]
gatherUsageStats = false

[client]
showErrorDetails = false

[logger]
level = "error"
```

Push to GitHub to apply changes.

### Add Custom Domain

In Streamlit Cloud:
1. **Manage app → Settings**
2. **Custom domain**
3. Add your domain and CNAME record

---

## 🆘 Support & Help

### Getting Help

1. **Check logs**
   - Streamlit Cloud → Logs
   - Look for error messages

2. **Common issues**
   - Missing API key: Check Secrets
   - Import errors: Check requirements.txt
   - File not found: Check file paths are correct

3. **Google AI Documentation**
   - [API Docs](https://ai.google.dev)
   - [API Console](https://aistudio.google.com/app/apikey)

4. **Streamlit Documentation**
   - [Docs](https://docs.streamlit.io)
   - [Community](https://discuss.streamlit.io)

---

## ✨ Next Steps

After successful deployment:

1. ⭐ Star this repo on GitHub
2. 📢 Share with friends
3. 💬 Suggest features in Issues
4. 🐛 Report bugs
5. 🤝 Contribute improvements

---

## 📝 Quick Reference

### Important Links

| Service | URL |
|---------|-----|
| Streamlit Cloud | https://streamlit.io/cloud |
| Google AI Console | https://aistudio.google.com/app/apikey |
| GitHub | https://github.com |
| Streamlit Docs | https://docs.streamlit.io |
| Google AI Docs | https://ai.google.dev |

### Key Commands

```bash
# Local testing
streamlit run streamlit_app.py

# Update requirements
pip freeze > requirements.txt

# Git workflow
git add .
git commit -m "Message"
git push origin main

# Check Python version
python --version
```

### File Checklist

```
✅ streamlit_app.py
✅ requirements.txt
✅ README.md
✅ .gitignore
✅ utils/__init__.py
✅ utils/image_processor.py
✅ utils/resume_processor.py
✅ utils/ai_generator.py
✅ utils/pdf_generator.py
```

---

## 🎉 Congratulations!

You've successfully:
- ✅ Created a GitHub repository
- ✅ Added QuickApply AI code
- ✅ Deployed to Streamlit Cloud
- ✅ Shared with the world

**Your app is now live and ready to help job seekers! 🚀**

---

**Need help?** Check the [GitHub Issues](https://github.com/YOUR_USERNAME/quickapply-ai/issues) or create a new issue.

**Found a bug?** Report it [here](https://github.com/YOUR_USERNAME/quickapply-ai/issues/new).

**Have a feature idea?** Share it in [Discussions](https://github.com/YOUR_USERNAME/quickapply-ai/discussions).

---

Made with ❤️ for job seekers everywhere
