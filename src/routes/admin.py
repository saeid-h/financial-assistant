"""
Admin routes for database management.
"""

from flask import Blueprint, request, jsonify, render_template, current_app
import sqlite3
import os

# Create blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/')
def admin_page():
    """Render the admin management page."""
    return render_template('admin.html')


@admin_bp.route('/api/reset-database', methods=['POST'])
def reset_database():
    """
    Reset the database by deleting all transactions and accounts.
    Requires confirmation token.
    
    Request JSON:
        {
            "confirmation": "DELETE ALL DATA",
            "reset_type": "all" | "transactions"
        }
    
    Returns:
        JSON with success status and counts
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'No data provided'
        }), 400
    
    # Require exact confirmation text
    confirmation = data.get('confirmation', '').strip()
    if confirmation != 'DELETE ALL DATA':
        return jsonify({
            'success': False,
            'error': 'Invalid confirmation text. You must type exactly: DELETE ALL DATA'
        }), 400
    
    reset_type = data.get('reset_type', 'all')
    
    if reset_type not in ['all', 'transactions']:
        return jsonify({
            'success': False,
            'error': 'Invalid reset_type. Must be "all" or "transactions"'
        }), 400
    
    try:
        db_path = current_app.config['DATABASE']
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Count before deletion
        cursor.execute("SELECT COUNT(*) FROM transactions")
        transaction_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM accounts")
        account_count = cursor.fetchone()[0]
        
        # Delete data based on reset_type
        if reset_type == 'all':
            # Delete all transactions first (due to foreign key)
            cursor.execute("DELETE FROM transactions")
            # Delete all accounts
            cursor.execute("DELETE FROM accounts")
            # Reset auto-increment counters
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='transactions'")
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='accounts'")
            
            conn.commit()
            conn.close()
            
            return jsonify({
                'success': True,
                'message': f'Database reset complete. Deleted {transaction_count} transactions and {account_count} accounts.',
                'transactions_deleted': transaction_count,
                'accounts_deleted': account_count
            })
        
        else:  # transactions only
            cursor.execute("DELETE FROM transactions")
            # Reset auto-increment counter
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='transactions'")
            
            conn.commit()
            conn.close()
            
            return jsonify({
                'success': True,
                'message': f'Transactions reset complete. Deleted {transaction_count} transactions. Kept {account_count} accounts.',
                'transactions_deleted': transaction_count,
                'accounts_deleted': 0
            })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Database reset failed: {str(e)}'
        }), 500


@admin_bp.route('/api/stats', methods=['GET'])
def get_stats():
    """Get database statistics."""
    try:
        db_path = current_app.config['DATABASE']
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM transactions")
        transaction_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM accounts")
        account_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM categories")
        category_count = cursor.fetchone()[0]
        
        # Get database file size
        db_size = os.path.getsize(db_path) if os.path.exists(db_path) else 0
        db_size_mb = db_size / (1024 * 1024)
        
        conn.close()
        
        return jsonify({
            'success': True,
            'stats': {
                'transactions': transaction_count,
                'accounts': account_count,
                'categories': category_count,
                'database_size_mb': round(db_size_mb, 2)
            }
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to get stats: {str(e)}'
        }), 500

