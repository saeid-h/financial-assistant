"""
Budget Service
Calculates budget progress, alerts, and analysis
"""

import sqlite3
from typing import List, Dict, Any
from datetime import date


class BudgetService:
    """Service for budget calculations and progress tracking"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    def _get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def get_budget_progress(self, budget_id: int) -> Dict[str, Any]:
        """
        Calculate progress for a specific budget.
        
        Returns: {
            "budget_id": 1,
            "category_name": "Groceries",
            "budgeted": 800.00,
            "actual": 654.32,
            "remaining": 145.68,
            "percentage": 81.79,
            "status": "warning",  # "good", "warning", "over"
            "alert": False
        }
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Get budget details
        cursor.execute("""
            SELECT b.*, c.name as category_name
            FROM budgets b
            LEFT JOIN categories c ON b.category_id = c.id
            WHERE b.id = ?
        """, (budget_id,))
        
        budget = cursor.fetchone()
        if not budget:
            conn.close()
            return None
        
        # Calculate actual spending
        cursor.execute("""
            SELECT SUM(ABS(amount)) as total
            FROM transactions
            WHERE category_id = ?
            AND amount < 0
            AND date >= ?
            AND date <= ?
        """, (budget['category_id'], budget['start_date'], budget['end_date']))
        
        result = cursor.fetchone()
        actual = float(result['total']) if result['total'] else 0.0
        
        conn.close()
        
        budgeted = float(budget['amount'])
        remaining = budgeted - actual
        percentage = (actual / budgeted * 100) if budgeted > 0 else 0.0
        
        # Determine status
        if percentage >= 100:
            status = 'over'
        elif percentage >= budget['alert_threshold']:
            status = 'warning'
        else:
            status = 'good'
        
        return {
            'budget_id': budget['id'],
            'category_id': budget['category_id'],
            'category_name': budget['category_name'],
            'budgeted': round(budgeted, 2),
            'actual': round(actual, 2),
            'remaining': round(remaining, 2),
            'percentage': round(percentage, 1),
            'status': status,
            'alert': percentage >= budget['alert_threshold'],
            'period_type': budget['period_type'],
            'start_date': budget['start_date'],
            'end_date': budget['end_date']
        }
    
    def get_all_budgets_progress(self, period_type: str = 'monthly') -> List[Dict[str, Any]]:
        """Get progress for all budgets"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Get all budgets for the current period
        today = date.today().isoformat()
        
        cursor.execute("""
            SELECT id FROM budgets
            WHERE period_type = ?
            AND start_date <= ?
            AND end_date >= ?
            ORDER BY id ASC
        """, (period_type, today, today))
        
        budget_ids = [row['id'] for row in cursor.fetchall()]
        conn.close()
        
        # Calculate progress for each
        progress_list = []
        for budget_id in budget_ids:
            progress = self.get_budget_progress(budget_id)
            if progress:
                progress_list.append(progress)
        
        return progress_list
    
    def get_budget_summary(self) -> Dict[str, Any]:
        """
        Get overall budget summary.
        
        Returns: {
            "total_budgeted": 5000.00,
            "total_actual": 3245.67,
            "total_remaining": 1754.33,
            "budgets_count": 5,
            "over_budget_count": 1,
            "at_risk_count": 2
        }
        """
        progress_list = self.get_all_budgets_progress()
        
        total_budgeted = sum(p['budgeted'] for p in progress_list)
        total_actual = sum(p['actual'] for p in progress_list)
        total_remaining = total_budgeted - total_actual
        over_budget_count = sum(1 for p in progress_list if p['status'] == 'over')
        at_risk_count = sum(1 for p in progress_list if p['status'] == 'warning')
        
        return {
            'total_budgeted': round(total_budgeted, 2),
            'total_actual': round(total_actual, 2),
            'total_remaining': round(total_remaining, 2),
            'budgets_count': len(progress_list),
            'over_budget_count': over_budget_count,
            'at_risk_count': at_risk_count
        }

