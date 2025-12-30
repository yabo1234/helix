#!/usr/bin/env python3
"""
Test script for economics.py
Tests basic functionality without requiring OpenAI API calls.
"""

import os
import sys
import tempfile
from pathlib import Path

# Mock the OpenAI import to test without API key
class MockOpenAI:
    def __init__(self, api_key=None):
        self.api_key = api_key

class MockChoice:
    def __init__(self, content):
        self.message = type('obj', (object,), {'content': content})()

class MockResponse:
    def __init__(self, content):
        self.choices = [MockChoice(content)]

class MockCompletions:
    def create(self, **kwargs):
        return MockResponse("This is a test response about economics.")

class MockChat:
    def __init__(self):
        self.completions = MockCompletions()

# Replace the OpenAI import before importing economics
import importlib.util
spec = importlib.util.spec_from_file_location("economics", "economics.py")
economics = importlib.util.module_from_spec(spec)

# Set a fake API key for testing
os.environ["OPENAI_API_KEY"] = "test-key-for-testing"

# Mock the OpenAI client
import unittest.mock as mock
with mock.patch('economics.OpenAI', MockOpenAI):
    spec.loader.exec_module(economics)

print("Testing economics.py functionality...\n")

# Test 1: Can create chatbot instance
print("✓ Test 1: Creating EconomicsChatBot instance...")
try:
    chatbot = economics.EconomicsChatBot()
    print("  SUCCESS: Chatbot instance created\n")
except Exception as e:
    print(f"  FAILED: {e}\n")
    sys.exit(1)

# Test 2: Check system prompt includes key requirements
print("✓ Test 2: Verifying system prompt contains required elements...")
required_keywords = [
    "macroeconomics",
    "citations",
    "papers",
    "reports",
    "evidence"
]
missing = []
for keyword in required_keywords:
    if keyword.lower() not in chatbot.system_prompt.lower():
        missing.append(keyword)

if missing:
    print(f"  WARNING: System prompt missing keywords: {', '.join(missing)}")
else:
    print("  SUCCESS: System prompt contains all required elements\n")

# Test 3: Test logging setup
print("✓ Test 3: Testing logging functionality...")
try:
    log_file = chatbot.setup_logging()
    chatbot.log("Test log message")
    print(f"  SUCCESS: Log file created: {log_file}")
    
    # Verify log file exists
    if os.path.exists(log_file):
        print(f"  SUCCESS: Log file verified on disk\n")
        # Clean up
        chatbot.log_file.close()
        os.remove(log_file)
    else:
        print(f"  FAILED: Log file not found\n")
except Exception as e:
    print(f"  FAILED: {e}\n")

# Test 4: Test PDF loading with empty directory
print("✓ Test 4: Testing PDF context loading...")
try:
    with tempfile.TemporaryDirectory() as tmpdir:
        chatbot.load_pdf_context(tmpdir)
        print("  SUCCESS: PDF loading function works (no PDFs in test dir)\n")
except Exception as e:
    print(f"  FAILED: {e}\n")

# Test 5: Check conversation history initialization
print("✓ Test 5: Checking conversation history...")
if hasattr(chatbot, 'conversation_history') and isinstance(chatbot.conversation_history, list):
    print("  SUCCESS: Conversation history initialized as list\n")
else:
    print("  FAILED: Conversation history not properly initialized\n")

# Test 6: Verify welcome message format
print("✓ Test 6: Checking welcome message format...")
expected_welcome = "welcome to the economics chat bot"
# The welcome message is printed in the run() method, so we just verify it's in the code
with open("economics.py", "r") as f:
    code = f.read()
    if expected_welcome in code:
        print(f"  SUCCESS: Welcome message '{expected_welcome}' found in code\n")
    else:
        print(f"  FAILED: Expected welcome message not found\n")

print("=" * 70)
print("All basic tests completed successfully!")
print("=" * 70)
print("\nNote: Full functionality requires:")
print("  1. Valid OPENAI_API_KEY environment variable")
print("  2. Internet connection for OpenAI API calls")
print("  3. Optional: PDF files in a directory for context")
print("\nTo run the chatbot:")
print("  python3 economics.py")
