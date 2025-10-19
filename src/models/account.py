"""
Account model for managing bank and credit card accounts.
"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Optional


class Account:
    """Model for bank/credit card accounts."""
    
    def __init__(self, db_path: str):
        """
        Initialize Account model.
        
        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path
    
    def create(self, name: str, account_type: str, institution: str = None, initial_balance: float = 0.0) -> int:
        """
        Create a new account.
        
        Args:
            name: Account name (e.g., "Chase Checking")
            account_type: Type of account (checking, savings, credit)
            institution: Financial institution name (optional)
            initial_balance: Starting balance (optional, default 0.00)
        
        Returns:
            ID of created account
        
        Raises:
            ValueError: If validation fails
        """
        # Validation
        if not name or not name.strip():
            raise ValueError("Account name is required")
        
        if account_type not in ['checking', 'savings', 'credit']:
            raise ValueError("Account type must be checking, savings, or credit")
        
        # Insert into database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO accounts (name, type, institution, initial_balance, current_balance, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name.strip(), account_type, institution, initial_balance, initial_balance, datetime.now(), datetime.now()))
            
            account_id = cursor.lastrowid
            conn.commit()
            return account_id
        
        finally:
            conn.close()
    
    def get_all(self) -> List[Dict]:
        """
        Get all accounts.
        
        Returns:
            List of account dictionaries
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT id, name, type, institution, initial_balance, current_balance, reference_date, created_at, updated_at
                FROM accounts
                ORDER BY created_at DESC
            """)
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        
        finally:
            conn.close()
    
    def get_by_id(self, account_id: int) -> Optional[Dict]:
        """
        Get account by ID.
        
        Args:
            account_id: Account ID
        
        Returns:
            Account dictionary or None if not found
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT id, name, type, institution, initial_balance, current_balance, reference_date, created_at, updated_at
                FROM accounts
                WHERE id = ?
            """, (account_id,))
            
            row = cursor.fetchone()
            return dict(row) if row else None
        
        finally:
            conn.close()
    
    def update(self, account_id: int, name: str = None, 
               account_type: str = None, institution: str = None, initial_balance: float = None,
               reference_date: str = None) -> bool:
        """
        Update an existing account.
        
        Args:
            account_id: Account ID
            name: New account name (optional)
            account_type: New account type (optional)
            institution: New institution (optional)
            initial_balance: New initial balance (optional)
            reference_date: Date when initial_balance was set (optional, YYYY-MM-DD)
        
        Returns:
            True if updated, False if not found
        
        Raises:
            ValueError: If validation fails
        """
        # Get existing account
        existing = self.get_by_id(account_id)
        if not existing:
            return False
        
        # Build update fields
        updates = []
        params = []
        
        if name is not None:
            if not name.strip():
                raise ValueError("Account name cannot be empty")
            updates.append("name = ?")
            params.append(name.strip())
        
        if account_type is not None:
            if account_type not in ['checking', 'savings', 'credit']:
                raise ValueError("Account type must be checking, savings, or credit")
            updates.append("type = ?")
            params.append(account_type)
        
        if institution is not None:
            updates.append("institution = ?")
            params.append(institution)
        
        if initial_balance is not None:
            updates.append("initial_balance = ?")
            params.append(initial_balance)
        
        if reference_date is not None:
            updates.append("reference_date = ?")
            params.append(reference_date)
        
        if not updates:
            return True  # Nothing to update
        
        updates.append("updated_at = ?")
        params.append(datetime.now())
        params.append(account_id)
        
        # Execute update
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute(f"""
                UPDATE accounts
                SET {', '.join(updates)}
                WHERE id = ?
            """, params)
            
            # If initial_balance was updated, recalculate current_balance
            if initial_balance is not None:
                # Get sum of all transactions for this account
                cursor.execute("""
                    SELECT COALESCE(SUM(amount), 0) 
                    FROM transactions 
                    WHERE account_id = ?
                """, (account_id,))
                
                transaction_sum = cursor.fetchone()[0]
                new_current_balance = initial_balance + transaction_sum
                
                # Update current_balance
                cursor.execute("""
                    UPDATE accounts 
                    SET current_balance = ? 
                    WHERE id = ?
                """, (new_current_balance, account_id))
            
            conn.commit()
            return cursor.rowcount > 0
        
        finally:
            conn.close()
    
    def delete(self, account_id: int) -> bool:
        """
        Delete an account.
        
        Args:
            account_id: Account ID
        
        Returns:
            True if deleted, False if not found
        
        Note:
            This will also delete all transactions associated with the account
            due to CASCADE foreign key constraint.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Enable foreign keys
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        try:
            cursor.execute("DELETE FROM accounts WHERE id = ?", (account_id,))
            conn.commit()
            return cursor.rowcount > 0
        
        finally:
            conn.close()
    
    def get_transaction_count(self, account_id: int) -> int:
        """
        Get count of transactions for an account.
        
        Args:
            account_id: Account ID
        
        Returns:
            Number of transactions
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT COUNT(*) FROM transactions
                WHERE account_id = ?
            """, (account_id,))
            
            return cursor.fetchone()[0]
        
        finally:
            conn.close()

