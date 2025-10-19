"""
Import routes for CSV file upload and transaction import.
"""

from flask import Blueprint, render_template, request, jsonify, session, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
import sys
import tempfile
from datetime import datetime

# Add src directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from models.account import Account
from models.transaction import Transaction
from services.csv_parser import CSVParser, CSVParseError
from services.transaction_validator import TransactionValidator
from services.file_archiver import FileArchiver
from services.duplicate_detector import DuplicateDetector

import_bp = Blueprint('import', __name__, url_prefix='/import')

ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@import_bp.route('/')
def import_page():
    """Show the import page."""
    from flask import current_app
    
    # Get all accounts for dropdown
    account_model = Account(current_app.config['DATABASE'])
    accounts = account_model.get_all()
    return render_template('import.html', accounts=accounts)


@import_bp.route('/upload', methods=['POST'])
def upload_file():
    """Handle CSV file upload and parse transactions."""
    
    # Check if file was uploaded
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    # Check if filename is empty
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Check file extension
    if not allowed_file(file.filename):
        return jsonify({'error': 'Only CSV files are allowed'}), 400
    
    # Get account_id
    account_id = request.form.get('account_id')
    if not account_id:
        return jsonify({'error': 'Please select an account'}), 400
    
    try:
        from flask import current_app
        account_id = int(account_id)
        
        # Verify account exists
        account_model = Account(current_app.config['DATABASE'])
        account = account_model.get_by_id(account_id)
        if not account:
            return jsonify({'error': f'Account with ID {account_id} not found'}), 404
        
    except ValueError:
        return jsonify({'error': 'Invalid account ID'}), 400
    
    # Save file temporarily
    temp_dir = tempfile.gettempdir()
    filename = secure_filename(file.filename)
    temp_path = os.path.join(temp_dir, f"{datetime.now().timestamp()}_{filename}")
    
    try:
        file.save(temp_path)
        
        # Parse CSV
        parser = CSVParser()
        transactions = parser.parse_file(temp_path)
        
        # Add account_id to each transaction
        for txn in transactions:
            txn['account_id'] = account_id
        
        # Validate transactions
        validator = TransactionValidator(db_path='data/financial_assistant.db')
        validated_results = validator.validate_transactions(transactions)
        
        # Separate valid and invalid transactions
        valid_transactions = []
        invalid_transactions = []
        
        for txn, result in validated_results:
            if result.is_valid:
                valid_transactions.append(txn)
            else:
                invalid_transactions.append({
                    'transaction': txn,
                    'errors': result.to_dict()['errors']
                })
        
        # Calculate summary statistics (following accounting standards)
        # total_credits = money coming in (positive amounts, deposits/income)
        # total_debits = money going out (negative amounts, withdrawals/expenses)
        total_credits = sum(txn['amount'] for txn in valid_transactions if txn['amount'] > 0)
        total_debits = sum(abs(txn['amount']) for txn in valid_transactions if txn['amount'] < 0)
        
        # Don't store transactions in session (too large for 800+ transactions!)
        # Instead, keep the temp file and re-parse on confirmation
        session['import_account_id'] = account_id
        session['import_filename'] = filename
        session['import_temp_file'] = temp_path  # Keep temp file for re-parsing
        session['import_valid_count'] = len(valid_transactions)  # For verification
        
        return jsonify({
            'success': True,
            'account_name': account['name'],
            'total_count': len(transactions),
            'valid_count': len(valid_transactions),
            'invalid_count': len(invalid_transactions),
            'total_credits': round(total_credits, 2),
            'total_debits': round(total_debits, 2),
            'transactions': [
                {
                    'date': txn['date'].isoformat(),
                    'description': txn['description'],
                    'amount': txn['amount']
                }
                for txn in valid_transactions[:100]  # Limit to first 100 for preview
            ],
            'invalid_transactions': invalid_transactions[:20]  # Show first 20 errors
        })
    
    except CSVParseError as e:
        # Clean up temp file on error
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return jsonify({'error': f'Failed to parse CSV: {str(e)}'}), 400
    
    except Exception as e:
        # Clean up temp file on error
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500
    
    # Note: temp file is NOT deleted here - it's kept for archiving after confirmation


@import_bp.route('/confirm', methods=['POST'])
def confirm_import():
    """Confirm and save transactions to database."""
    from flask import current_app
    
    # Get import info from session
    account_id = session.get('import_account_id')
    filename = session.get('import_filename')
    temp_file_path = session.get('import_temp_file')
    expected_count = session.get('import_valid_count')
    
    if not account_id or not temp_file_path:
        return jsonify({'error': 'No pending import found. Please upload a file first.'}), 400
    
    if not os.path.exists(temp_file_path):
        return jsonify({'error': 'Uploaded file no longer available. Please upload again.'}), 400
    
    try:
        # Re-parse the CSV file to get transactions
        parser = CSVParser()
        transactions = parser.parse_file(temp_file_path)
        
        # Validate and filter transactions
        validator = TransactionValidator(current_app.config['DATABASE'])
        valid_transactions = []
        
        for txn in transactions:
            txn['account_id'] = account_id
            result = validator.validate_transaction(txn)
            if result.is_valid:
                valid_transactions.append(txn)
        
        if len(valid_transactions) != expected_count:
            print(f"Warning: Expected {expected_count} valid transactions, got {len(valid_transactions)}")
        
        # Check for duplicates
        detector = DuplicateDetector(current_app.config['DATABASE'])
        non_duplicate_transactions = []
        duplicate_count = 0
        
        for txn in valid_transactions:
            duplicate_check = detector.check_duplicate(txn)
            
            # Only import if not a duplicate (is_duplicate = False means unique)
            if not duplicate_check['is_duplicate']:
                non_duplicate_transactions.append(txn)
            else:
                duplicate_count += 1
                confidence = duplicate_check['confidence']
                print(f"Skipping duplicate (confidence: {confidence:.0%}): {txn['date']} - {txn['description']} - ${txn['amount']}")
        
        # Save non-duplicate transactions to database
        count = Transaction.bulk_create(non_duplicate_transactions) if non_duplicate_transactions else 0
        
        # Archive the CSV file
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                archive_base = os.path.join(
                    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                    'data',
                    'archives'
                )
                archiver = FileArchiver(archive_base)
                archive_result = archiver.archive_file(temp_file_path, account_id, filename)
                
                if not archive_result['success']:
                    print(f"Warning: Failed to archive file: {archive_result.get('error')}")
                
                # Clean up temp file
                os.remove(temp_file_path)
            except Exception as e:
                print(f"Warning: Error during file archiving: {str(e)}")
                # Don't fail the import if archiving fails
        
        # Clear session
        session.pop('import_account_id', None)
        session.pop('import_filename', None)
        session.pop('import_temp_file', None)
        session.pop('import_valid_count', None)
        
        # Build response message
        if duplicate_count > 0:
            message = f'Successfully imported {count} new transactions. Skipped {duplicate_count} duplicate(s).'
        else:
            message = f'Successfully imported {count} transactions'
        
        return jsonify({
            'success': True,
            'message': message,
            'count': count,
            'duplicates_skipped': duplicate_count,
            'account_id': account_id
        })
    
    except Exception as e:
        return jsonify({'error': f'Failed to save transactions: {str(e)}'}), 500

