#!/usr/bin/env python3
"""
Reset Transactions - Clear all transactions while keeping accounts

Use this script to clear test data or start fresh with imports.
Accounts are preserved, only transactions are deleted.
"""

import sqlite3
import os
import sys

def reset_transactions():
    """Delete all transactions from database, keep accounts."""
    
    db_path = os.path.join(os.path.dirname(__file__), 'data', 'financial_assistant.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found: {db_path}")
        sys.exit(1)
    
    # Confirm with user
    response = input("⚠️  This will DELETE all transactions but keep accounts. Continue? (yes/no): ")
    if response.lower() not in ['yes', 'y']:
        print("Cancelled.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Count current transactions
    cursor.execute('SELECT COUNT(*) FROM transactions')
    count_before = cursor.fetchone()[0]
    
    # Delete all transactions
    cursor.execute('DELETE FROM transactions')
    conn.commit()
    
    # Verify
    cursor.execute('SELECT COUNT(*) FROM transactions')
    count_after = cursor.fetchone()[0]
    
    # Show accounts (preserved)
    cursor.execute('SELECT id, name, type, institution FROM accounts')
    accounts = cursor.fetchall()
    
    conn.close()
    
    print()
    print("=" * 60)
    print(f"✅ Deleted {count_before} transactions")
    print(f"✅ {count_after} transactions remaining")
    print()
    print(f"✅ Kept {len(accounts)} accounts:")
    for acc in accounts:
        institution = acc[3] or 'No institution'
        print(f"   - {acc[1]} ({acc[2]}) - {institution}")
    print("=" * 60)
    print()
    print("Ready to import fresh data!")

if __name__ == '__main__':
    reset_transactions()

