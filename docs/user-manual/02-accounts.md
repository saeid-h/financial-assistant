# 2. Account Management

[← Previous: Getting Started](./01-getting-started.md) | [Back to Index](./00-index.md) | [Next: Importing Transactions →](./03-importing-transactions.md)

---

## Overview

The Accounts feature lets you manage all your financial accounts in one place:
- Bank checking accounts
- Savings accounts  
- Credit cards

Each account tracks its balance based on imported transactions and a reference point you set.

---

## Accessing Account Management

**From Home Page**: Click "💳 Manage Accounts"  
**From Navigation**: Click "Accounts" in the top menu  
**Direct URL**: http://localhost:5001/accounts

---

## Adding a New Account

### Step-by-Step

1. **Click "+ Add Account"** button (top right)

2. **Fill in the form:**

   **Account Name** (Required)
   - Example: "Chase Checking", "Costco Visa"
   - Choose a name you'll recognize

   **Account Type** (Required)
   - **Checking**: Regular checking account
   - **Savings**: Savings, money market, CD accounts
   - **Credit**: Credit cards

   **Financial Institution** (Optional)
   - Example: "Chase Bank", "Bank of America"
   - Helps you remember which bank

   **Initial Balance** (Optional)
   - The balance when you start tracking
   - Example: $10,000.00
   - Can be set to $0 if you don't know

3. **Click "Save"**

### Example

```
Adding Chase Checking Account:

Account Name: Chase Checking
Type: Checking
Institution: Chase Bank
Initial Balance: 10000.00

[Save] [Cancel]
```

---

## Understanding Account Balances

### Reference Balance
The balance at a specific point in time (your starting point).

**Why it matters:**
- Without it, your current balance is just the sum of imported transactions
- Example: You import October transactions totaling -$2,570
  - Without reference: Current balance shows -$2,570 (misleading!)
  - With reference of $10,000: Current balance shows $7,430 ✓

### Reference Date
The date when the reference balance was accurate.

**Why it matters:**
- "I had $10,000" is incomplete
- "I had $10,000 on October 1, 2025" is precise
- Current balance = Reference + Sum(transactions after reference date)

### Current Balance
Automatically calculated:

```
Current Balance = Reference Balance + Sum(All Transactions)
```

**Color Coding:**
- **GREEN**: Positive (asset accounts) or available credit
- **RED**: Negative or debt owed

---

## Viewing Account Details

### Account Card

Each account is displayed as a card:

```
┌─────────────────────────────────────────────┐
│ Chase Checking                              │
│ Checking • Chase Bank                       │
│                                             │
│ Reference Balance: $10,000.00               │
│ As of 2025-10-01                            │
│                                             │
│ Current Balance: $7,429.41                  │
│                                             │
│ Created: 2025-10-18                         │
│                                             │
│ [View Transactions] [Edit] [Delete]         │
└─────────────────────────────────────────────┘
```

### Actions

**View Transactions**
- Shows all transactions for this account
- Filtered view of the transactions page

**Edit**
- Update account name, type, institution
- **Set or update reference balance and date**
- Changes save immediately

**Delete**
- Removes the account
- ⚠️ WARNING: Also deletes all associated transactions!
- Confirmation required

---

## Editing an Account

### How to Edit

1. **Click "Edit"** on the account card
2. **Update any fields:**
   - Account Name
   - Type
   - Institution
   - **Reference Balance**
   - **Reference Date** (required)
3. **Click "Update Account"**

### Setting Reference Balance for Existing Accounts

**Scenario**: You already imported transactions but didn't set a reference balance.

**Solution**:
1. Find a recent bank statement or online banking
2. Note the balance on a specific date (e.g., October 1: $10,000)
3. Click "Edit" on your account
4. Set:
   - Reference Balance: **10000**
   - Reference Date: **2025-10-01**
5. Click "Update Account"
6. Current balance updates immediately!

