# Economics Chat Bot - Usage Examples

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Your OpenAI API Key
```bash
export OPENAI_API_KEY='sk-your-actual-api-key-here'
```

### 3. Run the Chatbot
```bash
python3 economics.py
```

## Example Usage Session

```
Logging conversation to: economics_chat_log_20251230_120000.txt

======================================================================
welcome to the economics chat bot
======================================================================

Would you like to include PDF documents for context?
Enter the path to a directory containing PDFs (or press Enter to skip): ./research_papers

Loading 3 PDF file(s)...
  Reading: keynes_1936.pdf
  Reading: imf_outlook_2023.pdf
  Reading: fed_minutes_2024.pdf

Loaded 3 PDF document(s) for context.

You can now chat with the economics bot. Type 'exit', 'quit', or 'bye' to end the conversation.

You: What causes inflation?

Bot: Inflation is caused by several factors according to macroeconomic theory:

1. **Demand-Pull Inflation**: When aggregate demand exceeds aggregate supply, 
   prices rise. Keynes (1936) in "The General Theory of Employment, Interest 
   and Money" discussed how excess demand can lead to price increases.

2. **Cost-Push Inflation**: When production costs increase (wages, raw materials), 
   producers pass these costs to consumers. According to the IMF World Economic 
   Outlook (2023), supply chain disruptions have been a major source of recent 
   cost-push inflation.

3. **Monetary Inflation**: The Federal Reserve's research (Fed Minutes, 2024) 
   indicates that excessive money supply growth can lead to inflation, consistent 
   with Milton Friedman's monetarist theory.

Citations:
- Keynes, J.M. (1936). The General Theory of Employment, Interest and Money
- IMF World Economic Outlook (2023)
- Federal Reserve Meeting Minutes (2024)

You: What is the Phillips Curve?

Bot: The Phillips Curve represents the inverse relationship between unemployment 
and inflation, first documented by A.W. Phillips (1958) in his study "The Relation 
between Unemployment and the Rate of Change of Money Wage Rates in the United 
Kingdom, 1861-1957."

The curve suggests that:
- Lower unemployment → Higher inflation
- Higher unemployment → Lower inflation

However, the relationship has evolved. The "stagflation" of the 1970s challenged 
the traditional Phillips Curve, leading to the development of the "expectations-
augmented Phillips Curve" by Friedman (1968) and Phelps (1967).

Modern macroeconomic research, including papers from the Federal Reserve Bank 
(2024), shows that the relationship has weakened in recent decades, possibly due 
to better-anchored inflation expectations and changes in labor market dynamics.

Citations:
- Phillips, A.W. (1958). Economica, 25(100), 283-299
- Friedman, M. (1968). "The Role of Monetary Policy"
- Phelps, E.S. (1967). "Phillips Curves, Expectations of Inflation..."

You: exit

Bot: Thank you for using the Economics Chat Bot. Goodbye!

Conversation log saved to: economics_chat_log_20251230_120000.txt
```

## Features Demonstrated

✅ **Welcome Message**: "welcome to the economics chat bot"
✅ **PDF Context**: Loads up to 10 PDFs from a directory
✅ **Economics Focus**: Specialized in macroeconomics
✅ **Citations**: Every response includes proper academic citations
✅ **Command-Line Interface**: Simple text input/output
✅ **Timestamped Logging**: Conversation saved with timestamp

## Log File Format

The conversation is automatically saved to a file like `economics_chat_log_20251230_120000.txt`:

```
Economics Chat Bot Session Started: 2025-12-30 12:00:00
======================================================================

welcome to the economics chat bot
======================================================================

PDF Directory Input: ./research_papers

[12:00:15] You: What causes inflation?
[12:00:18] Bot: Inflation is caused by several factors...

[12:01:30] You: What is the Phillips Curve?
[12:01:35] Bot: The Phillips Curve represents...

[12:02:45] You: exit

Thank you for using the Economics Chat Bot. Goodbye!

Session Ended: 2025-12-30 12:02:45
======================================================================
```

## Troubleshooting

### "OPENAI_API_KEY environment variable not set"
Set your API key:
```bash
export OPENAI_API_KEY='your-key-here'
```

### "openai package not installed"
Install dependencies:
```bash
pip install -r requirements.txt
```

### PDF files not loading
- Ensure the directory path is correct
- Check that PDFs are readable
- Maximum 10 PDFs will be loaded
- Each PDF limited to first 10 pages

## Customization

You can modify `economics.py` to:
- Change the OpenAI model (default: gpt-3.5-turbo)
- Adjust response temperature (default: 0.7)
- Modify max tokens (default: 800)
- Customize the system prompt
- Change PDF page limits
