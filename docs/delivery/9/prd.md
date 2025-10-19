# PBI 9: Recurring Transaction Detection

**Status**: Agreed  
**Priority**: High  
**Complexity**: Medium  
**Owner**: Saeed  
**Created**: 2025-10-19  
**Start Date**: 2025-10-19  
**Target Completion**: TBD  

[Back to Backlog](../backlog.md)

---

## Overview

Implement automatic detection of recurring transactions (subscriptions, bills, regular payments) to help users manage ongoing financial commitments. The system will identify patterns in transaction history, track recurring items, and alert users to missing or changed payments.

## Problem Statement

Users have recurring financial commitments (subscriptions, bills, rent, insurance) that:
- Can be forgotten or overlooked
- May change without notice
- Are difficult to track across multiple accounts
- Need manual categorization every month
- Can cause budget issues if missed

**Current Pain Points:**
- No visibility into recurring expenses
- Can't track which subscriptions are active
- Missing payments go unnoticed
- Amount changes (price increases) aren't detected
- Manual effort to categorize the same transaction monthly

## User Stories

### Primary User Stories

**As a user, I want recurring transactions automatically detected**
- So I don't have to manually track subscriptions and bills
- And I can see all my recurring commitments in one place

**As a user, I want to be alerted when a recurring payment is missing**
- So I know if I missed a payment or a subscription was cancelled
- And I can take action if needed

**As a user, I want to be alerted when a recurring payment amount changes**
- So I'm aware of price increases
- And I can review if the change is expected

**As a user, I want recurring transactions automatically categorized**
- So I don't have to categorize the same transaction every month
- And my categorization is consistent

## Technical Approach

### Detection Algorithm

**Pattern Recognition:**
1. **Similar Description Matching** (Fuzzy matching with 85%+ similarity)
   - Netflix → Netflix Subscription
   - SPOTIFY → Spotify Premium
   - Use Levenshtein distance or similar

2. **Regular Intervals** (Weekly, Monthly, Quarterly, Annually)
   - Weekly: 7 days ± 2 days tolerance
   - Bi-weekly: 14 days ± 3 days
   - Monthly: 28-31 days ± 3 days
   - Quarterly: 90 days ± 7 days
   - Annually: 365 days ± 14 days

3. **Consistent Amount** (±10% variance allowed)
   - Exact: Same amount every time
   - Similar: Within 10% (allows for variable bills like utilities)

4. **Minimum Occurrences**: Require 3+ matches to establish pattern

### Database Schema

```sql
CREATE TABLE recurring_transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    merchant_name TEXT NOT NULL,
    description_pattern TEXT,
    frequency TEXT CHECK(frequency IN ('weekly', 'biweekly', 'monthly', 'quarterly', 'annual')),
    average_amount DECIMAL(12, 2),
    amount_variance DECIMAL(12, 2),
    category_id INTEGER,
    last_transaction_date DATE,
    next_expected_date DATE,
    status TEXT CHECK(status IN ('active', 'paused', 'cancelled')) DEFAULT 'active',
    alert_if_missing BOOLEAN DEFAULT 1,
    alert_if_amount_changes BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

CREATE TABLE recurring_transaction_instances (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recurring_id INTEGER NOT NULL,
    transaction_id INTEGER NOT NULL,
    expected_date DATE,
    actual_date DATE,
    expected_amount DECIMAL(12, 2),
    actual_amount DECIMAL(12, 2),
    variance_amount DECIMAL(12, 2),
    status TEXT CHECK(status IN ('on_time', 'late', 'missed', 'amount_changed')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (recurring_id) REFERENCES recurring_transactions(id) ON DELETE CASCADE,
    FOREIGN KEY (transaction_id) REFERENCES transactions(id) ON DELETE CASCADE
);
```

### Services

**RecurringTransactionDetector:**
- `scan_for_patterns()` - Analyze all transactions for patterns
- `detect_recurring(transaction)` - Check if new transaction matches pattern
- `calculate_next_expected()` - Predict next occurrence
- `check_for_missing()` - Identify missed payments

