# 9. Admin Functions

[← Previous: Transfer Transactions](./08-transfers.md) | [Back to Index](./00-index.md) | [Next: Troubleshooting →](./10-troubleshooting.md)

---

## Overview

The Admin page provides database management tools for maintaining your Financial Assistant installation.

**Access**: Click "Admin" in navigation or visit http://localhost:5001/admin

**⚠️ Warning**: Admin functions can delete data permanently. Use with caution!

---

## Database Statistics

At the top of the Admin page, you'll see current database stats:

```
┌─────────────────────────────────────┐
│ Database Statistics                 │
├─────────────────────────────────────┤
│ Accounts: 3                         │
│ Transactions: 1,234                 │
│ Categories: 45                      │
│ Categorization Rules: 65            │
│ Budgets: 8                          │
└─────────────────────────────────────┘
```

---

## Reset Transactions Only

**Button**: "Reset Transactions Only" (Yellow)

### What It Does

- Deletes ALL transactions from the database
- **Preserves**:
  - Accounts
  - Categories
  - Categorization rules
  - Budgets

**Use cases:**
- Testing imports
- Starting fresh with data
- Clearing test/dummy data
- Fixing corrupted transaction data

### Confirmation Steps

1. Click "Reset Transactions Only"
2. **First confirmation**: "Delete all X transactions?"
3. **Second confirmation**: "Type DELETE to confirm"
4. Type "DELETE" (uppercase)
5. Click "Confirm"

**Result**:
```
✓ Successfully deleted 1,234 transactions
✓ Accounts preserved (3 accounts remain)
✓ Categories preserved (45 categories remain)
✓ Rules preserved (65 rules remain)
```

---

## Reset Everything

**Button**: "Reset Everything" (Red)

### What It Does

**DELETES EVERYTHING:**
- All transactions
- All accounts
- All custom categories (keeps defaults)
- All custom rules (keeps defaults)
- All budgets

**Use cases:**
- Complete fresh start
- Major data corruption
- Switching to different dataset
- Testing from scratch

### Confirmation Steps

1. Click "Reset Everything"
2. **Warning dialog**: Lists what will be deleted
3. **First confirmation**: "Are you ABSOLUTELY sure?"
4. **Second confirmation**: "Type RESET to confirm"
5. Type "RESET" (uppercase)
6. Click "Confirm"

**Result**:
```
✓ All transactions deleted
✓ All accounts deleted
✓ Database reset to defaults
✓ 30 default categories remain
✓ 65 default rules remain
```

---

## Recategorization Tools

While not on the Admin page, these are important admin functions:

### Soft Recategorization

**Location**: Categories page  
**Button**: "🔄 Auto-Cat Uncategorized"

**What it does:**
- Applies rules to uncategorized transactions only
- Safe, non-destructive

**When to use:**
- After importing new transactions
- After adding new rules
- Regular maintenance

### Hard Recategorization

**Location**: Categories page  
**Button**: "⚡ Re-Cat ALL (Override)"

**What it does:**
- Recategorizes ALL transactions (overrides manual)
- Destructive - manual categorizations lost

**When to use:**
- Rules changed significantly
- Want fresh categorization
- Trust auto-cat over manual

---

## Backup Recommendations

### What to Backup

**Database file** (Most important):
```
Location: data/financial_assistant.db
Frequency: Weekly or before major changes
Method: Copy file to backup location
```

**Archived CSV files**:
```
Location: data/archives/
Frequency: Monthly
Method: Copy entire archives folder
```

**Configuration** (Optional):
```
Files: requirements.txt, pytest.ini
Frequency: After changes only
```

### Backup Process

**Manual backup:**
```bash
# Stop the application first
# Copy database
cp data/financial_assistant.db data/backups/financial_assistant_$(date +%Y%m%d).db

# Copy archives
cp -r data/archives/ data/backups/archives_$(date +%Y%m%d)/
```

**Restore from backup:**
```bash
# Stop the application
# Restore database
cp data/backups/financial_assistant_20251019.db data/financial_assistant.db

# Restart application
./start.sh
```

---

## Database Maintenance

### When to Reset Transactions

**Good reasons:**
- ✅ Testing import functionality
- ✅ Clearing dummy/test data
- ✅ Reimporting after fixing CSV issues
- ✅ Starting tracking period fresh

**Bad reasons:**
- ❌ Just to recategorize (use Soft Recat instead!)
- ❌ Fixing one wrong transaction (just delete that one!)
- ❌ Panic (think first!)

### When to Reset Everything

**Good reasons:**
- ✅ Major corruption
- ✅ Switching to different person's data
- ✅ Development/testing
- ✅ Complete restart

**Bad reasons:**
- ❌ Minor issues (use targeted fixes!)
- ❌ Don't like categorization (use Hard Recat!)
- ❌ Imported wrong file (just delete those transactions!)

