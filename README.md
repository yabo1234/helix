# Triple Helix Innovation Chatbot

An AI-powered chatbot specifically designed to interact with users on the topic of Triple Helix Innovation, integrating with OpenAI's GPT model and supporting PDF context inclusion.

## Features

1. **Welcome Message**: Greets users with "Welcome to the Triple Helix Innovation chatbot."
2. **OpenAI Integration**: Uses GPT-3.5-turbo with custom context emphasizing Triple Helix Innovation research
3. **PDF Context Support**: 
   - Prompts users to provide a directory containing up to 2 PDF files
   - Extracts and includes PDF text content in the chatbot context
4. **Interactive CLI**: Text-only command prompt interface for seamless interaction
5. **Chat Logging**: Automatically saves all interactions to timestamped transcript files
6. **Robust Error Handling**: Comprehensive error handling throughout the application

## Requirements

- Python 3.7+
- OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yabo1234/helix.git
cd helix
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set your OpenAI API key:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

## Usage

Run the chatbot:
```bash
python3 triple-helix-innovation.py
```

### Workflow

1. The chatbot displays a welcome message
2. You're prompted to enter a directory path containing PDF files (optional - press Enter to skip)
3. If provided, the chatbot loads and extracts text from up to 2 PDF files
4. Start chatting about Triple Helix Innovation topics
5. Type 'quit', 'exit', or 'bye' to end the session
6. All interactions are automatically saved to a timestamped transcript file

### Example Session

```
============================================================
Welcome to the Triple Helix Innovation chatbot.
============================================================
Chat transcript will be saved to: chat_transcript_20260123_105246.txt

Enter the path to a directory containing up to 2 PDF files (or press Enter to skip): /path/to/pdfs

Loading 2 PDF file(s)...
  - Processing research_paper.pdf...
  - Processing report.pdf...

Successfully loaded context from 2 PDF file(s).

You can now start chatting. Type 'quit', 'exit', or 'bye' to end the session.
------------------------------------------------------------

You: What is the Triple Helix model?

Chatbot: The Triple Helix model describes the collaborative innovation...
```

## Triple Helix Innovation Context

The chatbot is configured with expert knowledge on Triple Helix Innovation, which refers to the collaborative innovation model involving three key institutional spheres:

1. **University** - Knowledge production and education
2. **Industry** - Economic development and innovation
3. **Government** - Regulatory and policy framework

The chatbot can discuss:
- Triple Helix Innovation research and theory
- Policy questions related to innovation, technology governance, and regulation
- Contemporary issues (AI, deepfakes, innovation policy) through the Triple Helix lens
- The interplay between academia, industry, and government in addressing modern challenges

Responses are evidence-based and include citations when applicable.

## File Structure

```
helix/
├── triple-helix-innovation.py    # Main chatbot script
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git ignore rules
└── README.md                      # This file
```

## Dependencies

- `openai==0.28.1` - OpenAI Python library
- `PyPDF2==3.0.1` - PDF text extraction

## License

This project promotes knowledge economy innovation.
