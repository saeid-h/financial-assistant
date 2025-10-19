#!/usr/bin/env python3
"""
Migration script to add recurring transaction tracking tables.

This creates:
1. recurring_transactions - Stores detected recurring patterns
2. recurring_transaction_instances - Tracks each occurrence

Created: 2025-10-19
Author: Saeed Hoss
"""

import sqlite3
from datetime import datetime

# Database path
DB_PATH = 'data/financial_assistant.db'

def migrate():
    """Add recurring transaction tables to the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if tables already exist
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='recurring_transactions'
        """)
        
        if cursor.fetchone():
            print("✓ recurring_transactions table already exists")
            conn.close()
            return
        
        print("Creating recurring transaction tables...")
        
        # Create recurring_transactions table
        cursor.execute("""
            CREATE TABLE recurring_transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                merchant_name TEXT NOT NULL,
                description_pattern TEXT,
                frequency TEXT NOT NULL CHECK(frequency IN ('weekly', 'biweekly', 'monthly', 'quarterly', 'annual')),
                average_amount DECIMAL(12, 2) NOT NULL,
                amount_variance DECIMAL(12, 2) DEFAULT 0.00,
                category_id INTEGER,
                last_transaction_date DATE,
                next_expected_date DATE,
                status TEXT CHECK(status IN ('active', 'paused', 'cancelled')) DEFAULT 'active',
                alert_if_missing BOOLEAN DEFAULT 1,
                alert_if_amount_changes BOOLEAN DEFAULT 1,
                confidence_score DECIMAL(3, 2) DEFAULT 0.85,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories(id)
            )
        """)
        
        print("✓ Created recurring_transactions table")
        
        # Create recurring_transaction_instances table
        cursor.execute("""
            CREATE TABLE recurring_transaction_instances (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recurring_id INTEGER NOT NULL,
                transaction_id INTEGER,
                expected_date DATE,
                actual_date DATE,
                expected_amount DECIMAL(12, 2),
                actual_amount DECIMAL(12, 2),
                variance_amount DECIMAL(12, 2),
                status TEXT CHECK(status IN ('on_time', 'late', 'missed', 'amount_changed', 'expected')) DEFAULT 'expected',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (recurring_id) REFERENCES recurring_transactions(id) ON DELETE CASCADE,
                FOREIGN KEY (transaction_id) REFERENCES transactions(id) ON DELETE SET NULL
            )
        """)
        
        print("✓ Created recurring_transaction_instances table")
        
        # Create indexes for performance
        cursor.execute("""
            CREATE INDEX idx_recurring_status ON recurring_transactions(status)
        """)
        
        cursor.execute("""
            CREATE INDEX idx_recurring_next_expected ON recurring_transactions(next_expected_date)
        """)
        
        cursor.execute("""
            CREATE INDEX idx_instances_recurring ON recurring_transaction_instances(recurring_id)
        """)
        
        cursor.execute("""
            CREATE INDEX idx_instances_transaction ON recurring_transaction_instances(transaction_id)
        """)
        
        print("✓ Created performance indexes")
        
        conn.commit()
        
        # Verify tables were created
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name IN ('recurring_transactions', 'recurring_transaction_instances')
        """)
        
        tables = cursor.fetchall()
        print(f"\n✅ Migration completed successfully!")
        print(f"Created {len(tables)} tables:")
        for table in tables:
            print(f"  - {table[0]}")
        
        # Show table schemas
        print("\nTable schemas:")
        for table in ['recurring_transactions', 'recurring_transaction_instances']:
            cursor.execute(f"PRAGMA table_info({table})")
            columns = cursor.fetchall()
            print(f"\n{table} ({len(columns)} columns):")
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")
        
    except Exception as e:
        print(f"✗ Error during migration: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    print("=" * 60)
    print("Recurring Transactions Migration")
    print("=" * 60)
    migrate()
    print("\n" + "=" * 60)
    print("Migration complete!")
    print("=" * 60)