---

## Migration Scripts

Located in `src/`, these scripts update the database schema:

### Available Migrations

```
src/migrate_add_transfer_categories.py
→ Adds "transfer" category type and Savings & Investments categories

src/migrate_add_notes_tags.py
→ Adds transaction_notes, tags, and transaction_tags tables

src/migrate_add_budgets.py
→ Adds budgets table

src/migrate_add_account_balance.py
→ Adds initial_balance and current_balance to accounts

src/migrate_add_reference_date.py
→ Adds reference_date to accounts
```

### Running Migrations

**Only needed if:**
- Restoring old database
- Using database from before migrations
- Setting up from scratch

**Command:**
```bash
python src/migrate_add_reference_date.py
```

**Output:**
```
✓ Successfully added reference_date column
✓ Set reference_date = created_at for existing accounts
Updated 2 accounts
```

---

## Seeding Data

### Seeding Categorization Rules

If you reset everything and want the default 65+ rules back:

```bash
python src/seed_rules.py
```

This adds rules for:
- Groceries (Costco, Safeway, Trader Joe's, etc.)
- Gas stations (Shell, Chevron, 76, etc.)
- Subscriptions (Netflix, Spotify, etc.)
- Dining (Starbucks, Chipotle, etc.)
- Transfers (Autopay, Online Transfer, etc.)

### Reinitializing Database

If you need to completely recreate:

```bash
# Delete existing database
rm data/financial_assistant.db

# Recreate with defaults
python src/init_db.py

# Seed rules
python src/seed_rules.py

# Run all migrations
python src/migrate_add_transfer_categories.py
python src/migrate_add_notes_tags.py
python src/migrate_add_budgets.py
python src/migrate_add_account_balance.py
python src/migrate_add_reference_date.py
```

---

## Data Privacy & Security

### Local Storage Only

**All data stays on your computer:**
- Database: `data/financial_assistant.db` (local SQLite file)
- Archives: `data/archives/` (local folder)
- No cloud sync
- No external server calls
- Complete privacy

### Git Ignore

The `.gitignore` file protects sensitive data:

**Ignored (never committed to Git):**
- `*.db` - All database files
- `data/*/` - All data directories
- `*.csv` - CSV files
- `logs/` - Log files

**Tracked (safe to commit):**
- Source code
- Documentation
- Configuration files (no sensitive data)

### File Locations

```
financial-assistant/
├── data/
│   ├── financial_assistant.db    ← Your data (PRIVATE)
│   └── archives/                 ← CSV backups (PRIVATE)
├── src/                          ← Code (SAFE)
├── docs/                         ← Documentation (SAFE)
└── .gitignore                    ← Protects private data
```

---

## Best Practices

### ✅ DO

- **Backup before major changes** (before reset, before upgrades)
- **Test on dummy data** first before using real finances
- **Use "Transactions Only"** reset (preserves accounts/categories)
- **Keep archived CSVs** (data/archives folder is your backup!)

### ❌ DON'T

- Don't use "Reset Everything" unless absolutely necessary
- Don't delete `data/archives/` folder (it's your backup!)
- Don't commit `data/` to Git (it's ignored for privacy!)
- Don't run migrations multiple times (they check if already run)

---

## Troubleshooting Admin Functions

**Issue**: Reset buttons don't work  
**Solution**: Check browser console for JavaScript errors, hard refresh

**Issue**: Database stats show 0 for everything  
**Solution**: You've reset - re-import your data

**Issue**: Migration script fails  
**Solution**: Check if already run (most migrations check for existing columns)

**Issue**: Can't find database file  
**Solution**: It's in `data/financial_assistant.db` - check with `ls -la data/`

---

## Recovery Procedures

### Recovering from Accidental Reset

**If you reset transactions by mistake:**

1. **Check your archived CSVs**:
   ```bash
   ls -R data/archives/
   ```

2. **Re-import all CSVs**:
   - Go to Import page
   - Import each CSV file
   - Duplicate detection will skip any already imported

3. **Recategorize**:
   - Go to Categories page
   - Click "🔄 Auto-Cat Uncategorized"

**Result**: Data restored from archives!

### Recovering from "Reset Everything"

**More difficult** - you need to:
1. Re-create all accounts
2. Re-import all CSVs
3. Re-create budgets
4. Re-create custom categories (if any)
5. Re-create custom rules (if any)

**Prevention**: Always backup before using "Reset Everything"!

---

## Next Steps

- **Fix common issues** - See [Troubleshooting](./10-troubleshooting.md)
- **Optimize workflow** - Review [Getting Started](./01-getting-started.md)

---

[← Previous: Transfer Transactions](./08-transfers.md) | [Back to Index](./00-index.md) | [Next: Troubleshooting →](./10-troubleshooting.md)


