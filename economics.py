#!/usr/bin/env python3
"""
Economics Chat Bot - An AI-powered economics discussion assistant.

This script creates an interactive chatbot that discusses economics topics
using OpenAI's API, with support for PDF document context and conversation logging.
"""

import os
import sys
from datetime import datetime
from pathlib import Path
import json

try:
    from openai import OpenAI
except ImportError:
    print("Error: openai package not installed.")
    print("Please install it with: pip install openai")
    sys.exit(1)

try:
    import PyPDF2
except ImportError:
    print("Error: PyPDF2 package not installed.")
    print("Please install it with: pip install PyPDF2")
    sys.exit(1)


class EconomicsChatBot:
    """A chatbot specialized in economics discussions with PDF context support."""
    
    def __init__(self):
        """Initialize the chatbot with OpenAI client and conversation history."""
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            print("Error: OPENAI_API_KEY environment variable not set.")
            print("Please set it with: export OPENAI_API_KEY='your-api-key'")
            sys.exit(1)
        
        self.client = OpenAI(api_key=self.api_key)
        self.conversation_history = []
        self.pdf_context = ""
        self.log_file = None
        
        # System prompt for economics focus
        self.system_prompt = """You are an expert economics assistant specializing in macroeconomics. 
Your responses must be:
1. Consistent with established macroeconomic research and economic theory
2. Supported by citations to specific papers, reports, or well-known economic facts
3. Accurate and evidence-based
4. Clear and educational

When providing information, always cite your sources. For example:
- Reference specific economic papers (e.g., "According to Keynes (1936) in 'The General Theory'...")
- Cite reports from organizations (e.g., "The IMF World Economic Outlook (2023) indicates...")
- Reference well-established economic facts with their sources

If the user has provided PDF documents, incorporate relevant information from those documents 
into your responses when applicable, and cite them appropriately."""

    def setup_logging(self):
        """Create a timestamped log file for the conversation."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"economics_chat_log_{timestamp}.txt"
        self.log_file = open(log_filename, "w", encoding="utf-8")
        self.log(f"Economics Chat Bot Session Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        self.log("=" * 70 + "\n\n")
        return log_filename

    def log(self, message):
        """Write a message to the log file."""
        if self.log_file:
            self.log_file.write(message)
            self.log_file.flush()

    def extract_text_from_pdf(self, pdf_path):
        """Extract text content from a PDF file."""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                # Limit to first 10 pages to avoid context length issues
                max_pages = min(len(pdf_reader.pages), 10)
                for page_num in range(max_pages):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            print(f"Warning: Could not read PDF '{pdf_path}': {str(e)}")
            return ""

    def load_pdf_context(self, directory_path):
        """Load and process PDF files from the specified directory."""
        if not directory_path:
            return
        
        pdf_dir = Path(directory_path)
        if not pdf_dir.exists() or not pdf_dir.is_dir():
            print(f"Warning: Directory '{directory_path}' does not exist or is not a directory.")
            return
        
        pdf_files = list(pdf_dir.glob("*.pdf"))[:10]  # Limit to 10 PDFs
        
        if not pdf_files:
            print(f"No PDF files found in '{directory_path}'.")
            return
        
        print(f"\nLoading {len(pdf_files)} PDF file(s)...")
        all_text = []
        
        for pdf_file in pdf_files:
            print(f"  Reading: {pdf_file.name}")
            text = self.extract_text_from_pdf(pdf_file)
            if text:
                all_text.append(f"\n--- Content from {pdf_file.name} ---\n{text}")
        
        if all_text:
            self.pdf_context = "\n".join(all_text)
            context_summary = f"\nLoaded {len(pdf_files)} PDF document(s) for context.\n"
            print(context_summary)
            self.log(context_summary)

    def get_response(self, user_message):
        """Get a response from OpenAI API."""
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Prepare messages for API call
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Add PDF context if available (only on first message or when relevant)
        if self.pdf_context and len(self.conversation_history) <= 2:
            messages.append({
                "role": "system",
                "content": f"Additional context from provided documents:\n{self.pdf_context[:8000]}"  # Limit context size
            })
        
        # Add conversation history
        messages.extend(self.conversation_history)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=800
            )
            
            assistant_message = response.choices[0].message.content
            
            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
            
        except Exception as e:
            return f"Error communicating with OpenAI API: {str(e)}"

    def run(self):
        """Run the main chat loop."""
        # Setup logging
        log_filename = self.setup_logging()
        print(f"Logging conversation to: {log_filename}\n")
        
        # Welcome message
        welcome_message = "welcome to the economics chat bot"
        print("=" * 70)
        print(welcome_message)
        print("=" * 70)
        self.log(welcome_message + "\n")
        self.log("=" * 70 + "\n\n")
        
        # Ask for PDF directory
        print("\nWould you like to include PDF documents for context?")
        pdf_dir = input("Enter the path to a directory containing PDFs (or press Enter to skip): ").strip()
        self.log(f"PDF Directory Input: {pdf_dir if pdf_dir else 'None'}\n\n")
        
        if pdf_dir:
            self.load_pdf_context(pdf_dir)
        
        print("\nYou can now chat with the economics bot. Type 'exit', 'quit', or 'bye' to end the conversation.\n")
        
        # Main chat loop
        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                # Log user input
                self.log(f"[{datetime.now().strftime('%H:%M:%S')}] You: {user_input}\n")
                
                # Check for exit commands
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    farewell = "Thank you for using the Economics Chat Bot. Goodbye!"
                    print(f"\nBot: {farewell}")
                    self.log(f"\n{farewell}\n")
                    break
                
                # Get and display response
                response = self.get_response(user_input)
                print(f"\nBot: {response}\n")
                
                # Log bot response
                self.log(f"[{datetime.now().strftime('%H:%M:%S')}] Bot: {response}\n\n")
                
            except KeyboardInterrupt:
                print("\n\nChat interrupted by user.")
                self.log("\n\nChat interrupted by user.\n")
                break
            except Exception as e:
                print(f"\nAn error occurred: {str(e)}")
                self.log(f"\nError: {str(e)}\n")
        
        # Cleanup
        if self.log_file:
            self.log(f"\n\nSession Ended: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            self.log("=" * 70 + "\n")
            self.log_file.close()
            print(f"\nConversation log saved to: {log_filename}")


def main():
    """Main entry point for the economics chatbot."""
    chatbot = EconomicsChatBot()
    chatbot.run()


if __name__ == "__main__":
    main()
