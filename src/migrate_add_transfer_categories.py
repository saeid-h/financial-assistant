"""
Migration: Add 'transfer' category type and Savings/Investments categories.

This script updates the database to support a third category type: 'transfer'
for savings, investments, and account transfers.
"""

import sqlite3
import os
import sys

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'financial_assistant.db')


def migrate():
    """Add transfer category type and related categories."""
    
    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found at: {DB_PATH}")
        sys.exit(1)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("🔄 Starting migration...")
    
    # Step 1: Create new categories table with updated type constraint
    print("  Creating new categories table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            parent_id INTEGER,
            level INTEGER NOT NULL CHECK(level BETWEEN 1 AND 3),
            type TEXT NOT NULL CHECK(type IN ('income', 'expense', 'transfer')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (parent_id) REFERENCES categories_new(id) ON DELETE CASCADE,
            UNIQUE(name, parent_id)
        );
    """)
    
    # Step 2: Copy existing data
    print("  Copying existing categories...")
    cursor.execute("""
        INSERT INTO categories_new (id, name, parent_id, level, type, created_at)
        SELECT id, name, parent_id, level, type, created_at
        FROM categories
    """)
    
    # Step 3: Add new Savings/Investments categories
    print("  Adding Savings/Investments categories...")
    
    # Get max ID
    cursor.execute("SELECT MAX(id) FROM categories_new")
    max_id = cursor.fetchone()[0] or 0
    
    transfer_categories = [
        {'name': 'Savings & Investments', 'parent_id': None, 'level': 1, 'type': 'transfer'},
        {'name': 'Savings Account', 'parent': 'Savings & Investments', 'level': 2, 'type': 'transfer'},
        {'name': 'Emergency Fund', 'parent': 'Savings & Investments', 'level': 2, 'type': 'transfer'},
        {'name': 'Retirement', 'parent': 'Savings & Investments', 'level': 2, 'type': 'transfer'},
        {'name': 'Investment Account', 'parent': 'Savings & Investments', 'level': 2, 'type': 'transfer'},
        {'name': 'Account Transfer', 'parent': 'Savings & Investments', 'level': 2, 'type': 'transfer'},
    ]
    
    category_ids = {}
    
    for cat in transfer_categories:
        parent_id = None
        if 'parent' in cat:
            parent_id = category_ids.get(cat['parent'])
        elif 'parent_id' in cat:
            parent_id = cat['parent_id']
        
        cursor.execute("""
            INSERT INTO categories_new (name, parent_id, level, type)
            VALUES (?, ?, ?, ?)
        """, (cat['name'], parent_id, cat['level'], cat['type']))
        
        category_ids[cat['name']] = cursor.lastrowid
    
    # Step 4: Drop old table and rename new
    print("  Replacing old categories table...")
    cursor.execute("DROP TABLE categories")
    cursor.execute("ALTER TABLE categories_new RENAME TO categories")
    
    # Step 5: Recreate indexes
    print("  Recreating indexes...")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_categories_parent ON categories(parent_id)")
    
    conn.commit()
    conn.close()
    
    print("✅ Migration complete!")
    print(f"   Added 6 Savings/Investments categories")
    print(f"   Total categories: {len(transfer_categories) + max_id}")


if __name__ == '__main__':
    print("⚠️  This migration will modify the database structure.")
    print("   It will add support for 'transfer' category type")
    print("   and add Savings/Investments categories.")
    
    response = input("\nContinue? (yes/no): ")
    if response.lower() == 'yes':
        migrate()
    else:
        print("❌ Migration cancelled")

