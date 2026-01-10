# Commit Message and Log Files

## Files Created

### 1. COMMIT_MESSAGE.txt (Git Ignored)
This file contains the commit message for the initial project setup. It's formatted as a conventional commit message and can be used directly with `git commit -F COMMIT_MESSAGE.txt`.

**Location**: `COMMIT_MESSAGE.txt` (ignored by git, not committed)

**Usage**:
```bash
git commit -F COMMIT_MESSAGE.txt
```

Or copy the contents for a manual commit:
```bash
git commit -m "$(cat COMMIT_MESSAGE.txt)"
```

### 2. COMMIT_LOG.md (Git Ignored)
This file maintains a log of all commits for future reference. It includes:
- The initial commit message with full details
- Template for future commits
- Section to track upcoming commits

**Location**: `COMMIT_LOG.md` (ignored by git, not committed)

**Purpose**: Track commit history locally for documentation and reference.

### 3. CHANGELOG.md (Committed to Repository)
Standard changelog file following Keep a Changelog format. This is a standard project file and WILL be committed to the repository.

**Location**: `CHANGELOG.md` (committed to git)

**Purpose**: Track versioned changes for users and contributors.

## Quick Start

To use the commit message:

```bash
# Option 1: Use the file directly
git add .
git commit -F COMMIT_MESSAGE.txt

# Option 2: Copy and paste the message
cat COMMIT_MESSAGE.txt  # View the message
# Then manually commit with the message

# Option 3: Use git commit with the message content
git commit -m "feat: Initial project setup - Squirrel Detector for Raspberry Pi" \
  -m "Complete Squirrel Detector project implementation with cross-platform support..." \
  # (continue with rest of message)
```

## Future Commits

For future commits, add entries to `COMMIT_LOG.md` to track what was changed. This helps maintain a local history of commits and their purposes.

The `CHANGELOG.md` file should be updated with versioned changes and WILL be committed to the repository as it's a standard project file.
