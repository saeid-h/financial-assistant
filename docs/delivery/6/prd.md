# PBI-6: Enhanced Transaction Search and Filtering

**Status**: Agreed  
**Priority**: High (Phase 2)  
**Owner**: Saeed  
**Created**: 2025-10-20  
**Started**: 2025-10-20  

[Back to Backlog](../backlog.md)

## Overview

Enhance the transactions page with powerful search and filtering capabilities, allowing users to quickly find specific transactions, add notes and tags for better organization, and perform bulk operations on multiple transactions.

## Problem Statement

Currently, users can filter transactions by account and date range, but they cannot:
- Search for specific merchants or descriptions
- Filter by amount ranges
- Add personal notes to transactions
- Tag transactions with custom labels
- Perform bulk operations (categorize, tag, delete multiple items)
- Save and reuse search criteria

This makes it difficult to:
- Find specific transactions quickly
- Track spending at particular merchants
- Add context to unusual transactions
- Organize transactions beyond categories
- Manage large transaction sets efficiently

## User Stories

### Primary User Story
**As a user**, I want to search and filter transactions so that I can quickly find specific purchases or analyze spending patterns.

### Supporting User Stories
1. **As a user**, I want to search by merchant name or description so that I can find all transactions from a specific store
2. **As a user**, I want to filter by amount range so that I can find large purchases or small recurring charges
3. **As a user**, I want to add notes to transactions so that I can remember context or details
4. **As a user**, I want to tag transactions with custom labels so that I can organize them my way
5. **As a user**, I want to perform bulk operations so that I can efficiently manage many transactions at once
6. **As a user**, I want to save search filters so that I can reuse common searches

## Technical Approach

### Architecture
- **Backend**: Enhanced API endpoints with search/filter support
- **Frontend**: Advanced search UI with multi-criteria selection
- **Database**: Add notes and tags tables, full-text search index
- **Components**:
  - Search bar with auto-suggest
  - Advanced filter panel
  - Bulk selection UI
  - Notes/tags editor

### Database Schema Changes
```sql
-- Add notes table
CREATE TABLE transaction_notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_id INTEGER NOT NULL,
    note TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (transaction_id) REFERENCES transactions(id) ON DELETE CASCADE
);

-- Add tags table
CREATE TABLE tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    color TEXT DEFAULT '#667eea',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add transaction_tags junction table
CREATE TABLE transaction_tags (
    transaction_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (transaction_id, tag_id),
    FOREIGN KEY (transaction_id) REFERENCES transactions(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);
```

### Search Strategy
- Use SQLite LIKE for description/merchant search
- Support wildcards and partial matches
- Case-insensitive search
- Multi-field search (description AND/OR amount AND/OR category)

## UX/UI Considerations

### Enhanced Transactions Page Layout
```
┌─────────────────────────────────────────────────────────┐
│ [🔍 Search...]  [🎯 Advanced Filters]  [⚙️ Bulk Actions] │
├─────────────────────────────────────────────────────────┤
│ Active Filters: Date: Last 3 Months | Category: Food    │
│ [✗ Clear All]                                            │
├─────────────────────────────────────────────────────────┤
│ ☑ | Date | Description | Amount | Category | Tags | ⋮  │
│ ☑ | ...  | Walmart     | -$45   | Groceries| 🏷️   | ⋮  │
│   | ...  | Salary      | +$5000 | Income   |      | ⋮  │
└─────────────────────────────────────────────────────────┘
```

### Advanced Filter Panel
- Amount range (min/max)
- Category selector (multi-select)
- Tags filter (any/all)
- Has notes (yes/no/any)
- Transaction type (income/expense/all)
- Save filter button

### Bulk Operations
- Select all / Select none
- Bulk categorize
- Bulk tag
- Bulk delete
- Export selected

## Acceptance Criteria

### Must Have (Phase 2)
1. ✅ Search box in transactions page
2. ✅ Search by description/merchant (case-insensitive, partial match)
3. ✅ Filter by amount range (min and/or max)
4. ✅ Filter by multiple categories
5. ✅ Add notes to individual transactions
6. ✅ Create and manage custom tags
7. ✅ Tag transactions (one or multiple tags per transaction)
8. ✅ Filter by tags
9. ✅ Bulk select transactions (checkboxes)
10. ✅ Bulk categorize selected transactions
11. ✅ Bulk tag selected transactions
12. ✅ Active filters displayed with clear all option
13. ✅ Search performs well with 10,000+ transactions

### Should Have
- Auto-suggest for merchant names
- Search history
- Saved searches/filters
- Bulk delete with confirmation
- Export selected transactions
- Quick filters (preset common searches)

### Could Have
- Advanced query builder
- Regular expression search
- Fuzzy matching for merchants
- Smart search (natural language)

## Dependencies

### Technical Dependencies
- PBI 2 (CSV Import) - Done ✅
- PBI 3 (Account Management) - Done ✅
- PBI 4 (Transaction Categorization) - Done ✅
- SQLite FTS5 extension (built-in)

### Data Dependencies
- Transactions must be imported
- Database schema must be extended

## Open Questions

1. ~~Should search be real-time or require "Search" button click?~~
   - **Answer**: Real-time with debouncing (500ms)
2. ~~How many tags can a transaction have?~~
   - **Answer**: Unlimited
3. ~~Should we support saved searches?~~
   - **Answer**: Not in MVP, add later if requested
4. ~~Bulk operations limit?~~
   - **Answer**: Warn if > 100 selected, require confirmation

## Related Tasks

See [tasks.md](./tasks.md) for the complete task breakdown.

## Success Metrics

- Users can find any transaction in < 5 seconds
- Search returns results in < 200ms for 10,000 transactions
- Bulk operations complete in < 1 second for 100 items
- Users can add notes and tags without page reload
- All filters can be combined (AND logic)
- Active filters clearly visible
- Search with no results shows helpful message

## Risk Assessment

### Medium Risk
- **Performance**: Full-text search on large datasets
  - Mitigation: Use SQLite FTS5, add indexes, pagination
- **UX Complexity**: Too many filter options may confuse users
  - Mitigation: Progressive disclosure, clear labels, defaults

### Low Risk
- **Data integrity**: Notes/tags not critical to financial accuracy
  - Mitigation: Regular backups, soft delete option

## Implementation Notes

- Use FTS5 virtual table for fast text search
- Debounce search input to avoid excessive queries
- Use prepared statements to prevent SQL injection
- Validate all search parameters
- Add indexes on frequently filtered fields
- Consider pagination for very large result sets
- Store tags with color codes for visual distinction

## Revision History

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-10-20 | 1.0 | Initial PBI created | Saeed |

