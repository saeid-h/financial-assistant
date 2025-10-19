"""
Seed default categorization rules.

This script populates the categorization_rules table with common merchant patterns.
"""

import sqlite3
import os
import sys

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))

from models.category import Category

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'financial_assistant.db')


def seed_categorization_rules():
    """Seed default categorization rules."""
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check if rules already exist
    cursor.execute("SELECT COUNT(*) FROM categorization_rules")
    existing_count = cursor.fetchone()[0]
    
    if existing_count > 0:
        print(f"ℹ️  {existing_count} categorization rules already exist")
        response = input("Do you want to add more rules? (yes/no): ")
        if response.lower() != 'yes':
            conn.close()
            print("✓ Keeping existing rules")
            return
    
    # Get category IDs
    category_model = Category(DB_PATH)
    all_categories = category_model.get_all()
    
    # Build name→id mapping
    cat_map = {cat['name']: cat['id'] for cat in all_categories}
    
    # Define default rules
    # Format: (pattern, category_name, priority)
    default_rules = [
        # Groceries
        ('COSTCO|COSTCO WHSE', 'Groceries', 95),
        ('WALMART|WAL-MART', 'Groceries', 95),
        ('SAFEWAY|SAFEWAY STORE', 'Groceries', 95),
        ('TRADER JOE|TRADER JOES', 'Groceries', 95),
        ('WHOLE FOODS|WHOLEFOODS', 'Groceries', 95),
        ('KROGER', 'Groceries', 95),
        ('TARGET', 'Groceries', 90),  # Could also be shopping
        ('GROCERY|MARKET|SUPERMARKET', 'Groceries', 85),
        
        # Gas
        ('SHELL|SHELL OIL', 'Gas', 95),
        ('CHEVRON', 'Gas', 95),
        ('76|UNION 76', 'Gas', 95),
        ('ARCO|AM PM', 'Gas', 95),
        ('EXXON|MOBIL', 'Gas', 95),
        ('BP|BRITISH PETROLEUM', 'Gas', 95),
        ('VALERO', 'Gas', 95),
        ('TEXACO', 'Gas', 95),
        ('GAS STATION|FUEL', 'Gas', 85),
        
        # Dining Out
        ('RESTAURANT|CAFE|COFFEE', 'Dining Out', 85),
        ('STARBUCKS', 'Dining Out', 95),
        ('MCDONALDS|MCDONALD', 'Dining Out', 95),
        ('SUBWAY|CHIPOTLE|PANDA EXPRESS', 'Dining Out', 95),
        ('PIZZA|BURGER|TACO', 'Dining Out', 85),
        ('DOORDASH|UBER EATS|GRUBHUB', 'Dining Out', 95),
        
        # Shopping
        ('AMAZON|AMZN', 'Shopping', 95),
        ('EBAY', 'Shopping', 95),
        ('BEST BUY', 'Shopping', 95),
        ('APPLE.COM|APPLE STORE', 'Shopping', 95),
        
        # Entertainment
        ('NETFLIX|HULU|DISNEY', 'Subscriptions', 95),
        ('SPOTIFY|APPLE MUSIC', 'Subscriptions', 95),
        ('YOUTUBE PREMIUM', 'Subscriptions', 95),
        ('MOVIE|CINEMA|THEATER', 'Entertainment', 90),
        ('SPOTIFY|MUSIC', 'Entertainment', 85),
        
        # Utilities
        ('PG&E|PGE|PACIFIC GAS', 'Utilities', 95),
        ('WATER DISTRICT|WATER DEPT', 'Utilities', 95),
        ('ELECTRIC|ELECTRICITY', 'Utilities', 90),
        ('COMCAST|XFINITY', 'Utilities', 95),
        ('AT&T|ATT MOBILITY', 'Utilities', 95),
        ('VERIZON', 'Utilities', 95),
        ('T-MOBILE|TMOBILE', 'Utilities', 95),
        
        # Healthcare
        ('PHARMACY|WALGREENS|CVS|RITE AID', 'Healthcare', 95),
        ('DOCTOR|MEDICAL|CLINIC|HOSPITAL', 'Healthcare', 90),
        ('DENTAL|DENTIST', 'Healthcare', 95),
        
        # Transportation
        ('UBER|LYFT', 'Transportation', 95),
        ('PARKING', 'Transportation', 90),
        ('TOLL|BRIDGE|FASTRAK', 'Transportation', 90),
        ('AUTO|CAR REPAIR|MECHANIC', 'Car Maintenance', 90),
        
        # Housing
        ('RENT PAYMENT|RENT PMT', 'Rent', 95),
        ('MORTGAGE PAYMENT|MORTGAGE PMT', 'Mortgage', 95),
        ('PROPERTY TAX', 'Property Tax', 95),
        ('HOME DEPOT|LOWES|HARDWARE', 'Home Maintenance', 90),
        
        # Insurance
        ('INSURANCE|INS PAYMENT', 'Insurance', 90),
        ('GEICO|STATE FARM|ALLSTATE', 'Insurance', 95),
        
        # Income
        ('SALARY|PAYROLL|PAYCHECK', 'Salary', 95),
        ('DEPOSIT|DIRECT DEP', 'Salary', 80),  # Could be other income
        ('TRANSFER FROM', 'Other Income', 70),
        ('REFUND|RETURN', 'Other Income', 80),
    ]
    
    # Insert rules
    inserted = 0
    skipped = 0
    
    for pattern, category_name, priority in default_rules:
        category_id = cat_map.get(category_name)
        
        if not category_id:
            print(f"⚠️  Warning: Category '{category_name}' not found, skipping rule")
            skipped += 1
            continue
        
        try:
            cursor.execute("""
                INSERT INTO categorization_rules (pattern, category_id, priority, match_count)
                VALUES (?, ?, ?, 0)
            """, (pattern, category_id, priority))
            inserted += 1
        
        except sqlite3.IntegrityError:
            # Rule already exists
            skipped += 1
    
    conn.commit()
    conn.close()
    
    print(f"\n✓ Categorization rules seeded:")
    print(f"  - Inserted: {inserted}")
    print(f"  - Skipped (already exist): {skipped}")
    print(f"  - Total rules in database: {existing_count + inserted}")


if __name__ == '__main__':
    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found at: {DB_PATH}")
        print("Please run: python src/init_db.py")
        sys.exit(1)
    
    seed_categorization_rules()
    print("\n✓ Done!")

