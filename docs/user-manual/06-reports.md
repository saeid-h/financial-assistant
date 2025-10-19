# 6. Reports & Charts

[← Previous: Categorization](./05-categorization.md) | [Back to Index](./00-index.md) | [Next: Budget Management →](./07-budgets.md)

---

## Overview

The Reports page provides visual analysis of your spending patterns through 4 interactive charts powered by Chart.js.

**Access**: Click "Reports" in navigation or visit http://localhost:5001/reports

---

## Available Charts

### 1. 📈 Monthly Income vs Expenses (Line Chart)

**What it shows:**
- Income trend over time (green line)
- Expense trend over time (red line)
- Month-by-month comparison

**Use cases:**
- See if spending is increasing/decreasing
- Identify income fluctuations
- Compare summer vs winter spending

**Example:**
```
Jan 2025: Income $5,000, Expenses $3,500
Feb 2025: Income $5,000, Expenses $4,200
Mar 2025: Income $6,500, Expenses $3,800

→ You can see that Feb expenses were high!
```

### 2. 🥧 Spending by Category (Pie Chart)

**What it shows:**
- Percentage of total spending per category
- Visual breakdown of where money goes

**Use cases:**
- Identify biggest spending categories
- See budget allocation needs
- Find savings opportunities

**Example:**
```
Groceries: 35% ($1,050)
Dining Out: 20% ($600)
Transportation: 15% ($450)
Entertainment: 10% ($300)
Other: 20% ($600)

→ Groceries is your biggest expense!
```

### 3. 📊 Monthly Category Trends (Stacked Bar Chart)

**What it shows:**
- Month-by-month spending per category
- Stacked bars show category contribution

**Use cases:**
- See seasonal patterns (heating in winter, AC in summer)
- Track category spending over time
- Identify irregular months

**Example:**
```
October:
  Groceries: $1,200
  Dining: $400
  Gas: $200
  Total: $1,800

November:
  Groceries: $1,500
  Dining: $300
  Gas: $180
  Total: $1,980

→ November groceries were higher (Thanksgiving?)
```

### 4. 📊 Top 10 Categories (Horizontal Bar Chart)

**What it shows:**
- Highest spending categories
- Sorted by amount (largest first)

**Use cases:**
- Quick overview of biggest expenses
- Budget priority identification
- Savings opportunity analysis

**Example:**
```
1. Groceries:      $3,450
2. Rent:           $1,800
3. Dining Out:     $1,200
4. Gas:            $780
5. Entertainment:  $450
...

→ Top 3 categories account for 70% of spending
```

---

## Filtering Reports

### Date Range Filters

**8 Preset Options:**
- Last 7 Days
- Last 30 Days
- Last 90 Days
- Last 6 Months
- Last 12 Months
- This Month
- This Year
- All Time

**Custom Range:**
- Set "Date From" and "Date To"
- Click "Apply Filters"

**Example:**
```
Want to see just October 2025?
Date From: 2025-10-01
Date To: 2025-10-31
[Apply Filters]
```

### Account Filter

**Dropdown**: "All Accounts" or select specific account

**Use cases:**
- Analyze just your credit card spending
- Compare checking vs savings patterns
- Focus on one account

**Example:**
```
Filter: Costco Citi Visa (credit card only)
→ Charts show only Costco card spending
→ Helps track credit card categories
```

### Combining Filters

You can combine account + date range:

**Example**:
```
Account: Chase Checking
Date: Last 90 Days
→ Shows 3-month spending from your checking account
```

---

## Exporting Data

### CSV Export

**Button**: "Export to CSV" (top right of page)

**What you get:**
- CSV file with current filtered data
- Includes all visible transactions
- Headers: Date, Amount, Category, Description
- Opens in Excel/Numbers/Google Sheets

**Use cases:**
- Analyze in spreadsheet software
- Create custom charts
- Share with accountant
- Backup your data

**File naming:**
```
transactions_export_YYYYMMDD_HHMMSS.csv
Example: transactions_export_20251019_154530.csv
```

---

## Interpreting Charts

### Income vs Expenses (Line Chart)

**Green line above red line** = Saving money (good!) ✅
**Red line above green line** = Spending more than earning (warning!) ⚠️
**Lines converging** = Savings decreasing
**Lines diverging** = Savings increasing

**Example interpretation:**
```
Jan: Income $5k, Expenses $3k → Saved $2k ✅
Feb: Income $5k, Expenses $4k → Saved $1k (less)
Mar: Income $5k, Expenses $5.5k → Lost $500 ⚠️

→ Trend is worsening, need to reduce spending!
```

