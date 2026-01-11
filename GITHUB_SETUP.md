# GitHub Repository Setup Instructions

## Option 1: Create Repository on GitHub (Recommended)

1. Go to https://github.com/new
2. Repository name: `squirrel`
3. Description: `A Raspberry Pi application to detect squirrels in camera view and trigger GPIO`
4. Visibility: **Public** (or Private if you prefer)
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

## Option 2: Create Personal Access Token (If Needed)

If authentication fails, create a Personal Access Token:

1. Go to https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Name: `Squirrel Project`
4. Expiration: Choose your preference
5. Scopes: Check **`repo`** (full control of private repositories)
6. Click "Generate token"
7. **Copy the token** (you won't see it again!)

## After Creating Repository

Once the repository is created on GitHub, run:

```bash
git push -u origin main
```

When prompted:
- Username: `McGr`
- Password: Use your **Personal Access Token** (not your GitHub password)

## Alternative: Use Token in URL (One-time)

If you have a PAT, you can use it directly:

```bash
git remote set-url origin https://McGr:YOUR_PAT@github.com/McGr/squirrel.git
git push -u origin main
```

Replace `YOUR_PAT` with your actual Personal Access Token.

## Current Git Status

✅ Git repository initialized
✅ Git user configured (McGr / mikemcgregor58@gmail.com)
✅ Initial commit created (2f20df1)
✅ Remote configured: https://github.com/McGr/squirrel.git
⏳ Waiting for repository creation on GitHub
