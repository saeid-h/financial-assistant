# Financial Assistant - Quick Start Guide

## How to Run the Application

### The Issue You Experienced

When you tried to access `http://localhost:5000` in your browser and got "access denied", it's because **the Flask web server wasn't running yet**.

Think of it like this:
- The Flask application is like a restaurant
- Your browser is a customer
- If the restaurant isn't open (server not running), customers can't come in!

### Solution: Start the Flask Server First

**Step 1: Open Terminal**

Navigate to your project directory:
```bash
cd /Volumes/SSD/projects/financial-assistant
```

**Step 2: Start the Application**

Use the start script:
```bash
./start.sh
```

You should see output like this:
```
Starting Financial Assistant...
================================
Starting Flask server...
Access the application at: http://localhost:5001
Note: Using port 5001 (port 5000 is used by macOS AirPlay)
Press CTRL+C to stop the server
================================

============================================================
Financial Assistant - Starting...
============================================================
Server running at: http://localhost:5001
Database location: /Volumes/SSD/projects/financial-assistant/data/financial_assistant.db
Press CTRL+C to stop the server
============================================================
NOTE: Using port 5001 because port 5000 is used by macOS AirPlay

 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5001
```

**Step 3: Open Your Browser**

Now that the server is running, open your browser and go to:
```
http://localhost:5001
```

You should see the Financial Assistant home page! 🎉

**Step 4: Stop the Server**

When you're done, go back to the terminal and press:
```
CTRL + C
```

## Important Notes

1. **Keep the Terminal Open**: The terminal window where Flask is running must stay open. If you close it, the server stops.

2. **One Terminal for Server**: Use a separate terminal window if you need to run other commands while the server is running.

3. **Server Must Be Running**: Every time you want to use the app in your browser, make sure the Flask server is running first.

## Alternative: Manual Start

If you prefer to start manually:

```bash
# Step 1: Activate virtual environment
source venv/bin/activate

# Step 2: Start Flask
python src/app.py
```

## Common Issues

### Port 5000 vs 5001 - Why the Change?

**macOS Issue**: On Mac, port 5000 is often used by the AirPlay Receiver service. That's why you got "access denied"!

**Solution**: This app now uses **port 5001** instead.

If you still see "Address already in use" for port 5001:
```bash
# Find what's using port 5001
lsof -ti:5001

# Kill that process
kill -9 $(lsof -ti:5001)

# Then start again
./start.sh
```

To use port 5000 (if you really want to):
1. Disable AirPlay Receiver in System Settings
2. Edit `src/app.py` and change `port=5001` to `port=5000`

### Virtual Environment Not Activated

If you see "ModuleNotFoundError":
```bash
source venv/bin/activate
python src/app.py
```

### Database Not Found

If you see "Database not found":
```bash
python src/init_db.py
```

## Development Workflow

1. **Morning**: Start the Flask server (`./start.sh`)
2. **Work**: Keep browser tab open to http://localhost:5001
3. **Make Changes**: Edit code, refresh browser to see changes
4. **Evening**: Stop server (CTRL+C in terminal)

## Testing While Server is Running

To run tests, open a **new terminal window**:
```bash
cd /Volumes/SSD/projects/financial-assistant
source venv/bin/activate
pytest -v
```

Keep your original terminal with Flask running!

---

**Next Steps:**
- Start the server using `./start.sh`
- Access http://localhost:5001 in your browser
- Begin using the Financial Assistant!

**Remember**: Port 5001, not 5000 (macOS AirPlay uses 5000)

