"""
Unit tests for RecurringDetector service.

Tests pattern detection algorithm including:
- Description similarity matching
- Frequency detection from intervals
- Amount consistency checking
- Pattern detection and saving

Created: 2025-10-19
"""

import pytest
import sqlite3
from datetime import date, timedelta
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.services.recurring_detector import RecurringDetector


class TestRecurringDetector:
    """Test suite for RecurringDetector."""
    
    @pytest.fixture
    def detector(self, app):
        """Create detector instance with test database."""
        return RecurringDetector(app.config['DATABASE'])
    
    def test_is_similar_description(self, detector):
        """Test description similarity matching."""
        # Exact match
        assert detector.is_similar_description("NETFLIX", "NETFLIX") == True
        
        # Case insensitive
        assert detector.is_similar_description("Netflix", "NETFLIX") == True
        
        # Similar with numbers
        assert detector.is_similar_description("NETFLIX #123", "NETFLIX #456") == True
        
        # Similar with spaces
        assert detector.is_similar_description("NET FLIX", "NETFLIX") == True
        
        # Different merchants
        assert detector.is_similar_description("NETFLIX", "SPOTIFY") == False
        
        # Empty strings
        assert detector.is_similar_description("", "NETFLIX") == False
        assert detector.is_similar_description("NETFLIX", "") == False
    
    def test_extract_merchant_name(self, detector):
        """Test merchant name extraction."""
        # Remove location numbers
        assert "COSTCO WHSE" in detector.extract_merchant_name("COSTCO WHSE #123")
        
        # Remove long ID numbers
        merchant = detector.extract_merchant_name("NETFLIX 123456789")
        assert "NETFLIX" in merchant
        assert "123456789" not in merchant
        
        # Normalize whitespace
        merchant = detector.extract_merchant_name("SHELL   GAS   STATION")
        assert "SHELL GAS STATION" in merchant
    
    def test_calculate_intervals(self, detector):
        """Test interval calculation."""
        # 30-day intervals (monthly)
        dates = [
            date(2025, 1, 1),
            date(2025, 2, 1),  # 31 days
            date(2025, 3, 1),  # 28 days
            date(2025, 4, 1)   # 31 days
        ]
        intervals = detector.calculate_intervals(dates)
        assert len(intervals) == 3
        assert all(28 <= interval <= 31 for interval in intervals)
        
        # Single date
        assert detector.calculate_intervals([date(2025, 1, 1)]) == []
        
        # Empty list
        assert detector.calculate_intervals([]) == []
    
    def test_detect_frequency_monthly(self, detector):
        """Test monthly frequency detection."""
        # Perfect monthly (30 days)
        intervals = [30, 30, 30]
        result = detector.detect_frequency(intervals)
        assert result is not None
        frequency, confidence = result
        assert frequency == 'monthly'
        assert confidence > 0.9
        
        # Monthly with variance (28-31 days)
        intervals = [31, 28, 30, 31]
        result = detector.detect_frequency(intervals)
        assert result is not None
        frequency, confidence = result
        assert frequency == 'monthly'
        assert confidence > 0.5  # Adjusted for variance in month lengths
    
    def test_detect_frequency_weekly(self, detector):
        """Test weekly frequency detection."""
        # Perfect weekly (7 days)
        intervals = [7, 7, 7, 7]
        result = detector.detect_frequency(intervals)
        assert result is not None
        frequency, confidence = result
        assert frequency == 'weekly'
        assert confidence > 0.9
        
        # Weekly with slight variance
        intervals = [7, 6, 8, 7]
        result = detector.detect_frequency(intervals)
        assert result is not None
        frequency, confidence = result
        assert frequency == 'weekly'
    
    def test_detect_frequency_irregular(self, detector):
        """Test irregular intervals (no pattern)."""
        # Completely irregular
        intervals = [3, 45, 12, 89]
        result = detector.detect_frequency(intervals)
        assert result is None
        
        # Too few intervals
        intervals = [30]
        result = detector.detect_frequency(intervals)
        assert result is None
    
    def test_is_consistent_amount_exact(self, detector):
        """Test exact amount consistency."""
        # Exact same amounts
        amounts = [15.99, 15.99, 15.99]
        is_consistent, avg, variance = detector.is_consistent_amount(amounts)
        assert is_consistent == True
        assert avg == 15.99
        assert variance < 0.01
    
    def test_is_consistent_amount_similar(self, detector):
        """Test similar amount consistency."""
        # Within 10% variance
        amounts = [100.00, 105.00, 98.00]  # ±5%
        is_consistent, avg, variance = detector.is_consistent_amount(amounts)
        assert is_consistent == True
        assert 100 <= avg <= 102
        assert variance <= 0.10
    
    def test_is_consistent_amount_inconsistent(self, detector):
        """Test inconsistent amounts."""
        # Over 10% variance
        amounts = [100.00, 150.00, 80.00]  # ±50%
        is_consistent, avg, variance = detector.is_consistent_amount(amounts)
        assert is_consistent == False
        assert variance > 0.10
    
    def test_calculate_next_expected_date(self, detector):
        """Test next expected date calculation."""
        last_date = date(2025, 10, 1)
        
        # Monthly: +30 days
        next_date = detector.calculate_next_expected_date(last_date, 'monthly')
        assert next_date == date(2025, 10, 31)
        
        # Weekly: +7 days
        next_date = detector.calculate_next_expected_date(last_date, 'weekly')
        assert next_date == date(2025, 10, 8)
        
        # Quarterly: +90 days
        next_date = detector.calculate_next_expected_date(last_date, 'quarterly')
        assert next_date == date(2025, 12, 30)
    
    def test_detect_patterns_with_sample_data(self, detector, app):
        """Test pattern detection with sample recurring transactions."""
        conn = sqlite3.connect(app.config['DATABASE'])
        cursor = conn.cursor()
        
        try:
            # Create test account
            cursor.execute("""
                INSERT INTO accounts (name, type, institution) 
                VALUES ('Test Account', 'checking', 'Test Bank')
            """)
            account_id = cursor.lastrowid
            
            # Add Netflix transactions (perfect monthly pattern)
            base_date = date(2025, 1, 15)
            for i in range(5):
                txn_date = base_date + timedelta(days=30*i)
                cursor.execute("""
                    INSERT INTO transactions (account_id, date, description, amount)
                    VALUES (?, ?, ?, ?)
                """, (account_id, txn_date.strftime('%Y-%m-%d'), 'NETFLIX.COM', -15.99))
            
            conn.commit()
            
            # Detect patterns
            patterns = detector.detect_patterns(account_id=account_id)
            
            # Should detect Netflix as recurring
            assert len(patterns) > 0
            
            netflix_pattern = patterns[0]
            assert 'NETFLIX' in netflix_pattern['merchant_name'].upper()
            assert netflix_pattern['frequency'] == 'monthly'
            assert abs(netflix_pattern['average_amount'] - 15.99) < 0.01
            assert netflix_pattern['confidence_score'] > 0.80
            assert netflix_pattern['transaction_count'] == 5
            
        finally:
            conn.close()
    
    def test_group_similar_transactions(self, detector):
        """Test transaction grouping by similarity."""
        transactions = [
            {'id': 1, 'description': 'NETFLIX #123', 'amount': -15.99, 'date': '2025-01-01'},
            {'id': 2, 'description': 'NETFLIX #456', 'amount': -15.99, 'date': '2025-02-01'},
            {'id': 3, 'description': 'NETFLIX #789', 'amount': -15.99, 'date': '2025-03-01'},
            {'id': 4, 'description': 'SPOTIFY PREMIUM', 'amount': -9.99, 'date': '2025-01-01'},
            {'id': 5, 'description': 'COSTCO WHSE', 'amount': -156.78, 'date': '2025-01-01'},
        ]
        
        groups = detector.group_similar_transactions(transactions)
        
        # Should group Netflix transactions together
        netflix_group = None
        for merchant, txns in groups.items():
            if 'NETFLIX' in merchant:
                netflix_group = txns
                break
        
        assert netflix_group is not None
        assert len(netflix_group) == 3  # All 3 Netflix transactions grouped
        
        # Spotify and Costco should not be in Netflix group
        netflix_ids = [t['id'] for t in netflix_group]
        assert 4 not in netflix_ids
        assert 5 not in netflix_ids

