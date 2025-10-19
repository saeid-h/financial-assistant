# PBI-5: Visual Reports and Spending Analysis

**Status**: Agreed  
**Priority**: High (Phase 1 - MVP)  
**Owner**: Saeed  
**Created**: 2025-10-19  
**Started**: 2025-10-19  

[Back to Backlog](../backlog.md)

## Overview

Provide users with visual insights into their spending patterns through interactive charts and reports. This enables users to understand where their money goes, identify trends, and make informed financial decisions.

## Problem Statement

Users have imported transactions and categorized them, but they need visual representations to:
- Quickly understand spending patterns
- Compare income vs expenses over time
- Identify top spending categories
- Track trends month-over-month and year-over-year
- Export data for further analysis

Currently, users can only view raw transaction data in tables, which makes it difficult to:
- Spot trends and patterns
- Understand overall financial health
- Make data-driven decisions about spending

## User Stories

### Primary User Story
**As a user**, I want to see visual reports of my spending so that I can understand my financial patterns and make better financial decisions.

### Supporting User Stories
1. **As a user**, I want to see a monthly breakdown of my expenses by category so that I know where my money is going
2. **As a user**, I want to compare my income vs expenses over time so that I can see if I'm saving or overspending
3. **As a user**, I want to see category spending trends so that I can identify which areas are increasing or decreasing
4. **As a user**, I want to filter reports by date range so that I can focus on specific time periods
5. **As a user**, I want to export report data to CSV so that I can analyze it in other tools

## Technical Approach

### Architecture
- **Frontend**: Chart.js for interactive visualizations
- **Backend**: Flask API endpoints for aggregated data
- **Database**: SQL queries for efficient data aggregation
- **Components**:
  - Reports page with multiple chart sections
  - Data aggregation services
  - Export functionality

### Data Aggregation Strategy
- Pre-aggregate data by month/category for performance
- Cache results for common queries
- Support filtering by account and date range

### Chart Types
1. **Pie Chart**: Category breakdown (current month)
2. **Bar Chart**: Monthly expenses by category (last 12 months)
3. **Line Chart**: Income vs Expenses timeline (last 12 months)
4. **Stacked Bar Chart**: Category trends over time
5. **Comparison Chart**: Year-over-year analysis

### Technology Stack
- **Chart.js 4.x**: Interactive, responsive charts
- **Pandas**: Data aggregation and transformation
- **Flask**: API endpoints for chart data
- **SQLite**: Efficient aggregate queries

## UX/UI Considerations

### Reports Page Layout
```
┌─────────────────────────────────────────────────────┐
│ Financial Reports                        [Filters]   │
├─────────────────────────────────────────────────────┤
│ Date Range: [Last 12 Months ▼]  Account: [All ▼]   │
│ [Apply] [Export CSV]                                │
├─────────────────────────────────────────────────────┤
│ ┌──────────────────┐  ┌──────────────────────────┐ │
│ │  Income vs       │  │  This Month's            │ │
│ │  Expenses        │  │  Spending by Category    │ │
│ │  [Line Chart]    │  │  [Pie Chart]             │ │
│ └──────────────────┘  └──────────────────────────┘ │
├─────────────────────────────────────────────────────┤
│ ┌───────────────────────────────────────────────┐   │
│ │  Monthly Expenses by Category                 │   │
│ │  [Stacked Bar Chart]                          │   │
│ └───────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────┤
│ ┌───────────────────────────────────────────────┐   │
│ │  Top Spending Categories (This Month)         │   │
│ │  [Horizontal Bar Chart]                       │   │
│ └───────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

### Design Principles
- **Progressive Disclosure**: Show overview first, details on demand
- **Responsive Charts**: All charts resize for different screen sizes
- **Consistent Colors**: Use same color for each category across charts
- **Tooltips**: Interactive tooltips with detailed information
- **Loading States**: Show loading indicators while fetching data
- **Empty States**: Clear messages when no data available

### Filters
- **Date Range Presets**: This Month, Last Month, Last 3 Months, Last 6 Months, Last 12 Months, This Year, Last Year, Custom
- **Account Filter**: All Accounts, or specific account
- **Category Filter**: All Categories, Income Only, Expenses Only, Specific Category

## Acceptance Criteria

### Must Have (MVP)
1. ✅ Reports page accessible from main navigation
2. ✅ Display "Income vs Expenses" line chart for last 12 months
3. ✅ Display "Spending by Category" pie chart for current month
4. ✅ Display "Monthly Expenses by Category" stacked bar chart
5. ✅ Display "Top 10 Spending Categories" horizontal bar chart
6. ✅ Date range filter (predefined ranges)
7. ✅ Account filter (all or specific account)
8. ✅ Export all report data to CSV
9. ✅ Charts are interactive (hover for details)
10. ✅ Charts are responsive (work on different screen sizes)
11. ✅ Empty state handling (no data message)
12. ✅ Loading states while fetching data

### Should Have
- Category color consistency across all charts
- Custom date range selector
- Print-friendly view
- Category filter (income/expenses/specific category)
- Comparison view (compare two periods side-by-side)

### Could Have
- Year-over-year comparison chart
- Trend indicators (up/down arrows, percentages)
- Chart type toggles (switch between chart types)
- Save favorite report configurations
- Schedule automated reports

## Dependencies

### Technical Dependencies
- PBI 2 (CSV Import) - Done ✅
- PBI 3 (Account Management) - Done ✅
- PBI 4 (Transaction Categorization) - Done ✅
- Chart.js library (to be added)

### Data Dependencies
- Transactions must be imported
- Transactions must be categorized (at least partially)
- At least 1 month of data for meaningful reports

## Open Questions

1. ~~Should we pre-calculate aggregations or calculate on-demand?~~
   - **Answer**: Calculate on-demand initially, optimize later if needed
2. ~~What's the default date range?~~
   - **Answer**: Last 12 months
3. ~~Should we cache chart data?~~
   - **Answer**: Not initially, add caching if performance issues arise
4. ~~How to handle accounts with different currencies?~~
   - **Answer**: Out of scope for MVP, assume single currency
5. ~~Should reports include pending/uncleared transactions?~~
   - **Answer**: Include all transactions in database

## Related Tasks

See [tasks.md](./tasks.md) for the complete task breakdown.

## Success Metrics

- Users can view reports within 2 seconds of clicking "Reports" tab
- All charts load and display correctly with sample data
- Export generates valid CSV with all relevant data
- Charts are interactive and responsive
- Users can filter reports by date range and account
- No errors when viewing reports with 10,000+ transactions

## Risk Assessment

### High Risk
- None identified

### Medium Risk
- **Performance**: Large datasets may slow chart rendering
  - Mitigation: Aggregate data on backend, limit data points
- **Browser Compatibility**: Chart.js may have issues on older browsers
  - Mitigation: Test on multiple browsers, provide fallback

### Low Risk
- **Data Quality**: Missing categories may skew visualizations
  - Mitigation: Show "Uncategorized" as separate category
- **User Expectations**: Users may want more chart types
  - Mitigation: Start with core charts, gather feedback

## Implementation Notes

- Use Chart.js for all visualizations
- Color palette should match overall app design
- All API endpoints should return JSON in consistent format
- Consider using DataTables or similar for CSV export
- Ensure all queries use proper indexes for performance

## Revision History

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-10-19 | 1.0 | Initial PBI created | Saeed |