**RecurringTransactionManager:**
- CRUD operations for recurring transactions
- `get_all_active()` - List active recurring items
- `get_upcoming(days)` - Get expected transactions in next N days
- `get_alerts()` - Get missing/changed payment alerts

## UX/UI Considerations

### Recurring Transactions Page (`/recurring`)

**Layout:**
```
┌─────────────────────────────────────────────┐
│ 🔄 Recurring Transactions                   │
│ [🔍 Scan for New Patterns]  [➕ Add Manual] │
├─────────────────────────────────────────────┤
│ 📊 Summary                                  │
│ Active: 12 | Total Monthly: $1,245.50      │
│ Upcoming (7 days): 3 | Alerts: 2           │
├─────────────────────────────────────────────┤
│ 🚨 Alerts                                   │
│ ⚠️ Netflix payment missing (due 3 days ago)│
│ ⚠️ Electric bill increased by $25          │
├─────────────────────────────────────────────┤
│ 📋 Active Recurring Transactions           │
│                                             │
│ [Monthly] Netflix - $15.99                 │
│ 💳 Entertainment | Next: Oct 25            │
│ [Edit] [Pause] [Delete] [View History]     │
│                                             │
│ [Monthly] Rent - $1,800.00                 │
│ 🏠 Fixed Expenses | Next: Nov 1            │
│ [Edit] [Pause] [Delete] [View History]     │
└─────────────────────────────────────────────┘
```

### Visual Indicators

- **Status Colors:**
  - 🟢 Green: On time, no issues
  - 🟡 Yellow: Amount variance detected
  - 🔴 Red: Payment missing
  - ⏸️ Gray: Paused

- **Frequency Icons:**
  - 📅 Weekly
  - 📆 Monthly
  - 📊 Quarterly
  - 📈 Annual

## Acceptance Criteria

### Must Have (Phase 1)
- [ ] Detect recurring patterns from existing transactions (3+ occurrences)
- [ ] Support 5 frequency types (weekly, bi-weekly, monthly, quarterly, annual)
- [ ] Display list of detected recurring transactions
- [ ] Show upcoming expected payments (next 30 days)
- [ ] Alert on missing payments (3+ days overdue)
- [ ] Alert on amount changes (>10% variance)
- [ ] Edit recurring transaction details (name, amount, frequency)
- [ ] Pause/resume recurring tracking
- [ ] Delete recurring transaction
- [ ] Automatically categorize matched transactions

### Should Have (Phase 2)
- [ ] Manual add recurring transaction
- [ ] View transaction history for each recurring item
- [ ] Export recurring list to CSV
- [ ] Customize alert thresholds per item
- [ ] Fuzzy matching improvements

### Could Have (Phase 3)
- [ ] Predict price increases based on history
- [ ] Group related recurring items (e.g., all utilities)
- [ ] Compare to average (e.g., "Your Netflix is $2 higher than average")
- [ ] Integration with budget (auto-allocate recurring to budget)

## Dependencies

- **Requires:** PBI 2 (Transaction import), PBI 4 (Categorization)
- **Enables:** PBI 11 (Cash flow predictions use recurring data)
- **Related:** PBI 10 (Dashboard displays recurring insights)

## Open Questions

1. ~~How many occurrences to establish a pattern?~~ → **3 occurrences**
2. ~~What tolerance for date variance?~~ → **±10% of frequency period**
3. ~~What tolerance for amount variance?~~ → **±10% of average amount**
4. Should we detect one-time irregular patterns? → **Defer to Phase 2**
5. How to handle split transactions? → **Defer to Phase 2**

## Related Tasks

See [tasks.md](./tasks.md) for detailed task breakdown.

---

## History

| Date | Event | Details |
|------|-------|---------|
| 2025-10-19 | Created | PBI 9 PRD created for Phase 3 implementation |
| 2025-10-19 | Status Change | Moved from Proposed to Agreed |


