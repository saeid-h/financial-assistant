# 4. Viewing & Managing Transactions

[← Previous: Importing Transactions](./03-importing-transactions.md) | [Back to Index](./00-index.md) | [Next: Categorization →](./05-categorization.md)

---

## Overview

The Transactions page displays all your imported transactions with powerful search and filtering capabilities.

**Access**: Click "Transactions" in navigation or visit http://localhost:5001/transactions

---

## Transaction List

### Statistics Dashboard

At the top, you'll see 5 key metrics:

```
┌──────────────────────────────────────────────────────────────┐
│ Total Transactions: 1,234                                    │
├──────────────────────────────────────────────────────────────┤
│ 💰 Income & Deposits    💸 Expenses & Withdrawals            │
│ $8,234.50               $10,805.09                           │
│ Money IN (+)            Money OUT (-)                        │
├──────────────────────────────────────────────────────────────┤
│ 💹 Transfers            📊 Net Cash Flow                     │
│ $500.00                 -$2,570.59                           │
│ Between accounts        Income - Expenses                    │
└──────────────────────────────────────────────────────────────┘
```

**Understanding the metrics:**
- **Income & Deposits** (Green): All money coming IN
- **Expenses & Withdrawals** (Red): All money going OUT
- **Transfers** (Purple): Neutral movements between your accounts
- **Net Cash Flow**: Your TRUE wealth change (Income - Expenses, excludes transfers)

### Transaction Table

Each row shows:
- **Date**: When the transaction occurred
- **Account**: Which account (checking, savings, credit card)
- **Description**: What you paid for or received
- **Category**: Current category or "Uncategorized" button
- **Amount**: Transaction value with color coding
- **Actions**: Delete button

---

## Transaction Color Coding

### Amount Colors

- **GREEN (+)**: Income, deposits, money IN, debt DOWN
  - Examples: Salary, refunds, credit card payments

- **RED (-)**: Expenses, withdrawals, money OUT, debt UP
  - Examples: Groceries, bills, credit card charges

- **PURPLE (± )**: Transfers, neutral, money between accounts
  - Examples: Checking → Savings, credit card autopay

### Understanding Your Transactions

**Bank Account (Asset):**
```
+$3,500.00  GREEN  = Paycheck (money IN)
-$156.78    RED    = Groceries (money OUT)
+$500.00    PURPLE = Transfer from savings (neutral)
```

**Credit Card (Liability):**
```
-$156.78    RED    = Purchase (debt UP)
+$500.00    PURPLE = Payment from checking (debt DOWN)
+$10.93     GREEN  = Return/refund (debt DOWN)
```

---

## Filtering Transactions

### Filter by Account

**Dropdown**: "All Accounts" or select specific account

**Use case**: See only Chase transactions, or only Costco transactions

### Filter by Date Range

**Date From** and **Date To** fields

**Examples:**
- Last month: 2025-09-01 to 2025-09-30
- This year: 2025-01-01 to 2025-12-31
- Last 90 days: Calculate from today

**Click "Apply Filters"** after setting dates

### Search

**Real-time search** as you type in the search box

**Searches in**: Transaction descriptions

**Examples:**
- Type "costco" → Shows all Costco transactions
- Type "netflix" → Shows all Netflix transactions  
- Type "grocery" → Shows all with "grocery" in description

### Advanced Filters

**Click "Advanced Filters"** to expand:

**Amount Range:**
- Min: $0 (or leave blank)
- Max: $1000 (or leave blank)
- Example: Find all transactions between $100-$500

**Transaction Type:**
- All Transactions (default)
- Income Only (positive amounts)
- Expenses Only (negative amounts)

### Clear Filters

**Click "Clear"** button to reset all filters and show all transactions

---

## Managing Categories

### Viewing Category

Each transaction shows its current category:
- **Green badge**: Categorized (e.g., "Groceries", "Salary")
- **Gray "Uncategorized" button**: Not yet categorized

### Assigning Category

