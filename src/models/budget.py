"""
Budget Model
Handles CRUD operations for budgets
"""

import sqlite3
from typing import Optional, List, Dict
from datetime import date


class Budget:
    """Model for managing budgets"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    def _get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def create(self, category_id: int, amount: float, period_type: str,
               start_date: str, end_date: str, alert_threshold: int = 80) -> int:
        """Create a new budget"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO budgets 
            (category_id, amount, period_type, start_date, end_date, alert_threshold)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (category_id, amount, period_type, start_date, end_date, alert_threshold))
        
        budget_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return budget_id
    
    def get_by_id(self, budget_id: int) -> Optional[Dict]:
        """Get budget by ID"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT b.*, c.name as category_name
            FROM budgets b
            LEFT JOIN categories c ON b.category_id = c.id
            WHERE b.id = ?
        """, (budget_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    def get_all(self, period_type: Optional[str] = None) -> List[Dict]:
        """Get all budgets, optionally filtered by period type"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT b.*, c.name as category_name, c.type as category_type
            FROM budgets b
            LEFT JOIN categories c ON b.category_id = c.id
            WHERE 1=1
        """
        params = []
        
        if period_type:
            query += " AND b.period_type = ?"
            params.append(period_type)
        
        query += " ORDER BY c.name ASC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_current_budgets(self, period_type: str = 'monthly') -> List[Dict]:
        """Get budgets for the current period"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        today = date.today().isoformat()
        
        cursor.execute("""
            SELECT b.*, c.name as category_name, c.type as category_type
            FROM budgets b
            LEFT JOIN categories c ON b.category_id = c.id
            WHERE b.period_type = ?
            AND b.start_date <= ?
            AND b.end_date >= ?
            ORDER BY c.name ASC
        """, (period_type, today, today))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def update(self, budget_id: int, **kwargs) -> bool:
        """Update budget fields"""
        allowed_fields = ['amount', 'period_type', 'start_date', 'end_date', 'alert_threshold']
        updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
        
        if not updates:
            return False
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        set_clause = ', '.join(f"{k} = ?" for k in updates.keys())
        set_clause += ', updated_at = CURRENT_TIMESTAMP'
        values = list(updates.values()) + [budget_id]
        
        cursor.execute(f"""
            UPDATE budgets SET {set_clause}
            WHERE id = ?
        """, values)
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success
    
    def delete(self, budget_id: int) -> bool:
        """Delete a budget"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM budgets WHERE id = ?", (budget_id,))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return success

