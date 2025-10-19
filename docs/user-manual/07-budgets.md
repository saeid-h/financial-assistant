# 7. Budget Management

[← Previous: Reports & Charts](./06-reports.md) | [Back to Index](./00-index.md) | [Next: Transfer Transactions →](./08-transfers.md)

---

## Overview

Create monthly budgets for your spending categories, track progress in real-time, and receive alerts when approaching or exceeding limits.

**Access**: Click "Budgets" in navigation or visit http://localhost:5001/budgets

---

## Creating a Budget

### Step-by-Step

1. **Click "+ Create Budget"** button (top right)

2. **Fill in the form:**

   **Category** (Required)
   - Select from dropdown
   - Choose a spending category
   - Example: Groceries, Dining Out, Entertainment

   **Month** (Required)
   - Format: YYYY-MM
   - Example: 2025-11 (November 2025)
   - Use date picker or type manually

   **Amount Limit** (Required)
   - Your budget limit for this category this month
   - Example: $500 for groceries
   - Enter as decimal: 500.00

3. **Click "Save"**

### Example

```
Creating Grocery Budget for November:

Category: Groceries
Month: 2025-11
Amount: 500.00

[Save] [Cancel]
```

---

## Understanding Budget Cards

Each budget is displayed as a card:

```
┌─────────────────────────────────────────────┐
│ Groceries - November 2025                   │
│                                             │
│ Budget: $500.00                             │
│ Spent: $234.50 (47%)                        │
│                                             │
│ ▓▓▓▓▓▓░░░░░░░░ 47%                          │
│                                             │
│ Remaining: $265.50                          │
│ Status: 🟢 On Track                         │
│                                             │
│ [Edit] [Delete]                             │
└─────────────────────────────────────────────┘
```

### Budget Components

**Budget Amount**: Your limit ($500)  
**Spent**: Current spending in this category ($234.50)  
**Percentage**: Spent / Budget (47%)  
**Progress Bar**: Visual indicator  
**Remaining**: Budget - Spent ($265.50)  
**Status**: Alert level (see below)

---

## Budget Status & Alerts

### Status Levels

**🟢 On Track** (0-79% spent)
- Spending is under control
- Green progress bar
- You're doing great!

**🟡 Warning** (80-99% spent)  
- Approaching limit
- Yellow progress bar
- Time to slow down

**🔴 Over Budget** (100%+ spent)
- Exceeded limit
- Red progress bar
- Need to cut back or adjust budget

### Alert Thresholds

Configurable in Budget Service (default):
- **Warning**: 80% of budget
- **Over Budget**: 100% of budget

---

## Editing a Budget

**Steps:**
1. Click **"Edit"** on the budget card
2. Update:
   - Category (if needed)
   - Month (to apply to different month)
   - Amount (adjust limit up/down)
3. Click **"Update Budget"**

**Use cases:**
- Increase limit if too restrictive
- Decrease limit if too generous
- Copy budget to next month (change month field)

---

## Deleting a Budget

**Steps:**
1. Click **"Delete"** on the budget card
2. Confirm deletion

**Note**: This only deletes the budget tracking, not the transactions.

---

## Budget Best Practices

### Setting Realistic Budgets

**DON'T:**
- Set unrealistic goals ($50/month for groceries for family of 4)
- Copy someone else's budget
- Use round numbers without analysis

**DO:**
1. Check Reports → Spending by Category
2. See your average monthly spending per category
3. Start with current average
4. Reduce by 10-20% if trying to save

**Example:**
```
Current grocery spending (3-month average): $600/month

Budget options:
- Aggressive: $480/month (20% reduction)
- Moderate: $540/month (10% reduction)
- Maintenance: $600/month (current level)
```

### Which Categories to Budget

