# Direct Deployment to Hugging Face (No GitHub Linking Required)

This method pushes directly to Hugging Face Spaces - much simpler!

## ✅ What You Need

- Your Hugging Face Space already created (you're done with Step 4)
- Git initialized in your project
- Your code committed locally

---

## Step 1: Get Your Hugging Face Access Token

1. Go to: https://huggingface.co/settings/tokens
2. Click **"New token"**
3. Fill in:
   - **Name**: `commuter-agent-deploy` (or any name)
   - **Type**: Select **"Write"** ⚠️ (Important: Must be Write, not Read)
4. Click **"Generate token"**
5. **COPY THE TOKEN IMMEDIATELY** - it looks like: `hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - You won't see it again, so save it somewhere safe!

---

## Step 2: Push Directly to Hugging Face

Open PowerShell in your project directory and run these commands:

```powershell
# Make sure you're in the project directory
cd "C:\Users\Dell\OneDrive\Desktop\7th Semester\SPM\Project\CommuterAgent"

# Add Hugging Face as a remote
# Replace YOUR_USERNAME with your Hugging Face username
# Replace YOUR_TOKEN with the token you just copied
git remote add hf https://YOUR_USERNAME:YOUR_TOKEN@huggingface.co/spaces/YOUR_USERNAME/commuter-agent

# Push your code
git push hf main
```

**Example** (replace with your actual values):
```powershell
git remote add hf https://johndoe:hf_abc123xyz456@huggingface.co/spaces/johndoe/commuter-agent
git push hf main
```

**Note**: If you get "remote already exists" error:
```powershell
git remote remove hf
# Then add it again with the command above
```

---

## Step 3: Add Your Google Maps API Key

1. Go to your Hugging Face Space: https://huggingface.co/spaces/YOUR_USERNAME/commuter-agent
2. Click **"Settings"** tab
3. Scroll down to **"Repository secrets"** section
4. Click **"New secret"**
5. Fill in:
   - **Name**: `GOOGLE_MAPS_API_KEY` (exactly this, case-sensitive)
   - **Value**: Paste your actual Google Maps API key
6. Click **"Add secret"**

---

## Step 4: Wait for Build

1. Go to your Space's **"Logs"** tab
2. You should see the build starting automatically
3. Wait 2-5 minutes
4. Look for "Build successful" message

---

## Step 5: Test Your Deployment

Once built, your agent will be at:
```
https://YOUR_USERNAME-commuter-agent.hf.space
```

**Test the health endpoint:**
```
https://YOUR_USERNAME-commuter-agent.hf.space/health
```

Should return:
```json
{
  "status": "ok",
  "agent_name": "commuter-agent",
  "ready": true
}
```

---

## 🔧 Troubleshooting

### "Authentication failed" or "Permission denied"
- Make sure you're using the **Access Token** (starts with `hf_`), not your password
- Token must have **"Write"** permissions
- Check your username is correct

### "Remote already exists"
```powershell
git remote remove hf
# Then add it again
```

### Build fails
- Check the **"Logs"** tab in your Space
- Make sure all files are committed: `git status`
- Verify `requirements.txt` has all dependencies

### Can't find your Space URL
- Go to: https://huggingface.co/spaces
- Find your space in the list
- The URL format is: `https://huggingface.co/spaces/YOUR_USERNAME/SPACE_NAME`

---

## 📝 Updating Your Deployment

After making code changes:

```powershell
git add .
git commit -m "Your update description"
git push hf main
```

Hugging Face will automatically rebuild!

---

## 🎯 Quick Command Reference

```powershell
# One-time setup (replace YOUR_USERNAME and YOUR_TOKEN)
git remote add hf https://YOUR_USERNAME:YOUR_TOKEN@huggingface.co/spaces/YOUR_USERNAME/commuter-agent

# Push your code
git push hf main

# Update later
git add .
git commit -m "Update"
git push hf main
```
