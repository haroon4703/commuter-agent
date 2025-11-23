# Deployment Guide: Commuter Agent to Hugging Face Spaces

This guide will walk you through deploying your Commuter Agent to Hugging Face Spaces.

## Prerequisites

- GitHub account
- Hugging Face account (sign up at https://huggingface.co/)
- Git installed on your computer
- Your project files ready

## Step 1: Initialize Git Repository

If you haven't already initialized git in your project:

```bash
# Navigate to your project directory
cd "C:\Users\Dell\OneDrive\Desktop\7th Semester\SPM\Project\CommuterAgent"

# Initialize git repository
git init

# Add all files (except those in .gitignore)
git add .

# Create initial commit
git commit -m "Initial commit: Commuter Agent"
```

## Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Create a new repository:
   - **Repository name**: `commuter-agent` (or any name you prefer)
   - **Description**: "AI Commuter Assistance Agent built with LangGraph and FastAPI"
   - **Visibility**: Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
3. Click "Create repository"

## Step 3: Push to GitHub

After creating the repository, GitHub will show you commands. Use these:

```bash
# Add your GitHub repository as remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/commuter-agent.git

# Rename main branch if needed (GitHub uses 'main' by default)
git branch -M main

# Push your code to GitHub
git push -u origin main
```

**Note**: You may be prompted to authenticate. Use a Personal Access Token if needed.

## Step 4: Set Up Hugging Face Space

1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Fill in the details:
   - **Space name**: `commuter-agent` (or your preferred name)
   - **SDK**: Select **Docker** (we'll use Docker for FastAPI)
   - **Visibility**: Public or Private
   - **Hardware**: CPU Basic (free) or upgrade if needed
4. Click "Create Space"

## Step 5: Configure Hugging Face Space

### Option A: Connect GitHub Repository (Recommended)

1. In your Hugging Face Space settings, go to "Repository" tab
2. Click "Import from GitHub"
3. Select your repository: `YOUR_USERNAME/commuter-agent`
4. Click "Import"

### Option B: Manual Setup

If you prefer to set up manually:

1. In your Hugging Face Space, you'll see instructions to clone the repository
2. Clone it locally:
   ```bash
   git clone https://huggingface.co/spaces/YOUR_USERNAME/commuter-agent
   cd commuter-agent
   ```
3. Copy all your project files to this directory
4. Commit and push:
   ```bash
   git add .
   git commit -m "Add commuter agent files"
   git push
   ```

## Step 6: Add Environment Variables (API Keys)

1. In your Hugging Face Space, go to "Settings" → "Repository secrets"
2. Add your Google Maps API key:
   - **Name**: `GOOGLE_MAPS_API_KEY`
   - **Value**: Your actual API key
3. Click "Add secret"

**Note**: Hugging Face Spaces will automatically make these available as environment variables.

## Step 7: Update Dockerfile for Hugging Face

Hugging Face Spaces uses port 7860 by default. Make sure your Dockerfile is set up correctly. The current Dockerfile should work, but we'll verify it uses the PORT environment variable.

## Step 8: Wait for Deployment

1. After pushing your code, Hugging Face will automatically build and deploy
2. You can monitor the build logs in the "Logs" tab
3. Once deployed, your agent will be available at:
   `https://YOUR_USERNAME-commuter-agent.hf.space`

## Step 9: Test Your Deployment

1. Visit your Space URL
2. Test the health endpoint: `https://YOUR_USERNAME-commuter-agent.hf.space/health`
3. Test the main endpoint: `https://YOUR_USERNAME-commuter-agent.hf.space/commuter-agent`

## Troubleshooting

### Build Fails
- Check the logs in Hugging Face Space
- Ensure all dependencies are in `requirements.txt`
- Verify Dockerfile is correct

### API Key Not Working
- Check that the secret is named exactly `GOOGLE_MAPS_API_KEY`
- Verify the API key is valid
- Check logs for error messages

### Port Issues
- Hugging Face uses port 7860, but FastAPI apps should use the PORT environment variable
- The app.py file handles this automatically

## Updating Your Deployment

To update your deployed agent:

```bash
# Make changes to your code
git add .
git commit -m "Update agent"
git push
```

Hugging Face will automatically rebuild and redeploy.

