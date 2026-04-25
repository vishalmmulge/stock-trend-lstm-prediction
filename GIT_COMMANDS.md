# Git Commands Quick Reference

## Initial Setup (One Time Only)

```bash
# Navigate to your project folder
cd c:\Users\visha\Desktop\LIFE\stock-trend-lstm

# Configure Git (replace with your info)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Initialize repository
git init

# Add all files
git add .

# First commit
git commit -m "Initial commit: LSTM Stock Trend Prediction Project"

# Connect to GitHub (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/stock-trend-lstm-prediction.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Updating Your Project (After Making Changes)

```bash
# Check what files changed
git status

# Add all changed files
git add .

# Or add specific files
git add filename.py

# Commit with a message
git commit -m "Description of what you changed"

# Push to GitHub
git push
```

## Common Scenarios

### Scenario 1: Added new features
```bash
git add .
git commit -m "Added new feature: swing trading recommendations"
git push
```

### Scenario 2: Fixed bugs
```bash
git add .
git commit -m "Fixed bug in data preprocessing"
git push
```

### Scenario 3: Updated README
```bash
git add README.md
git commit -m "Updated documentation"
git push
```

### Scenario 4: Added screenshots
```bash
git add screenshots/
git commit -m "Added project screenshots"
git push
```

## Useful Commands

```bash
# View commit history
git log

# View remote repository URL
git remote -v

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Discard all local changes
git reset --hard

# Create a new branch
git checkout -b feature-name

# Switch back to main branch
git checkout main

# Pull latest changes from GitHub
git pull
```

## Troubleshooting

### Problem: "Permission denied"
```bash
# Use personal access token instead of password
# Or set up SSH keys (recommended)
```

### Problem: "Repository not found"
```bash
# Check remote URL
git remote -v

# Update remote URL
git remote set-url origin https://github.com/YOUR_USERNAME/CORRECT_REPO_NAME.git
```

### Problem: "Merge conflict"
```bash
# Pull first, resolve conflicts, then push
git pull
# Fix conflicts in files
git add .
git commit -m "Resolved merge conflicts"
git push
```

### Problem: "Large files"
```bash
# Remove large files from tracking
git rm --cached large_file.csv
# Add to .gitignore
echo "large_file.csv" >> .gitignore
git add .gitignore
git commit -m "Remove large files"
git push
```

## GitHub Personal Access Token Setup

1. Go to GitHub.com → Settings → Developer settings
2. Personal access tokens → Tokens (classic)
3. Generate new token (classic)
4. Select scopes: `repo` (full control)
5. Generate and copy the token
6. Use token as password when pushing

## Best Practices

✅ Commit often with clear messages
✅ Pull before you push
✅ Use .gitignore for sensitive files
✅ Write descriptive commit messages
✅ Keep commits focused (one feature/fix per commit)

❌ Don't commit passwords or API keys
❌ Don't commit large binary files
❌ Don't commit generated files (unless needed for demo)
❌ Don't use vague commit messages like "update" or "fix"

## Commit Message Examples

Good ✅:
- "Add LSTM model training script"
- "Fix data preprocessing bug in features.py"
- "Update README with installation instructions"
- "Add backtesting functionality"

Bad ❌:
- "update"
- "fix"
- "changes"
- "asdf"
