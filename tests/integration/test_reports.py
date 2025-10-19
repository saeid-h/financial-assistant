"""
Integration tests for reports functionality
"""

import pytest
from src.app import create_app


class TestReportsPage:
    """Tests for reports page structure and loading"""
    
    def test_reports_page_loads(self, client):
        """Test that reports page loads successfully"""
        response = client.get('/reports/')
        assert response.status_code == 200
        assert b'Financial Reports' in response.data
    
    def test_reports_includes_chartjs(self, client):
        """Test that Chart.js library is included"""
        response = client.get('/reports/')
        assert response.status_code == 200
        # Check for Chart.js CDN
        assert b'chart.js' in response.data or b'Chart.js' in response.data
    
    def test_reports_has_all_charts(self, client):
        """Test that all chart containers are present"""
        response = client.get('/reports/')
        assert response.status_code == 200
        
        # Check for all 4 chart canvas elements
        assert b'income-expense-chart' in response.data
        assert b'category-pie-chart' in response.data
        assert b'monthly-category-chart' in response.data
        assert b'top-categories-chart' in response.data
    
    def test_reports_has_filters(self, client):
        """Test that filter controls are present"""
        response = client.get('/reports/')
        assert response.status_code == 200
        
        # Check for filter controls
        assert b'date-range' in response.data
        assert b'account-filter' in response.data
        assert b'apply-filters' in response.data
        assert b'export-csv' in response.data
    
    def test_reports_has_date_range_options(self, client):
        """Test that date range dropdown has all options"""
        response = client.get('/reports/')
        assert response.status_code == 200
        
        # Check for date range options
        assert b'This Month' in response.data
        assert b'Last Month' in response.data
        assert b'Last 3 Months' in response.data
        assert b'Last 6 Months' in response.data
        assert b'Last 12 Months' in response.data
        assert b'This Year' in response.data
        assert b'Last Year' in response.data
        assert b'Custom Range' in response.data
    
    def test_reports_has_loading_states(self, client):
        """Test that loading indicators are present"""
        response = client.get('/reports/')
        assert response.status_code == 200
        
        # Check for loading indicators
        assert b'chart-loading' in response.data
        assert b'Loading chart' in response.data
    
    def test_reports_has_empty_states(self, client):
        """Test that empty state messages are present"""
        response = client.get('/reports/')
        assert response.status_code == 200
        
        # Check for empty state messages
        assert b'chart-empty' in response.data
        assert b'No data available' in response.data
    
    def test_reports_chart_containers_hidden_initially(self, client):
        """Test that chart containers are hidden on initial load"""
        response = client.get('/reports/')
        assert response.status_code == 200
        
        # Check that containers start hidden
        # They will be shown by JavaScript after data loads
        assert b'income-expense-container' in response.data
        assert b'style="display: none;"' in response.data


class TestReportsNavigation:
    """Tests for reports navigation"""
    
    def test_reports_link_in_navigation(self, client):
        """Test that Reports link is in the navigation"""
        response = client.get('/reports/')
        assert response.status_code == 200
        assert b'Reports' in response.data
    
    def test_reports_link_active_state(self, client):
        """Test that Reports link is marked active on reports page"""
        response = client.get('/reports/')
        assert response.status_code == 200
        # Check for active class on Reports link
        assert b'/reports' in response.data
        assert b'class="active"' in response.data

