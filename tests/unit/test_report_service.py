"""
Unit tests for ReportService
"""

import pytest
import sqlite3
from datetime import date, timedelta
from src.services.report_service import ReportService


@pytest.fixture
def report_service(app):
    """Create a ReportService instance with test database"""
    return ReportService(app.config['DATABASE'])


@pytest.fixture
def sample_data(app):
    """Insert sample transaction data for testing"""
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()
    
    # Create test account
    cursor.execute("""
        INSERT INTO accounts (name, type, institution)
        VALUES ('Test Checking', 'checking', 'Test Bank')
    """)
    account_id = cursor.lastrowid
    
    # Create test categories
    cursor.execute("INSERT INTO categories (name, type, level) VALUES ('Groceries', 'expense', 1)")
    groceries_id = cursor.lastrowid
    
    cursor.execute("INSERT INTO categories (name, type, level) VALUES ('Salary', 'income', 1)")
    salary_id = cursor.lastrowid
    
    cursor.execute("INSERT INTO categories (name, type, level) VALUES ('Rent', 'expense', 1)")
    rent_id = cursor.lastrowid
    
    # Insert transactions for the last 3 months
    today = date.today()
    
    # Month 1 - two months ago
    month1 = today.replace(day=1) - timedelta(days=60)
    cursor.execute("""
        INSERT INTO transactions (account_id, date, description, amount, category_id)
        VALUES (?, ?, 'Salary', 5000.00, ?)
    """, (account_id, month1.strftime('%Y-%m-%d'), salary_id))
    
    cursor.execute("""
        INSERT INTO transactions (account_id, date, description, amount, category_id)
        VALUES (?, ?, 'Groceries', -500.00, ?)
    """, (account_id, month1.strftime('%Y-%m-%d'), groceries_id))
    
    cursor.execute("""
        INSERT INTO transactions (account_id, date, description, amount, category_id)
        VALUES (?, ?, 'Rent', -2000.00, ?)
    """, (account_id, month1.strftime('%Y-%m-%d'), rent_id))
    
    # Month 2 - one month ago
    month2 = today.replace(day=1) - timedelta(days=30)
    cursor.execute("""
        INSERT INTO transactions (account_id, date, description, amount, category_id)
        VALUES (?, ?, 'Salary', 5000.00, ?)
    """, (account_id, month2.strftime('%Y-%m-%d'), salary_id))
    
    cursor.execute("""
        INSERT INTO transactions (account_id, date, description, amount, category_id)
        VALUES (?, ?, 'Groceries', -600.00, ?)
    """, (account_id, month2.strftime('%Y-%m-%d'), groceries_id))
    
    cursor.execute("""
        INSERT INTO transactions (account_id, date, description, amount, category_id)
        VALUES (?, ?, 'Rent', -2000.00, ?)
    """, (account_id, month2.strftime('%Y-%m-%d'), rent_id))
    
    # Month 3 - current month
    month3 = today.replace(day=5)
    cursor.execute("""
        INSERT INTO transactions (account_id, date, description, amount, category_id)
        VALUES (?, ?, 'Salary', 5000.00, ?)
    """, (account_id, month3.strftime('%Y-%m-%d'), salary_id))
    
    cursor.execute("""
        INSERT INTO transactions (account_id, date, description, amount, category_id)
        VALUES (?, ?, 'Groceries', -550.00, ?)
    """, (account_id, month3.strftime('%Y-%m-%d'), groceries_id))
    
    # Uncategorized transaction
    cursor.execute("""
        INSERT INTO transactions (account_id, date, description, amount, category_id)
        VALUES (?, ?, 'Unknown Charge', -100.00, NULL)
    """, (account_id, month3.strftime('%Y-%m-%d'),))
    
    conn.commit()
    conn.close()
    
    return account_id


