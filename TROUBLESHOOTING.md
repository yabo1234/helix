# Troubleshooting: "localhost refused to connect"

## Common Causes and Solutions

### 1. **OPENAI_API_KEY Not Set**
The web interface requires the OPENAI_API_KEY environment variable to start.

**Solution:**
```bash
export OPENAI_API_KEY='your-api-key-here'
python3 web_interface.py
```

Or use the quick start script:
```bash
export OPENAI_API_KEY='your-api-key-here'
./start_web.sh
```

**Error Message to Look For:**
If you see "Configuration Error: OPENAI_API_KEY environment variable not set", the server won't start.

---

### 2. **Dependencies Not Installed**
Flask and other dependencies must be installed before running.

**Solution:**
```bash
pip install -r requirements.txt
python3 web_interface.py
```

Or use the quick start script which auto-installs:
```bash
./start_web.sh
```

**Error Message to Look For:**
- "Error: flask and flask-session packages not installed"
- "ModuleNotFoundError: No module named 'flask'"

---

### 3. **Port 5000 Already in Use**
Another application might be using port 5000.

**Check if port is in use:**
```bash
lsof -i :5000
# or
netstat -an | grep 5000
```

**Solution A - Use Different Port:**
Edit `web_interface.py` line 208:
```python
app.run(host='0.0.0.0', port=8000, debug=True)  # Changed from 5000 to 8000
```

Then access: http://localhost:8000

**Solution B - Kill Process on Port 5000:**
```bash
# Find process ID
lsof -ti :5000

# Kill it (replace PID with actual number)
kill -9 <PID>
```

---

### 4. **Server Crashed on Startup**
Check the terminal output for error messages.

**What to look for:**
- Python syntax errors
- Import errors
- Configuration errors

**Solution:**
Read the error message in the terminal carefully and address the specific issue.

---

### 5. **Firewall Blocking Connection**
Your firewall might be blocking localhost connections.

**Solution:**
- Temporarily disable firewall for testing
- Add exception for Python/Flask on port 5000

---

### 6. **Wrong URL**
Make sure you're using the correct URL format.

**Correct URLs:**
- http://localhost:5000 ✓
- http://127.0.0.1:5000 ✓

**Incorrect URLs:**
- localhost:5000 ✗ (missing http://)
- https://localhost:5000 ✗ (using https instead of http)

---

## Step-by-Step Debugging

### Step 1: Set API Key
```bash
export OPENAI_API_KEY='your-actual-api-key'
echo $OPENAI_API_KEY  # Verify it's set
```

### Step 2: Install Dependencies
```bash
cd /path/to/helix
pip install -r requirements.txt
```

### Step 3: Run the Server
```bash
python3 web_interface.py
```

### Step 4: Check Terminal Output
Look for:
```
============================================================
Triple Helix Innovation Chatbot - Web Interface
============================================================

Starting web server...
Open your browser and navigate to: http://localhost:5000

Press Ctrl+C to stop the server
============================================================

 * Serving Flask app 'web_interface'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://YOUR_IP:5000
```

If you see this, the server is running correctly!

### Step 5: Open Browser
Navigate to: http://localhost:5000

---

## Quick Verification Commands

Run these commands to verify your setup:

```bash
# 1. Check Python version
python3 --version

# 2. Check if in correct directory
pwd
ls -la | grep web_interface.py

# 3. Verify API key is set
echo "API Key set: $([[ -n $OPENAI_API_KEY ]] && echo YES || echo NO)"

# 4. Check dependencies
python3 -c "import flask, flask_session; print('Dependencies OK')"

# 5. Check port availability
lsof -i :5000 || echo "Port 5000 is free"
```

---

## Alternative: Use a Different Port

If nothing else works, try a different port:

**Method 1: Edit web_interface.py**
```python
# Line 208
app.run(host='0.0.0.0', port=8080, debug=True)
```

**Method 2: Environment Variable**
```bash
export FLASK_RUN_PORT=8080
python3 web_interface.py
```

Then access: http://localhost:8080

---

## Still Having Issues?

1. **Check the full terminal output** - Copy any error messages
2. **Verify your environment** - Make sure you're in the correct directory
3. **Try the CLI version** - Run `python3 triple-helix-innovation.py` to verify OpenAI integration works
4. **Check system resources** - Ensure you have enough memory and disk space

---

## Example of Successful Startup

When everything works correctly, you should see:

**Terminal:**
```
============================================================
Triple Helix Innovation Chatbot - Quick Start
============================================================

✓ Dependencies already installed

============================================================
Starting Web Interface...
============================================================

📱 Open your browser and navigate to:
   http://localhost:5000

Press Ctrl+C to stop the server

============================================================

============================================================
Triple Helix Innovation Chatbot - Web Interface
============================================================

Starting web server...
Open your browser and navigate to: http://localhost:5000

Press Ctrl+C to stop the server
============================================================

 * Serving Flask app 'web_interface'
 * Debug mode: on
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
```

**Browser:**
- Purple gradient interface
- "🔬 Triple Helix Innovation Chatbot" header
- Input field with "Ask about Triple Helix Innovation..." placeholder
- "Send" button

---

**Last Updated:** January 2026  
**For More Help:** See WEB_INTERFACE_GUIDE.md
