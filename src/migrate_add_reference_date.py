#!/usr/bin/env python3
"""
Migration script to add reference_date column to accounts table.
This date indicates when the initial_balance (reference balance) was set.
"""

import sqlite3
from datetime import datetime

# Database path
DB_PATH = 'data/financial_assistant.db'

def migrate():
    """Add reference_date column to accounts table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if column already exists
        cursor.execute("PRAGMA table_info(accounts)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'reference_date' in columns:
            print("✓ reference_date column already exists")
            return
        
        print("Adding reference_date column to accounts table...")
        
        # Add reference_date column (date when initial_balance was set)
        cursor.execute("""
            ALTER TABLE accounts 
            ADD COLUMN reference_date DATE
        """)
        
        # Set default reference_date to created_at for existing accounts
        cursor.execute("""
            UPDATE accounts 
            SET reference_date = DATE(created_at)
            WHERE reference_date IS NULL
        """)
        
        conn.commit()
        print("✓ Successfully added reference_date column")
        print("✓ Set reference_date = created_at for existing accounts")
        
        # Show updated accounts
        cursor.execute("SELECT id, name, initial_balance, reference_date FROM accounts")
        accounts = cursor.fetchall()
        print(f"\nUpdated {len(accounts)} accounts:")
        for acc in accounts:
            print(f"  - {acc[1]}: Balance ${acc[2]:.2f} as of {acc[3]}")
        
    except Exception as e:
        print(f"✗ Error during migration: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    migrate()

