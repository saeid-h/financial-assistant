#!/usr/bin/env python3
"""
Recategorize All Uncategorized Transactions
Applies categorization rules to all uncategorized transactions
"""

import sqlite3
import os
import sys

# Add src directory to path
sys.path.insert(0, os.path.dirname(__file__))

from services.categorization_engine import CategorizationEngine

# Database path
DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    'data',
    'financial_assistant.db'
)

def recategorize_all():
    """Recategorize all uncategorized transactions"""
    
    print("=" * 60)
    print("Recategorizing All Uncategorized Transactions")
    print("=" * 60)
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        # Get all uncategorized transactions
        cursor.execute("""
            SELECT id, description, amount
            FROM transactions
            WHERE category_id IS NULL
            ORDER BY date DESC
        """)
        
        uncategorized = cursor.fetchall()
        total_uncategorized = len(uncategorized)
        
        print(f"\nFound {total_uncategorized} uncategorized transactions")
        
        if total_uncategorized == 0:
            print("✅ All transactions are already categorized!")
            return
        
        print("\nApplying categorization rules...\n")
        
        # Initialize categorization engine
        engine = CategorizationEngine(DB_PATH)
        
        categorized_count = 0
        
        for txn in uncategorized:
            # Create transaction dict for engine
            transaction = {
                'id': txn['id'],
                'description': txn['description'],
                'amount': txn['amount']
            }
            
            # Try to categorize
            result = engine.categorize_transaction(transaction)
            
            if result and result['category_id']:
                category_id = result['category_id']
                
                # Update transaction
                cursor.execute("""
                    UPDATE transactions 
                    SET category_id = ?
                    WHERE id = ?
                """, (category_id, txn['id']))
                
                categorized_count += 1
                
                # Use category name from result
                cat_name = result.get('category_name', 'Unknown')
                confidence = result.get('confidence', 0) * 100
                
                print(f"✓ #{txn['id']}: \"{txn['description'][:50]}...\" → {cat_name} ({confidence:.0f}%)")
        
        conn.commit()
        
        print("\n" + "=" * 60)
        print(f"✅ Recategorization Complete!")
        print("=" * 60)
        print(f"\nTotal uncategorized: {total_uncategorized}")
        print(f"Successfully categorized: {categorized_count}")
        print(f"Still uncategorized: {total_uncategorized - categorized_count}")
        print(f"Success rate: {(categorized_count / total_uncategorized * 100):.1f}%")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ Error during recategorization: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == '__main__':
    recategorize_all()

