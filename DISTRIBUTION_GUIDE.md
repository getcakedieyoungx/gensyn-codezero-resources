# GitHub Push Instructions

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `gensyn-codezero-resources` (or your preferred name)
3. Description: "Community resources and guides for Gensyn's CodeZero cooperative AI network"
4. Set to **Public**
5. **DO NOT** initialize with README (we already have one)
6. Click "Create repository"

## Step 2: Push to GitHub

After creating the repo, run these commands:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/gensyn-codezero-resources.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

## Step 3: Verify

Go to your repository URL and verify all files are there:
- README.md
- codezero_log_guide.md
- twitter_thread.txt
- devto_blog_post.md
- .gitignore

---

## Distribution Checklist

### Twitter Thread
✅ File ready: `twitter_thread.txt`
- Copy tweets 1-10
- Replace `[GITHUB LINK HERE]` in tweet 10 with your repo URL
- Post as thread on Twitter/X
- Tag @gensynai

### Dev.to Blog Post
✅ File ready: `devto_blog_post.md`
- Go to https://dev.to/new
- Copy entire content from `devto_blog_post.md`
- Add cover image (optional)
- Tags already set: gensyn, depin, ai, blockchain
- Publish!

### Discord
After GitHub is live:
- Post in #codezero-discussion or #technical-support
- Use this message:

```
Hey everyone! 👋

I created a technical guide for node runners who are confused about their logs:
**"How to Read Your CodeZero Logs: Are You Actually Learning?"**

📊 Covers:
- What "Policy Update" actually means
- How to know if you're getting rewards
- Healthy vs unhealthy log patterns
- Troubleshooting common issues

GitHub: [YOUR_REPO_URL]

Hope this helps some folks debug their nodes! Let me know if I got anything wrong or if you want me to add more sections.
```
