# 3. Importing Transactions

[← Previous: Account Management](./02-accounts.md) | [Back to Index](./00-index.md) | [Next: Viewing Transactions →](./04-viewing-transactions.md)

---

## Overview

Import your bank and credit card statements in CSV format. The system automatically:
- Detects CSV format (delimiters, date formats, column names)
- Validates transactions
- Detects duplicates
- Auto-categorizes transactions
- Archives original files

**Supported**: 100+ financial institutions including Chase, Bank of America, Wells Fargo, Citi, Capital One, Discover, Amex, and more.

---

## Accessing Import

**From Home Page**: Click "📥 Import Statements"  
**From Navigation**: Not in menu (access from home or direct URL)  
**Direct URL**: http://localhost:5001/import/

---

## CSV Import (Recommended)

### Step-by-Step Guide

#### 1. Download CSV from Your Bank

**Most banks**:
- Login to online banking
- Go to Account → Transactions or Activity
- Look for "Export" or "Download"
- Select "CSV" format (not PDF or Excel)
- Choose date range (e.g., last 3 months)
- Download file

**Common locations**:
- Chase: Account Details → Download activity
- Bank of America: Statements & Docs → Download transactions
- Citi: Account Activity → Download
- Wells Fargo: Account Activity → Download

#### 2. Upload to Financial Assistant

1. **Select Account**
   - Choose from dropdown
   - This is where transactions will be imported

2. **Choose File**
   - Click "Choose CSV File" button
   - Select your downloaded CSV file

3. **Upload and Preview**
   - Click "Upload and Preview" button
   - System processes the file (usually < 1 second)

#### 3. Review Preview

You'll see:
- ✅ **Valid transactions** in green (ready to import)
- ❌ **Invalid transactions** in red (won't import)
- **Statistics**:
  - Total rows processed
  - Valid transactions
  - Errors (if any)
  - Total credits (income)
  - Total debits (expenses)

**Example Preview:**
```
Summary:
Total Rows: 815
Valid Transactions: 812
Errors: 3
Total Credits: +$8,234.50
Total Debits: -$10,805.09

Transactions Preview:
Date       Description          Amount      Status
2025-10-15 COSTCO WHSE #123    -$156.78    ✓ Valid
2025-10-14 PAYCHECK DEPOSIT    +$3,500.00  ✓ Valid
2025-10-13 NETFLIX.COM         -$15.99     ✓ Valid
...
```

#### 4. Confirm Import

- Review the preview
- Click "Confirm Import" if everything looks good
- System will:
  - Save transactions to database
  - Check for duplicates (skip if found)
  - Auto-categorize using 65+ rules
  - Archive the original CSV file

**Success message shows:**
```
✓ Successfully imported 812 transactions
  - 245 duplicates skipped
  - 658 auto-categorized
  - 154 awaiting categorization
```

---

## Supported CSV Formats

Financial Assistant automatically detects and handles:

### Delimiters
- **Comma** (`,`) - Most common
- **Semicolon** (`;`) - European banks
- **Tab** (`\t`) - Some banks

### Date Formats
- YYYY-MM-DD (2025-10-19)
- MM/DD/YYYY (10/19/2025)
- DD/MM/YYYY (19/10/2025)
- M/D/YY (10/19/25)
- And more...

### Amount Columns

**Single Amount Column**:
- Positive = income/deposits
- Negative = expenses/withdrawals

**Debit/Credit Columns**:
- For bank accounts:
  - Credit = deposits (positive)
  - Debit = withdrawals (negative)
- For credit cards:
  - Credit = charges (negative, increases debt)
  - Debit = payments (positive, decreases debt)

### Column Names

The system recognizes many variations:
- **Date**: Date, Posting Date, Transaction Date, Trans Date
- **Description**: Description, Details, Merchant, Payee
- **Amount**: Amount, Transaction Amount, Sum
- **Debit**: Debit, Withdrawals, Charges
- **Credit**: Credit, Deposits, Payments

**See**: [CSV Format Guide](../CSV-FORMAT-GUIDE.md) for detailed format documentation

---

## Specific Bank Examples

### Chase (Checking)
```csv
Details,Posting Date,Description,Amount,Type,Balance,Check or Slip #
DEBIT,10/18/2025,COSTCO WHSE #123,-156.78,ACCT_XFER,9843.22,
CREDIT,10/15/2025,PAYCHECK,3500.00,ACH_CREDIT,10000.00,
```

**How it imports:**
- System detects: Comma delimiter, MM/DD/YYYY dates
- Maps: Posting Date → date, Description → description, Amount → amount
- Ignores: Details, Type, Balance, Check # columns

### Costco Citi Visa (Credit Card)
```csv
Status,Date,Description,Debit,Credit,Member Name
Cleared,10/15/2025,COSTCO WHSE #456,156.78,,SAEED HOSS
Cleared,10/10/2025,CITI AUTOPAY,,-500.00,SAEED HOSS
```

**How it imports:**
- System detects: Comma delimiter, MM/DD/YYYY dates, Debit/Credit columns
- For credit cards: Debit (charges) = negative, Credit (payments) = positive
- Ignores: Status, Member Name
- Result:
  - COSTCO charge: -$156.78 (increases debt)
  - Autopay: +$500.00 (decreases debt)

---

## Duplicate Detection

The system prevents importing the same transaction twice.

### How It Works

Transactions are considered duplicates if they match:
- **Account** (same account)
- **Date** (exact date match)
- **Amount** (exact amount match)
- **Description** (exact description match)

### What Happens

When uploading a CSV:
- System checks each transaction against existing ones
- Exact duplicates are **skipped**
- Success message shows: "245 duplicates skipped"

**This means you can:**
- Re-import overlapping date ranges safely
- Import the same file twice without creating duplicates
- Download monthly statements and import all of them

---

## Auto-Categorization During Import

When you confirm an import, the system:

1. **Applies 65+ rules** to match merchant names
2. **Categorizes automatically**:
   - COSTCO WHSE → Groceries
   - NETFLIX → Entertainment
   - SHELL → Transportation (Gas)
   - AUTOPAY → Account Transfer
   - And many more...

3. **Shows results**:
   ```
   658 auto-categorized (81%)
   154 awaiting categorization (19%)
   ```

**Uncategorized transactions** can be categorized manually later on the Transactions page.

---

## Manual Transaction Entry

If you have a cash transaction or need to add something manually:

### Step-by-Step

1. **Scroll down** on the Import page to "Manual Transaction Entry"

2. **Fill in the form**:
   - **Account**: Select from dropdown
   - **Date**: Use date picker or type YYYY-MM-DD
   - **Description**: What you paid for
   - **Amount**: Positive for income, negative for expenses
     - Example: -50.00 for a $50 expense
     - Example: 3500.00 for $3,500 income

3. **Click "Add Transaction"**

### Examples

**Cash Grocery Shopping**:
```
Account: Chase Checking
Date: 2025-10-19
Description: Trader Joe's (Cash)
Amount: -85.50

[Add Transaction]
```

**Cash Gift Received**:
```
Account: Chase Checking
Date: 2025-10-15
Description: Birthday Gift from Mom
Amount: 100.00

[Add Transaction]
```

---

## File Archiving

All imported CSV files are automatically archived:

**Location**: `data/archives/YYYY/MM/filename_timestamp.csv`

**Example**:
```
Original file: Chase8226_Activity_20251018.CSV
Archived to: data/archives/2025/10/Chase8226_Activity_20251018_20251019_033045.csv
```

**Why this matters:**
- Original files are preserved
- You can re-reference them if needed
- Organized by year and month
- Timestamp prevents filename conflicts

---

## Import Best Practices

### ✅ DO

- **Import in chronological order** (oldest first)
- **Set reference balance BEFORE importing** for accurate current balance
- **Download overlapping ranges** (duplicates will be skipped)
- **Review the preview** before confirming
- **Check auto-categorization results** and manually categorize remaining items

### ❌ DON'T

- Don't import to the wrong account
- Don't panic if you see duplicates skipped (it's a feature!)
- Don't import future-dated transactions (validation will fail)
- Don't mix different accounts in one CSV (separate files per account)

