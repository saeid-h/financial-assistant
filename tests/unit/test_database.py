"""
Unit tests for database schema and initialization.
"""

import sqlite3

def test_database_exists(app):
    """Test that database file is configured."""
    assert app.config['DATABASE'] is not None

def test_accounts_table_exists(app):
    """Test that accounts table exists with correct schema."""
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='accounts'")
    result = cursor.fetchone()
    
    assert result is not None
    assert result[0] == 'accounts'
    
    conn.close()

def test_transactions_table_exists(app):
    """Test that transactions table exists."""
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='transactions'")
    result = cursor.fetchone()
    
    assert result is not None
    assert result[0] == 'transactions'
    
    conn.close()

def test_categories_table_exists(app):
    """Test that categories table exists."""
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='categories'")
    result = cursor.fetchone()
    
    assert result is not None
    assert result[0] == 'categories'
    
    conn.close()

def test_categorization_rules_table_exists(app):
    """Test that categorization_rules table exists."""
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='categorization_rules'")
    result = cursor.fetchone()
    
    assert result is not None
    assert result[0] == 'categorization_rules'
    
    conn.close()

def test_insert_account(app, sample_account):
    """Test inserting an account into the database."""
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name, type FROM accounts WHERE id = ?", (sample_account,))
    result = cursor.fetchone()
    
    assert result is not None
    assert result[0] == sample_account
    assert result[1] == 'Test Checking'
    assert result[2] == 'checking'
    
    conn.close()

def test_insert_category(app, sample_category):
    """Test inserting a category into the database."""
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name, type, level FROM categories WHERE id = ?", (sample_category,))
    result = cursor.fetchone()
    
    assert result is not None
    assert result[0] == sample_category
    assert result[1] == 'Test Category'
    assert result[2] == 'expense'
    assert result[3] == 1
    
    conn.close()

def test_foreign_key_constraint(app, sample_account):
    """Test that foreign key constraints are enforced."""
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()
    
    # Enable foreign keys (required for each connection)
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # Try to insert transaction with non-existent account
    try:
        cursor.execute("""
            INSERT INTO transactions (account_id, date, description, amount)
            VALUES (99999, '2025-01-01', 'Test', 100.00)
        """)
        conn.commit()
        assert False, "Foreign key constraint should have failed"
    except sqlite3.IntegrityError:
        # This is expected
        pass
    
    conn.close()

