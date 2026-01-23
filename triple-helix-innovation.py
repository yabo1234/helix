#!/usr/bin/env python3
"""
Triple Helix Innovation Chatbot

A chatbot specifically designed to interact with users on the topic of 
Triple Helix Innovation, integrating with OpenAI's GPT model and 
supporting PDF context inclusion.
"""

import os
import sys
from datetime import datetime
from pathlib import Path
import json

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


class TripleHelixChatbot:
    """
    A chatbot for discussing Triple Helix Innovation with PDF context support.
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
        self.conversation_history = []
        self.pdf_context = ""
        self.transcript_file = None
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
    
    def create_transcript_file(self):
        """Create a timestamped transcript file for logging chat interactions."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"chat_transcript_{timestamp}.txt"
        try:
            self.transcript_file = open(filename, 'w', encoding='utf-8')
            self.log_to_transcript(f"Chat session started at {datetime.now().isoformat()}\n")
            self.log_to_transcript("="*60 + "\n")
            return filename
        except Exception as e:
            print(f"Warning: Could not create transcript file: {e}")
            return None
    
    def log_to_transcript(self, message):
        """Log a message to the transcript file."""
        if self.transcript_file:
            try:
                self.transcript_file.write(message)
                self.transcript_file.flush()
            except Exception as e:
                print(f"Warning: Could not write to transcript: {e}")
    
    def extract_text_from_pdf(self, pdf_path):
        """
        Extract text content from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text as a string
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page_num, page in enumerate(pdf_reader.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text += f"\n--- Page {page_num + 1} ---\n{page_text}"
                    except Exception as e:
                        print(f"Warning: Could not extract text from page {page_num + 1}: {e}")
                return text
        except Exception as e:
            print(f"Error reading PDF {pdf_path}: {e}")
            return ""
    
    def load_pdf_context(self):
        """
        Prompt user for a directory containing PDF files and load their content.
        Supports up to 2 PDF files.
        """
        while True:
            pdf_dir = input("\nEnter the path to a directory containing up to 2 PDF files (or press Enter to skip): ").strip()
            
            if not pdf_dir:
                print("Skipping PDF context loading.")
                return
            
            pdf_path = Path(pdf_dir)
            
            if not pdf_path.exists():
                print(f"Error: Directory '{pdf_dir}' does not exist. Please try again.")
                continue
            
            if not pdf_path.is_dir():
                print(f"Error: '{pdf_dir}' is not a directory. Please try again.")
                continue
            
            # Find PDF files
            pdf_files = list(pdf_path.glob("*.pdf"))
            
            if not pdf_files:
                print(f"Warning: No PDF files found in '{pdf_dir}'.")
                retry = input("Would you like to try another directory? (y/n): ").strip().lower()
                if retry != 'y':
                    return
                continue
            
            if len(pdf_files) > 2:
                print(f"Warning: Found {len(pdf_files)} PDF files. Only the first 2 will be processed.")
                pdf_files = pdf_files[:2]
            
            # Extract text from PDFs
            print(f"\nLoading {len(pdf_files)} PDF file(s)...")
            all_text = []
            
            for pdf_file in pdf_files:
                print(f"  - Processing {pdf_file.name}...")
                text = self.extract_text_from_pdf(pdf_file)
                if text:
                    all_text.append(f"\n=== Content from {pdf_file.name} ===\n{text}")
                else:
                    print(f"    Warning: No text extracted from {pdf_file.name}")
            
            if all_text:
                self.pdf_context = "\n".join(all_text)
                print(f"\nSuccessfully loaded context from {len(all_text)} PDF file(s).")
                self.log_to_transcript(f"\nPDF Context Loaded from directory: {pdf_dir}\n")
                self.log_to_transcript(f"Files processed: {', '.join([f.name for f in pdf_files])}\n")
                self.log_to_transcript("="*60 + "\n")
            else:
                print("Warning: No text could be extracted from any PDF files.")
            
            break
    
    def build_prompt_with_context(self, user_message):
        """
        Build the complete prompt including system context and PDF content.
        
        Args:
            user_message: The user's message
            
        Returns:
            List of messages for the OpenAI API
        """
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Add PDF context if available
        if self.pdf_context:
            context_message = (
                "The following PDF documents have been provided as additional context "
                "for this conversation. Please refer to them when relevant:\n\n"
                f"{self.pdf_context}"
            )
            messages.append({"role": "system", "content": context_message})
        
        # Add conversation history
        messages.extend(self.conversation_history)
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        return messages
    
    def get_chatbot_response(self, user_message):
        """
        Get a response from the OpenAI API.
        
        Args:
            user_message: The user's message
            
        Returns:
            The chatbot's response
        """
        try:
            messages = self.build_prompt_with_context(user_message)
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            assistant_message = response.choices[0].message.content
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": assistant_message})
            
            # Keep conversation history manageable (last 10 messages)
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
            
            return assistant_message
            
        except openai.error.AuthenticationError:
            return "Error: Invalid OpenAI API key. Please check your OPENAI_API_KEY environment variable."
        except openai.error.RateLimitError:
            return "Error: OpenAI API rate limit exceeded. Please try again later."
        except openai.error.APIError as e:
            return f"Error: OpenAI API error: {str(e)}"
        except Exception as e:
            return f"Error: An unexpected error occurred: {str(e)}"
    
    def run(self):
        """Run the interactive chatbot session."""
        print("="*60)
        print("Welcome to the Triple Helix Innovation chatbot.")
        print("="*60)
        
        # Create transcript file
        transcript_filename = self.create_transcript_file()
        if transcript_filename:
            print(f"Chat transcript will be saved to: {transcript_filename}")
        
        # Log welcome message
        self.log_to_transcript("Welcome to the Triple Helix Innovation chatbot.\n")
        
        # Load PDF context
        self.load_pdf_context()
        
        print("\nYou can now start chatting. Type 'quit', 'exit', or 'bye' to end the session.")
        print("-"*60)
        
        while True:
            try:
                # Get user input
                user_input = input("\nYou: ").strip()
                
                if not user_input:
                    continue
                
                # Log user input
                self.log_to_transcript(f"\nUser: {user_input}\n")
                
                # Check for exit commands
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("\nThank you for using the Triple Helix Innovation chatbot. Goodbye!")
                    self.log_to_transcript("\n" + "="*60 + "\n")
                    self.log_to_transcript(f"Chat session ended at {datetime.now().isoformat()}\n")
                    break
                
                # Get and display chatbot response
                response = self.get_chatbot_response(user_input)
                print(f"\nChatbot: {response}")
                
                # Log chatbot response
                self.log_to_transcript(f"\nChatbot: {response}\n")
                
            except KeyboardInterrupt:
                print("\n\nSession interrupted by user. Goodbye!")
                self.log_to_transcript("\n" + "="*60 + "\n")
                self.log_to_transcript(f"Chat session interrupted at {datetime.now().isoformat()}\n")
                break
            except Exception as e:
                print(f"\nError: {e}")
                self.log_to_transcript(f"\nError: {e}\n")
    
    def __del__(self):
        """Cleanup: close transcript file."""
        if self.transcript_file:
            try:
                self.transcript_file.close()
            except (OSError, Exception):
                pass


def main():
    """Main entry point for the chatbot."""
    try:
        chatbot = TripleHelixChatbot()
        chatbot.run()
    except ValueError as e:
        print(f"\nConfiguration Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nFatal Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
