# Financial Assistant

A local web-based financial analysis application for tracking, categorizing, and analyzing bank and credit card transactions.

## Features

- **CSV Import**: Upload bank statements and automatically parse transactions
- **Multi-Account Support**: Track multiple bank and credit card accounts
- **Smart Categorization**: Automatic transaction categorization with machine learning from your corrections
- **Budgeting**: Set and track budgets per category
- **Savings Goals**: Define and monitor progress toward financial goals
- **Reports & Visualizations**: Interactive charts and financial insights
- **Financial Health Dashboard**: Comprehensive overview of your financial status

## Technology Stack

- **Backend**: Python 3.11+ with Flask
- **Database**: SQLite3
- **Data Processing**: pandas
- **Frontend**: HTML5, CSS3, JavaScript with Chart.js
- **Testing**: pytest

## Installation

### Prerequisites

- Python 3.11 or higher
- Git
- Modern web browser

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/saeid-h/financial-assistant.git
   cd financial-assistant
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   ```

3. **Activate virtual environment**
   
   On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```
   
   On Windows:
   ```bash
   venv\Scripts\activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Initialize database**
   ```bash
   python src/init_db.py
   ```

6. **Run the application**
   
   **Option A - Using the start script (Recommended):**
   ```bash
   ./start.sh
   ```
   
   **Option B - Manual start:**
   ```bash
   source venv/bin/activate
   python src/app.py
   ```

7. **Access the application**
   
   Once the server is running, open your web browser and navigate to:
   ```
   http://localhost:5001
   ```
   
   You should see the Flask server output in terminal:
   ```
   Server running at: http://localhost:5001
   Press CTRL+C to stop the server
   ```
   
   **Note**: Using port 5001 because port 5000 is used by macOS AirPlay on Mac systems.
   
   **Important**: The Flask application must be running for the browser to access it!

## Supported CSV Formats

The application supports various CSV formats from different financial institutions:

### Format 1: Standard Bank Statement
```csv
Date,Description,Amount
10/14/2025,Grocery Store,-45.50
10/15/2025,Salary Deposit,2500.00
```

### Format 2: Debit/Credit Columns
```csv
Date,Merchant,Debit,Credit
10/14/2025,Grocery Store,45.50,
10/15/2025,Salary,0,2500.00
```

### Format 3: Credit Card Statement (with Status and Member Name)
```csv
Status,Date,Description,Debit,Credit,Member Name
Posted,10/14/2025,Amazon Purchase,125.50,,John Doe
Posted,10/15/2025,Payment - Thank You,,500.00,John Doe
```

### Supported Features:
- ✅ **Delimiters**: Comma, semicolon, tab, pipe
- ✅ **Date Formats**: MM/DD/YYYY, DD/MM/YYYY, YYYY-MM-DD, DD-MM-YYYY
- ✅ **Currency Symbols**: $, £, €, ¥, ₹
- ✅ **Number Formats**: 
  - US format: 1,234.56
  - European format: 1.234,56
- ✅ **Negative Amounts**: -100.00 or (100.00)
- ✅ **Optional Columns**: Status, Member Name, Balance, Card Number (automatically ignored)

### Column Name Variations (case-insensitive):
- **Date**: Date, Transaction Date, Posting Date, Trans Date
- **Description**: Description, Merchant, Payee, Details, Memo
- **Amount**: Amount, Transaction Amount, Value
- **Debit**: Debit, Withdrawal, Withdrawals, Paid Out
- **Credit**: Credit, Deposit, Deposits, Paid In

## Project Structure

```
financial-assistant/
├── docs/               # Documentation
├── src/                # Source code
│   ├── app.py         # Flask application entry point
│   ├── models/        # Database models
│   ├── services/      # Business logic
│   ├── routes/        # API endpoints
│   ├── static/        # Frontend assets (CSS, JS)
│   └── templates/     # HTML templates
├── data/              # Data storage (YYYY/MM structure)
├── tests/             # Test suite
├── config/            # Configuration files
├── logs/              # Application logs
└── requirements.txt   # Python dependencies
```

## Usage

### Importing Statements

1. Navigate to the "Import" page
2. Select your bank account
3. Upload CSV file
4. Review and confirm imported transactions

### Categorization

- New transactions are automatically categorized based on learned patterns
- Confirm or correct categories for new merchants
- System learns from your corrections for future imports

### Reports

- View monthly spending by category
- Analyze trends over time
- Compare year-over-year performance
- Export data for external analysis

### Budgeting

- Create monthly or yearly budgets per category
- Track spending against budgets
- Receive alerts when approaching limits

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/unit/test_models.py
```

### Code Style

This project follows Google Python Style Guide. Ensure your code:
- Uses meaningful variable names
- Includes docstrings for functions and classes
- Has appropriate comments for complex logic
- Passes all linter checks

### Contributing

1. Create a feature branch: `git checkout -b feature/description`
2. Make your changes
3. Write/update tests
4. Ensure tests pass: `pytest`
5. Commit with clear message: `git commit -m "task-id description"`
6. Push and create pull request

## Testing

The project uses pytest for testing:
- **Unit tests**: Test individual functions and methods
- **Integration tests**: Test component interactions
- **Target coverage**: 80%+

## Documentation

- **Project Specification**: `.cursor/rules/spec.mdc`
- **PBI Documentation**: `docs/delivery/backlog.md`
- **Git Rules**: `docs/technical/git-rules.md`
- **Technical Docs**: `docs/technical/`

## Troubleshooting

### Cannot Access localhost:5001 (or 5000)

**Problem**: Browser shows "access denied" or "connection refused"

**Solution 1**: The Flask application is not running. You must start it first:
```bash
cd /path/to/financial-assistant
./start.sh
```

Keep the terminal window open while using the application. You should see:
```
============================================================
Financial Assistant - Starting...
============================================================
Server running at: http://localhost:5001
```

Then access http://localhost:5001 in your browser.

**Solution 2**: Port 5000 is used by macOS AirPlay
On macOS, port 5000 is often occupied by the AirPlay Receiver service. This app now uses port 5001 instead. If you need to use port 5000:
1. Go to System Settings > General > AirDrop & Handoff
2. Disable "AirPlay Receiver"
3. Edit `src/app.py` and change port back to 5000

### Virtual Environment Issues

If you encounter issues with the virtual environment:
```bash
# Deactivate current environment
deactivate

# Remove old environment
rm -rf venv

# Create new environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Database Issues

If the database becomes corrupted:
```bash
# Backup your data first!
python src/init_db.py --reset
```

### Port Already in Use

The app now uses port 5001 by default to avoid conflicts with macOS AirPlay on port 5000. If you need a different port, edit `src/app.py` and change the port number in the `app.run()` call.

## License

MIT License - see [LICENSE](LICENSE) file for details.

This is open source software. You are free to use, modify, and distribute it.

## Privacy

All data is stored locally on your machine. No data is transmitted to external servers. Your financial information remains private and secure.

## Support

For questions or issues, refer to the documentation in the `docs/` directory or contact the project owner.

---

**Version**: 1.0.0  
**Author**: Saeed Hoss  
**Repository**: https://github.com/saeid-h/financial-assistant  
**Last Updated**: 2025-10-19