### Category Breakdown (Pie Chart)

**Large slices** = Major spending areas (target for budgets)  
**Many small slices** = Diffused spending (hard to control)  
**One dominant slice** = Concentrated spending (easy to budget)

**Example interpretation:**
```
Groceries: 40% (large slice)
→ Consider setting a grocery budget

10 slices each <5% (many small)
→ Consider grouping into "Miscellaneous"
```

### Monthly Trends (Stacked Bar)

**Growing bars over time** = Spending increasing ⚠️  
**Shrinking bars** = Spending decreasing ✅  
**Consistent bars** = Stable spending  
**Spikes** = Irregular expenses (investigate!)

**Example interpretation:**
```
Jul: $2,000
Aug: $2,100
Sep: $3,500 ← SPIKE!

→ Check September for unusual purchases
```

---

## Best Practices

### ✅ DO

- **Review charts monthly** to catch trends early
- **Use date filters** to compare time periods
- **Export data** before making big changes
- **Focus on top categories** for budget planning
- **Look for spikes** in stacked bar chart (investigate)

### ❌ DON'T

- Don't analyze without categorizing first (charts won't be useful)
- Don't compare different date ranges without adjusting for length
- Don't ignore trends (they show problems early!)

---

## Tips & Tricks

### Tip 1: Month-over-Month Comparison

**Compare this month to last month:**
1. Set Date Range: "This Month"
2. Note total expenses
3. Change to "Last 30 Days"
4. Compare values
5. Are you spending more or less?

### Tip 2: Year-over-Year Comparison

**Compare 2025 to 2024** (if you have data):
1. Filter: 2024-01-01 to 2024-12-31
2. Note total expenses
3. Filter: 2025-01-01 to 2025-12-31
4. Compare values
5. Calculate percentage change

### Tip 3: Seasonal Patterns

**Find seasonal expenses:**
1. Use "Last 12 Months" filter
2. Look at Monthly Trends chart
3. Identify peaks:
   - Summer: Travel, AC, vacation
   - Winter: Heating, holidays
   - Spring: Taxes, home improvement
   - Fall: Back to school, holidays

### Tip 4: Budget Planning

**Use reports to set budgets:**
1. Look at Spending by Category pie chart
2. Identify top 5 categories
3. Go to Budgets page
4. Create budgets for top categories
5. Use average monthly amount from charts

---

## Understanding Chart Data

### What's Included

**Income:**
- Salary, wages, bonuses
- Refunds, cashback
- Gifts received
- Interest earned

**Expenses:**
- Groceries, dining, shopping
- Bills, utilities, insurance
- Transportation, gas
- Entertainment, subscriptions

**EXCLUDED from charts:**
- **Transfers** (between accounts)
- **Uncategorized transactions** (in some charts)

### Why Transfers Are Excluded

Transfers don't change your net worth:
- Paying credit card from checking = $0 net change
- Moving savings to checking = $0 net change
- Internal movements ≠ income or expenses

**Charts show TRUE income/expenses** without transfer noise.

---

## Interactive Features

### Hovering

**Hover over chart elements** to see details:
- Line chart: Exact values for that month
- Pie chart: Category name, amount, percentage
- Bar chart: Category breakdown for that month

### Clicking (Pie Chart)

**Click a pie slice** to:
- Highlight that category
- See exact breakdown
- (Future: Filter transactions to that category)

### Zooming (Future Feature)

Currently not implemented, planned for future:
- Click and drag to zoom
- Reset zoom button
- Drill-down into specific time periods

---

## Common Questions

**Q: Why don't my charts show any data?**  
A: You need to:
1. Import transactions first
2. Categorize them (or run auto-categorize)
3. Refresh the Reports page

**Q: Charts show "No data available"**  
A: Check your date range filter - you might be filtering to a period with no transactions

**Q: Pie chart shows "Uncategorized" as biggest slice**  
A: Go to Categories page → Click "🔄 Auto-Cat Uncategorized" to categorize your transactions

**Q: Can I print the charts?**  
A: Use browser print (Cmd+P / Ctrl+P) - charts will print as images

**Q: Can I customize chart colors?**  
A: Not currently - colors are fixed for consistency

---

## Next Steps

- **Create budgets** based on your spending patterns - See [Budget Management](./07-budgets.md)
- **Understand transfer transactions** - See [Transfer Transactions](./08-transfers.md)
- **Set up alerts** - See [Budget Management](./07-budgets.md)

---

[← Previous: Categorization](./05-categorization.md) | [Back to Index](./00-index.md) | [Next: Budget Management →](./07-budgets.md)


