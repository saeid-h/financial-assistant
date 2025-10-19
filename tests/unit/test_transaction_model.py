"""
Unit tests for Transaction Model.
"""

import pytest
from datetime import date, timedelta
from models.transaction import Transaction


class TestTransactionModel:
    """Test cases for Transaction model."""
    
    def test_create_transaction(self, app, sample_account):
        """Test creating a transaction."""
        transaction_date = date.today()
        transaction_id = Transaction.create(
            account_id=sample_account,
            transaction_date=transaction_date,
            description="Test Transaction",
            amount=-100.00
        )
        
        assert transaction_id is not None
        assert transaction_id > 0
        
        # Verify it was created
        txn = Transaction.get_by_id(transaction_id)
        assert txn is not None
        assert txn['description'] == "Test Transaction"
        assert txn['amount'] == -100.00
    
    def test_create_transaction_with_category(self, app, sample_account, sample_category):
        """Test creating a transaction with a category."""
        transaction_id = Transaction.create(
            account_id=sample_account,
            transaction_date=date.today(),
            description="Categorized Transaction",
            amount=-50.00,
            category_id=sample_category
        )
        
        txn = Transaction.get_by_id(transaction_id)
        assert txn['category_id'] == sample_category
    
    def test_create_transaction_with_notes_and_tags(self, app, sample_account):
        """Test creating a transaction with notes and tags."""
        transaction_id = Transaction.create(
            account_id=sample_account,
            transaction_date=date.today(),
            description="Transaction with metadata",
            amount=-75.00,
            notes="This is a test note",
            tags="personal,grocery"
        )
        
        txn = Transaction.get_by_id(transaction_id)
        assert txn['notes'] == "This is a test note"
        assert txn['tags'] == "personal,grocery"
    
    def test_bulk_create_transactions(self, app, sample_account):
        """Test bulk creating transactions."""
        transactions = [
            {
                'account_id': sample_account,
                'date': date.today(),
                'description': 'Transaction 1',
                'amount': -100.00
            },
            {
                'account_id': sample_account,
                'date': date.today() - timedelta(days=1),
                'description': 'Transaction 2',
                'amount': -200.00
            },
            {
                'account_id': sample_account,
                'date': date.today() - timedelta(days=2),
                'description': 'Transaction 3',
                'amount': 500.00
            }
        ]
        
        count = Transaction.bulk_create(transactions)
        
        assert count == 3
        
        # Verify they were created
        txns = Transaction.get_by_account(sample_account)
        assert len(txns) >= 3
    
    def test_get_by_id_not_found(self, app):
        """Test getting a non-existent transaction."""
        txn = Transaction.get_by_id(99999)
        assert txn is None
    
    def test_get_by_account(self, app, sample_account):
        """Test getting transactions by account."""
        # Create some transactions
        Transaction.create(
            account_id=sample_account,
            transaction_date=date.today(),
            description="Transaction 1",
            amount=-100.00
        )
        Transaction.create(
            account_id=sample_account,
            transaction_date=date.today(),
            description="Transaction 2",
            amount=-200.00
        )
        
        txns = Transaction.get_by_account(sample_account)
        
        assert len(txns) >= 2
        assert all(txn['account_id'] == sample_account for txn in txns)
    
    def test_get_by_account_with_limit(self, app, sample_account):
        """Test getting transactions with limit."""
        # Create multiple transactions
        for i in range(5):
            Transaction.create(
                account_id=sample_account,
                transaction_date=date.today(),
                description=f"Transaction {i}",
                amount=-10.00 * (i + 1)
            )
        
        txns = Transaction.get_by_account(sample_account, limit=3)
        
        assert len(txns) <= 3
    
    def test_get_all_transactions(self, app, sample_account):
        """Test getting all transactions."""
        # Create some transactions
        Transaction.create(
            account_id=sample_account,
            transaction_date=date.today(),
            description="Transaction A",
            amount=-100.00
        )
        
        txns = Transaction.get_all()
        
        assert len(txns) >= 1
        assert any(txn['description'] == "Transaction A" for txn in txns)
    
    def test_get_all_with_limit(self, app, sample_account):
        """Test getting all transactions with limit."""
        # Create multiple transactions
        for i in range(5):
            Transaction.create(
                account_id=sample_account,
                transaction_date=date.today(),
                description=f"Transaction {i}",
                amount=-10.00
            )
        
        txns = Transaction.get_all(limit=2)
        
        assert len(txns) <= 2
    
    def test_delete_transaction(self, app, sample_account):
        """Test deleting a transaction."""
        # Create a transaction
        transaction_id = Transaction.create(
            account_id=sample_account,
            transaction_date=date.today(),
            description="To be deleted",
            amount=-100.00
        )
        
        # Delete it
        result = Transaction.delete(transaction_id)
        assert result is True
        
        # Verify it's gone
        txn = Transaction.get_by_id(transaction_id)
        assert txn is None
    
    def test_delete_transaction_not_found(self, app):
        """Test deleting a non-existent transaction."""
        result = Transaction.delete(99999)
        assert result is False
    
    def test_count_by_account(self, app, sample_account):
        """Test counting transactions by account."""
        # Get initial count
        initial_count = Transaction.count_by_account(sample_account)
        
        # Create some transactions
        for i in range(3):
            Transaction.create(
                account_id=sample_account,
                transaction_date=date.today(),
                description=f"Transaction {i}",
                amount=-10.00
            )
        
        # Check new count
        new_count = Transaction.count_by_account(sample_account)
        assert new_count == initial_count + 3
    
    def test_transactions_include_account_name(self, app, sample_account):
        """Test that transactions include account name from join."""
        Transaction.create(
            account_id=sample_account,
            transaction_date=date.today(),
            description="Test Join",
            amount=-100.00
        )
        
        txns = Transaction.get_by_account(sample_account)
        
        assert len(txns) >= 1
        assert 'account_name' in txns[0]
        assert txns[0]['account_name'] is not None

