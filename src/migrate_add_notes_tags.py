#!/usr/bin/env python3
"""
Database Migration: Add Notes and Tags Support
Adds tables for transaction notes, tags, and transaction-tag relationships
"""

import sqlite3
import os
from datetime import datetime

# Database path
DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    'data',
    'financial_assistant.db'
)

def migrate():
    """Add notes and tags tables to database"""
    
    print("=" * 60)
    print("Migration: Adding Notes and Tags Support")
    print("=" * 60)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if tables already exist
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name IN ('transaction_notes', 'tags', 'transaction_tags')
        """)
        existing = [row[0] for row in cursor.fetchall()]
        
        if existing:
            print(f"⚠️  Tables already exist: {', '.join(existing)}")
            print("   Skipping migration to avoid data loss")
            return
        
        # Create transaction_notes table
        print("\n1. Creating transaction_notes table...")
        cursor.execute("""
            CREATE TABLE transaction_notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_id INTEGER NOT NULL,
                note TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (transaction_id) REFERENCES transactions(id) ON DELETE CASCADE
            )
        """)
        print("   ✅ transaction_notes table created")
        
        # Create tags table
        print("\n2. Creating tags table...")
        cursor.execute("""
            CREATE TABLE tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                color TEXT DEFAULT '#667eea',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("   ✅ tags table created")
        
        # Create transaction_tags junction table
        print("\n3. Creating transaction_tags junction table...")
        cursor.execute("""
            CREATE TABLE transaction_tags (
                transaction_id INTEGER NOT NULL,
                tag_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (transaction_id, tag_id),
                FOREIGN KEY (transaction_id) REFERENCES transactions(id) ON DELETE CASCADE,
                FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
            )
        """)
        print("   ✅ transaction_tags junction table created")
        
        # Create indexes for performance
        print("\n4. Creating indexes...")
        cursor.execute("""
            CREATE INDEX idx_transaction_notes_transaction_id 
            ON transaction_notes(transaction_id)
        """)
        cursor.execute("""
            CREATE INDEX idx_transaction_tags_transaction_id 
            ON transaction_tags(transaction_id)
        """)
        cursor.execute("""
            CREATE INDEX idx_transaction_tags_tag_id 
            ON transaction_tags(tag_id)
        """)
        print("   ✅ Indexes created")
        
        # Seed with example tags
        print("\n5. Seeding example tags...")
        example_tags = [
            ('Business', '#667eea'),
            ('Personal', '#764ba2'),
            ('Tax-Deductible', '#28a745'),
            ('Reimbursable', '#ffc107'),
            ('Subscription', '#dc3545'),
            ('One-Time', '#17a2b8'),
            ('Split', '#6c757d'),
            ('Cash', '#fd7e14'),
            ('Gift', '#e83e8c'),
            ('Emergency', '#dc3545')
        ]
        
        for name, color in example_tags:
            cursor.execute("""
                INSERT INTO tags (name, color) VALUES (?, ?)
            """, (name, color))
        
        print(f"   ✅ {len(example_tags)} example tags seeded")
        
        # Commit changes
        conn.commit()
        
        print("\n" + "=" * 60)
        print("✅ Migration completed successfully!")
        print("=" * 60)
        print("\nNew tables created:")
        print("  - transaction_notes (for adding notes to transactions)")
        print("  - tags (for custom labels)")
        print("  - transaction_tags (many-to-many relationship)")
        print(f"\nSeeded {len(example_tags)} example tags:")
        for name, color in example_tags:
            print(f"  - {name} ({color})")
        print("\n")
        
    except sqlite3.Error as e:
        print(f"\n❌ Error during migration: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == '__main__':
    migrate()

