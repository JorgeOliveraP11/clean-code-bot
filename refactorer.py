import os
import click
import re
from typing import Optional
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# --- Security & Sanitization ---
def sanitize_input(code_content: str) -> str:
    """
    Basic sanitization to prevent prompt injection or malicious file execution.
    """
    # Remove common shell injection patterns or suspicious LLM override commands
    forbidden_patterns = [r"ignore previous instructions", r"system command", r"os.system"]
    for pattern in forbidden_patterns:
        if re.search(pattern, code_content, re.IGNORECASE):
            raise ValueError("Potential malicious input detected in code file.")
    return code_content.strip()

# --- The Prompt Template (CoT) ---
COT_PROMPT_TEMPLATE = """
You are an expert Senior Software Architect. Your task is to refactor the following code snippet.
Follow these steps strictly:

1. ANALYZE: Understand the logic and identify violations of SOLID principles or PEP8.
2. PLAN: Describe how you will decouple classes, improve naming, and add documentation.
3. EXECUTE: Provide ONLY the final, refactored Python code.

RULES:
- Apply SOLID principles (Single Responsibility, Open/Closed, etc.).
- Include comprehensive Google-style or JSDoc docstrings.
- Ensure the code is production-ready and type-hinted.

CODE TO REFACTOR:
---
{original_code}
---

FINAL REFACTORED CODE:
"""

@click.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--output', '-o', default='refactored_code.py', help='Output file path.')
@click.option('--provider', '-p', default='openai', help='LLM provider: openai or groq.')
def main(input_file: str, output: str, provider: str):
    """Refactor dirty code into SOLID, documented code."""
    
    click.echo(f"🚀 Reading {input_file}...")
    
    with open(input_file, 'r') as f:
        raw_code = f.read()

    try:
        clean_input = sanitize_input(raw_code)
    except ValueError as e:
        click.echo(f"❌ Security Error: {e}")
        return

    # API Configuration
    if provider == "groq":
        api_key = os.getenv("GROQ_API_KEY")
        base_url = "https://api.groq.com/openai/v1"
        model = "llama3-8b-8192" # High-speed inference
    else:
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = None
        model = "gpt-4-turbo"

    client = OpenAI(api_key=api_key, base_url=base_url)

    click.echo(f"🧠 Analyzing code using {provider}...")

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that refactors code to follow SOLID principles."},
                {"role": "user", "content": COT_PROMPT_TEMPLATE.format(original_code=clean_input)}
            ],
            temperature=0.2 # Lower temperature for consistency
        )

        refactored_code = response.choices[0].message.content

        # Clean up Markdown artifacts if the LLM includes them
        if "```python" in refactored_code:
            refactored_code = refactored_code.split("```python")[1].split("```")[0]

        with open(output, 'w') as f:
            f.write(refactored_code.strip())

        click.echo(f"✅ Refactored code saved to: {output}")

    except Exception as e:
        click.echo(f"❌ Error during API call: {e}")

if __name__ == '__main__':
    main()
