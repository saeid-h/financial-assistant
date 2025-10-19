"""
Reports Blueprint
Handles routes for financial reports and visualizations
"""

from flask import Blueprint, render_template, jsonify, request, current_app
from datetime import datetime, date

reports_bp = Blueprint('reports', __name__, url_prefix='/reports')


@reports_bp.route('/')
def reports_page():
    """Display the reports page with charts"""
    return render_template('reports.html')

