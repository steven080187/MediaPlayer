# GitHub Setup Guide - Get Your APK

## Step 1: Create GitHub Account
1. Go to https://github.com/signup
2. Create a free account (if you don't have one)

## Step 2: Create a New Repository
1. Go to https://github.com/new
2. Repository name: `private-player-android` (or whatever you want)
3. Choose: **Private** (recommended for privacy)
4. DON'T initialize with README, .gitignore, or license
5. Click "Create repository"

## Step 3: Push Your Code

GitHub will show you commands. Use these instead:

```bash
cd ~/PornApp-android

# Add the remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/private-player-android.git

# Push the code
git branch -M main
git push -u origin main
```

When prompted, use your GitHub username and a **Personal Access Token** (not password):
- Go to: https://github.com/settings/tokens
- Click "Generate new token (classic)"
- Give it a name like "PornApp Build"
- Check: `repo` (full control)
- Generate and copy the token
- Use this token as your password when pushing

## Step 4: Wait for Build

1. Go to your repository on GitHub
2. Click "Actions" tab
3. You'll see the build running (takes ~10-15 minutes)
4. When it's done (green checkmark ✓), click the workflow run
5. Scroll down to "Artifacts" section
6. Download `android-apk`
7. Extract the .apk file

## Step 5: Install on Android

1. Copy the APK to your Android phone
2. Open it to install
3. You may need to enable "Install from Unknown Sources" in Settings

## Troubleshooting

**Build fails?**
- Check the "Actions" tab for error logs
- The first build might fail - just click "Re-run jobs"

**Can't push to GitHub?**
- Make sure you're using a Personal Access Token, not your password
- Double-check the repository URL

**Need help?**
Let me know what error you're seeing!

## Alternative: Manual Build Trigger

After pushing your code, you can manually trigger builds:
1. Go to "Actions" tab
2. Click "Build Android APK" workflow
3. Click "Run workflow" button
4. Select "main" branch
5. Click green "Run workflow" button
