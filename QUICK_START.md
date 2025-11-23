# Quick Start: Deploy to Hugging Face

## 🚀 Quick Deployment Steps

### 1. Initialize Git (if not done)
```bash
git init
git add .
git commit -m "Initial commit"
```

### 2. Create GitHub Repo & Push
```bash
# Create repo on GitHub first, then:
git remote add origin https://github.com/YOUR_USERNAME/commuter-agent.git
git branch -M main
git push -u origin main
```

### 3. Create Hugging Face Space
1. Go to: https://huggingface.co/spaces
2. Click "Create new Space"
3. Select **Docker** SDK
4. Name it: `commuter-agent`
5. Click "Create"

### 4. Connect GitHub (Recommended)
- In Space Settings → Repository → Import from GitHub
- Select your repo
- Click "Import"

### 5. Add API Key
- Space Settings → Repository secrets
- Add: `GOOGLE_MAPS_API_KEY` = your key

### 6. Done! 🎉
Your agent will auto-deploy at:
`https://YOUR_USERNAME-commuter-agent.hf.space`

---

**Full guide**: See `DEPLOYMENT.md` for detailed instructions.

