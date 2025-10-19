#!/usr/bin/env python3
"""
Database Migration: Add Budget Management Support
Creates budgets table for tracking spending limits
"""

import sqlite3
import os
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

# Database path
DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    'data',
    'financial_assistant.db'
)

def migrate():
    """Add budgets table to database"""
    
    print("=" * 60)
    print("Migration: Adding Budget Management Support")
    print("=" * 60)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if table already exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='budgets'
        """)
        if cursor.fetchone():
            print("⚠️  budgets table already exists")
            print("   Skipping migration to avoid data loss")
            return
        
        # Create budgets table
        print("\n1. Creating budgets table...")
        cursor.execute("""
            CREATE TABLE budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_id INTEGER NOT NULL,
                amount DECIMAL(10, 2) NOT NULL CHECK(amount > 0),
                period_type TEXT NOT NULL CHECK(period_type IN ('monthly', 'yearly')),
                start_date DATE NOT NULL,
                end_date DATE NOT NULL,
                alert_threshold INTEGER DEFAULT 80 CHECK(alert_threshold BETWEEN 0 AND 100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
                UNIQUE(category_id, period_type, start_date)
            )
        """)
        print("   ✅ budgets table created")
        
        # Create index for performance
        print("\n2. Creating index...")
        cursor.execute("""
            CREATE INDEX idx_budgets_category_period 
            ON budgets(category_id, period_type, start_date, end_date)
        """)
        print("   ✅ Index created")
        
        # Seed with example budgets for current month
        print("\n3. Seeding example budgets...")
        
        # Get some common expense categories
        cursor.execute("""
            SELECT id, name FROM categories 
            WHERE type = 'expense' AND level = 1
            LIMIT 5
        """)
        categories = cursor.fetchall()
        
        # Calculate current month dates
        today = date.today()
        start_of_month = today.replace(day=1)
        end_of_month = (start_of_month + relativedelta(months=1)) - relativedelta(days=1)
        
        example_budgets = [
            (categories[0][0], 800.00, 'Groceries'),  # Groceries
            (categories[1][0], 2000.00, 'Housing'),   # Rent/Housing
            (categories[2][0], 300.00, 'Transportation') if len(categories) > 2 else None,
        ]
        
        count = 0
        for budget in example_budgets:
            if budget:
                cursor.execute("""
                    INSERT INTO budgets (category_id, amount, period_type, start_date, end_date, alert_threshold)
                    VALUES (?, ?, 'monthly', ?, ?, 80)
                """, (budget[0], budget[1], start_of_month.isoformat(), end_of_month.isoformat()))
                count += 1
                print(f"   - ${budget[1]:.2f} for {budget[2]}")
        
        print(f"   ✅ {count} example budgets seeded for current month")
        
        # Commit changes
        conn.commit()
        
        print("\n" + "=" * 60)
        print("✅ Migration completed successfully!")
        print("=" * 60)
        print("\nBudget table created with:")
        print("  - category_id (FK to categories)")
        print("  - amount (spending limit)")
        print("  - period_type (monthly/yearly)")
        print("  - start_date, end_date")
        print("  - alert_threshold (default 80%)")
        print(f"\nSeeded {count} example budgets for {start_of_month.strftime('%B %Y')}")
        print("\n")
        
    except sqlite3.Error as e:
        print(f"\n❌ Error during migration: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == '__main__':
    migrate()

