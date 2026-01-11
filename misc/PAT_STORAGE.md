# Personal Access Token (PAT) Storage Guide

## Important: PAT Security

**I will NOT remember your PAT** when you return to this project. Personal Access Tokens need to be stored securely and are not persisted in conversation history.

## Current Storage Method

Your PAT is currently stored in **Windows Credential Manager** (via `wincred` helper). This is secure and local to your machine.

### Verify Storage
```bash
git config credential.helper
# Should show: wincred
```

### View Stored Credentials
- Open **Credential Manager** (Windows)
- Search for: `git:https://github.com`
- Your GitHub credentials should be stored there

## Storage Options

### ✅ Recommended: Git Credential Helper (Current Setup)
**Status**: Already configured

Your PAT is stored in Windows Credential Manager:
- **Location**: Windows Credential Manager
- **Access**: `Control Panel` → `Credential Manager` → `Windows Credentials`
- **Look for**: `git:https://github.com`
- **Advantages**: 
  - Secure (encrypted by Windows)
  - Automatic (git uses it automatically)
  - No files to manage

### Option 2: Personal Access Token File (Local Only)

Store the PAT in a file that is **NOT committed to git**:

1. Create a file (e.g., `misc/.pat` or `.github-pat` in project root)
2. Add to `.gitignore`:
   ```
   .github-pat
   misc/.pat
   ```
3. Store token in the file
4. Use when needed: `cat .github-pat` or reference in scripts

**⚠️ Important**: Never commit this file!

### Option 3: Environment Variable

Set as system or user environment variable:
```powershell
# PowerShell (User level)
[System.Environment]::SetEnvironmentVariable('GITHUB_PAT', 'your-token-here', 'User')

# Or set in Windows Environment Variables GUI
# Control Panel → System → Advanced → Environment Variables
```

Then reference in scripts or git config if needed.

### Option 4: Password Manager

Store in a password manager like:
- Windows Credential Manager (already used)
- 1Password
- LastPass
- Bitwarden
- KeePass

Copy the token when needed for git operations.

## Your Current PAT Information

**Repository**: https://github.com/McGr/squirrel.git  
**Username**: McGr  
**PAT**: Currently stored in Windows Credential Manager

## When You Return

1. **Check if credentials are still stored**:
   ```bash
   git config credential.helper
   git push  # Will prompt if credentials expired
   ```

2. **If credentials expired or missing**:
   - Create a new PAT at: https://github.com/settings/tokens
   - Scope needed: `repo` (full control)
   - Use one of the storage methods above

3. **Test remote access**:
   ```bash
   git remote -v
   git fetch  # Test authentication
   ```

## Best Practices

1. ✅ **Use credential helper** (already set up - wincred)
2. ✅ **Never commit PATs** to git
3. ✅ **Store PATs securely** (encrypted storage)
4. ✅ **Use minimal scopes** (only `repo` for this project)
5. ✅ **Set expiration dates** on PATs (optional but recommended)
6. ✅ **Rotate PATs periodically** for security

## Token Expiration

PATs can expire if you set an expiration date. If you get authentication errors:
1. Go to https://github.com/settings/tokens
2. Check if your PAT is expired
3. Create a new one if needed
4. Update Windows Credential Manager with new token

## Quick Reference

**Create new PAT**: https://github.com/settings/tokens  
**Repository**: https://github.com/McGr/squirrel  
**View stored credentials**: Windows Credential Manager → `git:https://github.com`

---

**Note**: This file is tracked in git but doesn't contain actual tokens - it's just a guide for secure storage.