---

## Troubleshooting Import Issues

### "Failed to parse CSV"

**Possible causes:**
- File is not a valid CSV
- File is corrupted
- Wrong file type (Excel .xlsx instead of CSV)

**Solutions:**
- Re-download from your bank
- Open in a text editor to verify it's a CSV
- Try saving as CSV from Excel if needed

### "No transactions found"

**Possible causes:**
- CSV has only headers, no data rows
- All rows failed validation

**Solutions:**
- Check the CSV in a text editor
- Verify it has transaction data
- Check the "Invalid Transactions" section for error messages

### "All transactions marked as duplicates"

**Explanation:**
- You already imported this file
- All transactions are exact matches to existing ones
- This is normal and safe!

**Action:**
- No action needed if duplicate counts are expected
- Check date ranges if unexpected

### "Some transactions show as invalid"

**Common validation errors:**
1. **Future dates** - Transaction date is in the future
   - Solution: Check your computer's date/time
   
2. **Missing description** - Empty description field
   - Solution: System auto-fills with "Unknown Transaction"
   
3. **Invalid amount** - Amount is 0 or non-numeric
   - Solution: Check the CSV, may need manual correction

4. **Account not found** - Selected wrong account
   - Solution: Create the account first, then import

---

## Advanced Topics

### Importing Multiple Accounts

1. Import to Account A
2. Click "Import Another CSV" button
3. Select Account B
4. Upload different CSV
5. Repeat for all accounts

### Large Imports (1000+ transactions)

The system handles large imports efficiently:
- Tested with 815+ transactions
- No performance issues
- Preview shows all transactions
- Uses temporary file storage (not session cookies)

### Importing Historical Data

**Best approach:**
1. Download all available history from your bank
2. Set reference balance to balance BEFORE oldest transaction
3. Import all files chronologically
4. Current balance will be accurate

**Example:**
- Oldest transaction: Oct 1, 2025
- Bank balance on Sep 30, 2025: $10,000
- Set reference: $10,000 on Sep 30
- Import all October+ transactions
- Current balance = accurate ✓

---

## Next Steps

After importing transactions:

1. **View imported data** - [Viewing Transactions](./04-viewing-transactions.md)
2. **Categorize remaining items** - [Categorization](./05-categorization.md)
3. **Analyze spending** - [Reports & Charts](./06-reports.md)

---

[← Previous: Account Management](./02-accounts.md) | [Back to Index](./00-index.md) | [Next: Viewing Transactions →](./04-viewing-transactions.md)


