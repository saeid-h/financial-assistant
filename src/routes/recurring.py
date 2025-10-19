"""
Recurring Transactions Routes

Flask blueprint for recurring transaction management and monitoring.

Created: 2025-10-19
Author: Saeed Hoss
"""

from flask import Blueprint, render_template, jsonify, request, current_app
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from services.recurring_manager import RecurringManager
from services.recurring_detector import RecurringDetector

recurring_bp = Blueprint('recurring', __name__, url_prefix='/recurring')


@recurring_bp.route('/')
def recurring_page():
    """Display the recurring transactions management page."""
    return render_template('recurring.html', app_name='Financial Assistant')


@recurring_bp.route('/api/all')
def get_all_recurring():
    """Get all recurring transactions."""
    try:
        status = request.args.get('status')
        
        manager = RecurringManager(current_app.config['DATABASE'])
        recurring_list = manager.get_all(status=status)
        
        return jsonify({
            'success': True,
            'recurring_transactions': recurring_list
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@recurring_bp.route('/api/stats')
def get_recurring_stats():
    """Get recurring transaction statistics."""
    try:
        manager = RecurringManager(current_app.config['DATABASE'])
        stats = manager.get_statistics()
        
        return jsonify({
            'success': True,
            'stats': stats
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@recurring_bp.route('/api/upcoming')
def get_upcoming_recurring():
    """Get upcoming recurring transactions."""
    try:
        days = request.args.get('days', default=30, type=int)
        
        manager = RecurringManager(current_app.config['DATABASE'])
        upcoming = manager.get_upcoming(days=days)
        
        return jsonify({
            'success': True,
            'upcoming': upcoming
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@recurring_bp.route('/api/alerts')
def get_recurring_alerts():
    """Get all recurring transaction alerts."""
    try:
        manager = RecurringManager(current_app.config['DATABASE'])
        alerts = manager.get_all_alerts()
        
        return jsonify({
            'success': True,
            'alerts': alerts
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@recurring_bp.route('/api/scan', methods=['POST'])
def scan_for_patterns():
    """Scan transactions and detect recurring patterns."""
    try:
        account_id = request.json.get('account_id') if request.json else None
        min_confidence = request.json.get('min_confidence', 0.75) if request.json else 0.75
        
        detector = RecurringDetector(current_app.config['DATABASE'])
        result = detector.scan_and_save_all(account_id=account_id)
        
        return jsonify({
            'success': True,
            **result
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@recurring_bp.route('/api/<int:recurring_id>', methods=['GET'])
def get_recurring(recurring_id):
    """Get a specific recurring transaction with its instances."""
    try:
        manager = RecurringManager(current_app.config['DATABASE'])
        recurring = manager.get_by_id(recurring_id)
        
        if not recurring:
            return jsonify({'success': False, 'error': 'Not found'}), 404
        
        # Get instances
        instances = manager.get_instances(recurring_id, limit=12)
        
        return jsonify({
            'success': True,
            'recurring': recurring,
            'instances': instances
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@recurring_bp.route('/api/<int:recurring_id>', methods=['PUT'])
def update_recurring(recurring_id):
    """Update a recurring transaction."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        manager = RecurringManager(current_app.config['DATABASE'])
        success = manager.update(recurring_id, data)
        
        if not success:
            return jsonify({'success': False, 'error': 'Not found'}), 404
        
        return jsonify({'success': True, 'message': 'Updated successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@recurring_bp.route('/api/<int:recurring_id>', methods=['DELETE'])
def delete_recurring(recurring_id):
    """Delete a recurring transaction."""
    try:
        manager = RecurringManager(current_app.config['DATABASE'])
        success = manager.delete(recurring_id)
        
        if not success:
            return jsonify({'success': False, 'error': 'Not found'}), 404
        
        return jsonify({'success': True, 'message': 'Deleted successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@recurring_bp.route('/api/<int:recurring_id>/pause', methods=['POST'])
def pause_recurring(recurring_id):
    """Pause a recurring transaction."""
    try:
        manager = RecurringManager(current_app.config['DATABASE'])
        success = manager.pause(recurring_id)
        
        if not success:
            return jsonify({'success': False, 'error': 'Not found'}), 404
        
        return jsonify({'success': True, 'message': 'Paused successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@recurring_bp.route('/api/<int:recurring_id>/resume', methods=['POST'])
def resume_recurring(recurring_id):
    """Resume a paused recurring transaction."""
    try:
        manager = RecurringManager(current_app.config['DATABASE'])
        success = manager.resume(recurring_id)
        
        if not success:
            return jsonify({'success': False, 'error': 'Not found'}), 404
        
        return jsonify({'success': True, 'message': 'Resumed successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

