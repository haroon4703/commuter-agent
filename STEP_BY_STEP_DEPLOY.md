# Step-by-Step Deployment Guide

Follow these steps in order to deploy your Commuter Agent to Hugging Face Spaces.

## 📋 Prerequisites Checklist

- [ ] GitHub account (create at https://github.com/signup)
- [ ] Hugging Face account (create at https://huggingface.co/join)
- [ ] Git installed (check with `git --version`)
- [ ] Your Google Maps API key ready

---

## Step 1: Initialize Git Repository

Open PowerShell in your project directory and run:

```powershell
# Make sure you're in the project directory
cd "C:\Users\Dell\OneDrive\Desktop\7th Semester\SPM\Project\CommuterAgent"

# Initialize git repository
git init

# Add all files
git add .

# Create your first commit
git commit -m "Initial commit: Commuter Agent with LangGraph and FastAPI"
```

---

## Step 2: Create GitHub Repository

1. **Go to GitHub**: https://github.com/new
2. **Repository name**: `commuter-agent` (or any name you like)
3. **Description**: "AI Commuter Assistance Agent - Route planning, traffic updates, and travel mode suggestions"
4. **Visibility**: 
   - Choose **Public** (free, anyone can see)
   - Or **Private** (only you can see)
5. **IMPORTANT**: 
   - ❌ Do NOT check "Add a README file"
   - ❌ Do NOT check "Add .gitignore"
   - ❌ Do NOT check "Choose a license"
6. Click **"Create repository"**

---

## Step 3: Connect Local Repository to GitHub

After creating the repository, GitHub will show you commands. Use these in PowerShell:

```powershell
# Replace YOUR_USERNAME with your actual GitHub username
git remote add origin https://github.com/YOUR_USERNAME/commuter-agent.git

# Rename branch to 'main' (GitHub's default)
git branch -M main

# Push your code to GitHub
git push -u origin main
```

**Authentication**: 
- If prompted for username/password, use:
  - **Username**: Your GitHub username
  - **Password**: Use a **Personal Access Token** (not your GitHub password)
  - Create token at: https://github.com/settings/tokens
  - Select scope: `repo` (full control of private repositories)

---

## Step 4: Create Hugging Face Space

1. **Go to Hugging Face Spaces**: https://huggingface.co/spaces
2. Click **"Create new Space"** button (top right)
3. Fill in the form:
   - **Space name**: `commuter-agent` (or your preferred name)
   - **SDK**: Select **"Docker"** ⚠️ (Important: Must be Docker for FastAPI)
   - **Visibility**: Public or Private
   - **Hardware**: 
     - **CPU basic** (free tier - sufficient for this project)
     - Or upgrade if you need more resources
4. Click **"Create Space"**

---

## Step 5: Connect GitHub Repository to Hugging Face

### Option A: Import from GitHub (Easiest)

1. In your Hugging Face Space, go to **"Settings"** tab
2. Scroll to **"Repository"** section
3. Click **"Import from GitHub"**
4. Select your repository: `YOUR_USERNAME/commuter-agent`
5. Click **"Import"**
6. Wait for files to sync (may take a minute)

### Option B: Manual Push (Alternative)

If Option A doesn't work, you can push directly:

```powershell
# Add Hugging Face as a remote
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/commuter-agent

# Push to Hugging Face
git push hf main
```

**Note**: You'll need to authenticate with Hugging Face. Use your access token from: https://huggingface.co/settings/tokens

---

## Step 6: Add Google Maps API Key

1. In your Hugging Face Space, go to **"Settings"** tab
2. Scroll to **"Repository secrets"** section
3. Click **"New secret"**
4. Fill in:
   - **Name**: `GOOGLE_MAPS_API_KEY` (exactly this name, case-sensitive)
   - **Value**: Paste your actual Google Maps API key
5. Click **"Add secret"**

**Important**: The secret name must match exactly: `GOOGLE_MAPS_API_KEY`

---

## Step 7: Wait for Deployment

1. After connecting GitHub or pushing code, Hugging Face will automatically:
   - Detect your Dockerfile
   - Build your Docker image
   - Deploy your application

2. **Monitor the build**:
   - Go to **"Logs"** tab in your Space
   - Watch for build progress
   - Look for "Build successful" message

3. **Typical build time**: 2-5 minutes

---

## Step 8: Test Your Deployed Agent

Once deployed, your agent will be available at:

```
https://YOUR_USERNAME-commuter-agent.hf.space
```

### Test Health Endpoint:
```
https://YOUR_USERNAME-commuter-agent.hf.space/health
```

Expected response:
```json
{
  "status": "ok",
  "agent_name": "commuter-agent",
  "ready": true
}
```

### Test Main Endpoint:
Use a tool like Postman, curl, or the browser to test:

**URL**: `https://YOUR_USERNAME-commuter-agent.hf.space/commuter-agent`  
**Method**: POST  
**Headers**: `Content-Type: application/json`  
**Body**:
```json
{
  "messages": [
    {
      "role": "user",
      "content": "What's the best route to downtown?"
    }
  ]
}
```

---

## 🔧 Troubleshooting

### Build Fails
- **Check logs**: Go to "Logs" tab in Hugging Face Space
- **Common issues**:
  - Missing dependencies in `requirements.txt`
  - Dockerfile errors
  - Port configuration issues

### API Key Not Working
- Verify secret name is exactly: `GOOGLE_MAPS_API_KEY`
- Check that API key is valid
- Review logs for error messages
- Ensure Google Maps APIs are enabled in Google Cloud Console

### Port Issues
- Hugging Face uses port 7860 by default
- Our Dockerfile uses `${PORT:-7860}` which should work automatically
- If issues persist, check Dockerfile CMD line

### Authentication Errors
- For GitHub: Use Personal Access Token, not password
- For Hugging Face: Use Access Token from settings
- Ensure tokens have correct permissions

---

## ✅ Success Checklist

- [ ] Git repository initialized
- [ ] Code pushed to GitHub
- [ ] Hugging Face Space created
- [ ] GitHub repository connected to Space
- [ ] API key added as secret
- [ ] Build completed successfully
- [ ] Health endpoint returns 200 OK
- [ ] Main endpoint responds correctly

---

## 🎉 You're Done!

Your Commuter Agent is now live on Hugging Face Spaces! 

**Next Steps**:
- Share your Space URL with others
- Monitor usage in Hugging Face dashboard
- Update code by pushing to GitHub (auto-deploys)

---

## 📝 Updating Your Deployment

To update your agent after making changes:

```powershell
# Make your code changes
# Then commit and push:
git add .
git commit -m "Description of changes"
git push
```

Hugging Face will automatically detect the changes and rebuild!

