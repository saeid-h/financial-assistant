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
        date_from = request.args.get('date_from', type=str)
        date_to = request.args.get('date_to', type=str)
        search = request.args.get('search', type=str)
        amount_min = request.args.get('amount_min', type=float)
        amount_max = request.args.get('amount_max', type=float)
        transaction_type = request.args.get('type', type=str)
        limit = request.args.get('limit', type=int)
        
        # Parse category IDs (comma-separated)
        category_ids = None
        category_ids_str = request.args.get('category_ids', type=str)
        if category_ids_str:
            category_ids = [int(id) for id in category_ids_str.split(',') if id.strip()]
        
        # Parse tag IDs (comma-separated)
        tag_ids = None
        tag_ids_str = request.args.get('tag_ids', type=str)
        if tag_ids_str:
            tag_ids = [int(id) for id in tag_ids_str.split(',') if id.strip()]
        
        # Get filtered transactions
        transactions = Transaction.get_filtered(
            account_id=account_id,
            date_from=date_from,
            date_to=date_to,
            search=search,
            amount_min=amount_min,
            amount_max=amount_max,
            category_ids=category_ids,
            transaction_type=transaction_type,
            tag_ids=tag_ids,
            limit=limit
        )
        
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
    """Get transaction statistics with optional filtering."""
    try:
        account_id = request.args.get('account_id', type=int)
        date_from = request.args.get('date_from', type=str)
        date_to = request.args.get('date_to', type=str)
        search = request.args.get('search', type=str)
        amount_min = request.args.get('amount_min', type=float)
        amount_max = request.args.get('amount_max', type=float)
        transaction_type = request.args.get('type', type=str)
        
        # Parse category IDs (comma-separated)
        category_ids = None
        category_ids_str = request.args.get('category_ids', type=str)
        if category_ids_str:
            category_ids = [int(id) for id in category_ids_str.split(',') if id.strip()]
        
        # Parse tag IDs (comma-separated)
        tag_ids = None
        tag_ids_str = request.args.get('tag_ids', type=str)
        if tag_ids_str:
            tag_ids = [int(id) for id in tag_ids_str.split(',') if id.strip()]
        
        # Get filtered transactions for stats
        transactions = Transaction.get_filtered(
            account_id=account_id,
            date_from=date_from,
            date_to=date_to,
            search=search,
            amount_min=amount_min,
            amount_max=amount_max,
            category_ids=category_ids,
            transaction_type=transaction_type,
            tag_ids=tag_ids
        )
        
        # Calculate stats
        # Following accounting standards:
        # - Positive amounts = Credits (income, deposits, payments received)
        # - Negative amounts = Debits (expenses, withdrawals, payments made)
        total_transactions = len(transactions)
        total_credits = sum(t['amount'] for t in transactions if t['amount'] > 0)
        total_debits = sum(abs(t['amount']) for t in transactions if t['amount'] < 0)
        net_cash_flow = total_credits - total_debits
        
        # Get accounts
        account_model = Account(current_app.config['DATABASE'])
        accounts = account_model.get_all()
        
        stats = {
            'total_transactions': total_transactions,
            'total_credits': round(total_credits, 2),
            'total_debits': round(total_debits, 2),
            'net_cash_flow': round(net_cash_flow, 2),
            'accounts': accounts
        }
        
        return jsonify({
            'success': True,
            'stats': stats
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

