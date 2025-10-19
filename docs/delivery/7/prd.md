# PBI-7: Budget Management System

**Status**: Done  
**Priority**: High (Phase 2)  
**Owner**: Saeed  
**Created**: 2025-10-20  
**Started**: 2025-10-20  
**Completed**: 2025-10-20  

[Back to Backlog](../backlog.md)

## Overview

Implement a comprehensive budget management system that allows users to set monthly or yearly budgets for spending categories, track progress against budgets, and receive alerts when approaching or exceeding limits.

## Problem Statement

Users can see their spending in reports, but they cannot:
- Set spending limits for categories
- Track budget vs actual spending
- Get warned when approaching budget limits
- Plan future spending based on budgets
- Compare budget performance over time

This makes it difficult to:
- Control spending proactively
- Achieve financial goals
- Identify overspending categories
- Plan monthly expenses

## User Stories

### Primary User Story
**As a user**, I want to set budgets for categories so that I can control my spending and achieve my financial goals.

### Supporting User Stories
1. **As a user**, I want to create monthly budgets for each category so that I can plan my spending
2. **As a user**, I want to see visual progress indicators showing budget usage so that I know how much I have left
3. **As a user**, I want to receive alerts when I'm approaching a budget limit so that I can adjust my spending
4. **As a user**, I want to see budget vs actual reports so that I can understand my spending patterns
5. **As a user**, I want to copy budgets from previous months so that I don't have to recreate them

## Technical Approach

### Database Schema
```sql
CREATE TABLE budgets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    period_type TEXT NOT NULL CHECK(period_type IN ('monthly', 'yearly')),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    alert_threshold INTEGER DEFAULT 80,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);
```

### Components
- Budget management page
- Budget creation/edit modal
- Budget progress cards
- Budget vs actual charts
- Alert system

## Acceptance Criteria

### Must Have
1. ✅ Create monthly budgets for categories
2. ✅ Edit and delete budgets
3. ✅ Visual progress bars showing budget usage
4. ✅ Budget vs actual comparison
5. ✅ Alert when exceeding budget (visual indicator)
6. ✅ Budget overview dashboard
7. ✅ Copy budget to next month

### Should Have
- Yearly budgets
- Budget templates
- Historical budget performance
- Overspending insights

## Related Tasks
See [tasks.md](./tasks.md) for task breakdown.

## Revision History
| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-10-20 | 1.0 | Initial PBI created | Saeed |

