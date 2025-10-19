#!/usr/bin/env python3
"""
Database Migration: Add Current Balance to Accounts
Adds a balance field to track current account balance
"""

import sqlite3
import os

# Database path
DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    'data',
    'financial_assistant.db'
)

def migrate():
    """Add balance column to accounts table"""
    
    print("=" * 60)
    print("Migration: Add Current Balance to Accounts")
    print("=" * 60)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if column already exists
        cursor.execute("PRAGMA table_info(accounts)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'current_balance' in columns:
            print("⚠️  current_balance column already exists")
            print("   Skipping migration")
            return
        
        # Add balance column
        print("\n1. Adding current_balance column to accounts table...")
        cursor.execute("""
            ALTER TABLE accounts 
            ADD COLUMN current_balance DECIMAL(12, 2) DEFAULT 0.00
        """)
        print("   ✅ current_balance column added")
        
        # Calculate actual balances from transactions
        print("\n2. Calculating balances from transactions...")
        cursor.execute("""
            SELECT id, name, type FROM accounts
        """)
        accounts = cursor.fetchall()
        
        for account in accounts:
            account_id, name, acc_type = account
            
            # Sum all transactions for this account
            cursor.execute("""
                SELECT COALESCE(SUM(amount), 0) as balance
                FROM transactions
                WHERE account_id = ?
            """, (account_id,))
            
            balance = cursor.fetchone()[0]
            
            # Update account balance
            cursor.execute("""
                UPDATE accounts 
                SET current_balance = ?
                WHERE id = ?
            """, (balance, account_id))
            
            print(f"   - {name} ({acc_type}): ${balance:,.2f}")
        
        print(f"   ✅ {len(accounts)} account balances calculated")
        
        # Commit changes
        conn.commit()
        
        print("\n" + "=" * 60)
        print("✅ Migration completed successfully!")
        print("=" * 60)
        print("\nAccounts now have current_balance field")
        print("Balances calculated from transaction history")
        print("\n")
        
    except sqlite3.Error as e:
        print(f"\n❌ Error during migration: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == '__main__':
    migrate()

