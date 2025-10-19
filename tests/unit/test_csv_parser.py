"""
Unit tests for CSV Parser Service.
"""

import pytest
from datetime import date
from src.services.csv_parser import CSVParser, CSVParseError
import os


class TestCSVParser:
    """Test cases for CSV Parser Service."""
    
    @pytest.fixture
    def parser(self):
        """Create a CSV parser instance."""
        return CSVParser()
    
    @pytest.fixture
    def fixtures_dir(self):
        """Get the fixtures directory path."""
        return os.path.join(os.path.dirname(__file__), '..', 'fixtures', 'sample_statements')
    
    def test_parse_standard_csv(self, parser, fixtures_dir):
        """Test parsing standard CSV format."""
        file_path = os.path.join(fixtures_dir, 'standard_format.csv')
        transactions = parser.parse_file(file_path)
        
        assert len(transactions) == 4
        
        # Check first transaction
        assert transactions[0]['date'] == date(2025, 10, 19)
        assert transactions[0]['description'] == 'Grocery Store'
        assert transactions[0]['amount'] == -45.50
        assert transactions[0]['balance'] == 1234.50
        
        # Check second transaction
        assert transactions[1]['date'] == date(2025, 10, 20)
        assert transactions[1]['description'] == 'Salary Deposit'
        assert transactions[1]['amount'] == 2500.00
        assert transactions[1]['balance'] == 3734.50
    
    def test_parse_debit_credit_columns(self, parser, fixtures_dir):
        """Test parsing CSV with separate debit/credit columns."""
        file_path = os.path.join(fixtures_dir, 'debit_credit_format.csv')
        transactions = parser.parse_file(file_path)
        
        assert len(transactions) == 4
        
        # Debit should be negative
        assert transactions[0]['amount'] == -45.50
        
        # Credit should be positive
        assert transactions[1]['amount'] == 2500.00
        
        # Another debit
        assert transactions[2]['amount'] == -1200.00
    
    def test_parse_semicolon_delimiter(self, parser, fixtures_dir):
        """Test parsing CSV with semicolon delimiter."""
        file_path = os.path.join(fixtures_dir, 'semicolon_delimiter.csv')
        transactions = parser.parse_file(file_path)
        
        assert len(transactions) == 3
        assert transactions[0]['description'] == 'Grocery Store'
        assert transactions[0]['amount'] == -45.50
    
    def test_parse_tab_delimiter(self, parser, fixtures_dir):
        """Test parsing CSV with tab delimiter."""
        file_path = os.path.join(fixtures_dir, 'tab_delimiter.csv')
        transactions = parser.parse_file(file_path)
        
        assert len(transactions) == 3
        assert transactions[0]['description'] == 'Grocery Store'
        assert transactions[0]['amount'] == -45.50
    
    def test_parse_european_format(self, parser, fixtures_dir):
        """Test parsing European number format (comma as decimal separator)."""
        file_path = os.path.join(fixtures_dir, 'european_format.csv')
        transactions = parser.parse_file(file_path)
        
        assert len(transactions) == 3
        
        # European format: 1.234,56 = 1234.56
        assert transactions[0]['amount'] == -1234.56
        
        # European format: 2.500,00 = 2500.00
        assert transactions[1]['amount'] == 2500.00
        
        # European format: 45,50 = 45.50
        assert transactions[2]['amount'] == -45.50
    
    def test_parse_accounting_format(self, parser, fixtures_dir):
        """Test parsing accounting format with parentheses for negative."""
        file_path = os.path.join(fixtures_dir, 'accounting_format.csv')
        transactions = parser.parse_file(file_path)
        
        assert len(transactions) == 3
        
        # (45.50) should be negative
        assert transactions[0]['amount'] == -45.50
        
        # Regular positive
        assert transactions[1]['amount'] == 2500.00
        
        # (1200.00) should be negative
        assert transactions[2]['amount'] == -1200.00
    
    def test_parse_various_date_formats(self, parser, fixtures_dir):
        """Test parsing various date formats."""
        file_path = os.path.join(fixtures_dir, 'standard_format.csv')
        transactions = parser.parse_file(file_path)
        
        # MM/DD/YYYY format
        assert transactions[0]['date'] == date(2025, 10, 19)
        
        # Also test with debit_credit format (YYYY-MM-DD)
        file_path2 = os.path.join(fixtures_dir, 'debit_credit_format.csv')
        transactions2 = parser.parse_file(file_path2)
        
        # YYYY-MM-DD format
        assert transactions2[0]['date'] == date(2025, 10, 19)
        
        # Also test with semicolon format (DD/MM/YYYY)
        file_path3 = os.path.join(fixtures_dir, 'semicolon_delimiter.csv')
        transactions3 = parser.parse_file(file_path3)
        
        # DD/MM/YYYY format (with dayfirst=True fallback)
        assert transactions3[0]['date'] == date(2025, 10, 19)
    
    def test_empty_file(self, parser, fixtures_dir):
        """Test parsing empty CSV file."""
        file_path = os.path.join(fixtures_dir, 'empty.csv')
        
        with pytest.raises(CSVParseError) as exc_info:
            parser.parse_file(file_path)
        
        assert "empty" in str(exc_info.value).lower() or "no valid transactions" in str(exc_info.value).lower()
    
    def test_file_not_found(self, parser):
        """Test error handling for missing file."""
        with pytest.raises(CSVParseError) as exc_info:
            parser.parse_file("nonexistent_file.csv")
        
        assert "not found" in str(exc_info.value).lower()
    
    def test_invalid_csv_format(self, parser, tmp_path):
        """Test error handling for invalid CSV format."""
        # Create invalid CSV file
        invalid_file = tmp_path / "invalid.csv"
        invalid_file.write_text("This is not a valid CSV\nNo structure here")
        
        with pytest.raises(CSVParseError) as exc_info:
            parser.parse_file(str(invalid_file))
        
        # Should fail because it can't find required columns
        assert "date column" in str(exc_info.value).lower() or "description column" in str(exc_info.value).lower()
    
    def test_missing_date_column(self, parser, tmp_path):
        """Test error handling when date column is missing."""
        csv_file = tmp_path / "no_date.csv"
        csv_file.write_text("Description,Amount\nTest Transaction,100.00\n")
        
        with pytest.raises(CSVParseError) as exc_info:
            parser.parse_file(str(csv_file))
        
        assert "date column" in str(exc_info.value).lower()
    
    def test_missing_description_column(self, parser, tmp_path):
        """Test error handling when description column is missing."""
        csv_file = tmp_path / "no_description.csv"
        csv_file.write_text("Date,Amount\n10/19/2025,100.00\n")
        
        with pytest.raises(CSVParseError) as exc_info:
            parser.parse_file(str(csv_file))
        
        assert "description column" in str(exc_info.value).lower()
    
    def test_missing_amount_columns(self, parser, tmp_path):
        """Test error handling when amount columns are missing."""
        csv_file = tmp_path / "no_amount.csv"
        csv_file.write_text("Date,Description\n10/19/2025,Test Transaction\n")
        
        with pytest.raises(CSVParseError) as exc_info:
            parser.parse_file(str(csv_file))
        
        assert "amount column" in str(exc_info.value).lower()
    
    def test_raw_data_preserved(self, parser, fixtures_dir):
        """Test that raw row data is preserved."""
        file_path = os.path.join(fixtures_dir, 'standard_format.csv')
        transactions = parser.parse_file(file_path)
        
        # Check that raw_data exists and contains the original columns
        assert 'raw_data' in transactions[0]
        assert 'Date' in transactions[0]['raw_data']
        assert 'Description' in transactions[0]['raw_data']
        assert 'Amount' in transactions[0]['raw_data']
    
    def test_case_insensitive_columns(self, parser, tmp_path):
        """Test that column detection is case-insensitive."""
        csv_file = tmp_path / "mixed_case.csv"
        csv_file.write_text("DATE,DESCRIPTION,amount\n10/19/2025,Test,100.00\n")
        
        transactions = parser.parse_file(str(csv_file))
        
        assert len(transactions) == 1
        assert transactions[0]['description'] == 'Test'
    
    def test_parse_amount_with_currency_symbols(self, parser):
        """Test parsing amounts with currency symbols."""
        assert parser._parse_amount("$100.00") == 100.00
        assert parser._parse_amount("£50.50") == 50.50
        assert parser._parse_amount("€75.25") == 75.25
        assert parser._parse_amount("¥1000") == 1000.00
    
    def test_parse_amount_with_thousands_separator(self, parser):
        """Test parsing amounts with thousands separators."""
        assert parser._parse_amount("1,234.56") == 1234.56
        assert parser._parse_amount("$1,234.56") == 1234.56
        assert parser._parse_amount("12,345.67") == 12345.67
    
    def test_parse_negative_amounts(self, parser):
        """Test parsing negative amounts."""
        assert parser._parse_amount("-100.00") == -100.00
        assert parser._parse_amount("(100.00)") == -100.00
        assert parser._parse_amount("($100.00)") == -100.00
    
    def test_parse_amount_handles_nan(self, parser):
        """Test parsing NaN/empty values."""
        import pandas as pd
        assert parser._parse_amount(pd.NA) == 0.0
        assert parser._parse_amount("") == 0.0
        assert parser._parse_amount("   ") == 0.0
    
    def test_column_detection(self, parser):
        """Test column name detection patterns."""
        import pandas as pd
        
        # Test date column detection
        df = pd.DataFrame({'Transaction Date': [], 'Description': [], 'Amount': []})
        column_map = parser._detect_columns(df)
        assert 'date' in column_map
        assert column_map['date'] == 'Transaction Date'
        
        # Test description column detection
        df = pd.DataFrame({'Date': [], 'Merchant': [], 'Amount': []})
        column_map = parser._detect_columns(df)
        assert 'description' in column_map
        assert column_map['description'] == 'Merchant'
        
        # Test debit/credit detection
        df = pd.DataFrame({'Date': [], 'Description': [], 'Debit': [], 'Credit': []})
        column_map = parser._detect_columns(df)
        assert 'debit' in column_map
        assert 'credit' in column_map

