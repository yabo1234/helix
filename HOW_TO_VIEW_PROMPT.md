# How to Get the Rewritten LLM Prompt

This guide explains how to view and access the system prompt used by the Economics Chat Bot.

## Quick Answer

The Economics Chat Bot uses a specialized system prompt that instructs the AI to provide economics-focused responses with citations. You can view this prompt in three ways:

## Method 1: Display in Terminal (Recommended)

Simply run:

```bash
python3 economics.py --show-prompt
```

**Output:**
```
======================================================================
ECONOMICS CHATBOT SYSTEM PROMPT
======================================================================

You are an expert economics assistant specializing in macroeconomics. 
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
into your responses when applicable, and cite them appropriately.

======================================================================
```

**Advantages:**
- No dependencies required (works without OpenAI API key)
- Quick and easy
- See the exact prompt immediately

## Method 2: Export to File

To save the prompt to a file:

```bash
python3 economics.py --export-prompt my_prompt.txt
```

This creates a text file containing the system prompt.

**Advantages:**
- Keep a copy for reference
- Compare different versions
- Share with team members
- Edit and customize

**Example usage:**
```bash
# Export the prompt
python3 economics.py --export-prompt economics_prompt.txt

# View the file
cat economics_prompt.txt

# Edit in your favorite editor
nano economics_prompt.txt
```

## Method 3: Programmatic Access

If you want to access the prompt from Python code:

```python
from economics import SYSTEM_PROMPT

# Access the prompt directly
print(SYSTEM_PROMPT)

# Or use it in your own code
my_custom_prompt = SYSTEM_PROMPT + "\nAdditional instructions..."
```

**Or through the chatbot instance:**

```python
from economics import EconomicsChatBot

# Note: This requires OpenAI API key and dependencies
chatbot = EconomicsChatBot()
prompt = chatbot.get_system_prompt()
print(prompt)
```

## Understanding the Prompt

The system prompt defines:

1. **Role**: Expert economics assistant specializing in macroeconomics
2. **Response Requirements**:
   - Consistent with macroeconomic research
   - Supported by citations
   - Accurate and evidence-based
   - Clear and educational

3. **Citation Format**: Examples of how to reference sources
4. **PDF Integration**: Instructions for incorporating user-provided documents

## Customizing the Prompt

To customize the prompt:

1. Export it to a file:
   ```bash
   python3 economics.py --export-prompt my_custom_prompt.txt
   ```

2. Edit the file with your changes

3. Modify the `SYSTEM_PROMPT` variable in `economics.py` (line ~15)

4. Test your changes:
   ```bash
   python3 economics.py --show-prompt
   ```

## Command-Line Options Summary

```bash
# Show help and all options
python3 economics.py --help

# View the prompt
python3 economics.py --show-prompt

# Export the prompt
python3 economics.py --export-prompt filename.txt

# Run the chatbot normally
python3 economics.py
```

## FAQ

**Q: Do I need an OpenAI API key to view the prompt?**  
A: No! The `--show-prompt` and `--export-prompt` options work without any API key or dependencies.

**Q: Where is the prompt defined in the code?**  
A: The prompt is defined as `SYSTEM_PROMPT` at the top of `economics.py` (around line 15).

**Q: Can I modify the prompt?**  
A: Yes! Edit the `SYSTEM_PROMPT` variable in `economics.py` to customize the behavior.

**Q: How does the chatbot use this prompt?**  
A: The prompt is sent to OpenAI's API as a "system" message that sets the context for all conversations.

**Q: Does the prompt change during a conversation?**  
A: The system prompt stays the same, but PDF context may be added for the first few messages.

## Related Documentation

- [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) - Full usage examples
- [ECONOMICS_README.md](ECONOMICS_README.md) - Complete chatbot documentation
- [README.md](README.md) - Repository overview

## Getting Help

If you have questions about the prompt or need help customizing it:

1. Review the current prompt: `python3 economics.py --show-prompt`
2. Check the documentation: `ECONOMICS_README.md`
3. Look at examples: `USAGE_EXAMPLES.md`
4. Examine the code: `economics.py` (lines 15-28)
