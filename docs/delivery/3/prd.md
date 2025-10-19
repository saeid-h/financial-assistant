# PBI-3: Complete Account Management and Transaction Views

**Status**: Done  
**Priority**: P0 (Highest)  
**Phase**: Phase 1 - MVP  
**Created**: 2025-10-19  
**Completed**: 2025-10-19  
**Owner**: Saeed Hoss

[View in Backlog](../backlog.md#user-content-3)

## Overview

Complete the account management system by adding account-specific transaction views, detailed statistics, and account-type-aware display logic. This builds on the basic account CRUD operations from PBI-2 Task 2-1.

## Problem Statement

Users need to:
- View transactions for a specific account
- Understand account-specific financial patterns
- See correct sign conventions based on account type (checking vs credit card)
- Access detailed account information and statistics
- Navigate seamlessly between accounts and transactions

Currently:
- Accounts can be created/edited/deleted (from PBI-2)
- All transactions shown in one view
- No account-specific statistics
- Sign conventions don't consider account type

## User Stories

As a user, I want to:
1. Click on an account to see only its transactions
2. See account-specific statistics (balance, totals, transaction count)
3. Have credit card transactions displayed correctly (charges positive, payments negative)
4. Have bank account transactions displayed correctly (withdrawals negative, deposits positive)
5. Navigate easily between account view and all transactions
6. See which account each transaction belongs to

## Technical Approach

### 1. Account Details Page

**Route**: `/accounts/<account_id>`

**Features**:
- Account information header
- Account statistics:
  - Total transactions
  - Total credits (income/deposits/payments)
  - Total debits (expenses/withdrawals/charges)
  - Net cash flow
  - Current effective balance
- Filtered transaction list (this account only)
- Link back to all accounts

### 2. Account-Type-Aware Display

**Logic**:
Currently we follow accounting standards uniformly:
- Credit (deposits/income/payments) = Positive
- Debit (withdrawals/expenses/charges) = Negative

This works correctly for BOTH bank accounts AND credit cards from an accounting perspective.

**User Perspective**:
- Bank account: "Money in is good (positive), money out is bad (negative)" ✓ Current behavior
- Credit card: "Payments are good (reduce debt), charges are bad (increase debt)" ✓ Current behavior

**No change needed** - current implementation is correct!

### 3. Transaction Page Enhancements

**Add**:
- Account name in transaction list ✓ Already done
- Filter by account dropdown ✓ Already done
- Account statistics by filter ✓ Already done

### 4. Navigation Improvements

**Add**:
- "View Transactions" button on account cards
- "Filter by this account" option in transaction page
- Breadcrumb navigation

## UX/UI Considerations

### Account Cards Enhancement
- Add "View Transactions" button
- Show transaction count on card
- Show last transaction date

### Account Details Page
- Clean, focused layout
- Statistics cards at top
- Transaction list below
- Back button to accounts list

### Transaction List
- Account name column ✓ Done
- Filter dropdown ✓ Done
- Color coding by account type (optional)

## Acceptance Criteria

1. ✅ Users can view account list (Done in PBI-2)
2. ✅ Users can create/edit/delete accounts (Done in PBI-2)
3. ✅ Users can click account card buttons to view/edit
4. ✅ Users can view transactions for specific account
5. ✅ Account details page shows statistics
6. ✅ Transaction page shows account names (Done in PBI-2)
7. ✅ Import workflow handles large files (815+ transactions)
8. ✅ Transactions stored with correct account linkage
9. ✅ Account type properly influences display (accounting standards)

## Dependencies

- PBI-1: Project Setup ✅ Done
- PBI-2: CSV Import ✅ Done
- Database schema with foreign keys ✅ Done
- Transaction model ✅ Done
- Account model ✅ Done

## Open Questions

1. ~~Should credit cards show opposite signs from bank accounts?~~
   - **Answer**: No - accounting standards apply universally
   - Current implementation is correct
   
2. ~~How to handle large CSV imports (session size limit)?~~
   - **Answer**: Don't store in session, re-parse from temp file
   - ✅ Fixed in this PBI

3. Should we add "current balance" tracking?
   - **Answer**: Calculate from transactions (not store separately)
   - Use last transaction's balance if available

## Related Tasks

- Task 2-1: Account Management UI (foundation)
- Task 2-5: Import Upload UI (uses accounts)
- Tasks in this PBI: See tasks.md

## Success Metrics

- Import 800+ transactions successfully
- View account-specific statistics correctly
- Navigate smoothly between accounts and transactions
- All tests passing
- No session size errors


