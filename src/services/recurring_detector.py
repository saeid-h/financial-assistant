"""
Recurring Transaction Detection Service

Analyzes transaction history to identify recurring patterns (subscriptions, bills, regular payments).
Uses fuzzy matching, interval analysis, and amount consistency to detect patterns.

Created: 2025-10-19
Author: Saeed Hoss
"""

import sqlite3
from datetime import datetime, timedelta, date
from typing import List, Dict, Optional, Tuple
from collections import defaultdict
import Levenshtein


class RecurringDetector:
    """Service for detecting recurring transaction patterns."""
    
    # Frequency definitions (days, tolerance)
    FREQUENCIES = {
        'weekly': (7, 2),          # 7 days ± 2 days
        'biweekly': (14, 3),       # 14 days ± 3 days  
        'monthly': (30, 3),        # 30 days ± 3 days (28-31 day months)
        'quarterly': (90, 7),      # 90 days ± 7 days
        'annual': (365, 14)        # 365 days ± 14 days
    }
    
    # Detection thresholds
    MIN_OCCURRENCES = 3            # Need at least 3 transactions
    MIN_SIMILARITY = 0.85          # 85% description similarity
    MAX_AMOUNT_VARIANCE = 0.10     # ±10% amount variance
    MIN_CONFIDENCE = 0.75          # Minimum confidence to save pattern
    
    def __init__(self, db_path: str):
        """
        Initialize the detector.
        
        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path
    
    def is_similar_description(self, desc1: str, desc2: str, threshold: float = MIN_SIMILARITY) -> bool:
        """
        Check if two descriptions are similar using Levenshtein distance.
        
        Args:
            desc1: First description
            desc2: Second description
            threshold: Minimum similarity ratio (0.0-1.0)
        
        Returns:
            True if descriptions are similar enough
        """
        if not desc1 or not desc2:
            return False
        
        # Normalize (lowercase, strip whitespace)
        d1 = desc1.lower().strip()
        d2 = desc2.lower().strip()
        
        # Remove numbers for better matching (NETFLIX #123 == NETFLIX #456)
        import re
        d1_no_nums = re.sub(r'[#\d]+', '', d1).strip()
        d2_no_nums = re.sub(r'[#\d]+', '', d2).strip()
        
        # Calculate similarity ratio on normalized strings
        ratio = Levenshtein.ratio(d1_no_nums, d2_no_nums)
        
        return ratio >= threshold
    
    def extract_merchant_name(self, description: str) -> str:
        """
        Extract core merchant name from description.
        
        Args:
            description: Transaction description
        
        Returns:
            Simplified merchant name
        """
        # Remove common suffixes/prefixes
        desc = description.upper().strip()
        
        # Remove location numbers
        import re
        desc = re.sub(r'#\d+', '', desc)           # Remove #123
        desc = re.sub(r'\d{3,}', '', desc)         # Remove long numbers
        desc = re.sub(r'\s+', ' ', desc).strip()   # Normalize whitespace
        
        return desc[:50]  # Limit length
    
    def calculate_intervals(self, dates: List[date]) -> List[int]:
        """
        Calculate day intervals between consecutive dates.
        
        Args:
            dates: List of transaction dates (sorted)
        
        Returns:
            List of day intervals
        """
        if len(dates) < 2:
            return []
        
        intervals = []
        for i in range(1, len(dates)):
            delta = (dates[i] - dates[i-1]).days
            intervals.append(delta)
        
        return intervals
    
    def detect_frequency(self, intervals: List[int]) -> Optional[Tuple[str, float]]:
        """
        Detect frequency pattern from intervals.
        
        Args:
            intervals: List of day intervals between transactions
        
        Returns:
            Tuple of (frequency_name, confidence) or None if no pattern
        """
        if not intervals or len(intervals) < 2:
            return None
        
        avg_interval = sum(intervals) / len(intervals)
        
        # Try each frequency type
        best_match = None
        best_confidence = 0.0
        
        for freq_name, (expected_days, tolerance) in self.FREQUENCIES.items():
            # Check if average interval matches this frequency
            if abs(avg_interval - expected_days) <= tolerance:
                # Calculate confidence based on consistency
                deviations = [abs(interval - expected_days) for interval in intervals]
                avg_deviation = sum(deviations) / len(deviations)
                max_deviation = max(deviations)
                
                # Confidence decreases with deviation
                if max_deviation <= tolerance:
                    confidence = 1.0 - (avg_deviation / tolerance)
                    confidence = max(0.0, min(1.0, confidence))
                    
                    if confidence > best_confidence:
                        best_match = freq_name
                        best_confidence = confidence
        
        if best_match and best_confidence >= 0.5:
            return (best_match, best_confidence)
        
        return None
    
    def is_consistent_amount(self, amounts: List[float], tolerance: float = MAX_AMOUNT_VARIANCE) -> Tuple[bool, float, float]:
        """
        Check if amounts are consistent within tolerance.
        
        Args:
            amounts: List of transaction amounts
            tolerance: Maximum allowed variance (0.10 = ±10%)
        
        Returns:
            Tuple of (is_consistent, average_amount, variance)
        """
        if not amounts:
            return (False, 0.0, 0.0)
        
        # Calculate average (use absolute values for consistency)
        abs_amounts = [abs(amt) for amt in amounts]
        avg_amount = sum(abs_amounts) / len(abs_amounts)
        
        if avg_amount == 0:
            return (False, 0.0, 0.0)
        
        # Calculate variance as percentage of average
        max_deviation = max(abs(amt - avg_amount) for amt in abs_amounts)
        variance = max_deviation / avg_amount
        
        is_consistent = variance <= tolerance
        
        return (is_consistent, avg_amount, variance)
    
    def group_similar_transactions(self, transactions: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Group transactions by similar descriptions.
        
        Args:
            transactions: List of transaction dictionaries
        
        Returns:
            Dictionary mapping merchant name to list of similar transactions
        """
        groups = defaultdict(list)
        processed = set()
        
        for i, txn in enumerate(transactions):
            if i in processed:
                continue
            
            merchant = self.extract_merchant_name(txn['description'])
            group = [txn]
            processed.add(i)
            
            # Find similar transactions
            for j, other_txn in enumerate(transactions):
                if j <= i or j in processed:
                    continue
                
                if self.is_similar_description(txn['description'], other_txn['description']):
                    group.append(other_txn)
                    processed.add(j)
            
            if len(group) >= self.MIN_OCCURRENCES:
                groups[merchant] = group
        
        return dict(groups)
    
    def calculate_next_expected_date(self, last_date: date, frequency: str) -> date:
        """
        Calculate next expected transaction date.
        
        Args:
            last_date: Date of last transaction
            frequency: Frequency type
        
        Returns:
            Expected date of next transaction
        """
        expected_days, _ = self.FREQUENCIES.get(frequency, (30, 3))
        return last_date + timedelta(days=expected_days)
    
    def detect_patterns(self, account_id: Optional[int] = None, min_confidence: float = MIN_CONFIDENCE) -> List[Dict]:
        """
        Scan transactions to detect recurring patterns.
        
        Args:
            account_id: Optional account ID to limit scope
            min_confidence: Minimum confidence score to save pattern
        
        Returns:
            List of detected recurring patterns
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            # Get all transactions (negative amounts only - expenses/bills)
            query = """
                SELECT id, account_id, date, description, amount, category_id
                FROM transactions
                WHERE amount < 0
            """
            
            params = []
            if account_id:
                query += " AND account_id = ?"
                params.append(account_id)
            
            query += " ORDER BY description, date"
            
            cursor.execute(query, params)
            transactions = [dict(row) for row in cursor.fetchall()]
            
            if not transactions:
                return []
            
            # Group by similar descriptions
            groups = self.group_similar_transactions(transactions)
            
            detected_patterns = []
            
            # Analyze each group
            for merchant, txn_group in groups.items():
                if len(txn_group) < self.MIN_OCCURRENCES:
                    continue
                
                # Sort by date
                txn_group.sort(key=lambda x: x['date'])
                
                # Extract dates and amounts
                dates = [datetime.strptime(t['date'], '%Y-%m-%d').date() for t in txn_group]
                amounts = [abs(t['amount']) for t in txn_group]
                
                # Calculate intervals
                intervals = self.calculate_intervals(dates)
                
                if not intervals:
                    continue
                
                # Detect frequency
                freq_result = self.detect_frequency(intervals)
                if not freq_result:
                    continue
                
                frequency, freq_confidence = freq_result
                
                # Check amount consistency
                is_consistent, avg_amount, amount_variance = self.is_consistent_amount(amounts)
                
                if not is_consistent:
                    continue  # Amounts too variable
                
                # Calculate overall confidence
                # Factors: frequency confidence, amount consistency, occurrence count
                amount_confidence = 1.0 - amount_variance  # Lower variance = higher confidence
                occurrence_bonus = min(0.1 * (len(txn_group) - 3), 0.2)  # Bonus for more occurrences
                
                overall_confidence = (
                    freq_confidence * 0.5 +      # 50% weight on frequency
                    amount_confidence * 0.3 +    # 30% weight on amount consistency
                    0.2 + occurrence_bonus       # 20% base + bonus for occurrences
                )
                overall_confidence = min(1.0, overall_confidence)
                
                if overall_confidence < min_confidence:
                    continue  # Confidence too low
                
                # Get most common category
                category_ids = [t['category_id'] for t in txn_group if t['category_id']]
                most_common_category = max(set(category_ids), key=category_ids.count) if category_ids else None
                
                # Create pattern
                pattern = {
                    'merchant_name': merchant,
                    'description_pattern': txn_group[0]['description'][:100],
                    'frequency': frequency,
                    'average_amount': round(avg_amount, 2),
                    'amount_variance': round(amount_variance * avg_amount, 2),
                    'category_id': most_common_category,
                    'last_transaction_date': dates[-1].strftime('%Y-%m-%d'),
                    'next_expected_date': self.calculate_next_expected_date(dates[-1], frequency).strftime('%Y-%m-%d'),
                    'confidence_score': round(overall_confidence, 2),
                    'transaction_count': len(txn_group),
                    'transaction_ids': [t['id'] for t in txn_group]
                }
                
                detected_patterns.append(pattern)
            
            return detected_patterns
            
        finally:
            conn.close()
    
    def save_recurring_pattern(self, pattern: Dict) -> int:
        """
        Save a detected recurring pattern to the database.
        
        Args:
            pattern: Pattern dictionary from detect_patterns()
        
        Returns:
            ID of created recurring_transaction
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
                pattern['merchant_name'],
                pattern['description_pattern'],
                pattern['frequency'],
                pattern['average_amount'],
                pattern['amount_variance'],
                pattern.get('category_id'),
                pattern['last_transaction_date'],
                pattern['next_expected_date'],
                'active',
                1,  # alert_if_missing
                1,  # alert_if_amount_changes
                pattern.get('confidence_score', 0.85),
                datetime.now(),
                datetime.now()
            ))
            
            recurring_id = cursor.lastrowid
            
            # Create instances for matched transactions
            if 'transaction_ids' in pattern:
                for txn_id in pattern['transaction_ids']:
                    # Get transaction details
                    cursor.execute("SELECT date, amount FROM transactions WHERE id = ?", (txn_id,))
                    txn = cursor.fetchone()
                    if txn:
                        cursor.execute("""
                            INSERT INTO recurring_transaction_instances (
                                recurring_id, transaction_id, expected_date,
                                actual_date, expected_amount, actual_amount,
                                variance_amount, status, created_at
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            recurring_id,
                            txn_id,
                            txn[0],  # expected = actual for historical
                            txn[0],  # actual date
                            pattern['average_amount'],
                            abs(txn[1]),
                            abs(abs(txn[1]) - pattern['average_amount']),
                            'on_time',  # Historical transactions assumed on time
                            datetime.now()
                        ))
            
            conn.commit()
            return recurring_id
            
        except Exception as e:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def scan_and_save_all(self, account_id: Optional[int] = None) -> Dict[str, int]:
        """
        Scan for patterns and save all detected recurring transactions.
        
        Args:
            account_id: Optional account ID to limit scope
        
        Returns:
            Dictionary with scan results
        """
        patterns = self.detect_patterns(account_id=account_id)
        
        saved_count = 0
        skipped_count = 0
        
        for pattern in patterns:
            try:
                self.save_recurring_pattern(pattern)
                saved_count += 1
            except Exception as e:
                print(f"Skipped pattern '{pattern['merchant_name']}': {e}")
                skipped_count += 1
        
        return {
            'total_patterns': len(patterns),
            'saved': saved_count,
            'skipped': skipped_count
        }
    
    def check_new_transaction(self, transaction: Dict) -> Optional[int]:
        """
        Check if a new transaction matches an existing recurring pattern.
        
        Args:
            transaction: Transaction dictionary with id, description, amount, date
        
        Returns:
            Recurring transaction ID if matched, None otherwise
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            # Get all active recurring transactions
            cursor.execute("""
                SELECT * FROM recurring_transactions
                WHERE status = 'active'
                ORDER BY confidence_score DESC
            """)
            
            recurring_txns = cursor.fetchall()
            
            for rec in recurring_txns:
                # Check description similarity
                if self.is_similar_description(transaction['description'], rec['description_pattern']):
                    # Check amount consistency (±10%)
                    amount_diff = abs(abs(transaction['amount']) - rec['average_amount'])
                    if amount_diff / rec['average_amount'] <= self.MAX_AMOUNT_VARIANCE:
                        return rec['id']
            
            return None
            
        finally:
            conn.close()

