"""
Unit tests for Transaction Validator Service.
"""

import pytest
from datetime import date, timedelta
from src.services.transaction_validator import (
    TransactionValidator, 
    ValidationResult,
    ValidationError
)


class TestTransactionValidator:
    """Test cases for Transaction Validator."""
    
    @pytest.fixture
    def validator(self):
        """Create a validator instance."""
        return TransactionValidator()
    
    @pytest.fixture
    def validator_with_db(self, app):
        """Create a validator with database access."""
        return TransactionValidator(db_path=app.config['DATABASE'])
    
    @pytest.fixture
    def valid_transaction(self):
        """Create a valid transaction."""
        return {
            'date': date.today(),
            'description': 'Test Transaction',
            'amount': 100.00
        }
    
    def test_valid_transaction(self, validator, valid_transaction):
        """Test validation of a valid transaction."""
        result = validator.validate_transaction(valid_transaction)
        
        assert result.is_valid
        assert len(result.errors) == 0
    
    def test_validation_result_to_dict(self, validator, valid_transaction):
        """Test ValidationResult to_dict conversion."""
        result = validator.validate_transaction(valid_transaction)
        result_dict = result.to_dict()
        
        assert result_dict['valid'] is True
        assert result_dict['errors'] == []
    
    # Date Validation Tests
    
    def test_missing_date(self, validator):
        """Test validation fails when date is missing."""
        transaction = {
            'description': 'Test',
            'amount': 100.00
        }
        
        result = validator.validate_transaction(transaction)
        
        assert not result.is_valid
        assert any(error.field == 'date' for error in result.errors)
        assert any('required' in error.message.lower() for error in result.errors)
    
    def test_invalid_date_future(self, validator):
        """Test validation fails for future dates."""
        transaction = {
            'date': date.today() + timedelta(days=1),
            'description': 'Test',
            'amount': 100.00
        }
        
        result = validator.validate_transaction(transaction)
        
        assert not result.is_valid
        assert any(error.field == 'date' for error in result.errors)
        assert any('future' in error.message.lower() for error in result.errors)
    
    def test_invalid_date_too_old(self, validator):
        """Test validation fails for dates too far in the past."""
        transaction = {
            'date': date.today() - timedelta(days=11*365),  # 11 years ago
            'description': 'Test',
            'amount': 100.00
        }
        
        result = validator.validate_transaction(transaction)
        
        assert not result.is_valid
        assert any(error.field == 'date' for error in result.errors)
        assert any('past' in error.message.lower() for error in result.errors)
    
    def test_invalid_date_not_date_object(self, validator):
        """Test validation fails when date is not a date object."""
        transaction = {
            'date': '2025-10-19',  # String, not date object
            'description': 'Test',
            'amount': 100.00
        }
        
        result = validator.validate_transaction(transaction)
        
        assert not result.is_valid
        assert any(error.field == 'date' for error in result.errors)
        assert any('date object' in error.message.lower() for error in result.errors)
    
    # Amount Validation Tests
    
    def test_missing_amount(self, validator):
        """Test validation fails when amount is missing."""
        transaction = {
            'date': date.today(),
            'description': 'Test'
        }
        
        result = validator.validate_transaction(transaction)
        
        assert not result.is_valid
        assert any(error.field == 'amount' for error in result.errors)
        assert any('required' in error.message.lower() for error in result.errors)
    
    def test_invalid_amount_zero(self, validator):
        """Test validation fails for zero amount."""
        transaction = {
            'date': date.today(),
            'description': 'Test',
            'amount': 0
        }
        
        result = validator.validate_transaction(transaction)
        
        assert not result.is_valid
        assert any(error.field == 'amount' for error in result.errors)
        assert any('zero' in error.message.lower() for error in result.errors)
    
    def test_invalid_amount_too_large(self, validator):
        """Test validation fails for amounts exceeding max."""
        transaction = {
            'date': date.today(),
            'description': 'Test',
            'amount': 2_000_000.00  # Exceeds $1M limit
        }
        
        result = validator.validate_transaction(transaction)
        
        assert not result.is_valid
        assert any(error.field == 'amount' for error in result.errors)
        assert any('exceed' in error.message.lower() for error in result.errors)
    
    def test_invalid_amount_too_negative(self, validator):
        """Test validation fails for very negative amounts."""
        transaction = {
            'date': date.today(),
            'description': 'Test',
            'amount': -2_000_000.00  # Exceeds -$1M limit
        }
        
        result = validator.validate_transaction(transaction)
        
        assert not result.is_valid
        assert any(error.field == 'amount' for error in result.errors)
        assert any('exceed' in error.message.lower() for error in result.errors)
    
    def test_invalid_amount_not_number(self, validator):
        """Test validation fails for non-numeric amounts."""
        transaction = {
            'date': date.today(),
            'description': 'Test',
            'amount': 'not a number'
        }
        
        result = validator.validate_transaction(transaction)
        
        assert not result.is_valid
        assert any(error.field == 'amount' for error in result.errors)
        assert any('number' in error.message.lower() for error in result.errors)
    
    def test_valid_negative_amount(self, validator):
        """Test validation passes for valid negative amounts."""
        transaction = {
            'date': date.today(),
            'description': 'Test',
            'amount': -100.00
        }
        
        result = validator.validate_transaction(transaction)
        
        assert result.is_valid
    
    def test_valid_positive_amount(self, validator):
        """Test validation passes for valid positive amounts."""
        transaction = {
            'date': date.today(),
            'description': 'Test',
            'amount': 100.00
        }
        
        result = validator.validate_transaction(transaction)
        
        assert result.is_valid
    
    # Description Validation Tests
    
    def test_missing_description(self, validator):
        """Test validation fails when description is missing."""
        transaction = {
            'date': date.today(),
            'amount': 100.00
        }
        
        result = validator.validate_transaction(transaction)
        
        assert not result.is_valid
        assert any(error.field == 'description' for error in result.errors)
        assert any('required' in error.message.lower() for error in result.errors)
    
    def test_invalid_description_empty(self, validator):
        """Test validation fails for empty description."""
        transaction = {
            'date': date.today(),
            'description': '',
            'amount': 100.00
        }
        
        result = validator.validate_transaction(transaction)
        
        assert not result.is_valid
        assert any(error.field == 'description' for error in result.errors)
        assert any('empty' in error.message.lower() for error in result.errors)
    
    def test_invalid_description_whitespace_only(self, validator):
        """Test validation fails for whitespace-only description."""
        transaction = {
            'date': date.today(),
            'description': '   \t\n  ',
            'amount': 100.00
        }
        
        result = validator.validate_transaction(transaction)
        
        assert not result.is_valid
        assert any(error.field == 'description' for error in result.errors)
        assert any('empty' in error.message.lower() for error in result.errors)
    
    def test_invalid_description_too_long(self, validator):
        """Test validation fails for overly long descriptions."""
        transaction = {
            'date': date.today(),
            'description': 'A' * 501,  # Exceeds 500 char limit
            'amount': 100.00
        }
        
        result = validator.validate_transaction(transaction)
        
        assert not result.is_valid
        assert any(error.field == 'description' for error in result.errors)
        assert any('exceed' in error.message.lower() for error in result.errors)
    
    def test_valid_description_with_whitespace(self, validator):
        """Test validation passes for description with leading/trailing whitespace."""
        transaction = {
            'date': date.today(),
            'description': '  Valid Description  ',
            'amount': 100.00
        }
        
        result = validator.validate_transaction(transaction)
        
        assert result.is_valid
    
    # Multiple Errors Tests
    
    def test_multiple_errors_collected(self, validator):
        """Test that multiple validation errors are collected."""
        transaction = {
            'date': date.today() + timedelta(days=1),  # Invalid: future
            'description': '',  # Invalid: empty
            'amount': 0  # Invalid: zero
        }
        
        result = validator.validate_transaction(transaction)
        
        assert not result.is_valid
        assert len(result.errors) == 3
        
        # Check all three error types are present
        error_fields = {error.field for error in result.errors}
        assert 'date' in error_fields
        assert 'description' in error_fields
        assert 'amount' in error_fields
    
    # Bulk Validation Tests
    
    def test_bulk_validation(self, validator):
        """Test validation of multiple transactions."""
        transactions = [
            {
                'date': date.today(),
                'description': 'Valid Transaction 1',
                'amount': 100.00
            },
            {
                'date': date.today() + timedelta(days=1),  # Invalid
                'description': 'Invalid Transaction',
                'amount': 50.00
            },
            {
                'date': date.today(),
                'description': 'Valid Transaction 2',
                'amount': -75.00
            }
        ]
        
        results = validator.validate_transactions(transactions)
        
        assert len(results) == 3
        assert results[0][1].is_valid  # First transaction valid
        assert not results[1][1].is_valid  # Second transaction invalid
        assert results[2][1].is_valid  # Third transaction valid
    
    def test_bulk_validation_returns_tuples(self, validator):
        """Test bulk validation returns transaction-result tuples."""
        transactions = [
            {
                'date': date.today(),
                'description': 'Test',
                'amount': 100.00
            }
        ]
        
        results = validator.validate_transactions(transactions)
        
        assert len(results) == 1
        transaction, result = results[0]
        assert transaction == transactions[0]
        assert isinstance(result, ValidationResult)
    
    # Account ID Validation Tests
    
    def test_account_id_optional(self, validator):
        """Test that account_id is optional."""
        transaction = {
            'date': date.today(),
            'description': 'Test',
            'amount': 100.00
            # No account_id
        }
        
        result = validator.validate_transaction(transaction)
        
        assert result.is_valid
    
    def test_invalid_account_id_not_integer(self, validator):
        """Test validation fails for non-integer account_id."""
        transaction = {
            'date': date.today(),
            'description': 'Test',
            'amount': 100.00,
            'account_id': 'not_an_integer'
        }
        
        result = validator.validate_transaction(transaction)
        
        assert not result.is_valid
        assert any(error.field == 'account_id' for error in result.errors)
        assert any('integer' in error.message.lower() for error in result.errors)
    
    def test_account_id_exists(self, validator_with_db, app):
        """Test validation passes when account exists."""
        # Create an account
        import sqlite3
        conn = sqlite3.connect(app.config['DATABASE'])
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO accounts (name, type) VALUES (?, ?)",
            ("Test Account", "checking")
        )
        account_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        transaction = {
            'date': date.today(),
            'description': 'Test',
            'amount': 100.00,
            'account_id': account_id
        }
        
        result = validator_with_db.validate_transaction(transaction)
        
        assert result.is_valid
    
    def test_account_id_not_exists(self, validator_with_db):
        """Test validation fails when account doesn't exist."""
        transaction = {
            'date': date.today(),
            'description': 'Test',
            'amount': 100.00,
            'account_id': 99999  # Non-existent account
        }
        
        result = validator_with_db.validate_transaction(transaction)
        
        assert not result.is_valid
        assert any(error.field == 'account_id' for error in result.errors)
        assert any('does not exist' in error.message.lower() for error in result.errors)

