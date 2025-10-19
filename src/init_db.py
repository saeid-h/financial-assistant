"""
Database initialization script for Financial Assistant.

Creates SQLite database with schema for accounts, transactions, 
categories, and categorization rules.
"""

import sqlite3
import os
import sys
from datetime import datetime

# Database path
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'financial_assistant.db')

def create_database():
    """Create the SQLite database and all required tables."""
    
    # Ensure data directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    # Connect to database (creates file if doesn't exist)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # Create Accounts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL CHECK(type IN ('checking', 'savings', 'credit')),
            institution TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    # Create Categories table (hierarchical structure)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            parent_id INTEGER,
            level INTEGER NOT NULL CHECK(level BETWEEN 1 AND 3),
            type TEXT NOT NULL CHECK(type IN ('income', 'expense')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (parent_id) REFERENCES categories(id) ON DELETE CASCADE,
            UNIQUE(name, parent_id)
        );
    """)
    
    # Create Transactions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER NOT NULL,
            date DATE NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            category_id INTEGER,
            notes TEXT,
            tags TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE,
            FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
        );
    """)
    
    # Create Categorization Rules table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categorization_rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pattern TEXT NOT NULL,
            category_id INTEGER NOT NULL,
            priority INTEGER DEFAULT 0,
            match_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
            UNIQUE(pattern)
        );
    """)
    
    # Create indexes for better query performance
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_transactions_account ON transactions(account_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(date);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_transactions_category ON transactions(category_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_categories_parent ON categories(parent_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_rules_priority ON categorization_rules(priority DESC);")
    
    conn.commit()
    print(f"✓ Database created successfully at: {DB_PATH}")
    
    return conn

def seed_default_categories(conn):
    """Populate database with default category hierarchy."""
    
    cursor = conn.cursor()
    
    # Check if categories already exist
    cursor.execute("SELECT COUNT(*) FROM categories")
    if cursor.fetchone()[0] > 0:
        print("✓ Categories already exist, skipping seed data")
        return
    
    # Define default category structure
    categories = [
        # Income categories (Level 1)
        {'name': 'Income', 'parent_id': None, 'level': 1, 'type': 'income'},
        
        # Income subcategories (Level 2)
        {'name': 'Salary', 'parent': 'Income', 'level': 2, 'type': 'income'},
        {'name': 'Freelance', 'parent': 'Income', 'level': 2, 'type': 'income'},
        {'name': 'Investment', 'parent': 'Income', 'level': 2, 'type': 'income'},
        {'name': 'Other Income', 'parent': 'Income', 'level': 2, 'type': 'income'},
        
        # Expense categories (Level 1)
        {'name': 'Fixed Expenses', 'parent_id': None, 'level': 1, 'type': 'expense'},
        {'name': 'Variable Expenses', 'parent_id': None, 'level': 1, 'type': 'expense'},
        {'name': 'Discretionary', 'parent_id': None, 'level': 1, 'type': 'expense'},
        
        # Fixed Expenses subcategories (Level 2)
        {'name': 'Housing', 'parent': 'Fixed Expenses', 'level': 2, 'type': 'expense'},
        {'name': 'Transportation', 'parent': 'Fixed Expenses', 'level': 2, 'type': 'expense'},
        {'name': 'Insurance', 'parent': 'Fixed Expenses', 'level': 2, 'type': 'expense'},
        {'name': 'Utilities', 'parent': 'Fixed Expenses', 'level': 2, 'type': 'expense'},
        
        # Housing subcategories (Level 3)
        {'name': 'Rent', 'parent': 'Housing', 'level': 3, 'type': 'expense'},
        {'name': 'Mortgage', 'parent': 'Housing', 'level': 3, 'type': 'expense'},
        {'name': 'Property Tax', 'parent': 'Housing', 'level': 3, 'type': 'expense'},
        {'name': 'Home Maintenance', 'parent': 'Housing', 'level': 3, 'type': 'expense'},
        
        # Transportation subcategories (Level 3)
        {'name': 'Car Payment', 'parent': 'Transportation', 'level': 3, 'type': 'expense'},
        {'name': 'Gas', 'parent': 'Transportation', 'level': 3, 'type': 'expense'},
        {'name': 'Public Transit', 'parent': 'Transportation', 'level': 3, 'type': 'expense'},
        {'name': 'Car Maintenance', 'parent': 'Transportation', 'level': 3, 'type': 'expense'},
        
        # Variable Expenses subcategories (Level 2)
        {'name': 'Groceries', 'parent': 'Variable Expenses', 'level': 2, 'type': 'expense'},
        {'name': 'Healthcare', 'parent': 'Variable Expenses', 'level': 2, 'type': 'expense'},
        {'name': 'Personal Care', 'parent': 'Variable Expenses', 'level': 2, 'type': 'expense'},
        {'name': 'Clothing', 'parent': 'Variable Expenses', 'level': 2, 'type': 'expense'},
        
        # Discretionary subcategories (Level 2)
        {'name': 'Dining Out', 'parent': 'Discretionary', 'level': 2, 'type': 'expense'},
        {'name': 'Entertainment', 'parent': 'Discretionary', 'level': 2, 'type': 'expense'},
        {'name': 'Shopping', 'parent': 'Discretionary', 'level': 2, 'type': 'expense'},
        {'name': 'Travel', 'parent': 'Discretionary', 'level': 2, 'type': 'expense'},
        {'name': 'Subscriptions', 'parent': 'Discretionary', 'level': 2, 'type': 'expense'},
        {'name': 'Hobbies', 'parent': 'Discretionary', 'level': 2, 'type': 'expense'},
    ]
    
    # Dictionary to store category IDs by name
    category_ids = {}
    
    # Insert categories (must be done in order: level 1, then 2, then 3)
    for level in [1, 2, 3]:
        for cat in categories:
            if cat['level'] == level:
                parent_id = None
                if 'parent' in cat:
                    parent_name = cat['parent']
                    parent_id = category_ids.get(parent_name)
                elif 'parent_id' in cat:
                    parent_id = cat['parent_id']
                
                cursor.execute("""
                    INSERT INTO categories (name, parent_id, level, type)
                    VALUES (?, ?, ?, ?)
                """, (cat['name'], parent_id, cat['level'], cat['type']))
                
                category_ids[cat['name']] = cursor.lastrowid
    
    conn.commit()
    print(f"✓ Seeded {len(categories)} default categories")

def reset_database():
    """Delete and recreate the database (DESTRUCTIVE!)."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"✓ Deleted existing database at: {DB_PATH}")
    
    conn = create_database()
    seed_default_categories(conn)
    conn.close()

def main():
    """Main function to initialize database."""
    
    # Check for --reset flag
    if len(sys.argv) > 1 and sys.argv[1] == '--reset':
        response = input("⚠️  WARNING: This will delete all existing data! Continue? (yes/no): ")
        if response.lower() == 'yes':
            reset_database()
            print("✓ Database reset complete")
        else:
            print("✗ Database reset cancelled")
        return
    
    # Normal initialization
    if os.path.exists(DB_PATH):
        print(f"ℹ️  Database already exists at: {DB_PATH}")
        response = input("Do you want to reset it? (yes/no): ")
        if response.lower() == 'yes':
            reset_database()
        else:
            print("✓ Keeping existing database")
    else:
        conn = create_database()
        seed_default_categories(conn)
        conn.close()
        print("✓ Database initialization complete")

if __name__ == '__main__':
    main()

