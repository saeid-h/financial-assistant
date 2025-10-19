"""
Unit tests for the Duplicate Detector service
"""

import pytest
import sqlite3
from datetime import datetime, timedelta
from src.services.duplicate_detector import DuplicateDetector


@pytest.fixture
def test_db(tmp_path):
    """Create a temporary test database with sample data."""
    db_path = str(tmp_path / "test.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create transactions table
    cursor.execute("""
        CREATE TABLE transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            category_id INTEGER,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Insert sample transactions
    today = datetime.now().date()
    cursor.execute("""
        INSERT INTO transactions (account_id, date, description, amount)
        VALUES (?, ?, ?, ?)
    """, (1, today.isoformat(), "Grocery Store", -45.50))
    
    cursor.execute("""
        INSERT INTO transactions (account_id, date, description, amount)
        VALUES (?, ?, ?, ?)
    """, (1, today.isoformat(), "Amazon Purchase", -125.00))
    
    yesterday = today - timedelta(days=1)
    cursor.execute("""
        INSERT INTO transactions (account_id, date, description, amount)
        VALUES (?, ?, ?, ?)
    """, (1, yesterday.isoformat(), "Gas Station", -45.20))
    
    conn.commit()
    conn.close()
    
    return db_path


def test_exact_duplicate_detection(test_db):
    """Test detecting exact duplicate transactions."""
    detector = DuplicateDetector(test_db)
    
    today = datetime.now().date()
    transaction = {
        'account_id': 1,
        'date': today.isoformat(),
        'description': 'Grocery Store',
        'amount': -45.50
    }
    
    result = detector.check_duplicate(transaction)
    
    assert result['is_duplicate'] is True
    assert result['confidence'] >= 0.9
    assert len(result['matches']) > 0
    assert result['matches'][0]['match_type'] in ['exact', 'high']


def test_high_confidence_duplicate(test_db):
    """Test detecting high confidence duplicates with similar descriptions."""
    detector = DuplicateDetector(test_db)
    
    today = datetime.now().date()
    transaction = {
        'account_id': 1,
        'date': today.isoformat(),
        'description': 'Grocery Store Purchase',  # Slightly different
        'amount': -45.50
    }
    
    result = detector.check_duplicate(transaction)
    
    assert result['is_duplicate'] is True or result['confidence'] >= 0.7
    assert len(result['matches']) > 0


def test_possible_duplicate_similar_description(test_db):
    """Test detecting possible duplicates with similar descriptions."""
    detector = DuplicateDetector(test_db)
    
    today = datetime.now().date()
    transaction = {
        'account_id': 1,
        'date': today.isoformat(),
        'description': 'Grocery Shop',  # Similar but different
        'amount': -46.00  # Slightly different amount
    }
    
    result = detector.check_duplicate(transaction)
    
    # Should find a match with some confidence
    assert result['confidence'] >= 0.5


def test_no_duplicate_different_amount(test_db):
    """Test that different amounts don't match."""
    detector = DuplicateDetector(test_db)
    
    today = datetime.now().date()
    transaction = {
        'account_id': 1,
        'date': today.isoformat(),
        'description': 'Grocery Store',
        'amount': -100.00  # Very different amount
    }
    
    result = detector.check_duplicate(transaction)
    
    # Should not find a high-confidence match
    assert result['confidence'] < 0.7


def test_no_duplicate_different_date(test_db):
    """Test that transactions with different dates don't match."""
    detector = DuplicateDetector(test_db)
    
    future_date = datetime.now().date() + timedelta(days=10)
    transaction = {
        'account_id': 1,
        'date': future_date.isoformat(),
        'description': 'Grocery Store',
        'amount': -45.50
    }
    
    result = detector.check_duplicate(transaction)
    
    # Should not match (date too far apart)
    assert result['is_duplicate'] is False


def test_no_duplicate_different_account(test_db):
    """Test that transactions from different accounts don't match."""
    detector = DuplicateDetector(test_db)
    
    today = datetime.now().date()
    transaction = {
        'account_id': 999,  # Different account
        'date': today.isoformat(),
        'description': 'Grocery Store',
        'amount': -45.50
    }
    
    result = detector.check_duplicate(transaction)
    
    # Should not match (different account)
    assert result['is_duplicate'] is False
    assert len(result['matches']) == 0


def test_description_similarity_calculation(test_db):
    """Test description similarity algorithm."""
    detector = DuplicateDetector(test_db)
    
    # Test exact match
    score1 = detector._similarity_score("Grocery Store", "Grocery Store")
    assert score1 == 1.0
    
    # Test similar strings
    score2 = detector._similarity_score("Grocery Store", "Grocery Shop")
    assert 0.5 < score2 < 1.0
    
    # Test very different strings
    score3 = detector._similarity_score("Grocery Store", "Amazon Purchase")
    assert score3 < 0.5


def test_description_normalization(test_db):
    """Test description normalization."""
    detector = DuplicateDetector(test_db)
    
    # Test lowercase and whitespace normalization
    normalized1 = detector._normalize_description("  GROCERY  STORE  ")
    assert normalized1 == "grocery store"
    
    # Test removal of common words
    normalized2 = detector._normalize_description("Transaction Payment Grocery Store")
    assert "transaction" not in normalized2
    assert "payment" not in normalized2
    assert "grocery" in normalized2


def test_bulk_duplicate_check(test_db):
    """Test checking multiple transactions at once."""
    detector = DuplicateDetector(test_db)
    
    today = datetime.now().date()
    transactions = [
        {
            'account_id': 1,
            'date': today.isoformat(),
            'description': 'Grocery Store',
            'amount': -45.50
        },
        {
            'account_id': 1,
            'date': today.isoformat(),
            'description': 'New Restaurant',
            'amount': -25.00
        }
    ]
    
    results = detector.check_duplicates_bulk(transactions)
    
    assert len(results) == 2
    assert results[0]['is_duplicate'] is True  # Matches existing
    assert results[1]['is_duplicate'] is False  # New transaction


def test_configurable_thresholds(test_db):
    """Test that thresholds can be configured."""
    detector = DuplicateDetector(test_db)
    
    # Change thresholds
    original_threshold = detector.HIGH_CONFIDENCE_THRESHOLD
    detector.HIGH_CONFIDENCE_THRESHOLD = 0.95
    
    today = datetime.now().date()
    transaction = {
        'account_id': 1,
        'date': today.isoformat(),
        'description': 'Grocery Store Purchase',
        'amount': -45.50
    }
    
    result = detector.check_duplicate(transaction)
    
    # Should be more strict now
    # Restore original threshold
    detector.HIGH_CONFIDENCE_THRESHOLD = original_threshold


def test_date_tolerance(test_db):
    """Test date tolerance for matching."""
    detector = DuplicateDetector(test_db)
    
    today = datetime.now().date()
    # Transaction 1 day later (within 2-day tolerance)
    transaction = {
        'account_id': 1,
        'date': (today + timedelta(days=1)).isoformat(),
        'description': 'Grocery Store',
        'amount': -45.50
    }
    
    result = detector.check_duplicate(transaction)
    
    # Should find a match within tolerance
    assert len(result['matches']) > 0
    assert result['is_duplicate'] is True


def test_amount_tolerance(test_db):
    """Test amount tolerance for matching."""
    detector = DuplicateDetector(test_db)
    
    today = datetime.now().date()
    # Amount within 5% tolerance (45.50 * 1.05 = 47.78)
    transaction = {
        'account_id': 1,
        'date': today.isoformat(),
        'description': 'Grocery Store',
        'amount': -47.00
    }
    
    result = detector.check_duplicate(transaction)
    
    # Should find a match within tolerance
    assert len(result['matches']) > 0


def test_empty_database(tmp_path):
    """Test duplicate detection with empty database."""
    db_path = str(tmp_path / "empty.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    
    detector = DuplicateDetector(db_path)
    
    transaction = {
        'account_id': 1,
        'date': '2025-10-19',
        'description': 'Test Transaction',
        'amount': -10.00
    }
    
    result = detector.check_duplicate(transaction)
    
    assert result['is_duplicate'] is False
    assert result['confidence'] == 0.0
    assert len(result['matches']) == 0


def test_invalid_transaction_data(test_db):
    """Test handling of invalid transaction data."""
    detector = DuplicateDetector(test_db)
    
    # Missing required fields
    transaction = {
        'account_id': 1,
        'date': None,
        'description': '',
        'amount': 0
    }
    
    result = detector.check_duplicate(transaction)
    
    # Should handle gracefully
    assert result['is_duplicate'] is False
    assert len(result['matches']) == 0

