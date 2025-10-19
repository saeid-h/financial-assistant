"""
Account routes for account management.
"""

from flask import Blueprint, request, jsonify, render_template, current_app
from models.account import Account


# Create blueprint
accounts_bp = Blueprint('accounts', __name__)


@accounts_bp.route('/accounts')
def accounts_page():
    """Render the accounts management page."""
    return render_template('accounts.html')


@accounts_bp.route('/api/accounts', methods=['GET'])
def get_accounts():
    """
    Get all accounts.
    
    Returns:
        JSON list of accounts
    """
    account_model = Account(current_app.config['DATABASE'])
    accounts = account_model.get_all()
    
    return jsonify({
        'success': True,
        'accounts': accounts,
        'count': len(accounts)
    })


@accounts_bp.route('/api/accounts/<int:account_id>', methods=['GET'])
def get_account(account_id):
    """
    Get a specific account.
    
    Args:
        account_id: Account ID
    
    Returns:
        JSON account details or 404
    """
    account_model = Account(current_app.config['DATABASE'])
    account = account_model.get_by_id(account_id)
    
    if not account:
        return jsonify({
            'success': False,
            'error': 'Account not found'
        }), 404
    
    return jsonify({
        'success': True,
        'account': account
    })


@accounts_bp.route('/api/accounts', methods=['POST'])
def create_account():
    """
    Create a new account.
    
    Request JSON:
        {
            "name": "Account name",
            "type": "checking|savings|credit",
            "institution": "Bank name" (optional)
        }
    
    Returns:
        JSON with created account ID
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'No data provided'
        }), 400
    
    # Extract fields
    name = data.get('name')
    account_type = data.get('type')
    institution = data.get('institution')
    
    # Validate
    if not name:
        return jsonify({
            'success': False,
            'error': 'Account name is required'
        }), 400
    
    if not account_type:
        return jsonify({
            'success': False,
            'error': 'Account type is required'
        }), 400
    
    # Create account
    try:
        account_model = Account(current_app.config['DATABASE'])
        account_id = account_model.create(name, account_type, institution)
        
        return jsonify({
            'success': True,
            'message': 'Account created successfully',
            'account_id': account_id
        }), 201
    
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'An error occurred while creating the account'
        }), 500


@accounts_bp.route('/api/accounts/<int:account_id>', methods=['PUT'])
def update_account(account_id):
    """
    Update an existing account.
    
    Args:
        account_id: Account ID
    
    Request JSON:
        {
            "name": "New name" (optional),
            "type": "new_type" (optional),
            "institution": "New institution" (optional)
        }
    
    Returns:
        JSON success message or error
    """
    data = request.get_json()
    
    if not data:
        return jsonify({
            'success': False,
            'error': 'No data provided'
        }), 400
    
    # Update account
    try:
        account_model = Account(current_app.config['DATABASE'])
        success = account_model.update(
            account_id,
            name=data.get('name'),
            account_type=data.get('type'),
            institution=data.get('institution')
        )
        
        if not success:
            return jsonify({
                'success': False,
                'error': 'Account not found'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Account updated successfully'
        })
    
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'An error occurred while updating the account'
        }), 500


@accounts_bp.route('/api/accounts/<int:account_id>', methods=['DELETE'])
def delete_account(account_id):
    """
    Delete an account.
    
    Args:
        account_id: Account ID
    
    Returns:
        JSON success message or error
    
    Note:
        This will also delete all transactions associated with the account.
    """
    try:
        account_model = Account(current_app.config['DATABASE'])
        
        # Check transaction count
        transaction_count = account_model.get_transaction_count(account_id)
        
        success = account_model.delete(account_id)
        
        if not success:
            return jsonify({
                'success': False,
                'error': 'Account not found'
            }), 404
        
        return jsonify({
            'success': True,
            'message': f'Account deleted successfully. {transaction_count} transaction(s) were also deleted.'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'An error occurred while deleting the account'
        }), 500

