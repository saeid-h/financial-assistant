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

