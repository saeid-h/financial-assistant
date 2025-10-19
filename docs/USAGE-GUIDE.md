# Financial Assistant - Usage Guide

Quick reference guide for using Financial Assistant.

---

## 🏦 Account Management

### View Your Accounts

1. Click **Accounts** in the navigation bar
2. You'll see all your accounts displayed as cards

### Add a New Account

1. Click the **"+ Add Account"** button
2. Fill in the form:
   - **Account Name**: e.g., "Chase Checking", "Wells Fargo Credit Card"
   - **Account Type**: Select checking, savings, or credit card
   - **Institution** (optional): e.g., "Chase Bank"
3. Click **"Create Account"**
4. ✅ Account created and displayed immediately!

### Edit an Existing Account

**Super Easy! Just click on any account card:**

1. **Click** on the account card you want to edit
2. The edit modal opens with current information pre-filled
3. Make your changes:
   - Update the account name
   - Change the account type
   - Modify the institution
4. Click **"Update Account"** to save
5. ✅ Changes applied immediately!

**Tip:** When you hover over an account card, you'll see "Click to edit" appear in the corner.

### Delete an Account

1. **Click** on the account card
2. Click the red **"Delete Account"** button
3. **Confirm** the deletion in the dialog
4. ✅ Account removed (with safety confirmation!)

---

## 📥 Importing Transactions

### Upload Your Bank CSV

1. Click **Import** in the navigation bar (or on the home page)
2. **Select Account**: Choose which account these transactions belong to
3. **Choose File**: Click and select your CSV export from your bank
4. Click **"Upload and Preview"**

### Supported CSV Formats

✅ **Any format from any bank!** The system automatically detects:
- Column names (Date, Description, Amount, Debit, Credit, etc.)
- Delimiters (comma, semicolon, tab)
- Date formats (US, European, ISO)
- Number formats (US and European)

**Need help?** See [CSV Format Guide](CSV-FORMAT-GUIDE.md) with examples from Chase, Wells Fargo, Bank of America, and more!

### Review the Preview

After uploading, you'll see:
- ✅ **Valid transactions**: Ready to import
- ⚠️ **Invalid transactions**: With clear error messages
- 📊 **Summary statistics**:
  - Total transactions
  - Total credits (money in)
  - Total debits (money out)

### Confirm Import

1. Review the transaction preview
2. Check the summary statistics
3. If everything looks good, click **"Confirm Import"**
4. ✅ Transactions saved to database!

**Note:** You can click "Cancel" to start over without saving anything.

---

## 🎯 Tips & Best Practices

### Account Setup
- ✅ Use descriptive names: "Chase Freedom Credit Card" better than just "Credit Card"
- ✅ Add institution names for easy identification
- ✅ Set the correct account type (affects sign interpretation for imports)

### CSV Import
- ✅ **Don't edit your bank's CSV** - upload it as-is!
- ✅ **One account at a time** - Keep imports organized
- ✅ **Check the preview** - Always review before confirming
- ✅ **Watch for validation errors** - Fix data issues before importing

### Editing Accounts
- ✅ **Click the card** - Quickest way to edit
- ✅ **Update anytime** - You can change account details whenever needed
- ⚠️ **Delete carefully** - Deleting an account may affect associated transactions

---

## 🔧 Common Tasks

### Change Account Name
1. Click on the account card
2. Edit the name field
3. Click "Update Account"

### Fix Account Type
1. Click on the account card
2. Select the correct type from dropdown
3. Click "Update Account"

### Remove Old Account
1. Click on the account card
2. Click "Delete Account"
3. Confirm deletion

### Import Multiple Statement Files
1. Import first file (choose account, upload, confirm)
2. Click "Import" again for next file
3. Repeat for each file

### Check What Was Imported
- Go to "Transactions" page (coming soon!)
- Or check your account details

---

## ❓ Troubleshooting

### "Could not find date column"
- Your CSV might use a different column name
- Check the [CSV Format Guide](CSV-FORMAT-GUIDE.md)
- Try renaming the column to "Date" in Excel

### "Invalid date format"
- Make sure dates are consistent throughout the file
- System supports most formats automatically

### "Amount cannot be zero"
- Remove rows with $0.00 amounts
- Or check if the amount column is correct

### "Account ID does not exist"
- Create the account first before importing
- Make sure you selected an account from the dropdown

### Import button doesn't work
- Make sure you've selected both account and file
- Check file is .csv format
- Try refreshing the page

---

## 🚀 Navigation

**Main Menu** (Always visible at top):
- **Home** - Dashboard and feature overview
- **Accounts** - Manage your accounts
- **Import** - Upload CSV files
- **Transactions** - View all transactions (coming soon)
- **Reports** - Financial reports (coming soon)

**Quick Actions**:
- Click "Import Statements" card on home page → Goes to Import
- Click "Manage Accounts" card → Goes to Accounts
- Click any account card → Opens edit modal

---

## 📱 Keyboard Shortcuts

- **Esc** - Close any modal
- **Click outside modal** - Close modal
- **Enter in form** - Submit form

---

## 🔒 Privacy & Security

- ✅ **All data stays on your computer** - No cloud uploads
- ✅ **Database stored locally** - In your project directory
- ✅ **No internet required** - Runs entirely offline (after setup)
- ✅ **Git ignores data** - Your transactions won't be committed to version control

---

## 📚 Additional Resources

- **[CSV Format Guide](CSV-FORMAT-GUIDE.md)** - Comprehensive CSV format documentation
- **[README](../README.md)** - Installation and setup instructions
- **[PBI-2 Summary](delivery/2/PBI-2-SUMMARY.md)** - Technical implementation details

---

## 💡 Pro Tips

1. **Keep account names consistent** - Makes reports easier to read
2. **Import regularly** - Stay up-to-date with your finances
3. **Review transactions** - Always check the preview before confirming
4. **Use institution names** - Helps when you have multiple accounts of same type
5. **Backup your database** - Copy `data/financial_assistant.db` regularly

---

**Need more help?** Check the full documentation in the `docs/` directory!

