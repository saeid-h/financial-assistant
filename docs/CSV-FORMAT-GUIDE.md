# CSV Import Format Guide

## Overview

Financial Assistant is designed to handle CSV files from **any financial institution**. The system uses intelligent column detection to automatically identify the required fields regardless of column names or order.

---

## How It Works

### Flexible Column Detection

The parser automatically detects columns by matching common names (case-insensitive). You don't need to rename columns or reformat your CSV files!

### Required Fields

The system needs to identify these three pieces of information:

1. **Date** - When the transaction occurred
2. **Description** - What the transaction was for
3. **Amount** - How much money was involved

### How Amount is Determined

The system supports two approaches:

**Option A: Single Amount Column**
- Column like "Amount", "Transaction Amount", or "Value"
- Negative for expenses, positive for income

**Option B: Separate Debit/Credit Columns**
- Debit columns: charges, expenses, withdrawals (becomes negative)
- Credit columns: payments, deposits, income (becomes positive)

---

## Supported Column Names

### Date Columns (case-insensitive)
- `Date`
- `Transaction Date`
- `Posting Date`
- `Trans Date`
- `Transaction_Date`
- `Post Date`
- `Value Date`

**Example:** Your CSV can have "TRANSACTION DATE" or "posting_date" and it will work!

### Description Columns (case-insensitive)
- `Description`
- `Merchant`
- `Payee`
- `Details`
- `Memo`
- `Narrative`
- `Particulars`
- `Reference`

**Example:** Whether it's "MERCHANT NAME" or "description", it's automatically detected!

### Amount Column (if using single column)
- `Amount`
- `Transaction Amount`
- `Value`

### Debit Columns (if using separate columns)
- `Debit`
- `Withdrawal`
- `Withdrawals`
- `Debit Amount`
- `Paid Out`
- `Spend`

### Credit Columns (if using separate columns)
- `Credit`
- `Deposit`
- `Deposits`
- `Credit Amount`
- `Paid In`
- `Received`

### Optional Columns (Automatically Ignored)
These columns are recognized and safely ignored:
- `Status`
- `Member Name`
- `Member`
- `Account Holder`
- `Card Number`
- `Reference Number`
- `Balance`
- `Running Balance`

---

## Real-World Examples

### Example 1: Chase Bank Checking
```csv
Transaction Date,Description,Amount,Balance
10/14/2025,AMAZON.COM,-125.50,2374.50
10/15/2025,PAYCHECK DEPOSIT,2500.00,4874.50
10/16/2025,SHELL GAS STATION,-45.20,4829.30
```
✅ **Works!** Auto-detects: Date, Description, Amount

---

### Example 2: Wells Fargo Credit Card
```csv
Date,Merchant,Debit,Credit
10/14/2025,WALMART,89.75,
10/15/2025,PAYMENT - THANK YOU,,500.00
10/16/2025,TARGET,125.30,
```
✅ **Works!** Auto-detects: Date, Merchant (as Description), Debit/Credit

---

### Example 3: Bank of America (with Status)
```csv
Status,Date,Description,Debit,Credit,Member Name
Posted,10/14/2025,GROCERY STORE,89.75,,John Doe
Posted,10/15/2025,ONLINE PAYMENT,,500.00,John Doe
Pending,10/16/2025,GAS STATION,45.20,,John Doe
```
✅ **Works!** Auto-detects required fields, ignores Status and Member Name

---

### Example 4: Discover Card
```csv
Trans. Date,Description,Amount
10/14/2025,AMAZON MARKETPLACE,-89.99
10/15/2025,PAYMENT - THANK YOU,500.00
10/16/2025,COSTCO WHOLESALE,-125.50
```
✅ **Works!** Auto-detects abbreviated "Trans. Date"

---

### Example 5: European Bank (with semicolons)
```csv
Posting Date;Details;Withdrawal;Deposit
14.10.2025;Grocery Store;"1.234,56";
15.10.2025;Salary Deposit;;"2.500,00"
16.10.2025;Rent Payment;"890,50";
```
✅ **Works!** Auto-detects:
- Semicolon delimiter
- European date format (DD.MM.YYYY)
- European number format (1.234,56)

---

### Example 6: Capital One
```csv
Transaction Date,Posted Date,Card No.,Description,Category,Debit,Credit
10/14/2025,10/15/2025,****1234,WHOLE FOODS,Groceries,125.50,
10/15/2025,10/16/2025,****1234,PAYCHECK,Income,,2500.00
```
✅ **Works!** Ignores extra columns (Posted Date, Card No., Category)

---

## Supported Features

### Delimiters
- ✅ Comma (,)
- ✅ Semicolon (;)
- ✅ Tab (\t)
- ✅ Pipe (|)

**Auto-detected** - you don't need to tell the system which one!

### Date Formats
- ✅ MM/DD/YYYY (US format: 10/14/2025)
- ✅ DD/MM/YYYY (International: 14/10/2025)
- ✅ YYYY-MM-DD (ISO format: 2025-10-14)
- ✅ DD.MM.YYYY (European: 14.10.2025)
- ✅ MM-DD-YYYY (US with dashes: 10-14-2025)

