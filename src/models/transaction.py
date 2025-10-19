"""
Transaction Model for database operations.
"""

import sqlite3
from typing import List, Dict, Optional
from datetime import date


class Transaction:
    """Model for managing transactions."""
    
    DB_PATH = 'data/financial_assistant.db'
    
    @staticmethod
    def _get_db_path():
        """Get database path from Flask config or use default."""
        try:
            from flask import current_app
            return current_app.config.get('DATABASE', Transaction.DB_PATH)
        except (ImportError, RuntimeError):
            return Transaction.DB_PATH
    
    @staticmethod
    def create(account_id: int, transaction_date: date, description: str, 
               amount: float, category_id: Optional[int] = None,
               notes: Optional[str] = None, tags: Optional[str] = None) -> int:
        """
        Create a new transaction.
        
        Args:
            account_id: Account ID
            transaction_date: Transaction date
            description: Transaction description
            amount: Transaction amount (negative for expenses)
            category_id: Optional category ID
            notes: Optional notes
            tags: Optional tags (comma-separated)
        
        Returns:
            Transaction ID
        """
        conn = sqlite3.connect(Transaction._get_db_path())
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO transactions 
            (account_id, date, description, amount, category_id, notes, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (account_id, transaction_date.isoformat(), description, amount, 
              category_id, notes, tags))
        
        transaction_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return transaction_id
    
    @staticmethod
    def bulk_create(transactions: List[Dict]) -> int:
        """
        Create multiple transactions efficiently.
        
        Args:
            transactions: List of transaction dictionaries with keys:
                         account_id, date, description, amount, 
                         category_id (optional), notes (optional), tags (optional)
        
        Returns:
            Number of transactions created
        """
        conn = sqlite3.connect(Transaction._get_db_path())
        cursor = conn.cursor()
        
        # Prepare data for bulk insert
        data = [
            (
                t['account_id'],
                t['date'].isoformat() if isinstance(t['date'], date) else t['date'],
                t['description'],
                t['amount'],
                t.get('category_id'),
                t.get('notes'),
                t.get('tags')
            )
            for t in transactions
        ]
        
        cursor.executemany("""
            INSERT INTO transactions 
            (account_id, date, description, amount, category_id, notes, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, data)
        
        count = cursor.rowcount
        conn.commit()
        conn.close()
        
        return count
    
    @staticmethod
    def get_by_id(transaction_id: int) -> Optional[Dict]:
        """Get transaction by ID."""
        conn = sqlite3.connect(Transaction._get_db_path())
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM transactions WHERE id = ?
        """, (transaction_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    @staticmethod
    def get_by_account(account_id: int, limit: Optional[int] = None) -> List[Dict]:
        """
        Get transactions for an account.
        
        Args:
            account_id: Account ID
            limit: Optional limit on number of transactions
        
        Returns:
            List of transaction dictionaries
        """
        conn = sqlite3.connect(Transaction._get_db_path())
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = """
            SELECT t.*, c.name as category_name, a.name as account_name
            FROM transactions t
            LEFT JOIN categories c ON t.category_id = c.id
            LEFT JOIN accounts a ON t.account_id = a.id
            WHERE t.account_id = ?
            ORDER BY t.date DESC, t.id DESC
        """
        
        if limit:
            query += f" LIMIT {limit}"
        
        cursor.execute(query, (account_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    @staticmethod
    def get_all(limit: Optional[int] = None) -> List[Dict]:
        """
        Get all transactions across all accounts.
        
        Args:
            limit: Optional limit on number of transactions
        
        Returns:
            List of transaction dictionaries
        """
        conn = sqlite3.connect(Transaction._get_db_path())
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = """
            SELECT t.*, c.name as category_name, a.name as account_name
            FROM transactions t
            LEFT JOIN categories c ON t.category_id = c.id
            LEFT JOIN accounts a ON t.account_id = a.id
            ORDER BY t.date DESC, t.id DESC
        """
        
        if limit:
            query += f" LIMIT {limit}"
        
        cursor.execute(query)
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    @staticmethod
    def delete(transaction_id: int) -> bool:
        """
        Delete a transaction.
        
        Returns:
            True if deleted, False if not found
        """
        conn = sqlite3.connect(Transaction._get_db_path())
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
        
        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return deleted
    
    @staticmethod
    def count_by_account(account_id: int) -> int:
        """Get transaction count for an account."""
        conn = sqlite3.connect(Transaction._get_db_path())
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT COUNT(*) FROM transactions WHERE account_id = ?
        """, (account_id,))
        
        count = cursor.fetchone()[0]
        conn.close()
        
        return count
    
    @staticmethod
    def get_filtered(account_id: Optional[int] = None, 
                    date_from: Optional[str] = None, 
                    date_to: Optional[str] = None,
                    limit: Optional[int] = None) -> List[Dict]:
        """
        Get transactions with optional filtering by account and date range.
        
        Args:
            account_id: Optional account ID to filter by
            date_from: Optional start date (YYYY-MM-DD)
            date_to: Optional end date (YYYY-MM-DD)
            limit: Optional limit on number of transactions
        
        Returns:
            List of transaction dictionaries
        """
        conn = sqlite3.connect(Transaction._get_db_path())
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Build query with filters
        query = """
            SELECT t.*, c.name as category_name, a.name as account_name
            FROM transactions t
            LEFT JOIN categories c ON t.category_id = c.id
            LEFT JOIN accounts a ON t.account_id = a.id
            WHERE 1=1
        """
        params = []
        
        if account_id:
            query += " AND t.account_id = ?"
            params.append(account_id)
        
        if date_from:
            query += " AND t.date >= ?"
            params.append(date_from)
        
        if date_to:
            query += " AND t.date <= ?"
            params.append(date_to)
        
        query += " ORDER BY t.date DESC, t.id DESC"
        
        if limit:
            query += f" LIMIT {limit}"
        
        cursor.execute(query, params)
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]

