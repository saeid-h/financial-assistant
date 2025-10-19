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
   git clone <repository-url>
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
   ```bash
   python src/app.py
   ```

7. **Access the application**
   
   Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

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

If port 5000 is already in use:
```bash
# Run on different port
python src/app.py --port 5001
```

## License

This is a personal financial management tool. All rights reserved.

## Privacy

All data is stored locally on your machine. No data is transmitted to external servers. Your financial information remains private and secure.

## Support

For questions or issues, refer to the documentation in the `docs/` directory or contact the project owner.

---

**Version**: 1.0.0  
**Last Updated**: 2025-10-19

