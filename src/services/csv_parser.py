"""
CSV Parser Service for importing bank/credit card statements.

Handles various CSV formats with flexible column detection and date parsing.
"""

import pandas as pd
from datetime import datetime
from typing import List, Dict, Optional
from dateutil import parser as date_parser
import re


class CSVParseError(Exception):
    """Custom exception for CSV parsing errors."""
    pass


class CSVParser:
    """
    Flexible CSV parser for bank statement imports.
    
    Supports various formats with auto-detection of:
    - Delimiters (comma, semicolon, tab)
    - Date formats
    - Column names (case-insensitive)
    - Debit/Credit vs single Amount columns
    """
    
    # Common column name patterns (case-insensitive)
    DATE_COLUMNS = ['date', 'transaction date', 'posting date', 'trans date', 
                    'transaction_date', 'post date', 'value date']
    
    # Description columns in priority order - 'description' before 'details'
    DESCRIPTION_COLUMNS = ['description', 'merchant', 'payee', 'memo', 
                          'narrative', 'particulars', 'reference', 'details']
    
    # Columns to ignore (optional metadata)
    IGNORED_COLUMNS = ['status', 'member name', 'member', 'account holder',
                      'card number', 'reference number', 'ref', 'balance',
                      'type', 'check or slip #', 'check number', 'slip number']
    
    AMOUNT_COLUMNS = ['amount', 'transaction amount', 'value']
    
    DEBIT_COLUMNS = ['debit', 'withdrawal', 'withdrawals', 'debit amount',
                     'paid out', 'spend']
    
    CREDIT_COLUMNS = ['credit', 'deposit', 'deposits', 'credit amount',
                      'paid in', 'received']
    
    BALANCE_COLUMNS = ['balance', 'running balance', 'available balance',
                      'closing balance', 'current balance']
    
    def parse_file(self, file_path: str) -> List[Dict]:
        """
        Parse a CSV file and extract transactions.
        
        Args:
            file_path: Path to CSV file
        
        Returns:
            List of transaction dictionaries with standardized format:
            [
                {
                    'date': datetime.date,
                    'description': str,
                    'amount': float,  # negative for expenses
                    'balance': float or None,
                    'raw_data': dict  # original row data
                },
                ...
            ]
        
        Raises:
            CSVParseError: If file cannot be parsed or required fields missing
        """
        try:
            # Try to detect delimiter and read CSV
            df = self._read_csv_with_delimiter_detection(file_path)
            
            if df.empty:
                raise CSVParseError("CSV file is empty")
            
            # Detect column mappings
            column_map = self._detect_columns(df)
            
            # Validate required columns
            if not column_map.get('date'):
                raise CSVParseError("Could not find date column. Expected columns like: " + 
                                  ", ".join(self.DATE_COLUMNS))
            
            if not column_map.get('description'):
                raise CSVParseError("Could not find description column. Expected columns like: " + 
                                  ", ".join(self.DESCRIPTION_COLUMNS))
            
            if not column_map.get('amount') and not (column_map.get('debit') or column_map.get('credit')):
                raise CSVParseError("Could not find amount columns. Expected 'amount' column or 'debit'/'credit' columns")
            
            # Parse transactions
            transactions = []
            for index, row in df.iterrows():
                try:
                    transaction = self._parse_row(row, column_map)
                    if transaction:  # Skip rows that couldn't be parsed
                        transactions.append(transaction)
                except Exception as e:
                    # Log error but continue with other rows
                    print(f"Warning: Could not parse row {index + 1}: {str(e)}")
                    continue
            
            if not transactions:
                raise CSVParseError("No valid transactions found in CSV file")
            
            return transactions
        
        except pd.errors.EmptyDataError:
            raise CSVParseError("CSV file is empty or has no data")
        except pd.errors.ParserError as e:
            raise CSVParseError(f"Failed to parse CSV file: {str(e)}")
        except CSVParseError:
            raise
        except Exception as e:
            raise CSVParseError(f"Unexpected error parsing CSV: {str(e)}")
    
    def _read_csv_with_delimiter_detection(self, file_path: str) -> pd.DataFrame:
        """
        Read CSV with automatic delimiter detection.
        
        Tries common delimiters: comma, semicolon, tab
        """
        # Check if file exists first
        import os
        if not os.path.exists(file_path):
            raise CSVParseError(f"File not found: {file_path}")
        
        delimiters = [',', ';', '\t', '|']
        
        for delimiter in delimiters:
            try:
                df = pd.read_csv(file_path, delimiter=delimiter, encoding='utf-8-sig')
                # Check if we got multiple columns (successful delimiter detection)
                if len(df.columns) > 1:
                    return df
            except Exception:
                continue
        
        # Fallback: try default pandas detection
        try:
            return pd.read_csv(file_path, encoding='utf-8-sig')
        except Exception as e:
            raise CSVParseError(f"Could not read CSV with any common delimiter: {str(e)}")
    
    def _detect_columns(self, df: pd.DataFrame) -> Dict[str, str]:
        """
        Detect which columns contain which data.
        
        Returns dict mapping: {'date': 'Date', 'description': 'Description', ...}
        """
        column_map = {}
        
        # Normalize column names for comparison
        columns_lower = {col.lower().strip(): col for col in df.columns}
        
        # Find date column
        for pattern in self.DATE_COLUMNS:
            if pattern in columns_lower:
                column_map['date'] = columns_lower[pattern]
                break
        
        # Find description column
        for pattern in self.DESCRIPTION_COLUMNS:
            if pattern in columns_lower:
                column_map['description'] = columns_lower[pattern]
                break
        
        # Find amount column (single)
        for pattern in self.AMOUNT_COLUMNS:
            if pattern in columns_lower:
                column_map['amount'] = columns_lower[pattern]
                break
        
        # Find debit column
        for pattern in self.DEBIT_COLUMNS:
            if pattern in columns_lower:
                column_map['debit'] = columns_lower[pattern]
                break
        
        # Find credit column
        for pattern in self.CREDIT_COLUMNS:
            if pattern in columns_lower:
                column_map['credit'] = columns_lower[pattern]
                break
        
        # Find balance column (optional)
        for pattern in self.BALANCE_COLUMNS:
            if pattern in columns_lower:
                column_map['balance'] = columns_lower[pattern]
                break
        
        return column_map
    
    def _parse_row(self, row: pd.Series, column_map: Dict[str, str]) -> Optional[Dict]:
        """
        Parse a single row into a transaction.
        
        Returns None if row should be skipped.
        """
        # Extract date
        date_str = str(row[column_map['date']]).strip()
        if not date_str or date_str.lower() in ['nan', 'none', '']:
            return None
        
        try:
            parsed_date = self._parse_date(date_str)
        except ValueError as e:
            raise ValueError(f"Invalid date '{date_str}': {str(e)}")
        
        # Extract description
        description = str(row[column_map['description']]).strip()
        if not description or description.lower() in ['nan', 'none']:
            description = "Unknown Transaction"
        
        # Extract amount
        if column_map.get('amount'):
            # Single amount column
            amount = self._parse_amount(row[column_map['amount']])
        else:
            # Debit/Credit columns
            debit = self._parse_amount(row[column_map.get('debit', 'debit')]) if column_map.get('debit') else 0.0
            credit = self._parse_amount(row[column_map.get('credit', 'credit')]) if column_map.get('credit') else 0.0
            
            # Following ACCOUNTING STANDARDS from customer's perspective:
            # 
            # BANK ACCOUNT (Asset):
            # - Credit (deposits/income) = POSITIVE (increases asset)
            # - Debit (withdrawals/expenses) = NEGATIVE (decreases asset)
            # 
            # CREDIT CARD (Liability):
            # - Debit (payments) = POSITIVE (decreases liability) 
            # - Credit (charges) = NEGATIVE (increases liability)
            #
            # Summary: Money IN or Debt DOWN = POSITIVE
            #          Money OUT or Debt UP = NEGATIVE
            
            if credit != 0.0:
                amount = abs(credit)  # Credits are positive (deposits/income)
            elif debit != 0.0:
                amount = -abs(debit)  # Debits are negative (withdrawals/expenses)
            else:
                return None  # No transaction amount
        
        # Extract balance (optional)
        balance = None
        if column_map.get('balance'):
            try:
                balance = self._parse_amount(row[column_map['balance']])
            except ValueError:
                pass  # Balance is optional, skip if invalid
        
        return {
            'date': parsed_date,
            'description': description,
            'amount': amount,
            'balance': balance,
            'raw_data': row.to_dict()
        }
    
    def _parse_date(self, date_str: str) -> datetime.date:
        """
        Parse date string with flexible format detection.
        
        Supports: MM/DD/YYYY, DD/MM/YYYY, YYYY-MM-DD, DD-MM-YYYY, etc.
        """
        try:
            # Use dateutil parser for flexible parsing
            parsed = date_parser.parse(date_str, dayfirst=False)
            return parsed.date()
        except Exception:
            # Try with dayfirst=True for DD/MM/YYYY formats
            try:
                parsed = date_parser.parse(date_str, dayfirst=True)
                return parsed.date()
            except Exception as e:
                raise ValueError(f"Could not parse date: {str(e)}")
    
    def _parse_amount(self, amount_value) -> float:
        """
        Parse amount from various formats.
        
        Handles: 1234.56, (1234.56), -1234.56, $1,234.56, 1.234,56
        """
        if pd.isna(amount_value) or amount_value == '' or str(amount_value).strip() == '':
            return 0.0
        
        amount_str = str(amount_value).strip()
        
        # Remove currency symbols
        amount_str = re.sub(r'[$£€¥₹]', '', amount_str)
        
        # Remove spaces
        amount_str = amount_str.replace(' ', '')
        
        # Handle parentheses as negative (accounting format)
        is_negative = False
        if amount_str.startswith('(') and amount_str.endswith(')'):
            is_negative = True
            amount_str = amount_str[1:-1]
        
        # Handle comma as decimal separator (European format: 1.234,56)
        # vs comma as thousands separator (US format: 1,234.56)
        if ',' in amount_str and '.' in amount_str:
            # Both present: last one is decimal separator
            if amount_str.rindex(',') > amount_str.rindex('.'):
                # European: 1.234,56
                amount_str = amount_str.replace('.', '').replace(',', '.')
            else:
                # US: 1,234.56
                amount_str = amount_str.replace(',', '')
        elif ',' in amount_str:
            # Only comma: could be thousands or decimal
            # If there are digits after comma and they are 2 digits, it's decimal
            if re.search(r',\d{2}$', amount_str):
                amount_str = amount_str.replace(',', '.')
            else:
                amount_str = amount_str.replace(',', '')
        
        try:
            amount = float(amount_str)
            return -abs(amount) if is_negative else amount
        except ValueError as e:
            raise ValueError(f"Invalid amount format '{amount_value}': {str(e)}")

