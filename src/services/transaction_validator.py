"""
Transaction Validation Service.

Validates transaction data for integrity before database storage.
"""

from datetime import date, datetime, timedelta
from typing import Dict, List, Tuple, Optional
import sqlite3


class ValidationError:
    """Represents a single validation error."""
    
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
    
    def to_dict(self) -> Dict:
        return {
            'field': self.field,
            'message': self.message
        }


class ValidationResult:
    """Represents the result of validation."""
    
    def __init__(self):
        self.errors: List[ValidationError] = []
    
    @property
    def is_valid(self) -> bool:
        """Check if validation passed (no errors)."""
        return len(self.errors) == 0
    
    def add_error(self, field: str, message: str):
        """Add a validation error."""
        self.errors.append(ValidationError(field, message))
    
    def to_dict(self) -> Dict:
        """Convert to dictionary format."""
        return {
            'valid': self.is_valid,
            'errors': [error.to_dict() for error in self.errors]
        }


class TransactionValidator:
    """
    Validates transaction data integrity.
    
    Configuration:
    - MAX_PAST_YEARS: How many years back transactions are allowed
    - MAX_AMOUNT: Maximum transaction amount (absolute value)
    - MAX_DESCRIPTION_LENGTH: Maximum description length
    """
    
    # Configuration constants
    MAX_PAST_YEARS = 10
    MAX_AMOUNT = 1_000_000.00  # $1 million
    MAX_DESCRIPTION_LENGTH = 500
    MIN_DESCRIPTION_LENGTH = 1
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize validator.
        
        Args:
            db_path: Path to database (for account validation)
        """
        self.db_path = db_path
    
    def validate_transaction(self, transaction: Dict) -> ValidationResult:
        """
        Validate a single transaction.
        
        Args:
            transaction: Transaction dictionary with keys: date, description, amount
                         Optional: account_id
        
        Returns:
            ValidationResult with any errors found
        """
        result = ValidationResult()
        
        # Validate date
        self._validate_date(transaction.get('date'), result)
        
        # Validate amount
        self._validate_amount(transaction.get('amount'), result)
        
        # Validate description
        self._validate_description(transaction.get('description'), result)
        
        # Validate account_id if provided
        if 'account_id' in transaction and transaction['account_id'] is not None:
            self._validate_account_id(transaction['account_id'], result)
        
        return result
    
    def validate_transactions(
        self, 
        transactions: List[Dict]
    ) -> List[Tuple[Dict, ValidationResult]]:
        """
        Validate multiple transactions.
        
        Args:
            transactions: List of transaction dictionaries
        
        Returns:
            List of (transaction, ValidationResult) tuples
        """
        return [
            (transaction, self.validate_transaction(transaction))
            for transaction in transactions
        ]
    
    def _validate_date(self, transaction_date, result: ValidationResult):
        """Validate transaction date."""
        # Check if date is provided
        if transaction_date is None:
            result.add_error('date', 'Date is required')
            return
        
        # Check if it's a date object
        if not isinstance(transaction_date, date):
            result.add_error('date', 'Date must be a date object')
            return
        
        # Check if date is not in the future
        today = date.today()
        if transaction_date > today:
            result.add_error('date', 'Date cannot be in the future')
        
        # Check if date is not too far in the past
        min_date = today - timedelta(days=self.MAX_PAST_YEARS * 365)
        if transaction_date < min_date:
            result.add_error(
                'date', 
                f'Date cannot be more than {self.MAX_PAST_YEARS} years in the past'
            )
    
    def _validate_amount(self, amount, result: ValidationResult):
        """Validate transaction amount."""
        # Check if amount is provided
        if amount is None:
            result.add_error('amount', 'Amount is required')
            return
        
        # Check if it's a number
        try:
            amount_float = float(amount)
        except (ValueError, TypeError):
            result.add_error('amount', 'Amount must be a valid number')
            return
        
        # Check if amount is non-zero
        if amount_float == 0:
            result.add_error('amount', 'Amount cannot be zero')
        
        # Check if amount is within reasonable range
        if abs(amount_float) > self.MAX_AMOUNT:
            result.add_error(
                'amount',
                f'Amount cannot exceed ${self.MAX_AMOUNT:,.2f}'
            )
    
    def _validate_description(self, description, result: ValidationResult):
        """Validate transaction description."""
        # Check if description is provided
        if description is None:
            result.add_error('description', 'Description is required')
            return
        
        # Convert to string and strip whitespace
        desc_str = str(description).strip()
        
        # Check if not empty
        if len(desc_str) < self.MIN_DESCRIPTION_LENGTH:
            result.add_error('description', 'Description cannot be empty')
            return
        
        # Check maximum length
        if len(desc_str) > self.MAX_DESCRIPTION_LENGTH:
            result.add_error(
                'description',
                f'Description cannot exceed {self.MAX_DESCRIPTION_LENGTH} characters'
            )
    
    def _validate_account_id(self, account_id, result: ValidationResult):
        """Validate account ID exists in database."""
        # Check if account_id is provided
        if account_id is None:
            return  # Optional field
        
        # Check if it's a valid integer
        try:
            account_id_int = int(account_id)
        except (ValueError, TypeError):
            result.add_error('account_id', 'Account ID must be a valid integer')
            return
        
        # Check if account exists in database (if db_path is provided)
        if self.db_path:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT id FROM accounts WHERE id = ?",
                    (account_id_int,)
                )
                row = cursor.fetchone()
                conn.close()
                
                if not row:
                    result.add_error(
                        'account_id',
                        f'Account with ID {account_id_int} does not exist'
                    )
            except sqlite3.Error as e:
                result.add_error('account_id', f'Database error: {str(e)}')

