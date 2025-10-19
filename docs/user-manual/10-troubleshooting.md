# 10. Troubleshooting

[← Previous: Admin Functions](./09-admin.md) | [Back to Index](./00-index.md)

---

## Quick Fixes

### 🔧 Fix 95% of Issues

**The Magic Solution** - Try these first:

1. **Hard Refresh** (clears browser cache)
   ```
   Mac: Cmd + Shift + R
   Windows/Linux: Ctrl + Shift + R
   ```

2. **Restart the Application**
   ```bash
   # Stop: Ctrl+C in terminal
   # Start: ./start.sh
   ```

3. **Clear Browser Cache**
   - Open DevTools (Cmd+Option+I / F12)
   - Application tab → Clear Storage → Clear site data

---

## Application Won't Start

### Port Already in Use

**Error**: `Address already in use: 5001`

**Cause**: Another process is using port 5001 (or previous instance still running)

**Solutions:**

**Option A: Kill the process**
```bash
# Find process on port 5001
lsof -i :5001

# Kill it
kill -9 <PID>

# Restart
./start.sh
```

**Option B: Use different port**
```python
# Edit src/app.py
if __name__ == '__main__':
    app.run(debug=True, port=5002)  # Change to 5002
```

### macOS AirPlay Conflict

**Error**: Port 5000 in use

**Cause**: macOS AirPlay Receiver uses port 5000

**Solution**: We already use port 5001 to avoid this!

### Python Not Found

**Error**: `python: command not found`

**Solution**:
```bash
# Try python3 instead
python3 -m venv venv
python3 src/app.py

# Or install Python 3.13+
```

### Module Not Found

**Error**: `ModuleNotFoundError: No module named 'flask'`

**Cause**: Virtual environment not activated or dependencies not installed

**Solution**:
```bash
# Activate venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

---

## Database Issues

### Database File Not Found

**Error**: `no such table: accounts`

**Cause**: Database not initialized

**Solution**:
```bash
python src/init_db.py
python src/seed_rules.py

# Run migrations
python src/migrate_add_reference_date.py
# (run other migrations as needed)
```

### Database Locked

**Error**: `database is locked`

**Cause**: Another process accessing database, or SQLite timeout

**Solution**:
1. Stop all Flask instances
2. Close any DB browser tools
3. Restart Flask

### Foreign Key Constraint Error

**Error**: `FOREIGN KEY constraint failed`

**Cause**: Trying to delete account/category with dependent data

**Solution**:
- Delete dependent data first (transactions, budgets)
- Or use Admin → Reset to clear everything

---

## Import Issues

### CSV Parse Failed

**Error**: `Failed to parse CSV: Unexpected error parsing CSV`

**Causes & Solutions:**

**1. Wrong file type**
- Check file extension is `.csv` (not `.xlsx`, `.pdf`)
- Re-download from bank as CSV

**2. Corrupted file**
- Open in text editor to verify it's valid CSV
- Re-download from bank

**3. Unsupported format**
- Check [CSV Format Guide](../CSV-FORMAT-GUIDE.md)
- Contact support if format not supported

### No Pending Import Found

**Error**: `No pending import found. Please upload a file first.`

**Cause**: Session expired or browser issue

**Solution**:
1. Hard refresh (Cmd+Shift+R)
2. Upload CSV again
3. Click "Upload and Preview" 
4. Immediately click "Confirm Import"

### All Transactions Invalid

**Error**: Preview shows 0 valid, all invalid

**Causes:**
1. **Future dates** - Check CSV dates, adjust computer clock
2. **Account not selected** - Choose account from dropdown
3. **CSV format wrong** - Check file in text editor

**Solution**:
- Review invalid transaction errors
- Fix source issue
- Re-upload

### Duplicate Transactions

**Not an error** - This is a feature!

**What happened:**
- You imported the same file twice
- Or overlapping date ranges

**Result**:
```
✓ Successfully imported 0 transactions
  - 812 duplicates skipped
