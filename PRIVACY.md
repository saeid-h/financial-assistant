# Privacy & Data Protection

## Overview

Financial Assistant is designed with **privacy-first** principles. Your financial data never leaves your computer.

## Data Storage

### What's Stored Locally

All your financial data is stored exclusively on your local machine:

1. **Database**: `data/financial_assistant.db` - SQLite database with your transactions, accounts, and categories
2. **Import Archives**: `data/YYYY/MM/` - Original bank statement files organized by date
3. **Logs**: `logs/` - Application logs (no financial data)

### What's Protected by Git

The `.gitignore` file is configured to **prevent accidental commits** of your financial data:

```gitignore
# Database files
*.db
*.sqlite
*.sqlite3

# All data subdirectories (YYYY/MM archives)
data/*/

# Bank statements in all formats
data/**/*.csv
data/**/*.ofx
data/**/*.qfx
data/**/*.pdf
data/**/*.xlsx
data/**/*.xls

# Backups
data/**/backups/
```

**IMPORTANT**: These patterns ensure that even if you run `git add .` or `git add -A`, your actual financial data will NOT be committed to git.

## Network Activity

### What This App Does NOT Do

- ❌ No external API calls
- ❌ No cloud sync
- ❌ No analytics or tracking
- ❌ No data transmission to servers
- ❌ No third-party services
- ❌ No internet connection required (after installation)

### Local-Only Operation

- ✅ Runs entirely on localhost (127.0.0.1)
- ✅ Web interface accessible only from your machine
- ✅ All processing done locally
- ✅ Database stored locally
- ✅ Files never uploaded anywhere

## Data Security Best Practices

### Recommended Actions

1. **Backup Your Data**
   ```bash
   # Create encrypted backup
   tar -czf financial-assistant-backup-$(date +%Y%m%d).tar.gz data/
   ```

2. **Secure Your Files**
   - Keep your computer password-protected
   - Use full-disk encryption (FileVault on Mac, BitLocker on Windows)
   - Don't share the project directory

3. **Git Safety**
   - **Never force-add** data files: `git add -f data/` (DON'T DO THIS!)
   - Always check `git status` before committing
   - Review `.gitignore` to ensure it's not modified

4. **When Sharing Code**
   - The repository structure is safe to share
   - Your actual data is protected by `.gitignore`
   - Still, double-check before pushing to remote repositories

### Verify Data Protection

Check what would be committed:
```bash
# This should NOT show any files from data/ directory
git status

# Check what's ignored
git status --ignored
```

## Remote Repository Safety

If you push this code to GitHub/GitLab:

### Safe to Push (Public)
- ✅ Source code (`src/`)
- ✅ Tests (`tests/`)
- ✅ Documentation (`docs/`, `README.md`)
- ✅ Configuration files (`.gitignore`, `requirements.txt`)
- ✅ Empty directory markers (`.gitkeep`)

### Never Pushed (Protected)
- ❌ Your database (`data/*.db`)
- ❌ Your statements (`data/**/*.csv`, etc.)
- ❌ Your logs (`logs/*.log`)
- ❌ Your virtual environment (`venv/`)

## Data Deletion

### Removing Your Data

To completely remove all your financial data:

```bash
# Stop the application first (CTRL+C)

# Delete database
rm data/financial_assistant.db

# Delete archived statements
rm -rf data/20*/

# Delete logs
rm -rf logs/*.log

# Database will be recreated on next run (empty)
```

### Selling or Disposing Computer

Before selling or disposing of your computer:

1. Delete the entire project directory
2. Use secure deletion tools (e.g., `srm` on Mac, `shred` on Linux)
3. Ensure your disk is fully encrypted before disposal

## Accountability

### Your Responsibility

You are responsible for:
- Keeping your computer secure
- Not sharing your `data/` directory
- Verifying `.gitignore` before git operations
- Creating backups of your data
- Securing your backups

### Developer Responsibility

This application is provided "as-is" under MIT License:
- No warranties regarding data security
- User is responsible for data protection
- Use at your own risk

## Questions About Privacy

If you have questions or concerns about data privacy:

1. Review `.gitignore` - all protections are documented there
2. Check `git status` - verify no data files are staged
3. Test `git status --ignored` - verify data files are ignored
4. Review this document for best practices

## Summary

✅ **Your data stays on your computer**  
✅ **Git ignores all financial data**  
✅ **No network transmission**  
✅ **You control everything**

**Remember**: While this app is designed for privacy, you must still practice good security hygiene on your computer and with your git repository!

