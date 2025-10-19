# 1. Getting Started

[← Back to Index](./00-index.md) | [Next: Account Management →](./02-accounts.md)

---

## Installation

### Prerequisites
- **Python 3.13+** installed on your system
- **Git** (optional, for cloning the repository)
- **Web browser** (Chrome, Firefox, Safari, Edge)

### Step 1: Get the Code

**Option A: Clone from GitHub**
```bash
git clone https://github.com/saeid-h/financial-assistant.git
cd financial-assistant
```

**Option B: Download ZIP**
1. Visit https://github.com/saeid-h/financial-assistant
2. Click "Code" → "Download ZIP"
3. Extract to your desired location

### Step 2: Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Initialize Database

```bash
python src/init_db.py
```

You should see:
```
✓ Database created successfully
✓ 30 default categories seeded
✓ 65+ categorization rules seeded
```

### Step 4: Run the Application

```bash
# Easy way (recommended)
./start.sh

# OR manual way
python src/app.py
```

The application will start on **http://localhost:5001**

**Note**: Port 5000 is often used by macOS AirPlay Receiver, so we use port 5001.

---

## First Launch

### Step 1: Open Your Browser

Navigate to: **http://localhost:5001**

You should see the **Financial Assistant Home Page** with 6 feature cards:
- 💳 Manage Accounts
- 📥 Import Statements
- 🔍 Search & Filter
- 🏷️ Auto-Categorization
- 💰 Budget Management
- 📊 Reports & Charts

### Step 2: System Status Check

At the bottom of the home page, verify:
- ✓ Application is running on port 5001
- ✓ Database is connected
- ✓ Phase 1 & 2 Complete (7 PBIs)

---

## Quick Start Guide

### 5-Minute Setup

**1. Add Your First Account (1 minute)**
- Click "💳 Manage Accounts"
- Click "+ Add Account"
- Fill in:
  - Name: "Chase Checking"
  - Type: Checking
  - Institution: Chase Bank
  - Reference Balance: $10,000
  - Reference Date: 2025-10-01
- Click "Save"

**2. Import Your First CSV (2 minutes)**
- Click "📥 Import Statements"
- Select your account (Chase Checking)
- Click "Choose CSV File"
- Select your bank statement CSV
- Click "Upload and Preview"
- Review transactions
- Click "Confirm Import"

**3. Auto-Categorize (1 minute)**
- Click "🏷️ Auto-Categorization"
- Click "🔄 Auto-Cat Uncategorized" (green button)
- Wait for completion (65+ rules will categorize 80-90% of transactions)
- Click OK

**4. View Your Financial Picture (1 minute)**
- Click "📊 Reports & Charts"
- See 4 interactive charts:
  - Monthly Income vs Expenses
  - Spending by Category
  - Monthly Category Trends
  - Top 10 Categories
- Adjust date range if needed

**🎉 Congratulations!** You're now tracking your finances!

---

## Understanding the Interface

### Navigation Bar

Located at the top of every page:

```
┌────────────────────────────────────────────────┐
│ Financial Assistant                            │
│ [Home] [Accounts] [Transactions] [Categories]  │
│ [Reports] [Budgets] [Admin]                    │
└────────────────────────────────────────────────┘
```

- **Home** - Return to main dashboard
- **Accounts** - Manage your accounts
- **Transactions** - View and search all transactions
- **Categories** - View categories and rules, recategorize
- **Reports** - Visual charts and analysis
- **Budgets** - Set and track monthly budgets
- **Admin** - Database management and tools

### Home Page Features

Each feature card is clickable and takes you to that section:

| Feature | What It Does | Status |
|---------|--------------|--------|
| 💳 Manage Accounts | Add/edit checking, savings, credit cards | ✓ Active |
| 📥 Import Statements | Upload CSV from 100+ banks | ✓ Active |
| 🔍 Search & Filter | Find transactions quickly | ✓ Active |
| 🏷️ Auto-Categorization | Smart categorization with 65+ rules | ✓ Active |
| 💰 Budget Management | Set budgets, track progress | ✓ Active |
| 📊 Reports & Charts | 4 chart types, export to CSV | ✓ Active |

---

## Key Concepts

### Accounts
- **Checking/Savings**: Asset accounts (positive balance = good)
- **Credit Cards**: Liability accounts (negative balance = debt)
- Each account has:
  - **Reference Balance**: Balance at a specific date
  - **Reference Date**: When the reference balance was accurate
  - **Current Balance**: Reference + sum of all transactions

### Transactions
- **Income/Deposits**: GREEN (+) - Money coming IN
- **Expenses/Withdrawals**: RED (-) - Money going OUT
- **Transfers**: PURPLE (±) - Neutral, between your accounts

### Categories
- **3-Level Hierarchy**:
  - Level 1: Income, Expenses (Fixed/Variable/Optional), Transfers & Neutral
  - Level 2: Subcategories (e.g., Groceries, Entertainment, Rent)
  - Level 3: Details (e.g., Weekly Groceries, Monthly Groceries)

### Accounting Paradigm
```
Net Wealth Change = Income - Expenses
(Transfers are excluded - they don't change your net worth!)
```

---

## Next Steps

Now that you're up and running:

1. **Add All Your Accounts** - See [Account Management](./02-accounts.md)
2. **Import All Statements** - See [Importing Transactions](./03-importing-transactions.md)
3. **Set Up Budgets** - See [Budget Management](./07-budgets.md)
4. **Explore Reports** - See [Reports & Charts](./06-reports.md)

---

[← Back to Index](./00-index.md) | [Next: Account Management →](./02-accounts.md)