**Auto-detected** - system tries both US and international formats!

### Number Formats
- ✅ US format: `1,234.56` (comma thousands, period decimal)
- ✅ European format: `1.234,56` (period thousands, comma decimal)
- ✅ Currency symbols: `$1,234.56`, `£1,234.56`, `€1.234,56`
- ✅ Negative parentheses: `(1,234.56)` = -1,234.56
- ✅ Negative sign: `-1,234.56`

**Auto-detected** - system handles both formats!

---

## What If My Format Doesn't Work?

If your CSV format isn't recognized, here's what to check:

### 1. Check Required Columns
Your CSV **must** have:
- ✅ A date column (any of the supported names)
- ✅ A description column (any of the supported names)  
- ✅ Either: An amount column OR both debit and credit columns

### 2. Common Issues

**Issue: "Could not find date column"**
- Solution: Ensure you have a column with "date" in the name
- Workaround: Rename your date column to "Date" in Excel

**Issue: "Could not find description column"**
- Solution: Ensure you have a column describing the transaction
- Workaround: Rename to "Description"

**Issue: "Could not find amount columns"**
- Solution: You need either:
  - One column called "Amount" OR
  - Both "Debit" and "Credit" columns
- Workaround: Rename your columns or add an "Amount" column

### 3. Quick Fixes

If your CSV doesn't work immediately:

**Option A: Rename Columns (Easiest)**
1. Open CSV in Excel or Notepad
2. Change first row to: `Date,Description,Amount`
3. Save and try again

**Option B: Request Support for Your Format**
Send us:
- Name of your financial institution
- Sample of your CSV format (anonymize real data!)
- We'll add support for it

---

## Testing Your CSV

### Before Importing:

1. **Open in Excel/Notepad** - Verify it looks correct
2. **Check First Row** - Should be column headers
3. **Check Date Format** - Should be consistent
4. **Check Numbers** - Should be numbers (not text like "PENDING")

### Sample Test:

Create a simple test CSV:
```csv
Date,Description,Amount
10/14/2025,Test Transaction,-10.00
10/15/2025,Test Income,100.00
```

If this imports successfully, your setup is working!

---

## Advanced Features

### Handling Complex Scenarios

**Multiple Transaction Types:**
```csv
Date,Type,Description,Debit,Credit
10/14/2025,PURCHASE,AMAZON,125.50,
10/15/2025,PAYMENT,ONLINE PAYMENT,,500.00
10/16/2025,REFUND,RETURN CREDIT,,25.00
```
✅ System handles different transaction types automatically

**With Account Numbers:**
```csv
Account,Date,Description,Amount
****1234,10/14/2025,Purchase,-125.50
****1234,10/15/2025,Payment,500.00
```
✅ Extra columns are safely ignored

**With Categories:**
```csv
Date,Description,Category,Amount
10/14/2025,Grocery Store,Food & Dining,-89.75
10/15/2025,Gas Station,Auto & Transport,-45.20
```
✅ We ignore the Category column (we have our own categorization)

---

## Tips for Best Results

### 1. Use Original Bank Files
Don't edit or reformat - the system is designed for raw bank exports!

### 2. One Account Per File
Import one account's transactions at a time for better tracking.

### 3. Select Correct Account Type
When importing:
- Checking account → Select "checking" account
- Credit card → Select "credit" account
- This helps with proper sign interpretation

### 4. Review Preview
Always check the preview before confirming:
- ✅ Dates look correct
- ✅ Amounts have proper signs (negative for expenses)
- ✅ Descriptions are readable

---

## Getting Help

### If Your Format Still Doesn't Work:

1. **Check Validation Errors**
   - The system shows specific errors
   - Fix data issues (dates, amounts)

2. **Try Minimal CSV**
   - Create test file with just: Date, Description, Amount
   - If this works, problem is in optional columns

3. **Contact for Support**
   - Share your column headers (just first row)
   - We'll add support for your institution

---

## Supported Institutions (Tested)

We've tested with formats from:
- ✅ Chase Bank
- ✅ Wells Fargo
- ✅ Bank of America
- ✅ Capital One
- ✅ Discover
- ✅ American Express
- ✅ Citi Bank
- ✅ Generic CSV exports

**Your institution not listed?** Try anyway! The flexible detection works with most formats.

---

## Technical Details

### Column Detection Algorithm

1. **Normalize names**: Convert to lowercase, remove spaces/underscores
2. **Pattern matching**: Check against known column name patterns
3. **Fuzzy matching**: "Trans Date" matches "Transaction Date" pattern
4. **Validation**: Ensure at least required columns found
5. **Parsing**: Extract data using detected columns

### Amount Calculation

**Single Amount Column:**
```python
amount = parsed_value  # Use as-is
```

**Debit/Credit Columns:**
```python
if credit > 0:
    amount = +credit  # Income/payment
elif debit > 0:
    amount = -debit   # Expense/charge
```

---

**Remember:** The system is designed to be flexible! If your format isn't recognized, it's likely a quick fix. Don't hesitate to import and see what happens - the preview will show you exactly how it's interpreted before saving anything.