**High-impact categories** (budget these first):
- ✅ Groceries (usually #1 variable expense)
- ✅ Dining Out (easy to reduce)
- ✅ Entertainment (discretionary)
- ✅ Shopping (discretionary)
- ✅ Transportation (gas, if variable)

**Low-impact categories** (maybe skip):
- Fixed expenses (rent, insurance - can't easily change)
- Utilities (seasonal, hard to predict)
- One-time purchases

### Budget Frequency

**Monthly** is recommended because:
- Most bills are monthly
- Easy to track and adjust
- Matches bank statement cycles
- Natural planning period

---

## Tracking Progress

### Real-Time Updates

Budgets update **automatically** as you:
- Import new transactions
- Categorize transactions
- Delete transactions

**Example:**
```
Morning: Groceries budget at $234.50 (47%)
→ Import evening Costco trip: -$87.50
Afternoon: Groceries budget at $322.00 (64%)
```

### Mid-Month Check-In

**Recommended**: Check budgets around 15th of each month

1. Visit Budgets page
2. Review each budget status
3. **If yellow/red**:
   - Analyze spending on that category
   - Reduce spending for rest of month
   - Or adjust budget if unrealistic

---

## Budget Strategies

### Strategy 1: Envelope Method

Create budgets for ALL discretionary categories:
```
Groceries: $500
Dining Out: $200
Entertainment: $100
Shopping: $150
Gas: $200

Total Discretionary: $1,150/month
```

When a category hits 100%, stop spending there!

### Strategy 2: Focus Method

Budget only your top 3 problem categories:
```
Dining Out: $200 (you're overspending here)
Entertainment: $100 (subscriptions adding up)
Shopping: $150 (impulse purchases)
```

Ignore other categories, focus on improvement areas.

### Strategy 3: Savings Goal Method

Calculate savings goal first, then budget:
```
Monthly Income: $5,000
Savings Goal: $1,000 (20%)
Available for Spending: $4,000

Fixed Expenses: $2,200 (rent, utilities, insurance)
Remaining for Variable: $1,800

Budget:
- Groceries: $600
- Dining: $300
- Entertainment: $200
- Gas: $200
- Other: $500
Total: $1,800 (matches available!)
```

---

## Budget Reports Integration

### Using Reports to Set Budgets

1. Go to **Reports** page
2. Set filter: **"Last 90 Days"**
3. Look at **"Spending by Category"** pie chart
4. Identify top categories
5. Go to **Budgets** page
6. Create budgets for top categories
7. Use **average monthly amount** from last 3 months

**Example:**
```
From Reports (Last 90 Days):
Groceries total: $1,800 (3 months)
→ Average: $600/month

Create Budget:
Category: Groceries
Month: 2025-11 (next month)
Amount: $540 (10% reduction to save money)
```

---

## Common Scenarios

### Scenario 1: Going Over Budget

**What happened:**
- Groceries budget: $500
- Current spending: $580 (116%)
- Status: 🔴 Over Budget

**What to do:**
1. **Analyze**: Go to Transactions → Filter by Groceries
2. **Identify**: What caused overspending?
   - One large purchase? (Costco run)
   - Many small purchases? (eating out counted as groceries)
3. **Adjust**:
   - Option A: Reduce spending next month to compensate
   - Option B: Increase budget if it was too low
   - Option C: Recategorize incorrect transactions

### Scenario 2: Under Budget

**What happened:**
- Dining Out budget: $300
- Current spending: $120 (40%)
- Status: 🟢 On Track

**What to do:**
- **Celebrate!** You're doing great
- **Consider**: Can you reduce this budget further?
- **Reallocate**: Move savings to another category or goals

### Scenario 3: Budget Too Restrictive

**What happened:**
- Set grocery budget at $300
- Always exceed it (consistently 150-200%)
- Causing stress

**What to do:**
1. **Check reality**: Go to Reports → Last 3 months average
2. **Adjust budget**: Set to realistic level
3. **Then gradually reduce**: 10% per month until target reached

**Example:**
```
Current average: $600/month
Budget was: $300 (too aggressive!)

New approach:
Month 1: $600 (maintain current)
Month 2: $540 (10% reduction)
Month 3: $486 (10% more)
Month 4: $437 (10% more)
...
Eventually reach $300 goal
```

---

## Multiple Budgets

You can create multiple budgets:
- **Same category, different months**: Track progress over time
- **Different categories, same month**: Track multiple areas

**Example:**
```
November 2025 Budgets:
- Groceries: $500
- Dining Out: $200
- Entertainment: $100
- Gas: $200
Total: $1,000/month discretionary budget
```

---

## Tips & Tricks

### Tip 1: Start Small
Don't budget everything at once:
- Month 1: Budget top 2 categories
- Month 2: Add 2 more
- Month 3: Add final categories
- Gradually build discipline

### Tip 2: Use Round Numbers
- $500/month instead of $487.32
- Easier to remember
- Psychological impact ("I have $500")

### Tip 3: Include Buffer
- Set budget slightly below target
- Example: Want to spend $500, set budget at $450
- Creates cushion for unexpected items

### Tip 4: Review Weekly
- Check budgets every Sunday
- Mid-month check prevents overspending
- Adjust behavior early

---

## Troubleshooting

**Issue**: Budget shows 0% even though I've spent money  
**Solution**: Transactions aren't categorized - categorize them first

**Issue**: Budget shows >100% immediately  
**Solution**: You set the budget too low, or current month already has high spending - edit budget or wait for next month

**Issue**: Can't create budget for a category  
**Solution**: Category might not exist - create it first in Category Management

**Issue**: Budget disappeared  
**Solution**: Check if you accidentally deleted it - create a new one

---

## Next Steps

- **Understand transfers** - See [Transfer Transactions](./08-transfers.md)
- **Manage database** - See [Admin Functions](./09-admin.md)
- **Troubleshoot issues** - See [Troubleshooting](./10-troubleshooting.md)

---

[← Previous: Reports & Charts](./06-reports.md) | [Back to Index](./00-index.md) | [Next: Transfer Transactions →](./08-transfers.md)


