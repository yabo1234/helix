#!/usr/bin/env python3
"""
Web interface for Triple Helix Innovation Chatbot

A Flask-based web application that provides a browser interface for the 
Triple Helix Innovation chatbot.
"""

import os
import sys
from datetime import datetime
from pathlib import Path
import json

try:
    from flask import Flask, render_template, request, jsonify, session
    from flask_session import Session
except ImportError:
    print("Error: flask and flask-session packages not installed.")
    print("Please run: pip install flask flask-session")
    sys.exit(1)

try:
    import openai
except ImportError:
    print("Error: openai package not installed. Please run: pip install openai")
    sys.exit(1)

try:
    import PyPDF2
except ImportError:
    print("Error: PyPDF2 package not installed. Please run: pip install PyPDF2")
    sys.exit(1)


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


class WebTripleHelixChatbot:
    """
    Web-enabled version of Triple Helix Innovation chatbot.
    """
    
    def __init__(self):
        """Initialize the chatbot with necessary configurations."""
        self.api_key = os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable not set. "
                "Please set it with your OpenAI API key."
            )
        
        openai.api_key = self.api_key
        self.system_prompt = (
            "You are an expert assistant on Triple Helix Innovation research and policy analysis. "
            "Triple Helix Innovation refers to the collaborative innovation model "
            "involving three key institutional spheres: university, industry, and government. "
            "You can discuss Triple Helix Innovation research, its applications, and related policy questions. "
            "When discussing policy matters, consider the interplay between academia, industry, and government. "
            "Provide evidence-based insights and, when applicable, cite relevant facts, papers, or reports. "
            "You can address contemporary issues (such as AI regulation, deepfakes, innovation governance) "
            "through the lens of Triple Helix collaboration. "
            "Be specific, accurate, and thoughtful in your responses."
        )
    
    def get_response(self, user_message, conversation_history, pdf_context=""):
        """
        Get a response from the OpenAI API.
        
        Args:
            user_message: The user's message
            conversation_history: List of previous messages
            pdf_context: Optional PDF context
            
        Returns:
            The chatbot's response
        """
        try:
            messages = [{"role": "system", "content": self.system_prompt}]
            
            # Add PDF context if available
            if pdf_context:
                context_message = (
                    "The following PDF documents have been provided as additional context "
                    "for this conversation. Please refer to them when relevant:\n\n"
                    f"{pdf_context}"
                )
                messages.append({"role": "system", "content": context_message})
            
            # Add conversation history
            messages.extend(conversation_history)
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            assistant_message = response.choices[0].message.content
            return assistant_message
            
        except openai.error.AuthenticationError:
            return "Error: Invalid OpenAI API key. Please check your OPENAI_API_KEY environment variable."
        except openai.error.RateLimitError:
            return "Error: OpenAI API rate limit exceeded. Please try again later."
        except openai.error.APIError as e:
            return f"Error: OpenAI API error: {str(e)}"
        except Exception as e:
            return f"Error: An unexpected error occurred: {str(e)}"


# Initialize chatbot
try:
    chatbot = WebTripleHelixChatbot()
except ValueError as e:
    print(f"\nConfiguration Error: {e}")
    print("\nTo run the web interface, you need to set your OpenAI API key:")
    print("  export OPENAI_API_KEY='your-api-key-here'")
    print("\nThen run: python3 web_interface.py")
    sys.exit(1)


@app.route('/')
def index():
    """Render the main chat interface."""
    # Initialize session if needed
    if 'conversation_history' not in session:
        session['conversation_history'] = []
    if 'pdf_context' not in session:
        session['pdf_context'] = ""
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages."""
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    # Get conversation history from session
    conversation_history = session.get('conversation_history', [])
    pdf_context = session.get('pdf_context', "")
    
    # Get response from chatbot
    response = chatbot.get_response(user_message, conversation_history, pdf_context)
    
    # Update conversation history
    conversation_history.append({"role": "user", "content": user_message})
    conversation_history.append({"role": "assistant", "content": response})
    
    # Keep only last 10 messages
    if len(conversation_history) > 10:
        conversation_history = conversation_history[-10:]
    
    session['conversation_history'] = conversation_history
    
    return jsonify({
        'response': response,
        'timestamp': datetime.now().isoformat()
    })


@app.route('/clear', methods=['POST'])
def clear():
    """Clear conversation history."""
    session['conversation_history'] = []
    return jsonify({'status': 'success'})


@app.route('/upload_pdf_text', methods=['POST'])
def upload_pdf_text():
    """Handle PDF context upload (text content)."""
    data = request.json
    pdf_text = data.get('pdf_text', '')
    
    if pdf_text:
        session['pdf_context'] = pdf_text
        return jsonify({'status': 'success', 'message': 'PDF context loaded'})
    else:
        return jsonify({'status': 'error', 'message': 'No PDF text provided'}), 400


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})


if __name__ == '__main__':
    print("="*60)
    print("Triple Helix Innovation Chatbot - Web Interface")
    print("="*60)
    print("\nStarting web server...")
    print("Open your browser and navigate to: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
