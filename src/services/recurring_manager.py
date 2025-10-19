"""
Recurring Transaction Management Service

Provides CRUD operations, queries, and alert generation for recurring transactions.

Created: 2025-10-19
Author: Saeed Hoss
"""

import sqlite3
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional


class RecurringManager:
    """Service for managing recurring transactions and generating alerts."""
    
    def __init__(self, db_path: str):
        """
        Initialize the manager.
        
        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path
    
    # CRUD Operations
    
    def get_by_id(self, recurring_id: int) -> Optional[Dict]:
        """
        Get a recurring transaction by ID.
        
        Args:
            recurring_id: Recurring transaction ID
        
        Returns:
            Dictionary with recurring transaction data or None
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT r.*, c.name as category_name
                FROM recurring_transactions r
                LEFT JOIN categories c ON r.category_id = c.id
                WHERE r.id = ?
            """, (recurring_id,))
            
            row = cursor.fetchone()
            return dict(row) if row else None
            
        finally:
            conn.close()
    
    def get_all(self, status: Optional[str] = None) -> List[Dict]:
        """
        Get all recurring transactions, optionally filtered by status.
        
        Args:
            status: Optional status filter ('active', 'paused', 'cancelled')
        
        Returns:
            List of recurring transaction dictionaries
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            query = """
                SELECT r.*, c.name as category_name
                FROM recurring_transactions r
                LEFT JOIN categories c ON r.category_id = c.id
            """
            params = []
            
            if status:
                query += " WHERE r.status = ?"
                params.append(status)
            
            query += " ORDER BY r.next_expected_date ASC, r.merchant_name ASC"
            
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
            
        finally:
            conn.close()
    
    def get_active(self) -> List[Dict]:
        """
        Get all active recurring transactions.
        
        Returns:
            List of active recurring transactions
        """
        return self.get_all(status='active')
    
    def create(self, pattern_data: Dict) -> int:
        """
        Create a new recurring transaction.
        
        Args:
            pattern_data: Dictionary with recurring transaction fields
        
        Returns:
            ID of created recurring transaction
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO recurring_transactions (
                    merchant_name, description_pattern, frequency,
                    average_amount, amount_variance, category_id,
                    last_transaction_date, next_expected_date,
                    status, alert_if_missing, alert_if_amount_changes,
                    confidence_score, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                pattern_data['merchant_name'],
                pattern_data.get('description_pattern', pattern_data['merchant_name']),
                pattern_data['frequency'],
                pattern_data['average_amount'],
                pattern_data.get('amount_variance', 0.0),
                pattern_data.get('category_id'),
                pattern_data.get('last_transaction_date'),
                pattern_data.get('next_expected_date'),
                pattern_data.get('status', 'active'),
                pattern_data.get('alert_if_missing', 1),
                pattern_data.get('alert_if_amount_changes', 1),
                pattern_data.get('confidence_score', 0.85),
                datetime.now(),
                datetime.now()
            ))
            
            recurring_id = cursor.lastrowid
            conn.commit()
            return recurring_id
            
        finally:
            conn.close()
    
    def update(self, recurring_id: int, updates: Dict) -> bool:
        """
        Update a recurring transaction.
        
        Args:
            recurring_id: Recurring transaction ID
            updates: Dictionary of fields to update
        
        Returns:
            True if updated, False if not found
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Build UPDATE query dynamically
            update_fields = []
            params = []
            
            for field in ['merchant_name', 'description_pattern', 'frequency', 'average_amount',
                         'amount_variance', 'category_id', 'alert_if_missing', 'alert_if_amount_changes']:
                if field in updates:
                    update_fields.append(f"{field} = ?")
                    params.append(updates[field])
            
            if not update_fields:
                return True  # Nothing to update
            
            update_fields.append("updated_at = ?")
            params.append(datetime.now())
            params.append(recurring_id)
            
            cursor.execute(f"""
                UPDATE recurring_transactions
                SET {', '.join(update_fields)}
                WHERE id = ?
            """, params)
            
            conn.commit()
            return cursor.rowcount > 0
            
        finally:
            conn.close()
    
    def delete(self, recurring_id: int) -> bool:
        """
        Delete a recurring transaction (and all its instances via CASCADE).
        
        Args:
            recurring_id: Recurring transaction ID
        
        Returns:
            True if deleted, False if not found
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM recurring_transactions WHERE id = ?", (recurring_id,))
            conn.commit()
            return cursor.rowcount > 0
            
        finally:
            conn.close()
    
    def pause(self, recurring_id: int) -> bool:
        """Pause a recurring transaction (stop tracking)."""
        return self.update(recurring_id, {'status': 'paused'})
    
    def resume(self, recurring_id: int) -> bool:
        """Resume a paused recurring transaction."""
        return self.update(recurring_id, {'status': 'active'})
    
    # Query Methods
    
    def get_upcoming(self, days: int = 30) -> List[Dict]:
        """
        Get recurring transactions expected in the next N days.
        
        Args:
            days: Number of days to look ahead
        
        Returns:
            List of upcoming recurring transactions
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            end_date = (date.today() + timedelta(days=days)).strftime('%Y-%m-%d')
            
            cursor.execute("""
                SELECT r.*, c.name as category_name
                FROM recurring_transactions r
                LEFT JOIN categories c ON r.category_id = c.id
                WHERE r.status = 'active'
                  AND r.next_expected_date <= ?
                ORDER BY r.next_expected_date ASC
            """, (end_date,))
            
            return [dict(row) for row in cursor.fetchall()]
            
        finally:
            conn.close()
    
    def get_by_category(self, category_id: int) -> List[Dict]:
        """
        Get recurring transactions for a specific category.
        
        Args:
            category_id: Category ID
        
        Returns:
            List of recurring transactions
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT r.*, c.name as category_name
                FROM recurring_transactions r
                LEFT JOIN categories c ON r.category_id = c.id
                WHERE r.category_id = ?
                  AND r.status = 'active'
                ORDER BY r.average_amount DESC
            """, (category_id,))
            
            return [dict(row) for row in cursor.fetchall()]
            
        finally:
            conn.close()
    
    def get_monthly_total(self) -> float:
        """
        Calculate total monthly recurring expenses.
        
        Returns:
            Sum of all monthly recurring transaction amounts
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT SUM(average_amount) as total
                FROM recurring_transactions
                WHERE status = 'active'
                  AND frequency = 'monthly'
            """)
            
            result = cursor.fetchone()
            return result[0] if result[0] else 0.0
            
        finally:
            conn.close()
    
    # Alert Generation
    
    def get_missing_payments(self, days_overdue: int = 3) -> List[Dict]:
        """
        Find recurring payments that are overdue.
        
        Args:
            days_overdue: Number of days past expected date to consider missing
        
        Returns:
            List of missing payment alerts
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cutoff_date = (date.today() - timedelta(days=days_overdue)).strftime('%Y-%m-%d')
            
            cursor.execute("""
                SELECT r.*, c.name as category_name
                FROM recurring_transactions r
                LEFT JOIN categories c ON r.category_id = c.id
                WHERE r.status = 'active'
                  AND r.alert_if_missing = 1
                  AND r.next_expected_date <= ?
                ORDER BY r.next_expected_date ASC
            """, (cutoff_date,))
            
            alerts = []
            for row in cursor.fetchall():
                rec = dict(row)
                expected_date = datetime.strptime(rec['next_expected_date'], '%Y-%m-%d').date()
                days_late = (date.today() - expected_date).days
                
                alerts.append({
                    **rec,
                    'alert_type': 'missing_payment',
                    'days_late': days_late,
                    'severity': 'high' if days_late > 7 else 'medium'
                })
            
            return alerts
            
        finally:
            conn.close()
    
    def get_amount_changes(self, variance_threshold: float = 0.10) -> List[Dict]:
        """
        Find recurring transactions with recent amount changes.
        
        Args:
            variance_threshold: Minimum variance to trigger alert (0.10 = 10%)
        
        Returns:
            List of amount change alerts
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            # Get recurring transactions with recent instances
            cursor.execute("""
                SELECT r.*, c.name as category_name,
                       i.actual_amount, i.actual_date,
                       ABS(i.actual_amount - r.average_amount) as variance
                FROM recurring_transactions r
                LEFT JOIN categories c ON r.category_id = c.id
                LEFT JOIN recurring_transaction_instances i ON r.id = i.recurring_id
                WHERE r.status = 'active'
                  AND r.alert_if_amount_changes = 1
                  AND i.actual_date = r.last_transaction_date
                ORDER BY i.actual_date DESC
            """)
            
            alerts = []
            for row in cursor.fetchall():
                rec = dict(row)
                variance_pct = rec['variance'] / rec['average_amount'] if rec['average_amount'] > 0 else 0
                
                if variance_pct > variance_threshold:
                    alerts.append({
                        **rec,
                        'alert_type': 'amount_changed',
                        'variance_percent': round(variance_pct * 100, 1),
                        'old_amount': rec['average_amount'],
                        'new_amount': rec['actual_amount'],
                        'difference': round(rec['variance'], 2),
                        'severity': 'high' if variance_pct > 0.25 else 'medium'
                    })
            
            return alerts
            
        finally:
            conn.close()
    
    def get_all_alerts(self) -> Dict[str, List[Dict]]:
        """
        Get all alerts (missing payments and amount changes).
        
        Returns:
            Dictionary with 'missing' and 'changed' alert lists
        """
        return {
            'missing': self.get_missing_payments(),
            'changed': self.get_amount_changes(),
            'total_count': len(self.get_missing_payments()) + len(self.get_amount_changes())
        }
    
    # Instance Management
    
    def add_instance(self, recurring_id: int, transaction_id: int, 
                     expected_date: str, actual_date: str,
                     expected_amount: float, actual_amount: float,
                     status: str = 'on_time') -> int:
        """
        Add an instance linking a transaction to a recurring pattern.
        
        Args:
            recurring_id: Parent recurring transaction ID
            transaction_id: Actual transaction ID
            expected_date: When it was expected (YYYY-MM-DD)
            actual_date: When it actually occurred (YYYY-MM-DD)
            expected_amount: Expected amount
            actual_amount: Actual amount
            status: Instance status
        
        Returns:
            Instance ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            variance = abs(actual_amount - expected_amount)
            
            cursor.execute("""
                INSERT INTO recurring_transaction_instances (
                    recurring_id, transaction_id, expected_date, actual_date,
                    expected_amount, actual_amount, variance_amount,
                    status, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                recurring_id, transaction_id, expected_date, actual_date,
                expected_amount, actual_amount, variance,
                status, datetime.now()
            ))
            
            instance_id = cursor.lastrowid
            
            # Update parent recurring transaction
            cursor.execute("""
                UPDATE recurring_transactions
                SET last_transaction_date = ?,
                    next_expected_date = ?,
                    updated_at = ?
                WHERE id = ?
            """, (
                actual_date,
                self._calculate_next_date(actual_date, recurring_id),
                datetime.now(),
                recurring_id
            ))
            
            conn.commit()
            return instance_id
            
        finally:
            conn.close()
    
    def get_instances(self, recurring_id: int, limit: int = 10) -> List[Dict]:
        """
        Get instances for a recurring transaction.
        
        Args:
            recurring_id: Recurring transaction ID
            limit: Maximum number of instances to return
        
        Returns:
            List of instance dictionaries
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT i.*, t.description
                FROM recurring_transaction_instances i
                LEFT JOIN transactions t ON i.transaction_id = t.id
                WHERE i.recurring_id = ?
                ORDER BY i.actual_date DESC
                LIMIT ?
            """, (recurring_id, limit))
            
            return [dict(row) for row in cursor.fetchall()]
            
        finally:
            conn.close()
    
    def update_instance_status(self, instance_id: int, status: str) -> bool:
        """
        Update the status of an instance.
        
        Args:
            instance_id: Instance ID
            status: New status ('on_time', 'late', 'missed', 'amount_changed')
        
        Returns:
            True if updated, False if not found
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE recurring_transaction_instances
                SET status = ?
                WHERE id = ?
            """, (status, instance_id))
            
            conn.commit()
            return cursor.rowcount > 0
            
        finally:
            conn.close()
    
    # Helper Methods
    
    def _calculate_next_date(self, last_date: str, recurring_id: int) -> str:
        """
        Calculate next expected date based on frequency.
        
        Args:
            last_date: Last transaction date (YYYY-MM-DD)
            recurring_id: Recurring transaction ID
        
        Returns:
            Next expected date (YYYY-MM-DD)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT frequency FROM recurring_transactions WHERE id = ?", (recurring_id,))
            result = cursor.fetchone()
            
            if not result:
                return last_date
            
            frequency = result[0]
            last_dt = datetime.strptime(last_date, '%Y-%m-%d').date()
            
            # Calculate next date based on frequency
            frequency_days = {
                'weekly': 7,
                'biweekly': 14,
                'monthly': 30,
                'quarterly': 90,
                'annual': 365
            }
            
            days_to_add = frequency_days.get(frequency, 30)
            next_date = last_dt + timedelta(days=days_to_add)
            
            return next_date.strftime('%Y-%m-%d')
            
        finally:
            conn.close()
    
    def get_statistics(self) -> Dict:
        """
        Get statistics about recurring transactions.
        
        Returns:
            Dictionary with counts and totals
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Count by status
            cursor.execute("""
                SELECT status, COUNT(*) as count
                FROM recurring_transactions
                GROUP BY status
            """)
            
            status_counts = {row[0]: row[1] for row in cursor.fetchall()}
            
            # Calculate monthly recurring total
            monthly_total = self.get_monthly_total()
            
            # Count upcoming (next 7 days)
            upcoming = self.get_upcoming(days=7)
            
            # Get alerts
            alerts = self.get_all_alerts()
            
            return {
                'active_count': status_counts.get('active', 0),
                'paused_count': status_counts.get('paused', 0),
                'total_count': sum(status_counts.values()),
                'monthly_total': round(monthly_total, 2),
                'upcoming_count': len(upcoming),
                'alert_count': alerts['total_count']
            }
            
        finally:
            conn.close()

