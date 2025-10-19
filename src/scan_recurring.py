#!/usr/bin/env python3
"""
Bulk Scanner for Recurring Transactions

Scans all existing transactions to detect recurring patterns and saves them to the database.
Run this after importing historical data to identify subscriptions and bills.

Usage:
    python src/scan_recurring.py [--account-id ID] [--min-confidence 0.75]

Created: 2025-10-19
Author: Saeed Hoss
"""

import sys
import argparse
from services.recurring_detector import RecurringDetector

# Database path
DB_PATH = 'data/financial_assistant.db'


def scan_recurring_transactions(account_id=None, min_confidence=0.75):
    """
    Scan all transactions for recurring patterns.
    
    Args:
        account_id: Optional account ID to limit scope
        min_confidence: Minimum confidence score to save patterns
    """
    print("=" * 60)
    print("Recurring Transaction Scanner")
    print("=" * 60)
    
    detector = RecurringDetector(DB_PATH)
    
    if account_id:
        print(f"Scanning account ID: {account_id}")
    else:
        print("Scanning ALL accounts")
    
    print(f"Minimum confidence: {min_confidence}")
    print()
    
    # Detect patterns
    print("Analyzing transactions for recurring patterns...")
    patterns = detector.detect_patterns(account_id=account_id, min_confidence=min_confidence)
    
    print(f"✓ Found {len(patterns)} recurring patterns")
    print()
    
    if not patterns:
        print("No recurring patterns detected.")
        print("This could mean:")
        print("  - Not enough transaction history (need 3+ occurrences)")
        print("  - Transactions too irregular")
        print("  - Confidence threshold too high")
        return
    
    # Display detected patterns
    print("Detected Patterns:")
    print("-" * 60)
    for i, pattern in enumerate(patterns, 1):
        print(f"{i}. {pattern['merchant_name']}")
        print(f"   Frequency: {pattern['frequency']}")
        print(f"   Average: ${pattern['average_amount']:.2f}")
        print(f"   Variance: ${pattern['amount_variance']:.2f}")
        print(f"   Confidence: {pattern['confidence_score']:.2f}")
        print(f"   Occurrences: {pattern['transaction_count']}")
        print(f"   Next expected: {pattern['next_expected_date']}")
        print()
    
    # Ask for confirmation
    response = input(f"Save {len(patterns)} recurring patterns to database? (yes/no): ").lower()
    
    if response not in ['yes', 'y']:
        print("Scan cancelled. No patterns saved.")
        return
    
    # Save patterns
    print("\nSaving patterns...")
    saved = 0
    errors = 0
    
    for pattern in patterns:
        try:
            recurring_id = detector.save_recurring_pattern(pattern)
            saved += 1
            print(f"✓ Saved: {pattern['merchant_name']} (ID: {recurring_id})")
        except Exception as e:
            errors += 1
            print(f"✗ Error saving {pattern['merchant_name']}: {e}")
    
    print()
    print("=" * 60)
    print(f"Scan Complete!")
    print(f"  Patterns detected: {len(patterns)}")
    print(f"  Successfully saved: {saved}")
    print(f"  Errors: {errors}")
    print("=" * 60)
    
    if saved > 0:
        print(f"\nVisit http://localhost:5001/recurring to view recurring transactions")


def main():
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(
        description="Scan transactions for recurring patterns"
    )
    
    parser.add_argument(
        '--account-id',
        type=int,
        help='Limit scan to specific account ID'
    )
    
    parser.add_argument(
        '--min-confidence',
        type=float,
        default=0.75,
        help='Minimum confidence score to save patterns (default: 0.75)'
    )
    
    args = parser.parse_args()
    
    try:
        scan_recurring_transactions(
            account_id=args.account_id,
            min_confidence=args.min_confidence
        )
    except KeyboardInterrupt:
        print("\n\nScan cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

