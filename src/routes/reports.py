"""
Reports Blueprint
Handles routes for financial reports and visualizations
"""

from flask import Blueprint, render_template, jsonify, request, current_app, make_response
from datetime import datetime, date
from io import StringIO
import csv
import sys
import os

# Add src directory to path if needed
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from services.report_service import ReportService

reports_bp = Blueprint('reports', __name__, url_prefix='/reports')


def _parse_date(date_str):
    """Parse date string to date object"""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return None


@reports_bp.route('/')
def reports_page():
    """Display the reports page with charts"""
    return render_template('reports.html')


@reports_bp.route('/api/income-expenses')
def get_income_expenses_data():
    """Get monthly income vs expenses data for line chart"""
    account_id = request.args.get('account_id', type=int)
    start_date = _parse_date(request.args.get('start_date'))
    end_date = _parse_date(request.args.get('end_date'))
    
    report_service = ReportService(current_app.config['DATABASE'])
    data = report_service.get_monthly_income_expenses(
        account_id=account_id,
        start_date=start_date,
        end_date=end_date
    )
    
    # Format for Chart.js line chart
    return jsonify({
        'labels': [d['month'] for d in data],
        'datasets': [
            {
                'label': 'Income',
                'data': [d['income'] for d in data],
                'borderColor': '#28a745',
                'backgroundColor': 'rgba(40, 167, 69, 0.1)',
                'tension': 0.4,
                'fill': True
            },
            {
                'label': 'Expenses',
                'data': [d['expenses'] for d in data],
                'borderColor': '#dc3545',
                'backgroundColor': 'rgba(220, 53, 69, 0.1)',
                'tension': 0.4,
                'fill': True
            },
            {
                'label': 'Net',
                'data': [d['net'] for d in data],
                'borderColor': '#007bff',
                'backgroundColor': 'rgba(0, 123, 255, 0.1)',
                'borderDash': [5, 5],
                'tension': 0.4,
                'fill': False
            }
        ]
    })


@reports_bp.route('/api/category-breakdown')
def get_category_breakdown_data():
    """Get category breakdown for pie chart"""
    account_id = request.args.get('account_id', type=int)
    start_date = _parse_date(request.args.get('start_date'))
    end_date = _parse_date(request.args.get('end_date'))
    
    report_service = ReportService(current_app.config['DATABASE'])
    data = report_service.get_category_breakdown(
        account_id=account_id,
        start_date=start_date,
        end_date=end_date
    )
    
    # Color palette for categories
    colors = [
        '#667eea', '#764ba2', '#f093fb', '#4facfe',
        '#43e97b', '#fa709a', '#fee140', '#30cfd0',
        '#a8edea', '#fed6e3', '#c471f5', '#fa709a'
    ]
    
    # Format for Chart.js pie chart
    return jsonify({
        'labels': [d['category'] for d in data],
        'datasets': [{
            'data': [d['amount'] for d in data],
            'backgroundColor': colors[:len(data)],
            'borderWidth': 2,
            'borderColor': '#fff'
        }]
    })


@reports_bp.route('/api/monthly-category-trends')
def get_monthly_category_trends_data():
    """Get monthly category trends for stacked bar chart"""
    account_id = request.args.get('account_id', type=int)
    start_date = _parse_date(request.args.get('start_date'))
    end_date = _parse_date(request.args.get('end_date'))
    
    report_service = ReportService(current_app.config['DATABASE'])
    data = report_service.get_monthly_category_trends(
        account_id=account_id,
        start_date=start_date,
        end_date=end_date,
        top_n=10
    )
    
    # Color palette for categories (same as pie chart for consistency)
    colors = [
        '#667eea', '#764ba2', '#f093fb', '#4facfe',
        '#43e97b', '#fa709a', '#fee140', '#30cfd0',
        '#a8edea', '#fed6e3'
    ]
    
    # Format for Chart.js stacked bar chart
    datasets = []
    for idx, (category, amounts) in enumerate(data['categories'].items()):
        datasets.append({
            'label': category,
            'data': amounts,
            'backgroundColor': colors[idx % len(colors)],
            'borderColor': colors[idx % len(colors)],
            'borderWidth': 1
        })
    
    return jsonify({
        'labels': data['months'],
        'datasets': datasets
    })