**Formula**:
```
Example:
Reference: $10,000 on Oct 1
Transactions imported: -$2,570.59
Current Balance: $7,429.41 ✓
```

---

## Account Types Explained

### Checking Accounts
- **Purpose**: Day-to-day spending
- **Balance Sign**: Positive = money in account
- **Typical Transactions**: Salary deposits, bill payments, ATM withdrawals

### Savings Accounts
- **Purpose**: Long-term savings, emergency fund
- **Balance Sign**: Positive = money in account
- **Typical Transactions**: Transfers from checking, interest earned

### Credit Cards
- **Purpose**: Credit spending
- **Balance Sign**: 
  - Positive = You overpaid or got a refund
  - Negative = You owe money to the card issuer
- **Typical Transactions**:
  - Charges (negative) - Shopping, dining, gas
  - Payments (positive) - Paying off the card

---

## Best Practices

### ✅ DO

- **Set reference balance and date** for all accounts
- **Use the earliest date** from your imported transactions as reference date
- **Check your bank statement** for accurate reference balance
- **Update regularly** if your balance changes significantly

### ❌ DON'T

- Don't delete accounts with transactions (you'll lose data!)
- Don't set a reference date in the future
- Don't guess the reference balance (check your actual statement)

---

## Tips & Tricks

### Tip 1: Starting Fresh
If you're just starting to track finances:
- Set today's date as reference date
- Check your online banking for today's balance
- Set that as reference balance

### Tip 2: Historical Tracking
If you want to track past months:
- Find your oldest imported transaction date
- Get the balance from that date
- Set that date and balance as reference

### Tip 3: Credit Card Balances
For credit cards:
- Reference balance is often $0 (when you got the card)
- Or set it to your current balance at statement close date
- Negative = you owe money
- Positive = credit available (rare)

---

## Common Questions

**Q: What if I don't know my balance on a specific date?**  
A: Use today's date and today's balance, then only import future transactions.

**Q: Can I change the reference date later?**  
A: Yes! Just edit the account and update both reference balance and date.

**Q: Why is my current balance negative for a checking account?**  
A: Either:
1. You didn't set a reference balance (showing only sum of transactions)
2. Your reference balance was too low
3. You actually overdrafted

**Q: How often should I update reference balance?**  
A: Usually never! Set it once at the beginning. Current balance auto-updates as you import transactions.

---

## Troubleshooting

**Issue**: Current balance doesn't update after setting reference balance  
**Solution**: Hard refresh your browser (Cmd+Shift+R on Mac, Ctrl+Shift+R on Windows)

**Issue**: Can't delete an account  
**Solution**: The account has associated transactions. Delete those first, or use Admin → Reset Everything

**Issue**: Reference date field won't accept my date  
**Solution**: Use format YYYY-MM-DD or use the date picker (click calendar icon)

---

## Example Workflow

### Setting Up Your Checking Account

```
Step 1: Check Your Bank
- Login to Chase online banking
- Note current balance: $10,234.56
- Note today's date: 2025-10-19

Step 2: Add Account
- Name: Chase Checking
- Type: Checking
- Institution: Chase Bank
- Reference Balance: 10234.56
- Reference Date: 2025-10-19
- Click "Save"

Step 3: Import Transactions
- Go to Import page
- Select "Chase Checking"
- Upload your CSV
- All transactions import correctly

Step 4: Verify Balance
- Return to Accounts page
- Current Balance should match your bank
- Reference Balance: $10,234.56 (As of 2025-10-19)
- Current Balance: (auto-calculated based on transactions)
```

---

## What's Next?

Now that you have accounts set up, you're ready to:
1. **Import transactions** - See [Importing Transactions](./03-importing-transactions.md)
2. **Categorize spending** - See [Categorization](./05-categorization.md)
3. **Create budgets** - See [Budget Management](./07-budgets.md)

---

[← Previous: Getting Started](./01-getting-started.md) | [Back to Index](./00-index.md) | [Next: Importing Transactions →](./03-importing-transactions.md)