```

**Action**: No action needed if expected.

---

## Category Picker Issues

### Can't See Category

**Issue**: Category exists but not visible in picker

**Solutions:**

**1. Hard refresh**
```
Cmd + Shift + R (Mac)
Ctrl + Shift + R (Windows)
```

**2. Check hierarchy**
- Is it under a different parent?
- Example: "Travel" is under "Optional Expenses"

**3. Scroll in the column**
- Column 2 and 3 have scrollbars
- Category might be at the bottom

**4. Browser console debug**
```javascript
// Paste in console
console.log('Categories:', allCategoriesForPicker);
allCategoriesForPicker.filter(c => c.name.includes('Travel'));
```

### Picker Won't Open

**Issue**: Click category button, nothing happens

**Solutions:**
1. Hard refresh browser
2. Check browser console for JavaScript errors
3. Ensure JavaScript is enabled

### Can't Assign Category

**Issue**: "Assign Category" button disabled

**Solution**: Select a category in the picker first!

---

## Balance Issues

### Current Balance Wrong

**Issue**: Current balance doesn't match bank

**Causes & Solutions:**

**1. Reference balance not set**
```
Solution:
- Edit account
- Set reference balance and date
- Current will recalculate
```

**2. Missing transactions**
```
Solution:
- Check date range of imports
- Import missing months
```

**3. Transactions in wrong account**
```
Solution:
- Check transaction list
- Delete misplaced transactions
- Re-import to correct account
```

**4. Transfer double-counting**
```
Solution:
- If you imported both sides of transfer
- This is normal and correct
- Each account shows its side
```

### Reference Balance Not Showing

**Issue**: Can't see reference balance on account card

**Solution**:
- Hard refresh (Cmd+Shift+R)
- Update completed Oct 19, 2025
- Should always show now (even if $0.00)

---

## Performance Issues

### Slow Page Loading

**Issue**: Pages take long to load

**Causes:**
1. **Too many transactions** (10,000+)
   - Solution: Use date range filters
   - Solution: Archive old data

2. **Browser cache full**
   - Solution: Clear browser cache
   - Solution: Hard refresh

3. **Large CSV import**
   - Solution: Split into smaller files
   - Solution: Import in batches

### Charts Not Rendering

**Issue**: Reports page shows no charts

**Solutions:**
1. Categorize transactions first
2. Check date range (might be empty period)
3. Hard refresh browser
4. Check browser console for errors

---

## Browser-Specific Issues

### Safari

**Issue**: Category picker positioning wrong

**Solution**:
- Use Chrome/Firefox instead
- Or update Safari to latest version

**Issue**: Dates not working in forms

**Solution**:
- Type dates manually (YYYY-MM-DD)
- Or use Chrome/Firefox

### Firefox

**Issue**: Scrollbars not styled

**Solution**:
- This is normal (Firefox has different scrollbar styling)
- Functionality works, just looks different

### Mobile Browsers

**Issue**: UI not optimized for mobile

**Solution**:
- Financial Assistant is designed for desktop
- Use on laptop/desktop for best experience
- Mobile optimization planned for future

---

## Data Issues

### Transactions Wrong Color

**Issue**: Transfer showing as red/green instead of purple

**Solution**:
- Recategorize to "Account Transfer"
- Or run "Auto-Cat Uncategorized"
- Hard refresh to see purple color

### Categories Not Hierarchical

**Issue**: Category counts not summing to parent

**Status**: Known limitation, planned for future update

**Current**: Each category shows only direct transactions  
**Future**: Parent will show sum of all descendants

### Amounts Wrong Sign

**Issue**: Income showing negative, expenses showing positive

**Cause**: CSV format interpretation issue

**Solution**:
- Check [CSV Format Guide](../CSV-FORMAT-GUIDE.md)
- Verify with your bank's format
- May need manual adjustment

---

## Network & Connection Issues

### Can't Access localhost:5001

**Causes & Solutions:**

**1. Application not running**
```bash
# Start it
./start.sh
```

**2. Wrong port**
```
Try: http://localhost:5001 (not 5000!)
```

**3. Firewall blocking**
```
Solution:
- Check firewall settings
- Allow Python to accept connections
- Try http://127.0.0.1:5001
```

**4. Browser blocking**
```
Solution:
- Disable browser extensions
- Try incognito/private mode
- Try different browser
```

---

## Testing Issues

### Tests Failing

**Error**: `pytest` shows failures

**Common causes:**

**1. Database not in test mode**
```bash
# Tests should use in-memory DB
# Check conftest.py is in tests/ folder
```

**2. Dependencies outdated**
```bash
pip install --upgrade -r requirements.txt
```

**3. Python version**
```bash
# Needs Python 3.13+
python --version
```

### Coverage Low

**Issue**: Coverage report shows <80%

**Solution**:
- This is informational
- Not required for application to work
- Indicates areas needing more tests

---

## Import Error Messages

### "Transaction date cannot be in the future"

**Cause**: Your computer clock is wrong, or CSV has future dates

**Solution**:
- Check system date/time
- Check CSV dates
- Adjust one or the other

### "Invalid amount format"

**Cause**: Amount is 0, blank, or non-numeric

**Solution**:
- Check CSV in text editor
- Fix source data
- Or skip those rows

### "Account not found"

**Cause**: Selected wrong account or account doesn't exist

**Solution**:
- Create account first
- Then import transactions

---

## Visual/UI Issues

### Layout Broken

**Issue**: Page layout looks wrong, overlapping elements

**Solution**:
1. Hard refresh (Cmd+Shift+R)
2. Clear browser cache
3. Try different browser
4. Check browser zoom (should be 100%)

### Modal Won't Close

**Issue**: Category picker or account modal stuck open

**Solution**:
1. Press Escape key
2. Click outside modal (on overlay)
3. Hard refresh page
4. Close and reopen browser

### Buttons Not Clicking

**Issue**: Click buttons, nothing happens

**Solution**:
1. Check browser console for errors
2. Hard refresh
3. Ensure JavaScript enabled
4. Try different browser

---

## Getting Help

### Check These First

1. **This troubleshooting guide** (you're here!)
2. **Relevant user manual section** (based on feature)
3. **CSV Format Guide** (for import issues)
4. **README.md** (for technical setup)

### Still Stuck?

**Debug steps:**
1. Open browser DevTools (F12 or Cmd+Option+I)
2. Go to Console tab
3. Reproduce the issue
4. Look for red error messages
5. Take screenshot of console + screen
6. Check GitHub Issues

### Common Error Messages Decoded

```
"ModuleNotFoundError" → Dependencies not installed (pip install)
"database is locked" → Stop other Flask instances
"Connection refused" → Application not running (./start.sh)
"404 Not Found" → Wrong URL or route missing
"500 Internal Server Error" → Backend error, check terminal logs
```

---

## Preventive Maintenance

### Weekly

- [ ] Backup database file
- [ ] Check for any alerts (budgets, issues)
- [ ] Review uncategorized transactions

### Monthly

- [ ] Review all budgets
- [ ] Analyze spending reports
- [ ] Update budgets for next month
- [ ] Archive old CSV files (already done automatically!)

### Quarterly

- [ ] Full database backup
- [ ] Review and clean up categories
- [ ] Review and update categorization rules
- [ ] Check for application updates

---

## Recovery Checklist

**If something goes wrong:**

- [ ] Don't panic!
- [ ] Backup current database (even if corrupted)
- [ ] Check archived CSVs (your data backup)
- [ ] Try hard refresh first
- [ ] Restart application
- [ ] Check this troubleshooting guide
- [ ] Use Admin functions carefully
- [ ] Re-import from archives if needed

**Remember**: Your CSV archives in `data/archives/` are your ultimate backup!

---

## Known Limitations

### Current Version (v1.0-draft)

**Category Picker:**
- Scrolling in columns 2 & 3 may have issues
- Workaround: Use Category Management page
- Fix planned for future release

**Hierarchical Counting:**
- Parent categories don't sum children
- Each category shows only direct transactions
- Planned for future release

**Mobile Support:**
- Not optimized for mobile devices
- Use desktop/laptop for best experience

**Multi-Currency:**
- Only supports single currency (USD assumed)
- No currency conversion

---

## Version Information

**Current Version**: v1.0-draft  
**Release Date**: 2025-10-19  
**Status**: Phase 1 & 2 Complete  
**Python**: 3.13+  
**Flask**: 3.0.0  
**Database**: SQLite 3

**Git Tag**: To revert to stable release:
```bash
git checkout v1.0-draft
```

---

## Getting More Help

**Resources:**
- **User Manual**: docs/user-manual/ (all sections)
- **CSV Guide**: docs/CSV-FORMAT-GUIDE.md
- **Technical Docs**: docs/delivery/ (PBI documentation)
- **README**: README.md (setup and overview)
- **GitHub**: https://github.com/saeid-h/financial-assistant

**Contact:**
- **GitHub Issues**: Report bugs and feature requests
- **Author**: Saeed Hoss

---

[← Previous: Admin Functions](./09-admin.md) | [Back to Index](./00-index.md)


