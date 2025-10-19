"""
Transaction routes for Financial Assistant
"""

from flask import Blueprint, render_template, jsonify, request, current_app
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from models.transaction import Transaction
from models.account import Account


transactions_bp = Blueprint('transactions', __name__, url_prefix='/transactions')


@transactions_bp.route('/')
def transactions_page():
    """Display the transactions page."""
    return render_template('transactions.html')


@transactions_bp.route('/api/all')
def get_all_transactions():
    """Get all transactions with optional filtering."""
    try:
        account_id = request.args.get('account_id', type=int)
        limit = request.args.get('limit', type=int)
        offset = request.args.get('offset', 0, type=int)
        
        if account_id:
            transactions = Transaction.get_by_account(account_id, limit=limit)
        else:
            transactions = Transaction.get_all(limit=limit)
        
        return jsonify({
            'success': True,
            'transactions': transactions,
            'count': len(transactions)
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@transactions_bp.route('/api/<int:transaction_id>')
def get_transaction(transaction_id):
    """Get a single transaction by ID."""
    try:
        transaction = Transaction.get_by_id(transaction_id)
        
        if not transaction:
            return jsonify({'success': False, 'error': 'Transaction not found'}), 404
        
        return jsonify({
            'success': True,
            'transaction': transaction
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@transactions_bp.route('/api/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    """Delete a transaction."""
    try:
        success = Transaction.delete(transaction_id)
        
        if not success:
            return jsonify({'success': False, 'error': 'Transaction not found'}), 404
        
        return jsonify({
            'success': True,
            'message': 'Transaction deleted successfully'
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@transactions_bp.route('/api/stats')
def get_transaction_stats():
    """Get transaction statistics."""
    try:
        account_id = request.args.get('account_id', type=int)
        
        # Get all transactions for stats
        if account_id:
            transactions = Transaction.get_by_account(account_id)
        else:
            transactions = Transaction.get_all()
        
        # Calculate stats
        total_transactions = len(transactions)
        total_expenses = sum(t['amount'] for t in transactions if t['amount'] > 0)
        total_income = sum(abs(t['amount']) for t in transactions if t['amount'] < 0)
        net_cash_flow = total_income - total_expenses
        
        # Get accounts
        account_model = Account(current_app.config['DATABASE'])
        accounts = account_model.get_all()
        
        stats = {
            'total_transactions': total_transactions,
            'total_expenses': round(total_expenses, 2),
            'total_income': round(total_income, 2),
            'net_cash_flow': round(net_cash_flow, 2),
            'accounts': accounts
        }
        
        return jsonify({
            'success': True,
            'stats': stats
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

