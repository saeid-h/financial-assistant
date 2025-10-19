"""
Duplicate Detection Service for Financial Assistant

This service detects duplicate transactions to prevent re-importing the same data.
"""

import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from difflib import SequenceMatcher


class DuplicateDetector:
    """
    Service to detect duplicate transactions based on multiple criteria.
    """
    
    # Configurable thresholds
    EXACT_MATCH_THRESHOLD = 1.0
    HIGH_CONFIDENCE_THRESHOLD = 0.8
    POSSIBLE_MATCH_THRESHOLD = 0.6
    DATE_TOLERANCE_DAYS = 2
    AMOUNT_TOLERANCE_PERCENT = 5
    
    def __init__(self, db_path: str):
        """
        Initialize the duplicate detector.
        
        Args:
            db_path: Path to the SQLite database
        """
        self.db_path = db_path
    
    def check_duplicate(self, transaction: Dict) -> Dict:
        """
        Check if a single transaction is a duplicate.
        
        Args:
            transaction: Dictionary with keys: account_id, date, amount, description
            
        Returns:
            Dictionary with keys:
                - transaction: The input transaction
                - is_duplicate: Boolean indicating if it's a duplicate
                - confidence: Float from 0.0 to 1.0
                - matches: List of matching existing transactions
        """
        matches = self._find_potential_matches(transaction)
        
        if not matches:
            return {
                'transaction': transaction,
                'is_duplicate': False,
                'confidence': 0.0,
                'matches': []
            }
        
        # Get the highest confidence match
        best_match = max(matches, key=lambda m: m['confidence'])
        
        return {
            'transaction': transaction,
            'is_duplicate': best_match['confidence'] >= self.HIGH_CONFIDENCE_THRESHOLD,
            'confidence': best_match['confidence'],
            'matches': matches
        }
    
    def check_duplicates_bulk(self, transactions: List[Dict]) -> List[Dict]:
        """
        Check multiple transactions for duplicates.
        
        Args:
            transactions: List of transaction dictionaries
            
        Returns:
            List of duplicate check results
        """
        return [self.check_duplicate(txn) for txn in transactions]
    
    def _find_potential_matches(self, transaction: Dict) -> List[Dict]:
        """
        Find potential duplicate matches in the database.
        
        Args:
            transaction: Transaction to check
            
        Returns:
            List of potential matches with confidence scores
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Extract transaction details
        account_id = transaction.get('account_id')
        txn_date = self._parse_date(transaction.get('date'))
        amount = float(transaction.get('amount', 0))
        description = str(transaction.get('description', '')).strip()
        
        if not all([account_id, txn_date, description]):
            conn.close()
            return []
        
        # Calculate date range
        date_start = txn_date - timedelta(days=self.DATE_TOLERANCE_DAYS)
        date_end = txn_date + timedelta(days=self.DATE_TOLERANCE_DAYS)
        
        # Calculate amount range
        amount_tolerance = abs(amount) * (self.AMOUNT_TOLERANCE_PERCENT / 100)
        amount_min = amount - amount_tolerance
        amount_max = amount + amount_tolerance
        
        # Query for potential matches
        query = """
            SELECT id, date, description, amount, account_id
            FROM transactions
            WHERE account_id = ?
            AND date BETWEEN ? AND ?
            AND amount BETWEEN ? AND ?
        """
        
        cursor.execute(query, (
            account_id,
            date_start.isoformat(),
            date_end.isoformat(),
            amount_min,
            amount_max
        ))
        
        potential_matches = cursor.fetchall()
        conn.close()
        
        # Calculate confidence scores for each match
        matches = []
        for match in potential_matches:
            confidence, match_type = self._calculate_confidence(
                transaction, dict(match)
            )
            
            if confidence >= self.POSSIBLE_MATCH_THRESHOLD:
                matches.append({
                    'existing_transaction': dict(match),
                    'confidence': confidence,
                    'match_type': match_type
                })
        
        # Sort by confidence (highest first)
        matches.sort(key=lambda m: m['confidence'], reverse=True)
        
        return matches
    
    def _calculate_confidence(self, txn1: Dict, txn2: Dict) -> Tuple[float, str]:
        """
        Calculate confidence score between two transactions.
        
        Args:
            txn1: First transaction
            txn2: Second transaction (from database)
            
        Returns:
            Tuple of (confidence_score, match_type)
        """
        # Parse and compare dates
        date1 = self._parse_date(txn1.get('date'))
        date2 = self._parse_date(txn2.get('date'))
        date_diff = abs((date1 - date2).days)
        
        # Compare amounts
        amount1 = float(txn1.get('amount', 0))
        amount2 = float(txn2.get('amount', 0))
        
        # Exact amount match
        if abs(amount1 - amount2) < 0.01:  # Account for floating point precision
            amount_score = 1.0
        else:
            # Calculate percentage difference
            avg_amount = (abs(amount1) + abs(amount2)) / 2
            if avg_amount > 0:
                percent_diff = abs(amount1 - amount2) / avg_amount * 100
                amount_score = max(0, 1 - (percent_diff / self.AMOUNT_TOLERANCE_PERCENT))
            else:
                amount_score = 0
        
        # Compare descriptions
        desc1 = self._normalize_description(txn1.get('description', ''))
        desc2 = self._normalize_description(txn2.get('description', ''))
        description_score = self._similarity_score(desc1, desc2)
        
        # Date score (perfect match = 1.0, decreases with days difference)
        if date_diff == 0:
            date_score = 1.0
        else:
            date_score = max(0, 1 - (date_diff / self.DATE_TOLERANCE_DAYS))
        
        # Calculate overall confidence
        # Weights: date=30%, amount=40%, description=30%
        confidence = (
            date_score * 0.3 +
            amount_score * 0.4 +
            description_score * 0.3
        )
        
        # Determine match type
        if confidence >= self.EXACT_MATCH_THRESHOLD:
            match_type = 'exact'
        elif confidence >= self.HIGH_CONFIDENCE_THRESHOLD:
            match_type = 'high'
        else:
            match_type = 'possible'
        
        return round(confidence, 2), match_type
    
    def _normalize_description(self, description: str) -> str:
        """
        Normalize description for comparison.
        
        Args:
            description: Transaction description
            
        Returns:
            Normalized description
        """
        # Convert to lowercase and strip whitespace
        normalized = description.lower().strip()
        
        # Remove extra whitespace
        normalized = ' '.join(normalized.split())
        
        # Remove common words that don't add value
        common_words = ['transaction', 'payment', 'purchase', 'debit', 'credit']
        words = normalized.split()
        words = [w for w in words if w not in common_words]
        
        return ' '.join(words)
    
    def _similarity_score(self, str1: str, str2: str) -> float:
        """
        Calculate similarity score between two strings.
        
        Args:
            str1: First string
            str2: Second string
            
        Returns:
            Similarity score from 0.0 to 1.0
        """
        if not str1 or not str2:
            return 0.0
        
        # Use SequenceMatcher for similarity
        return SequenceMatcher(None, str1, str2).ratio()
    
    def _parse_date(self, date_value) -> datetime:
        """
        Parse date from various formats.
        
        Args:
            date_value: Date as string, datetime, or date object
            
        Returns:
            datetime object
        """
        if isinstance(date_value, datetime):
            return date_value
        
        if isinstance(date_value, str):
            # Try common date formats
            for fmt in ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y']:
                try:
                    return datetime.strptime(date_value, fmt)
                except ValueError:
                    continue
        
        # If all else fails, return a very old date
        return datetime(1970, 1, 1)