@reports_bp.route('/api/top-categories')
def get_top_categories_data():
    """Get top spending categories for horizontal bar chart"""
    account_id = request.args.get('account_id', type=int)
    start_date = _parse_date(request.args.get('start_date'))
    end_date = _parse_date(request.args.get('end_date'))
    limit = request.args.get('limit', 10, type=int)
    
    report_service = ReportService(current_app.config['DATABASE'])
    data = report_service.get_top_categories(
        account_id=account_id,
        start_date=start_date,
        end_date=end_date,
        limit=limit
    )
    
    # Format for Chart.js horizontal bar chart
    return jsonify({
        'labels': [d['category'] for d in data],
        'datasets': [{
            'label': 'Total Spending',
            'data': [d['amount'] for d in data],
            'backgroundColor': '#667eea',
            'borderColor': '#764ba2',
            'borderWidth': 1
        }],
        'metadata': {
            'transaction_counts': [d['transaction_count'] for d in data],
            'averages': [d['avg_per_transaction'] for d in data]
        }
    })


@reports_bp.route('/api/export')
def export_report_data():
    """Export all report data as CSV"""
    account_id = request.args.get('account_id', type=int)
    start_date = _parse_date(request.args.get('start_date'))
    end_date = _parse_date(request.args.get('end_date'))
    
    report_service = ReportService(current_app.config['DATABASE'])
    
    # Get all data
    income_expenses = report_service.get_monthly_income_expenses(
        account_id, start_date, end_date)
    category_breakdown = report_service.get_category_breakdown(
        account_id, start_date, end_date)
    top_categories = report_service.get_top_categories(
        account_id, start_date, end_date)
    
    # Build CSV
    output = StringIO()
    writer = csv.writer(output)
    
    # Metadata
    writer.writerow(['Financial Report'])
    writer.writerow(['Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
    if account_id:
        writer.writerow(['Account ID:', account_id])
    if start_date:
        writer.writerow(['Start Date:', start_date.strftime('%Y-%m-%d')])
    if end_date:
        writer.writerow(['End Date:', end_date.strftime('%Y-%m-%d')])
    writer.writerow([])
    
    # Section 1: Monthly Income vs Expenses
    writer.writerow(['Monthly Income vs Expenses'])
    writer.writerow(['Month', 'Income', 'Expenses', 'Net'])
    for row in income_expenses:
        writer.writerow([
            row['month'],
            f"{row['income']:.2f}",
            f"{row['expenses']:.2f}",
            f"{row['net']:.2f}"
        ])
    writer.writerow([])
    
    # Section 2: Category Breakdown
    writer.writerow(['Category Breakdown'])
    writer.writerow(['Category', 'Amount', 'Percentage', 'Transactions'])
    for row in category_breakdown:
        writer.writerow([
            row['category'],
            f"{row['amount']:.2f}",
            f"{row['percentage']:.1f}%",
            row['transaction_count']
        ])
    writer.writerow([])
    
    # Section 3: Top Categories
    writer.writerow(['Top Spending Categories'])
    writer.writerow(['Category', 'Total', 'Transactions', 'Avg per Transaction'])
    for row in top_categories:
        writer.writerow([
            row['category'],
            f"{row['amount']:.2f}",
            row['transaction_count'],
            f"{row['avg_per_transaction']:.2f}"
        ])
    
    # Create response
    output.seek(0)
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv'
    
    # Generate filename
    date_str = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'financial_report_{date_str}.csv'
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'
    
    return response


# ============================================================================
# NEW ENHANCED REPORTS - Phase 3+
# ============================================================================

@reports_bp.route('/month-comparison')
def month_comparison_page():
    """Display month-over-month comparison report page"""
    return render_template('reports_month_comparison.html')


@reports_bp.route('/api/month-comparison')
def get_month_comparison_data():
    """Get side-by-side comparison of two months"""
    month1 = request.args.get('month1')  # YYYY-MM
    month2 = request.args.get('month2')  # YYYY-MM
    
    if not month1 or not month2:
        return jsonify({'success': False, 'error': 'Both months required'}), 400
    
    import sqlite3
    from collections import defaultdict
    
    conn = sqlite3.connect(current_app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        # Get data for month 1
        cursor.execute("""
            SELECT c.name as category, SUM(ABS(t.amount)) as total
            FROM transactions t
            LEFT JOIN categories c ON t.category_id = c.id
            WHERE strftime('%Y-%m', t.date) = ?
              AND t.amount < 0
              AND (c.type IS NULL OR c.type != 'transfer')
            GROUP BY c.name
        """, (month1,))
        
        month1_data = {row['category'] or 'Uncategorized': row['total'] for row in cursor.fetchall()}
        
        # Get data for month 2
        cursor.execute("""
            SELECT c.name as category, SUM(ABS(t.amount)) as total
            FROM transactions t
            LEFT JOIN categories c ON t.category_id = c.id
            WHERE strftime('%Y-%m', t.date) = ?
              AND t.amount < 0
              AND (c.type IS NULL OR c.type != 'transfer')
            GROUP BY c.name
        """, (month2,))
        
        month2_data = {row['category'] or 'Uncategorized': row['total'] for row in cursor.fetchall()}
        
        # Combine categories
        all_categories = set(month1_data.keys()) | set(month2_data.keys())
        
        comparison = []
        for category in sorted(all_categories):
            m1_amount = month1_data.get(category, 0.0)
            m2_amount = month2_data.get(category, 0.0)
            variance = m2_amount - m1_amount
            variance_pct = (variance / m1_amount * 100) if m1_amount > 0 else 0
            
            comparison.append({
                'category': category,
                'month1_amount': round(m1_amount, 2),
                'month2_amount': round(m2_amount, 2),
                'variance': round(variance, 2),
                'variance_percent': round(variance_pct, 1)
            })
        
        # Calculate totals
        total_m1 = sum(month1_data.values())
        total_m2 = sum(month2_data.values())
        total_variance = total_m2 - total_m1
        total_variance_pct = (total_variance / total_m1 * 100) if total_m1 > 0 else 0
        
        conn.close()
        
        return jsonify({
            'success': True,
            'month1': month1,
            'month2': month2,
            'comparison': comparison,
            'totals': {
                'month1': round(total_m1, 2),
                'month2': round(total_m2, 2),
                'variance': round(total_variance, 2),
                'variance_percent': round(total_variance_pct, 1)
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@reports_bp.route('/merchants')
def merchants_page():
    """Display merchant analysis report page"""
    return render_template('reports_merchants.html')


@reports_bp.route('/api/merchants')
def get_merchant_data():
    """Get merchant analysis data"""
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    limit = request.args.get('limit', default=50, type=int)
    
    import sqlite3
    from collections import defaultdict
    
    conn = sqlite3.connect(current_app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        query = """
            SELECT description, amount, date
            FROM transactions
            WHERE 1=1
        """
        params = []
        
        if date_from:
            query += " AND date >= ?"
            params.append(date_from)
        
        if date_to:
            query += " AND date <= ?"
            params.append(date_to)
        
        query += " ORDER BY description"
        
        cursor.execute(query, params)
        transactions = cursor.fetchall()
        
        # Group by merchant (extract merchant name)
        from services.recurring_detector import RecurringDetector
        detector = RecurringDetector(current_app.config['DATABASE'])
        
        merchants = defaultdict(list)
        for txn in transactions:
            merchant = detector.extract_merchant_name(txn['description'])
            merchants[merchant].append(dict(txn))
        
        # Calculate merchant stats
        merchant_stats = []
        for merchant, txns in merchants.items():
            amounts = [abs(t['amount']) for t in txns]
            dates = [t['date'] for t in txns]
            
            merchant_stats.append({
                'merchant': merchant,
                'total_spent': round(sum(amounts), 2),
                'transaction_count': len(txns),
                'average_transaction': round(sum(amounts) / len(amounts), 2),
                'first_seen': min(dates),
                'last_seen': max(dates)
            })
        
        # Sort by total spent
        merchant_stats.sort(key=lambda x: x['total_spent'], reverse=True)
        
        # Limit results
        merchant_stats = merchant_stats[:limit]
        
        conn.close()
        
        return jsonify({
            'success': True,
            'merchants': merchant_stats,
            'total_merchants': len(merchant_stats)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@reports_bp.route('/net-worth')
def net_worth_page():
    """Display net worth tracker page"""
    return render_template('reports_net_worth.html')


@reports_bp.route('/api/net-worth')
def get_net_worth_data():
    """Get net worth trajectory over time"""
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    
    import sqlite3
    from datetime import datetime, timedelta
    from dateutil.relativedelta import relativedelta
    
    conn = sqlite3.connect(current_app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        # Get all accounts with their reference balances
        cursor.execute("""
            SELECT id, name, initial_balance, reference_date
            FROM accounts
        """)
        accounts = cursor.fetchall()
        
        # Determine date range
        if not date_from:
            # Get earliest reference date
            cursor.execute("SELECT MIN(reference_date) as min_date FROM accounts WHERE reference_date IS NOT NULL")
            result = cursor.fetchone()
            date_from = result['min_date'] if result['min_date'] else date.today().strftime('%Y-%m-%d')
        
        if not date_to:
            date_to = date.today().strftime('%Y-%m-%d')
        
        start = datetime.strptime(date_from, '%Y-%m-%d').date()
        end = datetime.strptime(date_to, '%Y-%m-%d').date()
        
        # Generate monthly snapshots
        snapshots = []
        current = start.replace(day=1)  # Start of month
        
        while current <= end:
            month_str = current.strftime('%Y-%m-%d')
            net_worth = 0
            
            for account in accounts:
                # Start with reference balance
                balance = account['initial_balance'] or 0
                
                # Add transactions up to this month
                cursor.execute("""
                    SELECT SUM(amount) as total
                    FROM transactions
                    WHERE account_id = ?
                      AND date <= ?
                """, (account['id'], month_str))
                
                result = cursor.fetchone()
                transaction_sum = result['total'] if result['total'] else 0
                balance += transaction_sum
                net_worth += balance
            
            snapshots.append({
                'date': current.strftime('%Y-%m'),
                'net_worth': round(net_worth, 2)
            })
            
            # Move to next month
            current = current + relativedelta(months=1)
        
        conn.close()
        
        # Calculate growth
        if len(snapshots) >= 2:
            start_worth = snapshots[0]['net_worth']
            end_worth = snapshots[-1]['net_worth']
            total_change = end_worth - start_worth
            months = len(snapshots) - 1
            avg_monthly_change = total_change / months if months > 0 else 0
        else:
            total_change = 0
            avg_monthly_change = 0
        
        return jsonify({
            'success': True,
            'snapshots': snapshots,
            'summary': {
                'current_net_worth': snapshots[-1]['net_worth'] if snapshots else 0,
                'start_net_worth': snapshots[0]['net_worth'] if snapshots else 0,
                'total_change': round(total_change, 2),
                'avg_monthly_change': round(avg_monthly_change, 2),
                'months_tracked': len(snapshots)
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@reports_bp.route('/builder')
def report_builder_page():
    """Display customizable report builder page"""
    return render_template('reports_builder.html')


@reports_bp.route('/api/custom', methods=['POST'])
def generate_custom_report():
    """Generate custom report based on user parameters"""
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'error': 'No parameters provided'}), 400
    
    metrics = data.get('metrics', ['total'])  # income, expenses, net, count, average
    grouping = data.get('grouping', 'category')  # category, merchant, account, date
    date_from = data.get('date_from')
    date_to = data.get('date_to')
    filters = data.get('filters', {})
    
    import sqlite3
    from collections import defaultdict
    
    conn = sqlite3.connect(current_app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        # Build dynamic query
        query = "SELECT t.*, c.name as category_name, a.name as account_name FROM transactions t "
        query += "LEFT JOIN categories c ON t.category_id = c.id "
        query += "LEFT JOIN accounts a ON t.account_id = a.id "
        query += "WHERE 1=1 "
        
        params = []
        
        if date_from:
            query += "AND t.date >= ? "
            params.append(date_from)
        
        if date_to:
            query += "AND t.date <= ? "
            params.append(date_to)
        
        if filters.get('account_id'):
            query += "AND t.account_id = ? "
            params.append(filters['account_id'])
        
        if filters.get('category_id'):
            query += "AND t.category_id = ? "
            params.append(filters['category_id'])
        
        cursor.execute(query, params)
        transactions = [dict(row) for row in cursor.fetchall()]
        
        # Group data
        groups = defaultdict(list)
        
        for txn in transactions:
            if grouping == 'category':
                key = txn['category_name'] or 'Uncategorized'
            elif grouping == 'merchant':
                from services.recurring_detector import RecurringDetector
                detector = RecurringDetector(current_app.config['DATABASE'])
                key = detector.extract_merchant_name(txn['description'])
            elif grouping == 'account':
                key = txn['account_name']
            elif grouping == 'date':
                key = txn['date'][:7]  # YYYY-MM
            else:
                key = 'All'
            
            groups[key].append(txn)
        
        # Calculate metrics for each group
        results = []
        for group_name, txns in groups.items():
            metric_values = {}
            
            if 'total' in metrics or 'income' in metrics or 'expenses' in metrics:
                income = sum(t['amount'] for t in txns if t['amount'] > 0)
                expenses = sum(abs(t['amount']) for t in txns if t['amount'] < 0)
                
                if 'income' in metrics:
                    metric_values['income'] = round(income, 2)
                if 'expenses' in metrics:
                    metric_values['expenses'] = round(expenses, 2)
                if 'total' in metrics:
                    metric_values['total'] = round(income + expenses, 2)
                if 'net' in metrics:
                    metric_values['net'] = round(income - expenses, 2)
            
            if 'count' in metrics:
                metric_values['count'] = len(txns)
            
            if 'average' in metrics:
                amounts = [abs(t['amount']) for t in txns]
                metric_values['average'] = round(sum(amounts) / len(amounts), 2) if amounts else 0
            
            results.append({
                'group': group_name,
                **metric_values
            })
        
        # Sort by first metric value
        if results:
            first_metric = list(results[0].keys())[1] if len(results[0]) > 1 else 'total'
            results.sort(key=lambda x: x.get(first_metric, 0), reverse=True)
        
        conn.close()
        
        return jsonify({
            'success': True,
            'results': results,
            'parameters': {
                'metrics': metrics,
                'grouping': grouping,
                'date_from': date_from,
                'date_to': date_to
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

