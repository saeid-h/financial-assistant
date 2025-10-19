"""
Integration tests for import functionality.
"""

import pytest
import json
import os
from io import BytesIO


def test_import_page_loads(client):
    """Test that the import page loads successfully."""
    response = client.get('/import/')
    assert response.status_code == 200
    assert b'Import Transactions' in response.data


def test_upload_csv_no_file(client):
    """Test upload without file fails."""
    response = client.post('/import/upload')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data


def test_upload_csv_no_account(client, tmp_path):
    """Test upload without account selection fails."""
    # Create a test CSV file
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("Date,Description,Amount\n10/19/2025,Test,-100.00\n")
    
    with open(csv_file, 'rb') as f:
        data = {
            'file': (f, 'test.csv')
        }
        response = client.post('/import/upload', data=data, content_type='multipart/form-data')
    
    assert response.status_code == 400
    result = json.loads(response.data)
    assert 'error' in result


def test_upload_csv_invalid_extension(client, sample_account):
    """Test upload with non-CSV file fails."""
    data = {
        'file': (BytesIO(b'test content'), 'test.txt'),
        'account_id': sample_account
    }
    
    response = client.post('/import/upload', data=data, content_type='multipart/form-data')
    
    assert response.status_code == 400
    result = json.loads(response.data)
    assert 'CSV' in result['error']


def test_upload_csv_success(client, sample_account, tmp_path):
    """Test successful CSV upload and parsing."""
    from datetime import date, timedelta
    
    # Use past dates to avoid validation errors
    d1 = (date.today() - timedelta(days=5)).strftime('%m/%d/%Y')
    d2 = (date.today() - timedelta(days=4)).strftime('%m/%d/%Y')
    d3 = (date.today() - timedelta(days=3)).strftime('%m/%d/%Y')
    
    # Create a valid test CSV file
    csv_content = f"""Date,Description,Amount
{d1},Grocery Store,-45.50
{d2},Salary Deposit,2500.00
{d3},Rent Payment,-1200.00
"""
    csv_file = tmp_path / "transactions.csv"
    csv_file.write_text(csv_content)
    
    with open(csv_file, 'rb') as f:
        data = {
            'file': (f, 'transactions.csv'),
            'account_id': str(sample_account)
        }
        response = client.post('/import/upload', data=data, content_type='multipart/form-data')
    
    assert response.status_code == 200
    result = json.loads(response.data)
    
    # Debug: print result if test fails
    if not result.get('success'):
        print(f"Upload failed: {result}")
    elif result.get('valid_count', 0) != 3:
        print(f"Expected 3 valid, got {result.get('valid_count', 0)}")
        print(f"Invalid count: {result.get('invalid_count', 0)}")
        if result.get('invalid_transactions'):
            print(f"Invalid transactions: {result['invalid_transactions']}")
    
    assert result['success'] is True
    assert result['valid_count'] == 3
    assert result['invalid_count'] == 0
    assert result['total_credits'] == 2500.00  # Positive amounts (deposits/income)
    assert result['total_debits'] == 1245.50  # Negative amounts (withdrawals/expenses)


def test_upload_csv_with_validation_errors(client, sample_account, tmp_path):
    """Test CSV upload with invalid transactions."""
    from datetime import date, timedelta
    
    future_date = (date.today() + timedelta(days=10)).strftime('%m/%d/%Y')
    
    valid_date = (date.today() - timedelta(days=2)).strftime('%m/%d/%Y')
    
    csv_content = f"""Date,Description,Amount
{future_date},Future Transaction,100.00
{valid_date},,100.00
{valid_date},Valid Transaction,-50.00
"""
    csv_file = tmp_path / "bad_transactions.csv"
    csv_file.write_text(csv_content)
    
    with open(csv_file, 'rb') as f:
        data = {
            'file': (f, 'bad_transactions.csv'),
            'account_id': str(sample_account)
        }
        response = client.post('/import/upload', data=data, content_type='multipart/form-data')
    
    assert response.status_code == 200
    result = json.loads(response.data)
    
    assert result['success'] is True
    # Note: Empty description gets replaced with "Unknown Transaction" so it passes validation
    assert result['valid_count'] == 2  # Two valid (empty desc becomes "Unknown Transaction")
    assert result['invalid_count'] == 1  # One invalid (future date)


def test_confirm_import_no_pending(client):
    """Test confirm without pending transactions fails."""
    response = client.post('/import/confirm')
    assert response.status_code == 400
    result = json.loads(response.data)
    assert 'error' in result


def test_full_import_workflow(client, sample_account, tmp_path):
    """Test complete import workflow from upload to confirm."""
    from datetime import date, timedelta
    
    d1 = (date.today() - timedelta(days=5)).strftime('%m/%d/%Y')
    d2 = (date.today() - timedelta(days=4)).strftime('%m/%d/%Y')
    
    # Step 1: Upload CSV
    csv_content = f"""Date,Description,Amount
{d1},Grocery Store,-45.50
{d2},Salary Deposit,2500.00
"""
    csv_file = tmp_path / "full_workflow.csv"
    csv_file.write_text(csv_content)
    
    with client.session_transaction() as sess:
        # Ensure clean session
        sess.pop('pending_transactions', None)
    
    with open(csv_file, 'rb') as f:
        data = {
            'file': (f, 'full_workflow.csv'),
            'account_id': str(sample_account)
        }
        response = client.post('/import/upload', data=data, content_type='multipart/form-data')
    
    assert response.status_code == 200
    upload_result = json.loads(response.data)
    assert upload_result['success'] is True
    assert upload_result['valid_count'] == 2
    
    # Step 2: Confirm import
    response = client.post('/import/confirm')
    assert response.status_code == 200
    confirm_result = json.loads(response.data)
    
    assert confirm_result['success'] is True
    assert confirm_result['count'] == 2
    assert confirm_result['account_id'] == sample_account
    
    # Step 3: Verify transactions were saved
    import sqlite3
    from models.transaction import Transaction
    
    transactions = Transaction.get_by_account(sample_account)
    # Note: Tests share database, so we might have more than just these 2
    assert len(transactions) >= 2
    
    # Check transaction details
    descriptions = [t['description'] for t in transactions]
    assert 'Grocery Store' in descriptions
    assert 'Salary Deposit' in descriptions


def test_debit_credit_format(client, sample_account, tmp_path):
    """Test CSV with debit/credit columns."""
    from datetime import date, timedelta
    
    d1 = (date.today() - timedelta(days=5)).strftime('%m/%d/%Y')
    d2 = (date.today() - timedelta(days=4)).strftime('%m/%d/%Y')
    
    csv_content = f"""Date,Merchant,Debit,Credit
{d1},Grocery Store,45.50,
{d2},Salary Deposit,,2500.00
"""
    csv_file = tmp_path / "debit_credit.csv"
    csv_file.write_text(csv_content)
    
    with open(csv_file, 'rb') as f:
        data = {
            'file': (f, 'debit_credit.csv'),
            'account_id': str(sample_account)
        }
        response = client.post('/import/upload', data=data, content_type='multipart/form-data')
    
    assert response.status_code == 200
    result = json.loads(response.data)
    
    assert result['success'] is True
    assert result['valid_count'] == 2
    assert result['total_credits'] == 2500.00
    assert result['total_debits'] == 45.50

