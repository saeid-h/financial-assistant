# PBI-4: Automatic Transaction Categorization

**Status**: Done  
**Priority**: P0 (MVP - Phase 1)  
**Phase**: Phase 1 - MVP  
**Created**: 2025-10-19  
**Completed**: 2025-10-19  
**Owner**: Saeed Hoss

[View in Backlog](../backlog.md#user-content-4)

## Overview

Implement intelligent automatic categorization of transactions using pattern matching and machine learning from user corrections. Categories will help users understand spending patterns and generate meaningful reports.

## Problem Statement

Users need to:
- Understand where their money goes (spending categories)
- See categorized spending reports
- Not manually categorize thousands of transactions
- Have flexibility to correct and customize categories
- Build custom rules that learn from their behavior

Currently:
- All transactions are "Uncategorized"
- No way to group similar transactions
- Can't generate category-based reports
- Manual categorization would be tedious

## User Stories

As a user, I want to:
1. See transactions automatically categorized by type (groceries, gas, utilities, etc.)
2. Manually assign categories to transactions
3. Have the system learn from my corrections
4. Create custom categories for my specific needs
5. See hierarchical categories (e.g., Expenses → Food → Groceries)
6. View spending by category
7. Override automatic categorization when needed

## Technical Approach

### 1. Category Hierarchy (2-3 Levels)

**Structure**: `Parent → Child → Optional Grandchild`

**Pre-defined Categories** (seeded in database):
```
Income
  └─ Salary
  └─ Freelance
  └─ Investment Returns
  └─ Other Income

Expenses
  ├─ Housing
  │   ├─ Rent/Mortgage
  │   ├─ Utilities
  │   └─ Home Maintenance
  ├─ Food
  │   ├─ Groceries
  │   ├─ Restaurants
  │   └─ Fast Food
  ├─ Transportation
  │   ├─ Gas/Fuel
  │   ├─ Public Transit
  │   ├─ Car Maintenance
  │   └─ Parking
  ├─ Shopping
  │   ├─ Clothing
  │   ├─ Electronics
  │   └─ General Retail
  ├─ Healthcare
  │   ├─ Medical
  │   ├─ Pharmacy
  │   └─ Insurance
  ├─ Entertainment
  │   ├─ Movies/Streaming
  │   ├─ Sports/Hobbies
  │   └─ Events
  └─ Bills
      ├─ Internet/Phone
      ├─ Subscriptions
      └─ Insurance

Transfers
  └─ Between Accounts
  └─ Savings
  └─ Investments
```

### 2. Pattern-Based Auto-Categorization

**Categorization Rules** (stored in `categorization_rules` table):
- Match patterns in transaction descriptions
- Priority-based matching (user rules > system rules)
- Fuzzy matching for flexibility
- Amount-based rules (optional)

**Example Rules**:
```python
{
  "pattern": "COSTCO|WALMART|SAFEWAY|TRADER JOE",
  "category_id": groceries_id,
  "confidence": 0.95,
  "rule_type": "system"
}

{
  "pattern": "SHELL|CHEVRON|76|ARCO|GAS",
  "category_id": gas_fuel_id,
  "confidence": 0.95,
  "rule_type": "system"
}
```

### 3. Manual Categorization UI

**Transaction List Enhancements**:
- Category dropdown on each transaction
- Quick-categorize button
- Bulk categorization (select multiple)
- Category filter/search

**Categorization Modal**:
- Search categories
- Browse hierarchy
- Create new category
- "Apply to similar transactions" checkbox

### 4. Learning System

**When User Manually Categorizes**:
1. Capture: transaction description pattern
2. Create/Update rule in database
3. Set rule_type = "user"
4. Higher priority than system rules
5. Option: "Apply to all similar transactions"

**Rule Creation Logic**:
```python
# User categorizes "STARBUCKS #1234" as "Food → Coffee"
# System extracts: "STARBUCKS"
# Creates rule: pattern="STARBUCKS", category="Coffee"
# Future "STARBUCKS #5678" auto-categorizes
```

### 5. Categorization Engine

**On Import**:
- Check each transaction against rules
- Match by priority: user rules → system rules
- Assign best match (highest confidence)
- Flag low-confidence matches for review

**Re-categorization**:
- User can trigger re-categorization
- Apply new rules to existing transactions
- Keep manual overrides

## UX/UI Considerations

### Transaction List
- Show category badge on each transaction
- Color-coded by category type
- Click to change category
- Bulk select for multi-categorize

### Category Management Page
- View all categories
- Add/edit/delete custom categories
- View categorization rules
- Enable/disable rules

### Reports Integration
- "Spending by Category" chart
- Category breakdown in statistics
- Filter by category

## Acceptance Criteria

1. ✅ 30+ default categories seeded in database
2. ✅ Categories display in transaction list
3. ✅ User can manually categorize any transaction
4. ✅ Pattern-based rules automatically categorize on import (56 rules)
5. ✅ System learns from user categorizations (API implemented)
6. ✅ Category dropdown shows hierarchical structure
7. ⏳ Bulk categorization works (API ready, UI pending)
8. ⏳ Category filter works on transaction page (pending)
9. ⏳ Statistics show category breakdowns (pending PBI-5)
10. ⏳ Users can create custom categories (API ready, UI pending)

## Dependencies

- PBI-1: Project Setup ✅ Done
- PBI-2: CSV Import ✅ Done
- PBI-3: Account Management ✅ Done
- Database: `categories` table ✅ Exists
- Database: `categorization_rules` table ✅ Exists

## Implementation Plan

### Phase 1: Basic Manual Categorization
- Add category dropdown to transactions
- Implement manual assignment
- Show categories in transaction list

### Phase 2: Pattern-Based Auto-Categorization
- Seed default rules
- Build matching engine
- Auto-categorize on import

### Phase 3: Learning System
- Capture user corrections
- Generate rules from patterns
- Apply to similar transactions

### Phase 4: Advanced Features
- Bulk categorization
- Custom categories
- Category management UI
- Reports integration

## Open Questions

1. Should we use fuzzy matching? **Answer: Yes, for flexibility**
2. Confidence threshold for auto-categorization? **Answer: 80%**
3. Allow users to delete default categories? **Answer: No, only disable**
4. Re-categorize all transactions when rules change? **Answer: User option**

## Related Tasks

See tasks.md for detailed breakdown.

## Success Metrics

- 80%+ of transactions auto-categorized
- User creates avg 5 custom categories
- 95%+ categorization accuracy after corrections
- Reduces manual work by 90%