class TestMonthlyIncomeExpenses:
    """Tests for get_monthly_income_expenses method"""
    
    def test_basic_monthly_data(self, report_service, sample_data):
        """Test getting monthly income and expenses"""
        data = report_service.get_monthly_income_expenses()
        
        assert len(data) >= 2  # At least 2 months of data
        
        # Check data structure
        for month_data in data:
            assert 'month' in month_data
            assert 'income' in month_data
            assert 'expenses' in month_data
            assert 'net' in month_data
            assert month_data['net'] == month_data['income'] - month_data['expenses']
    
    def test_filtered_by_account(self, report_service, sample_data, app):
        """Test filtering by account"""
        # Create another account with no transactions
        conn = sqlite3.connect(app.config['DATABASE'])
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO accounts (name, type, institution)
            VALUES ('Empty Account', 'savings', 'Test Bank')
        """)
        empty_account_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Get data for account with transactions
        data_with_txns = report_service.get_monthly_income_expenses(account_id=sample_data)
        assert len(data_with_txns) >= 2
        
        # Get data for empty account
        data_empty = report_service.get_monthly_income_expenses(account_id=empty_account_id)
        assert len(data_empty) == 0
    
    def test_filtered_by_date_range(self, report_service, sample_data):
        """Test filtering by date range"""
        today = date.today()
        start = today.replace(day=1) - timedelta(days=30)  # One month ago
        end = today
        
        data = report_service.get_monthly_income_expenses(start_date=start, end_date=end)
        
        # Should have at most 2 months
        assert len(data) <= 2


class TestCategoryBreakdown:
    """Tests for get_category_breakdown method"""
    
    def test_category_breakdown(self, report_service, sample_data):
        """Test getting category breakdown"""
        data = report_service.get_category_breakdown()
        
        assert len(data) >= 3  # Groceries, Rent, Uncategorized
        
        # Check data structure
        for category_data in data:
            assert 'category' in category_data
            assert 'amount' in category_data
            assert 'percentage' in category_data
            assert 'transaction_count' in category_data
            assert category_data['amount'] >= 0
            assert 0 <= category_data['percentage'] <= 100
    
    def test_percentages_sum_to_100(self, report_service, sample_data):
        """Test that percentages sum to approximately 100"""
        data = report_service.get_category_breakdown()
        
        total_percentage = sum(cat['percentage'] for cat in data)
        assert 99.0 <= total_percentage <= 101.0  # Allow for rounding
    
    def test_uncategorized_transactions(self, report_service, sample_data):
        """Test that uncategorized transactions are included"""
        data = report_service.get_category_breakdown()
        
        uncategorized = [cat for cat in data if cat['category'] == 'Uncategorized']
        assert len(uncategorized) == 1
        assert uncategorized[0]['amount'] > 0


class TestMonthlyCategoryTrends:
    """Tests for get_monthly_category_trends method"""
    
    def test_monthly_trends_structure(self, report_service, sample_data):
        """Test monthly category trends data structure"""
        data = report_service.get_monthly_category_trends()
        
        assert 'months' in data
        assert 'categories' in data
        assert isinstance(data['months'], list)
        assert isinstance(data['categories'], dict)
        
        # Check that each category has values for each month
        for category, values in data['categories'].items():
            assert len(values) == len(data['months'])
            assert all(isinstance(v, (int, float)) for v in values)
    
    def test_top_n_categories(self, report_service, sample_data):
        """Test limiting to top N categories"""
        data = report_service.get_monthly_category_trends(top_n=2)
        
        # Should have at most 2 categories
        assert len(data['categories']) <= 2


class TestTopCategories:
    """Tests for get_top_categories method"""
    
    def test_top_categories(self, report_service, sample_data):
        """Test getting top categories"""
        data = report_service.get_top_categories(limit=5)
        
        assert len(data) <= 5
        
        # Check data structure
        for category_data in data:
            assert 'category' in category_data
            assert 'amount' in category_data
            assert 'transaction_count' in category_data
            assert 'avg_per_transaction' in category_data
            
            # Check average calculation
            expected_avg = category_data['amount'] / category_data['transaction_count']
            assert abs(category_data['avg_per_transaction'] - expected_avg) < 0.01
    
    def test_top_categories_ordered(self, report_service, sample_data):
        """Test that categories are ordered by amount descending"""
        data = report_service.get_top_categories()
        
        amounts = [cat['amount'] for cat in data]
        assert amounts == sorted(amounts, reverse=True)


class TestEmptyData:
    """Tests for handling empty data"""
    
    def test_no_transactions(self, report_service):
        """Test methods with no transactions"""
        # Monthly income/expenses
        income_expenses = report_service.get_monthly_income_expenses()
        assert income_expenses == []
        
        # Category breakdown
        categories = report_service.get_category_breakdown()
        assert categories == []
        
        # Monthly trends
        trends = report_service.get_monthly_category_trends()
        assert trends['months'] == []
        assert trends['categories'] == {}
        
        # Top categories
        top = report_service.get_top_categories()
        assert top == []

