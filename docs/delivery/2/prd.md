# PBI-2: CSV Import and Transaction Management

**Status**: Done  
**Priority**: P0 (Highest)  
**Phase**: Phase 1 - MVP  
**Created**: 2025-10-19  
**Completed**: 2025-10-19  
**Owner**: Saeed Hoss

[View in Backlog](../backlog.md#user-content-2)

## Overview

Enable users to import bank and credit card statements from CSV files through a web interface. The system will parse transactions, validate data, detect duplicates, and store them in the database with proper archiving of source files.

## Problem Statement

Users need a way to get their financial data into the system. Manual entry is time-consuming and error-prone. Banks provide CSV exports of transactions, but:
- CSV formats vary by institution
- Users need to prevent duplicate imports
- Source files should be organized for reference
- Data quality must be validated before storage

## User Stories

As a user, I want to:
1. Upload CSV files containing my bank/credit card transactions via a web interface
2. See the transactions parsed and displayed before final import
3. Be warned if transactions already exist (duplicate detection)
4. Have my CSV files automatically archived by date for future reference
5. See a confirmation of how many transactions were imported
6. Update my data with new transactions from recent statements

## Technical Approach

### 1. File Upload Interface

**Upload Page** (`/import`)
- File input field accepting CSV files
- Account selection dropdown (from existing accounts)
- Upload button
- Progress indicator

**Technology:**
- HTML5 file input
- Flask file upload handling
- Client-side file validation (size, type)

### 2. CSV Parsing Strategy

**Flexible Parser:**
- Use pandas `read_csv()` for robust parsing
- Auto-detect delimiter (comma, semicolon, tab)
- Handle various date formats
- Support common CSV structures

**Expected CSV Format (Flexible):**
```csv
Date,Description,Amount,Balance
2025-10-01,Grocery Store,-45.50,1234.50
2025-10-02,Salary Deposit,2500.00,3734.50
```

**Alternative formats supported:**
- Date, Merchant, Debit, Credit
- Transaction Date, Description, Withdrawal, Deposit
- Auto-detect columns by common names

### 3. Data Validation

**Required Validations:**
1. Date is valid and parsable
2. Amount is numeric
3. Description is not empty
4. CSV has minimum required columns (date, description, amount)

**Error Handling:**
- Display validation errors to user
- Allow user to fix and re-upload
- Log parsing errors for debugging

### 4. Duplicate Detection

**Strategy:**
- Check if transaction exists with same:
  - Account ID
  - Date
  - Description (normalized)
  - Amount (within 0.01 tolerance)

**User Options:**
- Skip duplicates (default)
- Force import (update existing)
- Selective import (user chooses)

### 5. Database Storage

**Transaction Insert:**
```python
INSERT INTO transactions (
    account_id, date, description, amount,
    category_id, notes, tags,
    created_at, updated_at
) VALUES (?, ?, ?, ?, NULL, NULL, NULL, ?, ?)
```

**Batch Insert:**
- Use batch operations for performance
- Transaction safety (all or nothing)

### 6. File Archiving

**Archive Structure:**
```
data/
  2025/
    10/
      statement_checking_20251019_143022.csv
      statement_credit_20251019_143045.csv
```

**Naming Convention:**
```
statement_{account_name}_{YYYYMMDD}_{HHMMSS}.csv
```

### 7. Import Workflow

```
1. User uploads CSV file
2. System validates file format
3. Parse CSV with pandas
4. Validate each transaction
5. Check for duplicates
6. Display preview to user
7. User confirms import
8. Store transactions in database
9. Archive CSV file
10. Display success message with count
```

## UX/UI Considerations

### Import Page Layout

**Header:**
- Page title: "Import Transactions"
- Breadcrumb: Home > Import

**Form Section:**
1. Account Selection
   - Dropdown: "Select Account"
   - Link: "Don't see your account? Add one"

2. File Upload
   - File input with "Choose CSV File" button
   - Show selected filename
   - File size and format info

3. Options
   - Checkbox: "Skip duplicate transactions" (default: checked)
   - Checkbox: "Archive source file" (default: checked)

4. Action Buttons
   - "Upload and Parse" (primary button)
   - "Cancel" (secondary button)

**Preview Section:**
- Table showing parsed transactions
- Columns: Date, Description, Amount, Status
- Status indicators:
  - ✓ New transaction (green)
  - ⚠ Duplicate found (yellow)
  - ✗ Validation error (red)

**Summary Panel:**
- Total transactions in file: X
- New transactions: Y
- Duplicates: Z
- Errors: N

**Confirmation:**
- "Import X new transactions" button
- Cancel option

### Success Page

- Success message with count
- Link to view imported transactions
- Option to import another file

## Acceptance Criteria

1. ✓ Upload page accessible at `/import` route
2. ✓ User can select account from dropdown
3. ✓ User can upload CSV file (max 10MB)
4. ✓ System parses CSV and extracts transactions
5. ✓ System validates all transactions (date, amount, description)
6. ✓ System detects duplicates accurately
7. ✓ User sees preview of transactions before import
8. ✓ User can confirm or cancel import
9. ✓ Transactions stored in database correctly
10. ✓ CSV file archived in YYYY/MM directory structure
11. ✓ Success message shows count of imported transactions
12. ✓ Existing data can be updated with new imports
13. ✓ Error messages are clear and helpful
14. ✓ All import operations are covered by tests

## Dependencies

**Upstream**: 
- PBI 1: Project Setup (Done) - Requires database and Flask app

**Downstream**: 
- PBI 4: Smart Categorization - Will use imported transactions
- PBI 5: Reports - Will display imported data

**External Dependencies**:
- pandas (already installed)
- Python dateutil (already installed)

## Open Questions

None at this time.

## Related Tasks

[View Task List](./tasks.md)

## History

| Timestamp | Event | From Status | To Status | Details | User |
|-----------|-------|-------------|-----------|---------|------|
| 2025-10-19 00:00:00 | Created | N/A | Proposed | Initial PBI created | Saeed |
| 2025-10-19 18:30:00 | Approved | Proposed | Agreed | PBI approved for implementation | Saeed |
| 2025-10-19 18:35:00 | Started | Agreed | InProgress | Beginning implementation | Saeed |

