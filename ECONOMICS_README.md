# Economics Chat Bot

An AI-powered economics discussion assistant that uses OpenAI's API to provide expert guidance on macroeconomic topics, with support for PDF document context and conversation logging.

## Features

- **Economics Expertise**: Specialized in macroeconomics with citation requirements
- **PDF Context**: Load up to 10 PDF documents to provide additional context
- **Citation-Based Responses**: All answers reference academic papers, reports, or established economic facts
- **Conversation Logging**: Automatically saves timestamped transcripts of all conversations
- **Command-Line Interface**: Simple text-based interaction

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

## Usage

Run the chatbot from the command line:

```bash
python3 economics.py
```

Or make it executable and run directly:
```bash
chmod +x economics.py
./economics.py
```

## How It Works

1. **Startup**: The bot welcomes you with "welcome to the economics chat bot"
2. **PDF Context**: You'll be prompted to optionally provide a directory containing PDF files (up to 10 will be loaded)
3. **Chat**: Type your economics questions and press Enter
4. **Exit**: Type 'exit', 'quit', or 'bye' to end the conversation
5. **Logging**: The conversation is automatically saved to a timestamped file (e.g., `economics_chat_log_20251230_120000.txt`)

## System Prompt

The chatbot is configured with a specialized prompt that ensures:
- All responses are consistent with macroeconomic research
- Citations are provided for facts, papers, and reports
- Responses are accurate and evidence-based
- PDF context is incorporated when provided

## Requirements

- Python 3.6+
- OpenAI API key
- Internet connection for API calls

## Example Session

```
welcome to the economics chat bot
======================================================================

Would you like to include PDF documents for context?
Enter the path to a directory containing PDFs (or press Enter to skip): ./research_papers

Loading 3 PDF file(s)...
  Reading: keynes_general_theory.pdf
  Reading: imf_outlook_2023.pdf
  Reading: fed_policy_report.pdf

Loaded 3 PDF document(s) for context.

You can now chat with the economics bot. Type 'exit', 'quit', or 'bye' to end the conversation.

You: What is the role of monetary policy in controlling inflation?

Bot: Monetary policy plays a crucial role in controlling inflation through several mechanisms...
[Response includes citations and references to provided PDFs]

You: exit

Bot: Thank you for using the Economics Chat Bot. Goodbye!

Conversation log saved to: economics_chat_log_20251230_120000.txt
```

## License

This project is part of the helix repository.