1. **Click the "Uncategorized" button** (or existing category)
2. **Category picker opens** with 3 columns
3. **Select hierarchy**:
   - Column 1: Choose type (Income, Expenses, Transfers)
   - Column 2: Choose subcategory (Groceries, Entertainment, etc.)
   - Column 3: Choose detail (if available)
4. **Optional**: Check "🧠 Remember this for similar transactions" (creates auto-rule)
5. **Click "✓ Assign Category"**

**Example:**
```
Categorizing Costco purchase:

Column 1: 💸 Expenses
  → Click "Variable Expenses"

Column 2: Variable Expenses
  → Click "Groceries"

Column 3: (if you have details)
  → Click "Weekly Groceries" or "Monthly Groceries"

[✓] 🧠 Remember this for similar transactions
[✓ Assign Category]
```

### Creating New Category

**In the picker:**
1. Click "➕ Add New..." at the top of any column
2. Enter category name
3. Category is created and auto-selected
4. Click "✓ Assign Category"

**Example**: Adding "Gym Membership"
```
Column 1: Optional Expenses
Column 2: Click "➕ Add New Optional Expenses..."
Enter: "Gym Membership"
→ Created and selected!
[✓ Assign Category]
```

---

## Deleting Transactions

**Warning**: This permanently removes the transaction from your database.

**Steps:**
1. Find the transaction in the list
2. Click **"Delete"** button in the Actions column
3. Confirm deletion

**When to delete:**
- Duplicate you imported manually
- Test transaction
- Wrong account import

**Note**: Current balance updates automatically after deletion

---

## Best Practices

### ✅ DO

- **Filter by account** to focus on one account at a time
- **Use search** to quickly find specific merchants
- **Categorize regularly** (don't let uncategorized pile up)
- **Use "Remember this"** checkbox to create auto-rules for future
- **Review categories** monthly to ensure accuracy

### ❌ DON'T

- Don't delete transactions unless you're sure
- Don't leave everything uncategorized (reports won't be useful)
- Don't manually categorize if auto-categorization might work (use soft recategorize)

---

## Tips & Tricks

### Tip 1: Bulk Categorization
Instead of categorizing one-by-one:
1. Go to Categories page
2. Click "🔄 Auto-Cat Uncategorized" (soft mode)
3. 80-90% will auto-categorize

### Tip 2: Finding Problem Transactions
Use Advanced Filters:
- Large expenses: Set Amount Min = $500
- Small transactions: Set Amount Max = $10
- Income only: Select "Income Only"

### Tip 3: Monthly Review
Filter by date range:
- Set Date From: 2025-10-01
- Set Date To: 2025-10-31
- Review just October transactions

### Tip 4: Account Reconciliation
1. Filter by account (e.g., "Chase Checking")
2. Filter by date (e.g., last month)
3. Compare Current Balance to bank statement
4. Investigate if different

---

## Understanding Transaction Counts

**Why totals might not match bank statement:**

1. **Reference date effect**:
   - Transactions BEFORE reference date still show
   - But they're already included in reference balance
   - Don't double-count!

2. **Pending transactions**:
   - Bank statement shows pending
   - You only import posted transactions
   - This is normal

3. **Different date ranges**:
   - Bank statement: Oct 1-31
   - Your import: Only Oct 15-31
   - Filter to match date ranges

---

## Keyboard Shortcuts

- **Tab**: Navigate through filters
- **Enter**: Apply filters (when in filter field)
- **Escape**: Close category picker
- **Cmd+F** (Mac) / **Ctrl+F** (Windows): Browser search (searches whole page)

---

## What's Next?

- **Categorize efficiently** - See [Categorization](./05-categorization.md)
- **Analyze spending** - See [Reports & Charts](./06-reports.md)
- **Create budgets** - See [Budget Management](./07-budgets.md)

---

[← Previous: Importing Transactions](./03-importing-transactions.md) | [Back to Index](./00-index.md) | [Next: Categorization →](./05-categorization.md)


